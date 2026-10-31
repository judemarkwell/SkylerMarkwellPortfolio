"""Build the downloadable files.

- public/files/<slug>.pdf: every source document for a piece (as listed in scripts/previews.json),
  converted to PDF with images capped at 150 dpi and merged in order.
- public/files/credential-history.pdf: Kentucky credential history, as issued.
- public/files/asbury-transcript.pdf: the Asbury transcript with the student ID and date of birth
  removed. Pages are re-rendered as images so the removed text is really gone, not just covered.
- src/data/downloads.json: href and size for each file (committed).

Sources live in source-materials/ (not committed). Usage: python3 scripts/build_downloads.py
"""
import json, subprocess, tempfile, shutil
from pathlib import Path
import pdfplumber
import pypdfium2 as pdfium
from PIL import Image, ImageDraw
from pypdf import PdfWriter, PdfReader

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "source-materials"
OUT = ROOT / "public" / "files"
MANIFEST = ROOT / "src" / "data" / "downloads.json"

FILTERS = {".docx": "writer_pdf_Export", ".pptx": "impress_pdf_Export", ".xlsx": "calc_pdf_Export"}
OPTS = '{"ReduceImageResolution":{"type":"boolean","value":"true"},"MaxImageResolution":{"type":"long","value":"150"},"Quality":{"type":"long","value":"80"}}'


def to_pdf(src: Path, tmp: Path) -> Path:
    if src.suffix.lower() == ".pdf":
        return src
    out = tmp / (src.stem + ".pdf")
    if not out.exists():
        subprocess.run(["soffice", "--headless", "--convert-to", f"pdf:{FILTERS[src.suffix.lower()]}:{OPTS}",
                        "--outdir", str(tmp), str(src)], check=True, capture_output=True, timeout=600)
    return out


def redact_transcript(src: Path, dst: Path) -> None:
    """Black out the student ID and date of birth, then flatten each page to an image."""
    pages = []
    doc = pdfium.PdfDocument(str(src))
    with pdfplumber.open(str(src)) as pl:
        for i, pg in enumerate(pl.pages):
            scale = 200 / 72
            im = doc[i].render(scale=scale).to_pil().convert("RGB")
            dr = ImageDraw.Draw(im)
            words = pg.extract_words()
            for j, w in enumerate(words):
                if w["text"] in ("ID:", "DOB:"):
                    # the label and every word after it on the same line
                    line = [x for x in words[j:] if abs(x["top"] - w["top"]) < 3]
                    x0, x1 = w["x0"], max(x["x1"] for x in line[:4])
                    dr.rectangle((x0 * scale - 4, w["top"] * scale - 4, x1 * scale + 4, w["bottom"] * scale + 4), fill="black")
            pages.append(im)
    pages[0].save(dst, "PDF", resolution=200, save_all=True, append_images=pages[1:])


def main():
    spec = json.loads((ROOT / "scripts" / "previews.json").read_text())
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {}
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        for slug, cfg in spec.items():
            if slug.startswith("_"):
                continue
            sources = list(dict.fromkeys(name for name, _ in cfg["pages"]))
            writer = PdfWriter()
            for name in sources:
                for page in PdfReader(str(to_pdf(SRC / name, tmp))).pages:
                    writer.add_page(page)
            writer.compress_identical_objects(remove_duplicates=True, remove_unreferenced=True)
            dst = OUT / f"{slug}.pdf"
            with open(dst, "wb") as fh:
                writer.write(fh)
            manifest[slug] = {"href": f"files/{slug}.pdf", "bytes": dst.stat().st_size}
            print(slug, round(dst.stat().st_size / 1e6, 2), "MB")

    prof = SRC / "professional"
    shutil.copy(prof / "credential-history.pdf", OUT / "credential-history.pdf")
    manifest["_credential-history"] = {"href": "files/credential-history.pdf", "bytes": (OUT / "credential-history.pdf").stat().st_size}
    redact_transcript(prof / "asbury-transcript.pdf", OUT / "asbury-transcript.pdf")
    manifest["_asbury-transcript"] = {"href": "files/asbury-transcript.pdf", "bytes": (OUT / "asbury-transcript.pdf").stat().st_size}
    resume = OUT / "skyler-markwell-resume.pdf"
    if resume.exists():
        manifest["_resume"] = {"href": "files/skyler-markwell-resume.pdf", "bytes": resume.stat().st_size}
    MANIFEST.write_text(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
