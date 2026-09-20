#!/usr/bin/env python3
"""Assemble the static GitHub Pages site from the design handoff in src/handoff.

The handoff is a Design Component package: `Shoppypella.dc.html` (the root
component, all 8 screens), three sibling components it imports, the dc-runtime
(`support.js`) and the product photography. It is meant to be opened from a
directory, so almost everything already works as-is on a static host.

What this script changes:

  * the runtime is renamed to `assets/dc-runtime.js` and the head gets a real
    title, description, social preview and favicon;
  * the two Google Fonts stylesheet links are swapped for the self-hosted
    @font-face rules in `src/fonts` -- the site then needs no font CDN;
  * product photos are downscaled for the web;
  * the price-model page in `src/preismodell` ships as `docs/preismodell/`,
    with the same self-hosted fonts (Hanken Grotesk + IBM Plex Mono).

Everything else is copied verbatim, so the handoff stays the source of truth.
"""
import os, re, shutil
from PIL import Image

HANDOFF = "src/handoff"
FONT_DIR = "src/fonts"
OUT      = "docs"
ROOT     = "Shoppypella.dc.html"          # the root component -> index.html
SIBLINGS = ["ProductCard.dc.html", "Footer.dc.html", "Thumb.dc.html"]
PRICE    = "src/preismodell/index.html"   # -> docs/preismodell/index.html
OFFER    = "src/angebot/index.html"       # -> docs/angebot/index.html
MAX_PHOTO = (900, 1350)

HEAD = '''<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Shoppypella — İnteraktif Prototip</title>
<meta name="description" content="Shoppypella pazaryeri için interaktif prototip: ana sayfa, kategori, ürün detayı, satıcı mağazası, hesap, sepet, satıcı kaydı ve satıcı paneli.">
<meta property="og:title" content="Shoppypella — İnteraktif Prototip">
<meta property="og:description" content="İsviçre pazaryeri konsepti — 8 ekran, masaüstü ve mobil.">
<meta property="og:type" content="website">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<script src="assets/dc-runtime.js"></script>'''

FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
           '<rect width="64" height="64" rx="14" fill="#F2660F"/>'
           '<text x="32" y="46" font-family="Helvetica,Arial,sans-serif" font-size="42"'
           ' font-weight="900" fill="#fff" text-anchor="middle">S</text></svg>')

# The handoff pulls all four theme families from Google Fonts. We ship them.
GOOGLE_FONTS = re.compile(
    r'[ \t]*<link[^>]*fonts\.(?:googleapis|gstatic)\.com[^>]*>\n', re.I)


def self_hosted_fonts(names=("hanken-grotesk.css", "theme-fonts.css")):
    css = []
    for name in names:
        css.append("<style>\n%s\n</style>" %
                   open(f"{FONT_DIR}/{name}", encoding="utf-8").read().strip())
    return "\n".join(css) + "\n"


def build_index():
    html = open(f"{HANDOFF}/{ROOT}", encoding="utf-8").read()

    html = html.replace('<html>', '<html lang="tr">', 1)
    html = html.replace(
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<script src="./support.js"></script>', HEAD, 1)
    assert 'assets/dc-runtime.js' in html, "runtime script tag not rewritten"

    html, n = GOOGLE_FONTS.subn("", html)
    assert n == 4, f"expected 4 Google Fonts links, replaced {n}"
    html = html.replace("<helmet>\n", "<helmet>\n" + self_hosted_fonts(), 1)

    with open(f"{OUT}/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    return html


def build_price_model():
    """docs/preismodell/ -- a plain page, no runtime; fonts one level up."""
    html = open(PRICE, encoding="utf-8").read()
    html, n = GOOGLE_FONTS.subn("", html)
    assert n == 3, f"expected 3 Google Fonts links in the price model, replaced {n}"
    css = self_hosted_fonts(("hanken-grotesk.css", "ibm-plex-mono.css"))
    css = css.replace('url("assets/fonts/', 'url("../assets/fonts/')
    html = html.replace("<style>", css + "<style>", 1)
    os.makedirs(f"{OUT}/preismodell", exist_ok=True)
    with open(f"{OUT}/preismodell/index.html", "w", encoding="utf-8") as f:
        f.write(html)


def build_offer():
    """docs/angebot/ -- the interactive quote; same shape as the price model."""
    html = open(OFFER, encoding="utf-8").read()
    html, n = GOOGLE_FONTS.subn("", html)
    assert n == 3, f"expected 3 Google Fonts links in the offer, replaced {n}"
    css = self_hosted_fonts(("hanken-grotesk.css", "ibm-plex-mono.css"))
    css = css.replace('url("assets/fonts/', 'url("../assets/fonts/')
    html = html.replace("<style>", css + "<style>", 1)
    os.makedirs(f"{OUT}/angebot", exist_ok=True)
    with open(f"{OUT}/angebot/index.html", "w", encoding="utf-8") as f:
        f.write(html)


def copy_asset(rel):
    """Copy one `assets/…` reference out of the handoff, photos downscaled."""
    src, dst = f"{HANDOFF}/{rel}", f"{OUT}/{rel}"
    if rel.endswith(".jpeg"):
        im = Image.open(src)
        if im.width <= MAX_PHOTO[0] and im.height <= MAX_PHOTO[1]:
            shutil.copy(src, dst)          # already web-sized; don't re-encode
            return
        im = im.convert("RGB")
        im.thumbnail(MAX_PHOTO, Image.LANCZOS)
        im.save(dst, "JPEG", quality=85, optimize=True, progressive=True)
    elif rel.endswith(".png"):
        Image.open(src).save(dst, "PNG", optimize=True)
    else:
        shutil.copy(src, dst)


def main():
    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(f"{OUT}/assets/fonts", exist_ok=True)

    shutil.copy(f"{HANDOFF}/support.js", f"{OUT}/assets/dc-runtime.js")
    for name in sorted(os.listdir(FONT_DIR)):
        if name.endswith(".woff2"):
            shutil.copy(f"{FONT_DIR}/{name}", f"{OUT}/assets/fonts/{name}")

    # dc-runtime resolves `<dc-import name="X">` by fetching ./X.dc.html, so the
    # siblings ship next to index.html, untouched.
    for name in SIBLINGS:
        shutil.copy(f"{HANDOFF}/{name}", f"{OUT}/{name}")

    html = build_index()
    build_price_model()
    build_offer()

    # Only the photos the prototype actually shows; the handoff carries spares.
    refs = set()
    for text in [html] + [open(f"{OUT}/{n}", encoding="utf-8").read() for n in SIBLINGS]:
        refs |= set(re.findall(r'assets/[A-Za-z0-9_.-]+\.(?:jpeg|jpg|png|svg)', text))
    for rel in sorted(refs - {"assets/favicon.svg"}):
        copy_asset(rel)

    open(f"{OUT}/assets/favicon.svg", "w").write(FAVICON)
    open(f"{OUT}/.nojekyll", "w").close()

    missing = [r for r in refs if not os.path.exists(f"{OUT}/{r}")]
    assert not missing, f"referenced but not built: {missing}"

    print(f"runtime:    {os.path.getsize(OUT + '/assets/dc-runtime.js'):>8} bytes")
    print(f"fonts:      {len(os.listdir(OUT + '/assets/fonts')):>8} files")
    print(f"components: {len(SIBLINGS):>8} files")
    for rel in sorted(refs - {"assets/favicon.svg"}):
        print(f"  {rel:<20} {os.path.getsize(OUT + '/' + rel):>8} bytes")
    print(f"index:      {os.path.getsize(OUT + '/index.html'):>8} bytes")
    print(f"preismodell:{os.path.getsize(OUT + '/preismodell/index.html'):>8} bytes")
    print(f"angebot:    {os.path.getsize(OUT + '/angebot/index.html'):>8} bytes")


main()
