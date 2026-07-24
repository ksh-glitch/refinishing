#!/usr/bin/env python3
"""Build smoke-check for the Eleventy output in _site/.

History: this tool began as the Eleventy-migration parity gate — on
2026-07-24 all 19 pages built byte-identical to the pre-Eleventy root
pages (main content, header/footer, head element multiset). That gate
PASSED and was retired when Phase 3 intentionally changed page content.

Now it guards every build:
  1. every src page produced an output file
  2. exactly one <h1> per page
  3. every JSON-LD block parses
  4. no unrendered Nunjucks artifacts ({{ ... }} / {% ... %})
  5. internal .html links resolve to files in _site
  6. titles and meta descriptions present and unique site-wide
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "_site")

pages = sorted(
    os.path.relpath(p, os.path.join(ROOT, "src"))
    for p in glob.glob(os.path.join(ROOT, "src", "*.html"))
    + glob.glob(os.path.join(ROOT, "src", "projects", "*.html"))
)

fails = 0
titles, descs = {}, {}

def fail(page, msg):
    global fails
    fails += 1
    print(f"FAIL {page}: {msg}")

built_files = set()
if os.path.isdir(SITE):
    for dirpath, _dirs, files in os.walk(SITE):
        for name in files:
            if name.endswith(".html"):
                built_files.add(
                    os.path.relpath(os.path.join(dirpath, name), SITE))

for page in pages:
    path = os.path.join(SITE, page)
    if not os.path.exists(path):
        fail(page, "not built")
        continue
    html = open(path, encoding="utf-8").read()
    problems = []

    h1s = re.findall(r"<h1[\s>]", html)
    if len(h1s) != 1:
        problems.append(f"{len(h1s)} h1 elements")

    for i, block in enumerate(re.findall(
            r'<script type="application/ld\+json">(.*?)</script>', html, re.S)):
        try:
            json.loads(block)
        except Exception as e:
            problems.append(f"JSON-LD block {i} invalid: {e}")

    if re.search(r"{{.*?}}|{%.*?%}", html):
        problems.append("unrendered template artifacts")

    nodims = [t for t in re.findall(r"<img [^>]*>", html) if "width=" not in t]
    if nodims:
        problems.append(f"{len(nodims)} img(s) missing width/height")

    title = re.search(r"<title>(.*?)</title>", html, re.S)
    desc = re.search(r'<meta name="description" content="(.*?)"', html)
    if not title or not title.group(1).strip():
        problems.append("missing <title>")
    else:
        t = title.group(1).strip()
        if t in titles:
            problems.append(f"duplicate title (also {titles[t]})")
        titles[t] = page
    if not desc or not desc.group(1).strip():
        problems.append("missing meta description")
    else:
        d = desc.group(1).strip()
        if d in descs:
            problems.append(f"duplicate description (also {descs[d]})")
        descs[d] = page

    # Internal links are root-relative (/page.html, /projects/slug.html).
    for href in re.findall(r'href="/((?:projects/)?[a-z0-9][a-z0-9-]*\.html)(?:[?#][^"]*)?"', html):
        if href.replace("/", os.sep) not in built_files and href not in built_files:
            problems.append(f"broken internal link: /{href}")

    if problems:
        fail(page, "; ".join(sorted(set(problems))))
    else:
        print(f"PASS {page}")

print(f"\n{'ALL PASS' if fails == 0 else str(fails) + ' FAILURES'} "
      f"({len(pages)} pages checked)")
sys.exit(1 if fails else 0)
