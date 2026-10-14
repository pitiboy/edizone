#!/usr/bin/env python3
"""Merge GeoShop contour lines onto the surveyor (geodeta) CAD drawing."""

from __future__ import annotations

import math
from pathlib import Path

import ezdxf
import numpy as np
import rasterio
from ezdxf import bbox
from ezdxf.addons import Importer
from ezdxf.addons.drawing import Frontend, RenderContext, config
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
from shapely.geometry import LineString, box

WORK = Path("/workspace/gis-work")
GEODETA_SRC = WORK / "geodeta-meres.dxf"
GEOSHOP_SRC = WORK / "geoshop-szintvonal.pdf"
ORTHO = WORK / "ortofoto"

OUT_DXF = WORK / "geodeta-szintvonal-osszefuzve.dxf"
OUT_PNG = WORK / "geodeta-szintvonal-osszefuzve.png"
OUT_ORTHO_PNG = WORK / "ortofoto-geodeta-szintvonal.png"
OUT_ORTHO_TIF = WORK / "ortofoto-geodeta-szintvonal.tif"


def geodeta_extent(msp, pad_m: float = 2.0):
    ext = bbox.extents(msp)
    return box(
        ext.extmin.x - pad_m,
        ext.extmin.y - pad_m,
        ext.extmax.x + pad_m,
        ext.extmax.y + pad_m,
    )


def polyline_xy(entity) -> list[tuple[float, float]]:
    return [(float(p[0]), float(p[1])) for p in entity.get_points("xy")]


def entity_intersects(entity, region) -> bool:
    if entity.dxftype() != "LWPOLYLINE":
        return False
    pts = polyline_xy(entity)
    if len(pts) < 2:
        return False
    return LineString(pts).intersects(region)


def ensure_layers(doc, layer_names: list[str]) -> None:
    for name in layer_names:
        if name not in doc.layers:
            doc.layers.add(name)


def copy_lwpolyline(src, msp) -> None:
    points = list(src.get_points(format="xyseb"))
    msp.add_lwpolyline(
        points,
        dxfattribs={
            "layer": src.dxf.layer,
            "color": src.dxf.color,
            "linetype": src.dxf.linetype,
        },
    )


def merge_dxf() -> tuple[Path, box]:
    geodeta_src = ezdxf.readfile(str(GEODETA_SRC))
    geoshop = ezdxf.readfile(str(GEOSHOP_SRC))
    geodeta = ezdxf.new("R2010", setup=True)
    importer = Importer(geodeta_src, geodeta)
    importer.import_modelspace()
    block_names = [b.name for b in geodeta_src.blocks if not b.name.startswith("*")]
    if block_names:
        importer.import_blocks(block_names)
    importer.import_tables()
    importer.finalize()

    msp = geodeta.modelspace()
    region = geodeta_extent(msp)

    ensure_layers(
        geodeta,
        ["ALAPSZINTVONAL", "FELEZOSZINTVONAL", "FOSZINTVONAL"],
    )

    added = 0
    for entity in geoshop.modelspace():
        if entity_intersects(entity, region):
            copy_lwpolyline(entity, msp)
            added += 1

    geodeta.saveas(str(OUT_DXF))
    print(f"Merged DXF: {OUT_DXF} (+{added} contour polylines)")
    return OUT_DXF, region


def render_cad_png(dxf_path: Path, out_png: Path, region: box) -> None:
    doc = ezdxf.readfile(str(dxf_path))
    msp = doc.modelspace()

    fig = plt.figure(figsize=(12, 12), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1])
    ctx = RenderContext(doc)
    cfg = config.Configuration(
        background_policy=config.BackgroundPolicy.WHITE,
        color_policy=config.ColorPolicy.COLOR,
    )
    backend = MatplotlibBackend(ax)
    Frontend(ctx, backend, config=cfg).draw_layout(msp, finalize=True)

    ax.set_xlim(region.bounds[0], region.bounds[2])
    ax.set_ylim(region.bounds[1], region.bounds[3])
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")
    fig.savefig(out_png, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)
    print(f"CAD preview PNG: {out_png}")


def collect_contour_segments(doc, region: box) -> list[tuple[list[tuple[float, float]], str]]:
    segments: list[tuple[list[tuple[float, float]], str]] = []
    layer_colors = {
        "FOSZINTVONAL": "#8B0000",
        "FELEZOSZINTVONAL": "#CC5500",
        "ALAPSZINTVONAL": "#2E8B57",
    }
    for entity in doc.modelspace():
        if entity.dxftype() != "LWPOLYLINE":
            continue
        if not entity_intersects(entity, region):
            continue
        layer = entity.dxf.layer
        segments.append((polyline_xy(entity), layer_colors.get(layer, "#00FFFF")))
    return segments


def collect_vector_segments(doc, region: box) -> list[tuple[tuple[float, float], tuple[float, float]]]:
    lines: list[tuple[tuple[float, float], tuple[float, float]]] = []
    msp = doc.modelspace()
    for entity in msp:
        if entity.dxftype() == "LINE":
            lines.append(
                (
                    (float(entity.dxf.start.x), float(entity.dxf.start.y)),
                    (float(entity.dxf.end.x), float(entity.dxf.end.y)),
                )
            )
        elif entity.dxftype() == "LWPOLYLINE":
            pts = polyline_xy(entity)
            for a, b in zip(pts, pts[1:]):
                lines.append((a, b))
            if entity.closed and len(pts) > 2:
                lines.append((pts[-1], pts[0]))
    return lines


def world_to_pixel(xs: np.ndarray, ys: np.ndarray, transform):
    inv = ~transform
    cols, rows = inv * (xs, ys)
    return cols, rows


def render_ortho_composite(region: box) -> None:
    merged = ezdxf.readfile(str(OUT_DXF))
    contour_segments = collect_contour_segments(merged, region)
    vector_lines = collect_vector_segments(merged, region)

    with rasterio.open(ORTHO) as ds:
        win = rasterio.windows.from_bounds(*region.bounds, transform=ds.transform)
        win = win.round_offsets().round_lengths()
        data = ds.read(indexes=(1, 2, 3), window=win, boundless=True, fill_value=0)
        transform = rasterio.windows.transform(win, ds.transform)
        height, width = data.shape[1], data.shape[2]

    rgb = np.moveaxis(data, 0, -1)

    fig, ax = plt.subplots(figsize=(14, 14), dpi=200)
    ax.imshow(rgb, extent=(region.bounds[0], region.bounds[2], region.bounds[1], region.bounds[3]), origin="upper")

    if vector_lines:
        ax.add_collection(
            LineCollection(vector_lines, colors="#000000", linewidths=1.2, alpha=0.95, zorder=3)
        )

    for pts, color in contour_segments:
        ax.add_collection(
            LineCollection([pts], colors=color, linewidths=0.9, alpha=0.85, zorder=4)
        )

    ax.set_xlim(region.bounds[0], region.bounds[2])
    ax.set_ylim(region.bounds[1], region.bounds[3])
    ax.set_aspect("equal")
    ax.axis("off")
    fig.savefig(OUT_ORTHO_PNG, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)
    print(f"Orthophoto composite PNG: {OUT_ORTHO_PNG}")

    # GeoTIFF export (same pixel grid as orthophoto window)
    from rasterio.transform import from_bounds

    out_transform = from_bounds(*region.bounds, width=width, height=height)
    profile = {
        "driver": "GTiff",
        "height": height,
        "width": width,
        "count": 3,
        "dtype": "uint8",
        "transform": out_transform,
        "crs": merged.header.get("$INSUNITS", None),
    }
    with rasterio.open(ORTHO) as ds:
        profile["crs"] = ds.crs

    # Burn vectors/contours onto RGB copy using matplotlib figure renderer is heavy;
    # save georeferenced crop for GIS use and keep annotated PNG for visual check.
    with rasterio.open(OUT_ORTHO_TIF, "w", **profile) as dst:
        dst.write(data)
    print(f"Orthophoto georeferenced crop (base RGB): {OUT_ORTHO_TIF}")


def main() -> None:
    _, region = merge_dxf()
    render_cad_png(OUT_DXF, OUT_PNG, region)
    render_ortho_composite(region)


if __name__ == "__main__":
    main()
