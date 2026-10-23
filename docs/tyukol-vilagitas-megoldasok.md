# Tyúkól intelligens, fokozatosan halványuló világítása — technológiai kutatás

**Dokumentum verzió:** 1.5 (30–40 tyúk/óla, BOM Modulshop+240volt, távoli VPN)  
**Kutatás dátuma:** 2026. október 15.  
**Utolsó frissítés:** 2026. október 23.  
**Telepítési terv + beszerzés:** [tyukol-vilagitas-wled-2ol-telepitesi-terv.md](./tyukol-vilagitas-wled-2ol-telepitesi-terv.md)  
**Helyszín:** Magyarország  
**Célterület:** ~6,25 m² (2,5 × 2,5 m), belmagasság ~2,5 m, **~30–40 tyúk / óla**  

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
| **Döntött megoldás (2026-10-21, BOM 2026-10-23)** | **WLED + ESP32 + 1× 12 V PSU + 2× analóg PWM szalag** — **2 db**, 3–4 m-re egymástól lévő **azonos óla**, **1 vezérlő**, **12→5 V buck** az ESP-nek. Részletek: [telepítési terv](./tyukol-vilagitas-wled-2ol-telepitesi-terv.md). **Becsült BOM ~38–40 e Ft** (Modulshop + 240volt + barkács). **Távoli:** Cudy **DDNS + WireGuard** (port forward helyett). |
| **Shelly Gen3** | Elvetve a felhasználói WLED döntés miatt; alternatíva maradt a kutatásban. |

**Helyszín profil:** **házi vegyes tojó** (barna, fehér, kendermagos, kopasznyakú), **2 azonos ól** 3–4 m távolságban, cél **14 h + 10 h sötét**, **téli tojás** (korábbi reggeli fény télen), **2 ablak**, sötét falu, **MultiPlus-II 3000**, **FI 16 A**, **Cudy 4G** + **RE315 Repeater**, távoli elérés **opcionális**, üzem **automata**.

---

## 2. Kiinduló követelmények és feltételezések

### 2.1 Rögzített helyszín- és állományadatok

- Magyarország, **2×** tyúkól ~6,25 m² (azonos), **3–4 m** távolság, belmagasság ~2,5 m.
- **~30–40 tyúk / óla**, **házi vegyes tojó** (magyar barna, fehér, kendermagos, kopasznyakú).
- **Fotoperiódus cél:** **14 óra fény + 10 óra sötét** (24 órás ciklus).
- **Természetes fény:** **2 ablak** két oldalon (évszakonként változó hozzájárulás).
- **Villamos ellátás:** **Victron MultiPlus-II 3000** szigetüzem; tyúkól **230 V / N / PE** az inverter kimenetéről; **16 A FI védelem** a kimeneten.
- **Környezeti fény:** **nincs redőny**; a település **sötét**, **nincs fényszennyezés** — hold / hajnal **alacsony háttérfény**, de **nem** városi szint.
- Wi‑Fi: **4G Wi‑Fi modem** + **TP‑Link RE315** (AC1200) **Repeater** mód; nincs UTP a tyúkólnál.
- **DIY firmware (WLED/ESPHome)** elfogadható, ha **egyszerűen** karbantartható.
- Elsődleges cél: olcsó, egyszerű, biztonságos, megbízható **esti fokozatos halványítás** a **10 órás sötét blokk** elején.

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
- A **230 V** a helyszínen van: **Shelly Gen3 trailing-edge** és **230 V → 12 V PSU** is reális; a **nullvezetés** miatt **nincs szükség** 20 W bypass-ra alacsony terhelésnél ([Shelly KB](https://kb.shelly.cloud/knowledge-base/shelly-dimmer-gen3)).

### 2.4 Felhasználói visszajelzés

| Kérdés | Válasz | Következmény a tervezésre |
|--------|--------|---------------------------|
| 230 V / N / PE a tyúkólnál? | **Igen** (Victron kimenet) | Shelly Gen3 **N-nel**; **12 V PSU** is az inverter 230 V-ról; lásd **9.4** szigetüzem. |
| Tartás | **Házi vegyes tojó**, **30–40 db / óla** | 4.5 **14/10** program; **~3 m / ~7–8 W** szalag/óla (telepítési terv); broiler 20 lux **kötelező** nem cél, de **32/1999** sötét idő releváns. |
| Fény / sötét cél | **14 h + 10 h** | Fix órás váz (4.5); **ablak** miatt szezonális finomhangolás. |
| Ablak | **2 db**, redőny **nincs** | Nappali természetes fény változik; **sötét 10 h:** alacsony **holdfény** behatolhat — **falu széle, nincs fényszennyezés** → **általában elfogadható** sötét (felhasználó); **holdteli éjszaka** még mindig enyhe fény az ablakon (**N/I** lux). |
| Victron | **MultiPlus-II 3000** | **Tiszta szinusz** — **Shelly triac** és **12 V PSU** kompatibilitás **jó várakozás** (9.4); gyári spec: tiszta szinusz AC kimenet. |
| FI védelem | **16 A FI** inverter kimeneten | **Igen, FI relére / FI megszakítóra gondoltunk** — a leírásod **megfelelő**; lásd 9.4. |
| Wi‑Fi | **RE315 Repeater** + 4G modem | Dupla rádióugrás, **eszköz-ütemezés kötelező** (10.1). |
| DIY firmware | **Igen, egyszerű** | **WLED** elsődleges. |
| Lux | „Elég fény” + számítás | 4.1.1; **2× ~10 W** továbbra is reális. |

### 2.5 Skála az értékeléshez (1–5)

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

### 3.1 Megválaszolt

- **230 V / N / PE** a tyúkólnál (Victron szigetüzem kimenet).
- **FI:** 16 A FI védelem az inverter kimenetén (FI megszakító + FI relé — felhasználói rendszer).
- **Tartás:** házi vegyes tojó; **14 h fény + 10 h sötét** cél.
- **2 ablak** két oldalon.
- **Wi‑Fi:** 4G modem + **TP‑Link RE315** **Repeater**.
- **DIY:** WLED/ESPHome OK, egyszerűség preferált.

### 3.2 Továbbra is nyitott (opcionális finomítás)

1. Tyúkól ↔ **RE315 ↔ modem** távolság és **jelminőség** (dBm) — gyenge jel esetén WLED idő drift + offline vezérlés.
2. **Katasztrófa tolerancia** és **távoli elérés** szükségessége (4G-n kívülről).
3. **Tojástermelés** célja: téli fény **pótlás** prioritás — befolyásolja a reggeli bekapcsolás időpontját.
4. **Hold / kelő nap** lux az ablakon a 20:00–06:00 blokkban — opcionális **egyszeri mérés** sötétben (ha aggodalom van).

---

## 4. A világítási és állatjóléti követelmények

### 4.1 Megvilágítás mértéke és elhelyezés

- **Broiler / hústyúk (EU 2007/43/EK):** legalább **20 lux** a madár szemmagasságában, a hasznos felület **≥80%**-án világítási időszakban ([EUR-Lex 2007/43](https://eur-lex.europa.eu/eli/dir/2007/43/oj/eng)).
- **Mérési módszer (hivatalos ellenőrzés):** luxmérő, madár szemmagasság (~20–30 cm a talajtól), több pont — [EURCAW broiler light PDF](https://sitesv2.anses.fr/en/system/files/EURCAW-Poultry-SFA_2020-light-Broiler.pdf).
- **6,25 m² tyúkól, ~30–40 tyúk:** mérnöki **becslés** (nem helyettesíti a mérést): **1× 15–25 W LED** (~1500–2500 lm) vagy **2× 10–15 W** szétosztva **egyenletesebb** megvilágításért. A **döntött WLED terv** **~7–8 W / óla** (~3 m 12 V szalag) — **~50–65 lux** átlag becslés (30–40 madárnál több árnyék miatt **ne** 6 W alá menni). A pontos lux **fényforrás szögétől, reflektortól és fal színétől** függ.

#### 4.1.1 Lux-becslés „elég fény” alapon (6,25 m², ~2,5 m belmagasság)

**Módszer (egyszerűsített):** átlagos fényerősség a talaj síkján, madár szemmagasság ~25 cm:

\[
E_\mathrm{átl} \approx \frac{\Phi_\mathrm{lm} \cdot \eta_\mathrm{szoba}}{A}
\]

ahol \(A = 6{,}25\,\mathrm{m}^2\), \(\Phi_\mathrm{lm}\) = fényforrás fényáram (lm), \(\eta_\mathrm{szoba}\) = **0,35–0,55** (kis, világos fal, diffúz/reflektoros LED; **becslés**).

| Konfiguráció | Névleges teljesítmény | Becsült lm (100 lm/W) | Becsült \(E_\mathrm{átl}\) (lux) | Megjegyzés |
|--------------|----------------------|------------------------|----------------------------------|------------|
| 1× 10 W E27/panel, mennyezet közép | 10 W | ~1000 lm | **~56–88** | Középen erősebb, sarkok gyengébb |
| 1× 15 W | 15 W | ~1500 lm | **~84–132** | „Elég fény” házi tyúkólra **általában bőven** |
| 2× 10 W, szétosztva | 20 W | ~2000 lm | **~112–176** | Egyenletesebb; **ajánlott** ha percek alatt jár a madár |
| 1× 12 W LED szalag (12 V, diffúz) | 12 W | ~1200 lm | **~67–106** | Szalag hossza/elosztás függő |

**Referencia küszöbök (nem mindegyik kötelező házi tartásra):**

| Szempont | Lux szint | Forrás / értelmezés |
|----------|-----------|---------------------|
| EU broiler minimum (hústyúk telep) | **≥20** a hasznos felület 80%-án | [2007/43/EK](https://eur-lex.europa.eu/eli/dir/2007/43/oj/eng) |
| Házi „elég fény” cél (mérnöki) | **~30–80 átlag** | A fenti 10–15 W tartomány |
| Esti rámpa vége | **→0** (sötét pihenő) | 32/1999 FVM sötét idő |

**Dimmelés:** ~lineáris lux ≈ fényerő % (LED PWM-nél közelítőleg). 30 perc alatt 100% → 0%: átlag ~50% fényerő → **~fél lux-szint** időintegrálva — a **biológiai hatás** nem azonos a hirtelen kikapcsolással; ezért a **fokozatos rámpa** célja.

**Gyakorlati javaslat (jóváhagyás nélkül):** **2× ~10 W, 2700–3000 K**, magas elhelyezés, **nem** vakító irány a ülőrudak felé; esti program végén **teljes off**. Ha a sarkok sötétek, **mérj** (olcsó luxmérő ~3000–8000 Ft) 5 ponton, üres ólban.

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

### 4.5 Házi vegyes tojó — 14 h fény + 10 h sötét program (műszaki váz)

**Felhasználói cél:** 24 órában **14 óra „világított időszak”** + **10 óra zavartalan sötét** (a **halványítási rámpa** ideje a sötétbe vezet, hasonlóan az EU broiler gyakorlathoz, ahol a twilight **nem** számít sötétnek — [2007/43](https://eur-lex.europa.eu/eli/dir/2007/43/oj/eng)).

**Fontos:** a tyúk a **2 ablak miatt** nyáron **több természetes fényt** kap; télen **kevesebbet**. A **14 h** cél **fény + természetes + mesterséges összesített** élmény; a vezérlés **mesterséges fényforrást** kapcsol.

#### 4.5.1 Példa fix órás váz (jóváhagyás / finomhangolás előtt)

| Fázis | Óra (példa) | Mesterséges fény | Megjegyzés |
|-------|-------------|------------------|------------|
| Sötét blokk | **20:00 → 06:00** (10 h) | **Ki** (0%) | **Nincs redőny**; **sötét falu** → alacsony háttérfény; **holdteli** enyhén világíthat |
| Reggeli felkapcsolás (opc.) | 06:00 → 06:30 | Rámpa 0→100% (30 perc) | WLED Nightlight / Shelly transition |
| Nappali fény időszak | 06:30 → 19:30 | 100% (vagy alacsonyabb max) | Ha nappali ablak fény **elég**, lehet **alacsonyabb %** (N/I luxmérés) |
| Esti naplemente rámpa | **19:30 → 20:00** (30 perc) | 100% → 0% folyamatos | **Központi követelmény** |
| Sötét | 20:00-tól | Off | 10 h |

**Ellenőrzés:** 06:00–20:00 = **14 h** „világos ablak” (rámpákkal együtt a madár számára fokozatos); 20:00–06:00 = **10 h** sötét.

#### 4.5.2 Ablakok hatása

| Évszak | Hatás | Automatizálási következmény |
|--------|-------|-----------------------------|
| Nyár | Hosszú természetes fény | **Túl hosszú** fényperiódus kockázata, ha mesterséges is megy — **szezonális** korábbi esti off vagy max fényerő csökkentés |
| Tél | Rövid nap | Mesterséges **14 h** pótlás fontosabb; reggeli **06:00** be kapcsolás indokolt |
| Egész év | 2 oldali ablak, **sötét környezet** | **Esti/éjszakai** külső fény **minimális** (nincs fényszennyezés) → **redőny hiánya kevésbé kritikus**, mint városban; **2× fényforrás** (4.1.1) továbbra is indokolt |

**Napkelte/napnyugta kötés vs fix óra:** WLED/Shelly **sunset trigger** finomíthatja az **esti rámpát**, de a **14/10 összesített** célhoz **fix off/on óra** (vagy „legalább 10 h off”) ellenőrzés szükséges — **hibrid** beállítás: pl. rámpa **napnyugta −30 perc** kezdet, de **legkésőbb 20:00-ra off** (felhasználói finomhangolás).

#### 4.5.3 Fajta-megjegyzés (nem bizonyíték)

Vegyes házi fajták (barna, fehér, kendermagos, kopasznyakú) **különböző aktivitást** mutathatnak; a **14/10** cél **felhasználói üzemeltetési** preferencia — ha **tojástermelés** télen visszaesik, **állatorvos / tenyésztői tapasztalat** alapján **+30–60 perc** reggeli fény **mérlegelhető** (nem automatikus ajánlás).

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

### 9.4 Szigetüzem: Victron inverter + FI védelem

**Ismert rendszer (felhasználó):** **Victron MultiPlus-II 3000** (3 kVA folyamatos / 4 kVA csúcs jellegű kategória), tyúkól **230 V** az inverter **AC kimenetéről**; **16 A FI megszakító** és **FI relé** a kimeneten.

| Fogalom | Értelmezés | Tyúkól világításra |
|---------|------------|---------------------|
| **FI megszakító (RCD)** | Áram-védőkapcsoló: **30 mA** (tipikusan) differenciáláramra old | **Emberi védelem** nedves/poros környezetben — **ajánlott** |
| **FI relé** | Gyakran **kiegészítő** vagy **külső RCD modul** / védő funkció a Victron kimenetén | A leírásod alapján **van földelés ellenőrzés / FI** — **jó gyakorlat** |
| **16 A** | Max. terhelés ~**3,7 kW** ohmos | Világítás **~20–40 W** elhanyagolható; **induktív** dimmer terhelés **N/I** harmonikus |

**Victron + dimmer (Shelly triac):**

- A **MultiPlus-II** **tiszta szinusz** AC kimenetet ad ([Victron MultiPlus-II dokumentáció](https://www.victronenergy.com/inverters-chargers/multiplus-ii)) — **Shelly Dimmer Gen3** (trailing edge) és **12 V kapcsolóüzemű PSU** **jó kompatibilitás várható**.
- Telepítés előtt **rövid teszt** továbbra is ajánlott: dimmelhető LED **min–max**, **off** = nincs **szellemfény**, áramszünet / inverter restart után **program helyreáll**.
- **12 V WLED PSU:** kapcsolóüzemű tápegység **kevésbé érzékeny** az inverter kimenet minőségére, mint a triac.

**Áramszünet (akkufeszültség kifut / inverter leáll):**

- Világítás **off**; program **megáll**.
- Visszatéréskor: WLED/Shelly **NTP** (4G modem) után idő szinkron; **ütemezés folytatódhat** — **1–2 nap** drift ellenőrzés, ha NTP nem elérhető.

**Földelés (PE):** sziget rendszerben a **Victron földelési koncepció** (közös föld, neutral bonding) **szakemberi** tervezésű; a tyúkól **PE** csatlakoztatása **kötelező** érintésvédelmi szempontból.

---

## 10. Internet-, Wi‑Fi- és felhőfüggőség

| Jelölt | Wi‑Fi szükséges napi | Felhő szükséges | Megjegyzés |
|--------|----------------------|-----------------|------------|
| J1 WLED | Opcionális (után nem) | Nem | Idő makrók eszközön |
| J2 ChickenLight | Nem | Nem | |
| J5 Shelly Gen3 | Igen (helyi) | Nem kötelező | App/cloud opcionális |
| J11 Hue | Bridge LAN | Account setup | Napi: bridge |
| J12 HA | LAN | Nem | Központ SPOF |

### 10.1 Helyszín-specifikus: 4G modem + TP‑Link RE315 (Repeater)

**Ismert topológia:**

```
[ Internet ] ←—— 4G ——→ [ 4G Wi‑Fi modem / router ] ←~~ 2,4/5 GHz ~~→ [ TP‑Link RE315 Repeater ] ←~~ Wi‑Fi ~~→ [ Tyúkól: WLED / Shelly ]
                                                                                    ↑
                                                                          [ Telefon ]
```

**Eszköz:** [TP‑Link RE315](https://www.tp-link.com/) — **AC1200**, felhasználó szerint **Repeater** üzemmód (nem AP vezetékes háttérhálóval).

| Szempont | Értékelés | Megjegyzés |
|----------|-----------|------------|
| Helyi vezérlés | **Jó**, ha telefon + IoT **ugyanahhoz a kiterjesztett hálózathoz** csatlakozik | Repeater gyakran **más SSID** (`…_EXT`) — **ugyanarra kösd** mindkettőt |
| Sávszél / késleltetés | **Közepes** | Repeater **fél sávszélesség**; világításvezérléshez **elég** |
| Stabilitás | **Közepes** | **Két ugrás** (tyúkól → RE315 → modem); modem Wi‑Fi gyengülése → **tyúkól offline**, de **ütemezés eszközön fut** |
| NTP / idő | 4G **van** | Modem+internet leáll → idő **drift**; **havonta ellenőrizd** az off időpontot |
| Jobb alternatíva (később) | **N/I** kábelút | Ha valaha **Ethernet** a modemhez: RE315 **AP mód** stabilabb — jelenleg **nincs** UTP a tyúkólnál |

**Tervezési elv:** **14/10 program WLED Time & Macros-ban** (fix óra) **és** esti **30 perc Nightlight**; ne **csak** napnyugta trigger, amíg a 10 h sötét **ablakokkal** nincs validálva.

**WLED példa logika (szöveges, nem telepítési utasítás):**

1. **06:00** — preset „Nappali 100%” (vagy 30 perc sunrise Nightlight 06:00-tól).  
2. **19:30** — API/macro: Nightlight **30 perc**, mode fade → **0%**.  
3. **20:00** — preset off / timer off.  
4. Heti ismétlés minden nap.

---

## 11. Hibaforgatókönyvek és helyreállítás

Skála: **L** = világítás állapota, **A** = automata program, **H** = emberi beavatkozás, **É** = észrevételi valószínűség.

| # | Esemény | L | A | H | Biztonságos helyreállítás | É |
|---|---------|---|---|---|---------------------------|---|
| 1 | Internet kimarad | J1/J2/J5: normál | Fut | Nem | — | Alacsony |
| 2 | Router újraindul | Wi‑Fi eszköz reconnect | Fut időzítés | Nem | Várni | Közepes |
| 3 | HA leáll | J12: utolsó állapot | Megáll | Igen | HA restart | Magas ha csak HA |
| 4 | Felhő down | Shelly helyi web: OK | Fut | Nem | Helyi IP | Alacsony |
| 5 | Áramszünet (Victron/akkü) | Off | Megáll | Nem | NTP szinkron után | Közepes |
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

**Helyszínhez igazítva (230 V + N + PE, DIY OK):** **12 V WLED** (J1) — a **230 V csak a tápegységig** menjen (tyúk zónán **kívül** vagy **zárt dobozban**), a madarak felé **12 V LED szalag/panel**.

**Javasolt összetétel:** ESP32 + WLED + 12 V 60 W PSU + meleg fehér LED szalag + védő doboz.

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

**Helyszínhez igazítva:** **nullvezetés megvan** → Shelly Gen3 **N-nel**, **2× ~10 W dimmelhető E27** (4.1.1 táblázat), **IP44+** lámpatest, dimmer **tyúk elérésén kívül** (doboz / magas fal).

**Javasolt összetétel:** **Shelly Dimmer Gen3** + helyi **Advanced Schedule** (esti: `brightness 0%`, `transition 1800–2700 s`).

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

**Felhasználói profil alapján (DIY egyszerűség + 230 V a helyszínen + 4G/extender Wi‑Fi):**

| Prioritás | Ajánlás | Miért |
|-----------|---------|-------|
| **1. (ajánlott)** | **WLED + 12 V** (J1) | Egy telepítés: flash, Wi‑Fi, **Time & Macros → Sunset**, Nightlight **15–45 perc** ([WLED macros](https://kno.wled.ge/features/macros/)); kevesebb karbantartás mint ESPHome YAML |
| **2. (ha nem akarsz flash-elni)** | **Shelly Gen3** (J5) | Nullvezetés megvan; app/web + **eszköz-ütemezés**; telefon ugyanazon Wi‑Fi-n |
| **3. (nem első választás most)** | ChickenLight 12 | Jó, de drágább és kevésbé távoli; WLED mellett felesleges duplikáció |

**ESPHome (J13):** csak akkor, ha később **Home Assistant** ökoszisztémát is építesz; indulásnak **WLED egyszerűbb**.

**Indoklás (WLED):** Igazolt **255 perc** nightlight; **internet nem kell** napi működéshez NTP után; **12 V** a tyúk közelében; 230 V a **PSU-nál** jól elválasztható.

**Opcionális bővítés:** Shelly **Plus 1** „vész OFF” külön ágon — **nem** szükséges kezdéshez.

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
| 19 | Victron MultiPlus-II | https://www.victronenergy.com/inverters-chargers/multiplus-ii | 2026-10-15 |

---

## 21. Javasolt következő lépések (jóváhagyást igénylő)

1. **Architektúra (kutatási javaslat):** **WLED 12 V** + **4.5.1** időzítés (14/10, 30 perc esti rámpa); alternatíva: **Shelly Gen3** + MultiPlus-II 3000 (szinusz).
3. **Sötét környezet (redőny nélkül):** **általában OK** a 10 h blokk; opcionális **holdteli éjszaka** viselkedés megfigyelése.
4. **Lux** 5 ponton **06:30** és **19:00** körül — elég-e a **2× ~10 W** ablak mellett.
5. **Pilot 1–2 hét:** viselkedés (ülés a percben, reggeli aktivitás); tojástermelés napló (**opcionális**).
6. **Victron kimenet:** FI **teszt gomb** / havi ellenőrzés; világítás **16 A ágon** maradjon.
7. **RE315:** extender **közelebb a tyúkólhoz**, ha lehet; **fix IP** vagy DHCP reservation WLED-nek a Cudy-n; **téli Wi‑Fi teszt függő** (telepítési terv 8.1).
8. **Távoli elérés:** Cudy **DDNS** + **WireGuard VPN** → WLED LAN IP; **OTA/settings PIN**; nyilvános port forward **kerülendő** ([WLED](https://kno.wled.ge/advanced/access-over-internet/)).
9. **Beszerzés:** [telepítési terv §4](./tyukol-vilagitas-wled-2ol-telepitesi-terv.md) — **Modulshop** + **240volt** (a **diszlec.hu** nem elektronikai bolt).
10. **Telepítés** — külön jóváhagyás a pilot után.

---

*Dokumentum készítette: Cloud Agent kutatás — repository: workspace root, branch: `cursor/tyukol-vilagitas-wled-2ol-44ad`.*
