# Deployment notes

`npm run build` produces `dist/`, a folder of static files. Any static host works. Nothing here is needed for the site itself.

- **Netlify / Cloudflare Pages:** build command `npm run build`, output `dist`. Copy `netlify/_redirects` into `public/` for real 301 redirects from old Weebly URLs.
- **Apache (e.g. GreenGeeks cPanel):** upload the contents of `dist/`. Copy `apache/.htaccess` into `public/` first (it also forces HTTPS, which the old site didn't).
- **Any other host:** the `public/*.html` fallback pages still redirect old URLs (via meta refresh).

Before pointing DNS anywhere: the domain's email is hosted at GreenGeeks. Keep the MX records.

Hosting has not been chosen yet (2026-10-10).
