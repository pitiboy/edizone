#!/usr/bin/env python3
"""Kömlőd 383/384: geodéta felmérés + GeoShop szintvonalak + ortofotó.

A geodéta rajz EOV méterben marad (EPSG:23700), a területegység / extent
nem változik. A szintvonalakat a geodéta EXTMIN–EXTMAX téglalapjára vágjuk.
"""

from __future__ import annotations

import math
import re
from pathlib import Path

import ezdxf
import numpy as np
from ezdxf.enums import TextEntityAlignment
from PIL import Image
from shapely.geometry import LineString, box

Image.MAX_IMAGE_PIXELS = None

ROOT = Path(__file__).resolve().parent
FORRAS = ROOT / "forras"
GEOSHOP_DXF = FORRAS / "geoshop_szintvonal.dxf"
GEODETA_DXF = FORRAS / "geodeta.dxf"
ORTOFOTO = Path("/tmp/maps/ortofoto")

OUT_DXF = ROOT / "geodeta_szintvonalakkal.dxf"
OUT_PNG = ROOT / "geodeta_szintvonalakkal.png"
OUT_ORTO = ROOT / "ortofoto_geodeta_szintvonalakkal.png"
OUT_ORTO_TIGHT = ROOT / "ortofoto_geodeta_szintvonalakkal_telekextent.png"

# GeoTIFF: PixelIsArea, Y csökken lefelé (standard).
ORTO_X0 = 588000.0
ORTO_Y0 = 248000.0
ORTO_PX = 0.4

# Szintvonal stílus
CONTOUR_STYLE = {
    "FOSZINTVONAL": {
        "aci": 30,
        "rgb": (0.55, 0.22, 0.05),
        "lw": 2.4,
        "ls": "-",
        "label": "Főszintvonal (10 m)",
        "fontsize": 8,
        "z_step": 10.0,
    },
    "ALAPSZINTVONAL": {
        "aci": 40,
        "rgb": (0.72, 0.38, 0.12),
        "lw": 1.1,
        "ls": "-",
        "label": "Alapszintvonal (2,5 m)",
        "fontsize": 7,
        "z_step": 2.5,
    },
    "FELEZOSZINTVONAL": {
        "aci": 8,
        "rgb": (0.62, 0.45, 0.28),
        "lw": 0.7,
        "ls": (0, (3, 2)),
        "label": "Felezőszintvonal",
        "fontsize": 6,
        "z_step": None,
    },
}

GEODETA_DRAW = {
    "Földrészlet határ": {"rgb": (0.05, 0.05, 0.05), "lw": 2.0, "ls": "-", "zorder": 6},
    "Előzetes földrészlet vonal": {"rgb": (0.75, 0.05, 0.05), "lw": 1.6, "ls": (0, (6, 2)), "zorder": 6},
    "Megszűnő földrészlet vonal": {"rgb": (0.75, 0.15, 0.15), "lw": 1.2, "ls": (0, (2, 2)), "zorder": 5},
    "Gazdasági és melléképület": {"rgb": (0.12, 0.22, 0.55), "lw": 1.8, "ls": "-", "zorder": 7},
    "Épület tartozék (lépcső_ terasz_ rámpa)": {"rgb": (0.18, 0.40, 0.70), "lw": 1.3, "ls": "-", "zorder": 7},
    "Megszűnő jel": {"rgb": (0.75, 0.15, 0.15), "lw": 1.0, "ls": "-", "zorder": 5},
}


def geodeta_extent(doc) -> tuple[float, float, float, float]:
    extmin = doc.header["$EXTMIN"]
    extmax = doc.header["$EXTMAX"]
    xmin = float(extmin[0] if isinstance(extmin, (tuple, list)) else extmin.x)
    ymin = float(extmin[1] if isinstance(extmin, (tuple, list)) else extmin.y)
    xmax = float(extmax[0] if isinstance(extmax, (tuple, list)) else extmax.x)
    ymax = float(extmax[1] if isinstance(extmax, (tuple, list)) else extmax.y)
    return xmin, ymin, xmax, ymax


def clip_polyline(pts, xmin, ymin, xmax, ymax) -> list[list[tuple[float, float]]]:
    if len(pts) < 2:
        return []
    line = LineString([(float(x), float(y)) for x, y in pts])
    if line.is_empty or line.length == 0:
        return []
    inter = line.intersection(box(xmin, ymin, xmax, ymax))
    if inter.is_empty:
        return []
    parts = []
    geoms = [inter] if inter.geom_type == "LineString" else list(getattr(inter, "geoms", []))
    for g in geoms:
        if g.geom_type != "LineString" or g.length < 0.05:
            continue
        parts.append([(float(x), float(y)) for x, y in g.coords])
    return parts


def longest_part(parts: list[list[tuple[float, float]]]):
    best, best_len = None, 0.0
    for pts in parts:
        length = sum(
            math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1])
            for i in range(1, len(pts))
        )
        if length > best_len:
            best, best_len = pts, length
    return best, best_len


def _point_along(pts: list[tuple[float, float]], segs: list[float], total: float, frac: float):
    target = total * frac
    acc = 0.0
    for i, d in enumerate(segs):
        if acc + d >= target:
            t = (target - acc) / d if d else 0
            x = pts[i][0] + t * (pts[i + 1][0] - pts[i][0])
            y = pts[i][1] + t * (pts[i + 1][1] - pts[i][1])
            return x, y
        acc += d
    return pts[-1]


def label_anchor(pts: list[tuple[float, float]], xmin, ymin, xmax, ymax):
    """Pont a vágott vonalon, a kerettől beljebb."""
    if not pts or len(pts) < 2:
        return None
    segs = []
    total = 0.0
    for i in range(1, len(pts)):
        d = math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1])
        segs.append(d)
        total += d
    if total < 4:
        return None
    m = 4.0
    for frac in (0.5, 0.38, 0.62, 0.28, 0.72):
        x, y = _point_along(pts, segs, total, frac)
        if xmin + m < x < xmax - m and ymin + m < y < ymax - m:
            return x, y
    for x, y in pts:
        if xmin + 2.0 < x < xmax - 2.0 and ymin + 2.0 < y < ymax - 2.0:
            return x, y
    return None


def collect_contours(xmin, ymin, xmax, ymax):
    src = ezdxf.readfile(GEOSHOP_DXF)
    out = []  # dicts
    for e in src.modelspace():
        if e.dxftype() != "LWPOLYLINE":
            continue
        layer = e.dxf.layer
        if layer not in CONTOUR_STYLE:
            continue
        elev = float(e.dxf.elevation)
        pts = [(float(x), float(y)) for x, y in e.get_points("xy")]
        parts = clip_polyline(pts, xmin, ymin, xmax, ymax)
        if not parts:
            continue
        out.append({"layer": layer, "elev": elev, "parts": parts})
    return out


def explode_insert_lines(doc, insert):
    """Block INSERT → world-coordinate line segments."""
    block = doc.blocks.get(insert.dxf.name)
    if block is None:
        return []
    x0, y0 = insert.dxf.insert.x, insert.dxf.insert.y
    rot = math.radians(insert.dxf.rotation)
    sx, sy = insert.dxf.xscale, insert.dxf.yscale
    c, s = math.cos(rot), math.sin(rot)
    segs = []
    for e in block:
        if e.dxftype() != "LINE":
            continue
        pts = []
        for p in (e.dxf.start, e.dxf.end):
            x, y = p.x * sx, p.y * sy
            pts.append((x0 + x * c - y * s, y0 + x * s + y * c))
        segs.append(pts)
    return segs


def collect_geodeta(doc):
    lines = []
    points = []
    texts = []
    inserts = []
    msp = doc.modelspace()
    for e in msp:
        t = e.dxftype()
        if t == "LINE":
            lines.append(
                {
                    "layer": e.dxf.layer,
                    "a": (float(e.dxf.start.x), float(e.dxf.start.y)),
                    "b": (float(e.dxf.end.x), float(e.dxf.end.y)),
                    "za": float(e.dxf.start.z),
                    "zb": float(e.dxf.end.z),
                }
            )
        elif t == "POINT":
            loc = e.dxf.location
            points.append((float(loc.x), float(loc.y), float(loc.z), e.dxf.layer))
        elif t == "TEXT":
            ins = e.dxf.insert
            texts.append(
                {
                    "text": e.dxf.text,
                    "xy": (float(ins.x), float(ins.y)),
                    "h": float(e.dxf.height),
                    "rot": float(e.dxf.rotation),
                    "layer": e.dxf.layer,
                }
            )
        elif t == "INSERT":
            for a, b in explode_insert_lines(doc, e):
                inserts.append({"layer": e.dxf.layer, "a": a, "b": b})
    return lines, points, texts, inserts


def build_combined_dxf(geodeta_doc, contours, xmin, ymin, xmax, ymax):
    """Új DXF: geodéta entitások másolva + vágott szintvonalak. Extent változatlan."""
    src_layers = {
        "Földrészlet határ": 100,
        "Helyrajziszám": 100,
        "Előzetes földrészlet vonal": 1,
        "Gazdasági és melléképület": 110,
        "Épület tartozék (lépcső_ terasz_ rámpa)": 111,
        "Megszűnő földrészlet vonal": 145,
        "Megszűnő jel": 1,
        "Pontok": 7,
    }
    doc = ezdxf.new("R2013", setup=True)
    doc.header["$INSUNITS"] = 6
    doc.header["$EXTMIN"] = (xmin, ymin, 0)
    doc.header["$EXTMAX"] = (xmax, ymax, 0)
    for name, color in src_layers.items():
        if name not in doc.layers:
            doc.layers.add(name, color=color)
    for name, st in CONTOUR_STYLE.items():
        if name not in doc.layers:
            doc.layers.add(name, color=st["aci"])
    doc.layers.add("SZINTVONAL_FELIRAT", color=30)
    doc.layers.add("SZINTEZESI_PONT_FELIRAT", color=8)

    msp = doc.modelspace()
    lines, points, texts, inserts = collect_geodeta(geodeta_doc)
    for ln in lines:
        msp.add_line(
            (ln["a"][0], ln["a"][1], ln["za"]),
            (ln["b"][0], ln["b"][1], ln["zb"]),
            dxfattribs={"layer": ln["layer"]},
        )
    for ins in inserts:
        msp.add_line(ins["a"], ins["b"], dxfattribs={"layer": ins["layer"]})
    for x, y, z, layer in points:
        msp.add_point((x, y, z), dxfattribs={"layer": layer})
        if z > 1:
            t = msp.add_text(
                f"{z:.2f}",
                dxfattribs={"layer": "SZINTEZESI_PONT_FELIRAT", "height": 0.7},
            )
            t.set_placement((x + 0.6, y + 0.4), align=TextEntityAlignment.LEFT)
    for tx in texts:
        t = msp.add_text(
            tx["text"],
            dxfattribs={"layer": tx["layer"], "height": tx["h"], "rotation": tx["rot"]},
        )
        t.set_placement(tx["xy"], align=TextEntityAlignment.LEFT)

    labeled = set()
    for c in contours:
        for part in c["parts"]:
            pl = msp.add_lwpolyline(
                [(x, y) for x, y in part],
                dxfattribs={"layer": c["layer"], "elevation": c["elev"]},
            )
            pl.dxf.elevation = c["elev"]
        key = (c["layer"], round(c["elev"], 2))
        if key in labeled:
            continue
        pts, length = longest_part(c["parts"])
        anchor = label_anchor(pts, xmin, ymin, xmax, ymax) if pts else None
        if anchor is None:
            continue
        labeled.add(key)
        h = 1.6 if c["layer"] == "FOSZINTVONAL" else 1.2
        t = msp.add_text(
            f"{c['elev']:g}",
            dxfattribs={
                "layer": "SZINTVONAL_FELIRAT",
                "height": h,
                "color": CONTOUR_STYLE[c["layer"]]["aci"],
            },
        )
        t.set_placement(anchor, align=TextEntityAlignment.MIDDLE_CENTER)

    doc.saveas(OUT_DXF)
    patch_dxf_extents(OUT_DXF, xmin, ymin, xmax, ymax)
    return doc


def patch_dxf_extents(path: Path, xmin, ymin, xmax, ymax):
    """ezdxf mentéskor $EXTMIN/$EXTMAX sentinelre megy; a geodéta-extentet visszaírjuk."""
    text = path.read_text(encoding="utf-8")

    def repl_block(varname: str, x: float, y: float, z: float) -> None:
        nonlocal text
        pat = rf"(  9\n\${varname}\n 10\n)[^\n]+(\n 20\n)[^\n]+(\n 30\n)[^\n]+"
        repl = rf"\g<1>{x:.9f}\g<2>{y:.9f}\g<3>{z:.3f}"
        text2, n = re.subn(pat, repl, text, count=1)
        if n != 1:
            raise RuntimeError(f"nem található ${varname} a DXF-ben")
        text = text2

    repl_block("EXTMIN", xmin, ymin, 0.0)
    repl_block("EXTMAX", xmax, ymax, 0.0)
    path.write_text(text, encoding="utf-8")


def format_elev(z: float) -> str:
    if abs(z - round(z)) < 1e-6:
        return f"{int(round(z))}"
    return f"{z:.1f}".replace(".", ",")


def draw_scalebar(ax, xmin, ymin, xmax, ymax, meters=20, color="0.15"):
    span_x = xmax - xmin
    span_y = ymax - ymin
    x0 = xmin + span_x * 0.06
    y0 = ymin + span_y * 0.06
    ax.plot([x0, x0 + meters], [y0, y0], color=color, lw=2.2, solid_capstyle="butt", zorder=10)
    ax.plot([x0, x0], [y0 - span_y * 0.008, y0 + span_y * 0.008], color=color, lw=2.2, zorder=10)
    ax.plot(
        [x0 + meters, x0 + meters],
        [y0 - span_y * 0.008, y0 + span_y * 0.008],
        color=color,
        lw=2.2,
        zorder=10,
    )
    ax.text(
        x0 + meters / 2,
        y0 + span_y * 0.018,
        f"{meters} m",
        ha="center",
        va="bottom",
        fontsize=8,
        color=color,
        zorder=10,
    )


def draw_north(ax, xmin, ymin, xmax, ymax, color="0.15"):
    x = xmax - (xmax - xmin) * 0.07
    y = ymax - (ymax - ymin) * 0.12
    dy = (ymax - ymin) * 0.08
    ax.annotate(
        "",
        xy=(x, y + dy),
        xytext=(x, y),
        arrowprops=dict(arrowstyle="-|>", color=color, lw=1.4),
        zorder=10,
    )
    ax.text(x, y + dy + (ymax - ymin) * 0.012, "É", ha="center", va="bottom", fontsize=9, color=color, zorder=10)


def render_combined_png(geodeta_pack, contours, xmin, ymin, xmax, ymax, path: Path, title: str):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    lines, points, texts, inserts = geodeta_pack
    span_x, span_y = xmax - xmin, ymax - ymin
    px_per_m = 22
    dpi = 160
    fig_w = span_x * px_per_m / dpi + 2.4
    fig_h = span_y * px_per_m / dpi + 2.2
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)
    ax.set_aspect("equal")
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_facecolor("white")
    fig.patch.set_facecolor("white")

    # szintvonalak (alul)
    for c in sorted(contours, key=lambda d: d["elev"]):
        st = CONTOUR_STYLE[c["layer"]]
        for part in c["parts"]:
            xs, ys = zip(*part)
            ax.plot(xs, ys, color=st["rgb"], lw=st["lw"], ls=st["ls"], zorder=3, solid_capstyle="round")
        pts, length = longest_part(c["parts"])
        anchor = label_anchor(pts, xmin, ymin, xmax, ymax) if pts else None
        if anchor and length > 5:
            ax.text(
                anchor[0],
                anchor[1],
                format_elev(c["elev"]),
                color=st["rgb"],
                fontsize=st["fontsize"],
                ha="center",
                va="center",
                zorder=4,
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.75),
            )

    def draw_seg(a, b, layer):
        st = GEODETA_DRAW.get(layer)
        if not st:
            st = {"rgb": (0.2, 0.2, 0.2), "lw": 1.0, "ls": "-", "zorder": 5}
        ax.plot(
            [a[0], b[0]],
            [a[1], b[1]],
            color=st["rgb"],
            lw=st["lw"],
            ls=st["ls"],
            zorder=st["zorder"],
            solid_capstyle="round",
        )

    for ln in lines:
        draw_seg(ln["a"], ln["b"], ln["layer"])
    for ins in inserts:
        draw_seg(ins["a"], ins["b"], ins["layer"])

    parcel_xy = set()
    for ln in lines:
        if ln["layer"] == "Földrészlet határ":
            parcel_xy.add((round(ln["a"][0], 3), round(ln["a"][1], 3)))
            parcel_xy.add((round(ln["b"][0], 3), round(ln["b"][1], 3)))
    for x, y, z, _layer in points:
        ax.plot(x, y, "o", ms=2.8, color="0.15", zorder=8)
        if z > 1 and (round(x, 3), round(y, 3)) in parcel_xy:
            ax.text(x + 0.8, y + 0.6, f"{z:.2f}", fontsize=6.5, color="0.2", zorder=8)

    for t in texts:
        ax.text(
            t["xy"][0],
            t["xy"][1],
            t["text"],
            fontsize=11,
            fontweight="bold",
            color="0.05",
            ha="center",
            va="center",
            zorder=9,
        )

    draw_scalebar(ax, xmin, ymin, xmax, ymax)
    draw_north(ax, xmin, ymin, xmax, ymax)

    ax.set_xlabel("EOV Y (kelet, m)  ·  EPSG:23700")
    ax.set_ylabel("EOV X (észak, m)")
    ax.ticklabel_format(useOffset=False, style="plain")
    from matplotlib.ticker import FuncFormatter

    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _p: f"{v:.0f}"))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _p: f"{v:.0f}"))
    ax.tick_params(labelsize=7)
    ax.grid(True, color="0.88", lw=0.4, zorder=0)
    ax.set_axisbelow(True)
    ax.set_title(title, fontsize=11, pad=10)

    handles = [
        Line2D([0], [0], color=CONTOUR_STYLE["FOSZINTVONAL"]["rgb"], lw=2.4, label="Főszintvonal (10 m)"),
        Line2D([0], [0], color=CONTOUR_STYLE["ALAPSZINTVONAL"]["rgb"], lw=1.2, label="Alapszintvonal (2,5 m)"),
        Line2D([0], [0], color=GEODETA_DRAW["Földrészlet határ"]["rgb"], lw=2.0, label="Földrészlet-határ"),
        Line2D([0], [0], color=GEODETA_DRAW["Előzetes földrészlet vonal"]["rgb"], lw=1.6, ls=(0, (6, 2)), label="Előzetes megosztás"),
        Line2D([0], [0], color=GEODETA_DRAW["Megszűnő földrészlet vonal"]["rgb"], lw=1.2, ls=(0, (2, 2)), label="Megszűnő határ"),
        Line2D([0], [0], color=GEODETA_DRAW["Gazdasági és melléképület"]["rgb"], lw=1.8, label="Melléképület"),
        Line2D([0], [0], color=GEODETA_DRAW["Épület tartozék (lépcső_ terasz_ rámpa)"]["rgb"], lw=1.3, label="Épület-tartozék"),
        Line2D([0], [0], marker="o", color="0.15", lw=0, ms=4, label="Szintezett pont (mBf)"),
    ]
    ax.legend(
        handles=handles,
        loc="lower right",
        fontsize=7,
        framealpha=0.92,
        edgecolor="0.8",
        title="Jelmagyarázat",
        title_fontsize=8,
    )
    fig.text(
        0.01,
        0.005,
        "Forrás: geodéta DWG (telek + objektumok) + GeoShop szintvonal DXF. "
        "A geodéta EOV-extentje változatlan. Magasság: mBf a szintvonal-elevation és a felmérési pontok alapján.",
        fontsize=6.5,
        color="0.3",
        ha="left",
        va="bottom",
    )
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(path, dpi=dpi, facecolor="white")
    plt.close(fig)


def eov_to_px(x, y):
    col = (x - ORTO_X0) / ORTO_PX
    row = (ORTO_Y0 - y) / ORTO_PX
    return col, row


def write_pgw(path: Path, pixel_m: float, xmin: float, ymax: float):
    # World file: pixel center of upper-left
    cx = xmin + pixel_m / 2.0
    cy = ymax - pixel_m / 2.0
    path.write_text(f"{pixel_m:.10f}\n0.0\n0.0\n{-pixel_m:.10f}\n{cx:.6f}\n{cy:.6f}\n", encoding="utf-8")


def render_ortho_overlay(
    geodeta_pack,
    contours,
    xmin,
    ymin,
    xmax,
    ymax,
    out_png: Path,
    buffer_m: float,
    title: str,
    upsample: int = 8,
):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.patheffects as pe
    import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D

    bx0, by0 = xmin - buffer_m, ymin - buffer_m
    bx1, by1 = xmax + buffer_m, ymax + buffer_m

    im = Image.open(ORTOFOTO)
    w, h = im.size
    c0, r0 = eov_to_px(bx0, by1)  # UL
    c1, r1 = eov_to_px(bx1, by0)  # LR
    c0i, r0i = max(0, int(math.floor(c0))), max(0, int(math.floor(r0)))
    c1i, r1i = min(w, int(math.ceil(c1))), min(h, int(math.ceil(r1)))
    crop = im.crop((c0i, r0i, c1i, r1i))
    # A vágás EOV-sarkai a pixel-sarokra igazítva
    crop_xmin = ORTO_X0 + c0i * ORTO_PX
    crop_ymax = ORTO_Y0 - r0i * ORTO_PX
    crop_xmax = ORTO_X0 + c1i * ORTO_PX
    crop_ymin = ORTO_Y0 - r1i * ORTO_PX

    if upsample > 1:
        crop = crop.resize((crop.width * upsample, crop.height * upsample), Image.Resampling.LANCZOS)
    arr = np.asarray(crop)

    lines, points, texts, inserts = geodeta_pack
    span_x = crop_xmax - crop_xmin
    span_y = crop_ymax - crop_ymin
    dpi = 160
    fig_w = max(10.0, span_x / 16)
    fig_h = max(7.5, span_y / 16) + 0.9
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)
    ax.set_aspect("equal")
    ax.imshow(
        arr,
        extent=(crop_xmin, crop_xmax, crop_ymin, crop_ymax),
        origin="upper",
        zorder=1,
        interpolation="nearest",
    )
    ax.set_xlim(crop_xmin, crop_xmax)
    ax.set_ylim(crop_ymin, crop_ymax)

    # geodéta extent keret
    ax.add_patch(
        plt.Rectangle(
            (xmin, ymin),
            xmax - xmin,
            ymax - ymin,
            fill=False,
            ec="white",
            lw=0.6,
            ls=(0, (2, 2)),
            zorder=2,
            alpha=0.7,
        )
    )

    for c in sorted(contours, key=lambda d: d["elev"]):
        st = CONTOUR_STYLE[c["layer"]]
        # ortofotón a vágott vonalakat a bufferes ablakhoz újra vágjuk? A contours
        # a geodéta extentre vannak vágva — step 2-nél a bufferes nézethez
        # a teljes geoshopból újra vágunk, ha buffer>0.
        parts = c["parts"]
        for part in parts:
            xs, ys = zip(*part)
            ax.plot(
                xs,
                ys,
                color=(1.0, 0.85, 0.15),
                lw=st["lw"] + 0.4,
                ls=st["ls"],
                zorder=4,
                solid_capstyle="round",
            )
        pts, length = longest_part(parts)
        anchor = label_anchor(pts, xmin, ymin, xmax, ymax) if pts else None
        if anchor and length > 5:
            ax.text(
                anchor[0],
                anchor[1],
                format_elev(c["elev"]),
                color="black",
                fontsize=st["fontsize"] + 1,
                ha="center",
                va="center",
                zorder=5,
                bbox=dict(boxstyle="round,pad=0.15", fc=(1, 0.95, 0.55), ec="none", alpha=0.88),
            )

    def draw_seg(a, b, layer, color, lw):
        ax.plot([a[0], b[0]], [a[1], b[1]], color=color, lw=lw, zorder=6, solid_capstyle="round")

    parcel_color = (0.05, 1.0, 0.85)
    bldg_color = (1.0, 0.25, 0.15)
    acc_color = (1.0, 0.55, 0.15)
    dash_color = (1.0, 0.4, 0.85)

    for ln in lines:
        layer = ln["layer"]
        if layer == "Földrészlet határ":
            # halo
            ax.plot([ln["a"][0], ln["b"][0]], [ln["a"][1], ln["b"][1]], color="black", lw=3.2, zorder=5, solid_capstyle="round")
            draw_seg(ln["a"], ln["b"], layer, parcel_color, 1.8)
        elif layer == "Gazdasági és melléképület":
            ax.plot([ln["a"][0], ln["b"][0]], [ln["a"][1], ln["b"][1]], color="black", lw=2.6, zorder=5, solid_capstyle="round")
            draw_seg(ln["a"], ln["b"], layer, bldg_color, 1.6)
        elif "tartozék" in layer:
            draw_seg(ln["a"], ln["b"], layer, acc_color, 1.4)
        elif "Megszűnő" in layer:
            ax.plot(
                [ln["a"][0], ln["b"][0]],
                [ln["a"][1], ln["b"][1]],
                color=dash_color,
                lw=1.4,
                ls=(0, (3, 2)),
                zorder=6,
            )
        elif "Előzetes" in layer:
            ax.plot(
                [ln["a"][0], ln["b"][0]],
                [ln["a"][1], ln["b"][1]],
                color=(1.0, 0.15, 0.15),
                lw=1.8,
                ls=(0, (6, 2)),
                zorder=6,
            )
        else:
            draw_seg(ln["a"], ln["b"], layer, "white", 1.2)

    for ins in inserts:
        ax.plot(
            [ins["a"][0], ins["b"][0]],
            [ins["a"][1], ins["b"][1]],
            color=dash_color,
            lw=1.4,
            zorder=6,
        )

    for x, y, z, _layer in points:
        ax.plot(x, y, "o", ms=3.0, color="white", markeredgecolor="black", markeredgewidth=0.4, zorder=8)

    for t in texts:
        ax.text(
            t["xy"][0],
            t["xy"][1],
            t["text"],
            fontsize=12,
            fontweight="bold",
            color="white",
            ha="center",
            va="center",
            zorder=9,
            path_effects=[pe.withStroke(linewidth=3, foreground="black")],
        )

    draw_scalebar(ax, crop_xmin, crop_ymin, crop_xmax, crop_ymax, meters=20, color="white")
    draw_north(ax, crop_xmin, crop_ymin, crop_xmax, crop_ymax, color="white")

    ax.set_xlabel("EOV Y (kelet, m)  ·  EPSG:23700")
    ax.set_ylabel("EOV X (észak, m)")
    ax.ticklabel_format(useOffset=False, style="plain")
    from matplotlib.ticker import FuncFormatter

    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _p: f"{v:.0f}"))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _p: f"{v:.0f}"))
    ax.tick_params(labelsize=7, colors="0.15")
    ax.set_title(title, fontsize=11, pad=10)

    handles = [
        Line2D([0], [0], color=(1.0, 0.85, 0.15), lw=2.0, label="Szintvonal (mBf)"),
        Line2D([0], [0], color=parcel_color, lw=2.0, label="Földrészlet-határ"),
        Line2D([0], [0], color=(1.0, 0.15, 0.15), lw=1.8, ls=(0, (6, 2)), label="Előzetes megosztás"),
        Line2D([0], [0], color=dash_color, lw=1.4, ls=(0, (3, 2)), label="Megszűnő határ"),
        Line2D([0], [0], color=bldg_color, lw=1.8, label="Melléképület"),
        Line2D([0], [0], color=acc_color, lw=1.4, label="Épület-tartozék"),
    ]
    ax.legend(
        handles=handles,
        loc="lower right",
        fontsize=7,
        framealpha=0.88,
        edgecolor="0.8",
        title="Jelmagyarázat",
        title_fontsize=8,
    )
    cap = (
        f"Ortofotó (0,4 m/px) + geodéta felmérés + GeoShop szintvonalak. "
        f"{'Buffer: ' + str(int(buffer_m)) + ' m. ' if buffer_m else 'Geodéta-extent, méretarány változatlan. '}"
        "Koordináta: EOV / EPSG:23700."
    )
    fig.text(0.01, 0.005, cap, fontsize=6.5, color="0.25", ha="left", va="bottom")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(out_png, dpi=dpi, facecolor="white")
    plt.close(fig)

    georef_png = Path(str(out_png).replace(".png", "_georef.png"))
    render_georef_raster(
        geodeta_pack,
        contours,
        xmin,
        ymin,
        xmax,
        ymax,
        crop,
        crop_xmin,
        crop_ymin,
        crop_xmax,
        crop_ymax,
        georef_png,
        pixel_m=ORTO_PX / upsample,
    )
    write_pgw(georef_png.with_suffix(".pgw"), ORTO_PX / upsample, crop_xmin, crop_ymax)
    return crop_xmin, crop_ymin, crop_xmax, crop_ymax


def render_georef_raster(
    geodeta_pack,
    contours,
    xmin,
    ymin,
    xmax,
    ymax,
    crop_img,
    crop_xmin,
    crop_ymin,
    crop_xmax,
    crop_ymax,
    out_png: Path,
    pixel_m: float,
):
    """Tengely nélküli, világfájllal georeferálható raszter (PNG + PGW)."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.patheffects as pe
    import matplotlib.pyplot as plt

    w, h = crop_img.size
    dpi = 100
    fig = plt.figure(figsize=(w / dpi, h / dpi), dpi=dpi)
    ax = fig.add_axes((0, 0, 1, 1))
    ax.imshow(
        np.asarray(crop_img),
        extent=(crop_xmin, crop_xmax, crop_ymin, crop_ymax),
        origin="upper",
        interpolation="nearest",
        zorder=1,
    )
    ax.set_xlim(crop_xmin, crop_xmax)
    ax.set_ylim(crop_ymin, crop_ymax)
    ax.set_axis_off()
    ax.set_aspect("equal")

    for c in sorted(contours, key=lambda d: d["elev"]):
        st = CONTOUR_STYLE[c["layer"]]
        for part in c["parts"]:
            xs, ys = zip(*part)
            ax.plot(xs, ys, color=(1.0, 0.85, 0.15), lw=st["lw"] + 0.6, ls=st["ls"], zorder=4, solid_capstyle="round")
        pts, length = longest_part(c["parts"])
        anchor = label_anchor(pts, xmin, ymin, xmax, ymax) if pts else None
        if anchor and length > 5:
            ax.text(
                anchor[0],
                anchor[1],
                format_elev(c["elev"]),
                color="black",
                fontsize=7,
                ha="center",
                va="center",
                zorder=5,
                bbox=dict(boxstyle="round,pad=0.12", fc=(1, 0.95, 0.55), ec="none", alpha=0.9),
            )

    lines, points, texts, inserts = geodeta_pack
    parcel_color = (0.05, 1.0, 0.85)
    bldg_color = (1.0, 0.25, 0.15)
    acc_color = (1.0, 0.55, 0.15)
    dash_color = (1.0, 0.4, 0.85)

    for ln in lines:
        layer = ln["layer"]
        xs, ys = [ln["a"][0], ln["b"][0]], [ln["a"][1], ln["b"][1]]
        if layer == "Földrészlet határ":
            ax.plot(xs, ys, color="black", lw=3.4, zorder=5, solid_capstyle="round")
            ax.plot(xs, ys, color=parcel_color, lw=1.9, zorder=6, solid_capstyle="round")
        elif layer == "Gazdasági és melléképület":
            ax.plot(xs, ys, color="black", lw=2.8, zorder=5, solid_capstyle="round")
            ax.plot(xs, ys, color=bldg_color, lw=1.7, zorder=6, solid_capstyle="round")
        elif "tartozék" in layer:
            ax.plot(xs, ys, color=acc_color, lw=1.5, zorder=6, solid_capstyle="round")
        elif "Megszűnő" in layer:
            ax.plot(xs, ys, color=dash_color, lw=1.5, ls=(0, (3, 2)), zorder=6)
        elif "Előzetes" in layer:
            ax.plot(xs, ys, color=(1.0, 0.15, 0.15), lw=1.9, ls=(0, (6, 2)), zorder=6)
        else:
            ax.plot(xs, ys, color="white", lw=1.2, zorder=6)

    for ins in inserts:
        ax.plot(
            [ins["a"][0], ins["b"][0]],
            [ins["a"][1], ins["b"][1]],
            color=dash_color,
            lw=1.5,
            zorder=6,
        )
    for x, y, z, _layer in points:
        ax.plot(x, y, "o", ms=2.6, color="white", markeredgecolor="black", markeredgewidth=0.4, zorder=8)
    for t in texts:
        ax.text(
            t["xy"][0],
            t["xy"][1],
            t["text"],
            fontsize=22,
            fontweight="bold",
            color="white",
            ha="center",
            va="center",
            zorder=9,
            path_effects=[pe.withStroke(linewidth=5, foreground="black")],
        )

    fig.savefig(out_png, dpi=dpi, pad_inches=0)
    plt.close(fig)


def collect_contours_window(xmin, ymin, xmax, ymax):
    return collect_contours(xmin, ymin, xmax, ymax)


def main():
    geodeta_doc = ezdxf.readfile(GEODETA_DXF)
    xmin, ymin, xmax, ymax = geodeta_extent(geodeta_doc)
    print(f"Geodéta extent EOV: X {xmin:.3f}–{xmax:.3f}  Y {ymin:.3f}–{ymax:.3f}")
    print(f"Span: {xmax-xmin:.3f} m × {ymax-ymin:.3f} m")

    contours = collect_contours(xmin, ymin, xmax, ymax)
    print(f"Vágott szintvonal-szakaszok: {len(contours)}")
    for c in sorted(contours, key=lambda d: (d["elev"], d["layer"])):
        n = sum(len(p) for p in c["parts"])
        print(f"  {c['layer']:18s}  {c['elev']:6.1f} m   {len(c['parts'])} rész, {n} csúcs")

    geodeta_pack = collect_geodeta(geodeta_doc)
    lines, points, texts, inserts = geodeta_pack
    print(f"Geodéta: {len(lines)} vonal, {len(points)} pont, {len(texts)} szöveg, {len(inserts)} insert-vonal")

    build_combined_dxf(geodeta_doc, contours, xmin, ymin, xmax, ymax)
    print("DXF:", OUT_DXF)

    render_combined_png(
        geodeta_pack,
        contours,
        xmin,
        ymin,
        xmax,
        ymax,
        OUT_PNG,
        "Kömlőd hrsz. 383–384  ·  geodéta felmérés + GeoShop szintvonalak\n"
        "EOV / EPSG:23700  ·  a geodéta területegysége változatlan",
    )
    print("PNG:", OUT_PNG)

    # Step 2: ortofotó — kontextusos (25 m buffer) + tight (eredeti extent)
    buf = 25.0
    contours_buf = collect_contours(xmin - buf, ymin - buf, xmax + buf, ymax + buf)
    render_ortho_overlay(
        geodeta_pack,
        contours_buf,
        xmin,
        ymin,
        xmax,
        ymax,
        OUT_ORTO,
        buffer_m=buf,
        title="Kömlőd hrsz. 383–384  ·  ortofotó + geodéta rajz + szintvonalak",
        upsample=8,
    )
    print("Orto (buffer 25 m):", OUT_ORTO)

    render_ortho_overlay(
        geodeta_pack,
        contours,
        xmin,
        ymin,
        xmax,
        ymax,
        OUT_ORTO_TIGHT,
        buffer_m=0.0,
        title="Kömlőd hrsz. 383–384  ·  ortofotó + geodéta + szintvonal  (geodéta-extent)",
        upsample=10,
    )
    print("Orto (telek extent):", OUT_ORTO_TIGHT)


if __name__ == "__main__":
    main()
