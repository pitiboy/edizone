# Tyúkól intelligens, fokozatosan halványuló világítása — technológiai kutatás

**Dokumentum verzió:** 1.0  
**Kutatás dátuma:** 2026. október 15.  
**Helyszín:** Magyarország  
**Célterület:** ~6,25 m² (2,5 × 2,5 m), belmagasság ~2,5 m, ~30 tyúk  

> **Jogi és döntési figyelmeztetés:** Ez a dokumentum **kutatási és döntéselőkészítő** anyag. Nem minősül vásárlási, kivitelezési, villamos szerelési vagy állatgyógyászati jóváhagyásnak. A konkrét termékek és árak a lekérdezés napján ellenőrizhető forrásokból származnak; a hiányzó vagy nem igazolt adatok külön jelöléssel szerepelnek.

---

## 1. Vezetői összefoglaló

Egy ~6,25 m²-es tyúkól esti **fokozatos fényerő-csökkenését** (15–45 perc, villogás nélkül, végén teljes sötét) több architektúrával is meg lehet oldani. A kutatás szerint a **legfontosabb műszaki szűrő** nem a Wi-Fi vagy a telefonos app, hanem az, hogy a jelölt rendszer **igazolhatóan** támogat-e **programozható, folyamatos fényerő-rámpát** — sok „okos” vagy „LED” termék csak be/kikapcsolást vagy rövid (≤5 s) átmenetet kínál.

**Fő megállapítások:**

| Téma | Következtetés |
|------|----------------|
| **Követelmény-kritikus funkció** | 15–45 perces esti rámpa: legjobban **12 V PWM** (WLED Nightlight, ESPHome, ChickenLight 12, TC420) vagy **Shelly Dimmer Gen3 helyi ütemezés** (0,5–10 800 s átmenet) oldja meg hivatalos dokumentációval. A **Shelly Dimmer 2** max. **5 s** átmenet — önmagában **nem** felel meg hosszú naplemente-szimulációnak ([Shelly Dimmer 2 user guide](https://www.shelly.com/documents/user_guide/shelly_dimmer_2.pdf)). |
| **Internetfüggetlenség** | A napi működéshez **nem szükséges** folyamatos internet: WLED időzítő, ESPHome `sun` komponens, ChickenLight 12, Shelly **eszközön tárolt** ütemezés (NTP/időszinkron után) működhet helyi Wi‑Fi-n / offline órával. A **felhőközpontú** okosizzók (eWeLink-only scene, Hue account) gyengébbek áramszünet / felhőkimaradás esetén. |
| **Biztonság** | A tyúkól poros, párás, ammóniás környezet és **állati rágcsálás** miatt a **230 V-os falba süllyesztett dimmer** csak megfelelő **IP-védettségű lámpatesttel**, **zárt elhelyezéssel** és **szakember által végzett** szereléssel ajánlható alapként. **12 V SELV** rendszerrel a tyúkóli szakaszban alacsonyabb az érintésvédelmi kockázat, de a **230 V → 12 V tápegység** elhelyezése és védelme továbbra is kritikus ([MSZ EN 60598 / alacsonyfeszültségű világítás gyakorlat](https://eur-lex.europa.eu/)). |
| **Állatjólét (jog / ajánlás)** | A **2007/43/EK** broiler irányelv **20 lux** minimumot és sötét periódusokat ír elő **hústyúk tartására** — a házi ~30 tyúkos tartás **joghatása eltérő** (lásd 4. fejezet). A magyar **32/1999. FVM rendelet** általánosan előír sötét nyugalmi időt mesterséges világításnál ([NJT 32/1999](https://njt.jog.gov.hu/jogszabaly/1999-32-20-82)). |
| **Ajánlott csomagok (előzetes, jóváhagyás nélkül)** | **Olcsó:** 12 V WLED + ESP32 + tápegység + LED szalag. **Közepes:** Shelly Dimmer Gen3 + 0–10 V / trailing-edge kompatibilis fényforrás + helyi ütemezés. **Legjobb összesített:** 12 V ESPHome **vagy** ChickenLight 12 + minőségi PSU — erős helyi automatika, kevés felhőfüggés, javítható. |

**Kritikus tisztázandó kérdések** (részletesen 3. fejezet): van-e **nullvezeték** a tyúkólnál; melyik Wi‑Fi hálózat **ugyanahhoz a LAN/routerhez** tartozik; van-e **230 V konnektor vagy csak környező épület-villamos**; a tartás **házi baromfi / tojó / hústyúk** minősége.

---

## 2. Kiinduló követelmények és feltételezések

### 2.1 Rögzített helyszín- és állományadatok

- Magyarország, tyúkól ~6,25 m², belmagasság ~2,5 m.
- ~30 tyúk.
- Wi‑Fi elérhető (több SSID — **hálózati topológia nem ismert**).
- Nincs UTP/Ethernet a tyúkólnál.
- Elsődleges cél: olcsó, egyszerű, biztonságos, megbízható **esti fokozatos halványítás**.

### 2.2 Funkcionális elvárások (11 pont)

| # | Követelmény | Kutatási megjegyzés |
|---|-------------|---------------------|
| 1 | Automatikus esti elsötétítés | Ütemezés + rámpa |
| 2 | Beállítható rámaidő (15/20/30/45 perc) | Nem minden termék |
| 3 | Folyamatos, villogás nélküli csökkenés | PWM / trailing-edge minőségfüggő |
| 4 | Teljes kikapcsolás a végén | „0%” vs „off” különbség LED-nél |
| 5 | Heti / napi program | Eszköz- vagy központi szint |
| 6 | Manuális fényerő | App / gomb / web UI |
| 7 | Opcionális telefonos távoli vezérlés | LAN vs internet |
| 8 | Opcionális reggeli fokozatos felkapcsolás | Ugyanaz a rámpa-infrastruktúra |
| 9 | Újraindítás / áramszünet után kiszámíthatóság | `restore_mode`, RTC, NTP |
| 10 | Internetkimaradás mellett is automatikus működés | Helyi ütemezés prioritás |
| 11 | Későbbi módosíthatóság csere nélkül | Firmware / app / HA |

### 2.3 Mérnöki feltételezések (explicit, nem igazolt)

- A tyúkól **beltéri, nem fűtött** lehet; téli fagy és magas páratartalom valószínű.
- Egyetlen fő fényforrás vagy egy zóna elegendő lehet 6,25 m²-hez (**lux mérés javasolt** — 4. fejezet).
- A kutatás **nem** feltételez 230 V-os konnektort a tyúkólon belül; ha nincs, **12 V vagy távoli PSU** szükséges.

### 2.4 Skála az értékeléshez (1–5)

| Érték | Jelentés |
|-------|----------|
| 1 | Gyenge / magas kockázat / magas költség / nem igazolt |
| 2 | Korlátozott |
| 3 | Elfogadható kompromisszumokkal |
| 4 | Jó |
| 5 | Kiváló a kategóriájában |

**„N/I”** = nem igazolt / nincs elegendő adat.

---

## 3. Tisztázandó kérdések

Az alábbi kérdések **döntőek** a végleges architektúra és költség szempontjából. Kérjük, ezekre válasz nélkül ne zárjon le telepítési döntést.

### 3.1 Villamos és szerelési környezet

1. Van-e a tyúkólon belül **230 V CA konnektor** vagy csak **környező épületből** vezetett világítás?
2. Elérhető-e a **nullvezeték (N)** a tervezett dimmer helyén? (Shelly Gen3 nulla nélkül is megy, de **min. 20 W** vagy bypass — [Shelly KB Gen3](https://kb.shelly.cloud/knowledge-base/shelly-dimmer-gen3).)
3. Van-e **védőföld (PE)** és **FI/RCD** védelem** a vonalon?
4. Ki végezheti a szerelést: **jogosultsággal rendelkező villanyszerelő** szükséges-e (230 V bekötés, falba süllyesztés)?
5. Mekkora a **kábelút** tyúk → router/Wi‑Fi jel (műfal, fém, távolság)?

### 3.2 Hálózat

6. A „több Wi‑Fi” közül **melyik SSID** tartozik ahhoz a routerhez, amelyen **helyi LAN** elérés kell (telefon app / Home Assistant)?
7. Van-e ** vendég hálózat izoláció** (AP/client isolation), ami megakadályozza a helyi vezérlést?
8. Szükséges-e **interneten keresztüli** elérés, vagy elég a **helyi hálózat**?

### 3.3 Tartás és állatjólét

9. A ~30 tyúk **tojó**, **hústyúk**, vagy **vegyes házi** tartás? (Jogkövetelmények eltérnek.)
10. Van-e már **természetes fény** (ablak) — mennyi órán át?
11. Kívánt **nappali világítási idő** és **sötét periódus** hossza (óra)?

### 3.4 Üzemeltetés

12. Elfogadható-e **egyedi firmware** (WLED / ESPHome) karbantartása?
13. Mi a **katasztrófa forgatókönyv**: ha a lámpa hajnalig 100%-on marad, vagy hétig sötét van?

---

## 4. A világítási és állatjóléti követelmények

### 4.1 Megvilágítás mértéke és elhelyezés

- **Broiler / hústyúk (EU 2007/43/EK):** legalább **20 lux** a madár szemmagasságában, a hasznos felület **≥80%**-án világítási időszakban ([EUR-Lex 2007/43](https://eur-lex.europa.eu/eli/dir/2007/43/oj/eng)).
- **Mérési módszer (hivatalos ellenőrzés):** luxmérő, madár szemmagasság (~20–30 cm a talajtól), több pont — [EURCAW broiler light PDF](https://sitesv2.anses.fr/en/system/files/EURCAW-Poultry-SFA_2020-light-Broiler.pdf).
- **6,25 m² tyúkól, ~30 tyúk:** mérnöki **becslés** (nem helyettesíti a mérést): **1× 15–25 W LED** (~1500–2500 lm) vagy **2× 10–15 W** szétosztva **egyenletesebb** megvilágításért. A pontos lux **fényforrás szögétől, reflektortól és fal színétől** függ.

### 4.2 Színhőmérséklet és spektrum

- **Szakmai irányelv (általános baromfi):** meleg fehér **2700–3000 K** gyakori a nyugodt viselkedéshez; **nem** univerzális biológiai recept.
- **UV / spektrum:** a tyúk **látása eltér** az emberétől (UV-A érzékenység); lux ≠ „csirke lux” ([EURCAW](https://sitesv2.anses.fr/en/system/files/EURCAW-Poultry-SFA_2020-light-Broiler.pdf)).
- **Villódzás:** alacsony frekvenciájú PWM (<200 Hz) **esetleg** észrevehető; **≥1 kHz PWM** (ChickenLight 12: ~1,2 kHz — [Celtis](https://www.celtis.me/chickenlight12v)) vagy minőségi driver csökkenti a kockázatot.

### 4.3 Esti elsötétítés időtartama

- **EU broiler irányelv:** a **halványítási (twilight) idő** **nem** számít a kötelező sötét órákba ([2007/43](https://eur-lex.europa.eu/eli/dir/2007/43/oj/eng)).
- **Council of Europe ajánlás (idézve VKM összefoglaló):** „twilight period … sufficient to permit birds to settle” — **konkrét perc szám nincs** ([VKM PDF](https://vkm.no/download/18.1b70ef9115d3ac37645b2b5/1500030302470/7643446bd0.pdf)).
- **Felhasználói cél (15–45 perc):** etológiai szempontból **reális tartomány**; **állatorvos / baromfitartási tanácsadó** konzultáció javasolt egyedi állományra.

### 4.4 Magyar jogszabály (házi / általános baromfi)

- **32/1999. (III. 31.) FVM rendelet:** nem tartható **folyamatos sötétben**; mesterséges világításnál **sötét nyugalmi idő**; tojóknál **24 órás ritmus**, ~**nap harmada zavartalan sötét** ([NJT](https://njt.jog.gov.hu/jogszabaly/1999-32-20-82)).
- **1998. évi XXVIII. tv. állatvédelem:** a rendelet **kivételei** (pl. kedvtelésből tartott állat — **bizonytalan**, hogy a házi tyúk kategória) — **jogászi értelmezés szükséges** konkrét tartási módra ([NJT 1998/XXVIII](https://njt.jog.gov.hu/jogszabaly/1998-28-00-00)).
- **Következtetés:** a projekt **állatjóléti programját** (világítási órák, sötét idő) **dokumentálja**, és szükség esetén **NÉBIH / állatorvos** konzultáció.

---

## 5. A lehetséges architektúrák áttekintése

```
┌─────────────────────────────────────────────────────────────────┐
│  A. Önálló (internet nélkül / minimális)                        │
│     • Analóg időkapcsoló + fázishasító dimmer (gyenge rámpa)    │
│     • 12 V TC420 / LTD3 PC-programozott dimmer                  │
│     • ChickenLight 12 (PWM, napkelte/napnyugta)                 │
└─────────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────────┐
│  B. Okosotthon / Wi‑Fi                                          │
│     • Shelly Dimmer Gen3 (helyi schedule, 0.5–10800 s)          │
│     • Sonoff MINI Extreme Dimmer / D1 (eWeLink, korlátok)       │
│     • Okosizzó (Gyenge: rövid transition)                       │
│     • Hue + Bridge (rámpa max ~60 perc, bridge kötelező)        │
│     • Zigbee (Tradfri + HA/Z2M — központ kell)                  │
└─────────────────────────────────────────────────────────────────┘
┌─────────────────────────────────────────────────────────────────┐
│  C. Saját / hibrid                                              │
│     • ESP32 + WLED (Nightlight 1–255 perc)                      │
│     • ESPHome monokróm PWM + sun trigger                        │
│     • Shelly 0–10 V + Mean Well ELG dimmable driver             │
└─────────────────────────────────────────────────────────────────┘
```

**Internet szükségessége napi működéshez:**

| Architektúra | Napi működés internet nélkül |
|--------------|------------------------------|
| WLED időzítő + RTC/NTP egyszeri | **Igen** (NTP után) |
| ESPHome beágyazott automata | **Igen** |
| ChickenLight 12 | **Igen** (dátum/óra beállítás után) |
| Shelly Gen3 eszköz-ütemezés | **Részben** — időszinkron / napkelte offset-hez kezdeti beállítás; ütemezés eszközön ([shelly.guide scheduling](https://shelly.guide/en/app/scheduling/)) |
| Philips Hue automatizmus | **Nem megbízható** bridge + account nélkül |
| Tuya/eWeLink-only scene | **Gyenge** |

---

## 6. A konkrét termékjelöltek teljes táblázata

> **Árlekérdezés dátuma:** 2026-10-15, bruttó HUF, ha nincs jelezve: **szállítás és szerelés nélkül**.

### 6.1 Összefoglaló fő táblázat

| ID | Kategória | Gyártó / típus | Rámpa (igazolt) | Helyi auto. net nélkül | Távoli (telefon) | Becsült teljes rendszer (HUF) | HU beszerzés |
|----|-----------|----------------|-----------------|------------------------|------------------|-------------------------------|--------------|
| J1 | 12V WLED | ESP32 DevKit + WLED firmware | **1–255 perc** Nightlight ([WLED JSON API](https://kno.wled.ge/interfaces/json-api/)) | Igen (timer) | LAN + opcionális HA | ~25 000–45 000 | doitsmart, drot-elektro, LED shop |
| J2 | 12V baromfi | **ChickenLight 12** (Celtis) | Beállítható dimmidő (**N/I max perc**) | Igen | Nincs Wi‑Fi | ~55 000–95 000 | celtis.me (DE, EU szállítás) |
| J3 | 12V programozó | **TC420** USB idődimmer | PC profil (**N/I perc/részlet**) | Igen | Nem | ~35 000–60 000 | NL/HU import shop |
| J4 | 12V programozó | **LTD3 12V 20A** | Geleidelijk 0–100% lépések ([broedkooi](https://www.broedkooiverlichting.com/product/1784867/automatische-dimmer-ltd3-12v-20a)) | Igen | Nem | ~40 000–70 000 | NL shop |
| J5 | Wi‑Fi dimmer | **Shelly Dimmer Gen3** | **0,5–10 800 s** schedule action ([KB](https://kb.shelly.cloud/knowledge-base/shelly-dimmer-gen3)) | Részben | Igen (web/cloud) | ~45 000–120 000 | [Alza 18 690 Ft](https://www.alza.hu/shelly-gen3-dimmer-wifi-d13020888.htm) |
| J6 | Wi‑Fi 0–10V | **Shelly Gen3 0–10V** | Vezérli a drivert; rámpa = driver + beállítás | Részben | Igen | ~50 000–130 000 | [Alza 8 790 Ft](https://www.alza.hu/shelly-gen3-0-10-v-wifi-d12788356.htm) |
| J7 | Wi‑Fi dimmer | **Shelly Dimmer 2** | Max **5 s** ([PDF](https://www.shelly.com/documents/user_guide/shelly_dimmer_2.pdf)) | Részben | Igen | ~35 000–90 000 | HU viszonteladók |
| J8 | Wi‑Fi dimmer | **Sonoff D1** | **N/I** hosszú rámpa natívan; ESPHome **1 s** default ([ESPHome](https://esphome.io/components/light/sonoff_d1/)) | eWeLink időzítő | Igen | ~30 000–80 000 | hestore ~6991 Ft (készlet függő) |
| J9 | Wi‑Fi dimmer | **SONOFF MINI Extreme Dimmer** | **N/I** hosszú rámpa | Matter/WiFi | Igen | ~50 000–100 000 | [Alza ~12 590 Ft](https://www.alza.hu/olcso-fenyeroszabalyzok/sonoff/18881645-v12265.htm) |
| J10 | Zigbee | **IKEA TRÅDFRI** E27 + gateway | HA `transition` másodpercek (**max N/I** egy lépésben) | Gateway + HA | LAN HA-n keresztül | ~40 000–90 000 | IKEA HU |
| J11 | Zigbee/Bridge | **Philips Hue** + Bridge | Fade **≤60 perc** ([Android Authority / Hue app](https://www.androidauthority.com/philips-hue-sunrise-sunset-966513/)) | Bridge helyi | Igen | ~80 000–180 000 | MediaMarkt, stb. |
| J12 | Központi HA | **Home Assistant** (RPi 4/5) + integráció | Integrációfüggő | Igen (HA fut) | Igen | ~80 000–200 000+ | RPi + SSD |
| J13 | ESPHome | ESP32 + MOSFET + 12V LED | **`transition_length: 45min`** ([ESPHome light](https://esphome.io/components/light/)) | Igen | Opcionális HA/API | ~25 000–50 000 | DIY |
| J14 | Hibrid | ChickenLight 12 + Shelly **Plus 1** (monitor) | CL12 rámpa | Igen | Részleges | ~70 000–110 000 | Vegyes |
| J15 | Analóg | Időkapcsoló + **fázishasító** dimmer | Rossz / lépéses | Igen | Nem | ~15 000–35 000 | Barkács |
| J16 | Okosizzó | Generic Tuya WiFi bulb | **N/I** 30+ perc | Gyenge | Felhő | ~8 000–25 000 | eMAG |
| J17 | Zigbee | **Aqara** LED / dimmer + Hub M2 | **N/I** 45 perc natívan | Hub LAN | Igen | ~50 000–100 000 | eMAG, Xiaomi |
| J18 | Baromfi 12V | **Season Generator SOL-LED 12V** | Napkelte/napnyugta perc (**igazolt leírás**) | Igen | Nem | ~96 000+ (240 EUR) | [Redwing IT](https://www.allevamentoredwing.com/en/prodotti/season-generator-sol-led-12v/) |
| J19 | Wi‑Fi | **ESPHome + Sonoff D1** (flashed) | ESPHome transition (**igen**, de D1 lépésesség **N/I**) | Igen | Igen | ~25 000–55 000 | DIY |
| J20 | DALI | Shelly Gen3 DALI | DALI fade driverfüggő | Részben | Igen | ~60 000–150 000 | [Alza 20 490 Ft](https://www.alza.hu/shelly-gen3-dimmer-dali-wifi-d12726907.htm) |

**Aqara (J17):** Zigbee eszközök tipikusan **rövid** transitiont támogatnak; hosszú naplemente-rámpához **Home Assistant automatizmus** szükséges — ez **központi függőség**, ezért nem került a top 3 csomagba. Konkrét modell-specifikus max. fade idő: **N/I** (nem igazolt gyártói PDF).

**Season Generator (J18):** Professzionális madártenyésztő időzítő, **12 V**, két kimenet, buffer akku említve — túldimensionált ~30 házi tyúkhoz, de **referencia** baromfi-specifikus rámpára.

### 6.2 Tápegység és fényforrás (kiegészítő sorok)

| ID | Termék | Szerep | Ár (2026-10-15) | Forrás |
|----|--------|--------|-----------------|--------|
| P1 | V-TAC 60W 12V PSU | 12V rendszer | 3 300 Ft | [ledbau.hu 3246](https://ledbau.hu/led-tapegysegek-12v) |
| P2 | LED Solution 60W 12V | 12V rendszer | 4 980 Ft | [ledsolution.hu](https://www.ledsolution.hu/led-tapegyseg-trafo-12v-60w-belteri/) |
| P3 | Mean Well LPV-60-12 IP67 | Külső/biztonságosabb PSU | 7 567 Ft | [energiahaza.hu](https://www.energiahaza.hu/LED-tapegyseg-Mean-Well-LPV-60-12-60W-12V) |
| P4 | Mean Well **ELG** / **LCM** 0–10V | Dimmable constant voltage | ~15 000–35 000 Ft | Viszonteladók (**pontos modell: N/I**) |
| P5 | ESP32-DevKitC | WLED/ESPHome | 3 100–5 031 Ft | [doitsmart.hu](https://www.doitsmart.hu/shop/esp32-devkitc-38-pines-fejlesztopanel-wifi-es-bluetooth-kepesseggel-usb-c/), [drot-elektro.hu](https://www.drot-elektro.hu/arduino-platform/232741-esp32-devkitc-38pin-fejlesztoi-lap-usb-c.html) |

---

## 7. Részletes műszaki összehasonlítás

### 7.1 Fényerő-rámpa — kritikus szűrés

| Jelölt | Módszer | 15–45 perc rámpa | Bizonyíték |
|--------|---------|------------------|------------|
| **Shelly Dimmer Gen3** | Trailing edge 230 V | **Igen** (ütemezésben 0,5–10800 s) | Shelly KB Pro/Gen3 schedule „transition duration property” |
| **Shelly Dimmer 2** | Trailing edge | **Nem** (max 5000 ms) | User guide |
| **WLED** | PWM | **Igen** (Nightlight 1–255 min) | kno.wled.ge JSON API `nl.dur` |
| **ESPHome** | PWM | **Igen** (`transition_length`) | esphome.io light component |
| **ChickenLight 12** | PWM 1,2 kHz | **Igen** (dimmidő állítható, max **N/I**) | Celtis termékoldal |
| **Philips Hue** | Zigbee | **Részben** (max 60 perc fade) | Hue app dokumentáció / teszt |
| **IKEA Tradfri** | Zigbee | **Bizonytalan** (integráció / firmware) | GitHub HA issue #85535 |
| **Sonoff D1** | Triac | **N/I** natív hosszú | D1 API csak brightness 1–100 |

**Esti program minta (Shelly Gen3):**  
1) Nappali fény 100% → 2) Ütemezett esemény: `brightness=0%`, `transition=1800` s (30 perc) → 3) `on=false`. **Két lépés szükségessége** és a „off” viselkedés LED típussal **mérés előtt N/I**.

### 7.2 Kompatibilitás és terhelés

- **Shelly Gen3 trailing edge:** max **150 W dimmelhető LED**; nullával **nincs min. terhelés** ([KB](https://kb.shelly.cloud/knowledge-base/shelly-dimmer-gen3)).
- **12 V:** ChickenLight max **50 W** lámpaterhelés ([Celtis](https://www.celtis.me/chickenlight12v)).
- **6,25 m²:** tipikus LED teljesítmény **10–30 W** — mindkét architektúra feleslegesen nagy fejezet.

---

## 8. Kompatibilitási és műszaki kockázatok

| Kockázat | Érintett jelöltek | Mitigation |
|----------|-------------------|------------|
| LED nem dimmelhető 230 V triacon | J5, J7, J8 | **Explicit „dimmable”** lámpa; compat lista |
| Alacsony fényen villogás | Triac, rossz driver | 12 V PWM; min brightness tuning Shelly-n |
| „Off” után halvány fény | Shelly nulla nélkül | Nullvezeték vagy bypass |
| Wi‑Fi 2,4 GHz lefedettség | Minden Wi‑Fi | AP közelebb; ESP8266/32 |
| Több SSID, más subnet | B kategória | Ugyanaz a LAN; mDNS |
| Tyúk kábel rágás | Minden | **12 V** tyúk zónában; csatorna, magas elvezetés |
| Ammónia / pára | Elektronika | IP40+ burkolat; PSU **tyúk zónán kívül** |
| Idő eltérés napkelte után | Shelly/WLED | Szezonális offset; manuális finomhangolás |

---

## 9. Biztonsági elemzés

### 9.1 Villamos biztonság

- **230 V tyúkólon:** érintésvédelmi és tűzvédelmi kockázat **magasabb**; MSZ EN szabványok szerinti **lámpatest, védelem, szerelés** — **szakember**.
- **12 V SELV** a madarak elérése közelében: **alacsonyabb** érintés kockázat; rövidzárlat / túláram → **biztosíték**, megfelelő **AWG/keresztmetszet**, **Mean Well** jó minőségű PSU.
- **Túlmelegedés:** dimmer / PSU ne legyen szalmán, fa porban zárt dobozban **ventiláció nélkül**.

### 9.2 Tűz és hibamód

| Hiba | Következmény | Enyhítés |
|------|--------------|----------|
| Beragadt 100% | Kevesebb sötét idő, stressz | Heti ellenőrzés; mechanikus bypass kapcsoló |
| Beragadt off | Sötét, baleset | Tartalék zseblámpa ellenőrzéshez |
| Dimmer meghibásodás rövidzárlat | Túláram | 16 A B/C automata; minőségi dimmer |

### 9.3 Informatikai biztonság

- Shelly / Sonoff **cloud account** → jelszó, 2FA ahol van.
- **Távoli elérés** csak szükség esetén; helyi vezérlés prioritás.

---

## 10. Internet-, Wi‑Fi- és felhőfüggőség

| Jelölt | Wi‑Fi szükséges napi | Felhő szükséges | Megjegyzés |
|--------|----------------------|-----------------|------------|
| J1 WLED | Opcionális (után nem) | Nem | Idő makrók eszközön |
| J2 ChickenLight | Nem | Nem | |
| J5 Shelly Gen3 | Igen (helyi) | Nem kötelező | App/cloud opcionális |
| J11 Hue | Bridge LAN | Account setup | Napi: bridge |
| J12 HA | LAN | Nem | Központ SPOF |

**Több Wi‑Fi hálózat:** feltételezés, hogy **nem** ugyanaz a router — távoli vezérléshez **ugyanaz a L2/L3 hálózat** vagy **VPN** szükséges (tisztázandó, 3. fejezet).

---

## 11. Hibaforgatókönyvek és helyreállítás

Skála: **L** = világítás állapota, **A** = automata program, **H** = emberi beavatkozás, **É** = észrevételi valószínűség.

| # | Esemény | L | A | H | Biztonságos helyreállítás | É |
|---|---------|---|---|---|---------------------------|---|
| 1 | Internet kimarad | J1/J2/J5: normál | Fut | Nem | — | Alacsony |
| 2 | Router újraindul | Wi‑Fi eszköz reconnect | Fut időzítés | Nem | Várni | Közepes |
| 3 | HA leáll | J12: utolsó állapot | Megáll | Igen | HA restart | Magas ha csak HA |
| 4 | Felhő down | Shelly helyi web: OK | Fut | Nem | Helyi IP | Alacsony |
| 5 | Áramszünet | Off | Megáll | Nem | NTP szinkron után | Közepes |
| 6 | Visszatérő áram | restore_mode függő | Újraindul | Ellenőrizni | WLED/Shelly beállítás | Közepes |
| 7 | Idő/config elveszik | Rossz időpont | Rossz | Igen | Újrabeállítás | Magas |
| 8 | Dimmer hibás | Off vagy ON | Nem | Igen | Csere | Magas |
| 9 | Dimmer stuck ON | 100% | Nem | Igen | Kapcsoló elé | **Magas** |
| 10 | App/account nem elérhető | Helyi web/WLED UI | Fut | Nem | LAN böngésző | Alacsony |

**Preferált:** J1, J2, J5 **helyi ütemezéssel**, nem csak felhő scene-nel.

---

## 12. Teljes költségmodell és hároméves TCO

### 12.1 Közös feltételezések

- **Áram:** ~40 Ft/kWh (2026-os **becslés**, **N/I** hivatalos ár).
- **LED átlag teljesítmény:** 20 W névleges, **effektív 12 W** (dimmed + rövid nappali).
- **Napi üzem:** 10 h „világítási ablak”, átlag 60% fény → ~12 W × 10 h = **0,12 kWh/nap** → ~44 kWh/év → **~1 760 Ft/év**.
- **Szerelés szakemberrel (230 V):** **15 000–40 000 Ft** egyszeri (**becslés**, piaci).
- **TCO 3 év** = beruházás + 3× energia + 3× karbantartás (0–5 000 Ft/év DIY).

### 12.2 Csomagonkénti beruházás (részletes)

#### Olcsó — WLED 12 V (J1)

| Tétel | Ft |
|-------|-----|
| ESP32 DevKit | 3 100–5 000 |
| 60W 12V PSU (P1/P2) | 3 300–5 000 |
| LED szalag / modul 2700K ~5 m IP65 | 8 000–15 000 |
| MOSFET modul / WLED board | 0–3 000 |
| Doboz, WAGO, biztosíték, kábel | 5 000–10 000 |
| Szállítás | 2 000–4 000 |
| **Összesen** | **~21 000–42 000** |
| 3 év TCO (+ energia) | **~26 000–48 000** |

#### Közepes — Shelly Gen3 + dimmelhető 230 V lámpa (J5)

| Tétel | Ft |
|-------|-----|
| Shelly Dimmer Gen3 | 18 690 |
| Dimmelhető LED panel/izzó 2× ~15W | 10 000–25 000 |
| Burkolat, vezeték (ha engedélyezett) | 5 000–15 000 |
| Villanyszerelő (opcionális) | 0–35 000 |
| **Összesen** | **~34 000–94 000** |
| 3 év TCO | **~39 000–110 000** |

#### Közepes alternatíva — ChickenLight 12 (J2)

| Tétel | Ft |
|-------|-----|
| ChickenLight 12 (~98 EUR) | ~39 000 (1 EUR≈400 Ft **becslés**) |
| PSU + LED | 10 000–20 000 |
| Szállítás DE→HU | 3 000–8 000 |
| **Összesen** | **~52 000–67 000** |
| 3 év TCO | **~57 000–73 000** |

#### Legjobb összesített — ESPHome 12 V (J13)

Hasonló J1-hez + **~0 Ft szoftver**, esetleg **Home Assistant** opcionális (+25 000–60 000 ha már nincs).

---

## 13. Súlyozott értékelés és érzékenységvizsgálat

### 13.1 Kezdeti súlyok (elemzési)

| Dimenzió | Súly |
|----------|------|
| Biztonság | 20% |
| Hibatűrés / üzembiztonság | 20% |
| Egyszerűség / kezelhetőség | 15% |
| Teljes költség / ár-érték | 20% |
| Internetfüggetlenség | 10% |
| Távoli hozzáférés | 5% |
| Karbantarthatóság / bővíthetőség | 10% |

**Biztonsági kizáró feltétel:** J15 (nyílt áramkör barkács 230 V), nem minősített Tuya 230 V **ajánlás nélkül** kiesnek a „ajánlott” listából.

### 13.2 Pontszámok (1–5) — fő jelöltek

| Dimenzió | J1 WLED 12V | J2 ChickenLight | J5 Shelly Gen3 | J11 Hue | J12 HA |
|----------|-------------|-----------------|----------------|---------|--------|
| Bekerülési költség (↓ jobb) | 5 | 3 | 4 | 2 | 2 |
| 3 év TCO (↓) | 5 | 4 | 4 | 2 | 2 |
| Ár-érték | 5 | 4 | 4 | 3 | 3 |
| Komplexitás (↓) | 3 | 4 | 3 | 4 | 1 |
| Kezelhetőség | 3 | 4 | 4 | 5 | 3 |
| Távoli elérés | 4 | 1 | 4 | 5 | 5 |
| Internetfüggetlenség | 5 | 5 | 4 | 2 | 4 |
| Wi‑Fi függés (↓) | 3 | 5 | 3 | 3 | 3 |
| Robusztusság | 4 | 4 | 3 | 4 | 3 |
| Hibatűrés | 4 | 5 | 4 | 3 | 3 |
| Karbantarthatóság | 4 | 3 | 4 | 3 | 4 |
| Bővíthetőség | 4 | 2 | 4 | 4 | 5 |
| Biztonság (12V/SELV) | 5 | 5 | 3* | 3* | 3* |
| Fényerő-rámpa | 5 | 4 | 5 | 4 | 5 |
| Beszerezhetőség | 4 | 3 | 5 | 4 | 4 |
| Gyártói függőség (↓) | 5 | 4 | 4 | 2 | 4 |

\*Shelly/Hue 230 V: biztonság **telepítéstől függ** — megfelelő szereléssel 4.

### 13.3 Súlyozott összpontszám (becslés, normalizált 1–5 skála)

| Jelölt | Súlyozott átlag |
|--------|-----------------|
| **J1 WLED 12V** | **~4,3** |
| **J2 ChickenLight 12** | **~4,0** |
| **J5 Shelly Gen3** | **~3,8** |
| J13 ESPHome | ~4,2 |
| J11 Hue | ~3,0 |
| J12 HA-only | ~2,9 |

### 13.4 Érzékenység

- **Ha az ár súlya 35%:** J1, J3, J4 emelkedik; J2, J5 közelebb egymáshoz.
- **Ha megbízhatóság + hibatűrés 35%:** J2, J1 (egyszerűbb mint HA), J5 (helyi schedule) előrébb; Hue visszaesik.

---

## 14. Olcsó megoldás (csomag A)

**Javasolt összetétel:** **12 V WLED** (J1) — ESP32 + Mean Well / V-TAC PSU + meleg fehér LED szalag + védő doboz.

| Elem | Modell / megjegyzés |
|------|---------------------|
| Vezérlő | ESP32 + [WLED](https://kno.wled.ge/) |
| Rámpa | Nightlight mode 1 vagy 3, `dur` 15–45 ([API](https://kno.wled.ge/interfaces/json-api/)) |
| Időzítés | WLED Time & Macros — sunset offset ([Macros](https://kno.wled.ge/features/macros/)) |
| Távoli | Telefon böngésző `http://wled-xxxx.local` helyi Wi‑Fi |

**Bekerülés:** ~21 000–42 000 Ft (12. fejezet).

**Korlátozások:** Első konfiguráció Wi‑Fi + PC/telefon; firmware frissítés saját felelősség; **nincs** gyári CE „tyúkól csomag”.

**Biztonsági feltételek:** PSU és 230 V csatlakozás **tyúk zónán kívül**; 12 V oldalon **mechanikai védelem**.

**Hibák:** Áramszünet után WLED restore beállításoktól függ; NTP szükséges pontos időhöz.

---

## 15. Közepes árú megoldás (csomag B)

**Javasolt összetétel:** **Shelly Dimmer Gen3** + **2× dimmelhető E27 LED** (~15 W) + **nullvezeték** (ha elérhető) + helyi **Advanced Schedule**.

| Elem | Funkció |
|------|---------|
| Esti rámpa | Egy ütemezés: brightness 0%, transition **900–2700 s** |
| Reggeli (opc.) | Ellentétes rámpa |
| Távoli | Shelly app / helyi web UI, cloud opcionális |

**Bekerülés:** ~34 000–94 000 Ft (szereléssel).

**Kompromisszumok:** 230 V a tyúkóli közelében; triac kompatibilitás; **Shelly Dimmer 2 ne** legyen hosszú rámpára.

**Alternatíva ugyanazon áron:** **ChickenLight 12** — kevesebb telefon, több „baromfi-specifikus” logika, nincs Wi‑Fi.

---

## 16. Legjobb összesített megoldás (csomag C)

**Javasolt összetétel:** **ESPHome 12 V monokróm PWM** (J13) *vagy* **WLED (J1)** — döntés a **programozási preferencia** alapján (YAML vs makró).

**Indoklás:** Igazolt **45 perc** `transition_length`; beépített **`sun` trigger** napnyugtához ([ESPHome sun](https://esphome.io/components/sun/)); **internet nélkül** fut; 12 V a madár-zónában; költség kedvező.

**Opcionális bővítés:** Home Assistant csak távoli felülethez — **nem** kötelező a napi rámpához.

**Ha zero DIY:** **ChickenLight 12** + minőségi 12 V LED — kevesebb karbantartás, magasabb ár.

---

## 17. A jelöltek kizárásának indokai

| Jelölt | Indok |
|--------|-------|
| Shelly Dimmer 2 (J7) | Max 5 s transition — nem teljesíti 15–45 perc követelményt |
| Sonoff D1 (J8) | Hosszú rámpa nem igazolt; gyártó out of stock |
| Generic Tuya okosizzó (J16) | Rámpa / offline N/I; felhőfüggés |
| Fázishasító + időkapcsoló (J15) | Biztonság / rámpa minőség / tyúk környezet |
| Hue (J11) | Bridge költség, 60 perc fade limit, ökoszisztéma zárt |
| HA-only (J12) | Központ SPOF — önmagában nem minimál |
| IKEA Tradfri (J10) | Hosszú fade + gateway + integráció kockázat |

---

## 18. Nyitott kérdések és bizonytalanságok

- ChickenLight 12 **maximális dimmidő** percben — **N/I** (csak „einstellbar”).
- TC420 / LTD3 **pontos lépésszám** 45 perces sima görbéhez — **N/I**.
- Tyúkól **lux értékek** mérés nélkül — **becslés**.
- **EUR/HUF** árfolyam ChickenLight-nál — becslés használva.
- Sonoff MINI Extreme **transition max** másodperc — **N/I** (marketing: flicker-free).
- Shelly Gen3 schedule **internet szükséges-e első napkelte synchez** — dokumentáció ellentmondásos (web UI vs shelly.guide); **helyi teszt szükséges**.

---

## 19. Beszerzési lista és ellenőrizhető terméklinkek

### 19.1 Olcsó csomag (WLED)

| Darab | Termék | Link |
|-------|--------|------|
| 1 | ESP32 DevKitC USB-C | https://www.doitsmart.hu/shop/esp32-devkitc-38-pines-fejlesztopanel-wifi-es-bluetooth-kepesseggel-usb-c/ |
| 1 | 12V 60W PSU V-TAC 3246 | https://ledbau.hu/led-tapegysegek-12v |
| 1 | WLED dokumentáció | https://kno.wled.ge/ |
| ~5 m | LED szalag 2700K IP65 | Helyi LED shop (**modell: N/I**) |

### 19.2 Közepes csomag (Shelly)

| Darab | Termék | Link |
|-------|--------|------|
| 1 | Shelly Dimmer Gen3 | https://www.alza.hu/shelly-gen3-dimmer-wifi-d13020888.htm |
| 2 | Dimmelhető LED E27 | Gyártói compat lista (**N/I modell**) |
| — | Shelly KB | https://kb.shelly.cloud/knowledge-base/shelly-dimmer-gen3 |

### 19.3 Baromfi-specifikus

| Darab | Termék | Link |
|-------|--------|------|
| 1 | ChickenLight 12 | https://www.celtis.me/chickenlight12v |

### 19.4 Hibrid 0–10V (haladó)

| Darab | Termék | Link |
|-------|--------|------|
| 1 | Shelly Gen3 0–10V | https://www.alza.hu/shelly-gen3-0-10-v-wifi-d12788356.htm |
| 1 | Mean Well LPV-60-12 | https://www.energiahaza.hu/LED-tapegyseg-Mean-Well-LPV-60-12-60W-12V |

---

## 20. Forrásjegyzék

| # | Forrás | URL | Hozzáférés |
|---|--------|-----|------------|
| 1 | Shelly Dimmer 2 User Guide | https://www.shelly.com/documents/user_guide/shelly_dimmer_2.pdf | 2026-10-15 |
| 2 | Shelly Dimmer Gen3 KB | https://kb.shelly.cloud/knowledge-base/shelly-dimmer-gen3 | 2026-10-15 |
| 3 | Shelly scheduling guide | https://shelly.guide/en/app/scheduling/ | 2026-10-15 |
| 4 | WLED JSON API | https://kno.wled.ge/interfaces/json-api/ | 2026-10-15 |
| 5 | WLED Macros / Time | https://kno.wled.ge/features/macros/ | 2026-10-15 |
| 6 | ESPHome Light | https://esphome.io/components/light/ | 2026-10-15 |
| 7 | ESPHome Sun | https://esphome.io/components/sun/ | 2026-10-15 |
| 8 | ChickenLight 12 Celtis | https://www.celtis.me/chickenlight12v | 2026-10-15 |
| 9 | EU Directive 2007/43 | https://eur-lex.europa.eu/eli/dir/2007/43/oj/eng | 2026-10-15 |
| 10 | EURCAW Light broiler | https://sitesv2.anses.fr/en/system/files/EURCAW-Poultry-SFA_2020-light-Broiler.pdf | 2026-10-15 |
| 11 | HU 32/1999 FVM | https://njt.jog.gov.hu/jogszabaly/1999-32-20-82 | 2026-10-15 |
| 12 | Philips Hue sunset automation | https://www.androidauthority.com/philips-hue-sunrise-sunset-966513/ | 2026-10-15 |
| 13 | Alza Shelly Gen3 ár | https://www.alza.hu/shelly-gen3-dimmer-wifi-d13020888.htm | 2026-10-15 |
| 14 | Sonoff D1 ITEAD | https://itead.cc/product/sonoff-d1-smart-dimmer-switch/ | 2026-10-15 |
| 15 | LTD3 dimmer | https://www.broedkooiverlichting.com/product/1784867/automatische-dimmer-ltd3-12v-20a | 2026-10-15 |
| 16 | Sonoff D1 API | https://help.sonoff.tech/docs/D1-API | 2026-10-15 |
| 17 | Season Generator SOL-LED | https://www.allevamentoredwing.com/en/prodotti/season-generator-sol-led-12v/ | 2026-10-15 |
| 18 | Farmtronics LD dimmer module | https://www.farmtronics.com.au/store/LD-Light-Dimming-Module-p833825073 | 2026-10-15 |

---

## 21. Javasolt következő lépések (jóváhagyást igénylő)

1. **Válasz** a 3. fejezet tisztázó kérdéseire (nullvezeték, Wi‑Fi topológia, 230 V elérhetőség, tartás típusa).
2. **Lux mérés** üres tyúkólban prototípus fényforrással (telefon lux app **csak orientáció**, kalibrált mérő jobb).
3. **Döntés** 12 V vs 230 V architektúráról — **biztonság elsődleges**.
4. **Pilot:** egy jelölt (J1 vagy J5) **egyetlen esti rámpával** — viselkedés megfigyelése (ugrik-e, marad-e halvány fény).
5. **Villamos szerelés** jóváhagyása szakemberrel, ha 230 V.
6. **Állatorvos / baromfi tanácsadó** — sötét/idő program véglegesítése tojó/hústyúk profilhoz.
7. **Telepítés és vásárlás** — csak a fenti lépések után, külön felhasználói jóváhagyással.

---

*Dokumentum készítette: Cloud Agent kutatás — repository: workspace root, branch: `cursor/tyukol-vilagitas-kutatas-44ad`.*
