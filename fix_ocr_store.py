with open("core/ocr_store.py", "w", encoding="utf-8") as f:
    f.write("""import json
import logging
from pathlib import Path
from typing import Dict, Optional, List

logger = logging.getLogger(__name__)


class OCRStore:

    def __init__(self, cache_dir: Path):
        self.store_path = Path(cache_dir) / "ocr_data.json"
        self._data = {}
        self._load()

    def _load(self):
        if self.store_path.exists():
            try:
                with open(self.store_path, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
                logger.info(f"OCR store loaded: {len(self._data)} pages")
            except Exception as e:
                logger.warning(f"OCR store load failed: {e}")
                self._data = {}

    def _save(self):
        try:
            self.store_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.store_path, "w", encoding="utf-8") as f:
                json.dump(self._data, f, ensure_ascii=False, indent=2)
            logger.info(f"OCR store saved: {len(self._data)} pages")
        except Exception as e:
            logger.error(f"OCR store save failed: {e}")

    def add_page(self, filename, page, image_path, ocr_text):
        key = filename + "::page_" + str(page)
        self._data[key] = {
            "filename":   filename,
            "page":       page,
            "image_path": image_path,
            "ocr_text":   ocr_text,
        }
        self._save()
        logger.info(f"OCR stored: {filename} page {page} ({len(ocr_text)} chars)")

    def get_page(self, filename, page):
        key = filename + "::page_" + str(page)
        return self._data.get(key)

    def has_page(self, filename, page):
        key = filename + "::page_" + str(page)
        return key in self._data

    def get_all_filenames(self):
        return sorted(list({v["filename"] for v in self._data.values()}))

    def delete_file(self, filename):
        keys = [k for k, v in self._data.items() if v["filename"] == filename]
        for k in keys:
            del self._data[k]
        self._save()

    def count(self):
        return len(self._data)
""")
print("Done")
