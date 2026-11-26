import fitz
import pytesseract
from PIL import Image
from pathlib import Path
import json
import io

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

pdf_path   = Path(r'C:\Documents\documind_enterprise\data\uploads\Big Data Analytics.pdf')
images_dir = Path(r'C:\Documents\documind_enterprise\data\page_images')
cache_dir  = Path(r'C:\Documents\documind_enterprise\data\cache')
images_dir.mkdir(exist_ok=True)
cache_dir.mkdir(exist_ok=True)

ocr_data = {}
doc      = fitz.open(str(pdf_path))

for i in range(min(3, doc.page_count)):
    page_num = i + 1
    print(f'Processing page {page_num}...')

    # Screenshot
    pix      = doc[i].get_pixmap(dpi=150)
    img_path = images_dir / f'BigDataAnalytics_page_{page_num}.png'
    pix.save(str(img_path))

    # OCR
    img      = Image.open(str(img_path))
    ocr_text = pytesseract.image_to_string(img, config='--oem 3 --psm 6')
    print(f'OCR text length: {len(ocr_text)}')
    print(f'First 200 chars: {ocr_text[:200]}')

    # Save to store
    key = f'Big Data Analytics.pdf::page_{page_num}'
    ocr_data[key] = {
        'filename':   'Big Data Analytics.pdf',
        'page':       page_num,
        'image_path': str(img_path),
        'ocr_text':   ocr_text.strip(),
    }

doc.close()

# Save json
out = cache_dir / 'ocr_data.json'
with open(str(out), 'w', encoding='utf-8') as f:
    json.dump(ocr_data, f, ensure_ascii=False, indent=2)

print(f'Saved {len(ocr_data)} pages to {out}')
print(f'File exists: {out.exists()}')
print(f'File size: {out.stat().st_size} bytes')
