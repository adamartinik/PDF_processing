## PDF Screenshot Tool v2.0 – README

### Prehľad

GUI nástroj pre rýchle vytváranie PDF z postupných snímok obrazovky. Aplikácia umožňuje:
- vyrezať definovanú oblasť obrazovky (X1, Y1, X2, Y2),
- vykonať viacnásobné snímanie pri posúvaní dokumentu,
- konvertovať vytvorené PNG súbory do jedného PDF,
- prípadne PNG po skončení automaticky odstrániť.

### Kľúčové vlastnosti

- **Tri karty**: Complete Process, Screenshots Only, PNG → PDF.
- **Živý náhľad rozmerov** vybranej oblasti (šírka × výška).
- **Indikácia priebehu** a status riadky pre každú kartu.
- **Moderný vzhľad**: macOS `aqua` téma s fallbackom `clam`, svetlé pozadie, biele popisky, konzistentné štýly.
- **Bezpečne na pozadí**: dlhšie operácie bežia vo vláknach a UI ostáva responzívne.

### Požiadavky

- Python 3.9+ (odporúčané)
- Knižnice:
  - `tkinter` (súčasť štandardnej distribúcie Pythonu)
  - `Pillow` (PIL)
  - `pyautogui`

### Inštalácia závislostí

```bash
python3 -m pip install --upgrade pip
python3 -m pip install pillow pyautogui
```

Na macOS môže `pyautogui` vyžadovať dodatočné balíky (napr. `pyobjc`). Ak by inštalácia zlyhala, doinštalujte:

```bash
python3 -m pip install pyobjc
```

### Oprávnenia na macOS

Pre snímanie obrazovky musí mať Python/Terminal povolenie v System Settings:
- Privacy & Security → Screen Recording → povoliť pre váš interpreter (Terminal, iTerm, VS Code, atď.).
- V prípade problémov reštartujte aplikáciu a zrušte/znovu povoľte oprávnenie.

### Spustenie

```bash
python3 supertool_v2.py
```

### Popis rozhrania

#### Complete Process
- Zadáte oblasť snímania: `Top-Left (X1, Y1)` a `Bottom-Right (X2, Y2)`.
- Zadáte `Number of pages` a `Output folder name`.
- Voliteľne zaškrtnete „Delete PNG files after PDF creation“.
- Stlačením „Start Complete Process“ prebehne:
  1) Snímkovanie (s 5 s odpočtom),
  2) Konverzia PNG → PDF,
  3) (voliteľné) odstránenie PNG.
- Po skončení sa sprístupnia tlačidlá „Open PDF“ a „Open Folder“.

#### Screenshots Only
- Rovnaké nastavenie oblasti.
- `Start Screenshots` vytvorí len PNG súbory (bez PDF kroku).

#### PNG → PDF
- Vyberiete priečinok s PNG.
- Zadáte názov výsledného PDF.
- Klikom na „Create PDF“ sa PNG zoradia podľa mena a spoja do jedného PDF.

### Štýlovanie a témy

- Aplikácia používa tému `aqua` (macOS), s automatickým fallbackom `clam`.
- Všetky `ttk.Label` sú nastavené tak, aby mali biely text; dedičstvo pozadia je z kontajnera.
- Karty Notebooku: biely tučný text, rovnaká šírka kariet, bez „raised“ efektu na aktívnej karte.
- Polia `Entry` a sekundárne tlačidlá majú tmavý text pre čitateľnosť na svetlom pozadí.

### Tipy pre snímanie

- Zvoľte oblasť tak, aby neprekážal panel úloh/dok/horný panel systému.
- Pred štartom nastavte dokument na prvú stránku a kurzor mimo snímanej oblasti.
- Posun strán prebieha simulovaním klávesu „Down“. Ak aplikácia neposúva, aktivujte okno s dokumentom pred štartom.

### Typické pracovné postupy

1) Kompletný proces od snímok po PDF:
   - Complete Process → nastavte oblasť, počty, názov priečinka → Start Complete Process.
2) Najprv snímky, neskôr PDF:
   - Screenshots Only → Start Screenshots → PNG → PDF.

### Formát výstupov

- PNG: `strana_XX.png` v priečinku `~/Desktop/<Output folder name>`.
- PDF: `<Output folder name>.pdf` uložené do rovnakého priečinka.

### Riešenie problémov

- „Invalid coordinates“: skontrolujte, že `X2 > X1` a `Y2 > Y1`.
- „No PNG files found“: pre konverziu musia byť v priečinku súbory s príponou `.png`.
- Čierne/šedé náhľady na macOS: skontrolujte povolenia Screen Recording.
- Farby/štýl sa nemení: na niektorých systémoch môže `aqua` nie byť dostupná – funguje fallback `clam`.

### Klávesové skratky a interakcie

- Počas snímania sa simuluje kláves `Down` medzi stránkami.
- Ak potrebujete iný spôsob posunu (PageDown/Šípka), upravte obsluhu v kóde (`pyautogui.press('down')`).

### Bezpečnosť a ochrana súkromia

- Snímky obrazovky sa ukladajú lokálne do vášho profilu používateľa (`~/Desktop`).
- Nástroj neposiela žiadne dáta na internet.

### Rozšírenia a nápady (Roadmap)

- Voľba klávesu pre posun (Down/PageDown/Custom).
- Adaptívny delay medzi stránkami.
- Podpora iných formátov vstupu (JPG, TIFF) pri konverzii do PDF.
- Kompresia PDF a voľba kvality.

### Zmeny vo verzii v2

- Nový vzhľad a svetlá paleta.
- macOS `aqua` téma s fallbackom `clam`.
- Biele labely, odstránenie sivého podfarbenia, lepšie dedenie pozadia.
- Notebook karty: biely tučný text, rovnaká šírka, odstránený „raised“ efekt.
- Stabilnejšie vlákna pre dlhé operácie, zreteľné status správy a progress bary.

### Licencia

Použitie podľa interných pravidiel projektu, prípadne doplňte konkrétnu licenciu (MIT/Apache-2.0 atď.).

### Podpora

Problémy a návrhy otvárajte ako issues v repozitári alebo kontaktujte udržiavateľa projektu.


