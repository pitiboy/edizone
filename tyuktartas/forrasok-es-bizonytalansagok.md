# Források és bizonytalanságok

## Elsődleges / hivatalos jellegű

| Téma | Forrás |
|------|--------|
| Baromfi tápanyagigény (NRC 1994 alap) | [Merck Veterinary Manual — Nutritional Requirements of Poultry](https://www.merckvetmanual.com/poultry/nutrition-and-management-poultry/nutritional-requirements-of-poultry) |
| NRC 1994 teljes szöveg | [Nutrient Requirements of Poultry, 9th ed. (PDF)](https://img1.wsimg.com/blobby/go/cef62d35-7a84-4a76-a0b6-562062e3ac2e/downloads/NRC%20Aves%201994.pdf) |
| NRC 10. kiadás (2025/2026) | [National Academies — 10th Revised Edition](https://www.nationalacademies.org/read/25395) |
| Kukorica takarmány | [Poultry Extension — Corn in poultry diets](https://poultry.extension.org/articles/feeds-and-feeding-of-poultry/feed-ingredients-for-poultry/cereals-in-poultry-diets/corn-in-poultry-diets/) |
| Egész napraforgó összetétel | [INRA Feedtables — sunflower seed whole](https://www.feedtables.com/content/sunflower-seed-whole) |
| Napraforgó organikus baromfinál | [eOrganic — Using Sunflower Seed](https://eorganic.org/pages/70235/using-sunflower-seed-in-organic-poultry-diets) |
| Tojáshéj Ca | [Scientific Reports 2021 — coarse eggshell](https://www.nature.com/articles/s41598-021-92589-y) |

## Tudományos cikkek / reviews

| Téma | Forrás |
|------|--------|
| Napraforgó dara, lizin | [PMC — sunflower meal layers 30%](https://pmc.ncbi.nlm.nih.gov/articles/PMC10850339/) |
| Forage, organikus layer | [Increased foraging in organic layers (PhD összefoglaló)](https://exa.ai/library/publication/h5sq6zp7fzr) |
| Forage vs termelés | [Nutrient-restricted organic layers](https://exa.ai/library/publication/ddwb3hf56vf) |
| Legelő ~20% ration | [Taylor & Francis 2025 — dietary forage organic poultry](https://www.tandfonline.com/doi/full/10.1080/01448765.2025.2483212) |
| Range enrichment | [Forage intake, trees](https://exa.ai/library/publication/tc0dd8r00n4) |

## Őshonos magyar tyúk — genetika / termelés

| Téma | Forrás |
|------|--------|
| Tojás/ testsúly fajtánként | [PLOS One — six Hungarian local breeds](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0238849) |
| HU-BA rendszer | [HU-BA system PDF](http://geneconservation.hu/sites/default/files/hu_ba_system_paper.pdf) |
| Sárga magyar, szezon | [Backyard Poultry — Hungarian Yellow](https://backyardpoultry.iamcountryside.com/chickens-101/hungarian-yellow-chickens-2/) |
| Fajta történet | [EPA — Animal welfare 2009 PDF](https://epa.oszk.hu/02000/02067/00014/pdf/EPA02067_AWETH2009119148.pdf) |

## Tapasztalati / másodlagos

- Backyard Poultry cikk: **tapasztalati** termelési adatok, hasznos de nem kísérleti protokoll.
- LinkedIn / sajtó NRC 10. kiadás: **announcement**, részletes számok helyett a 1994/Merck táblázatot használtuk a számításokban.

## Bizonytalanságok — prioritás

1. **Napi adag** (g/tyúk) és **onetető** használat — ismeretlen.
2. Gabonák **tételszintű** ME, CP, toxin (penész).
3. **Parazita / oltás** állapot.
4. **Ólom / fészek** kapacitás (I. 1,5 éves tojók).
5. II. állomány **pontos nem-bontás** vágás után.
6. **Bio tanúsítás** — milyen kiegészítő engedett.
7. Tojástermelés **3–4 hetes trend** költözés után.
8. Vegyes I. állomány → **fajta szerinti** termelés eltérés.

## Számítások reprodukálása

A 3:1:1 súlyozott átlagok Python középérték-számítással készültek (2026-09-28 agent run). A pontos szkript **nem** került külön fájlba; a [takarmany-szamitasok.md](./takarmany-szamitasok.md) tartalmazza a végeredményeket és a feltételezéseket.
