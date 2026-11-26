import fitz
from pathlib import Path

upload_dir = Path(r'C:\Documents\documind_enterprise\data\uploads')
images_dir = Path(r'C:\Documents\documind_enterprise\data\page_images')
images_dir.mkdir(exist_ok=True)

for pdf_path in upload_dir.glob('*.pdf'):
    pdf_path  = pdf_path.resolve()
    safe_stem = ''.join(c if c.isalnum() or c in '-_' else '_' for c in pdf_path.stem)
    doc       = fitz.open(str(pdf_path))
    n         = doc.page_count
    for i in range(n):
        out = images_dir / f'{safe_stem}_page_{i+1}.png'
        if not out.exists():
            doc[i].get_pixmap(dpi=150).save(str(out))
    doc.close()
    print(f'Done: {pdf_path.name} -> {n} pages -> stem: {safe_stem}')

total = len(list(images_dir.glob('*.png')))
print(f'Total images saved: {total}')
