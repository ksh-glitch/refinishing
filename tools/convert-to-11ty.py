#!/usr/bin/env python3
"""One-time converter: root *.html pages -> src/ Eleventy templates.

Reads each chrome-bearing page, extracts the per-page head data and the
<main> content, and writes src/<page>.html with JSON front matter.
Also generates src/_includes/header.njk and footer.njk FROM index.html
itself, so the shared chrome is byte-identical to the current site by
construction. Root originals are left untouched (verify-build.py compares
the built output against them).
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
INC = os.path.join(SRC, "_includes")

PAGES = [
    "index.html", "refinishing.html", "upholstery.html", "doors.html",
    "projects.html", "gallery.html", "commissions.html", "about.html",
    "estimate.html", "guides.html", "furniture-care.html",
    "worth-restoring.html", "restoration-costs.html", "french-polish.html",
    "reupholster-or-replace.html", "chair-repair.html",
    "shipping-heirloom.html", "trade.html", "damage-restoration.html",
]


def read(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.read()


def extract_chrome():
    """Generate header.njk / footer.njk from the current index.html bytes."""
    html = read("index.html")
    header = re.search(r"(<header class=\"site-header[^\"]*\">.*?</header>)", html, re.S).group(1)
    footer = re.search(r"(<footer class=\"site-footer\">.*?</footer>)", html, re.S).group(1)

    # Parameterize the dark-hero header variant (only index uses it today).
    header = header.replace(
        '<header class="site-header header-on-dark">',
        '<header class="site-header{% if headerOnDark %} header-on-dark{% endif %}">',
    )
    # Parameterize aria-current on every nav link (index carries none itself).
    def nav_link(m):
        href, label = m.group(1), m.group(2)
        key = href[:-len(".html")]
        return ('<a href="%s"{%% if navKey == "%s" %%} aria-current="page"{%% endif %%}>%s</a>'
                % (href, key, label))
    header = re.sub(r'<a href="([a-z-]+\.html)">([^<]+)</a>', nav_link, header)

    os.makedirs(INC, exist_ok=True)
    # One-shot migration helper: NEVER overwrite includes once they exist —
    # header.njk/footer.njk are hand-maintained after the initial conversion
    # (the nav was restructured in Phase 2C).
    for name, content in (("header.njk", header), ("footer.njk", footer)):
        path = os.path.join(INC, name)
        if os.path.exists(path):
            print(f"includes: {name} exists — left untouched")
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content + "\n")
            print(f"includes: {name} generated from index.html")


def convert(page):
    html = read(page)
    head = re.search(r"<head>(.*?)</head>", html, re.S).group(1)
    # The noscript reveal-fallback is boilerplate emitted by base.njk —
    # drop it here so its inner <style> is not re-captured as headExtra.
    head = re.sub(r"<noscript>.*?</noscript>", "", head, flags=re.S)

    def one(pattern, required=True):
        m = re.search(pattern, head, re.S)
        if not m and required:
            sys.exit(f"FATAL {page}: no match for {pattern!r}")
        return m.group(1) if m else None

    data = {
        "layout": "base.njk",
        "permalink": "/" + page,
        "doctitle": one(r"<title>(.*?)</title>"),
        "description": one(r'<meta name="description" content="(.*?)">'),
        "canonical": one(r'<link rel="canonical" href="https://www\.refinishing\.org(/[^"]*)">'),
        "ogType": one(r'<meta property="og:type" content="(.*?)">'),
        "ogTitle": one(r'<meta property="og:title" content="(.*?)">'),
        "ogDescription": one(r'<meta property="og:description" content="(.*?)">'),
        "ogImage": one(r'<meta property="og:image" content="(.*?)">'),
    }
    # index canonical is "/" but permalink must stay /index.html for the file;
    # Eleventy writes /index.html for permalink "/" anyway — keep explicit.
    if page == "index.html":
        data["permalink"] = "/index.html"

    schemas = re.findall(r'<script type="application/ld\+json">.*?</script>', head, re.S)
    if schemas:
        data["schemas"] = "\n  ".join(schemas)
    extra = re.findall(r'<link rel="preload"[^>]*>', head) + \
            re.findall(r"<style>.*?</style>", head, re.S)
    if extra:
        data["headExtra"] = "\n  ".join(extra)
    if "header-on-dark" in html:
        data["headerOnDark"] = True
    nav = re.search(r'<nav class="site-nav".*?</nav>', html, re.S).group(0)
    cur = re.search(r'<a href="([a-z-]+)\.html" aria-current="page"', nav)
    if cur:
        data["navKey"] = cur.group(1)

    body = html.split('<main id="main">', 1)[1].rsplit("</main>", 1)[0]

    os.makedirs(SRC, exist_ok=True)
    with open(os.path.join(SRC, page), "w", encoding="utf-8") as f:
        f.write("---json\n" + json.dumps(data, indent=2, ensure_ascii=False) + "\n---\n" + body)
    print(f"converted: {page} (navKey={data.get('navKey')}, "
          f"schemas={len(schemas)}, extra={len(extra)})")


if __name__ == "__main__":
    extract_chrome()
    for p in PAGES:
        convert(p)
    print(f"\n{len(PAGES)} pages written to src/")
