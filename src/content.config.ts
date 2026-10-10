// Content schemas. The build fails if any file doesn't match, which keeps
// hand edits (and future automated edits) from silently breaking a page.
import { defineCollection } from "astro:content";
import { glob, file } from "astro/loaders";
import { z } from "astro/zod";

// One Markdown file per news item: src/content/news/<slug>.md
// The file name (without .md) is the item's permanent id.
const news = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/news" }),
  schema: z
    .object({
      title: z.string(),
      date: z.coerce.date().optional(),            // leave out if unknown; shown as "Date needed"
      source: z.string().optional(),               // publication or author
      url: z.string().optional(),                  // external link or /docs/... file; leave out for CLC's own posts
      section: z.enum(["fci-letcher", "further-reading"]).default("fci-letcher"),
      link_status: z.enum(["ok", "dead"]).default("ok"),
      link_checked: z.coerce.date().optional(),    // when a dead link was last checked
      link_note: z.string().optional(),            // e.g. "Page not found."
      summary: z.string().optional(),
      image: z.string().optional(),                // e.g. /images/news/my-photo.jpg
      image_alt: z.string().optional(),
      draft: z.boolean().default(false),           // true = kept in source, not published
      original_source_url: z.string().optional(),  // where this came from on the old Weebly site
    })
    .refine((d) => !d.image || !!d.image_alt, {
      message: "image_alt is required when image is set",
      path: ["image_alt"],
    }),
});

// Prose pages (home intro, why we oppose, letter, about, status box).
const text = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/text" }),
  schema: z.object({
    title: z.string(),
    updated: z.coerce.date().optional(),
    original_source_url: z.string().optional(),
  }),
});

const videos = defineCollection({
  loader: file("./src/content/videos.yaml"),
  schema: z.object({
    id: z.string(),            // YouTube video id
    order: z.number(),         // display order, 1 = first
    title: z.string(),
    description: z.string().optional(),
  }),
});

export const collections = { news, text, videos };
