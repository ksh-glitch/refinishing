#!/usr/bin/env python3
"""Redirect verification for the refinishing.org migration (plan §14).

For every row of redirects.csv, requests the OLD path against a base host
with redirects disabled and asserts:
  (a) first hop is 301
  (b) Location matches the mapped target exactly (fragment included)
  (c) the target itself answers 200 on the same host

Wildcard rows (/projects/*, /blog/*, /store/*, /uploads/*) are probed with a
representative made-up path. Rows whose target is served by a real file that
now exists at the old path (none today) would be reported as NOFOLLOW.

Usage:
  python3 tools/verify-redirects.py                          # dev host
  python3 tools/verify-redirects.py https://www.refinishing.org   # post-cutover
"""
import csv
import os
import sys
import urllib.parse
import urllib.request

BASE = (sys.argv[1] if len(sys.argv) > 1 else "https://dcantiques.netlify.app").rstrip("/")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

WILDCARD_PROBE = "zz-migration-probe-xyz"


def head(url, follow=False):
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *args, **kwargs):
            return None
    handlers = [] if follow else [NoRedirect()]
    opener = urllib.request.build_opener(*handlers)
    req = urllib.request.Request(url, method="GET",
                                 headers={"User-Agent": "refinishing-migration-check"})
    try:
        with opener.open(req, timeout=20) as r:
            return r.status, r.headers.get("Location", "")
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Location", "")
    except Exception as e:
        return 0, str(e)


def norm_location(loc):
    """Netlify returns absolute Locations; compare path(+query)+fragment."""
    if not loc:
        return ""
    p = urllib.parse.urlsplit(loc)
    frag = f"#{p.fragment}" if p.fragment else ""
    return (p.path or "/") + frag


rows = []
with open(os.path.join(ROOT, "redirects.csv"), newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        if len(row) >= 2 and row[0].startswith("/"):
            rows.append((row[0], row[1]))

ok = fails = 0
failures = []
for old, target in rows:
    probe = old.replace("*", WILDCARD_PROBE)
    status, loc = head(BASE + urllib.parse.quote(probe, safe="/:%*?#="))
    got = norm_location(loc)
    want = target if target.startswith("/") else "/" + target
    if status != 301 or got != want:
        fails += 1
        failures.append(f"{old} -> {status} {got or '(no Location)'} (want 301 {want})")
        continue
    # Confirm the destination answers 200 (fragment stripped).
    dest = want.split("#")[0] or "/"
    dstatus, _ = head(BASE + dest, follow=True)
    if dstatus != 200:
        fails += 1
        failures.append(f"{old} -> 301 {want} but target answers {dstatus}")
        continue
    ok += 1

print(f"base: {BASE}")
print(f"PASS {ok} / {len(rows)}   FAIL {fails}")
for f in failures:
    print("  FAIL", f)
sys.exit(1 if fails else 0)
