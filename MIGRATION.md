# Go-live migration checklist — refinishing.org

Goal: zero dead links, zero lost rankings, and a significant SEO improvement.
The redirect map covers **every URL in the old site's sitemap (55 URLs) plus
extensionless variants and 66 migrated image URLs** — verified: all 59 legacy
page URLs resolve against the new site with no dead ends.

## What's already in place (in this repo)

- `_redirects` — 96 rules, Netlify format (specific rules before wildcards)
- `.htaccess` — the same map for Apache hosts
- `redirects.csv` — human-readable documentation of every mapping
- **Path continuity** — the highest-value URLs did not change at all:
  `/about.html`, `/estimate.html`, `/gallery.html`, `/projects.html`
- `/furniture-care.html` — preserves the indexed "Fine Furniture Care 101"
  article (the old blog's flagship content) instead of redirecting it away
- Per-page SEO: unique titles + meta descriptions with DC/MD/VA phrasing,
  canonicals, Open Graph + Twitter cards, `LocalBusiness` schema (home),
  `Service` schema (3 service pages), `FAQPage` schema (about), `Article`
  schema (care guide), `BreadcrumbList` on interior pages
- `sitemap.xml` + `robots.txt`, custom `404.html` (noindex)
- Performance: preloaded LCP hero images, width/height on images (no CLS),
  lazy-loading below the fold, `font-display: swap`

## Cutover steps (in order)

1. **Before switching DNS**: in Google Search Console, verify the property
   for `www.refinishing.org` (and the domain property) if not already done.
   Export current queries/rankings as a baseline.
2. Deploy this folder to the new host (e.g. Netlify). Confirm the deploy
   serves `_redirects` (test: `curl -I https://<preview>/testimonials.html`
   → `301` → `/about.html#testimonials`).
3. Set `www.refinishing.org` as the **primary domain**; ensure apex
   `refinishing.org` 301s to `www` (Netlify does this automatically once the
   primary domain is set). Old canonical was `www` — keep it.
4. Force HTTPS.
5. Switch DNS. Keep the Weebly site untouched until DNS has fully propagated.
6. **Immediately after cutover**:
   - Spot-check 10–15 legacy URLs from `redirects.csv` return 301 → 200.
   - Submit `sitemap.xml` in Search Console.
   - Use URL Inspection → Request indexing for `/`, the three service pages
     and `/furniture-care.html`.
7. **The following weeks**: watch Search Console → Coverage for 404 spikes
   (any URL we missed shows up there — add a redirect rule and redeploy),
   and Performance for position changes. Expect some churn for 2–4 weeks;
   the 301s pass ranking signals.
8. Update the Google Business Profile website link, Yelp, Facebook,
   Instagram bio links if any of them point at deep pages.

## Why rankings should improve, not just survive

- Old keyword-rich landing pages 301 to focused successors
  (`door-restoration-washington-dc-va-md.html` → `/doors.html` with matching
  title/H1/copy including Capitol Hill & Georgetown).
- Real structured data (LocalBusiness, Service, FAQPage) where the old site
  had only Weebly defaults.
- Much faster, mobile-first pages (old site: render-blocking Weebly bundles).
- Preserved and improved evergreen content (`/furniture-care.html`).
- Descriptive alt text on every image; before/after photos redirected
  file-to-file so Google Images equity carries over.
