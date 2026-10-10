import { getCollection, type CollectionEntry } from "astro:content";

type Item = CollectionEntry<"news">;

// Newest first; undated items go last, in file-name order.
export function byDateDesc(a: Item, b: Item) {
  const da = a.data.date?.getTime() ?? -Infinity;
  const db = b.data.date?.getTime() ?? -Infinity;
  if (da !== db) return db - da;
  return a.id.localeCompare(b.id);
}

export async function getNews() {
  const all = (await getCollection("news", (e) => !e.data.draft)).sort(byDateDesc);
  return {
    main: all.filter((e) => e.data.section === "fci-letcher" && e.data.link_status === "ok"),
    further: all.filter((e) => e.data.section === "further-reading" && e.data.link_status === "ok"),
    dead: all.filter((e) => e.data.link_status === "dead"),
  };
}
