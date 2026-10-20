"""Generate Prometheus social media assets from the source banner.

Usage: python3 media/build.py
"""
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter

ROOT = Path(__file__).parent
SRC = ROOT / "source" / "prometheus-pantheon-original.jpg"
BG = (2, 2, 2)  # sampled from the source background

# Content box of the wordmark + "PANTHEON" in the source (x0, y0, x1, y1), with breathing room
WORDMARK_BOX = (30, 55, 985, 318)
# The "P" glyph with its vine, used as the round avatar monogram
MONOGRAM_BOX = (30, 76, 154, 216)


def feathered(img, radius):
    """Return img with alpha fading to 0 at the edges, so it melts into the BG."""
    w, h = img.size
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rectangle((radius, radius, w - radius, h - radius), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius / 2))
    out = img.convert("RGBA")
    out.putalpha(mask)
    return out


def scaled(img, width=None, height=None):
    w, h = img.size
    if width is None:
        width = round(w * height / h)
    if height is None:
        height = round(h * width / w)
    out = img.resize((width, height), Image.LANCZOS)
    # Light sharpen to compensate for upscaling the low-res source
    return out.filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))


def glow(size, center, radius, strength=38):
    """Soft green radial glow, to give large canvases some depth."""
    w, h = size
    layer = Image.new("RGB", size, BG)
    dot = Image.new("L", size, 0)
    cx, cy = center
    ImageDraw.Draw(dot).ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=strength)
    dot = dot.filter(ImageFilter.GaussianBlur(radius / 2))
    green = Image.new("RGB", size, (40, 160, 70))
    layer.paste(green, (0, 0), dot)
    return layer


def canvas(size, art, center=None, glow_radius=None, feather=None):
    w, h = size
    center = center or (w // 2, h // 2)
    base = glow(size, center, glow_radius) if glow_radius else Image.new("RGB", size, BG)
    # Art is light-on-black, so a screen blend merges it into the glow without a visible box
    layer = Image.new("RGB", size, (0, 0, 0))
    piece = feathered(art, feather or max(8, art.width // 60))
    layer.paste(piece, (center[0] - art.width // 2, center[1] - art.height // 2), piece)
    return ImageChops.screen(base, layer)


def circle_preview(img):
    """PNG with a transparent outside, to check how the avatar looks once cropped round."""
    s = img.width
    big = Image.new("L", (s * 4, s * 4), 0)
    ImageDraw.Draw(big).ellipse((0, 0, s * 4 - 1, s * 4 - 1), fill=255)
    out = img.convert("RGBA")
    out.putalpha(big.resize((s, s), Image.LANCZOS))
    return out


def save(img, name):
    path = ROOT / name
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix == ".jpg":
        img.convert("RGB").save(path, quality=95, subsampling=0)
    else:
        img.save(path, optimize=True)
    print(f"{name:45s} {img.width}x{img.height}")


def main():
    src = Image.open(SRC).convert("RGB")
    wordmark = src.crop(WORDMARK_BOX)
    monogram = src.crop(MONOGRAM_BOX)

    # --- Avatars (square, safe inside a circle) -----------------------------
    # Monogram "P": readable even at the tiny sizes TG/X/Discord render avatars.
    s = 640
    mono = canvas((s, s), scaled(monogram, height=round(s * 0.66)), glow_radius=s // 2, feather=22)
    save(mono, "avatar/avatar-monogram-640.png")
    save(mono.resize((512, 512), Image.LANCZOS), "avatar/avatar-monogram-512.png")
    save(circle_preview(mono), "avatar/preview-round-monogram.png")

    # Full wordmark: fits the inscribed circle (width ~ 82% of diameter).
    full = canvas((s, s), scaled(wordmark, width=round(s * 0.84)), glow_radius=s // 2)
    save(full, "avatar/avatar-wordmark-640.png")
    save(circle_preview(full), "avatar/preview-round-wordmark.png")

    # --- Banners --------------------------------------------------------------
    # X / Twitter header 1500x500. Kept away from the bottom-left (profile pic)
    # and the top/bottom strips that get cropped on mobile.
    x = canvas((1500, 500), scaled(wordmark, width=1060), center=(790, 235), glow_radius=420)
    save(x, "banners/x-header-1500x500.jpg")

    # Telegram / website link preview (Open Graph) 1200x630
    save(canvas((1200, 630), scaled(wordmark, width=980), glow_radius=420), "banners/og-link-preview-1200x630.jpg")

    # Discord server banner 960x540
    save(canvas((960, 540), scaled(wordmark, width=800), glow_radius=360), "banners/discord-banner-960x540.jpg")

    # LinkedIn page cover 1584x396
    save(canvas((1584, 396), scaled(wordmark, height=330), glow_radius=380), "banners/linkedin-cover-1584x396.jpg")

    # YouTube channel art 2560x1440 (art stays in the 1546x423 all-device safe zone)
    save(canvas((2560, 1440), scaled(wordmark, width=1500), glow_radius=900), "banners/youtube-2560x1440.jpg")

    # --- Posts ----------------------------------------------------------------
    save(canvas((1080, 1080), scaled(wordmark, width=940), glow_radius=520), "posts/square-post-1080.jpg")
    save(canvas((1080, 1920), scaled(wordmark, width=980), glow_radius=600), "posts/story-1080x1920.jpg")


if __name__ == "__main__":
    main()
