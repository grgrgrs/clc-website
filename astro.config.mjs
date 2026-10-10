// @ts-check
import { defineConfig } from "astro/config";

export default defineConfig({
  site: "https://concernedletchercountians.org",
  // Pages are written as /news/index.html, served at /news/.
  trailingSlash: "ignore",
});
