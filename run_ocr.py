import fitz
import pytesseract
from PIL import Image
from pathlib import Path
import json
import sys

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

upload_dir = Path(r"C:\Documents\documind_enterprise\data\uploads")
images_dir = Path(r"C:\Documents\documind_enterprise\data\page_images")
cache_dir  = Path(r"C:\Documents\documind_enterprise\data\cache")

images_dir.mkdir(exist_ok=True)
cache_dir.mkdir(exist_ok=True)

ocr_data   = {}
store_path = cache_dir / "ocr_data.json"

if store_path.exists():
    with open(store_path, "r", encoding="utf-8") as f:
        ocr_data = json.load(f)
    print(f"Loaded existing OCR data: {len(ocr_data)} pages")

pdfs = list(upload_dir.glob("*.pdf"))
print(f"Found {len(pdfs)} PDFs")

for pdf_path in pdfs:
    pdf_path  = pdf_path.resolve()
    filename  = pdf_path.name
    safe_stem = "".join(c if c.isalnum() or c in "-_" else "_" for c in pdf_path.stem)
    print(f"\nProcessing: {filename}")

    try:
        doc     = fitz.open(str(pdf_path))
        n_pages = doc.page_count
        print(f"  Pages: {n_pages}")

        for i in range(n_pages):
            page_num = i + 1
            key      = filename + "::page_" + str(page_num)
            img_path = images_dir / (safe_stem + "_page_" + str(page_num) + ".png")

            if not img_path.exists():
                pix = doc[i].get_pixmap(dpi=150)
                pix.save(str(img_path))
                print(f"  Screenshot: page {page_num}")

            if key in ocr_data:
                print(f"  OCR already done: page {page_num}")
                continue

            try:
                img      = Image.open(str(img_path))
                ocr_text = pytesseract.image_to_string(img, config="--oem 3 --psm 6")
                ocr_text = ocr_text.strip()
                if len(ocr_text) < 5:
                    ocr_text = "[No readable text on this page]"
            except Exception as e:
                print(f"  OCR error page {page_num}: {e}")
                ocr_text = "[OCR failed]"

            ocr_data[key] = {
                "filename":   filename,
                "page":       page_num,
                "image_path": str(img_path),
                "ocr_text":   ocr_text,
            }
            print(f"  OCR done: page {page_num} ({len(ocr_text)} chars)")

        doc.close()

    except Exception as e:
        print(f"  Error: {e}")

with open(store_path, "w", encoding="utf-8") as f:
    json.dump(ocr_data, f, ensure_ascii=False, indent=2)

print(f"\nSaved {len(ocr_data)} pages to {store_path}")
print(f"File size: {store_path.stat().st_size} bytes")
print("Images saved:", len(list(images_dir.glob("*.png"))))
