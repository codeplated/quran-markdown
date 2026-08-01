#!/usr/bin/env python3
"""
Composites Arabic surah-name text onto each generated thumbnail.

Legibility strategy (works regardless of whether the underlying image is
dark or bright):
    1. Sample the average brightness of the base image directly under
       where the text will sit, and pick a light or dark fill color
       accordingly.
    2. Add a stroke (outline) in the opposite tone around every glyph,
       via morphological dilation of the alpha mask.
    3. Add a soft, blurred drop shadow beneath everything for extra
       separation, especially on busy/textured backgrounds where a
       flat stroke alone can still blend in.

This uses Pango/HarfBuzz (via render_arabic_text.py) for correct Arabic
shaping, and pure PIL for the compositing - no extra dependencies beyond
what's already installed.

Usage:
    python3 overlay_batch.py
"""
import csv
import sys
from pathlib import Path

from PIL import Image, ImageFilter

sys.path.insert(0, str(Path(__file__).parent))
from render_arabic_text import render_text_png

# ---- Config -------------------------------------------------------------
INPUT_DIR = Path("thumbnailsPreProcess")        # raw ComfyUI output
OUTPUT_DIR = Path("thumbnails")  # final composited images
CSV_PATH = Path("surah_themes.csv")

FONT = "NotoSansArabic-Bold"   # <-- replace with your identified calligraphy font's family name

TEXT_MAX_WIDTH_FRAC = 0.82   # text block max width, as a fraction of image width
TEXT_MAX_HEIGHT_FRAC = 0.20  # text block max height, as a fraction of image height
BOTTOM_MARGIN_FRAC = 0.07    # gap between text baseline area and image bottom edge

STROKE_PX = 6
SHADOW_OFFSET = (0, 8)
SHADOW_BLUR = 10
SHADOW_OPACITY = 130          # 0-255

BRIGHTNESS_THRESHOLD = 140    # above this (0-255 scale) counts as a "bright" region
DARK_FILL = (255, 255, 255)
DARK_STROKE = (20, 20, 20)
LIGHT_FILL = (20, 20, 20)
LIGHT_STROKE = (255, 255, 255)

TMP_MASK_PATH = Path("/tmp/_overlay_mask_tmp.png")
# --------------------------------------------------------------------------


def load_rows():
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def sample_brightness(base_rgb_img, box):
    region = base_rgb_img.convert("L").crop(box)
    hist = region.histogram()
    total_pixels = sum(hist)
    if total_pixels == 0:
        return 128
    weighted_sum = sum(i * count for i, count in enumerate(hist))
    return weighted_sum / total_pixels


def build_colored_layer(alpha_mask, rgb_color):
    layer = Image.new("RGBA", alpha_mask.size, rgb_color + (255,))
    layer.putalpha(alpha_mask)
    return layer


def process_one(image_path, arabic_text, out_path):
    base = Image.open(image_path).convert("RGBA")
    W, H = base.size

    # 1. Render the master glyph shape at a large, fixed font size for
    #    good raster quality, using plain white fill - only the alpha
    #    channel (the glyph shapes) is used from here on; final color
    #    is decided per-image below.
    render_text_png(arabic_text, FONT, str(TMP_MASK_PATH),
                     font_size=220, color=(255, 255, 255))
    mask_img = Image.open(TMP_MASK_PATH).convert("RGBA")
    mw, mh = mask_img.size

    # 2. Scale to fit within the target text-box bounds, preserving
    #    aspect ratio, so short and long surah names both read at a
    #    consistent visual weight relative to the thumbnail.
    max_w = W * TEXT_MAX_WIDTH_FRAC
    max_h = H * TEXT_MAX_HEIGHT_FRAC
    scale = min(max_w / mw, max_h / mh)
    new_w, new_h = max(1, int(mw * scale)), max(1, int(mh * scale))
    mask_img = mask_img.resize((new_w, new_h), Image.LANCZOS)
    alpha = mask_img.split()[-1]

    # 3. Position: bottom-centered.
    x = (W - new_w) // 2
    y = int(H * (1 - BOTTOM_MARGIN_FRAC) - new_h)

    # 4. Sample brightness of the base image under the text box and
    #    pick fill/stroke colors accordingly.
    box = (max(0, x), max(0, y), min(W, x + new_w), min(H, y + new_h))
    brightness = sample_brightness(base, box)
    if brightness > BRIGHTNESS_THRESHOLD:
        fill_color, stroke_color = LIGHT_FILL, LIGHT_STROKE
    else:
        fill_color, stroke_color = DARK_FILL, DARK_STROKE

    # 5. Build stroke layer via morphological dilation of the alpha mask
    #    (PIL's MaxFilter on a single-channel image IS dilation).
    dilated_alpha = alpha.filter(ImageFilter.MaxFilter(STROKE_PX * 2 + 1))
    stroke_layer = build_colored_layer(dilated_alpha, stroke_color)
    fill_layer = build_colored_layer(alpha, fill_color)

    # 6. Build soft drop shadow from a blurred copy of the alpha mask.
    shadow_alpha = alpha.filter(ImageFilter.GaussianBlur(SHADOW_BLUR))
    shadow_alpha = shadow_alpha.point(lambda p: int(p * SHADOW_OPACITY / 255))
    shadow_layer = Image.new("RGBA", (new_w, new_h), (0, 0, 0, 255))
    shadow_layer.putalpha(shadow_alpha)

    # 7. Composite: shadow (offset) -> stroke -> fill, on top of base.
    canvas = base.copy()
    sx, sy = x + SHADOW_OFFSET[0], y + SHADOW_OFFSET[1]
    canvas.alpha_composite(shadow_layer, (sx, sy))
    canvas.alpha_composite(stroke_layer, (x, y))
    canvas.alpha_composite(fill_layer, (x, y))

    canvas.convert("RGB").save(out_path)


def main():
    rows = load_rows()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for row in rows:
        number = row["number"].zfill(3)
        name = row["transliteration"]
        arabic_full = f"سورة {row['arabic_name']}"

        matches = list(INPUT_DIR.glob(f"surah_{number}_*"))
        if not matches:
            print(f"[{number}] MISSING generated image for {name}, skipping")
            continue

        src = matches[0]
        #out_path = OUTPUT_DIR / f"surah_{number}_{name}.png"
        out_path = OUTPUT_DIR / f"surah_{number}.png"
        process_one(src, arabic_full, out_path)
        print(f"[{number}] {name} -> {out_path.name}")

    print("Overlay pass complete.")


if __name__ == "__main__":
    main()
