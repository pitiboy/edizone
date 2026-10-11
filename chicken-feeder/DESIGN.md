# DIY Automatic Chicken Feeder — Engineering Design (10–20 Birds)

**Document:** CF-FEED-001 rev A  
**Target flock:** 10–20 laying hens (≈120–150 g feed/day each → 1.2–3.0 kg/day total)  
**Design intent:** Gravity-fed hopper, positive-displacement rotary meter, timed + manual dispense, hobbyist-buildable (3D print + simple machining + COTS electronics).

---

## 1. Design summary

| Parameter | Value |
|-----------|--------|
| Hopper capacity | 25 L nominal (20–30 L adjustable via extension ring) |
| Cone included angle | 60° (wall 30° from vertical) |
| Metering wheel | Ø120 mm, 6 pockets, 25 mm pocket depth |
| Drop opening | Ø65 mm |
| Drive | 12 V geared DC motor, ≈8–12 RPM at wheel |
| Position feedback | Hall-effect switch + diametric magnet on wheel |
| Control | 12 V controller, 2+ daily schedules, manual push button |
| Trough | Covered, 600 mm long, moisture-resistant |

**Portion math (calibration):** Each pocket holds ≈35–45 mL loose layer pellets (ρ ≈ 0.62 g/mL) → **≈22–28 g per compartment**. One full revolution = 6 portions ≈ **130–170 g**. For 2 kg/day, ≈ **12–15 revolutions/day** (programmable).

---

## 2. System architecture

```
┌─────────────────────────────────────────────────────────────┐
│  HOPPER (food-safe HDPE/PP) + 60° cone insert               │
│       ↓ gravity                                              │
│  ANTI-JAM WIper / throat ring (flexible PA/Silicone)        │
│       ↓                                                      │
│  ROTARY METERING WHEEL (6 compartments) in sealed housing   │
│       ↓                                                      │
│  OUTLET CHUTE (Ø65 → 50 mm) + optional closable slide       │
│       ↓                                                      │
│  COVERED TROUGH (ground or wall-mount stand)                │
└─────────────────────────────────────────────────────────────┘

Electronics: 12 V PSU → controller → MOSFET → motor; Hall → controller; button → controller
```

See `drawings/` for: isometric cutaway, side section, top view, anti-jam detail, dosing wheel detail, wiring, exploded assembly.

---

## 3. Mechanical design

### 3.1 Hopper and cone (Items 1–3)

- **Outer shell (1):** Food-grade HDPE bucket or fabricated cylinder, **Ø340 mm OD × 280 mm** straight section, **3 mm** wall. Lid (1a) with **Ø60 mm** vent + insect screen and O-ring groove.
- **Cone insert (2):** PP or HDPE, **60° included angle**, **ID 310 mm → 68 mm** at throat (2 mm clearance over **Ø65 mm** metering inlet). Cone height **≈220 mm**. Bonded to shell with **FDA silicone** and **6× M5** bolts through flange (**PCD 280 mm**).
- **Extension ring (optional 3):** **+80 mm** height → ~30 L.

**Anti-bridging:** Steep 60° cone + throat ring **Item 11** (beveled ID 68→65 mm, **15 mm** long) prevents hang-up at square edge.

### 3.2 Metering housing (Items 4–6)

- **Upper housing (4):** PETG/PP print or machined PP, mates to cone throat, contains wiper mount and motor bracket.
- **Lower housing (5):** Same material, **Ø122 mm** bore for wheel clearance **0.8 mm/side**, integrates **Ø65 mm** drop bore and chute flange.
- **Gasket (6):** **1.5 mm** silicone, sandwiched between 4 and 5, **4× M4×25** cap screws **PCD 95 mm**.

### 3.3 Rotary metering wheel (Item 7)

- **OD 120.0 mm**, **overall width 28 mm**, **6× pockets** at **60°** spacing.
- **Pocket:** **25 mm** deep (axial), **18 mm** wide at rim, **5 mm** floor thickness at hub side; rim lip **1 mm** to retain feed until over drop.
- **Material:** PETG (dry) or **UHMW-PE** (low friction, washable). **Not** PLA (creeps in heat).
- **Shaft:** **Ø6 mm** 304 SS, **40 mm** exposed; **2× M2 set screws** or **1.5×3 mm** dowel pin.
- **Magnet pocket:** **Ø6×3 mm** neodymium (Item 26) press-fit **one pocket**, triggers Hall once/rev.

**Rotation:** **Clockwise** viewed from motor (adjustable in firmware).

### 3.4 Anti-jam mechanism (Items 8–9)

- **Flexible wiper (8):** **80×25×3 mm** **70A silicone** or **PA12** finger, **15 mm** into throat, mounted at **35°** to vertical on pin **Ø3 mm**.
- **Agitator cam (9):** **PETG**, **Ø8 mm** bump on wheel face hits wiper root every **60°**, **0.5 mm** deflection — breaks bridges without crushing pellets.
- **Throat clearance:** Wiper tip to wheel crown **2–3 mm** (adjust via slotted mount **±4 mm**).

### 3.5 Outlet and trough (Items 10, 12–13)

- **Chute (10):** **Ø65→50 mm** taper, **120 mm** long, **30°** down to trough; **removable** for cleaning.
- **Trough (12):** **600×200×120 mm** HDPE, **2× hinged lid** sections, **Ø3 mm** drain holes every **100 mm**.
- **Stand (13):** **32×32 mm** treated lumber or **40×40×2 mm** aluminum tube, **850 mm** feed height (adjust **700–950 mm**).

### 3.6 Drive train (Items 14–16)

- **Motor (14):** **12 V 30:1** micro metal gearmotor (e.g. GA12-N20 class), **~200 RPM** motor → **~6.7 RPM** output; **2:1** belt or gear → **~10 RPM** wheel (**≈6 s/rev**).
- **Motor bracket (15):** slotted for tension, **2× M3** to housing.
- **Coupling (16):** **5 mm** motor shaft to **Ø6 mm** wheel shaft — ** helical slit PETG** or **brass tube + set screw**.

**Stall current:** Fuse **500 mA** on motor line; firmware stops after **2 s** stall.

---

## 4. Electronics

### 4.1 Components

| Ref | Part | Notes |
|-----|------|--------|
| 20 | 12 V 2 A PSU | Indoor or weatherproof box |
| 21 | Controller board | Arduino Nano + DS3231 RTC (or custom PCB) |
| 22 | Hall sensor | A3144 / OH44E, open-collector |
| 23 | Manual button | IP65 momentary, panel mount |
| 24 | N-channel MOSFET | IRLZ44N or AO4407 logic-level |
| 25 | Flyback diode | 1N5819 across motor |

### 4.2 Wiring (see `drawings/wiring-diagram.svg`)

- **12 V GND** common at PSU; **star ground** at controller.
- **Motor:** MOSFET low-side switch, diode cathode to **+12 V**.
- **Hall:** **10 kΩ** pull-up to **5 V** (or **3.3 V**), signal to digital input with **100 nF** debounce cap.
- **Button:** INPUT_PULLUP, active low.
- **Enclosure:** IP54, **grommet** for motor/sensor cables.

### 4.3 Firmware behavior (sketch)

1. On schedule (e.g. **06:30** and **16:00**), run **N** revolutions (default **7** → ~42 portions ≈ **1.0–1.2 kg**).
2. Count Hall pulses; stop when count = **6×N** (or **N** if one pulse/rev — magnet placement gives **1 pulse/rev**).
3. Manual button: **1 revolution** (6 portions) per press, **3 s** debounce.
4. **Max run 30 s** timeout; **stall detect** if no Hall edge in **4 s** while motor on.

---

## 5. Assembly sequence (exploded view order)

1. Install **Hall sensor (22)** and **motor (14)** in **lower housing (5)**.  
2. Press **magnet (26)** into **wheel (7)**; mount **wiper (8)** and **cam (9)**.  
3. Join **upper (4)** + **lower (5)** with **wheel** on **Ø6 shaft**; torque **M4** to **2 N·m**.  
4. Bolt **cone (2)** to hopper **(1)**; mount assembly **(4–5)** to cone throat (**4× M5**).  
5. Attach **chute (10)** and **trough (12)**; route cable to **enclosure (20–21)**.  
6. Calibrate: weigh **10 revolutions**, adjust `gramsPerRev` in firmware.

---

## 6. Maintenance and reliability

- **Weekly:** Empty trough, inspect wiper wear, wipe cone interior.  
- **Monthly:** Disassemble **4–5–7**, wash with mild detergent; check gasket.  
- **Moisture:** Lid vent downwind; desiccant bag in lid optional; electronics **not** in hopper.  
- **Blockage:** If stall timeout trips, manual button runs **reverse 1/6 rev** (optional H-bridge) or user clears throat.

---

## 7. Drawing index

| File | Content |
|------|---------|
| `isometric-cutaway.svg` | Full assembly, cutaway, flow arrows |
| `side-section.svg` | Vertical section, dimensions |
| `top-view.svg` | Plan, bolt circles, motor/sensor |
| `anti-jam-detail.svg` | Wiper, cam, clearances |
| `dosing-wheel-detail.svg` | Pocket geometry, magnet |
| `wiring-diagram.svg` | Power and signals |
| `exploded-assembly.svg` | BOM items exploded |

---

## 8. Bill of materials

| # | Description | Material / spec | Qty | Key dimensions |
|---|-------------|-----------------|-----|----------------|
| 1 | Hopper shell | Food HDPE | 1 | Ø340×280 mm, 3 mm wall |
| 1a | Hopper lid | HDPE + SS mesh | 1 | Ø340, vent Ø60 mm |
| 2 | Cone insert | PP | 1 | 60° cone, ID 310→68 mm |
| 3 | Extension ring (opt.) | HDPE | 1 | +80 mm height |
| 4 | Meter upper housing | PETG/PP | 1 | See drawing |
| 5 | Meter lower housing | PETG/PP | 1 | Bore Ø122, drop Ø65 |
| 6 | Housing gasket | Silicone sheet | 1 | 1.5 mm, PCD 95 |
| 7 | Metering wheel | UHMW/PETG | 1 | Ø120×28, 6 pockets |
| 8 | Flexible wiper | 70A silicone | 1 | 80×25×3 mm |
| 9 | Agitator cam | PETG | 1 | Ø8×4 mm lump |
| 10 | Outlet chute | PP tube | 1 | Ø65→50, L=120 mm |
| 11 | Throat ring | PP | 1 | Bevel 68→65 mm |
| 12 | Covered trough | HDPE | 1 | 600×200×120 mm |
| 13 | Stand | Alu/timber | 1 | H≈850 mm |
| 14 | Geared motor | 12 V 30:1 | 1 | GA12-N20 class |
| 15 | Motor bracket | 2 mm Al | 1 | Slotted |
| 16 | Shaft coupling | Brass/PETG | 1 | 5→6 mm |
| 17 | Wheel shaft | 304 SS | 1 | Ø6×60 mm |
| 18 | Bearings (opt.) | 606ZZ | 2 | Press in housing |
| 19 | Fasteners kit | SS A2 | 1 | M3/M4/M5 assortment |
| 20 | Power supply | 12 V 2 A | 1 | IEC or barrel |
| 21 | Controller | Nano+RTC | 1 | DS3231 module |
| 22 | Hall sensor | A3144 | 1 | 3-wire |
| 23 | Manual button | IP65 | 1 | Panel mount |
| 24 | MOSFET + heatsink | IRLZ44N | 1 | Logic level |
| 25 | Flyback diode | 1N5819 | 1 | — |
| 26 | Magnet | NdFeB N35 | 1 | Ø6×3 mm |
| 27 | Enclosure | ABS IP54 | 1 | 120×80×60 mm |
| 28 | Wire + fuse | 18 AWG, 500 mA | — | Motor line fused |

**Suggested print settings (4, 5, 7, 9):** 4 walls, 30% gyroid, PETG **0.28 mm**, oriented for water drain (no horizontal cup pockets).

---

## 9. Tolerance and inspection

- Wheel OD: **120.0 ±0.15 mm**; housing bore: **122.0 +0.2/−0 mm**.  
- Runout: **<0.3 mm** TIR on wheel OD.  
- Drop alignment: pocket center ± **2 mm** over **Ø65** bore.  
- Leak test: dry corn — **no dribble** when motor stopped >24 h.

---

*End of design document CF-FEED-001 rev A*
