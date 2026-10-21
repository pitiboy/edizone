# WLED — 2 tyúkól, 1 vezérlő, 1 táp, 2 szalag (telepítési terv)

**Státusz:** döntött koncepció + megvehető terméklista (nem telepítési jóváhagyás)  
**Dátum:** 2026. október 21.  
**Kapcsolódó kutatás:** [tyukol-vilagitas-megoldasok.md](./tyukol-vilagitas-megoldasok.md)

---

## 1. Mit választottunk

| Paraméter | Érték |
|-----------|--------|
| Vezérlés | **WLED** (ESP32) |
| Ólák | **2 db**, azonos (~6,25 m²), **3–4 m** távolság |
| LED | **2 db** külön **12 V meleg fehér IP65 szalag** (nem címzett / analóg 2 vezetékes) |
| Táp | **1 db** 12 V PSU (230 V a **MultiPlus-II 3000** kimenetről) |
| Fotoperiódus | **14 h fény + 10 h sötét**, esti **30 perc** rámpa |
| Téli tojás | Igen → **télen korábbi reggeli be** (lásd 5. fejezet) |
| Távoli | **Automata eszközön**; telefon/csak **Cudy 4G LAN** (opcionális), **nem kell naponta nyomkodni** |
| Wi‑Fi | Cudy 4G router + **TP‑Link RE315 Repeater**; télben jel **bizonytalan** → vezérlő **meleg/zárt** helyre |

---

## 2. Miért analóg 12 V szalag (nem WS2812)

- Olcsó, **IP65**, meleg fehér, tyúkólnál bevált.
- WLED **PWM White** mód: **2 külön GPIO + MOSFET**, a két óla **szinkron** ugyanarra a presetre / időzítésre ([WLED compatible strips](https://kno.wled.ge/basics/compatible-led-strips/)).
- A **3–4 m** távolság **adatvezeték** (címzett LED) számára kockázatos; **12 V + PWM** kábelen megy a fényerő, csak **+12 V és GND** megy ki ólánként (plusz a vezérlő jele a központi dobozban marad).

---

## 3. Elvi bekötés

```
[ MultiPlus 230V ] → [ FI 16A ág ] → [ 12V PSU ] ──┬── MOSFET1 → Óla A szalag (+12V)
                                                    └── MOSFET2 → Óla B szalag (+12V)

[ ESP32 ] ── GPIO16 ── MOSFET1 gate
          ── GPIO17 ── MOSFET2 gate
          ── Wi‑Fi → RE315 → Cudy 4G (NTP + opcionális böngésző)

Közös GND: PSU ↔ ESP32 ↔ MOSFET ↔ mindkét szalag
```

**Központi doboz** (javaslat): a **két óla között** vagy **védett falfülke** (ahol télen nem fagy −10 °C alá az ESP32). A **PSU + ESP32 + MOSFET** ide kerül; **230 V csak a dobozig**.

**12 V elosztás:** PSU kimenet → **2 A-os biztosíték / óla** → **1,5 mm²** (vagy 2×0,75 mm² párhuzamos) **4 m**-ig ólánként; **+12 V** a szalag elején, **GND** vissza.

**Szalag hossz / óla:** ~**2,5–3 m** mennyezet körül (6,25 m² óla); egy **5 m-es tekercsből** kettévágva **1 tekercs elég**.

---

## 4. Beszerzési lista (konkrét, bruttó HUF)

**Árlekérdezés:** 2026-10-21. Szállítás és szerelés **nincs** benne.

| # | Darab | Termék | Cikkszám / megjegyzés | Bruttó ár | Link |
|---|-------|--------|------------------------|-----------|------|
| 1 | 1 | **ESP32-DevKitC** 38 pin USB-C | pl. Drot elektro | **5 031 Ft** | https://www.drot-elektro.hu/arduino-platform/232741-esp32-devkitc-38pin-fejlesztoi-lap-usb-c.html |
| 2 | 1 | **Mean Well LPV-60-12** (60 W, 12 V, IP67) | EHMWLPV-60-12 | **7 567 Ft** | https://www.energiahaza.hu/LED-tapegyseg-Mean-Well-LPV-60-12-60W-12V |
| 3 | 2 | **MOSFET illesztő modul** 3,3 V PWM, 12 V / 3 A+ | pl. IRLZ44N modul | **2× 357 Ft ≈ 714 Ft** | https://kinaiwebaruhaz.hu/elektronika/mosfet-kapcsolo-modul-dc-fan-motor-led-szalag-21556.html |
| 4 | 1 | **Avide LED szalag** 12 V **2700K IP65 5 m** (~12 W / tekercs) | ABLS12V2835-60EW65 | **~7 661 Ft** (VTAC) | https://www.vtac.hu/led-termek/led-szalag/kulteri/ (keresés: Avide 12W 2700K IP65 5m) |
| 4b | *alt.* | Ugyanaz 7,2 W / 5 m (gyengébb) | | **~6 878 Ft** | https://www.240volt.hu/termek/avide-led-szalag-12v-7-2w-2700k-ip65-5m-br-skuabls12v2835-60ew65-7-2w/ |
| 5 | 2 | **Mini biztosíték** 12 V vonalra (2 A) + foglalat | autó / LED | **~1 500 Ft** | helyi |
| 6 | 1 | **IP65 szerelődoboz** + WAGO, **1,5 mm²** flex kábel ~10 m, ragasztható csatlakozó szalaghoz | | **~6 000–10 000 Ft** | barkács |
| 7 | 0 | WLED szoftver | ingyenes | **0 Ft** | https://install.wled.me/ |

### Összesítés

| Kategória | Ft |
|-----------|-----|
| Elektronika (1–3) | **~13 300** |
| LED + kiegészítők (4–6) | **~15 000–19 000** |
| **Összesen (becslés)** | **~28 000–32 000 Ft** |

**Megjegyzés:** olcsóbb PSU: V-TAC 60 W **~3 300 Ft** ([ledbau 3246](https://ledbau.hu/led-tapegysegek-12v)) → teljes **~24 000 Ft**, de tyúkólnál a **Mean Well IP67** robosztusabb.

**Terhelés:** 2× ~6 W szalag ≈ **12 W** + ESP ≈ **15 W** → **60 W PSU bőven elég**.

---

## 5. Időzítés — 14 h fény, 10 h sötét, téli tojás

### 5.1 Alap napi ütem (éves átlag)

| Esemény | Időpont | WLED |
|---------|---------|------|
| Sötét blokk kezdete | **20:00** | Nightlight **30 perc** → 0%, majd off |
| Sötét | **20:00–06:00** | **10 h** (mesterséges off) |
| Reggeli fény | **06:00** | Preset 100% (opc. 30 perc sunrise Nightlight) |
| Nappali | **06:00–19:30** | 100% (max fényerő limit ~80% ha túl erős) |

**14 h „világos ablak”:** 06:00 → 20:00.

### 5.2 Téli finomhangolás (tojás)

Télen rövid a nap + 2 ablak kevesebb fényt ad → **mesterséges reggeli előbb**:

| Évszak | Javasolt **bekapcsolás** | Esti rámpa kezdete | Off |
|--------|--------------------------|--------------------|-----|
| Nov–feb | **05:30** | 19:30 | 20:00 |
| Már–ápr, szept–okt | **05:45** | 19:30 | 20:00 |
| Máj–aug | **06:00** | 19:30 | 20:00 |

*14 h megtartása:* télen **05:30–19:30** = 14 h, off továbbra is **20:00** (sötét 20:00–05:30 = 9,5 h — **közelít**; ha szigorú 10 h sötét kell, off **19:30** és reggel **05:30** = 10 h sötét, 14 h fény **05:30–19:30**).  

**Ajánlott szigorú változat (10 h sötét):** fény **05:30–19:30**, rámpa **19:00–19:30**, off **19:30**, reggel **05:30**.

WLED: **Time & Macros** → heti ismétlés; szezonváltáskor **2 preset** (Tél/Nyár) elég.

---

## 6. WLED beállítás (checklist, nem helyettesíti a kézikönyvet)

1. Flash: https://install.wled.me/ → **ESP32**.
2. **Config → LED Preferences:**  
   - Output 1: **PWM White**, GPIO **16**, max current ~650 mA (≈8 W)  
   - Output 2: **PWM White**, GPIO **17**, ugyanaz  
   - Mindkét szalag **szinkron**: ugyanaz a preset / **Sync** / egy segment mindkettőre (WLED verziótól függ — cél: **azonos fényerő**).
3. **Time & Macros:** NTP be, időzóna **Europe/Budapest**; makrók: Tél/Nyár (5. fejezet).
4. **Nightlight:** mode **Fade**, **30 perc**, target 0.
5. **Apply preset at boot:** utolsó znám vagy Tél preset.
6. **Cudy router:** DHCP **foglalás** ESP32 MAC-re (fix IP); NTP engedélyezve.

Források: [WLED multi-strip](https://kno.wled.ge/features/multi-strip/), [PWM strips](https://kno.wled.ge/basics/compatible-led-strips/), [Time & Macros](https://kno.wled.ge/features/macros/).

---

## 7. Távoli elérés (Cudy 4G) — automata marad

| Funkció | Működés |
|---------|---------|
| Napi rámpa + 14/10 | **100% WLED-ben**, internet **nem kell** |
| Idő szinkron | **NTP** a Cudy-n keresztül (4G); ha 4G kimarad → **drift** (havonta ellenőrizd) |
| Távoli „ránézés” / felülírás | Ugyanazon LAN-on (4G VPN / Cudy app / port forward) → `http://<wled-ip>` — **opcionális** |
| Te nem nyomkodsz | Időzítő + preset; telefon csak **hiba / szezonváltás** |

---

## 8. Tél, fagy, Wi‑Fi

- **ESP32** üzem: ~−20…+60 °C (modul függő); **Wi‑Fi** gyengülhet fagyban.
- **Megoldás:** vezérlődoboz **szigetelt falfülke** / ólán **kívül** de védett helyen; **RE315** a melegebb zónában, ha lehet.
- **Áramszünet** (Victron): fény ki; visszatérés után WLED boot preset.

---

## 9. Nyitott kérdések (minimális)

1. **Ólánként hány tyúk?** (lux finomítás — eredeti kutatás ~30 db / óla feltételezés.)
2. **RE315 ↔ tyúkól** jelerősség télen (egy **Wi‑Fi teszt** fagyos napon).
3. **Cudy modell** / VPN: kívülről is el akarod-e érni a WLED-et, vagy elég helyi Wi‑Fi.

---

## 10. Forrásjegyzék

| Forrás | URL | Dátum |
|--------|-----|-------|
| WLED PWM / analóg szalag | https://kno.wled.ge/basics/compatible-led-strips/ | 2026-10-21 |
| WLED multi output | https://kno.wled.ge/features/multi-strip/ | 2026-10-21 |
| Mean Well LPV-60-12 | https://www.energiahaza.hu/LED-tapegyseg-Mean-Well-LPV-60-12-60W-12V | 2026-10-21 |
| ESP32 DevKit | https://www.drot-elektro.hu/arduino-platform/232741-esp32-devkitc-38pin-fejlesztoi-lap-usb-c.html | 2026-10-21 |
