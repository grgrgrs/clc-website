# CLC Design Proposal (draft, 2026-10-10)

Mockup: open `design/mockup/index.html` and `design/mockup/news.html` in a browser. These are static throwaway files, not the real build.

## Idea
CLC already has a visual identity out in the world: the green-and-white **"No Letcher Prison" billboard** and the green **X**. The site borrows from these instead of inventing a new brand.
- The X becomes the logo.
- The billboard photo is the home-page image. It's shown as a photograph with real alt text and no text overlaid on it (P3).
- The footer is a solid green band with **ConcernedLetcherCountians.org** in large white type, echoing the billboard's bottom strip. This is the one bold element. Everything else stays quiet.

## Tokens
| Token | Value | Source / use |
|---|---|---|
| green | `#225345` | the X logo: headings, footer band |
| link green | `#1d6349` | links (about 7:1 contrast on white) |
| ink | `#1d2421` | body text |
| muted | `#535e59` | dates, sources |
| sky | `#eaf2fa` | sky behind the billboard: "Where things stand" box, news search bar |
| ochre | `#8f5418` | autumn hillside: used only for "needs attention" notes (date needed, dead link, placeholder text) and the keyboard focus outline |

**Type:**
- Headings: **Alegreya Sans** (bold, humanist, slightly hand-cut).
- Body: **Literata** (a serif designed for long reading on screens).
- The base size is 18px, larger than usual, because many readers are older.
- In the real build, the fonts are self-hosted so the site makes no Google calls.

## Layout rules
- Content is left-aligned. Text is capped at about 38rem wide so lines stay readable.
- There's no hamburger menu. The six nav links simply wrap on phones, so no JavaScript is needed for navigation.
- There are no cards, no animation, and no full-bleed hero with text on top of a photo.
- The only JavaScript is the News search/sort. Without it, the list still works and shows newest first.
- Items with missing data are marked visibly in ochre ("Date needed"), so gaps get noticed and fixed rather than hidden.

## Open design questions
- Is the X graphic good enough as a logo at small sizes? Its text becomes unreadable below about 80px. A cleaner redraw as SVG (the X shape plus the separate wordmark) would be crisp everywhere.
- Should Home show the billboard photo, or would CLC prefer a landscape without text in it?
