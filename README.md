# PDF_processing
Screenshoting and processing documents
# 📸 PDF Screenshot Tool

Automatizovaný nástroj na vytváranie screenshotov z PDF dokumentov a ich konverziu späť do PDF formátu.

## 🎯 Funkcie

### 1. 📸 Automatické screenshoty PDF
- Automaticky prechádza cez stránky PDF dokumentu
- Robí screenshoty každej stránky v definovanej oblasti
- Ukladá obrázky ako PNG súbory do organizovaného priečinka

### 2. 🔄 Konverzia PNG → PDF
- Zlučuje viacero PNG obrázkov do jedného PDF súboru
- Zachováva kvalitu obrázkov
- Automatické zoradenie stránok

### 3. 🚀 Kompletný proces
- Kombinuje obe funkcie do jedného procesu
- Screenshoty + konverzia do PDF v jednom kroku
- Možnosť automatického vyčistenia PNG súborov po konverzii

## 📋 Požiadavky

- Python 3.x
- macOS (používa `pyautogui` a systémové príkazy pre Mac)

### Knižnice

```bash
pip3 install pyautogui Pillow
```

## 🚀 Inštalácia

1. Naklonuj repozitár:
```bash
git clone https://github.com/adamartinik/PDF_processing.git
cd PDF_processing
```

2. Nainštaluj závislosti:
```bash
pip3 install pyautogui Pillow
```

Alebo spusti script - automaticky ti ponúkne inštaláciu chýbajúcich knižníc.

## 💻 Použitie

### Spustenie nástroja

```bash
python3 supertool.py
```

### Hlavné menu

Po spustení sa zobrazí menu s možnosťami:

```
1. 📸 Len screenshoty PDF súboru
2. 🔄 Len konverzia PNG → PDF
3. 🚀 Screenshoty + konverzia do PDF (kompletný proces)
4. ❌ Ukončiť
```

### Postup pre screenshoty (možnosť 1 alebo 3)

1. Otvor PDF súbor v prehliadači (napr. Preview, Adobe Reader)
2. Uisti sa, že PDF okno je na popredí
3. Spusti script a zadaj:
   - Počet stránok na screenshot
   - Názov výstupného priečinka
4. Script začne po 5-sekundovom odpočítavaní
5. Screenshoty sa uložia na Desktop v zadanom priečinku

### Postup pre konverziu PNG → PDF (možnosť 2)

1. Vyber priečinok s PNG súbormi z Desktop
2. Zadaj názov výstupného PDF súboru
3. Script vytvorí PDF zo všetkých PNG súborov v priečinku

## ⚙️ Nastavenia

### Screenshot oblasť

Predvolená oblasť screenshotu je definovaná v kóde:

```python
SCREENSHOT_OBLAST = (880, 180, 840, 1150)  # (x, y, šírka, výška)
```

**Prispôsobenie oblasti:**
- Zmeň hodnoty v súbore `supertool.py` na riadku ~34
- `x, y` = pozícia ľavého horného rohu
- `šírka, výška` = rozmery screenshotu v pixeloch

### Bezpečnostné funkcie

- **FAILSAFE**: Pohyb myšou do ľavého horného rohu obrazovky zastaví script
- **Keyboard Interrupt**: `Ctrl+C` bezpečne ukončí proces

## 📁 Štruktúra výstupných súborov

```
Desktop/
└── [názov_projektu]/
    ├── strana_01.png
    ├── strana_02.png
    ├── strana_03.png
    ├── ...
    └── [názov_projektu].pdf
```

## 🔧 Riešenie problémov

### Script nefunguje správne

**Problem:** Screenshoty sú prázdne alebo zachytávajú zlú oblasť
- **Riešenie:** Uprav `SCREENSHOT_OBLAST` podľa tvojej obrazovky a PDF viewera

**Problem:** Script neklikaním prechádza na ďalšiu stránku
- **Riešenie:** Uisti sa, že PDF okno je aktívne (kliknuté) pred spustením scriptu

**Problem:** Chyba pri importovaní knižníc
- **Riešenie:** Spusti `pip3 install pyautogui Pillow`

### macOS povolenia

Ak script nefunguje, môže byť potrebné povoliť:
- **Prístupnosť (Accessibility)** pre Terminal/Python
- **Nahrávanie obrazovky (Screen Recording)**

Nastavenia → Súkromie a Bezpečnosť → Prístupnosť/Nahrávanie obrazovky

## 🛠️ Technické detaily

### Použité technológie

- **pyautogui**: Automatizácia GUI, screenshoty, simulácia klávesnice
- **Pillow (PIL)**: Spracovanie obrázkov a tvorba PDF
- **pathlib**: Moderná práca so súborovým systémom
- **time**: Časovanie a pauzy medzi operáciami

### Ako to funguje?

1. **Screenshot mód**: Script používa `pyautogui.screenshot()` na zachytenie definovanej oblasti obrazovky
2. **Navigácia**: Simuluje stláčanie šípky dolu (`down arrow`) na posun na ďalšiu stránku
3. **Konverzia**: Používa Pillow na otvorenie PNG súborov a ich zloženie do viacstránkového PDF

## 📝 Príklad použitia

```bash
# Spustenie nástroja
$ python3 supertool.py

# Výber možnosti 3 (kompletný proces)
> 3

# Zadanie parametrov
> Koľko strán chceš screenshotovať? 10
> Zadaj názov priečinka: Moja_Prezentacia

# Po dokončení
✅ PDF úspešne vytvorený!
📍 Umiestnenie: ~/Desktop/Moja_Prezentacia/Moja_Prezentacia.pdf
📊 Veľkosť súboru: 5.2 MB
📋 Počet strán: 10
```

## 🤝 Prispievanie

Príspevky sú vítané! Pre väčšie zmeny prosím najprv otvor issue na diskusiu o tom, čo by si chcel zmeniť.

## 📄 Licencia

[MIT](https://choosealicense.com/licenses/mit/)

## 👨‍💻 Autor

Adam Martiník - [@adamartinik](https://github.com/adamartinik)

## 🔮 Budúce vylepšenia

- [ ] GUI rozhranie
- [ ] Podpora Windows a Linux
- [ ] Automatická detekcia PDF viewera
- [ ] Konfiguračný súbor pre nastavenia
- [ ] Batch processing viacerých PDF súborov
- [ ] OCR (rozpoznávanie textu) na screenshotoch
- [ ] Kompresia PDF výstupu

---

⭐️ Ak ti tento nástroj pomohol, daj mu hviezdu na GitHub!