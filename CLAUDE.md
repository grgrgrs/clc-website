# CLC website

Website for Concerned Letcher Countians (CLC), a volunteer group in Letcher County, Kentucky, opposing the proposed federal prison (FCI Letcher). It replaces the old Weebly site at concernedletchercountians.org. That site stays live until launch: never modify it.

## Stack
- Astro 7, static output only. No React, no Tailwind, no CMS, no database.
- Plain CSS in `src/styles/site.css`. Design tokens (colours, fonts) are at the top. Fonts are self-hosted through `@fontsource` packages.
- The only client-side JavaScript is the search/sort on the News page. Every page must work without JavaScript.

## Commands
```sh
npm install
npm run dev       # local dev server (http://localhost:4321)
npm run build     # static site -> dist/
npm run preview   # serve dist/ locally
```
Always run `npm run build` after content changes. The content schemas in `src/content.config.ts` fail the build on bad data, and that's intended.

## Where things live
| What | Where |
|---|---|
| News items | `src/content/news/<slug>.md`, one file per item |
| Page text (home intro, "proposed prison", status box, why we oppose, letter, about) | `src/content/text/*.md` |
| "Where things stand" box on the home page | `src/content/text/status.md`. Update the `updated:` date whenever the text changes |
| Videos | `src/content/videos.yaml` |
| Org name, address, email, nav, social links | `src/site.ts` |
| Page templates | `src/pages/` (one file = one URL), shared shell in `src/layouts/Base.astro` |
| Images and PDFs | `public/images/`, `public/docs/`. Use lowercase-hyphenated file names |
| Old Weebly URLs | `public/*.html` (meta-refresh fallbacks); real 301 rules in `deploy/` |
| Host-specific config | `wrangler.jsonc` (Cloudflare, must be at the repo root); alternatives in `deploy/` |

## Adding a news item
Create `src/content/news/YYYY-MM-DD-short-name.md` (use `undated-short-name.md` if the date is unknown):

```md
---
title: "Headline as published"
date: 2026-10-10
source: "Publication or author"
url: "https://example.com/article"
section: fci-letcher          # or further-reading
summary: "Optional one line."
image: "/images/news/2026-10-10-short-name.jpg"   # optional
image_alt: "What the image shows"                  # required if image is set
---
```
- For CLC's own post, leave out `url` and write the post below the frontmatter. It gets its own page at `/news/<slug>/`.
- To hide an item without deleting it, add `draft: true`.
- When a link breaks, set `link_status: dead`, `link_checked: <date>` and `link_note: "Page not found."`. Keep the original `url`: George wants dead links kept for reference.
- The file name is the item's permanent id. Don't rename existing files.

## Rules
- `src/content/text/letter-to-bop-2024.md` is a historical document. Reproduce it verbatim and never correct its text.
- Neighbors' quotes in `about.md` are reproduced as written.
- Don't invent facts about the prison project's status. The status box text comes from CLC.
- `original_source_url` records where migrated content came from on the old site. Keep it.
- The domain's email (MX) is hosted at GreenGeeks. Any DNS change at launch must preserve it.

## Deploying
- Hosted on Cloudflare Workers (Workers Builds). Config: `wrangler.jsonc` (keep its `"previews": {}` block).
- **Pushing to `main` deploys production** (https://clc-website.george-172.workers.dev). Don't push to `main` unless the change is approved.
- Proposed changes go on a short-named branch. Each push gets a preview at `https://<branch-with-/-as-->-clc-website.george-172.workers.dev`.
- Check a deployment with `/build.json` (`commit`, `branch`).
- Full verified behavior and the publish flow: `docs/deployment.md`.

## Background docs
- `docs/deployment.md`: production/preview behavior on Cloudflare (verified)
- `docs/phase1-review.md`: review of Borgart and the old site, plus architecture decisions
- `docs/content-plan.md`: site map, redirects, open questions for CLC
- `design/design-proposal.md` and `design/mockup/`: the approved design direction (the mockup is reference only)
- `_original-site-snapshot-2026-10-10/`: raw HTML and assets of the old site (not deployed)
- `migration/`: one-time scripts used to move content off Weebly
