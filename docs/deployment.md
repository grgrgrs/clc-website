# Deployment: production and preview behavior

Verified end to end on 2026-10-10 (UTC 2026-10-11) with the throwaway branch `test/cloudflare-preview`, since deleted. Anything not verified is marked **[unverified]**.

## Hosting
- **Host:** Cloudflare Workers, using Workers Builds connected to GitHub `grgrgrs/clc-website`.
- **Static assets only:** there is no Worker script. `wrangler.jsonc` at the repo root serves `./dist`.
- **Production URL:** https://clc-website.george-172.workers.dev
- **No custom domain yet.** DNS for concernedletchercountians.org still points at the old GreenGeeks/Weebly site. The domain's email (MX) is at GreenGeeks and must be preserved when DNS moves.

## What happens on push

| Push to | Cloudflare runs | Result |
|---|---|---|
| `main` | `npm clean-install` → `npm run build` → `npx wrangler deploy` | Production updated |
| any other branch | `npm clean-install` → `npm run build` → `npx wrangler preview` | A preview for that branch is created or updated. Production is untouched |

- **Wrangler version:** pinned in `devDependencies` (4.149.0), so `npx wrangler` uses that version, not whatever is newest.
- **`wrangler preview` is an open-beta Cloudflare command.** It requires the `"previews": {}` block in `wrangler.jsonc`. Without that block, branch builds fail; that's what happened in the first test.
- **Build environment:** Node 24, with npm reading `package-lock.json`.
- **Build commands:** set in the Cloudflare dashboard (Workers & Pages → clc-website → Settings → Build), not in the repo.

## Preview URLs
- **Pattern:** `https://<preview-name>-clc-website.george-172.workers.dev`
- **Naming:** `<preview-name>` is the git branch name with `/` replaced by `-`. Example: branch `test/cloudflare-preview` → `https://test-cloudflare-preview-clc-website.george-172.workers.dev`.
- **Stable per branch:** later pushes to the same branch update the same URL. This was verified across three pushes.
- **Not indexed:** previews send `X-Robots-Tag: noindex`, so search engines skip them.
- **Branch names:** keep them short, about 50 characters or fewer. The preview name plus `-clc-website` must fit within a 63-character DNS label. **[unverified, inferred from DNS rules]**
- **Previews outlive their branch.** After `test/cloudflare-preview` was deleted, its preview URL still returned the old content. Remove a preview explicitly with `npx wrangler preview delete` (needs Cloudflare auth), or from the dashboard. Whether Cloudflare eventually expires previews is **[unverified]**.

## Build status
- **Where to look:** every build posts a GitHub check run named **"Workers Builds: clc-website"** on the pushed commit.
- **Reading it:** `GET https://api.github.com/repos/grgrgrs/clc-website/commits/<sha>/check-runs`. Wait for `status: completed`, then read `conclusion: success | failure`.
- **What it contains:** the summary links to the Cloudflare build page (production builds also show a Version ID). It does **not** include the preview URL; derive that from the branch name using the pattern above.
- **Build logs:** visible only in the Cloudflare dashboard, which needs a login.
- **Timing:** a typical build finished about 1 to 2 minutes after the push.

## Verifying what's live: `/build.json`
Every deployment serves `/build.json`:

```json
{ "commit": "<full 40-char SHA>", "branch": "main", "built": "<ISO timestamp>" }
```

- **On Cloudflare:** `commit` and `branch` come from `WORKERS_CI_COMMIT_SHA` and `WORKERS_CI_BRANCH`.
- **Locally:** they fall back to git.
- **A change is live** when `/build.json` on the target URL reports the expected commit. Then fetch the changed page and check for the content.

## The publish flow (verified)
1. Create a branch from `main`, commit the change, and push.
2. Wait for the GitHub check run to succeed.
3. Open the preview URL. Confirm its `/build.json` commit matches the branch head, and review the change.
4. If it's approved, merge the branch into `main` and push. The test used `--no-ff`, so there is an explicit merge commit.
5. Wait for the check run on the merge commit. Confirm production's `/build.json` reports that commit with `"branch": "main"`, then confirm the content.
6. Delete the branch, and delete its preview if you want to clean up.

**Evidence from the test:**

| Step | Commit | Result |
|---|---|---|
| Preview | `1fd0eaa` | Showed the test change |
| Production during preview | stayed at `b750688` | Did not show the test change |
| Production after merge | merge commit `b750688` | Reported `branch: main`, and all pages returned 200 |

## Known issues, deferred
- **Unknown URLs don't show the site's `404.html`.** Production returns an empty 404 and previews return plain "Not found", even with `not_found_handling: "404-page"`. This needs investigating.
- **Old Weebly URLs take two hops.** For example, `/news.html` gets a Cloudflare 307 to `/news`, which is the meta-refresh page that sends visitors to `/news/`. They arrive, but not through a permanent 301. The likely fix is to copy `deploy/netlify/_redirects` into `public/`, since Workers static assets honor `_redirects`. **[unverified]**
