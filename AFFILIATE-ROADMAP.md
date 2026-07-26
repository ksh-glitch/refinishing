# Affiliate & product-revenue roadmap

Owner goal (2026-07-26): grow affiliate income from the current ~$15–30/year
into a real secondary revenue line, **without** turning refinishing.org into a
DIY content farm or diluting the restoration positioning. Amazon is not
required — better programs are listed below.

Decided and closed: **the for-sale antique inventory is not being revived.**
The `/store/* → /` redirect stays as-is.

---

## 1. The economics, stated plainly

Amazon pays **3%** on furniture, tools and home-improvement products (cut from
8% in April 2020, never restored). The recommended items are $10–25, so each
sale earns roughly **$0.45–0.75**.

| Target/yr | Sales needed | Product-intent pageviews/yr* |
| --- | --- | --- |
| $30 (today) | ~50 | ~12,000 |
| $500 | ~900 | ~200,000 |
| $2,000 | ~3,600 | ~800,000 |

\* assuming ~8% click-through to the merchant and ~5% conversion.

**Implication:** Amazon alone cannot become material at this site's traffic
without a national DIY audience — the exact audience the site filters out.
Growth has to come from *higher commission per sale* and *higher-intent
placement*, not from chasing volume.

---

## 2. The rule that keeps this on-brand

> **Care and protection content = yes. DIY restoration content = no.**

Someone buying a $19 polish because a restorer told them to owns furniture
worth protecting, and is a plausible future client. Someone learning to strip
a dresser is neither. Every piece below must pass that test.

Corollary: the "what NOT to buy" section carries no affiliate links and never
should. It is the reason the recommendations are believable.

---

## 3. Done (2026-07-26)

- `/furniture-care-kit.html` — the anchor page. Four real products, honest
  usage notes, a no-affiliate "keep away from a fine finish" section, and a
  "when to stop and call" section that routes valuable pieces to the form.
- Disclosure moved **above** the first affiliate link (FTC guidance).
- All affiliate links consolidated onto that one page; the care guide is
  editorial again.
- `rel="sponsored nofollow noopener"` on every monetized link.
- GA4 `affiliate_click` event with `product` and `page` parameters.

---

## 4. Next: better programs than Amazon

Amazon's 3% is the floor, not the ceiling. Worth applying to, in rough order
of fit. **All rates below must be verified at signup — do not publish or plan
against them until confirmed.**

| Program | Why it fits | Typical commission | Notes |
| --- | --- | --- | --- |
| **Mohawk / RPM finishing** | Already the products we recommend | Trade/dealer pricing rather than affiliate | Better as a **dealer margin** play than an affiliate one — see §5 |
| **Rockler** | Woodworking + finishing supplies, affluent hobbyist | typically high single digits | Has a real affiliate program |
| **Woodcraft** | Same category, strong brand | typically high single digits | |
| **Highland Woodworking** | Finishing specialists, French polish supplies | mid single digits | Niche but exactly our topic |
| **Lee Valley / Veritas** | Premium tools, design-conscious buyers | varies | Audience overlaps our client profile |
| **Wayfair / Perigold** | Perigold is the luxury tier — furniture care, protection | low single digits | Perigold buyers match our client profile |
| **Chairish / 1stDibs** | Antique marketplaces — our audience literally shops here | varies, can be meaningful per sale | **Highest ticket per conversion of anything on this list** |

**The strategic point:** one Chairish/1stDibs/Perigold conversion can be worth
more than a hundred Amazon polish sales. High-ticket antique marketplaces are
the natural fit for an audience that owns and buys good furniture.

---

## 5. Higher-value alternatives to affiliate entirely

1. **Sell the products directly.** Mohawk is a trade line; a restoration shop
   can buy at dealer pricing. Selling a care kit at retail is a 30–50% margin
   instead of 3%, on the same recommendation, to the same people — and every
   restored piece that leaves the shop is a natural point of sale.
2. **A branded care kit.** The shop's own polish/cloth/marker set, handed to
   every client at delivery and sold on the site. Highest margin, strongest
   brand fit, real work to set up.
3. **YouTube.** The channel already has workshop footage. Product links in
   descriptions convert better than text links, a video earns for years, and
   restoration content has a genuine audience there — without putting DIY
   content on refinishing.org. Ad revenue unlocks at 1,000 subscribers and
   4,000 watch hours.

---

## 6. Content pipeline (one or two a month)

Each piece is problem-first, ends at a product or the kit page, and is judged
on whether it brings in owners of good furniture — not on raw traffic.

1. **Put down the Pledge** — silicone polishes and why restorers hate them
   *(strongest hook; partly written in the care guide already)*
2. **White rings and heat blush** — what to try before calling anyone
3. **Humidity and your antiques** — DMV summers, cracked veneer, hygrometers
4. **Sun damage** — UV film, placement, what fading actually costs
5. **Moving furniture without wrecking it** — pads, felt, straps
6. **Leather care for antique seating**
7. **Cleaning brass and hardware** without stripping patina
8. **Winter heating and joint shrinkage** (seasonal, Nov–Jan)
9. **Protecting a table through the holidays** (seasonal, Nov)

---

## 7. Measurement

`affiliate_click` fires with `product` and `page`. After one quarter of live
data (post-cutover), review:

- clicks per product → drop what nobody clicks
- clicks per source page → write more of what works
- **assessment-form submissions from care-content sessions** — the real
  question is whether this content also produces restoration clients. If it
  does, it earns its place regardless of commission.

---

## 8. Gates

- Nothing here earns anything until **domain cutover** — the site currently
  serves `x-robots-tag: noindex` and cannot rank or be cited.
- Do not publish commission rates or program claims from this document
  without verifying them at signup.
- Amazon Associates requires the disclosure to remain present and prominent;
  keep it above the links on any new page.
