"""Print the /resume/ page to public/files/skyler-markwell-resume.pdf (no phone number; print CSS hides the site chrome).
Usage: python3 scripts/build_resume_pdf.py http://localhost:4321/SkylerMarkwellPortfolio/resume/
"""
import sys, json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
out = ROOT / "public" / "files" / "skyler-markwell-resume.pdf"
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    pg.goto(sys.argv[1], wait_until="networkidle"); pg.emulate_media(media="print")
    pg.pdf(path=str(out), format="Letter", margin={"top": "0.6in", "bottom": "0.6in", "left": "0.7in", "right": "0.7in"}, print_background=False)
    b.close()
m = ROOT / "src" / "data" / "downloads.json"
d = json.loads(m.read_text()); d["_resume"] = {"href": "files/skyler-markwell-resume.pdf", "bytes": out.stat().st_size}
m.write_text(json.dumps(d, indent=2)); print(out, out.stat().st_size)
