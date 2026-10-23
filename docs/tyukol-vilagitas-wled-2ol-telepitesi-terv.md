# WLED — 2 tyúkól, 1 vezérlő, 1 táp, 2 szalag (telepítési terv)

**Státusz:** döntött koncepció + megvehető terméklista (nem telepítési jóváhagyás)  
**Dátum:** 2026. október 23. (§9 válaszok, BOM Anro + Modulshop, távoli elérés)  
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
| LED teljesítmény / óla | **~14,4 W** (**4,8 W/m** × **3 m**, Anro 3528-60 IP65) | Erősebb, mint a korábbi Avide **~7,2 W/óla** — **30–40 tyúknál** jobb árnyékmentesítés; lux → **mérés** üres ólában |
| WLED max % | **~70–90%** nappal (fényerő limit); sarkok sötétek → **luxmérés** | 9,6 W/m szalag **7120** ezzel a PSU-val **2×3 m-re túl nagy terhelés** — maradj **7154**-nél |
| Beszerzés | **6 m** méteráras **2700–3200 K**, **IP65**, **3528-60** (Anro) → **2×3 m** + maradék | Nem 5 m tekercs — **méterre rendelés** |

**Terhelés összesen:** 2× ~14,4 W ≈ **29 W** LED + buck/ESP ≈ **1–2 W** → **Mean Well 60 W** ~50%-on — rendben.

---

## 4. Beszerzési lista (Anro + Modulshop + helyi, bruttó HUF)

**Árlekérdezés:** 2026-10-23 (termékoldalak). Szerelés **nincs** benne.

### 4.1 Preferált bolt — **anrodiszlec.hu** (Anro Díszlec)

Az **Anro Díszlec** ([anrodiszlec.hu](https://www.anrodiszlec.hu/)) **LED / világítás / Mean Well** elektronikai webshop — **ez a preferált forrás** a táp, szalag, IP65 doboz, WAGO és szalag-kábel tételekre.

**Ne keverd** a **diszlec.hu / diszlecek.hu / diszlec-stukko.hu** oldalakkal: azok **díszléc és stukkó** boltok, **nem** ESP32 / MOSFET / buck. Hasonló név: **Distrelec.hu** (B2B katalógus) — szintén **nem** ugyanaz.

**Anrón nincs** (2026-10-23, keresés): **ESP32 DevKit**, **MOSFET trigger modul**, **CN3903** (12→5 V buck), **autó mini biztosíték + foglalat**, **8 mm DC szalagcsatlakozó** — ezek **Modulshop** + **helyi autó-/ barkács** (minimális).

### 4.2 anrodiszlec.hu (elsődleges)

| # | Db | Termék | Bruttó | Link |
|---|-----|--------|--------|------|
| A1 | 1 | **Mean Well LPV-60-12**, 12 V / 5 A / 60 W, **IP67** (tyúkódnál javasolt) | **5 890 Ft** | https://www.anrodiszlec.hu/product_info.php/products_id/25163 |
| A2 | 6 m | **ANRO LED szalag** kültéri **3528-60**, **4,8 W/m**, 12 V, **meleg fehér** (~2700–3200 K), **IP65**, PureSilicone (CRI>90) — **2×3 m/óla** | **6× 1 990 = 11 940 Ft** | https://www.anrodiszlec.hu/product_info.php/products_id/7154 |
| A2b | *nem aj.* | **3528-120**, **9,6 W/m** (7120) — **2×3 m ≈ 58 W** LED, PSU-hoz szoros | **6× 2 590** | https://www.anrodiszlec.hu/product_info.php/products_id/7120 |
| A3 | 1 | **S-BOX** kötődoboz **195×145×75 mm**, **IP65**, fekete, csavaros fedél | **3 080 Ft** | https://www.anrodiszlec.hu/product_info.php/products_id/41961 |
| A4 | 6 | **Wago 221** csatos összekötő, **3×4 mm²** | **6× 180 = 1 080 Ft** | https://www.anrodiszlec.hu/product_info.php/products_id/11220 |
| A5 | 10 m | **Mentavill** vezeték LED szalaghoz, piros/fekete **2×0,75 mm²** | **10× 210 = 2 100 Ft** | https://www.anrodiszlec.hu/product_info.php/products_id/30480 |

| | Ft |
|--|-----|
| **Részösszeg Anro** | **24 090** |
| Szállítás (házhoz, [tájékoztató](https://www.anrodiszlec.hu/article_info.php/articles_id/51): **1 990 Ft-tól**) | **1 990** |
| **Anro összesen** | **26 080** |

*Szalag:* méterre rendelés; vágás után **forrasztás** vagy **WAGO** a szalag vezetékén (Anrón nincs olcsó **8 mm DC apa** — opció: [240volt csatlakozó](#46-korábbi-terv-modulshop--240volt-összehasonlításhoz) külön rendelés **nem** kell, ha forrasztasz).

### 4.3 Modulshop.hu (kiegészítő — vezérlés)

| # | Db | Termék | Bruttó | Link |
|---|-----|--------|--------|------|
| M1 | 1 | **ESP32 WROOM-32D**, CP2102, USB-C, 38 pin (dual core, 2× PWM) | **3 350 Ft** | https://modulshop.hu/esp32-wroom-32d-cp2102-usb-c-38-pin |
| M3 | 2 | **MosFet trigger modul** 15 A / 400 W (PWM LED-hez) | **2× 450 = 900 Ft** | https://modulshop.hu/mosfet-trigger-modul-15a-400w-734 |
| M4 | 1 | **CN3903** mini buck **12 V → 5 V** fix, max ~3 A (ESP32 táp a 12 V buszról) | **250 Ft** | https://modulshop.hu/cn3903-mini-dc-dc-step-down-konverter-5v-os-3713 |
| M5 | *alt.* | **IRLZ44N** logic-level MOSFET (ha a trigger modul **3,3 V**-n nem kapcsol) | **2× ~200 Ft** | https://modulshop.hu/ (keresés: IRLZ44N) |

| | Ft |
|--|-----|
| **Részösszeg Modulshop** (PSU **Anróról**, M2 **nincs**) | **4 500** |
| Szállítás (pl. Foxpost / MPL automata) | **1 250** |
| **Modulshop összesen** | **5 750** |

*Megjegyzés:* a trigger modul adatlapja **5–20 V** vezérlő jelet ír — **teszteld** WLED PWM-mel; ha gyenge, **IRLZ44N** + közös GND.  
*Alternatíva ESP táp:* külön **5 V USB-töltő** (230 V a dobozban) a buck helyett.

### 4.4 Helyi / barkács (Anrón nincs)

| # | Db | Termék | Becslés | Megjegyzés |
|---|-----|--------|---------|------------|
| H1 | 2 | **2 A** mini biztosíték + **ATO/mini foglalat** (12 V ág / óla) | **~800–1 500 Ft** | autóbolt, inShop, barkács |
| H2 | ~8 m | **1,5 mm²** flex (PSU → ólák, **4 m** áganként) | **~2 000–3 500 Ft** | a **2×0,75 mm²** (A5) főleg szalag oldali; nagyobb áramhoz **1,5 mm²** ajánlott |
| H3 | 0 | WLED firmware | **0 Ft** | https://install.wled.me/ |

### 4.5 Végösszeg (ajánlott — Anro + Modulshop + helyi)

| Forrás | Ft |
|--------|-----|
| **anrodiszlec.hu** | **26 080** |
| **Modulshop.hu** | **5 750** |
| Helyi (biztosíték + 1,5 mm², közép) | **~3 000** |
| **Összesen (becslés)** | **~34 830 Ft** |

**Terhelés:** 2× ~14,4 W LED + ~2 W vezérlés ≈ **31 W** → **60 W Mean Well** ~52%-on — rendben.

### 4.6 Korábbi terv (Modulshop + 240volt) — összehasonlításhoz

Ugyanazon nap korábbi, **Modulshop-centrikus** lista (olcsóbb PSU Modulshopban, szalag **240volt** Avide tekercs):

| Forrás | Részösszeg | Szállítás | Összesen |
|--------|------------|-----------|----------|
| Modulshop (ESP32 + **60 W PSU** + MOSFET + buck) | 7 100 | 1 250 | **8 350** |
| 240volt (2× Avide **12 W / 5 m** IP65 + 2× DC csatlakozó) | 20 888 | 2 990 | **23 878** |
| Barkács (doboz + WAGO + kábel, közép) | — | — | **~8 000** |
| **Régi végösszeg** | | | **~40 200 Ft** |

| | Anro + Modulshop + helyi | Modulshop + 240volt + barkács |
|--|---------------------------|------------------------------|
| **Végösszeg** | **~34 830 Ft** | **~40 200 Ft** |
| **Különbség** | **~5 370 Ft** olcsóbb | |
| **Webshopok** | **2** (+ helyi) | **2** (+ helyi) |
| **PSU** | Mean Well **IP67** (Anro) | Modulshop 60 W (nem IP67) |
| **Szalag / óla** | **~14,4 W**, méteráras Anro | **~7,2 W**, Avide tekercs |
| **Doboz / WAGO / szalag-kábel** | Anrón | Barkácsboltból becsült |
| **Szállítás összesen** | **~3 240 Ft** | **~4 240 Ft** |

*Spóri 240volt változat* (7,2 W/5 m Avide): **~38 100 Ft** — még mindig **~3 270 Ft** drágább, gyengébb fény/óla.

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
   - Output 1: **PWM White**, GPIO **16**, max current ~**1 200 mA** (≈14 W @ 12 V)  
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
| 1 | Ólánként hány tyúk? | **30–40 db** → **~3 m**, **~14,4 W/óla** szalag (Anro 4,8 W/m; 4. fejezet) |
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
| Anro Díszlec (Mean Well, IP65 szalag, doboz, WAGO) | https://www.anrodiszlec.hu/ | 2026-10-23 |
| Modulshop (ESP32, MOSFET, CN3903 buck) | https://modulshop.hu/ | 2026-10-23 |
| 240volt (korábbi BOM — Avide szalag) | https://www.240volt.hu/ | 2026-10-23 |
