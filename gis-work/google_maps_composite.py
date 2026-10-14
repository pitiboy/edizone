#!/usr/bin/env python3
"""Overlay geodeta + contours on latest Google Maps satellite imagery."""

from __future__ import annotations

import io
import math
from pathlib import Path

import ezdxf
import mercantile
import numpy as np
import rasterio
import requests
from ezdxf import bbox
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
from PIL import Image
from pyproj import Transformer
from rasterio.crs import CRS
from rasterio.transform import from_bounds
from rasterio.warp import Resampling, reproject
from scipy.ndimage import shift as nd_shift
from shapely.geometry import LineString, box
from skimage.color import rgb2gray
from skimage.registration import phase_cross_correlation

from merge_contours import (
    OUT_DXF,
    ORTHO,
    collect_contour_segments,
    collect_vector_segments,
)

WORK = Path("/workspace/gis-work")
OUT_PNG = WORK / "googlemaps-geodeta-szintvonal.png"
OUT_TIF = WORK / "googlemaps-geodeta-szintvonal.tif"

GOOGLE_TILE_URL = "https://mt1.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}"
GOOGLE_MAPS_CENTER = (47.5494997, 18.2673182)  # lat, lon from user link
EOV = CRS.from_epsg(23700)
WEB_MERCATOR = CRS.from_epsg(3857)
TO_WGS84 = Transformer.from_crs(EOV, "EPSG:4326", always_xy=True)
TO_EOV = Transformer.from_crs("EPSG:4326", EOV, always_xy=True)


def plot_boundary_region(msp, pad_m: float = 2.0) -> box:
    xs: list[float] = []
    ys: list[float] = []
    for entity in msp:
        if entity.dxftype() != "LINE" or entity.dxf.layer != "Földrészlet határ":
            continue
        xs.extend([float(entity.dxf.start.x), float(entity.dxf.end.x)])
        ys.extend([float(entity.dxf.start.y), float(entity.dxf.end.y)])
    if not xs:
        ext = bbox.extents(msp)
        return box(ext.extmin.x - pad_m, ext.extmin.y - pad_m, ext.extmax.x + pad_m, ext.extmax.y + pad_m)
    return box(min(xs) - pad_m, min(ys) - pad_m, max(xs) + pad_m, max(ys) + pad_m)


def region_with_context(region: box, pad_m: float = 35.0) -> box:
    minx, miny, maxx, maxy = region.bounds
    return box(minx - pad_m, miny - pad_m, maxx + pad_m, maxy + pad_m)


def pick_zoom(region_wgs84: box) -> int:
    min_lon, min_lat, max_lon, max_lat = region_wgs84.bounds
    lat = (min_lat + max_lat) / 2.0
    width_m = (max_lon - min_lon) * 111_320 * math.cos(math.radians(lat))
    for z in range(21, 15, -1):
        m_per_px = 156543.03392 * math.cos(math.radians(lat)) / (2**z)
        if width_m / m_per_px <= 1024:
            return z
    return 17


def fetch_google_mosaic(region_wgs84: box, zoom: int) -> tuple[np.ndarray, rasterio.Affine]:
    min_lon, min_lat, max_lon, max_lat = region_wgs84.bounds
    tiles = list(mercantile.tiles(min_lon, min_lat, max_lon, max_lat, zooms=zoom))
    if not tiles:
        raise RuntimeError("No Google tiles found for region")

    xs = [t.x for t in tiles]
    ys = [t.y for t in tiles]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    tile_size = 256
    width = (max_x - min_x + 1) * tile_size
    height = (max_y - min_y + 1) * tile_size
    canvas = np.zeros((height, width, 3), dtype=np.uint8)

    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
        }
    )

    for tile in tiles:
        url = GOOGLE_TILE_URL.format(x=tile.x, y=tile.y, z=zoom)
        resp = session.get(url, timeout=30)
        resp.raise_for_status()
        img = np.array(Image.open(io.BytesIO(resp.content)).convert("RGB"))
        row = (tile.y - min_y) * tile_size
        col = (tile.x - min_x) * tile_size
        canvas[row : row + tile_size, col : col + tile_size] = img

    ul = mercantile.xy_bounds(mercantile.Tile(min_x, min_y, zoom))
    lr = mercantile.xy_bounds(mercantile.Tile(max_x, max_y, zoom))
    transform = from_bounds(ul.left, lr.bottom, lr.right, ul.top, width, height)
    return canvas, transform


def warp_to_eov(
    rgb: np.ndarray, src_transform, dst_region: box, resolution: float = 0.35
) -> tuple[np.ndarray, rasterio.Affine]:
    minx, miny, maxx, maxy = dst_region.bounds
    width = max(1, int(round((maxx - minx) / resolution)))
    height = max(1, int(round((maxy - miny) / resolution)))
    dst_transform = from_bounds(minx, miny, maxx, maxy, width, height)
    dst = np.zeros((3, height, width), dtype=np.uint8)

    for band in range(3):
        reproject(
            source=rgb[:, :, band],
            destination=dst[band],
            src_transform=src_transform,
            src_crs=WEB_MERCATOR,
            dst_transform=dst_transform,
            dst_crs=EOV,
            resampling=Resampling.bilinear,
        )
    return dst, dst_transform


def load_ortho_on_grid(region: box, shape: tuple[int, int], resolution: float) -> np.ndarray | None:
    if not ORTHO.exists():
        return None
    height, width = shape
    dst_transform = from_bounds(*region.bounds, width, height)
    dst = np.zeros((3, height, width), dtype=np.uint8)
    with rasterio.open(ORTHO) as ds:
        win = rasterio.windows.from_bounds(*region.bounds, transform=ds.transform)
        win = win.round_offsets().round_lengths()
        src = ds.read(indexes=(1, 2, 3), window=win, boundless=True, fill_value=0)
        src_transform = rasterio.windows.transform(win, ds.transform)
        for band in range(3):
            reproject(
                source=src[band],
                destination=dst[band],
                src_transform=src_transform,
                # Orthophoto grid uses EOV meter values even if CRS metadata is LOCAL_CS.
                src_crs=EOV,
                dst_transform=dst_transform,
                dst_crs=EOV,
                resampling=Resampling.bilinear,
            )
    return dst


def apply_pixel_shift(rgb: np.ndarray, col_shift: float, row_shift: float) -> np.ndarray:
    shifted = nd_shift(
        np.moveaxis(rgb, 0, -1),
        shift=(row_shift, col_shift, 0),
        order=1,
        mode="nearest",
    )
    return np.moveaxis(shifted, -1, 0).astype(np.uint8)


def anchor_shift_to_google_pin(plot_region: box) -> tuple[float, float]:
    px = (plot_region.bounds[0] + plot_region.bounds[2]) / 2
    py = (plot_region.bounds[1] + plot_region.bounds[3]) / 2
    g_lon, g_lat = GOOGLE_MAPS_CENTER[1], GOOGLE_MAPS_CENTER[0]
    gx, gy = TO_EOV.transform(g_lon, g_lat)
    return float(px - gx), float(py - gy)


def refine_with_orthophoto(
    google_rgb: np.ndarray,
    ortho_rgb: np.ndarray,
    resolution: float,
    max_shift_m: float = 8.0,
) -> tuple[np.ndarray, tuple[float, float]]:
    g = rgb2gray(np.moveaxis(google_rgb, 0, -1))
    o = rgb2gray(np.moveaxis(ortho_rgb, 0, -1))
    g = (g - g.mean()) / (g.std() + 1e-6)
    o = (o - o.mean()) / (o.std() + 1e-6)

    shift, error, _ = phase_cross_correlation(o, g, upsample_factor=10)
    row_shift, col_shift = shift
    max_px = max_shift_m / resolution
    if abs(col_shift) > max_px or abs(row_shift) > max_px or error > 0.35:
        return google_rgb, (0.0, 0.0)

    refined = apply_pixel_shift(google_rgb, float(col_shift), float(row_shift))
    return refined, (float(col_shift), float(row_shift))


def plot_composite(
    region: box,
    google_rgb: np.ndarray,
    vector_lines,
    contour_segments,
    alignment_note: str,
) -> None:
    rgb = np.moveaxis(google_rgb, 0, -1)
    fig, ax = plt.subplots(figsize=(14, 14), dpi=220)
    ax.imshow(
        rgb,
        extent=(region.bounds[0], region.bounds[2], region.bounds[1], region.bounds[3]),
        origin="upper",
    )

    if vector_lines:
        ax.add_collection(
            LineCollection(vector_lines, colors="#FFFFFF", linewidths=1.5, alpha=0.95, zorder=3)
        )
        ax.add_collection(
            LineCollection(vector_lines, colors="#111111", linewidths=0.9, alpha=0.95, zorder=4)
        )

    for pts, color in contour_segments:
        ax.add_collection(
            LineCollection([pts], colors=color, linewidths=1.0, alpha=0.9, zorder=5)
        )

    ax.set_xlim(region.bounds[0], region.bounds[2])
    ax.set_ylim(region.bounds[1], region.bounds[3])
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(f"Google Maps műhold + geodéta + szintvonal ({alignment_note})", fontsize=10)
    fig.savefig(OUT_PNG, bbox_inches="tight", pad_inches=0.05)
    plt.close(fig)


def save_geotiff(rgb: np.ndarray, transform, path: Path) -> None:
    profile = {
        "driver": "GTiff",
        "height": rgb.shape[1],
        "width": rgb.shape[2],
        "count": 3,
        "dtype": "uint8",
        "crs": EOV,
        "transform": transform,
    }
    with rasterio.open(path, "w", **profile) as dst:
        dst.write(rgb)


def main() -> None:
    merged = ezdxf.readfile(str(OUT_DXF))
    msp = merged.modelspace()
    plot_region = plot_boundary_region(msp, pad_m=2.0)
    view_region = region_with_context(plot_region, pad_m=45.0)

    minx, miny, maxx, maxy = view_region.bounds
    corners = [(minx, miny), (minx, maxy), (maxx, miny), (maxx, maxy)]
    lons, lats = zip(*(TO_WGS84.transform(x, y) for x, y in corners))
    region_wgs84 = box(min(lons), min(lats), max(lons), max(lats))

    zoom = pick_zoom(region_wgs84)
    google_rgb, google_transform = fetch_google_mosaic(region_wgs84, zoom)
    resolution = 0.35
    google_eov, eov_transform = warp_to_eov(google_rgb, google_transform, view_region, resolution=resolution)

    alignment_note = f"EPSG:23700, zoom={zoom}"
    anchor_dx, anchor_dy = anchor_shift_to_google_pin(plot_region)
    google_eov = apply_pixel_shift(
        google_eov,
        col_shift=anchor_dx / resolution,
        row_shift=-anchor_dy / resolution,
    )
    alignment_note += f", Google pin igazítás ~{math.hypot(anchor_dx, anchor_dy):.1f} m"

    ortho = load_ortho_on_grid(view_region, (google_eov.shape[1], google_eov.shape[2]), resolution)
    if ortho is not None and ortho.size > 0:
        google_eov, shift_px = refine_with_orthophoto(google_eov, ortho, resolution)
        if shift_px != (0.0, 0.0):
            alignment_note += f", orto finomhangolás dx={shift_px[0]:.2f}px dy={shift_px[1]:.2f}px"

    plot_cx = (plot_region.bounds[0] + plot_region.bounds[2]) / 2
    plot_cy = (plot_region.bounds[1] + plot_region.bounds[3]) / 2
    plot_lon, plot_lat = TO_WGS84.transform(plot_cx, plot_cy)
    center_dist_m = math.hypot(
        (plot_lat - GOOGLE_MAPS_CENTER[0]) * 111_320,
        (plot_lon - GOOGLE_MAPS_CENTER[1]) * 111_320 * math.cos(math.radians(plot_lat)),
    )
    alignment_note += f", telek-közép vs Google link ~{center_dist_m:.1f} m (WGS84)"

    vector_lines = collect_vector_segments(merged, plot_region)
    contour_segments = collect_contour_segments(merged, plot_region)

    save_geotiff(google_eov, eov_transform, OUT_TIF)
    plot_composite(view_region, google_eov, vector_lines, contour_segments, alignment_note)

    print(f"Google composite PNG: {OUT_PNG}")
    print(f"Google composite GeoTIFF (EOV): {OUT_TIF}")
    print(f"Alignment: {alignment_note}")


if __name__ == "__main__":
    main()
