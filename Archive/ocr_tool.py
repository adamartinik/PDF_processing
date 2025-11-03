#!/usr/bin/env python3
"""
OCR Text Recognition Tool
Rozpoznáva text z obrázkov (PNG, JPG, PDF) pomocou Tesseract OCR
"""

import os
import sys
from pathlib import Path
import glob
from datetime import datetime

def check_tesseract():
    """Kontrola či je Tesseract nainštalovaný"""
    import subprocess
    try:
        result = subprocess.run(['tesseract', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            print(f"✅ {version}")
            return True
        else:
            return False
    except FileNotFoundError:
        return False

def get_available_languages():
    """Získanie dostupných jazykov pre OCR"""
    import subprocess
    try:
        result = subprocess.run(['tesseract', '--list-langs'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            langs = result.stdout.strip().split('\n')[1:]  # Preskočiť prvý riadok
            return [lang.strip() for lang in langs if lang.strip()]
        else:
            return ['eng']  # Default fallback
    except Exception:
        return ['eng']

def preprocess_image(image_path, enhance=True):
    """Predspracovanie obrázka pre lepšie OCR výsledky"""
    import cv2
    import numpy as np
    
    # Načítanie obrázka
    img = cv2.imread(str(image_path))
    if img is None:
        raise ValueError(f"Nepodarilo sa načítať obrázok: {image_path}")
    
    if enhance:
        # Konverzia na grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Zväčšenie rozlíšenia (2x)
        height, width = gray.shape
        gray = cv2.resize(gray, (width * 2, height * 2), interpolation=cv2.INTER_CUBIC)
        
        # Odstránenie šumu pomocou Gaussian blur
        gray = cv2.GaussianBlur(gray, (1, 1), 0)
        
        # Zlepšenie kontrastu pomocou adaptive threshold
        gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY, 11, 2)
        
        return gray
    else:
        return img

def ocr_single_image(image_path, language='eng', enhance=True, config=''):
    """OCR rozpoznávanie jedného obrázka"""
    import pytesseract
    from PIL import Image
    import cv2
    
    print(f"  → Spracúvam: {image_path.name}")
    
    try:
        # Predspracovanie obrázka
        if enhance:
            processed_img = preprocess_image(image_path, enhance=True)
            # Konverzia OpenCV → PIL
            pil_img = Image.fromarray(processed_img)
        else:
            pil_img = Image.open(image_path)
        
        # OCR konfigurácia
        if not config:
            config = '--oem 3 --psm 6'  # Default config
        
        # Rozpoznávanie textu
        text = pytesseract.image_to_string(pil_img, lang=language, config=config)
        
        # Získanie confidence score
        data = pytesseract.image_to_data(pil_img, lang=language, config=config, output_type=pytesseract.Output.DICT)
        confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        
        return text.strip(), avg_confidence
        
    except Exception as e:
        print(f"  ❌ Chyba pri OCR: {e}")
        return "", 0

def ocr_multiple_images(image_paths, language='eng', enhance=True):
    """OCR rozpoznávanie viacerých obrázkov"""
    results = []
    total_confidence = 0
    
    print(f"\n🔍 Spracúvam {len(image_paths)} obrázkov...")
    print(f"📝 Jazyk: {language}")
    print(f"🎯 Vylepšenie: {'Zapnuté' if enhance else 'Vypnuté'}")
    print("-" * 50)
    
    for i, image_path in enumerate(image_paths, 1):
        print(f"[{i}/{len(image_paths)}]", end=" ")
        
        text, confidence = ocr_single_image(image_path, language, enhance)
        
        if text:
            results.append({
                'file': image_path.name,
                'text': text,
                'confidence': confidence
            })
            total_confidence += confidence
            print(f"  ✓ Rozpoznaných {len(text)} znakov (spoľahlivosť: {confidence:.1f}%)")
        else:
            print(f"  ⚠️  Žiadny text nenájdený")
    
    avg_confidence = total_confidence / len(results) if results else 0
    
    print("-" * 50)
    print(f"📊 Celkový výsledok: {len(results)}/{len(image_paths)} úspešne spracovaných")
    print(f"📈 Priemerná spoľahlivosť: {avg_confidence:.1f}%")
    
    return results

def save_results(results, output_path, format_type='txt'):
    """Uloženie výsledkov OCR"""
    
    if format_type == 'txt':
        # Jeden súbor so všetkým textom
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"OCR Výsledky - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            
            for result in results:
                f.write(f"Súbor: {result['file']}\n")
                f.write(f"Spoľahlivosť: {result['confidence']:.1f}%\n")
                f.write("-" * 30 + "\n")
                f.write(result['text'])
                f.write("\n\n" + "=" * 60 + "\n\n")
    
    elif format_type == 'separate':
        # Separátne súbory pre každý obrázok
        output_dir = output_path.parent / f"{output_path.stem}_separate"
        output_dir.mkdir(exist_ok=True)
        
        for result in results:
            file_name = Path(result['file']).stem + '.txt'
            file_path = output_dir / file_name
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"Zdrojový súbor: {result['file']}\n")
                f.write(f"Spoľahlivosť: {result['confidence']:.1f}%\n")
                f.write(f"Čas: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("-" * 40 + "\n\n")
                f.write(result['text'])
        
        print(f"📁 Separátne súbory uložené v: {output_dir}")

def main():
    print("=" * 60)
    print("           OCR TEXT RECOGNITION TOOL")
    print("=" * 60)
    
    # Kontrola Tesseract inštalácie
    print("🔧 Kontrola systému...")
    if not check_tesseract():
        print("❌ Tesseract OCR nie je nainštalovaný!")
        print("\nInštalácia:")
        print("brew install tesseract tesseract-lang")
        print("pip3 install pytesseract opencv-python")
        return
    
    # Získanie dostupných jazykov
    available_langs = get_available_languages()
    print(f"🌍 Dostupné jazyky: {', '.join(available_langs)}")
    print()
    
    try:
        # Výber zdrojového priečinka
        desktop_path = Path.home() / "Desktop"
        
        print("📁 Dostupné priečinky na Desktop:")
        folders = [f for f in desktop_path.iterdir() if f.is_dir() and not f.name.startswith('.')]
        
        for i, folder in enumerate(folders, 1):
            # Počet obrázkov v priečinku
            img_count = len(list(folder.glob("*.png"))) + len(list(folder.glob("*.jpg"))) + len(list(folder.glob("*.jpeg")))
            print(f"{i}. {folder.name} ({img_count} obrázkov)")
        
        print(f"{len(folders) + 1}. Zadať vlastnú cestu")
        
        # Výber priečinka
        while True:
            try:
                choice = int(input("\nVyber priečinok: "))
                if 1 <= choice <= len(folders):
                    source_folder = folders[choice - 1]
                    break
                elif choice == len(folders) + 1:
                    path = input("Zadaj cestu: ").strip()
                    source_folder = Path(path)
                    if not source_folder.exists():
                        print("Priečinok neexistuje!")
                        continue
                    break
                else:
                    print("Neplatná voľba!")
            except ValueError:
                print("Zadaj platné číslo!")
        
        # Nájdenie obrázkov
        image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.PNG', '*.JPG', '*.JPEG']
        image_paths = []
        
        for ext in image_extensions:
            image_paths.extend(source_folder.glob(ext))
        
        image_paths = sorted(image_paths)
        
        if not image_paths:
            print(f"❌ V priečinku {source_folder.name} sa nenašli žiadne obrázky!")
            return
        
        print(f"\n📷 Našiel som {len(image_paths)} obrázkov")
        
        # Výber jazyka
        print(f"\nDostupné jazyky: {', '.join(available_langs)}")
        language = input("Vyber jazyk [eng]: ").strip().lower()
        if not language or language not in available_langs:
            language = 'eng'
        
        # Nastavenia spracovania
        enhance_choice = input("Zapnúť vylepšenie obrázkov? (y/n) [y]: ").strip().lower()
        enhance = enhance_choice not in ['n', 'no', 'nie']
        
        # Spustenie OCR
        results = ocr_multiple_images(image_paths, language, enhance)
        
        if not results:
            print("❌ Nepodarilo sa rozpoznať žiadny text!")
            return
        
        # Uloženie výsledkov
        output_name = f"OCR_{source_folder.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        output_path = source_folder / output_name
        
        print(f"\n💾 Ukladám výsledky...")
        
        # Typ výstupu
        print("Možnosti uloženia:")
        print("1. Jeden súbor so všetkým textom")
        print("2. Separátne súbory pre každý obrázok")
        
        format_choice = input("Vyber možnosť [1]: ").strip()
        format_type = 'separate' if format_choice == '2' else 'txt'
        
        save_results(results, output_path, format_type)
        
        print(f"✅ Výsledky uložené: {output_path}")
        
        # Ponuka na otvorenie
        open_choice = input("\nChceš otvoriť výsledky? (y/n): ").lower()
        if open_choice in ['y', 'yes', 'ano']:
            os.system(f'open "{output_path}"')
        
    except KeyboardInterrupt:
        print("\n⚠️  OCR proces bol prerušený")
    except Exception as e:
        print(f"❌ Chyba: {e}")

def install_requirements():
    """Inštalácia potrebných knižníc"""
    print("Inštalujem Python knižnice...")
    os.system("pip3 install pytesseract opencv-python numpy pillow")
    print("\nPre Tesseract OCR spusti:")
    print("brew install tesseract tesseract-lang")

if __name__ == "__main__":
    # Kontrola závislostí
    missing_libs = []
    
    try:
        import pytesseract
    except ImportError:
        missing_libs.append("pytesseract")
    
    try:
        import cv2
    except ImportError:
        missing_libs.append("opencv-python")
    
    try:
        import numpy
    except ImportError:
        missing_libs.append("numpy")
    
    if missing_libs:
        print(f"Chýbajúce knižnice: {', '.join(missing_libs)}")
        choice = input("Chceš ich nainštalovať? (y/n): ")
        if choice.lower() in ['y', 'yes', 'ano']:
            install_requirements()
            print("Spusti script znovu po inštalácii.")
        else:
            print(f"Nainštaluj manuálne: pip3 install {' '.join(missing_libs)}")
    else:
        main()
