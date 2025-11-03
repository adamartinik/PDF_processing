#!/usr/bin/env python3
"""
PDF Screenshot Automatizácia Script
Automaticky robí screenshoty PDF súborov na macOS
"""

import pyautogui
import os
import time
from pathlib import Path

def main():
    print("=== PDF Screenshot Automatizácia ===")
    print("Uisti sa, že:")
    print("1. Máš otvorený PDF súbor")
    print("2. PDF okno je aktívne na popredí")
    print("3. Si pripravený začať")
    print()
    
    # Predvolené súradnice pre screenshot oblasť
    SCREENSHOT_OBLAST = (850, 130, 850, 1220)  # (x, y, šírka, výška)
    print(f"Oblasť screenshotu: x={SCREENSHOT_OBLAST[0]}, y={SCREENSHOT_OBLAST[1]}")
    print(f"Veľkosť: {SCREENSHOT_OBLAST[2]}×{SCREENSHOT_OBLAST[3]} pixelov")
    print()
    
    # Bezpečnostné nastavenie - zabráni náhodnému spusteniu
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.1
    
    try:
        # Získanie počtu strán
        while True:
            try:
                pocet_stran = int(input("Koľko strán chceš screenshotovať? "))
                if pocet_stran > 0:
                    break
                else:
                    print("Počet strán musí byť väčší ako 0")
            except ValueError:
                print("Zadaj platné číslo")
        
        # Získanie názvu súboru
        nazov_suboru = input("Zadaj názov priečinka (bez .pdf): ").strip()
        if not nazov_suboru:
            nazov_suboru = "PDF_Screenshots"
        
        # Vytvorenie priečinka na Desktop
        desktop_path = Path.home() / "Desktop"
        priecinok_path = desktop_path / nazov_suboru
        
        # Vytvorenie priečinka ak neexistuje
        priecinok_path.mkdir(exist_ok=True)
        print(f"\nPriečinok vytvorený: {priecinok_path}")
        
        # Countdown pred začatím
        print("\nScript začne za:")
        for i in range(3, 0, -1):
            print(f"{i}...")
            time.sleep(1)
        print("ŠTART!")
        
        # Hlavný cyklus screenshotov
        for strana in range(1, pocet_stran + 1):
            print(f"Spracúvam stranu {strana}/{pocet_stran}")
            
            # RIEŠENIE 2: Priamy screenshot pomocou pyautogui
            screenshot_nazov = f"strana_{strana:02d}.png"
            screenshot_cesta = priecinok_path / screenshot_nazov
            
            print(f"  → Robím screenshot: {screenshot_nazov}")
            
            # Screenshot predvolenej oblasti
            try:
                x, y, sirka, vyska = SCREENSHOT_OBLAST
                screenshot = pyautogui.screenshot(region=(x, y, sirka, vyska))
                screenshot.save(str(screenshot_cesta))
                print(f"  ✓ Screenshot uložený: {screenshot_cesta}")
            except Exception as e:
                print(f"  ❌ Chyba pri screenshote: {e}")
            
            print("  → Prechádzam na ďalšiu stranu (šípka dolu)...")
            pyautogui.press('down')
            time.sleep(0.5)
            print(f"  ✓ Strana {strana} spracovaná")
        
        print(f"\n✅ Hotovo! Vytvorených {pocet_stran} screenshotov v priečinku: {nazov_suboru}")
        print("📁 Priečinok sa nachádza na Desktop")
        
        # Otvorenie priečinka v Finder
        odpoved = input("\nChceš otvoriť priečinok v Finder? (y/n): ").lower()
        if odpoved in ['y', 'yes', 'ano']:
            os.system(f'open "{priecinok_path}"')
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Script bol prerušený používateľom")
    except Exception as e:
        print(f"\n❌ Nastala chyba: {e}")
    
    print("\nScript ukončený.")

def install_requirements():
    """Pomocná funkcia na inštaláciu potrebných knižníc"""
    print("Inštalujem potrebné knižnice...")
    os.system("pip3 install pyautogui")
    print("Knižnice nainštalované!")

if __name__ == "__main__":
    # Kontrola či je nainštalované pyautogui
    try:
        import pyautogui
        main()
    except ImportError:
        print("Knižnica pyautogui nie je nainštalovaná.")
        odpoved = input("Chceš ju nainštalovať automaticky? (y/n): ")
        if odpoved.lower() in ['y', 'yes', 'ano']:
            install_requirements()
            print("Spusti script znovu po inštalácii.")
        else:
            print("Nainštaluj manuálne: pip3 install pyautogui")

"""
ZMENA SÚRADNÍC:
Ak chceš zmeniť oblasť screenshotu, uprav túto linku v main() funkcii:
SCREENSHOT_OBLAST = (850, 130, 850, 1220)  # (x, y, šírka, výška)

Aktuálne súradnice:
- Ľavý horný roh: x=850, y=130
- Pravý dolný roh: x=1700, y=1350
- Veľkosť oblasti: 850×1220 pixelov

Pre zistenie nových súradníc použi:
- DigitalColor Meter (Applications → Utilities)
- Screenshot Preview (cmd+shift+5) - zobrazí súradnice
"""
