# Go-live migration checklist — refinishing.org

Goal: zero dead links, zero lost rankings, and a significant SEO improvement.
The redirect map covers **every URL in the old site's sitemap (55 URLs) plus
extensionless variants and 66 migrated image URLs** — verified: all 59 legacy
page URLs resolve against the new site with no dead ends.

## What's already in place (in this repo)

- `_redirects` — 102 rules, Netlify format (specific rules before wildcards; incl.
  /services.html, /testpagearchive.html, /1/feed, the Angie's List award PDF and
  an `/uploads/*` catch-all added after the 2026-07 live-crawl audit)
- `netlify.toml` — Pretty URLs OFF (keeps .html canonical URLs), asset caching,
  and a **pre-launch `X-Robots-Tag: noindex` header** for the dev host
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

## Pre-cutover quality gate (run against dcantiques.netlify.app after each deploy)

- `python3 tools/verify-build.py` locally (h1s, JSON-LD, links, titles, img dims)
- Google Rich Results Test + Schema.org validator on: `/`, `/refinishing.html`,
  `/antique-restoration.html`, `/projects/federal-style-collection.html`,
  `/estimate.html` (works despite the pre-launch noindex header)
- PageSpeed Insights, mobile — budget: performance ≥ 90, LCP < 2.5 s, CLS < 0.1
- Manual passes: mobile nav + Services/Trade dropdowns on a phone; the
  assessment form's five paths incl. photo upload; keyboard-only walk of the
  lightbox (focus trap + focus restore) and both dropdowns

## Cutover runbook

### T-minus 2 days (owner + operator)

1. **Search Console**: verify the `www.refinishing.org` URL-prefix property
   AND the `refinishing.org` domain property (DNS TXT). Export current
   queries/pages as the ranking baseline. (Same host + same URLs = a platform
   swap, NOT a site move — do **not** use the Change of Address tool.)
2. **DNS inventory**: at the current DNS host (likely Weebly-managed), export
   every record — especially **MX and any TXT/SPF/DKIM for info@ and
   estimates@ email**. These must be re-created exactly wherever DNS ends up.
   Breaking email is the worst possible cutover failure.
3. **Lower DNS TTLs to 300s** on the A/CNAME records for refinishing.org and
   www, so a rollback takes minutes rather than hours.
4. **Netlify Forms**: enable form detection on project `dcantiques`, redeploy,
   and send one test through the estimate form (with a photo — confirm it
   arrives and lands on `/thanks.html`) and one through the newsletter form
   (→ `/subscribed.html`). Submissions are silently discarded until this is
   done (MIGRATION-PROOF.md §3).
5. **Ads conversion**: create the estimate conversion in Google Ads and paste
   the real label into `thanks.html` (currently a commented placeholder).
6. Run the full pre-cutover quality gate above, plus:
   `npm run verify:redirects` (against dcantiques.netlify.app) → must be
   **PASS on every row** after the latest deploy.

### Cutover day (in order)

7. In Netlify: add custom domains `refinishing.org` + `www.refinishing.org`;
   set **www as primary** (old canonical was www — keep it; apex then 301s
   to www automatically). Verify the exact DNS targets Netlify shows in the
   dashboard — use those values, not documentation from memory.
8. At the DNS host: point `www` (CNAME) and the apex (A/ALIAS) at the values
   from step 7. Recreate the MX/TXT records from step 2 if DNS is moving hosts.
9. Wait for certificate provisioning; Force HTTPS.
10. **Deploy the noindex removal**: delete the `X-Robots-Tag = "noindex"`
    header block from `netlify.toml` in a single-purpose commit and deploy.
    The real domain must never serve noindex.
11. Validate, in this order:
    ```
    python3 tools/verify-redirects.py https://www.refinishing.org
    curl -sI https://refinishing.org/            # expect 301 → https://www
    curl -sI http://www.refinishing.org/         # expect 301 → https
    curl -sI https://www.refinishing.org/ | grep -i x-robots   # expect NOTHING
    ```
    Then hand-check the crown jewels: `/old-home-page.html`, both legacy door
    URLs, `/testimonials.html`, `/projects/restoration-federal-style-antiques`,
    one `/uploads/...` image.
12. **Search Console, same day**: submit `sitemap.xml`; URL-Inspect →
    Request indexing for `/`, `/refinishing.html`, `/antique-restoration.html`,
    `/doors.html`, `/estimate.html`, `/furniture-care.html`.
13. Update website links on: Google Business Profile, Yelp, Angi, Facebook,
    Instagram bio, Houzz (https://www.houzz.com/pro/afrdc), Nextdoor —
    especially any that point at deep pages.

### Weeks 1–4: monitoring

- **Daily, week 1**: Search Console → Pages (404 spikes = a missed URL; add a
  redirect row to `_redirects` + `redirects.csv` + `.htaccess`, redeploy);
  Netlify Forms submissions arriving; GA4 realtime shows traffic on
  G-H890QYMC8J.
- **Weekly**: GSC Performance vs the exported baseline (expect churn for 2–4
  weeks; 301s carry the signals); Crawl Stats for anomalies; rankings on the
  watchlist queries (furniture restoration/refinishing washington dc, antique
  restoration maryland/virginia, historic door restoration dc, french
  polishing washington dc).
- Keep the Weebly subscription (and its DNS export) for **at least 30 days**.

### Rollback

Trigger: site down/misrouted, email broken, forms not delivering and not
fixable same-day, or a security/DNS mistake. (Do NOT roll back for normal
ranking churn in weeks 1–2.)

1. Repoint DNS to the saved Weebly values (TTL 300 → minutes to take effect).
2. Re-add the `X-Robots-Tag = "noindex"` block to `netlify.toml` and deploy,
   so the dev host goes back to being non-indexable.
3. Diagnose, fix, re-run this runbook from step 6.

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
