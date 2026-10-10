# CLC Content Plan

Status: **site map confirmed with adjustments** (2026-10-10). Based on George's marks on the section 5 inventory in `phase1-review.md`.

## Site map

| Page | URL | Contents | Old source |
|---|---|---|---|
| Home | `/` | Mission statement (P1), cleaned-up paragraph (P2), hero photo (P3, fixed), "Current status" box (X1), links into Why We Oppose / News / Videos | /index.html |
| Why We Oppose | `/why-we-oppose/` | The 16 talking points as an evergreen list. The expired deadline is removed and typos are fixed (T1). Links to the letter as history | /clc-talking-points.html |
| Letter to the BOP (2024) | `/why-we-oppose/letter-to-bop-2024/` | The full FEIS comment letter, kept as a historical document. **Text reproduced verbatim**, with no corrections (T2: decided 2026-10-10) | /our-letter-to-the-bop.html |
| News | `/news/` | All article links as one sortable/filterable list, followed by a "Further reading" section (N3) and a "Dead links" section (N4) | /news.html |
| Videos | `/videos/` | 6 YouTube videos with titles, plus a link to the channel (V1, X2) | /videos.html |
| About | `/about/` | Mission paragraph (A1) and neighbors' quotes (Q1). No gallery or map for now (A2, A3) | /about.html, /find-out-what-your-neighbors-are-saying.html |
| Contact | `/contact/` | PO Box, email (clickable), nonprofit/LLC line (C1). Mailing list: TBD (C2) | /contact.html |
| *(later)* Area History | `/history/` | Public-education articles from the historic register research. Kept out of the nav until the first article exists | new |

Global elements:
- Footer: org name, PO Box, email, YouTube link, and "© {current year}" (C1, G3).
- Logo: the "NO NEW LETCHER PRISON" X graphic (T3).

## Removed for now
- Survey form and petition PDF (S1, S2)
- Empty "CLC COMMENTS" / "More!" pages (G1)
- Stock banner images (G2)
- About photo gallery (A2)
- Weebly map (A3)

All of these are kept in `_original-site-snapshot-2026-10-10/`.

## News item representation
One Markdown file per item in `src/content/news/`. The frontmatter is:

```yaml
title: "Updates on Proposed Federal Prison Site in Kentucky"
date: 2025-07-23
source: "Appalachian Voices"
url: "https://appvoices.org/2025/07/23/updates-on-proposed-federal-prison-site-in-kentucky/"
section: fci-letcher        # fci-letcher | further-reading
link_status: ok             # ok | dead  (dead → listed under "Dead links", URL shown for reference)
summary: "Optional one-line description."
image: "/images/news/2025-07-23-appvoices.jpg"   # optional photo/image for any item
image_alt: "Description of the image"           # required whenever image is set
original_source_url: "https://concernedletchercountians.org/news.html"
```

- Any news item may carry an optional image (from George's P3 note). The build fails if an item has an image but no alt text.
- The two former "featured" items (Herald-Leader, Vera) become ordinary items. Their headlines are written out as text instead of being baked into images (N1, N2).
- The Mountain Eagle letter PDF (N5) is an ordinary item whose `url` points to the self-hosted copy at `/docs/`.
- Sorting and filtering (by date, by text) is a small script layered on a plain list. Without JavaScript, the list still shows newest first.
- CLC's own updates can be news items with a body and no external `url`.

## Old URL redirects

| Old URL | New URL |
|---|---|
| /index.html | / |
| /clc-talking-points.html | /why-we-oppose/ |
| /our-letter-to-the-bop.html | /why-we-oppose/letter-to-bop-2024/ |
| /news.html | /news/ |
| /videos.html | /videos/ |
| /about.html | /about/ |
| /find-out-what-your-neighbors-are-saying.html | /about/ |
| /contact.html | /contact/ |
| /survey.html, /clc-comments.html, /more.html | / |

## Open questions (for Artie)
- P2: a replacement source for the "fifth federal prison" claim. The current link is dead.
- Whether the cost is $505M or $506M.
- X1: the current-status text, and who keeps it updated. The site launches with a short example marked "to be updated by CLC".
- X3: whether the site should have a get-involved/donate section.
- Whether to update date-bound talking points (the 2029 opening estimate, the Blackey Bridge closure). The letter itself stays verbatim.
- Photo permissions. The sunrise/dusk/flag banner photos have an unknown source and are **not used**.
- C2/forms: choose a service, and export the current subscribers from the Weebly dashboard.
- X2: which social accounts to create.
