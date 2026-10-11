# Deployment notes

**Current host: Cloudflare Workers (Workers Builds).**
- Pushes to `main` deploy production at https://clc-website.george-172.workers.dev.
- Pushes to any other branch create a preview.
- Config: `/wrangler.jsonc`. Wrangler requires that file at the repo root.
- Full verified behavior: `docs/deployment.md`.

`npm run build` produces `dist/`, a folder of static files, so the site isn't tied to Cloudflare. The other files here are for alternative hosts:

- **Netlify / Cloudflare Pages:** build command `npm run build`, output `dist`. Copy `netlify/_redirects` into `public/` for real 301 redirects from old Weebly URLs.
- **Apache (e.g. GreenGeeks cPanel):** upload the contents of `dist/`. Copy `apache/.htaccess` into `public/` first; it also forces HTTPS, which the old site didn't.
- **Any host:** the `public/*.html` fallback pages redirect old URLs with a meta refresh.

Before pointing DNS anywhere: the domain's email is hosted at GreenGeeks. Keep the MX records.
