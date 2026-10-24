"""Build the Sitekeeper test site: content/<lang>/<slug>.html + layout -> out/.

Standard library only. Content file = header lines "key: value", a line "---",
then the page body. content/<lang>/_site.html holds header/footer texts as
<p data-key="..."> lines. es is served at the root, ru under /ru/.
"""
import html
import json
import pathlib
import re
import shutil

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT.parent / "out"
CONFIG = json.loads((ROOT / "config.json").read_text())
KEY_RE = re.compile(r'<p data-key="([a-z0-9_]+)">(.*?)</p>', re.DOTALL)


def parse(path):
    raw = path.read_text(encoding="utf-8")
    head, _, body = raw.partition("\n---\n")
    meta = dict(line.split(": ", 1) for line in head.splitlines() if ": " in line)
    return meta, body


def layout(lang, meta, body, site):
    prefix = "" if lang == "es" else f"{lang}/"
    base = CONFIG["base_url"].rstrip("/") + "/"
    booking = ""
    if meta.get("slug") == "reserva" and CONFIG.get("booking_site_id"):
        booking = (f'<script src="{CONFIG["app_url"]}/booking.js" '
                   f'data-site="{CONFIG["booking_site_id"]}" data-lang="{lang}" defer></script>')
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<base href="{base}">
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>{html.escape(meta.get("title", ""))}</title>
<meta name="description" content="{html.escape(meta.get("description", ""), quote=True)}">
<link rel="stylesheet" href="assets/site.css">
</head>
<body>
<header><a href="{prefix}index.html">{site.get("header_name", "")}</a>
 <nav><a href="{prefix}reserva.html">{site.get("header_link_reserva", "")}</a></nav></header>
<main>
{body}
</main>
<footer><p>{site.get("footer_legal", "")}</p></footer>
{booking}
</body>
</html>
"""


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    for sub in ("media", "assets"):
        if (ROOT / sub).is_dir():
            shutil.copytree(ROOT / sub, OUT / sub)
    for lang_dir in sorted((ROOT / "content").iterdir()):
        lang = lang_dir.name
        site_file = lang_dir / "_site.html"
        site = dict(KEY_RE.findall(parse(site_file)[1])) if site_file.exists() else {}
        target = OUT if lang == "es" else OUT / lang
        target.mkdir(exist_ok=True)
        for page in sorted(lang_dir.glob("*.html")):
            if page.name.startswith("_"):
                continue
            meta, body = parse(page)
            (target / page.name).write_text(layout(lang, meta, body, site), encoding="utf-8")
    (OUT / ".nojekyll").write_text("")
    print("built", sum(1 for _ in OUT.rglob("*.html")), "pages")


if __name__ == "__main__":
    main()
