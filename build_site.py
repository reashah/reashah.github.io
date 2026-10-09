"""Build the standalone website in ./docs (served by GitHub Pages) from index.html.

index.html is the artifact version (no <html>/<head> wrapper). This wraps it in a
full document with the base styles the artifact viewer normally supplies, and copies
the images next to it. Run after every edit:  python3 build_site.py
"""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "docs"

BASE_CSS = """
:root { color-scheme: light; padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); }
*, *::before, *::after { box-sizing: border-box; }
body { margin: 0; font: 14px/1.5 system-ui, -apple-system, "Segoe UI", sans-serif; }
img { max-width: 100%; }
[hidden] { display: none !important; }
"""

HEAD_EXTRA = """<meta name="description" content="Rea Shah: brand strategy portfolio. Unilever portfolio strategy, agency brand research and consumer insight, set out as a personal brand book.">
<meta property="og:title" content="Rea Shah">
<meta property="og:description" content="Brand strategy portfolio, set out as a personal brand book.">
<meta property="og:type" content="website">
<meta property="og:image" content="rea.jpg">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Ccircle cx='32' cy='32' r='32' fill='%23121118'/%3E%3Ctext x='32' y='43' font-family='Arial Black,Arial' font-weight='900' font-size='30' text-anchor='middle' fill='%23ffffff'%3Ers%3C/text%3E%3C/svg%3E">"""


def build():
    src = (ROOT / "index.html").read_text(encoding="utf-8")
    style_end = src.index("</style>") + len("</style>")
    head_part, body_part = src[:style_end], src[style_end:]
    title = re.search(r"<title>.*?</title>", head_part).group(0)
    head_rest = head_part.replace(title, "", 1)

    doc = f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{title}
{HEAD_EXTRA}
<style>{BASE_CSS}</style>
{head_rest.strip()}
</head>
<body>
{body_part.strip()}
</body>
</html>
"""
    OUT.mkdir(exist_ok=True)
    (OUT / "index.html").write_text(doc, encoding="utf-8")
    (OUT / ".nojekyll").write_text("")
    copied = []
    for f in sorted(ROOT.iterdir()):
        if f.suffix.lower() in {".jpg", ".jpeg", ".png", ".svg", ".webp"}:
            shutil.copy2(f, OUT / f.name)
            copied.append(f.name)
    print(f"Built docs/index.html with {len(copied)} images")


if __name__ == "__main__":
    build()
