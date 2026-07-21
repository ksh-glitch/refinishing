# The Workshop Letter — sending guide

Occasional email newsletter for Antiques & Furniture Restoration Inc.
Issues live in this folder as email-safe HTML (`issue-01.html`, `issue-02.html`, …).

## Where the subscribers are

Sign-ups come from the footer form on every page (`<form name="newsletter">`,
a Netlify Form). To get the list:

1. Netlify dashboard → **dcantiques** project → **Forms** → **newsletter**.
2. Export submissions as CSV; the `email` column is the list.
3. De-duplicate and remove anyone who has replied "unsubscribe."

**Note (July 2026):** form detection is currently *not enabled* on the
dcantiques project — enable it under Project configuration → Forms, then
redeploy, or submissions will not be collected. Any Weebly-era subscriber
export from the old site should be merged into the same list (owner has it).

## How an issue is built

- Email-safe rules: everything inline-styled, tables for layout, 600 px wide,
  Georgia font stack, no webfonts, no JavaScript, no external CSS.
- Palette (matches the site): Gesso `#f5f0e6` ground · Walnut ink `#2a211b` ·
  Garnet `#8c3b2e` accent · Brass `#a98352` hairlines · Vellum `#ede4d3` panels.
- Images must use **absolute URLs** (`https://www.refinishing.org/assets/img/...`)
  — relative paths break in email clients. Use the `.jpg` copies, not `.webp`
  (broader client support). These URLs only resolve once DNS points
  www.refinishing.org at the new Netlify site — don't send an issue before
  cutover (or temporarily swap in `https://dcantiques.netlify.app/...`).
- Every issue: a short letter-from-the-bench intro, one real project story,
  one care tip, and the free-estimate CTA. Never invent facts or prices;
  "free" applies to estimates only (delivery is quoted with the estimate).
- Keep `<meta name="robots" content="noindex, nofollow">` in the head — these
  pages are served on the site but must stay out of search and out of
  `sitemap.xml`.

## How to send

There is no ESP wired up yet — sending is manual:

1. Open the issue file locally in a browser, select-all, and copy — or paste
   the raw HTML into a client/ESP that accepts HTML source (recommended).
2. Send **To:** info@refinishing.org, **Bcc:** the subscriber list
   (Bcc protects subscribers' addresses).
3. Subject line pattern: `The Workshop Letter · No. 1 — <lead story>`.
4. Send yourself a test first; check both light and dark mode, and that both
   Federal images load.
5. Honor unsubscribes immediately (they arrive as replies).

If volume grows, move the list into a proper ESP (Buttondown, Mailchimp, etc.)
and paste each issue's HTML as a raw-HTML campaign — the files here are
already compatible.
