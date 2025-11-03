#!/usr/bin/env python3
"""
PNG to PDF Converter Script
Spojí sériu PNG screenshotov do jedného PDF súboru
"""

import os
from pathlib import Path
from PIL import Image
import glob

def main():
    print("=== PNG to PDF Converter ===")
    print("Spojí všetky PNG súbory z priečinka do jedného PDF")
    print()
    
    try:
        # Získanie cesty k priečinku s PNG súbormi
        desktop_path = Path.home() / "Desktop"
        
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
                    zdrojovy_priecinok = priecinky[volba - 1]
                    break
                elif volba == len(priecinky) + 1:
                    cesta = input("Zadaj cestu k priečinku: ").strip()
                    zdrojovy_priecinok = Path(cesta)
                    if not zdrojovy_priecinok.exists():
                        print("Priečinok neexistuje!")
                        continue
                    break
                else:
                    print("Neplatná voľba!")
            except ValueError:
                print("Zadaj platné číslo!")
        
        # Nájdenie všetkých PNG súborov
        png_subory = sorted(zdrojovy_priecinok.glob("*.png"))
        
        if not png_subory:
            print(f"❌ V priečinku {zdrojovy_priecinok.name} sa nenašli žiadne PNG súbory!")
            return
        
        print(f"\n📁 Našiel som {len(png_subory)} PNG súborov v: {zdrojovy_priecinok.name}")
        
        # Zobrazenie súborov na kontrolu
        print("\nSúbory na spracovanie:")
        for i, subor in enumerate(png_subory[:10], 1):  # Zobraz prvých 10
            print(f"  {i}. {subor.name}")
        if len(png_subory) > 10:
            print(f"  ... a {len(png_subory) - 10} ďalších")
        
        # Názov výstupného PDF súboru
        navrhnuty_nazov = f"{zdrojovy_priecinok.name}.pdf"
        pdf_nazov = input(f"\nNázov PDF súboru [{navrhnuty_nazov}]: ").strip()
        if not pdf_nazov:
            pdf_nazov = navrhnuty_nazov
        
        if not pdf_nazov.endswith('.pdf'):
            pdf_nazov += '.pdf'
        
        # Umiestnenie výstupného PDF
        pdf_cesta = zdrojovy_priecinok / pdf_nazov
        
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
            return
        
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
                    quality=95,  # Vysoká kvalita
                    optimize=False
                )
            else:
                prvy_obrazok.save(pdf_cesta, format='PDF', quality=95)
            
            print(f"✅ PDF úspešně vytvorený!")
            print(f"📁 Umiestnenie: {pdf_cesta}")
            
            # Informácie o súbore
            velkost_mb = pdf_cesta.stat().st_size / (1024 * 1024)
            print(f"📊 Veľkosť súboru: {velkost_mb:.1f} MB")
            print(f"📋 Počet strán: {len(obrazky)}")
            
            # Ponuka na otvorenie
            odpoved = input("\nChceš otvoriť PDF súbor? (y/n): ").lower()
            if odpoved in ['y', 'yes', 'ano']:
                os.system(f'open "{pdf_cesta}"')
                
        except Exception as e:
            print(f"❌ Chyba pri vytváraní PDF: {e}")
        
        # Zatvorenie obrázkov (uvoľnenie pamäte)
        for img in obrazky:
            img.close()
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Script bol prerušený používateľom")
    except Exception as e:
        print(f"\n❌ Nastala chyba: {e}")
    
    print("\nScript ukončený.")

def install_requirements():
    """Pomocná funkcia na inštaláciu potrebných knižníc"""
    print("Inštalujem potrebné knižnice...")
    os.system("pip3 install Pillow")
    print("Knižnice nainštalované!")

if __name__ == "__main__":
    # Kontrola či je nainštalované Pillow
    try:
        from PIL import Image
        main()
    except ImportError:
        print("Knižnica Pillow nie je nainštalovaná.")
        odpoved = input("Chceš ju nainštalovať automaticky? (y/n): ")
        if odpoved.lower() in ['y', 'yes', 'ano']:
            install_requirements()
            print("Spusti script znovu po inštalácii.")
        else:
            print("Nainštaluj manuálne: pip3 install Pillow")
