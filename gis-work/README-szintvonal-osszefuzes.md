# Geodéta + GeoShop szintvonal összefűzés

## Eredményfájlok (1. lépés)

A két CAD forrás **ugyanabban a koordináta-rendszerben** van (EOV-szerű méteres térképi koordináták), ezért a szintvonalak közvetlenül ráemelhetők a geodéta rajzra **skálaváltoztatás nélkül**.

| Fájl | Leírás |
|------|--------|
| `geodeta-szintvonal-osszefuzve.dxf` | Geodéta rajz + a telek kiterjedésére eső GeoShop szintvonalak |
| `geodeta-szintvonal-osszefuzve.dwg` | Ugyanez DWG formátumban (AutoCAD / QGIS) |
| `geodeta-szintvonal-osszefuzve.png` | Gyors ellenőrző előnézet |
| `ortofoto-geodeta-szintvonal.png` | Ortofotó + geodéta vonalak + szintvonalak (2. lépés előnézet) |

Újrafuttatás:

```bash
python3 /workspace/gis-work/merge_contours.py
```

## 2. lépés – prompt ortofotóra helyezéshez

Másold be ezt egy új Cursor / GIS agent beszélgetésbe (a fájlok Drive-linkjeivel vagy helyi útvonalaival):

---

**Prompt (magyar):**

> Van egy georeferált ortofotóm (GeoTIFF, méteres koordináták, pl. SOCET-SET / EOV), egy geodéta által mért telekrajzom (DWG/DXF: parcellahatár, épületek, pontok), és egy GeoShop szintvonal térképem (DXF: ALAPSZINTVONAL, FELEZOSZINTVONAL, FOSZINTVONAL rétegek).
>
> **Feladat:** Készíts egy **új, különálló** fájlt, ahol az ortofotó a háttér, és rajta látszanak a geodéta vonalai és a már összeillesztett szintvonalak.
>
> **Követelmények:**
> 1. Ne változtasd meg a geodéta rajz koordináta-rendszerét és méteres skáláját (nincs torzítás, nincs új vetület).
> 2. Az ortofotó és a CAD rétegek illeszkedjenek: ellenőrizd a telek sarokpontokat / ismert objektumokat (épület, út) vizuálisan.
> 3. Kimenet: georeferált **GeoTIFF** (RGB + vektor égetve vagy külön réteg) és egy **PNG előnézet** ugyanarra a kiterjedésre.
> 4. Vonalstílus: geodéta = fekete, fő szintvonal = sötétpiros, köztes = narancs, alap = zöld, 0,8–1,2 pt vonalvastagság.
> 5. Ha szükséges, a szintvonalakat csak a telek bounding box-ára (±2 m) vágd, de a geodéta rajz teljes kiterjedését tartsd meg.
>
> **Források:**
> - Ortofotó: `https://drive.google.com/open?id=1ywl1j6rVbSVS9oJJdbop0e3bt9B2ao3n`
> - Geodéta (mérés): `https://drive.google.com/file/d/1tLvObndND1VR6qDdLDHSyWJFFNSXYpL9/view`
> - GeoShop szintvonal: `https://drive.google.com/file/d/1BWsNzhh84CFhkZEd4cx3w2aoctRY7isF/view`
> - (Ha kész) összefűzött CAD: `geodeta-szintvonal-osszefuzve.dxf`
>
> QGIS / GDAL / Python (ezdxf + rasterio) megoldás is jó. A végén írd le a koordináta-rendszer ellenőrzését (extents, CRS).

---

## Megjegyzés

Az ortofotó és a CAD koordináták ebben az esetben **illeszkednek** (a telek a `588000–594000 E / 244000–248000 N` ortofotó-extent-en belül van). Ha egy másik ortofotón eltérés lenne, először `gdalinfo` / QGIS „Georeferencer” szükséges.
