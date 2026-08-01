#!/usr/bin/env python3
"""
Renders shaped Arabic text to a transparent PNG using Pango + HarfBuzz
(via PyGObject + Cairo). This handles Arabic contextual letter shaping
and any calligraphic ligatures defined in the font's GSUB table correctly
- something plain PIL text drawing cannot do.

Usage:
    python3 render_arabic_text.py \
        --text "سورة الفاتحة" \
        --font "Your Font Name Bold" \
        --size 140 \
        --color "#000000" \
        --out fatiha_text.png

Then composite the resulting transparent PNG onto a generated thumbnail
with PIL (see overlay_batch.py).
"""
import argparse
import cairo
import gi

gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")
from gi.repository import Pango, PangoCairo


def render_text_png(text, font_desc, out_path, font_size=140,
                     color=(0, 0, 0), padding=20):
    """
    Renders `text` shaped via Pango/HarfBuzz to a tightly-cropped
    transparent PNG at `out_path`.

    font_desc: a Pango font description string, e.g. "Amiri Bold 140"
               (family name + optional weight + size). If you pass
               font_size separately, size in font_desc is overridden.
    color: RGB tuple, 0-255 each.
    padding: transparent margin around the text, in px.
    """
    # First pass: measure text at a throwaway surface to get exact ink extents
    tmp_surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 10, 10)
    tmp_ctx = cairo.Context(tmp_surface)
    layout = PangoCairo.create_layout(tmp_ctx)

    font = Pango.FontDescription(font_desc)
    font.set_size(font_size * Pango.SCALE)
    layout.set_font_description(font)

    # Right-to-left base direction + Arabic script itemization is handled
    # automatically by Pango once the text contains Arabic codepoints,
    # but we set it explicitly to be safe.
    layout.set_auto_dir(True)
    layout.set_text(text, -1)

    ink_rect, logical_rect = layout.get_pixel_extents()
    width = ink_rect.width + padding * 2
    height = ink_rect.height + padding * 2

    # Second pass: real surface sized to fit, transparent background
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)
    ctx.set_source_rgba(0, 0, 0, 0)
    ctx.paint()

    layout2 = PangoCairo.create_layout(ctx)
    layout2.set_font_description(font)
    layout2.set_auto_dir(True)
    layout2.set_text(text, -1)

    r, g, b = [c / 255 for c in color]
    ctx.set_source_rgba(r, g, b, 1.0)

    # Offset so the ink extents (not the logical box, which includes
    # font-metric whitespace) sit flush against our padding.
    ctx.translate(padding - ink_rect.x, padding - ink_rect.y)
    PangoCairo.show_layout(ctx, layout2)

    surface.write_to_png(out_path)
    return width, height


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--text", required=True, help="Arabic text to render")
    p.add_argument("--font", required=True,
                    help='Pango font description, e.g. "Amiri Bold"')
    p.add_argument("--size", type=int, default=140)
    p.add_argument("--color", default="#000000")
    p.add_argument("--out", required=True)
    args = p.parse_args()

    hex_color = args.color.lstrip("#")
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    w, h = render_text_png(args.text, args.font, args.out,
                            font_size=args.size, color=rgb)
    print(f"Wrote {args.out} ({w}x{h}px)")
