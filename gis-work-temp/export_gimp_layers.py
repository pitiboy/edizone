#!/usr/bin/env python3
"""Export aligned Google base layer + transparent geodeta overlay + GIMP project."""

from __future__ import annotations

import io
import struct
import zipfile
import zlib
from pathlib import Path

import ezdxf
import numpy as np
from ezdxf.addons.drawing import Frontend, RenderContext, config
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from matplotlib import pyplot as plt
from PIL import Image

from google_maps_composite import (
    BUILDING_FOOTPRINT_SHIFT_EAST_M,
    BUILDING_FOOTPRINT_SHIFT_SOUTH_M,
    OUT_DXF,
    TO_WGS84,
    apply_eov_shift,
    fetch_google_mosaic,
    pick_zoom,
    plot_boundary_region,
    region_with_context,
    warp_to_eov,
)
from merge_contours import collect_contour_segments, collect_vector_segments
from shapely.geometry import box

WORK = Path("/workspace/gis-work")
OUT_GOOGLE = WORK / "googlemaps.png"
OUT_OVERLAY = WORK / "geodeta-szintvonal-transparent.png"
OUT_XCF = WORK / "geodeta-google-gimp.xcf"
OUT_ORA = WORK / "geodeta-google-gimp.ora"
OUT_COMPOSITE = WORK / "googlemaps-geodeta-szintvonal.png"
RESOLUTION = 0.35


def build_google_layer(view_region: box) -> np.ndarray:
    minx, miny, maxx, maxy = view_region.bounds
    corners = [(minx, miny), (minx, maxy), (maxx, miny), (maxx, maxy)]
    lons, lats = zip(*(TO_WGS84.transform(x, y) for x, y in corners))
    region_wgs84 = box(min(lons), min(lats), max(lons), max(lats))
    zoom = pick_zoom(region_wgs84)
    google_rgb, google_transform = fetch_google_mosaic(region_wgs84, zoom)
    google_eov, _ = warp_to_eov(google_rgb, google_transform, view_region, resolution=RESOLUTION)
    google_eov = apply_eov_shift(
        google_eov,
        east_m=BUILDING_FOOTPRINT_SHIFT_EAST_M,
        south_m=BUILDING_FOOTPRINT_SHIFT_SOUTH_M,
        resolution=RESOLUTION,
    )
    return np.moveaxis(google_eov, 0, -1).astype(np.uint8)


def render_overlay_rgba(view_region: box, dxf_path: Path) -> np.ndarray:
    doc = ezdxf.readfile(str(dxf_path))
    msp = doc.modelspace()
    plot_region = plot_boundary_region(msp, pad_m=2.0)

    width = int(round((view_region.bounds[2] - view_region.bounds[0]) / RESOLUTION))
    height = int(round((view_region.bounds[3] - view_region.bounds[1]) / RESOLUTION))
    dpi = 100
    fig = plt.figure(figsize=(width / dpi, height / dpi), dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor((0, 0, 0, 0))
    fig.patch.set_alpha(0.0)

    ctx = RenderContext(doc)
    cfg = config.Configuration(
        background_policy=config.BackgroundPolicy.CUSTOM,
        custom_bg_color="#00000000",
        color_policy=config.ColorPolicy.COLOR,
    )
    backend = MatplotlibBackend(ax)
    Frontend(ctx, backend, config=cfg).draw_layout(msp, finalize=True)

    ax.set_xlim(view_region.bounds[0], view_region.bounds[2])
    ax.set_ylim(view_region.bounds[1], view_region.bounds[3])
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")

    buf = io.BytesIO()
    fig.savefig(buf, format="png", transparent=True, dpi=dpi, pad_inches=0)
    plt.close(fig)
    buf.seek(0)
    rgba = np.array(Image.open(buf).convert("RGBA"))
    if rgba.shape[0] != height or rgba.shape[1] != width:
        rgba = np.array(Image.fromarray(rgba).resize((width, height), Image.Resampling.LANCZOS))
    return rgba


def save_png(path: Path, arr: np.ndarray) -> None:
    Image.fromarray(arr).save(path)


def compose_preview(google: np.ndarray, overlay: np.ndarray) -> np.ndarray:
    base = google.astype(np.float32)
    alpha = overlay[..., 3:4].astype(np.float32) / 255.0
    rgb = overlay[..., :3].astype(np.float32)
    out = base * (1.0 - alpha) + rgb * alpha
    return np.clip(out, 0, 255).astype(np.uint8)


def write_ora(path: Path, google: np.ndarray, overlay: np.ndarray) -> None:
    h, w = google.shape[:2]
    stack = f"""<?xml version="1.0" encoding="UTF-8"?>
<image w="{w}" h="{h}">
  <stack>
    <layer name="googlemaps" src="data/googlemaps.png" x="0" y="0" opacity="1.0"/>
    <layer name="geodeta-szintvonal" src="data/geodeta-szintvonal-transparent.png" x="0" y="0" opacity="1.0"/>
  </stack>
</image>
"""
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_STORED) as zf:
        zf.writestr("mimetype", "image/openraster")
        zf.writestr("stack.xml", stack)
        gbuf = io.BytesIO()
        Image.fromarray(google).save(gbuf, format="PNG")
        zf.writestr("data/googlemaps.png", gbuf.getvalue())
        obuf = io.BytesIO()
        Image.fromarray(overlay).save(obuf, format="PNG")
        zf.writestr("data/geodeta-szintvonal-transparent.png", obuf.getvalue())


def _write_xcf_string(data: bytearray, value: str) -> None:
    data.extend(value.encode("utf-8"))
    data.append(0)
    pad = (4 - (len(value) + 1) % 4) % 4
    data.extend(b"\x00" * pad)


def _write_xcf_property_list(data: bytearray, props: list[tuple[int, bytes]]) -> None:
    for prop_type, payload in props:
        data.extend(struct.pack(">I", prop_type))
        data.extend(struct.pack(">I", len(payload)))
        data.extend(payload)
        pad = (4 - len(payload) % 4) % 4
        data.extend(b"\x00" * pad)
    data.extend(struct.pack(">I", 0))


def _write_xcf_channel(data: bytearray, pixels: np.ndarray) -> None:
    h, w = pixels.shape
    _write_xcf_property_list(
        data,
        [
            (0x0101, struct.pack(">I", w)),  # WIDTH
            (0x0102, struct.pack(">I", h)),  # HEIGHT
        ],
    )
    data.extend(struct.pack(">I", 1))  # COMPRESSION: RLE
    for row in pixels:
        raw = row.astype(np.uint8).tobytes()
        rle = bytearray()
        i = 0
        while i < len(raw):
            chunk = raw[i : i + 126]
            rle.append(len(chunk))
            rle.extend(chunk)
            i += 126
        rle.append(0)
        compressed = zlib.compress(bytes(rle), level=9)
        data.extend(struct.pack(">I", len(compressed)))
        data.extend(compressed)


def write_xcf(path: Path, google: np.ndarray, overlay: np.ndarray) -> None:
    """Minimal GIMP XCF (v11) export with two RGBA layers."""
    h, w = google.shape[:2]
    over = overlay
    if over.shape[:2] != (h, w):
        over = np.array(Image.fromarray(over).resize((w, h), Image.Resampling.LANCZOS))

    data = bytearray()
    data.extend(b"gimp xcf v011")
    data.extend(b"\x00" * 3)
    data.extend(struct.pack(">I", w))
    data.extend(struct.pack(">I", h))
    data.extend(struct.pack(">I", 0))  # base_type RGB
    _write_xcf_property_list(data, [(0x0301, struct.pack(">f", 300.0))])  # RESOLUTION

    def write_layer(name: str, rgba: np.ndarray) -> None:
        _write_xcf_property_list(
            data,
            [
                (0x0101, struct.pack(">I", w)),
                (0x0102, struct.pack(">I", h)),
            ],
        )
        _write_xcf_string(data, name)
        data.extend(struct.pack(">I", 40))  # layer flags: visible
        data.extend(struct.pack(">I", 0))  # no alpha lock
        data.extend(struct.pack(">I", w))
        data.extend(struct.pack(">I", h))
        data.extend(struct.pack(">I", 0))  # layer type RGBA
        data.extend(struct.pack(">I", 0))  # no mask
        data.extend(struct.pack(">I", 4))  # channels
        for idx in range(4):
            data.extend(struct.pack(">I", idx))  # R,G,B,A
            _write_xcf_channel(data, rgba[..., idx])
        data.extend(struct.pack(">I", 0))  # end layer

    write_layer("googlemaps", np.dstack([google, np.full((h, w), 255, dtype=np.uint8)]))
    write_layer("geodeta-szintvonal", over)
    data.extend(struct.pack(">I", 0))  # end layers
    data.extend(struct.pack(">I", 0))  # end channels
    path.write_bytes(data)


def main() -> None:
    merged = ezdxf.readfile(str(OUT_DXF))
    view_region = region_with_context(plot_boundary_region(merged.modelspace(), 2.0), pad_m=45.0)

    google = build_google_layer(view_region)
    overlay = render_overlay_rgba(view_region, OUT_DXF)
    if google.shape[:2] != overlay.shape[:2]:
        overlay = np.array(
            Image.fromarray(overlay).resize((google.shape[1], google.shape[0]), Image.Resampling.LANCZOS)
        )

    save_png(OUT_GOOGLE, google)
    save_png(OUT_OVERLAY, overlay)
    save_png(OUT_COMPOSITE, compose_preview(google, overlay))
    write_ora(OUT_ORA, google, overlay)
    write_xcf(OUT_XCF, google, overlay)

    print(f"Google base: {OUT_GOOGLE} ({google.shape[1]}x{google.shape[0]})")
    print(f"Transparent overlay: {OUT_OVERLAY}")
    print(f"GIMP XCF: {OUT_XCF}")
    print(f"OpenRaster backup: {OUT_ORA}")
    print(f"Preview composite: {OUT_COMPOSITE}")
    print(
        "Alignment on Google layer: "
        f"E+{BUILDING_FOOTPRINT_SHIFT_EAST_M:.1f} m, S+{BUILDING_FOOTPRINT_SHIFT_SOUTH_M:.1f} m"
    )


if __name__ == "__main__":
    main()
