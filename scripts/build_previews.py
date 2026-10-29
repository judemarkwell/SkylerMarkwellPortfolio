"""Render preview images for every portfolio piece.

Reads source documents from source-materials/ (not committed), converts Office files
to PDF with LibreOffice, renders the listed pages, and writes:
  public/previews/<slug>-<n>.jpg   (not committed until Skyler approves publishing)
  src/data/previews.json           (image sizes only; committed)
Also resizes source-materials/image.jpg to public/previews/skyler.jpg.

Usage: python3 scripts/build_previews.py
"""
import json, subprocess, tempfile, shutil
from pathlib import Path
import pypdfium2 as pdfium
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC, OUT = ROOT / "source-materials", ROOT / "public" / "previews"
MANIFEST = ROOT / "src" / "data" / "previews.json"
MAX = 1100

def to_pdf(src: Path, tmp: Path) -> Path:
    if src.suffix.lower() == ".pdf":
        return src
    pdf = tmp / (src.stem + ".pdf")
    if not pdf.exists():
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(tmp), str(src)],
                       check=True, capture_output=True, timeout=300)
    return pdf

def main():
    spec = json.loads((ROOT / "scripts" / "previews.json").read_text())
    OUT.mkdir(parents=True, exist_ok=True); MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    manifest = {}
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        for slug, cfg in spec.items():
            if slug.startswith("_"):
                continue
            manifest[slug] = []
            for n, (name, page) in enumerate(cfg["pages"]):
                doc = pdfium.PdfDocument(str(to_pdf(SRC / name, tmp)))
                im = doc[page].render(scale=2.4).to_pil().convert("RGB")
                if "crop" in cfg:
                    l, tp, r, b = cfg["crop"]; w, h = im.size
                    im = im.crop((int(w * l), int(h * tp), int(w * r), int(h * b)))
                im.thumbnail((MAX, MAX), Image.LANCZOS)
                im.save(OUT / f"{slug}-{n}.jpg", quality=74, optimize=True, progressive=True)
                manifest[slug].append({"src": f"previews/{slug}-{n}.jpg", "width": im.width, "height": im.height})
            print(slug, len(manifest[slug]))
    head = SRC / "image.jpg"
    if head.exists():
        im = Image.open(head).convert("RGB"); im.thumbnail((900, 900), Image.LANCZOS)
        im.save(OUT / "skyler.jpg", quality=80, optimize=True, progressive=True)
        manifest["_headshot"] = [{"src": "previews/skyler.jpg", "width": im.width, "height": im.height}]
    MANIFEST.write_text(json.dumps(manifest, indent=2))

if __name__ == "__main__":
    main()
