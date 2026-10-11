// /build.json: identifies which version of the site is live.
// Lets a person (or a future publishing tool) confirm a change has deployed.
// Cloudflare Workers Builds provides the commit and branch as environment
// variables; local builds fall back to asking git.
import { execSync } from "node:child_process";

function git(args: string) {
  try {
    return execSync(`git ${args}`, { stdio: ["ignore", "pipe", "ignore"] }).toString().trim();
  } catch {
    return "unknown";
  }
}

export function GET() {
  const commit = process.env.WORKERS_CI_COMMIT_SHA || git("rev-parse HEAD");
  const branch = process.env.WORKERS_CI_BRANCH || git("rev-parse --abbrev-ref HEAD");
  return new Response(JSON.stringify({ commit, branch, built: new Date().toISOString() }, null, 2), {
    headers: { "Content-Type": "application/json" },
  });
}
