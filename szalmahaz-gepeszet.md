# SZALMAHÁZ – ÉPÜLETGÉPÉSZETI ÉS ENERGIARENDSZER MÉLYKUTATÁSI FELADAT

## 0. SZEREPED ÉS A KUTATÁS CÉLJA

Te egy több szakterületet koordináló, magas szintű épületgépészeti, épületfizikai, energetikai, ökológiai és gazdasági kutató-agent vagy.

A feladatod nem egy előre kiválasztott technológia igazolása.

A feladatod az, hogy a rendelkezésre álló projektinformációk alapján:

1. feltárd az összes érdemben szóba jöhető műszaki megoldást,
2. objektíven megvizsgáld azok műszaki, gazdasági, ökológiai és üzemeltetési tulajdonságait,
3. az egymással kombinálható rendszereket is vizsgáld,
4. azonosítsd a kombinációk előnyeit és a komplexitásból fakadó hátrányokat,
5. számítsd ki vagy becsüld meg a beruházási és hosszú távú költségeket,
6. vizsgáld meg az energia- és részleges hálózatfüggetlenséget,
7. vizsgáld meg az önellátás lehetőségét,
8. vizsgáld meg az ökológiai és életciklus-szempontokat,
9. tárd fel az egyes megoldások kockázatait és bizonytalanságait,
10. végül adj több, egymástól műszakilag és filozófiailag is eltérő, koherens rendszerkoncepciót.

A végső következtetésnél NE indulj ki abból, hogy a jelenlegi elképzelések valamelyike biztosan jó.

A projektgazdák elképzeléseit és preferenciáit követelményként, prioritásként vagy vizsgálandó hipotézisként kezeld, de soha ne tekintsd bizonyított műszaki ténynek.

---

# 1. PROJEKTDOKUMENTUMOK ELSŐDLEGES FORRÁSA

A projekt GitHub repository:

https://github.com/pitiboy/ultetes

Elsőként olvasd be és dolgozd fel a repository releváns dokumentumait.

Kiemelten:

`szalmahaz.md`

FONTOS:

- ne feltételezd, hogy a dokumentumok teljesek;
- ne kérdezd újra azt, ami már egyértelműen szerepel bennük;
- keresd meg az ellentmondásokat;
- keresd meg a hiányzó, de a gépészeti döntéshez szükséges adatokat;
- a Google Drive-ra mutató hivatkozásokat is azonosítsd;
- ha ezek tartalma hozzáférhető, dolgozd fel;
- ha nem hozzáférhetőek, ezt külön jelöld.

A projekt dokumentációjában szereplő régi, bizonytalan vagy esetleg elavult jogi, építésügyi, energetikai vagy műszaki adatokat ne tekintsd automatikusan aktuálisnak.

---

# 2. ELSŐ FÁZIS – PROJEKTREKONSTRUKCIÓ

A kutatás előtt készíts egy strukturált projektprofilt.

Fogalmazd meg:

## Épület

- helyszín
- település
- tervezett hasznos alapterület
- lehetséges alaprajzi változatok
- pince
- földszint
- esetleges későbbi tetőtér
- tájolás
- tervezett használat
- várható használati mód változása

## Szerkezet

Különítsd el:

- ismert adat
- tervezett adat
- feltételezés
- hiányzó adat

Különösen:

- szalmabála fal
- palló/fa váz
- vályogtapasztás/vályogvakolat
- belső és külső rétegrend
- födém
- tető
- padló
- pince
- nyílászárók
- légtömörség

NE fogadj el automatikusan egy feltételezett U-értéket.

Ha a későbbi számításokhoz szükséges, határozz meg több reális rétegrendi változatot.

---

# 3. HIÁNYZÓ PARAMÉTEREK

A kutatás kezdetén készíts:

## „Hiányzó / tisztázandó paraméterek” listát

Csak olyan kérdéseket tegyél fel, amelyek ténylegesen befolyásolhatják a műszaki vagy gazdasági eredményt.

Kategóriák:

- épületfizika
- használat
- fűtés
- HMV
- szellőzés
- elektromos rendszer
- napelem
- akkumulátor
- szennyvíz
- pince
- költségkeret
- kivitelezési lehetőségek
- jogszabály / engedélyezés

Ne kérdezz feleslegesen.

Ha egy paraméter hiányzik, de ésszerű tartomány megadható, akkor:

1. adj meg egy feltételezett tartományt,
2. számolj több forgatókönyvvel,
3. jelöld világosan, hogy ez feltételezés.

Ne állítsd le a kutatást minden hiányzó adat miatt.

---

# 4. ALAPELV – TECHNOLÓGIAI SEMLEGESSÉG

Különösen fontos:

NE indulj ki abból, hogy:

- a hőszivattyú jó;
- a tömegkályha jó;
- a fatüzelés jó;
- az elektromos fűtés rossz;
- a napelem mindig gazdaságos;
- az akkumulátor mindig szükséges;
- az off-grid mindig jobb;
- a gépesítés mindig jobb;
- a low-tech mindig ökológiaibb.

Ezeket vizsgáld meg.

A kutatás eredménye változtathatja meg az eredeti feltételezéseket.

---

# 5. ÉPÜLETFIZIKA – EZ LEGYEN A KUTATÁS ALAPJA

A gépészeti rendszert ne önmagában vizsgáld.

Először becsüld meg az épület várható:

- hőveszteségét,
- fűtési energiaigényét,
- csúcshőigényét,
- hőtároló képességét,
- felfűtési dinamikáját,
- lehűlési dinamikáját,
- nyári hőterhelését.

Vizsgáld külön:

### A szalmabála + vályog kombináció hatását

- hőszigetelés
- hőtárolás
- fáziseltolás
- páratechnika
- nedvesség
- légtömörség
- belső felületi hőmérséklet
- túlmelegedés
- szerkezeti tartósság

Különösen vizsgáld:

> Mennyiben változtatja meg egy nagy hőtároló tömegű, szalmával jól szigetelt, vályoggal vakolt kis épület gépészeti igényét egy hagyományos családi házhoz képest?

---

# 6. HASZNÁLATI PROFIL

Külön vizsgáld a következő üzemállapotokat:

### A. Hétvégi használat

Például:

- péntek esti érkezés
- szombat
- vasárnap
- távozás

### B. Folyamatos téli használat

### C. Átmeneti időszak

Például:

- 5–15 °C külső hőmérséklet
- napközben napsütés
- este rövid idejű fűtési igény

### D. Hálózatkimaradás

### E. Hosszabb borús időszak

### F. Nyári meleg

Ne feltételezd, hogy minden üzemállapothoz ugyanaz a fűtési rendszer optimális.

---

# 7. FŰTÉSI ALTERNATÍVÁK

Vizsgáld meg legalább az alábbiakat, de ne korlátozd magad erre:

## Fatüzelés

- tömegkályha
- cserépkályha
- kandalló
- kályha
- rakétakályha, ha műszakilag releváns
- faelgázosító kazán
- fa + puffertároló
- csikótűzhely / sparhelt
- ezek kombinációi

## Pellet

- pelletkályha
- pelletkazán

## Hőszivattyú

- levegő-levegő
- levegő-víz
- talajszondás
- talajkollektoros
- egyéb releváns megoldások

## Elektromos

- elektromos padlófűtés
- elektromos fűtőpanel
- infrapanel
- elektromos kazán
- egyéb direkt elektromos megoldások

## Egyéb

Vizsgáld meg azokat az alternatívákat is, amelyek 2026-ban vagy a következő néhány évben technológiailag relevánsak lehetnek.

Ha egy technológiát kizársz, indokold meg.

---

# 8. HŐLEADÓ RENDSZEREK

Vizsgáld:

- padlófűtés
- falfűtés
- mennyezetfűtés
- radiátor
- fan-coil
- légfűtés
- klímás hőleadás
- közvetlen sugárzó fűtés
- tömegkályha közvetlen hőleadása

Minden esetben vizsgáld:

- reakcióidő
- komfort
- alacsony hőigényű épülethez való illeszkedés
- túlméretezés
- szabályozhatóság
- áramszüneti működés
- karbantartás
- élettartam
- javíthatóság

---

# 9. GYORS RÁSEGÍTŐ FŰTÉS

Külön kutatási kérdés:

> Mi a legésszerűbb megoldás olyan enyhe időszakokban, amikor csak 30–120 perces gyors fűtési igény jelentkezik?

Vizsgáld például:

- kis fatüzelés
- tömegkályha üzemmód
- sparhelt
- kandalló
- levegő-levegő hőszivattyú
- elektromos fűtés
- infrapanel
- egyéb lehetőség

NE feltételezd előre, hogy valamelyik a megfelelő.

---

# 10. MELEGVÍZ

A HMV-t önálló alrendszerként vizsgáld.

Lehetséges megoldások:

- elektromos bojler
- hőszivattyús bojler
- fatüzelésből HMV
- tömegkályha / csikótűzhely hőhasznosítása
- indirekt tároló
- napkollektor
- PV + villamos HMV
- kombinált megoldások

Vizsgáld azt is, hogy érdemes-e egyáltalán a fűtéssel szorosan összekapcsolni.

Ne tekintsd kötelezőnek a fatüzelésből történő HMV-t.

---

# 11. SZELLŐZÉS

Vizsgáld:

- természetes szellőzés
- ablakos szellőzés
- decentralizált hővisszanyerős szellőzés
- központi hővisszanyerős szellőzés
- hibrid megoldások

Különösen fontos:

- szalmabála szerkezet
- vályog
- légtömörség
- páraterhelés
- pince
- fürdő
- konyha
- gombatermesztő pince

Vizsgáld, hogy a hővisszanyerős szellőzés mennyire indokolt egy ilyen kis, alacsony energiaigényű épületben.

---

# 12. HŰTÉS ÉS NYÁRI ÜZEM

NE kezeld kötelező követelményként az aktív hűtést.

Először vizsgáld:

- tájolás
- árnyékolás
- üvegezés
- pergola
- növényzet
- éjszakai szellőzés
- vályog hőtárolása
- szalma hőtechnikai viselkedése
- tető kialakítása
- pince hőhatása

Ez alapján becsüld meg az aktív hűtési igényt.

Ha egy fűtési rendszer egyben hűteni is tud, azt külön előnyként értékeld, de csak akkor, ha a többletköltség és komplexitás indokolható.

---

# 13. ELEKTROMOS ENERGIARENDSZER

A projekt meglévő rendszere:

- kb. 3,5 kWp napelem
- kb. 12 kWh akkumulátortároló
- jelenleg szigetüzemű rendszer
- elsősorban az általános elektromos fogyasztást szolgálja
- nem cél nagy mennyiségű akkumulátort használni fűtésre

Az új épület néhány méterre lesz a jelenlegi rendszertől.

Lehetséges:

- átkötés
- vészhelyzeti energiaátvitel
- kábelezés
- megfelelő elektromos infrastruktúra kialakítása

A kutatás során ne feltételezd, hogy a meglévő akkumulátort közvetlenül a fűtésre kell használni.

Vizsgáld meg:

- mire elegendő a meglévő rendszer;
- milyen fogyasztásokat tud biztosítani;
- mennyi ideig;
- milyen téli korlátai vannak;
- szükséges-e PV-bővítés;
- szükséges-e akkumulátorbővítés;
- milyen fogyasztásokat célszerű hálózatról működtetni;
- mi legyen áramszünetkor automatikusan lekapcsolható;
- mi működjön manuálisan;
- mi legyen nem elektromos.

---

# 14. RÉSZLEGES OFF-GRID KONCEPCIÓ

A cél nem feltétlenül a teljes off-grid rendszer.

Az alapvető filozófia:

> hálózat jelenlétében legyen kényelmes és gazdaságos;
> hálózat kiesésekor a nem létfontosságú fogyasztások visszafogásával a ház továbbra is működőképes maradjon.

Különösen a fűtés legyen lehetőleg:

- nem elektromos függőségű,
- manuálisan működtethető,
- javítható,
- helyben rendelkezésre álló erőforrásra építhető.

Vizsgáld meg a részleges off-grid és teljes off-grid közötti gazdasági különbséget.

Ne feltételezd, hogy a teljes off-grid gazdaságilag racionális.

---

# 15. ÖNELLÁTÁS

A projekt egyik kiemelt célja a külső rendszerektől való nagyfokú függetlenség.

A függetlenségi igény körülbelül:

**9/10**

Vizsgáld:

- tüzelőanyag-önellátás
- fa beszerzés
- saját faanyag lehetősége
- szárítás
- tárolás
- energia
- villamos energia
- HMV
- szellőzés
- fűtés
- karbantartás
- alkatrészfüggőség
- szakemberfüggőség
- hálózatfüggőség

Ne csak azt vizsgáld:

> „működik-e?”

Hanem:

> „mennyire lehet külső szolgáltatóktól és infrastruktúrától függetlenül fenntartani 10–30 éven keresztül?”

---

# 16. KOMPLEXITÁS

A több rendszer kombinációja nem automatikusan előny.

Minden rendszerkombinációnál értékeld:

- komponensek száma
- szabályozási komplexitás
- egymásra utaltság
- hibapontok száma
- karbantartási igény
- szakemberigény
- javíthatóság
- alkatrészellátás
- áramszüneti működés
- felhasználói beavatkozás szükségessége

Külön vizsgáld:

### Redundancia

Mi történik, ha:

- az egyik rendszer meghibásodik?
- nincs áram?
- nincs tüzelőanyag?
- nincs napsütés?
- meghibásodik egy vezérlő?
- meghibásodik egy szivattyú?
- meghibásodik az inverter?

A cél nem a maximális redundancia.

A cél az:

> **ésszerű redundancia minimális szükségtelen komplexitással.**

---

# 17. ÖKOLÓGIAI ÉRTÉKELÉS

Az ökológiai értékelést ne egyszerűsítsd le CO₂-ra.

Vizsgáld:

- életciklus-emisszió
- primerenergia
- beágyazott energia
- nyersanyagigény
- ritka anyagok
- gyártási energia
- szállítás
- üzemeltetés
- karbantartás
- cserealkatrészek
- élettartam
- újrahasznosíthatóság
- javíthatóság
- helyi erőforrások
- légszennyezés
- biomassza fenntarthatósága
- elektromos energia forrása

Különösen:

> A „megújuló” ne jelentsen automatikusan „ökológiailag jobb” minősítést.

Például a fatüzelésnél külön vizsgáld:

- fenntartható erdőgazdálkodás
- fa szárítása
- hatásfok
- részecskekibocsátás
- NOx
- szén-monoxid
- helyi levegőminőség
- tüzelőanyag-szállítás

---

# 18. GAZDASÁGI MODELLEZÉS – KÖTELEZŐ

A gazdasági elemzés legyen számszerű.

A lehető legjobb 2026-os magyarországi árakat használd.

Mindenhol:

- Ft
- Ft/év
- kWh/év
- kWh hő
- COP/SCOP
- tüzelőanyag-mennyiség
- karbantartás
- élettartam

szerepeljen, ahol értelmezhető.

## Beruházási költség

Becsüld meg:

- készülék
- anyag
- szerelés
- szabályozás
- gépészet
- kémény
- tároló
- puffertartály
- hőleadók
- villamos infrastruktúra
- PV
- akkumulátor
- szellőzés
- HMV

Különítsd el:

- anyagköltség
- munkadíj
- járulékos költség

Ha csak intervallum adható:

**X–Y Ft**

formában add meg.

---

# 19. 10 / 20 / 30 ÉVES TCO

Minden releváns rendszerre számíts:

### 10 év
### 20 év
### 30 év

teljes tulajdonlási költséget.

TCO:

**CAPEX + energia + karbantartás + javítás + komponenscsere – releváns maradványérték**

Ha szükséges, számíts:

- nominális TCO
- diszkontált jelenértékű TCO

is.

A diszkontráta legyen explicit.

---

# 20. ÉLETTARTAM ÉS CSERE

Külön számold:

- inverter
- akkumulátor
- hőszivattyú
- kompresszor
- szivattyúk
- ventilátorok
- vezérlések
- bojler
- kémény
- tömegkályha
- napelem

várható élettartamát.

Ne használj egyetlen optimista élettartamot.

Adj:

- tipikus
- kedvező
- kedvezőtlen

forgatókönyvet, ha indokolt.

---

# 21. ENERGIAÁR-SZENZITIVITÁS

Vizsgáld legalább:

### kedvező
### alap
### kedvezőtlen

energiaár-forgatókönyvvel.

Külön:

- villamos energia
- tűzifa
- pellet
- egyéb energiaforrás

Ha egy ár jövőbeli alakulása nem becsülhető megbízhatóan, ne találj ki számot.

Adj érzékenységvizsgálatot.

---

# 22. 2027–2029 VÁRHATÓ ÁRAK ÉS TÁMOGATÁSOK

Külön fejezetben vizsgáld a következő 2–3 év várható változásait.

Vizsgáld:

- lakossági energiaárak
- napelemárak
- akkumulátorárak
- hőszivattyúárak
- fa/pellet árak
- szerelési költségek
- építőanyagok
- támogatási programok
- pályázatok
- adók
- szabályozási változások

FONTOS:

### Tilos kitalálni jövőbeli támogatásokat.

A következő kategóriákat külön kezeld:

**MEGERŐSÍTETT**
- hivatalos döntés
- kihirdetett jogszabály
- hivatalos pályázati kiírás

**VALÓSZÍNŰ / INDOKOLT FELTÉTELEZÉS**
- megfelelő forrás alapján indokolt trend

**SPEKULÁCIÓ**
- csak akkor szerepelhet, ha világosan annak nevezed.

Ha nincs megfelelő bizonyíték:

> „Nem áll rendelkezésre kellően megbízható adat.”

A bizonytalanság jobb válasz, mint egy kitalált szám.

---

# 23. FORRÁSKEZELÉS

A kutatás egyik legfontosabb része a forrásminőség.

Preferált sorrend:

1. magyar jogszabály / hivatalos állami forrás
2. hivatalos hatóság
3. gyártói műszaki dokumentáció
4. szabvány / szakmai szervezet
5. tudományos publikáció
6. egyetemi / kutatóintézeti anyag
7. szakmai kereskedő
8. kivitelezői árlista
9. fórum / Reddit / közösségi tapasztalat

A forrásoknál mindig legyen:

- dátum
- URL
- forrás típusa
- milyen állítást támaszt alá

A marketingállításokat kezeld kritikusan.

---

# 24. FORRÁSOK KERESÉSÉNEK SZABÁLYAI

Minden lényeges számszerű állítást próbálj legalább egy elsődleges vagy magas minőségű forrással alátámasztani.

Ha árakat több helyről találsz:

- legalább 3 független adatpontot keress, ha ez reálisan lehetséges;
- mutasd a tartományt;
- ne használj egyetlen webshop árát „piaci árként”.

A magyarországi árak legyenek prioritásban.

Külföldi adatot csak akkor használj, ha:

- magyar adat nincs;
- vagy a műszaki paraméterhez releváns.

Ilyenkor jelezd az eltérést.

---

# 25. SZÁMÍTÁSI FEGYELEM

Minden számításnál írd le:

- bemeneti adatok
- feltételezések
- képlet / módszer
- eredmény
- bizonytalanság

Ne rejtsd el a feltételezéseket.

Ha egy szám csak nagyságrendi becslés:

> „nagyságrendi becslés”

jelöléssel használd.

---

# 26. RENDSZERKONCEPCIÓK

A kutatás végén ne egyetlen rendszert javasolj.

Alakíts ki legalább 4–6 koherens rendszerkoncepciót.

Például csak szemléltetésként:

- low-tech / magas önállóság
- fatüzelés-központú hibrid
- hőszivattyús
- minimális gépészetű
- elektromos + PV
- többféle redundanciát alkalmazó

De ezek csak példák.

A tényleges koncepciókat a kutatás eredménye alapján hozd létre.

---

# 27. MINDEN RENDSZERKONCEPCIÓHOZ

Mutasd meg:

- működési elv
- komponensek
- beruházási költség
- éves energiaigény
- éves költség
- karbantartás
- 10 éves TCO
- 20 éves TCO
- 30 éves TCO
- várható élettartam
- áramszüneti működés
- részleges off-grid kompatibilitás
- önellátási lehetőség
- ökológiai hatás
- komplexitás
- meghibásodási kockázat
- javíthatóság
- szakemberfüggőség
- felhasználói munka
- előnyök
- hátrányok
- bizonytalanságok

---

# 28. FELHASZNÁLÓI MUNKA ÉS KÉNYELEM

Ne csak pénzben mérj.

Vizsgáld:

- napi munka
- heti munka
- éves karbantartás
- tüzelőanyag előkészítés
- tüzelőanyag tárolása
- hamuzás
- takarítás
- ellenőrzés
- manuális beavatkozás
- automatizálás

A projektgazdák kifejezetten hajlandók munkát vállalni a rendszer működtetéséért.

Ez előnyként kezelhető az alacsonyabb technológiai komplexitású rendszereknél.

De ne feltételezd, hogy a sok kézi munka automatikusan elfogadható: számszerűsítsd és írd le.

---

# 29. MEGBÍZHATÓSÁG

Vizsgáld:

- normál működés
- áramszünet
- hosszabb áramszünet
- inverterhiba
- szivattyúhiba
- vezérlési hiba
- tüzelőanyag-hiány
- extrém hideg
- hosszabb borús idő
- nyári hőhullám

Különösen:

> Mi történik, ha a rendszer legfontosabb aktív komponense meghibásodik?

És:

> A ház fűthető marad-e?

---

# 30. „FAIL-SAFE” ÉS VÉSZÜZEM

Minden rendszer esetében legyen:

### „Mi történik, ha minden elromlik?” elemzés.

Külön:

- áramszünet
- automatika meghibásodása
- szivattyú meghibásodása
- termosztáthiba
- inverterhiba
- kommunikációs hiba

A lehető legegyszerűbb kézi vészüzemet is vizsgáld.

---

# 31. BIZTONSÁG

Külön vizsgáld:

- CO
- tűz
- kémény
- füstgáz
- forró felületek
- forróvíz
- nyomás
- túlfűtés
- puffertartály
- tágulási tartály
- elektromos biztonság
- akkumulátor
- pince
- nedvesség
- penész
- szén-monoxid

A biztonsági követelményeknél elsődleges forrásokat használj.

---

# 32. SZALMABÁLA + FA VÁZ + VÁLYOG

Külön szakértői részben vizsgáld:

- páradiffúzió
- kapilláris nedvesség
- légszivárgás
- kondenzáció
- faváz nedvessége
- szalmabála nedvessége
- pince felől érkező nedvesség
- gépészeti áttörések
- kéményáttörések
- fűtési rendszerek hatása a szerkezetre
- hőhidak

Különösen fontos:

> A gépészeti rendszer hogyan befolyásolja a szalmabála és faváz hosszú távú tartósságát?

---

# 33. PINCE

A pince speciális funkcióit külön vizsgáld:

- kb. 30 m² gombatermesztés
- kb. 10 m² növénytárolás
- kb. 10 m² gépészet
- kb. 10 m² tárolás

A párás pince és a száraz gépészeti pince közötti kapcsolat különösen fontos.

Vizsgáld:

- szellőzés
- párakezelés
- légutánpótlás
- hőmérséklet
- gépészeti berendezések elhelyezése
- korrózió
- penész
- pince hőhatása a házra

---

# 34. SZENNYVÍZ

Bár a fő kutatás fókusza a fűtés és gépészet, vizsgáld röviden:

- közcsatorna
- száraz WC
- komposzt WC
- gyökérzónás kezelés
- Greenwater
- egyéb releváns decentralizált megoldások

Külön:

- beruházás
- üzemeltetés
- engedélyezés
- ökológia
- karbantartás
- hálózatfüggetlenség

---

# 35. AGENT ORCHESTRATION – CURSOR

A kutatást több specializált agent segítségével végezd.

NE használj indokolatlanul sok agentet.

A cél nem az agentek száma, hanem a kutatás minősége.

Javasolt felosztás:

## Agent 1 – Project Analyst

Feladata:

- projekt dokumentáció
- követelmények
- hiányzó adatok
- ellentmondások
- használati profil

## Agent 2 – Building Physics

Feladata:

- hőveszteség
- hőigény
- hőtárolás
- dinamika
- szalmabála
- vályog
- nyári túlmelegedés

## Agent 3 – Heating Systems

Feladata:

- minden releváns fűtési technológia
- hőleadók
- hibrid rendszerek
- áramszüneti működés

## Agent 4 – Renewable / Electrical

Feladata:

- PV
- akkumulátor
- részleges off-grid
- hálózat
- inverter
- energiamenedzsment
- backup

## Agent 5 – HMV / Ventilation / Cooling

Feladata:

- HMV
- szellőzés
- hővisszanyerés
- hűtés
- nyári üzem

## Agent 6 – Economics

Feladata:

- CAPEX
- OPEX
- TCO
- 10/20/30 év
- energiaárak
- árérzékenység
- támogatások

## Agent 7 – Ecology / Life Cycle

Feladata:

- LCA
- CO₂
- primerenergia
- anyagigény
- légszennyezés
- javíthatóság
- életciklus

## Agent 8 – Reliability / Resilience

Feladata:

- hibák
- áramszünet
- redundancia
- komplexitás
- javíthatóság
- önellátás

## Agent 9 – Independent Skeptic

Ez az agent kifejezetten arra szolgáljon, hogy:

- megtámadja a többi agent következtetéseit;
- keresse a rejtett feltételezéseket;
- ellenőrizze a számításokat;
- keresse a technológiai elfogultságot;
- keresse a túl optimista állításokat;
- ellenőrizze a forrásokat.

## Agent 10 – Chief Integrator

Feladata:

- az összes agent eredményének összefésülése;
- ellentmondások feloldása;
- egységes számítási modell létrehozása;
- rendszerkoncepciók létrehozása;
- végső jelentés elkészítése.

Ha a Cursor Agent környezet korlátozza az egyidejű agentek számát, a feladatokat ütemezetten végezd.

---

# 36. AGENTEK EGYÜTTMŰKÖDÉSE

Az agentek ne izoláltan dolgozzanak.

A munkafolyamat:

1. Project Analyst létrehozza a projektmodellt.
2. Building Physics meghatározza a hőigény kereteit.
3. A technológiai agentek ezek alapján dolgoznak.
4. Economics ezekből számol.
5. Ecology és Reliability külön értékel.
6. Independent Skeptic ellenőrzi az eredményeket.
7. Chief Integrator összeállítja a végső modellt.

Ne engedd, hogy egy technológiai agent a saját feltételezéseiből teljes projektmodellt építsen.

---

# 37. ELLENTMONDÁSOK KEZELÉSE

Ha két agent eltérő eredményre jut:

NE válassz automatikusan.

Vizsgáld:

- bemeneti adatok
- módszertan
- forrás
- feltételezés
- időpont
- alkalmazási környezet

Ha nem oldható fel:

> mutasd be mindkét eredményt és a bizonytalanság okát.

---

# 38. FÜGGETLEN ELLENŐRZÉS

A végleges jelentés előtt ellenőrizd:

- számításokat
- mértékegységeket
- árakat
- energiaárakat
- CAPEX-et
- TCO-t
- élettartamot
- támogatási információkat
- jogszabályi állításokat
- technológiai állításokat

A Chief Integrator nem fogadhatja el automatikusan a másik agent eredményét.

---

# 39. PONTOZÁS

Ha pontozást használsz, az ne legyen „jó/rossz” jellegű szubjektív értékelés.

A pontozási rendszer csak akkor használható, ha:

1. előre definiált;
2. mérhető;
3. reprodukálható;
4. minden technológiára azonos;
5. megmutatod a mögöttes adatokat.

Lehetséges dimenziók:

- CAPEX
- OPEX
- TCO
- önellátás
- hálózatfüggetlenség
- komplexitás
- karbantartás
- javíthatóság
- ökológiai hatás
- komfort
- üzembiztonság

Ha a pontozás félrevezető lenne, inkább használj összehasonlító táblázatot.

---

# 40. NE ADJ „VARÁZSLATOS” VÉGSŐ VÁLASZT

A végén ne csak azt írd:

> „Ezt a rendszert válassátok.”

Hanem mutasd meg:

### Milyen prioritások mellett melyik koncepció válik logikussá?

Például:

- ha az önellátás elsődleges;
- ha a minimális beruházás elsődleges;
- ha a minimális munka elsődleges;
- ha a maximális komfort elsődleges;
- ha a legalacsonyabb TCO elsődleges;
- ha az ökológiai lábnyom elsődleges;
- ha a meghibásodás elleni robusztusság elsődleges.

A projektgazdák döntését ne helyettesítsd.

---

# 41. VÉGSŐ JELENTÉS FORMÁTUMA

A végső dokumentum Markdown legyen.

Javasolt szerkezet:

# Szalmabála ház – épületgépészeti és energetikai kutatás

## 1. Executive Summary

## 2. Projekt és követelmények

## 3. Kiindulási adatok

## 4. Hiányzó adatok és feltételezések

## 5. Épületfizikai modell

## 6. Várható hőigény

## 7. Fűtési technológiák

## 8. Hőleadó rendszerek

## 9. Gyors rásegítő fűtés

## 10. HMV

## 11. Szellőzés

## 12. Nyári hőterhelés és hűtés

## 13. PV és elektromos rendszer

## 14. Részleges off-grid működés

## 15. Önellátás

## 16. Komplexitás és redundancia

## 17. Ökológiai értékelés

## 18. Gazdasági elemzés

## 19. 10/20/30 éves TCO

## 20. Energiaár-szenzitivitás

## 21. 2027–2029 várható változások

## 22. Rendszerkoncepciók

## 23. Meghibásodási és vészüzemi forgatókönyvek

## 24. Kockázatok

## 25. Bizonytalanságok

## 26. Döntési mátrix

## 27. Következtetések

## 28. További kutatási kérdések

## 29. Forrásjegyzék

---

# 42. KÖTELEZŐ ÖSSZEHASONLÍTÓ TÁBLÁZAT

A végén legyen legalább egy nagy összehasonlító táblázat:

| Rendszer | CAPEX | Éves költség | 10 év TCO | 20 év TCO | 30 év TCO | Áramszünet | Önellátás | Komplexitás | Karbantartás | Ökológiai szempont | Komfort |
|---|---:|---:|---:|---:|---:|---|---|---|---|---|---|

Ahol nincs megbízható adat:

`N/A – nincs megbízható adat`

szerepeljen, ne kitalált érték.

---

# 43. MÁSODIK KÖTELEZŐ TÁBLÁZAT

Legyen egy:

## „Mi történik, ha...?” táblázat

| Esemény | Rendszer reakciója | Fűtés megmarad? | HMV megmarad? | Villamos energia | Manuális beavatkozás |
|---|---|---|---|---|---|
| Hálózat kiesik | | | | | |
| 3 nap borús idő | | | | | |
| Inverter meghibásodik | | | | | |
| Hőszivattyú meghibásodik | | | | | |
| Szivattyú meghibásodik | | | | | |
| Tüzelőanyag hiányzik | | | | | |
| Extrém hideg | | | | | |

---

# 44. HARMADIK KÖTELEZŐ TÁBLÁZAT

## „Önellátási függőségi térkép”

Vizsgáld:

| Erőforrás | Külső függőség | Saját előállítás lehetősége | Tárolhatóság | Vészhelyzeti alternatíva |
|---|---|---|---|---|
| Villamos energia | | | | |
| Tűzifa | | | | |
| HMV | | | | |
| Fűtés | | | | |
| Szellőzés | | | | |
| Szennyvíz | | | | |
| Alkatrész | | | | |
| Szakember | | | | |

---

# 45. BIZONYTALANSÁGI JELÖLÉS

Minden fontos adatot sorolj az alábbi kategóriák valamelyikébe:

🟢 **Magas bizonyosság**

🟡 **Közepes bizonyosság**

🔴 **Alacsony bizonyosság / becslés**

A bizonyosságot indokold.

---

# 46. KUTATÁSI ETIKA

Tilos:

- adatot kitalálni;
- árakat kitalálni;
- támogatást kitalálni;
- gyártói adatot átalakítani úgy, hogy annak más legyen a jelentése;
- bizonytalan adatot biztos tényként bemutatni;
- egy technológiát előnyben részesíteni pusztán azért, mert modern;
- egy technológiát hátrányba hozni pusztán azért, mert low-tech;
- egyetlen forrásból messzemenő következtetést levonni.

Ha nincs adat:

> „Nincs elegendő megbízható adat.”

Ha becslés:

> „Becslés – az alábbi feltételezésekkel.”

Ha feltételezés:

> „Feltételezés – a projekt jelenlegi információi alapján.”

---

# 47. A LEGFONTOSABB MÓDSZERTANI ELV

A kutatás ne a következő kérdésre próbáljon választ adni:

> „Hogyan valósítsuk meg a tömegkályhás, részben off-grid házat?”

Hanem erre:

> **„Milyen épületgépészeti és energetikai rendszer biztosítja ennek a konkrét épületnek a hosszú távon legjobb műszaki, gazdasági, ökológiai, önellátási, megbízhatósági és komfortprofilját, figyelembe véve a projektgazdák preferenciáit, de azokat nem tekintve előre eldöntött műszaki válasznak?”**

Ez legyen az egész kutatás vezérfonala.

---

# 48. VÉGSŐ MINŐSÉGELLENŐRZÉS

A végleges jelentés elkészítése előtt ellenőrizd:

- [ ] minden releváns fűtési technológia szerepel;
- [ ] nincs technológiai előítélet;
- [ ] az épületfizika megelőzi a gépészeti döntést;
- [ ] a hétvégi használat vizsgálva van;
- [ ] az állandó használat vizsgálva van;
- [ ] az átmeneti időszak vizsgálva van;
- [ ] az áramszünet vizsgálva van;
- [ ] a részleges off-grid működés vizsgálva van;
- [ ] az önellátás vizsgálva van;
- [ ] a komplexitás vizsgálva van;
- [ ] a redundancia vizsgálva van;
- [ ] az ökológiai életciklus vizsgálva van;
- [ ] a légszennyezés vizsgálva van;
- [ ] a 10/20/30 éves TCO elkészült;
- [ ] az energiaár-érzékenység elkészült;
- [ ] a 2027–2029 várható változásokat csak bizonyítható adatok alapján kezelted;
- [ ] nincs kitalált támogatás;
- [ ] nincs kitalált ár;
- [ ] minden jelentős számnak van forrása vagy explicit feltételezése;
- [ ] az ellentmondásokat feloldottad vagy bemutattad;
- [ ] az Independent Skeptic ellenőrzése megtörtént;
- [ ] a végső döntéshez szükséges kompromisszumok világosan látszanak.

---

# 49. VÉGSŐ FELADAT

A teljes kutatás végén készíts egy olyan döntéstámogató dokumentumot, amelyből egy építtető és egy építész/gépész szakember együtt képes:

1. megérteni az alternatívákat;
2. látni a költségeket;
3. látni a hosszú távú következményeket;
4. látni az ökológiai kompromisszumokat;
5. látni az önellátás mértékét;
6. látni a rendszer komplexitását;
7. látni a meghibásodási forgatókönyveket;
8. és végül saját döntést hozni.

A jelentés célja tehát nem egy technológia „eladása”, hanem a lehető legjobb minőségű, forrásolt és számszerűsített döntéstámogatás.



# végső kimenet 
Amennyiben eddig a dokumentum máshogy rendelkezett , akkor is a kimenet egy  fájl legyen itt a repository ban egy új prként .
Emellett, amennyiben lehetséges , grafikai elemeket is tartalmazhat a fájl, az összehasonlítás, és a megértés, döntés segítése érdekében 