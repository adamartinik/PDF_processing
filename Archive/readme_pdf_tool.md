# PDF Screenshot a Konverzia Nástroj

Automatizovaný nástroj na vytváranie screenshotov z PDF súborov a ich konverziu do jedného PDF dokumentu na macOS.

## 🎯 Čo nástroj robí

- **Automatické screenshoty** PDF stránok v preddefinovanej oblasti
- **Konverzia PNG → PDF** - spojenie obrázkov do jedného PDF súboru  
- **Kompletný workflow** - screenshoty + automatická konverzia + cleanup
- **Organizované ukladanie** - automatické vytvorenie priečinkov na Desktop

## 🚀 Rýchly štart

1. **Spusti nástroj:**
   ```bash
   python3 pdf_complete_tool.py
   ```

2. **Vyber možnosť:**
   - `1` - Len screenshoty PDF súboru
   - `2` - Len konverzia existujúcich PNG do PDF
   - `3` - **Kompletný proces** (odporúčané)
   - `4` - Ukončiť

3. **Pre kompletný proces:**
   - Otvor PDF súbor a nechaj ho aktívny
   - Vyber možnosť `3`
   - Zadaj počet strán na screenshotovanie
   - Zadaj názov priečinka
   - Počkaj na dokončenie screenshotov
   - Potvrd názov výsledného PDF súboru
   - Rozhodní o otvorení PDF a zmazaní PNG súborov

## 📐 Nastavenie súradníc screenshotu

**Aktuálne nastavené súradnice:**
- **Ľavý horný roh**: x=850, y=130
- **Pravý dolný roh**: x=1700, y=1350  
- **Veľkosť oblasti**: 850×1220 pixelov

### Zmena súradníc

Pre zmenu oblasti screenshotu uprav **riadok 52** v súbore `pdf_complete_tool.py`:

```python
SCREENSHOT_OBLAST = (850, 130, 850, 1220)  # (x, y, šírka, výška)
```

**Výpočet parametrov:**
- `x` = ľavý okraj (px)
- `y` = horný okraj (px) 
- `šírka` = pravý_okraj - ľavý_okraj
- `výška` = dolný_okraj - horný_okraj

**Zistenie súradníc:**
- Použij aplikáciu **DigitalColor Meter** (Applications → Utilities)
- Alebo **CMD+Shift+4** → zobrazí súradnice pri výbere oblasti

## 📁 Štruktúra výstupu

```
Desktop/
├── Nazov_Projektu/           # Priečinok so screenshotmi
│   ├── strana_01.png
│   ├── strana_02.png
│   ├── strana_03.png
│   └── Nazov_Projektu.pdf    # Finálny PDF súbor
```

## ⚙️ Nastavenie macOS povolení

Po prvom spustení nástroja macOS vyžaduje povolenia:

1. **Systémové nastavenia** → **Súkromie a bezpečnosť** → **Prístupnosť**
   - Pridaj **Terminal** (alebo tvoju Python IDE)

2. **Systémové nastavenia** → **Súkromie a bezpečnosť** → **Nahrávanie obrazovky**
   - Pridaj **Terminal** (alebo tvoju Python IDE)

## 🛠 Inštalácia na novom Mac

### 1. Inštalácia Homebrew
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Pridaj Homebrew do PATH (spusti po inštalácii)
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

### 2. Inštalácia Python 3
```bash
# Cez Homebrew (odporúčané)
brew install python

# Alebo stiahni z python.org a nainštaluj manuálne
# https://www.python.org/downloads/
```

### 3. Inštalácia potrebných Python knižníc
```bash
# Všetky potrebné knižnice naraz
pip3 install pyautogui Pillow

# Alebo jednotlivo
pip3 install pyautogui    # Pre automatizáciu klávesnice/myši
pip3 install Pillow      # Pre prácu s obrázkami a PDF
```

### 4. Alternatívne cez requirements.txt

Vytvor súbor `requirements.txt`:
```
pyautogui>=0.9.54
Pillow>=10.0.0
```

Nainštaluj:
```bash
pip3 install -r requirements.txt
```

### 5. Overenie inštalácie
```bash
# Test Python verzie
python3 --version

# Test knižníc
python3 -c "import pyautogui; print('pyautogui OK')"
python3 -c "from PIL import Image; print('Pillow OK')"
```

## 🔧 Riešenie problémov

### Chyba: "pyautogui nie je nainštalované"
```bash
pip3 install --upgrade pyautogui
```

### Chyba: "PIL nie je nainštalované"  
```bash
pip3 install --upgrade Pillow
```

### Chyba: "Prístup odmietnutý"
- Skontroluj povolenia v Systémových nastaveniach (viz sekcia vyššie)
- Reštartuj Terminal po pridaní povolení

### Python not found
```bash
# Ak máš len python (nie python3)
python --version

# Vytvor alias v ~/.zprofile
echo 'alias python3=python' >> ~/.zprofile
source ~/.zprofile
```

## 💡 Tipy na používanie

- **PDF okno musí byť aktívne** pred spustením screenshotov
- **Súradnice sú fixné** - script vždy screenshotuje tú istú oblasť
- **Failsafe**: Pohni myšou do ľavého horného rohu pre okamžité zastavenie
- **Ctrl+C** kedykoľvek prerušuje script
- **Kompletný proces** je najefektívnejší - urobí všetko naraz

## 📝 Licencia

Free to use. Vytvorené pre automatizáciu práce s PDF dokumentmi.

---

**Autor**: Custom PDF Tool  
**Verzia**: 1.0  
**Posledná aktualizácia**: 2025
