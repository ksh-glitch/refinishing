# Antiques & Furniture Restoration Inc — refinishing.org redesign

A complete, hand-built static redesign of https://www.refinishing.org/ ("Catalogue Raisonné" design direction: the site as a privately printed catalog of 35 years of restored heirlooms).

## Pages

- `index.html` — home, with the draggable before/after "seam" hero
- `refinishing.html` — furniture refinishing & antique restoration (flagship)
- `upholstery.html` — fine upholstery
- `doors.html` — exterior door restoration
- `projects.html` — case studies (Federal Collection, secretary, lowboy…)
- `gallery.html` — filterable archive with the three-step showcase & lightbox
- `about.html` — story, clients, The Ledger (testimonials), FAQs, visit
- `estimate.html` — free estimate form + contact

## Stack

Pure static HTML/CSS/JS — no frameworks, no build step. Shared styles in
`assets/css/main.css` (design tokens at the top), behaviors in `assets/js/main.js`
(seam slider, lightbox, filters, reveals — all progressive enhancement).
Fonts: Fraunces, Source Serif 4, Archivo via Google Fonts.

## Run locally

```
python3 -m http.server 8734
```

## Imagery

- `assets/img/gallery/` — **real client-work photographs** carried over from the
  existing site (before / stripped / after sets).
- `assets/img/gen/` — AI-generated editorial photography (hero, service cards,
  workshop) used as stand-ins for a future commissioned shoot. Replace with real
  photography when available; art direction notes: warm 3400–3800K, raking
  window light, hands at work, damage photographed with dignity.

## Deploying

Any static host works. The estimate form is marked up for Netlify Forms
(`data-netlify="true"`); on other hosts, wire the form or rely on the
`estimates@refinishing.org` email path. `robots.txt` + `sitemap.xml` included;
canonical URLs point at https://www.refinishing.org/.
