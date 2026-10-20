"""Green flame mark in the Prometheus logo style: a flame drawn in '#' glyphs with a phosphor glow.

Usage: python3 media/flame.py  (writes into media/ember/)
"""
import math
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).parent
BG = (2, 2, 2)
GREEN = (150, 255, 170)
FONT = "/System/Library/Fonts/Menlo.ttc"


def flame_polygon(cx, top, h, w, lean=0.0):
    """Teardrop flame outline: pointed, slightly curled tip, round base."""
    left, right = [], []
    steps = 120
    for i in range(steps + 1):
        t = i / steps  # 0 = tip, 1 = base
        y = top + t * h
        # width profile: grows from the tip, rounds off at the base
        if t < 0.72:
            half = w / 2 * math.sin(t / 0.72 * math.pi / 2) ** 1.6
        else:
            k = (t - 0.72) / 0.28
            half = w / 2 * math.sqrt(max(0.0, 1 - k * k))
        sway = lean * w * (1 - t) ** 2 * math.sin(t * math.pi * 1.5)
        left.append((cx + sway - half, y))
        right.append((cx + sway + half, y))
    return left + right[::-1]


def hash_fill(size, mask, cell, font):
    """Grid of '#' glyphs clipped to the mask."""
    layer = Image.new("L", size, 0)
    d = ImageDraw.Draw(layer)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], int(cell * 0.62)):
            if mask.getpixel((min(x + cell // 3, size[0] - 1), min(y + cell // 2, size[1] - 1))) > 128:
                d.text((x, y), "#", fill=200, font=font)
    return ImageChops.multiply(layer, mask)


def flame_mark(s):
    """Square flame mark of side s, light-on-black."""
    size = (s, s)
    # Main tongue plus two side tongues, so it reads as fire rather than a drop
    outer = Image.new("L", size, 0)
    d = ImageDraw.Draw(outer)
    d.polygon(flame_polygon(s * 0.5, s * 0.08, s * 0.8, s * 0.5, lean=0.45), fill=255)
    d.polygon(flame_polygon(s * 0.33, s * 0.34, s * 0.54, s * 0.3, lean=-0.9), fill=255)
    d.polygon(flame_polygon(s * 0.67, s * 0.28, s * 0.6, s * 0.3, lean=0.9), fill=255)
    inner = Image.new("L", size, 0)
    ImageDraw.Draw(inner).polygon(flame_polygon(s * 0.5, s * 0.46, s * 0.38, s * 0.2, lean=-0.6), fill=255)

    stroke = max(2, s // 120)
    edge = ImageChops.subtract(outer, outer.filter(ImageFilter.MinFilter(stroke * 2 + 1)))
    inner_edge = ImageChops.subtract(inner, inner.filter(ImageFilter.MinFilter(stroke * 2 + 1)))
    body = ImageChops.subtract(outer, inner.filter(ImageFilter.MaxFilter(stroke * 4 + 1)))
    glyphs = hash_fill(size, body, max(10, s // 28), ImageFont.truetype(FONT, max(10, s // 28)))

    light = ImageChops.lighter(ImageChops.lighter(edge, inner_edge), glyphs)
    core = inner.filter(ImageFilter.GaussianBlur(s / 40)).point(lambda v: v * 0.55)
    light = ImageChops.lighter(light, core)

    glow = light.filter(ImageFilter.GaussianBlur(s / 50)).point(lambda v: min(255, v * 2))
    halo = outer.filter(ImageFilter.GaussianBlur(s / 9)).point(lambda v: v * 0.22)
    alpha = ImageChops.lighter(ImageChops.lighter(light, glow), halo)

    out = Image.new("RGB", size, BG)
    out.paste(Image.new("RGB", size, GREEN), (0, 0), alpha)
    return out


def main():
    out = ROOT / "ember"
    out.mkdir(exist_ok=True)
    mark = flame_mark(1024)
    mark.save(out / "flame-mark-1024.png", optimize=True)
    mark.resize((640, 640), Image.LANCZOS).save(out / "flame-avatar-640.png", optimize=True)

    # Banner variant: two flames flank PANTHEON like temple torches
    src = Image.open(ROOT / "source" / "prometheus-pantheon-original.jpg").convert("RGB")
    torch = flame_mark(84)
    banner = src.copy()
    for x in (262, 680):  # either side of the word PANTHEON
        banner = ImageChops.screen(banner, _placed(banner.size, torch, (x, 226)))
    banner.save(out / "banner-with-flames.jpg", quality=95)
    print("wrote", ", ".join(p.name for p in sorted(out.iterdir())))


def _placed(size, img, pos):
    layer = Image.new("RGB", size, (0, 0, 0))
    layer.paste(img, pos)
    return layer


if __name__ == "__main__":
    main()
