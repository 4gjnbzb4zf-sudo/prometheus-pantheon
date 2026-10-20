"""Wrap site/ember-generator.html (artifact source) into a full index.html for GitHub Pages.

Usage: python3 site/build_index.py
"""
from pathlib import Path

ROOT = Path(__file__).parent.parent
BASE = "https://4gjnbzb4zf-sudo.github.io/prometheus-pantheon"

src = (ROOT / "site" / "ember-generator.html").read_text()
style_end = src.index("</style>") + len("</style>")
head, body = src[:style_end], src[style_end:]

meta = f"""<meta name="description" content="Draw a real-world ember idea, do it well, post the proof with #PrometheusEmber. The flame cannot be stolen. It can only be given.">
<meta property="og:title" content="Prometheus Ember Generator">
<meta property="og:description" content="Find a real good deed to do today, with AI help or by hand, and post the action shot with #PrometheusEmber.">
<meta property="og:image" content="{BASE}/media/banners/og-link-preview-1200x630.jpg">
<meta property="og:url" content="{BASE}/">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="media/avatar/avatar-monogram-512.png">
<style>html,body{{margin:0}} img{{max-width:100%}} [hidden]{{display:none!important}}</style>"""

(ROOT / "index.html").write_text(f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{head}
{meta}
</head>
<body>{body}
</body>
</html>
""")
print("wrote index.html")
