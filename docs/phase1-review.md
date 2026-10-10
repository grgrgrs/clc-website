# CLC Website Rebuild — Phase 1 Review

Date: 2026-10-10. Evidence: the local `borgart-site` repo, plus a read-only crawl of concernedletchercountians.org (the raw HTML and assets are in `_original-site-snapshot-2026-10-10/`).

Labels used below: **[O]** = observed directly, **[I]** = inferred, **[R]** = recommendation.

---

## 1. What Borgart is technically

The source is at `C:\Users\georg\Documents\Projects\borgart-site`. Its remote is github.com/grgrgrs/borgart-site, and the last commit was 2026-09-01. [O]

| Aspect | Finding |
|---|---|
| Stack | Astro 4.16 static site generator, with Tailwind 3 (and its typography plugin) and React 19 [O] |
| Output | Fully static HTML written to `dist/`. There is no server code and no database [O] |
| Structure | `src/pages/*.astro` holds 19 pages, one file per route. `src/layouts/BaseLayout.astro` holds the head/SEO, header nav, and footer. `src/components/` holds Hero, Section, CTA and servicecard.jsx. `src/styles/global.css` holds CSS custom-property tokens and a few shared classes [O] |
| Content representation | Content is hand-written HTML inside each `.astro` page. There are no content collections, no Markdown, and no data files. Announcements (for example the class promo) are hard-coded blocks in `index.astro` [O] |
| Styling | Tailwind utilities, combined with many inline `style="color: var(--…)"` attributes and arbitrary values like `text-[0.82rem]` [O] |
| Assets | Assets sit loose in `public/`. Some filenames contain spaces (`AI Knows Business 1080x1080.png`), and there is also a `.mov` and a `.xcf` source file. Brand marks are in `public/images/brand/` [O] |
| Commands | `npm run dev`, `npm run build`, `npm run preview` [O] |
| Deployment | A push to `main` triggers a GitHub Action that runs `flyctl deploy`. That uses a Dockerfile: a Node 18 build stage, then nginx:alpine serving `dist/` on Fly.io [O] |
| Claude guidance | A short `CLAUDE.md` describing the stack, commands and conventions. `docs/borgart-llc-context.md` holds business context [O] |

Things in Borgart that are not obvious from the live site:
- Only 6 of the 19 pages are linked from the nav. The rest (for example `/process`, `/work`, `/vr`, `/reviews`) are still built and deployed [O].
- `Hero`, `Section` and `CTA` use dark-theme colours that don't match the current light design [O]. I infer they are leftovers from an earlier design [I].
- `src/scripts/theme.js` (the dark-mode toggle) isn't imported anywhere [O].
- React is used for exactly one component, on a page that isn't in the nav [O].
- The nginx config uses `try_files … /index.html`. As a result, any bad URL returns the home page with status 200 instead of a 404 page [O].
- The `CLAUDE.md` description ("independent reviewer of AI companion devices…") is out of date compared with the current site [O].

## 2. What to carry into CLC from Borgart [R]

**Carry over:**
- A static site generator that produces plain HTML/CSS. There's no CMS, no database and no server runtime.
- A single shared layout for the head, nav and footer.
- One file per page.
- Git as the history, the rollback mechanism and the audit trail.
- A short `CLAUDE.md` that tells Claude the conventions and commands.
- The three-command workflow: `dev`, `build`, `preview`.
- CSS custom-property design tokens.
- An external form service (Formspree or similar) instead of server code.
- Astro itself, because you already know its workflow and it handles structured content well. See the alternatives in section 4.

**Don't carry over:**
- Content embedded in page markup. News and other repeatable items should be data files.
- Pervasive inline styles and arbitrary Tailwind values. Plain CSS with semantic class names is easier to change safely.
- React, and probably Tailwind as well. Neither is needed for a site this size.
- Unused components and scripts, and pages that are deployed but orphaned.
- The Docker/Fly coupling and the soft-404 nginx fallback.
- Loose asset naming (spaces, source files such as `.xcf` and `.mov` in `public/`).
- Borgart branding, fonts, palette and copy.

## 3. Current CLC site — inventory and assessment

### Platform [O unless marked]
- The site is built with Weebly's "Birdseye" theme through a GreenGeeks reseller, and it publishes static files to GreenGeeks shared hosting. The site files are on GreenGeeks: 65.60.38.74, nameservers ns1/ns2.greengeeks.net.
- The domain's email (its MX record) also points at GreenGeeks. **This matters whenever DNS moves** [I].
- The last publish was about 2026-05-02 (from the Last-Modified header).
- HTTPS works with HSTS. `www` redirects to the apex domain.
- Plain `http://` is *not* redirected to `https://`.
- GA4 tag `G-94G1NKBWGF` appears on 5 of the 11 pages.
- There's no sitemap and no blog.

### Nav and pages (11 live pages)
```
Home (/index.html)                         ~160 words: hero H2 + 1 paragraph
News (/news.html)                          ~2 featured image-links + ~25 external article links (Nov 2022 – Jul 2025)
Videos (/videos.html)                      6 YouTube embeds, no text
CLC COMMENTS (dead label → empty page /clc-comments.html)
  └ CLC Talking Points                     16 points; headline "comments due Mon Aug 12" (2024 FEIS — expired)
About (/about.html)                        4-sentence mission, 8-photo gallery, Weebly map
Survey (/survey.html)                      Weebly survey form + petition PDF (2023)
Contact (/contact.html)                    PO Box 166 Blackey KY 41804, info@…, mailing-list form
More! (dead label → empty page /more.html)
  └ Find out what your neighbors are saying 7 anonymous resident quotes
Our Letter to the BOP                      ~2,100-word FEIS comment letter, ~Aug 2024, 15 reasons
```

### Global content
- No logo, and the site title area is blank.
- The page title and `og:site_name` are wrongly set to "IN THE NEWS".
- The footer contains only "© 2023 Concerned Letcher Countians, LLC".
- There are no social links, no donate button, and no volunteer or join path.

### Media and documents
- **Videos:** 6 videos from youtube.com/@ConcernedLetcherCountians:
  - Trail Towns Not Jail Towns
  - Prison Jobs?
  - Prison Employee and Inmate Suicide Rates
  - Whose money…
  - Amelia Kirby EIS hearing
  - Lydia Pelot Hobbs EIS hearing
- **PDFs:** both are self-hosted and both currently work.
  - Artie Ann Bates' Mountain Eagle letter (May 2023)
  - The petition form (May 2023)
- **Images:** 18 uploads.
  - Of these, 3 are byte-identical copies of the theme's stock "blue smoke" banner.
  - CLC-specific images: the billboard hero, the "NO NEW LETCHER PRISON" X graphic, 8 About-gallery photos (mostly credited to Artie Ann Bates; one from sierraclub.org), and 2 news thumbnails with headlines baked into the image.
  - Alt text is mostly missing or just says "Picture".

### Problems found
- **Expired:**
  - The Talking Points deadline (Aug 12, 2024).
  - The BOP letter, which is now historical.
  - The 2023 survey and petition (the survey still offers "Seed Time" as a source).
  - The 2023 footer.
  - News has had nothing new since July 2025.
  - The site does not say what the project's current status is.
- **Broken outbound links (confirmed):**
  - socialjusticejournal.org (the home page's only link)
  - proposed-fci-letchercountyky.com, both links: the official FEIS/DEIS site is gone
  - nonewletcherprison.com: the domain no longer resolves
  - Ohio Valley ReSource
  - Sen. Warren's report
  - investappalachia, which now redirects elsewhere
  - Inconclusive because the sites block bots: kentucky.com, thehill.com, nytimes, wsj, and oregonbusiness.
- **Structural:**
  - Two empty nav-parent pages, each with only one child.
  - Inconsistent nav labels.
  - The home page has no calls to action and no pointers to news or videos.
  - The email address isn't a clickable link.
- **Duplication:**
  - The 16 talking points largely duplicate the letter's 15 reasons.
  - The cost is given as both $505M and $506M.
  - The same WSJ link appears twice.
- **Survey form defects:**
  - A required dummy "Select One: Option 1/2/3" field.
  - "incaracerated" is misspelled.
- **Typos:** "Lecher", "Roxanna" vs "Roxana", "Hugh Hurtwitz", and FEIS mislabelled as "(DEIS)".

### Hard to migrate automatically
- **Forms:** past survey responses and the mailing-list subscribers sit in the Weebly/GreenGeeks dashboard. You'll need to export them by hand. The forms also need a new backend.
- **Gallery lightbox and map widget:** these get rebuilt simply.
- **Text baked into images:** needs alt text, or a rebuild in HTML.
- **Weebly markup:** the `<font>` tags, multi-column tables, zero-width spaces, and numbered lists written as paragraphs all need cleanup. The text itself is all in static HTML, so extraction is easy.

## 4. Recommended architecture [R]

```
clc-website/
  CLAUDE.md                  conventions + "how to add a news item"
  package.json               astro only (no React/Tailwind)
  astro.config.mjs
  src/
    content.config.ts        schema for news/videos/documents (validated at build)
    content/
      news/2025-07-23-appvoices-updates.md   ← one file per item, frontmatter + optional body
      videos.yaml            list of YouTube IDs/titles
      documents.yaml         PDFs with title/date/description
    data/site.yaml           org name, address, email, nav, footer, social links
    layouts/Base.astro       head/SEO, nav, footer (reads site.yaml)
    components/              only a handful: NewsList, VideoEmbed, Figure
    pages/                   index, news/, videos, about, contact, … (prose in Markdown where possible)
    styles/site.css          one plain stylesheet with tokens
  public/
    images/, docs/           kebab-case filenames
  deploy/                    host-specific config, isolated (e.g. _redirects, .htaccess)
  _original-site-snapshot-2026-10-10/   crawl evidence (not deployed)
```

**News items** use one Markdown file each. The frontmatter is:
- `title`, `date`, `source` (publication), `url` (external link, optional), `summary`, `draft: true|false`, and `original_source_url` (where it came from on the Weebly site).

Astro checks the schema at build time, so a malformed item fails loudly instead of silently breaking a page. This also maps directly onto the future BorgPost operations:

| BorgPost operation | How it would work |
|---|---|
| Create | Add a file |
| Update | Edit the file |
| Remove | Delete the file, or set `draft` |
| Stage | Open a branch or PR |
| Preview | A preview build or deploy |
| Publish | Merge to main |
| Verify | A build stamp (for example `/build.json` with the commit hash) that can be fetched from the live site |

None of this gets built now.

**Hosting assumptions:**
- `npm run build` produces a plain `dist/` folder of static files.
- That folder can go to Netlify, Cloudflare Pages, GitHub Pages, Fly/nginx, or be uploaded to GreenGeeks cPanel.
- Host-specific files (redirects, headers, deploy workflow) live in `deploy/`, so the site doesn't depend on any one host.
- Old `.html` URLs get 301 redirects to the new paths, for example `/news.html` → `/news/`.
- **DNS caution:** moving the site must not disturb the domain's email records at GreenGeeks.

**Forms:** a hosted form service. Formspree is already used for Borgart; Netlify Forms is an option if you choose Netlify. Alternatively, a Google Form link would avoid a form backend entirely.

**Decisions I'd like you to confirm** (I haven't made any of them yet):
1. **Astro (current version 5.x) versus something lighter.** Eleventy is a bit simpler, and plain hand-written HTML would have no build step at all but would make news-list maintenance worse. I recommend Astro because it matches Borgart and has strong content schemas.
2. **No Tailwind, and plain CSS.** I recommend this.
3. **Whether the survey and mailing list continue.** If so, which service handles them.
4. **A git repo for the project.** I recommend a new GitHub repo. Borgart already lives on GitHub (github.com/grgrgrs/borgart-site), so this matches.

## 5. Content inventory for your review

Mark each item KEEP / CHANGE / COMBINE / REMOVE / UNSURE.

| # | Item | Source | Notes / my suggestion |
|---|---|---|---|
| P1 | Home: hero mission statement | /index.html | Core message. Needs a status update (is the prison still "proposed"?) |
| P2 | Home: "prison on strip-mine site / few jobs / $505M / fifth federal prison" paragraph | /index.html | Its only link is dead. Settle on $505M vs $506M |
| P3 | Home: billboard hero photo | /index.html | Strong local image; the text in it is baked into the photo |
| N1 | News: 2 featured image-links (Herald-Leader Hal Rogers op-ed; Vera Institute) | /news.html | Convert to normal news items with real text |
| N2 | News: ~15 "On FCI Letcher" links (2022–2025) | /news.html | Each becomes a news file. Drop or archive the dead ones (see N4) |
| N3 | News: ~10 "Related news" links (prisons, climate, etc.) | /news.html | Generic and older. Candidate to remove, or move to a "Further reading" list |
| N4 | Dead links: official FCI site (FEIS/DEIS), nonewletcherprison.com, Ohio Valley ReSource, Warren report, Social Justice Journal | various | Remove, or replace with Wayback Machine links |
| N5 | Mountain Eagle letter PDF (A. A. Bates, May 2023) | /news.html | Self-hosted; easy to keep |
| V1 | 6 YouTube videos | /videos.html | Easy to keep. Add titles and short descriptions |
| T1 | Talking Points (16 points) | /clc-talking-points.html | The Aug 2024 deadline has passed. Could become an evergreen "Why we oppose FCI Letcher" page |
| T2 | Letter to the BOP (FEIS comment, ~Aug 2024) | /our-letter-to-the-bop.html | Overlaps T1. Keep as a dated historical document, combine with T1, or remove |
| T3 | "NO NEW LETCHER PRISON" X graphic | /clc-talking-points.html | Possibly a de facto logo |
| Q1 | Neighbors' quotes (7) | /find-out-what-…html | Could become a section on Home or About |
| A1 | About: mission paragraph | /about.html | Thin. Expand? |
| A2 | About: 8-photo gallery (Artie Ann Bates photos; one from sierraclub.org) | /about.html | Rights are unclear for the Sierra Club image |
| A3 | About: Letcher County map | /about.html | Replace with a simple embed, or remove |
| S1 | Survey form | /survey.html | 2023-era and has defects. Remove, revise, or replace with a Google Form? |
| S2 | Petition PDF (May 2023) | /survey.html | Probably obsolete |
| C1 | Contact: PO Box, email, "nonprofit LLC" line | /contact.html | Keep. Put it in a global footer too |
| C2 | Mailing-list signup form | /contact.html | Keep? Needs a new service, and the existing list must be exported |
| G1 | Empty pages "CLC COMMENTS" and "More!" | nav | Remove |
| G2 | Stock blue-smoke / flag / sunrise banners | several | Remove or replace with local photos |
| G3 | Footer "© 2023 …" | global | Replace with a proper footer |
| X1 | *New, not on the current site:* project status / latest update | — | Recommended. The site's biggest current gap |
| X2 | *New:* YouTube channel link (and any other social accounts) | — | The channel exists, but the site never links to it |
| X3 | *New:* "Get involved" or donate path | — | Only if CLC wants one |

---

## Decisions (2026-10-10)

1. Framework: Astro (current major version) — **agreed**.
2. Styling: plain CSS, no Tailwind, no React — **agreed**.
3. Forms (survey / mailing list): **TBD**.
4. Version control: new GitHub repo — **agreed** (not yet created).
5. Content inventory (section 5): **awaiting George's KEEP/CHANGE/COMBINE/REMOVE/UNSURE marks**. No migration or build work until then.
