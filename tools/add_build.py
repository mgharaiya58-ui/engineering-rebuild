"""Scaffold a new build folder for this portfolio.

What it does:
  1. Creates a folder like 03-2-to-1-multiplexer/
  2. Copies your photos and screenshots into it with standard names,
     rotated correctly and resized so the repo stays small
  3. Writes a README.md template that already shows those images
  4. Adds a row to the progress table in the main README.md

Setup (once):
  pip install pillow

Usage (run from anywhere; the script finds the repo itself):
  python tools/add_build.py 03 "2-to-1 multiplexer" \
      --concepts "Selection logic, AND as a door" \
      --photos IMG_1601.jpg IMG_1602.jpg \
      --tinkercad mux_sim.png \
      --schematic mux_schematic.png

Then fill in the TODO parts of the new README and upload the folder to GitHub.
"""
import argparse
import datetime
import re
import sys
from pathlib import Path

try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit("Pillow is missing. Install it with:  pip install pillow")

try:  # optional: lets the script read iPhone .heic photos
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError:
    pass

REPO = Path(__file__).resolve().parent.parent
MAIN_README = REPO / "README.md"
MARKER = "<!-- progress-end -->"
MAX_SIDE = 1600  # pixels; keeps photos sharp but small


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def save_image(src, dst):
    src = Path(src).expanduser()
    if not src.exists():
        sys.exit(f"File not found: {src}")
    try:
        img = Image.open(src)
    except Exception:
        sys.exit(f"Can't open {src}. If it's a .heic photo, run: pip install pillow-heif")
    img = ImageOps.exif_transpose(img)  # fixes sideways phone photos
    img.thumbnail((MAX_SIDE, MAX_SIDE))
    if dst.suffix == ".jpg":
        img.convert("RGB").save(dst, quality=85, optimize=True)
    else:
        img.save(dst, optimize=True)
    print(f"  saved {dst.relative_to(REPO)}")


def readme_template(num, title, sim_imgs, photo_imgs):
    lines = [f"# {num} — {title}", "",
             "TODO: one or two sentences on what this circuit does and where it is used in real chips.", "",
             "## Parts", "", "| Part | Qty |", "|------|-----|", "| TODO | |", "",
             "## Wiring", "", "| Signal | Chip pin |", "|--------|----------|", "| TODO | |", "",
             "## Simulation", ""]
    if sim_imgs:
        for name, alt in sim_imgs:
            lines += [f"![{alt}]({name})", ""]
    else:
        lines += ["TODO: describe the simulation, or re-run the script with --tinkercad.", ""]
    lines += ["## Real build", ""]
    if photo_imgs:
        for name in photo_imgs:
            lines += [f"![Breadboard build]({name})", ""]
    else:
        lines += ["TODO: add photos by re-running the script with --photos.", ""]
    lines += ["## Results", "",
              "| Inputs | Expected | Measured |", "|:------:|:--------:|:--------:|", "| TODO | | |", "",
              "## Bugs I hit and how I found them", "",
              "1. TODO: what went wrong, how you found it, how you fixed it.", "",
              "## What I learned", "", "- TODO", ""]
    return "\n".join(lines)


def add_progress_row(num, title, folder, concepts, date):
    text = MAIN_README.read_text(encoding="utf-8")
    if f"| {num} |" in text:
        print(f"  main README already has a row for {num}; left it unchanged")
        return
    if MARKER not in text:
        print(f"  couldn't find {MARKER} in README.md; add the progress row by hand")
        return
    row = f"| {num} | [{title}]({folder}/) | {concepts} | ✅ | ✅ | {date} |\n"
    MAIN_README.write_text(text.replace(MARKER, row + MARKER), encoding="utf-8")
    print("  added a row to the progress table in README.md")


def main():
    p = argparse.ArgumentParser(description="Scaffold a new portfolio build folder.")
    p.add_argument("number", help="build number, e.g. 03")
    p.add_argument("title", help='build title, e.g. "2-to-1 multiplexer"')
    p.add_argument("--concepts", default="TODO", help="short list of concepts for the progress table")
    p.add_argument("--photos", nargs="*", default=[], help="photos of the real build")
    p.add_argument("--tinkercad", help="screenshot of the Tinkercad breadboard view")
    p.add_argument("--schematic", help="screenshot of the Tinkercad schematic view")
    p.add_argument("--date", default=datetime.date.today().isoformat())
    a = p.parse_args()

    num = a.number.zfill(2)
    folder = f"{num}-{slugify(a.title)}"
    out = REPO / folder
    out.mkdir(exist_ok=True)
    print(f"Build folder: {folder}/")

    sim_imgs = []
    if a.tinkercad:
        save_image(a.tinkercad, out / "tinkercad.png"); sim_imgs.append(("tinkercad.png", "Tinkercad simulation"))
    if a.schematic:
        save_image(a.schematic, out / "schematic.png"); sim_imgs.append(("schematic.png", "Schematic"))
    photo_imgs = []
    for i, ph in enumerate(a.photos, 1):
        name = "breadboard.jpg" if i == 1 else f"breadboard-{i}.jpg"
        save_image(ph, out / name); photo_imgs.append(name)

    readme = out / "README.md"
    if readme.exists():
        print("  README.md already exists; not overwritten (your edits are safe)")
    else:
        readme.write_text(readme_template(num, a.title, sim_imgs, photo_imgs), encoding="utf-8")
        print("  wrote README.md template")

    add_progress_row(num, a.title, folder, a.concepts, a.date)
    print("\nNext: fill in the TODOs in the new README, then upload the folder and README.md to GitHub.")


if __name__ == "__main__":
    main()
