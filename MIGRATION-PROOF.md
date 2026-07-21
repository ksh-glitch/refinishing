# Migration Proof — live Netlify deploy

**Date:** 2026-07-21
**Live URL tested:** https://dcantiques.netlify.app (Netlify project `dcantiques`,
site id `43fcad46-96cb-40ee-a0b9-2c91c584bb88`)
**Scope:** Workstream 0.A of the go-live plan — prove the redirect map and internal
links on the live deploy *before* DNS cutover. Cutover-day steps (Workstream 0.B)
and post-cutover watch (0.C) remain owner-present tasks; see `MIGRATION.md`.

## Summary

| Check | Result | Detail |
| --- | --- | --- |
| Redirect crawl (all 96 rows of `redirects.csv`) | **PASS — 96/96** | after forcing 2 shadowed rules; see below |
| Internal spider from `/` (pages, images, CSS, JS) | **PASS — 95 URLs, 19 pages, 0 dead** | includes new trade.html + client logos |
| Mixed content (`http://` subresources) | **PASS — none** | |
| Netlify Forms registration | **ATTENTION** | form detection **not enabled** on the project |

Deploy verified `ready` (deploy `6a5fd80c96056d0008cb3460`, commit `0a7bc25`).

## 1. Redirect crawl — 96/96 required

Method: for every row of `redirects.csv`, request `https://dcantiques.netlify.app<old_path>`
with redirects disabled and assert (a) first hop is `301`, (b) `Location` equals the
mapped target exactly (fragment included), (c) the target itself answers `200`.
Wildcard rows are probed with a representative path (`/projects/some-legacy-page-xyz` etc.).

- **First run (pre-fix): 94/96.** Two rows served `200` directly instead of
  redirecting, because non-forced Netlify rules lose to file/extension matches:
  - `/index.html` — shadowed by the deployed file
  - `/projects` — resolved by Netlify's extension matching to `projects.html`
- **Fix:** forced both rules with `!` in `_redirects`
  (commit `2c8f9de`, "Force /index.html and /projects redirects").
- **Re-run (post-fix): 96/96 PASS.** Every old page and image URL answers
  `301 → 200` at exactly the mapped target, wildcards included.

## 2. Internal spider — zero 404s required

Method: breadth-first crawl from `/`, following every internal `href`/`src`/`srcset`/
`poster`, `og:image`/meta URLs, and `url()` references inside `main.css`. Netlify's
Pretty-URLs optimization rewrites internal links to extensionless paths (`/about`),
which the spider treats as pages.

- **Run 1 (before Workstream 1 landed): 77 URLs checked (18 pages) — 0 bad, 0 mixed content.**
- **Run 2 (after Workstream 1 landed): 95 URLs checked (19 pages) — 0 bad, 0 mixed
  content.** The extra URLs are `trade.html` and the 17 client logo files;
  `newsletter/issue-01.html` is intentionally unlinked and `noindex`, so the
  spider does not reach it (checked by hand: `200`).

## 3. Netlify Forms — read-only status check

Queried the Netlify API (project reader) on 2026-07-21:

- Project `dcantiques` reports **`forms: "not enabled"`**, and the forms list for
  the site is **empty** — neither the `estimate` form nor the `newsletter` form is
  registered.
- Consequence: submissions to the estimate form and the footer newsletter form
  are currently **not collected** on the live deploy.
- **Action required (owner / dashboard):** enable form detection under
  *Project configuration → Forms* in the Netlify dashboard, then trigger a
  redeploy, then submit one test through the estimate form (with photo) and one
  through the newsletter form and confirm both appear under *Forms* and the
  estimate lands on `/thanks.html` (plan step 0.A.3). This is a project-settings
  change, so it was deliberately not made from this session.

## 4. Fonts / analytics

Pages load Google Fonts (`fonts.googleapis.com`) and gtag (`AW-1036488597`) from
`<head>` boilerplate on every page; local browser QA showed no console errors on
the touched pages. Full live-console verification is part of the cutover-day
checklist once the real domain is serving.

## Notes

- `redirects.csv` remains the documentation of record for the map; `_redirects`
  now carries `301!` on the two shadowed rows. `.htaccess` (Apache fallback) is
  unchanged — it does not have the shadowing problem.
- Re-run this entire proof against `https://www.refinishing.org` immediately
  after DNS cutover (plan 0.B.3) — the real domain is the only test that counts.
