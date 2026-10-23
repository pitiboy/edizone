# WLED — 2 tyúkól, 1 vezérlő, 1 táp, 2 szalag (telepítési terv)

**Státusz:** döntött koncepció + megvehető terméklista (nem telepítési jóváhagyás)  
**Dátum:** 2026. október 23. (§9 válaszok, BOM, távoli elérés)  
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
| Tyúk / óla | **30–40 db** (azonos ólák) |
| Távoli | **Igen, kívülről is** (Cudy **DDNS** + **WireGuard VPN** ajánlott); napi üzem **automata**, telefon csak felülbírálat / szezon |
| Wi‑Fi | Cudy 4G router + **TP‑Link RE315 Repeater**; **téli jelteszt függő** (lásd 8–9. fejezet) → vezérlő **meleg/zárt** helyre |

---

## 2. Miért analóg 12 V szalag (nem WS2812)

- Olcsó, **IP65**, meleg fehér, tyúkólnál bevált.
- WLED **PWM White** mód: **2 külön GPIO + MOSFET**, a két óla **szinkron** ugyanarra a presetre / időzítésre ([WLED compatible strips](https://kno.wled.ge/basics/compatible-led-strips/)).
- A **3–4 m** távolság **adatvezeték** (címzett LED) számára kockázatos; **12 V + PWM** kábelen megy a fényerő, csak **+12 V és GND** megy ki ólánként (plusz a vezérlő jele a központi dobozban marad).

---

## 3. Elvi bekötés

```
[ MultiPlus 230V ] → [ FI 16A ág ] → [ 12V PSU ] ──┬── MOSFET1 → Óla A szalag (+12V)
                                                    ├── MOSFET2 → Óla B szalag (+12V)
                                                    └── [ 12→5 V buck ] → ESP32 5 V (CN3903)

[ ESP32 ] ── GPIO16 ── MOSFET1 gate (logic-level / illesztő)
          ── GPIO17 ── MOSFET2 gate
          ── Wi‑Fi → RE315 → Cudy 4G (NTP; távoli: VPN → LAN)

Közös GND: PSU ↔ ESP32 ↔ MOSFET ↔ buck ↔ mindkét szalag
```

**Központi doboz** (javaslat): a **két óla között** vagy **védett falfülke** (ahol télen nem fagy −10 °C alá az ESP32). A **PSU + ESP32 + MOSFET** ide kerül; **230 V csak a dobozig**.

**12 V elosztás:** PSU kimenet → **2 A-os biztosíték / óla** → **1,5 mm²** (vagy 2×0,75 mm² párhuzamos) **4 m**-ig ólánként; **+12 V** a szalag elején, **GND** vissza.

**Szalag hossz / teljesítmény / óla (30–40 tyúk):**

| Paraméter | Javasolt érték | Indoklás |
|-----------|----------------|----------|
| Szalag hossz | **~3 m** mennyezet/perem (6,25 m²) | 30–40 madárnál több **árnyék** → hosszabb, egyenletesebb fény |
| LED teljesítmény / óla | **~7–8 W** (12 W/5 m tekercsből **3 m** vágva) | ~720 lm/óla → becsült **~50–65 lux** átlag (η≈0,45; [kutatás 4.1.1](./tyukol-vilagitas-megoldasok.md)) |
| WLED max % | **~80–100%** nappal; sarkok sötétek → **luxmérés** üres ólában | 40 madárnál ne menj **6 W/óla** alá hosszú távon |
| Tekercs | **2× 5 m, 12 W, 2700 K IP65** (Avide) → **2× ~3 m** + maradék | 1 tekercs csak **2×2,5 m** (~6 W/óla) — **30 madárra elég**, **40-nél szorosabb** |

**Terhelés összesen:** 2× ~7,2 W ≈ **14,5 W** + buck/ESP ≈ **1–2 W** → **60 W PSU** bőven elég.

---

## 4. Beszerzési lista (2 webshop + helyi, bruttó HUF)

**Árlekérdezés:** 2026-10-23. Szerelés **nincs** benne.

### 4.1 „Diszlec” preferencia — tisztázás

A **diszlec.hu / diszlecek.hu / diszlec-stukko.hu** oldalak **díszléc és stukkó** webshopok, **nem** elektronikai alkatrész-forrás. Hasonló névvel elektronikára a **Distrelec.hu** (nagy B2B katalógus, drágább szállítás) — ez **nem** ugyanaz.  
**Jelen terv:** elektronika **Modulshop.hu**-ról (egy csomag, alacsony szállítás); **meleg fehér IP65 szalag** csak **240volt.hu**-n (Modulshopnál nincs megfelelő 2700 K kültéri fehér szalag).

### 4.2 Modulshop.hu (elsődleges elektronika)

| # | Db | Termék | Bruttó | Link |
|---|-----|--------|--------|------|
| M1 | 1 | **ESP32 WROOM-32D**, CP2102, USB-C, 38 pin (dual core, 2× PWM) | **3 350 Ft** | https://modulshop.hu/esp32-wroom-32d-cp2102-usb-c-38-pin |
| M2 | 1 | **12 V 5 A** kapcsolóüzemű tápegység, 230 V AC, 60 W | **2 600 Ft** | https://modulshop.hu/12-voltos-5a-tapegyseg-ac-dc |
| M3 | 2 | **MosFet trigger modul** 15 A / 400 W (PWM LED-hez) | **2× 450 = 900 Ft** | https://modulshop.hu/mosfet-trigger-modul-15a-400w-734 |
| M4 | 1 | **CN3903** mini buck **12 V → 5 V** fix, max ~3 A (ESP32 táp a 12 V buszról) | **250 Ft** | https://modulshop.hu/cn3903-mini-dc-dc-step-down-konverter-5v-os-3713 |
| M5 | *alt.* | **IRLZ44N** logic-level MOSFET (ha a trigger modul **3,3 V**-n nem kapcsol) | **2× 200 Ft** | https://modulshop.hu/ (keresés: IRLZ44N) |

| | Ft |
|--|-----|
| **Részösszeg Modulshop** | **7 100** |
| Szállítás (pl. Foxpost / MPL automata) | **1 250** |
| **Modulshop összesen** | **8 350** |

*Megjegyzés:* a trigger modul adatlapja **5–20 V** vezérlő jelet ír — **teszteld** WLED PWM-mel; ha gyenge, **IRLZ44N** + közös GND.  
*Alternatíva ESP táp:* külön **5 V USB-töltő** (230 V a dobozban) a buck helyett — plusz kábel, de kevesebb ripple-aggodalom.

**PSU minőség:** tyúkódnál opcionális **Mean Well LPV-60-12 IP67** (~7 500 Ft, pl. energiahaza.hu) a Modulshop 60 W helyett — **3. bolt**, csak ha külön kell.

### 4.3 240volt.hu (LED szalag + csatlakozó)

| # | Db | Termék | Bruttó | Link |
|---|-----|--------|--------|------|
| L1 | 2 | **Avide** 12 V **12 W** **2700 K IP65 5 m** (ABLS12V2835-60EW65) — **3 m/óla** vágás | **2× 9 970 = 19 940 Ft** | https://www.240volt.hu/termek/avide-led-szalag-12v-12w-2700k-ip65-5m-br-skuabls12v2835-60ew65/ |
| L1b | *spóri* | Ugyanaz **7,2 W / 5 m** (gyengébb, 30 madár alsó sáv) | **2× 8 880 = 17 760 Ft** | https://www.240volt.hu/termek/avide-led-szalag-12v-7-2w-2700k-ip65-5m-br-skuabls12v2835-60ew65-7-2w/ |
| L2 | 2 | **12 V DC apa** csatlakozó szalaghoz 8 mm (forrasztás nélkül opció) | **2× 474 = 948 Ft** | https://www.240volt.hu/termek/abls12v3528-8mm-dccon-m/ |

| | Ft |
|--|-----|
| **Részösszeg 240volt** (12 W, 2 tekercs + 2 csatlakozó) | **20 888** |
| Szállítás MPL (kis csomag, tájékoztató minimum) | **2 990** |
| **240volt összesen** | **23 878** |

### 4.4 Helyi / barkács (nincs egy webshopban)

| # | Db | Termék | Becslés |
|---|-----|--------|---------|
| H1 | 2 | **2 A** mini biztosíték + foglalat (12 V ág / óla) | **~1 500 Ft** |
| H2 | 1 | **IP65 szerelődoboz**, WAGO, **1,5 mm²** flex ~10 m, ragasztható szalagcsatlakozó | **~6 000–10 000 Ft** |
| H3 | 0 | WLED firmware | **0 Ft** — https://install.wled.me/ |

### 4.5 Végösszeg

| Forrás | Ft |
|--------|-----|
| Modulshop | **8 350** |
| 240volt (ajánlott 12 W szalag) | **23 878** |
| Barkács (közép) | **~8 000** |
| **Összesen (becslés)** | **~40 200 Ft** |
| *Spóri szalag (7,2 W)* | **~38 100 Ft** |

**Terhelés:** 2× ~7,2 W LED + ~2 W vezérlés ≈ **16 W** → **60 W PSU** ~27%-on — hosszú élettartam.

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
   - Output 1: **PWM White**, GPIO **16**, max current ~**600 mA** (≈7 W @ 12 V)  
   - Output 2: **PWM White**, GPIO **17**, ugyanaz  
   - Mindkét szalag **szinkron**: ugyanaz a preset / **Sync** / egy segment mindkettőre (WLED verziótól függ — cél: **azonos fényerő**).
3. **Time & Macros:** NTP be, időzóna **Europe/Budapest**; makrók: Tél/Nyár (5. fejezet).
4. **Nightlight:** mode **Fade**, **30 perc**, target 0.
5. **Apply preset at boot:** utolsó znám vagy Tél preset.
6. **Cudy router:** DHCP **foglalás** ESP32 MAC-re (fix IP); NTP engedélyezve.
7. **Tápellátás:** buck **IN+/IN−** a 12 V PSU-ról; **OUT 5 V** → ESP **5 V** + **GND** (ne 12 V az ESP-re). USB-C csak flash / szerviz.
8. **Biztonság (távoli):** **Config → Security** → **OTA PIN** + **Settings PIN**; ne hagyd nyitva a nyilvános interneten ([WLED — access over internet](https://kno.wled.ge/advanced/access-over-internet/)).

Források: [WLED multi-strip](https://kno.wled.ge/features/multi-strip/), [PWM strips](https://kno.wled.ge/basics/compatible-led-strips/), [Time & Macros](https://kno.wled.ge/features/macros/).

---

## 7. Távoli elérés (Cudy 4G + DDNS) — automata marad, VPN előnyben

| Funkció | Működés |
|---------|---------|
| Napi rámpa + 14/10 | **100% WLED-ben**, internet **nem kell** |
| Idő szinkron | **NTP** a Cudy-n (4G); kimaradás → **drift** (havonta ellenőrizd) |
| Távoli WLED | **WireGuard kliens** → otthoni LAN → `http://<wled-fix-ip>` (pl. `192.168.10.x`) |
| Te nem nyomkodsz | Időzítő + preset; telefon **hiba / szezon / ránézés** |

**Cudy modell:** a pontos menü **modellfüggő** (4G LTE router vs mesh). Ellenőrizd a matricán / web UI-n: **General Settings → VPN** alatt van-e **WireGuard Server** és **OpenVPN Server**; **Advanced Settings → Network → DDNS**. Ha nincs WireGuard, **OpenVPN Server** ugyanerre jó ([Cudy VPN](https://docs.cudy.com/user_guide/wireless_router/vpn/)). 4G-nél a WAN IP legyen **publikus** (System Status → WAN → „public IP” egyezik a külsővel) — különben DDNS/VPN **nem megbízható** ([Cudy DDNS](https://docs.cudy.com/user_guide/mesh_system/network/)).

### 7.1 DDNS a Cudy-n

1. Regisztráció **No-IP**, **DynDNS**, vagy a Cudy által listázott szolgáltatónál (ingyenes aldomain).
2. Cudy: **Advanced Settings → Network → DDNS** → Enable, szolgáltató, **hostname + felhasználó + jelszó**, Check / Force interval → **Save & Apply**.
3. Teszt: mobilnetről (Wi‑Fi ki) ping / nslookup a hostname-re — a **4G WAN IP**-t kell mutatnia.

### 7.2 Fix IP az ESP32-nek (LAN)

1. WLED első boot után: **Config → WiFi** → jegyezd fel a **MAC** címet.
2. Cudy: **Advanced Settings → Network → LAN / DHCP** → **Address Reservation** (vagy „DHCP binding”): MAC → pl. **`192.168.10.50`** (a te alhálózatod szerint).
3. WLED újraindítás után ugyanaz az IP — bookmark: `http://192.168.10.50`.

### 7.3 Ajánlott: WireGuard VPN (port forward helyett)

1. **General Settings → VPN** → Enable → **WireGuard Server** → Client Access: **Internet and Local Network** (vagy **Local Network** ha csak WLED kell).
2. Listen port alap **51820/UDP** — **ne** kell nyilvánosan forwardolni a WLED 80-as portját.
3. **Add client** → export **`.conf`** → telefon / laptop **WireGuard app**.
4. A kliens config **Endpoint** mezőjében a Cudy **DDNS hostname** + port (pl. `tyukol.ddns.net:51820`), ne fix IP ([Cudy WireGuard](https://docs.cudy.com/user_guide/wireless_router/vpn/)).
5. VPN csatlakozás után böngésző: `http://192.168.10.50` — ugyanúgy, mintha a farm Wi‑Fi-n lennél.

**OpenVPN:** ha csak OpenVPN van, ugyanaz a logika: szerver a Cudy-n, kliens app, LAN elérés — lassabb, de WLED-hez elég.

### 7.4 Fallback: port forward WLED-re (nem ajánlott)

Csak ha **nincs** VPN a routeren:

| Lépés | Beállítás |
|-------|-----------|
| Port forward | WAN **egyedi port** (pl. **5080/tcp**) → **`192.168.10.50:80`** |
| WLED | **OTA PIN + Settings PIN** kötelező; erős **WiFi jelszó** |
| Kockázat | WLED **nincs** erős web auth; botok portszkennelnek — [WLED figyelmeztet](https://kno.wled.ge/advanced/access-over-internet/) |

**Ne** tedd ki simán `:80`-at a nyilvános internetre.

### 7.5 Biztonsági összefoglaló

| Megoldás | Előny | Hátrány |
|----------|--------|---------|
| **WireGuard / OpenVPN** | WLED **rejtett** marad a LAN-on; egy titkosított csatorna | Kliens app telepítés, egyszeri konfig |
| **DDNS + port forward** | Egyszerű URL | WLED sebezhető; brute force / ismert CVE-k |
| **Csak helyi Wi‑Fi** | Legbiztonságosabb | Nincs kívülről ránézés |

---

## 8. Tél, fagy, Wi‑Fi

- **ESP32** üzem: ~−20…+60 °C (modul függő); **Wi‑Fi** gyengülhet fagyban.
- **Megoldás:** vezérlődoboz **szigetelt falfülke** / ólán **kívül** de védett helyen; **RE315** a melegebb zónában, ha lehet.
- **Áramszünet** (Victron): fény ki; visszatérés után WLED boot preset.

### 8.1 Függő teendő — téli Wi‑Fi (nem blokkolja a beszerzést)

| # | Teendő | Mikor | Elfogadás |
|---|--------|-------|-----------|
| T1 | **Wi‑Fi jelerősség** mérés a **vezérlődoboz** helyén és mindkét ólában (pl. WiFi Analyzer / telefon dBm) | **Első fagyos napon** (≤0 °C körül), amikor még **nincs/perg** fagy | ≥ **−75 dBm** cél; gyengébb → RE315 közelebb / magasabbra |
| T2 | WLED **NTP** és **egy preset** váltás teszt ugyanazon a napon | T1 után | Ha kimarad → boot után idő ellenőrzés |

*2026-10-23:* még **nem volt fagy** — a teszt **hetek múlva** várható; addig a terv és a vásárlás **végrehajtható**.

---

## 9. Nyitott kérdések — megválaszolva / függő

| # | Kérdés | Döntés / állapot |
|---|--------|------------------|
| 1 | Ólánként hány tyúk? | **30–40 db** → **~3 m**, **~7–8 W/óla** szalag (4. fejezet, 3. fejezet táblázat) |
| 2 | RE315 jel télen | **Függő T1** (8.1) — **nem blokkolja** a tervet |
| 3 | Kívülről WLED? | **Igen** — **DDNS + WireGuard** (7. fejezet); Cudy **4G**, dinamikus IP OK |

---

## 10. Forrásjegyzék

| Forrás | URL | Dátum |
|--------|-----|-------|
| WLED PWM / analóg szalag | https://kno.wled.ge/basics/compatible-led-strips/ | 2026-10-21 |
| WLED internetes elérés | https://kno.wled.ge/advanced/access-over-internet/ | 2026-10-23 |
| WLED multi output | https://kno.wled.ge/features/multi-strip/ | 2026-10-21 |
| Cudy DDNS | https://docs.cudy.com/user_guide/mesh_system/network/ | 2026-10-23 |
| Cudy VPN (WireGuard / OpenVPN) | https://docs.cudy.com/user_guide/wireless_router/vpn/ | 2026-10-23 |
| Modulshop (ESP32, PSU, MOSFET, buck) | https://modulshop.hu/ | 2026-10-23 |
| 240volt Avide IP65 szalag | https://www.240volt.hu/ | 2026-10-23 |
