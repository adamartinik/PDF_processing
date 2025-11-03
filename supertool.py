#!/usr/bin/env python3
"""
Kompletný PDF Screenshot Nástroj
1. Automatické screenshoty PDF súborov
2. Konverzia PNG obrázkov do PDF
3. Kombinácia oboch procesov
"""

import os
import time
from pathlib import Path
import glob

def menu():
    """Hlavné menu s možnosťami"""
    print("=" * 50)
    print("       KOMPLETNÝ PDF SCREENSHOT NÁSTROJ")
    print("=" * 50)
    print()
    print("Vyber možnosť:")
    print("1. 📸 Len screenshoty PDF súboru")
    print("2. 📄 Len konverzia PNG → PDF")
    print("3. 🚀 Screenshoty + konverzia do PDF (kompletný proces)")
    print("4. ❌ Ukončiť")
    print()
    
    while True:
        try:
            volba = int(input("Zadaj možnosť (1-4): "))
            if 1 <= volba <= 4:
                return volba
            else:
                print("Zadaj číslo 1-4!")
        except ValueError:
            print("Zadaj platné číslo!")

def screenshot_pdf():
    """Funkcia na screenshoty PDF súboru"""
    print("\n" + "="*30)
    print("📸 SCREENSHOTY PDF SÚBORU")
    print("="*30)
    print("Uisti sa, že:")
    print("1. Máš otvorený PDF súbor")
    print("2. PDF okno je aktívne na popredí")
    print("3. Si pripravený začať")
    print()
    
    # Predvolené súradnice pre screenshot oblasť
    SCREENSHOT_OBLAST = (880, 180, 840, 1150)  # (x, y, šírka, výška)
    print(f"Oblasť screenshotu: x={SCREENSHOT_OBLAST[0]}, y={SCREENSHOT_OBLAST[1]}")
    print(f"Veľkosť: {SCREENSHOT_OBLAST[2]}×{SCREENSHOT_OBLAST[3]} pixelov")
    print()
    
    # Bezpečnostné nastavenie
    import pyautogui
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.1
    
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
    for i in range(5, 0, -1):
        print(f"{i}...")
        time.sleep(1)
    print("ŠTART!")
    
    # Hlavný cyklus screenshotov
    for strana in range(1, pocet_stran + 1):
        print(f"Spracúvam stranu {strana}/{pocet_stran}")
        
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
    
    return priecinok_path, nazov_suboru

def png_to_pdf(priecinok_path=None, navrhnuty_nazov=None):
    """Funkcia na konverziu PNG do PDF"""
    from PIL import Image
    
    print("\n" + "="*30)
    print("📄 KONVERZIA PNG → PDF")
    print("="*30)
    
    desktop_path = Path.home() / "Desktop"
    
    # Ak nie je zadaný priečinok, nechaj používateľa vybrať
    if priecinok_path is None:
        # Zobrazenie dostupných priečinkov na Desktop
        priecinky = [f for f in desktop_path.iterdir() if f.is_dir() and not f.name.startswith('.')]
        
        print("Dostupné priečinky na Desktop:")
        for i, priecinok in enumerate(priecinky, 1):
            # Počet PNG súborov v priečinku
            png_count = len(list(priecinok.glob("*.png")))
            print(f"{i}. {priecinok.name} ({png_count} PNG súborov)")
        
        print(f"{len(priecinky) + 1}. Zadať vlastnú cestu")
        print()
        
        # Výber priečinka
        while True:
            try:
                volba = int(input("Vyber priečinok (číslo): "))
                if 1 <= volba <= len(priecinky):
                    priecinok_path = priecinky[volba - 1]
                    break
                elif volba == len(priecinky) + 1:
                    cesta = input("Zadaj cestu k priečinku: ").strip()
                    priecinok_path = Path(cesta)
                    if not priecinok_path.exists():
                        print("Priečinok neexistuje!")
                        continue
                    break
                else:
                    print("Neplatná voľba!")
            except ValueError:
                print("Zadaj platné číslo!")
    
    # Nájdenie všetkých PNG súborov
    png_subory = sorted(priecinok_path.glob("*.png"))
    
    if not png_subory:
        print(f"❌ V priečinku {priecinok_path.name} sa nenašli žiadne PNG súbory!")
        return None
    
    print(f"\n📁 Našiel som {len(png_subory)} PNG súborov v: {priecinok_path.name}")
    
    # Zobrazenie súborov na kontrolu
    print("\nSúbory na spracovanie:")
    for i, subor in enumerate(png_subory[:5], 1):  # Zobraz prvých 5
        print(f"  {i}. {subor.name}")
    if len(png_subory) > 5:
        print(f"  ... a {len(png_subory) - 5} ďalších")
    
    # Názov výstupného PDF súboru
    if navrhnuty_nazov is None:
        navrhnuty_nazov = f"{priecinok_path.name}.pdf"
    else:
        navrhnuty_nazov = f"{navrhnuty_nazov}.pdf"
        
    pdf_nazov = input(f"\nNázov PDF súboru [{navrhnuty_nazov}]: ").strip()
    if not pdf_nazov:
        pdf_nazov = navrhnuty_nazov
    
    if not pdf_nazov.endswith('.pdf'):
        pdf_nazov += '.pdf'
    
    # Umiestnenie výstupného PDF
    pdf_cesta = priecinok_path / pdf_nazov
    
    print(f"\n🔄 Spracúvam {len(png_subory)} obrázkov...")
    
    # Načítanie a konverzia obrázkov
    obrazky = []
    
    for i, png_subor in enumerate(png_subory, 1):
        print(f"  → Načítavam {png_subor.name} ({i}/{len(png_subory)})")
        
        try:
            # Otvorenie obrázka
            img = Image.open(png_subor)
            
            # Konverzia na RGB (potrebné pre PDF)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            obrazky.append(img)
            
        except Exception as e:
            print(f"  ❌ Chyba pri načítavaní {png_subor.name}: {e}")
    
    if not obrazky:
        print("❌ Nepodarilo sa načítať žiadne obrázky!")
        return None
    
    # Vytvorenie PDF súboru
    print(f"\n📄 Vytváram PDF súbor: {pdf_nazov}")
    
    try:
        # Prvý obrázok ako základ PDF
        prvy_obrazok = obrazky[0]
        
        # Ostatné obrázky ako ďalšie strany
        ostatne_obrazky = obrazky[1:] if len(obrazky) > 1 else None
        
        # Uloženie ako PDF
        if ostatne_obrazky:
            prvy_obrazok.save(
                pdf_cesta,
                format='PDF',
                append_images=ostatne_obrazky,
                save_all=True,
                quality=95,
                optimize=False
            )
        else:
            prvy_obrazok.save(pdf_cesta, format='PDF', quality=95)
        
        print(f"✅ PDF úspešne vytvorený!")
        print(f"📁 Umiestnenie: {pdf_cesta}")
        
        # Informácie o súbore
        velkost_mb = pdf_cesta.stat().st_size / (1024 * 1024)
        print(f"📊 Veľkosť súboru: {velkost_mb:.1f} MB")
        print(f"📋 Počet strán: {len(obrazky)}")
        
        # Zatvorenie obrázkov (uvoľnenie pamäte)
        for img in obrazky:
            img.close()
            
        return pdf_cesta
        
    except Exception as e:
        print(f"❌ Chyba pri vytváraní PDF: {e}")
        return None

def kompletny_proces():
    """Kompletný proces: screenshoty + konverzia do PDF"""
    print("\n" + "="*40)
    print("🚀 KOMPLETNÝ PROCES: SCREENSHOTY + PDF")
    print("="*40)
    
    # 1. Krok: Screenshoty
    try:
        priecinok_path, nazov_suboru = screenshot_pdf()
        
        # Krátka pauza medzi procesmi
        print("\n" + "-"*30)
        input("Stlač Enter pre pokračovanie na konverziu do PDF...")
        
        # 2. Krok: Konverzia do PDF
        pdf_cesta = png_to_pdf(priecinok_path, nazov_suboru)
        
        if pdf_cesta:
            print(f"\n🎉 KOMPLETNÝ PROCES DOKONČENÝ!")
            print(f"📁 Screenshoty: {priecinok_path}")
            print(f"📄 PDF súbor: {pdf_cesta}")
            
            # Ponuky po dokončení
            print("\nÚkony po dokončení:")
            
            # Otvorenie PDF
            odpoved = input("Chceš otvoriť PDF súbor? (y/n): ").lower()
            if odpoved in ['y', 'yes', 'ano']:
                os.system(f'open "{pdf_cesta}"')
            
            # Zmazanie PNG súborov
            odpoved = input("Chceš zmazať PNG súbory (zostane len PDF)? (y/n): ").lower()
            if odpoved in ['y', 'yes', 'ano']:
                png_subory = list(priecinok_path.glob("*.png"))
                for png_subor in png_subory:
                    png_subor.unlink()
                print(f"✅ Zmazaných {len(png_subory)} PNG súborov")
            
        else:
            print("❌ Konverzia do PDF zlyhala!")
            
    except KeyboardInterrupt:
        print("\n⚠️  Proces bol prerušený používateľom")
    except Exception as e:
        print(f"❌ Chyba počas procesu: {e}")

def main():
    """Hlavná funkcia programu"""
    try:
        while True:
            volba = menu()
            
            if volba == 1:
                # Len screenshoty
                priecinok_path, nazov_suboru = screenshot_pdf()
                odpoved = input("\nChceš otvoriť priečinok so screenshotmi? (y/n): ").lower()
                if odpoved in ['y', 'yes', 'ano']:
                    os.system(f'open "{priecinok_path}"')
                    
            elif volba == 2:
                # Len konverzia PNG → PDF
                pdf_cesta = png_to_pdf()
                if pdf_cesta:
                    odpoved = input("\nChceš otvoriť PDF súbor? (y/n): ").lower()
                    if odpoved in ['y', 'yes', 'ano']:
                        os.system(f'open "{pdf_cesta}"')
                        
            elif volba == 3:
                # Kompletný proces
                kompletny_proces()
                
            elif volba == 4:
                # Ukončenie
                print("\n👋 Ďakujem za použitie nástroja!")
                break
            
            # Možnosť opakovania
            print("\n" + "-"*50)
            odpoved = input("Chceš spustiť ďalšiu operáciu? (y/n): ").lower()
            if odpoved not in ['y', 'yes', 'ano']:
                print("\n👋 Ďakujem za použitie nástroja!")
                break
                
    except KeyboardInterrupt:
        print("\n\n⚠️  Program bol prerušený používateľom")
    except Exception as e:
        print(f"\n❌ Nastala chyba: {e}")
    
    print("Program ukončený.")

def install_requirements():
    """Inštalácia potrebných knižníc"""
    print("Inštalujem potrebné knižnice...")
    os.system("pip3 install pyautogui Pillow")
    print("Knižnice nainštalované!")

if __name__ == "__main__":
    # Kontrola závislostí
    missing_libs = []
    
    try:
        import pyautogui
    except ImportError:
        missing_libs.append("pyautogui")
    
    try:
        from PIL import Image
    except ImportError:
        missing_libs.append("Pillow")
    
    if missing_libs:
        print(f"Chýbajúce knižnice: {', '.join(missing_libs)}")
        odpoved = input("Chceš ich nainštalovať automaticky? (y/n): ")
        if odpoved.lower() in ['y', 'yes', 'ano']:
            install_requirements()
            print("Spusti script znovu po inštalácii.")
        else:
            print(f"Nainštaluj manuálne: pip3 install {' '.join(missing_libs)}")
    else:
        main()
