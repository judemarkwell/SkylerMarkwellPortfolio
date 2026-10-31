"""Build web photos and the classroom loop from source-materials/photos/ (not committed).

Writes public/photos/<key>-<w>.jpg (+ <key>.mp4 for video) and src/data/photos.json (sizes only).
Blur boxes hide student names before anything is resized. Usage: python3 scripts/build_photos.py
"""
import json, subprocess
from pathlib import Path
from PIL import Image, ImageOps, ImageFilter, ImageDraw
import pillow_heif
pillow_heif.register_heif_opener()

ROOT = Path(__file__).resolve().parent.parent
SRC, OUT = ROOT / "source-materials" / "photos", ROOT / "public" / "photos"
WIDTHS = (800, 1600)

def box(im, f):
    w, h = im.size
    return (int(w * f[0]), int(h * f[1]), int(w * f[2]), int(h * f[3]))

def main():
    spec = json.loads((ROOT / "scripts" / "photos.json").read_text())
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for key, cfg in spec.items():
        if key.startswith("_"):
            continue
        src = SRC / cfg["src"]
        if cfg.get("video"):
            mp4, poster = OUT / f"{key}.mp4", OUT / f"{key}-poster.jpg"
            if cfg.get("keepAudio"):
                # A talking video: full length, sound kept, no crop.
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-vf", "scale=1280:-2", "-c:v", "libx264", "-preset", "veryfast",
                                "-crf", "27", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", str(mp4)], check=True)
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "2", "-i", str(src), "-frames:v", "1", "-vf", "scale=1280:-2", "-q:v", "4", str(poster)], check=True)
            else:
                # Only the first `seconds` are kept and the left edge is cropped: later frames show student name cards, and the left wall has photos.
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-t", str(cfg.get("seconds", 5)), "-an", "-vf", "crop=iw*0.9:ih:iw*0.1:0,scale=720:-2,fps=30",
                                "-c:v", "libx264", "-preset", "veryfast", "-crf", "28", "-pix_fmt", "yuv420p",
                                "-movflags", "+faststart", str(mp4)], check=True)
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "1.5", "-i", str(src), "-frames:v", "1",
                                "-vf", "crop=iw*0.9:ih:iw*0.1:0,scale=720:-2", "-q:v", "4", str(poster)], check=True)
            pw, ph = Image.open(poster).size
            manifest[key] = {"video": f"photos/{key}.mp4", "poster": f"photos/{key}-poster.jpg", "width": pw, "height": ph}
            print(key, "video", mp4.stat().st_size // 1024, "KB")
            continue
        im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
        # Student faces and names: blurred on the full-size original, before any crop or resize.
        if cfg.get("blurFaces") or cfg.get("blurRects"):
            W, H = im.size
            mask = Image.new("L", im.size, 0); dr = ImageDraw.Draw(mask)
            for x, y, w, h in cfg.get("blurFaces", []):
                cx, cy, rx, ry = (x + w / 2) * W, (y + h / 2) * H, w * W * 0.8, h * H * 0.9
                dr.ellipse((cx - rx, cy - ry * 1.05, cx + rx, cy + ry), fill=255)
            for x, y, w, h in cfg.get("blurRects", []):
                dr.rounded_rectangle((x * W, y * H, (x + w) * W, (y + h) * H), radius=min(w * W, h * H) * 0.2, fill=255)
            mask = mask.filter(ImageFilter.GaussianBlur(radius=max(W, H) / 400))
            heavy = im.resize((max(1, W // 48), max(1, H // 48)), Image.BILINEAR).resize(im.size, Image.BILINEAR).filter(ImageFilter.GaussianBlur(radius=max(W, H) / 300))
            im = Image.composite(heavy, im, mask)
        for b in cfg.get("blur", []):
            region = box(im, b)
            patch = im.crop(region).filter(ImageFilter.GaussianBlur(radius=max(im.size) / 260))
            im.paste(patch, region)
        if "crop" in cfg:
            im = im.crop(box(im, cfg["crop"]))
        if cfg.get("blurEllipses"):
            w, h = im.size
            mask = Image.new("L", im.size, 0); dr = ImageDraw.Draw(mask)
            for cx, cy, rx, ry in cfg["blurEllipses"]:
                dr.ellipse((int((cx - rx) * w), int((cy - ry) * h), int((cx + rx) * w), int((cy + ry) * h)), fill=255)
            mask = mask.filter(ImageFilter.GaussianBlur(radius=w / 60))
            im = Image.composite(im.filter(ImageFilter.GaussianBlur(radius=w / 320)), im, mask)
        srcs = []
        for w in WIDTHS:
            c = im.copy(); c.thumbnail((w, w * 2), Image.LANCZOS)
            c.save(OUT / f"{key}-{w}.jpg", quality=78, optimize=True, progressive=True)
            srcs.append({"src": f"photos/{key}-{w}.jpg", "width": c.width, "height": c.height})
        manifest[key] = {"srcset": srcs, "width": srcs[-1]["width"], "height": srcs[-1]["height"]}
        print(key, srcs[-1]["width"], "x", srcs[-1]["height"])
    (ROOT / "src" / "data" / "photos.json").write_text(json.dumps(manifest, indent=2))

if __name__ == "__main__":
    main()
