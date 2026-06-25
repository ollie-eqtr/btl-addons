"""Inline the Phase 1 Family Dining hi-fi prototype into one portable file.

Reads the linked working file (phase1-dining-fam-hifi.html + app.css + the
assets-*/ and neutraface-text/ folders) and writes a single self-contained
HTML file with every font, icon and food photo embedded as a base64 data URI.

The linked working file is left untouched so iteration can continue; re-run
this script after any change to regenerate the portable build.
"""
import base64, re, pathlib

SRC = pathlib.Path("phase1-dining-fam-hifi.html")
CSS = pathlib.Path("app.css")
OUT = pathlib.Path("phase1-dining-fam-hifi-embed.html")

MIME = {
    ".otf": "font/otf", ".ttf": "font/ttf", ".woff": "font/woff", ".woff2": "font/woff2",
    ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".svg": "image/svg+xml", ".gif": "image/gif", ".webp": "image/webp",
}

def data_uri(path):
    p = pathlib.Path(path)
    mime = MIME.get(p.suffix.lower(), "application/octet-stream")
    b64 = base64.b64encode(p.read_bytes()).decode("ascii")
    return "data:%s;base64,%s" % (mime, b64)

# 1) Inline every url("...") in app.css (fonts + CSS images) as data URIs.
css = CSS.read_text(encoding="utf-8")
URL_RE = re.compile(r"""url\((['"]?)([^'")]+)\1\)""")
seen = {}
def repl(m):
    url = m.group(2).strip()
    if url.startswith(("data:", "http://", "https://")):
        return m.group(0)
    if url not in seen:
        seen[url] = data_uri(url)
    return 'url("%s")' % seen[url]
css_inlined, n_css = URL_RE.subn(repl, css)

# 2) Build the runtime ASSETS map for the meal-plate <img> tags built in JS
#    (DISH points at assets-img/). Only include files NOT already inlined via
#    the CSS, so each image is embedded once.
assets = {}
d = pathlib.Path("assets-img")
if d.is_dir():
    for f in sorted(d.iterdir()):
        rel = "assets-img/%s" % f.name
        if f.is_file() and f.suffix.lower() in MIME and rel not in css:
            assets[rel] = data_uri(f)
assets_js = "window.ASSETS={" + ",".join('"%s":"%s"' % (k, v) for k, v in assets.items()) + "};"

# 3) Splice the inlined CSS into the HTML and inject the ASSETS map.
html = SRC.read_text(encoding="utf-8")

html, n_link = re.subn(r'<link\b[^>]*href="app\.css"[^>]*>',
                       "<style>\n" + css_inlined + "\n</style>", html, count=1)
assert n_link == 1, "stylesheet <link> not found (replaced %d)" % n_link

html, n_assets = re.subn(r"window\.ASSETS\s*=\s*window\.ASSETS\s*\|\|\s*\{\};",
                         assets_js, html, count=1)
assert n_assets == 1, "window.ASSETS initialiser not found (replaced %d)" % n_assets

# 4) Inline asset references that sit directly in HTML attributes, e.g.
#    <img src="assets-img/drinks.jpg"> in the drinks modal.
ATTR_RE = re.compile(r'(src|href)="((?:assets-[^"/]+|neutraface-text)/[^"]+)"')
def attr_repl(m):
    attr, url = m.group(1), m.group(2)
    if not pathlib.Path(url).is_file():
        return m.group(0)
    if url not in seen:
        seen[url] = data_uri(url)
    return '%s="%s"' % (attr, seen[url])
html, n_attr = ATTR_RE.subn(attr_repl, html)

OUT.write_text(html, encoding="utf-8")

# Genuine external references would appear inside url(), src="" or the app.css <link>.
# The remaining "assets-*/..." strings are only JS lookup keys (DISH + window.ASSETS).
leftover = re.findall(r'(?:url\(["\']?(?:assets-|neutraface-)|src="(?:assets-|neutraface-)|href="app\.css")', html)
print("OK -> %s" % OUT.name)
print("  CSS url() inlined : %d" % n_css)
print("  HTML attrs inlined: %d" % n_attr)
print("  runtime assets    : %d (%s)" % (len(assets), ", ".join(sorted(assets))))
print("  output size       : %.1f MB" % (OUT.stat().st_size / 1048576))
print("  external refs     : %d %s" % (len(leftover), "(OK, fully self-contained)" if not leftover else "!! still linked: %s" % set(leftover)))
