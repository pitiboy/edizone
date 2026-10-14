# Kömlőd hrsz. 383–384 — geodéta + szintvonal + ortofotó

A geodéta DWG EOV-koordinátáit (EPSG:23700, méter) **nem skáláztuk és nem toltuk el**. A GeoShop szintvonalakat ugyanabba a koordináta-rendszerbe vágtuk a geodéta `$EXTMIN`–`$EXTMAX` téglalapjára, majd az összedolgozott vektort rárajzoltuk az ortofotóra.

## Geodéta extent (változatlan)

| | EOV Y (kelet) | EOV X (észak) |
|---|---|---|
| min | 591207,404 m | 245306,231 m |
| max | 591360,891 m | 245399,695 m |
| méret | **153,487 m** | **93,464 m** |

A szintezett pontok magassága kb. **186,8–202,9 mBf**; a GeoShop szintvonalak elevation-értéke ezzel egyezik (187,5 … 207,5 m, 2,5 m alapszintvonal / 10 m főszintvonal).

## Kimeneti fájlok

| Fájl | Mi ez |
|---|---|
| `geodeta_szintvonalakkal.dxf` | CAD: eredeti geodéta vonalak + vágott szintvonalak, EOV méterben, eredeti extent |
| `geodeta_szintvonalakkal.png` | Ugyanez rajzként, méretarányos (20 m-es lépték) |
| `ortofoto_geodeta_szintvonalakkal.png` | Ortofotó + rajz, **25 m-es** környezet a telek körül |
| `ortofoto_geodeta_szintvonalakkal_georef.png` + `.pgw` | Tengely nélküli georeferált raszter (QGIS: PNG+world file, EOV) |
| `ortofoto_geodeta_szintvonalakkal_telekextent.png` | Ortofotó + rajz, **pontosan a geodéta-extent** |
| `ortofoto_geodeta_szintvonalakkal_telekextent_georef.png` + `.pgw` | Ugyanez georeferálva |
| `forras/` | Eredeti GeoShop DXF, geodéta DWG és a belőle készült DXF |
| `osszeilleszt.py` | Újrageneráló script |

DXF-rétegek: eredeti geodéta rétegek + `ALAPSZINTVONAL`, `FOSZINTVONAL`, `SZINTVONAL_FELIRAT`, `SZINTEZESI_PONT_FELIRAT` (utóbbi kikapcsolható).

Újragenerálás (a nyers ortofotó `/tmp/maps/ortofoto` alatt):

```bash
python3 telek-terkep/osszeilleszt.py
```

## Újrafelhasználható prompt (ortofotó + összedolgozott rajz)

Ha máshol, másik modellben vagy GIS-ben kell újra összerakni:

```
Feladat: két (és egy harmadik) georeferált állományt EOV / EPSG:23700 méterben
összeilleszteni, skálázás és eltolás nélkül.

Bemenet:
1) Geodéta felmérés (DWG/DXF): telekhatár, épületek, pontok. Ez a mester.
   Extentét, méteregységét, EOV-koordinátáit TILOS megváltoztatni.
2) GeoShop szintvonal DXF (ALAPSZINTVONAL, FOSZINTVONAL, FELEZOSZINTVONAL),
   LWPOLYLINE elevation = mBf. Csak a geodéta EXTMIN–EXTMAX téglalapjába
   eső szakaszokat másold át, vágd a keretre. Magassági felirat = elevation.
3) Ortofotó GeoTIFF: pixel 0,4 m, tie point (0,0) → EOV (588000, 248000),
   X = 588000 + col*0,4 ; Y = 248000 − row*0,4 (PixelIsArea, észak fent).

Lépés 1 — CAD/PNG, geodéta-extent:
- Nyisd a geodéta rajzot EOV-ban.
- Másold rá a vágott szintvonalakat új rétegekre.
- Ne resample-eld, ne igazítsd “szemre”, ne változtasd a területegységet.
- Kimenet: DXF + méretarányos PNG (lépték, É-nyíl, jelmagyarázat, mBf).

Lépés 2 — külön fájl, ortofotó-alap:
- Vágd ki az ortofotóból a geodéta-extentet (opcionális 20–30 m buffer csak
  a kontextushoz; a vektorok továbbra is az eredeti EOV-koordinátákon).
- Rajzold rá a 1. lépés vektorait: telekhatár, előzetes/megszűnő vonal,
  épületek, szintvonal + magasság.
- Kimenet: annotált PNG, PLUSZ tengely nélküli georeferált PNG + world file
  (vagy GeoTIFF) EPSG:23700-ban.

Ellenőrzés: a melléképület és a telekhatár egybeesik az ortofotón látható
tetővel/kerítéssel; a 190–200 mBf szintvonalak a szintezett pontok Z-jével
konzisztensek. Magyar feliratok, hrsz. 383 és 384.
```
