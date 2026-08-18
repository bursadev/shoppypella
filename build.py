#!/usr/bin/env python3
"""Unpack the Shoppypella single-file bundle into a static GitHub Pages site.

The source `shoppypella-tr.html` is a self-unpacking bundle: a manifest of
base64 assets keyed by UUID, plus a template in which every asset reference is
that bare UUID. At runtime the bundler rewrites UUID -> blob: URL.

A static host needs none of that, so we write the assets to disk and rewrite
the UUIDs to relative paths instead. That also repairs the `assets/imgNN.jpeg`
product references, which were broken in the bundle (no filesystem to resolve
them against).
"""
import base64, gzip, json, os, re, shutil, sys
from PIL import Image

SRC  = "src/shoppypella-tr.html"
OUT  = "docs"
PHOTO_DIR = "src/photos"
COMPONENT_DIR = "components"
RUNTIME_UUID = "7a428bfa-87d0-470e-8db9-7fcb796f5c1e"
HERO_BLUE    = "7e70d42e-f407-4dea-9b99-b67e3a813b78"   # London Blue  -> img01
HERO_ROSE    = "97e0184a-d894-4c15-99db-afb2078964ab"   # Rose Paris   -> img02

# Catalog slot -> source photo. The logic script references img01-08 and img10.
PHOTOS = {
    "img01": "WhatsApp Image 2026-06-28 at 15.58.24.jpeg",      # Oda Kokusu London Blue
    "img02": "WhatsApp Image 2026-06-28 at 15.58.24 (1).jpeg",  # Oda & Tekstil Rose Paris
    "img03": "WhatsApp Image 2026-06-28 at 15.58.26.jpeg",      # Mega Mop yedek baslik
    "img04": "WhatsApp Image 2026-06-28 at 15.58.26 (1).jpeg",  # Mikrofiber yer bezi 50x70
    "img05": "WhatsApp Image 2026-06-28 at 15.58.26 (2).jpeg",  # Mutfak bezi 3'lu gri
    "img06": "WhatsApp Image 2026-06-28 at 15.58.26 (3).jpeg",  # Havlu bez 8'li renkli
    "img07": "WhatsApp Image 2026-06-28 at 15.58.26 (4).jpeg",  # Zor kir teli 10'lu
    "img08": "WhatsApp Image 2026-06-28 at 15.58.26 (5).jpeg",  # Zor kir bezi 2'li
    "img10": "WhatsApp Image 2026-06-28 at 15.58.26 (7).jpeg",  # Mutfak bezi 3'lu renkli
}

def read_bundle():
    lines = open(SRC, encoding="utf-8").read().split("\n")
    manifest = template = None
    # Match the tag lines exactly -- the unpacker's own JS mentions these
    # type strings too, and would otherwise match first.
    for i, ln in enumerate(lines):
        if ln.strip() == '<script type="__bundler/manifest">':
            manifest = json.loads(lines[i + 1])
        if ln.strip() == '<script type="__bundler/template">':
            template = json.loads(lines[i + 1])
    assert manifest and template, "manifest/template not found"
    return manifest, template

def asset_bytes(entry):
    raw = base64.b64decode(entry["data"])
    return gzip.decompress(raw) if entry.get("compressed") else raw

def main():
    manifest, template = read_bundle()
    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(f"{OUT}/assets/fonts", exist_ok=True)

    # 1. runtime
    with open(f"{OUT}/assets/dc-runtime.js", "wb") as f:
        f.write(asset_bytes(manifest[RUNTIME_UUID]))
    template = template.replace(RUNTIME_UUID, "assets/dc-runtime.js")

    # 2. fonts
    fonts = 0
    for uuid, entry in manifest.items():
        if entry["mime"] != "font/woff2":
            continue
        with open(f"{OUT}/assets/fonts/{uuid}.woff2", "wb") as f:
            f.write(asset_bytes(entry))
        template = template.replace(uuid, f"assets/fonts/{uuid}.woff2")
        fonts += 1

    # 3. product photos, downscaled for the web
    for slot, src in sorted(PHOTOS.items()):
        im = Image.open(os.path.join(PHOTO_DIR, src)).convert("RGB")
        im.thumbnail((900, 1350), Image.LANCZOS)
        im.save(f"{OUT}/assets/{slot}.jpeg", "JPEG", quality=85, optimize=True,
                progressive=True)

    # The two bundled hero images are the same London Blue / Rose Paris shots
    # the catalog already names, so point them at the catalog slots.
    template = template.replace(HERO_BLUE, "assets/img01.jpeg")
    template = template.replace(HERO_ROSE, "assets/img02.jpeg")

    # These photos are branded marketing tiles, not white-background cutouts,
    # so multiply blending would tint the whole tile blue.
    template = template.replace(";mix-blend-mode:multiply", "")

    leftover = re.findall(r'"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"', template)
    assert not leftover, f"unresolved UUID refs: {set(leftover)}"

    # 4. head: real title, language, social preview, favicon
    head = '''<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Shoppypella — İnteraktif Prototip</title>
<meta name="description" content="Shoppypella pazaryeri için interaktif prototip: ana sayfa, kategori, ürün detayı, satıcı mağazası, hesap, sepet ve satıcı paneli.">
<meta property="og:title" content="Shoppypella — İnteraktif Prototip">
<meta property="og:description" content="İsviçre pazaryeri konsepti — 8 ekran, masaüstü ve mobil.">
<meta property="og:type" content="website">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">'''
    template = template.replace(
        '<meta name="viewport" content="width=device-width, initial-scale=1">', head, 1)
    template = template.replace("<html>", '<html lang="tr">', 1)

    with open(f"{OUT}/index.html", "w", encoding="utf-8") as f:
        f.write(template)

    # Brand mark, lifted from the bundle's own splash screen.
    open(f"{OUT}/assets/favicon.svg", "w").write(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
        '<rect width="64" height="64" rx="14" fill="#F2660F"/>'
        '<text x="32" y="46" font-family="Helvetica,Arial,sans-serif" font-size="42"'
        ' font-weight="900" fill="#fff" text-anchor="middle">S</text></svg>')

    # 5. sibling Design Components. The bundle referenced ProductCard, Thumb and
    # Footer but shipped none of them, so every product grid and thumbnail
    # rendered as an empty placeholder. dc-runtime resolves `<dc-import name="X">`
    # by fetching ./X.dc.html, which a static host can actually serve.
    comps = 0
    for name in sorted(os.listdir(COMPONENT_DIR)):
        if name.endswith(".dc.html"):
            shutil.copy(f"{COMPONENT_DIR}/{name}", f"{OUT}/{name}")
            comps += 1
    print(f"components: {comps}")

    open(f"{OUT}/.nojekyll", "w").close()

    print(f"runtime: {os.path.getsize(OUT+'/assets/dc-runtime.js')} bytes")
    print(f"fonts:   {fonts}")
    for slot in sorted(PHOTOS):
        print(f"  {slot}.jpeg  {os.path.getsize(f'{OUT}/assets/{slot}.jpeg'):>7} bytes")
    print(f"index:   {os.path.getsize(OUT+'/index.html')} bytes")

main()
