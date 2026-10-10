// /build.json: identifies which version of the site is live.
// Lets a person (or a future publishing tool) confirm a change has deployed.
import { execSync } from "node:child_process";

function commit() {
  try {
    return execSync("git rev-parse --short HEAD", { stdio: ["ignore", "pipe", "ignore"] }).toString().trim();
  } catch {
    return "unknown";
  }
}

export function GET() {
  return new Response(JSON.stringify({ commit: commit(), built: new Date().toISOString() }, null, 2), {
    headers: { "Content-Type": "application/json" },
  });
}
