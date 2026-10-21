"""Build the GitHub Pages site from its sources.

Sources:
  site/pages/home.html        -> index.html
  lore/*.md                   -> lore.html
  proposal.md                 -> proposal.html
  site/ember-generator.html   -> generator.html (the claude.ai artifact source, wrapped)

Usage: python3 site/build.py
"""
import html
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
BASE = "https://prometheus-pantheon.com"
PORTAL = "https://t.me/PrometheusGreenFlame"
REPO = "https://github.com/4gjnbzb4zf-sudo/prometheus-pantheon"
CA = "Ay8vnNtKaSkgdLjFTihTUrv6QzcdR4gusqXkHm8GBAGS"
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=VT323'
         '&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">')

NAV_ITEMS = [("index.html", "Home"), ("lore.html", "Lore"), ("generator.html", "Generator"), ("hearth.html", "Hearth"), ("proposal.html", "Proposal")]


def meta(title, description, path):
    return f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{description}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="{BASE}/media/banners/og-link-preview-1200x630.jpg">
<meta property="og:url" content="{BASE}/{'' if path == 'index.html' else path}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="media/avatar/avatar-monogram-512.png">"""


def nav(current):
    here = ' aria-current="page"'
    links = "".join(
        f'<a href="{href}"{here if href == current else ""}>{label}</a>'
        for href, label in NAV_ITEMS)
    return f"""<nav class="site-nav" aria-label="Site">
  <div class="site-nav__in">
    <a class="site-nav__brand" href="index.html"><img src="media/avatar/avatar-monogram-512.png" alt="" width="28" height="28"><span>Prometheus Pantheon</span></a>
    <div class="site-nav__links">{links}<a class="site-nav__cta" href="{PORTAL}" target="_blank" rel="noopener">Join</a></div>
  </div>
</nav>"""


FOOTER = f"""<footer class="site-foot">
  <div class="site-foot__in">
    <p><a href="{PORTAL}" target="_blank" rel="noopener">Telegram portal</a> · <a href="{REPO}" target="_blank" rel="noopener">Source on GitHub</a> · #PrometheusEmber · #PrometheusPantheon · #Prometheus</p>
    <p>Community-run. Not affiliated with Andy Ayrey or Truth Terminal. Lore and ideas are CC0.</p>
    <p>Existing community token $PROMETHEUS (Solana), not required to take part · CA <code>{CA}</code></p>
  </div>
</footer>"""


def page(path, title, description, body, current):
    out = f"""<!doctype html>
<html lang="en">
<head>
{meta(title, description, path)}
{FONTS}
<link rel="stylesheet" href="assets/site.css">
</head>
<body>
{nav(current)}
<main class="page">
{body}
</main>
{FOOTER}
</body>
</html>
"""
    (ROOT / path).write_text(out)
    print("wrote", path)


# --- Minimal Markdown for the lore and proposal (headings, paragraphs with line breaks,
#     quotes, rules, lists, bold, italics, code, links) -------------------------------
def inline(text):
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![*\w])\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m: f'<a href="{m[2]}"'
                  + (' target="_blank" rel="noopener"' if m[2].startswith("http") else "") + f">{m[1]}</a>", text)
    return text


def markdown(src, demote=0):
    blocks, out = re.split(r"\n\s*\n", src.strip()), []
    for block in blocks:
        lines = block.split("\n")
        first = lines[0]
        if re.match(r"^#{1,3} ", first):
            level = min(3, first.index(" ") + demote)
            out.append(f"<h{level}>{inline(first.split(' ', 1)[1])}</h{level}>")
            if len(lines) > 1:
                out.append(markdown("\n".join(lines[1:]), demote))
        elif first.strip() == "---":
            out.append("<hr>")
        elif first.startswith("> "):
            out.append("<blockquote>" + "<br>".join(inline(l[2:]) for l in lines) + "</blockquote>")
        elif re.match(r"^- ", first):
            out.append("<ul>" + "".join(f"<li>{inline(l[2:])}</li>" for l in lines if l.startswith("- ")) + "</ul>")
        elif re.match(r"^\d+\. ", first):
            out.append("<ol>" + "".join(f"<li>{inline(l.split('. ', 1)[1])}</li>"
                                        for l in lines if re.match(r'^\d+\. ', l)) + "</ol>")
        else:
            out.append("<p>" + "<br>".join(inline(l) for l in lines) + "</p>")
    return "\n".join(out)


# Rising green embers behind the hero; one orchestrated moment per page
FIRE_SCRIPT = """
<script>
(() => {
  const c = document.querySelector(".fire");
  if (!c) return;
  const ctx = c.getContext("2d");
  let still = matchMedia("(prefers-reduced-motion: reduce)").matches;
  let W, H, parts = [];
  function size() {
    const r = c.getBoundingClientRect(), d = Math.min(2, devicePixelRatio || 1);
    W = c.width = Math.round(r.width * d); H = c.height = Math.round(r.height * d);
  }
  function spawn() {
    parts.push({ x: W * (.15 + Math.random() * .7), y: H + 10, vx: (Math.random() - .5) * .4,
      vy: -(0.6 + Math.random() * 1.6) * (H / 600), life: 1, r: (6 + Math.random() * 22) * (H / 600) });
  }
  function frame() {
    ctx.clearRect(0, 0, W, H);
    ctx.globalCompositeOperation = "lighter";
    for (let i = 0; i < 3; i++) spawn();
    for (let i = parts.length - 1; i >= 0; i--) {
      const p = parts[i];
      p.x += p.vx + Math.sin((p.y + i) / 40) * .4; p.y += p.vy; p.life -= .004; p.r *= .997;
      if (p.life <= 0 || p.y < -40) { parts.splice(i, 1); continue; }
      const g = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, p.r);
      g.addColorStop(0, `rgba(170,255,190,${.22 * p.life})`);
      g.addColorStop(1, "rgba(40,160,70,0)");
      ctx.fillStyle = g; ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2); ctx.fill();
    }
    if (!still) requestAnimationFrame(frame);
  }
  size(); addEventListener("resize", size);
  // Prewarm so the embers already fill the hero on first paint
  const run = still; still = true; for (let k = 0; k < 420; k++) frame(); still = run;
  if (!still) frame();
})();
</script>"""


def build_home():
    page("index.html", "Prometheus Pantheon",
         "The Ember Loom: a community hyperstition. Do one real good deed, with AI help or by hand, and post the proof with #PrometheusEmber.",
         (ROOT / "site" / "pages" / "home.html").read_text() + FIRE_SCRIPT, "index.html")


def build_hearth():
    page("hearth.html", "The Hearth: Give the Flame",
         "Give $PROMETHEUS directly to people doing real good: Spark, Forge, Pass it on. No treasury, no middleman.",
         (ROOT / "site" / "pages" / "hearth.html").read_text() + FIRE_SCRIPT, "hearth.html")


def build_lore():
    chapter = (ROOT / "lore" / "chapter-0-the-first-ember.md").read_text()
    rules = (ROOT / "lore" / "README.md").read_text()
    body = f"""<article class="prose prose--poem">
<div class="chapter-mark">Chapter 0</div>
{markdown(chapter)}
</article>
<section class="prose">
{markdown(rules, demote=1)}
<p><a class="btn" href="{REPO}/issues/new?template=chapter.md" target="_blank" rel="noopener">Propose a chapter or fragment</a></p>
</section>"""
    page("lore.html", "The Ember Loom: Lore",
         "Chapter 0: The First Ember, and the Loom's law. CC0 community lore of the Prometheus Pantheon.",
         body, "lore.html")


def build_proposal():
    body = f"""<article class="prose">
{markdown((ROOT / "proposal.md").read_text())}
</article>"""
    page("proposal.html", "The Ember Loom Proposal",
         "A community experiment, started by one person, owned by no one. What the Ember Loom is, isn't, and how decisions are made.",
         body, "proposal.html")


def build_generator():
    src = (ROOT / "site" / "ember-generator.html").read_text()
    # The artifact embeds the banner as a data URI; the site serves the real file instead
    src = re.sub(r'src="data:image/jpeg;base64,[^"]+"', 'src="media/source/prometheus-pantheon-original.jpg"', src)
    style_end = src.index("</style>") + len("</style>")
    head, body = src[:style_end], src[style_end:]
    head = re.sub(r"<title>.*?</title>\n?", "", head)
    out = f"""<!doctype html>
<html lang="en">
<head>
{meta("Prometheus Ember Generator", "Find a real good deed to do today, with AI help or by hand, and post the action shot with #PrometheusEmber.", "generator.html")}
<link rel="stylesheet" href="assets/site.css">
{head}
</head>
<body>
{nav("generator.html")}
{body}
</body>
</html>
"""
    (ROOT / "generator.html").write_text(out)
    print("wrote generator.html")


if __name__ == "__main__":
    build_home()
    build_hearth()
    build_lore()
    build_proposal()
    build_generator()
