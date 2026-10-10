"""One-time helper (2026-10-10): write one Markdown file per link from the old News page.

Link statuses come from _original-site-snapshot-2026-10-10/linkcheck.txt.
Run from the project root: python migration/make_news.py
"""
import json, os

OLD_NEWS = "https://concernedletchercountians.org/news.html"
OLD_HOME = "https://concernedletchercountians.org/index.html"
CHECKED = "2026-10-10"

# slug, date or None, title, source, url, section, status, extra fields
ITEMS = [
 ("2025-07-27-the-hill-prison-reform-laws", "2025-07-27", "Prison reform laws could safely send thousands home — if they’re enforced", "The Hill",
  "https://thehill.com/opinion/criminal-justice/5420297-criminal-justice-reform-bureau-prisons/", "fci-letcher", "ok", {}),
 ("2025-07-23-appalachian-voices-updates", "2025-07-23", "Updates on proposed federal prison site in Kentucky", "Appalachian Voices",
  "https://appvoices.org/2025/07/23/updates-on-proposed-federal-prison-site-in-kentucky/", "fci-letcher", "ok", {}),
 ("2024-05-05-herald-leader-coal-or-cages", "2024-05-05", "Appalachia deserves more than coal or cages. Another federal prison is not the answer.", "Mandi Fugate Sheffel, Lexington Herald-Leader",
  "https://www.kentucky.com/opinion/op-ed/article287391400.html", "fci-letcher", "ok", {}),
 ("2024-03-13-lpm-environment-economy", "2024-03-13", "Here’s how a new federal prison could impact environment, economy in eastern Kentucky", "Louisville Public Media",
  "https://www.lpm.org/investigate/2024-03-13/heres-how-a-new-federal-prison-could-impact-environment-economy-in-eastern-kentucky", "fci-letcher", "ok", {}),
 ("2023-11-29-kentucky-lantern-fast-track", "2023-11-29", "Study: Kentuckians increasingly excluded from lawmaking process by fast-track maneuvers", "Kentucky Lantern",
  "https://kentuckylantern.com/2023/11/29/study-kentuckians-increasingly-excluded-from-lawmaking-process-by-fast-track-maneuvers/", "fci-letcher", "ok",
  {"_note": "Email-tracking parameters removed from the original link."}),
 ("2023-05-05-herald-leader-bad-idea", "2023-05-05", "Federal prison in Letcher County was bad idea the first time — let’s not revisit it", "Lexington Herald-Leader",
  "https://www.kentucky.com/opinion/op-ed/article275067391.html", "fci-letcher", "ok", {}),
 ("2023-05-05-daily-yonder-prison-cells-over-homes", "2023-05-05", "Building prison cells over homes", "The Daily Yonder",
  "https://dailyyonder.com/building-prison-cells-over-homes-in-central-appalachia/2023/05/05/", "fci-letcher", "ok",
  {"summary": "Video and podcast with Sylvia Ryerson and Judah Schept."}),
 ("2023-05-03-mountain-eagle-bates-letter", "2023-05-03", "Is a federal prison really our best bet?", "Artie Ann Bates, letter to the editor, The Mountain Eagle",
  "/docs/2023-05-03-bates-letter-mountain-eagle.pdf", "fci-letcher", "ok",
  {"summary": "PDF of the letter as published.", "_note": "Originally hosted at /uploads/1/4/5/6/145638394/abates_letter_mtneagle_05032023.pdf"}),
 ("2023-03-29-nyt-flood-relief", "2023-03-29", "Eastern Kentucky needs flood relief, not another prison", "The New York Times",
  "https://www.nytimes.com/2023/03/29/opinion/kentucky-prison-flood.html?unlocked_article_code=HJjfe2Hta1FiuMocyay01PBNntiGOXK9Bex-oIlzJRwDXaKu65nFyrGa2AhR37GQDhCBBIvkEIS1r5DHA_XNtkGmMIqAYJk5OROctuIIMERM3M2tKjVRYu9_6CF5OD33VYemsyviQXRVNC3CRQQeR3uObteugIsT4pMeFrVOXRSpIGwL61xzvXuKPSEdkHb2k322urAh-C0a6rHm4RzXnnSr7W30UqbYY92ejIAP4Bw7StueMblFaYrEjnGfttrXw-cD87B0-NJHPGe7c5PrNq2XDq0_a182chziegOraz4es_ue66wL8DHw8Tysa-90FSWn7m66Z8Lblij_vAhC&smid=url-share",
  "fci-letcher", "ok", {"summary": "“A trauma on top of the trauma.”", "_note": "Old site said March 23, 2023; the URL says 2023/03/29. Using the URL date. The link is a gift link that bypasses the paywall."}),
 ("undated-herald-leader-hal-rogers", None, "Hal Rogers is using political tricks to force an unneeded federal prison in Letcher", "Opinion, Lexington Herald-Leader",
  "https://www.kentucky.com/opinion/op-ed/article290566924.html", "fci-letcher", "ok",
  {"image": "/images/news/herald-leader-hal-rogers.png",
   "image_alt": "Headline and photo from the Herald-Leader article: Letcher Governance Project members hold a banner opposing the prison while Rep. Hal Rogers speaks at a 2016 SOAR summit.",
   "_note": "Was a featured image link at the top of the old News page. Publication date not shown on the old site."}),
 ("undated-vera-toxic-land", None, "Building prisons on toxic land has devastating consequences", "Vera Institute of Justice",
  "https://www.vera.org/news/building-prisons-on-toxic-land-has-devastating-consequences", "fci-letcher", "ok",
  {"_note": "Was a featured image link at the top of the old News page. Publication date not shown on the old site."}),
 ("undated-kypolicy-prison-counties", None, "Three southeastern Kentucky counties already obtained federal prisons, and it did not pay off", "Kentucky Center for Economic Policy",
  "https://kypolicy.org/letcher-county-prison-will-not-help-economy/", "fci-letcher", "ok", {"summary": "Economic analysis."}),
 ("undated-baffler-after-the-flood", None, "After the flood", "Tarence Ray, The Baffler",
  "https://thebaffler.com/latest/after-the-flood-ray", "fci-letcher", "ok", {}),
 # Dead links (George: keep, in a separate section, with the broken link attached for reference)
 ("2024-07-12-bop-final-eis", "2024-07-12", "Final Environmental Impact Statement for proposed Federal Correctional Institution and Prison Camp, Letcher County, KY", "Federal Bureau of Prisons project site",
  "https://www.proposed-fci-letchercountyky.com/reports-studies", "fci-letcher", "dead", {"link_note": "The project site no longer exists."}),
 ("undated-bop-draft-eis", None, "Draft Environmental Impact Statement for proposed development of a new Federal Correctional Institution and Federal Prison Camp, Letcher County, KY", "Federal Bureau of Prisons project site (PDF)",
  "https://www.proposed-fci-letchercountyky.com/_files/ugd/5947b2_6cd3ea7da5044517b0a31a636019012f.pdf", "fci-letcher", "dead", {"link_note": "The project site no longer exists."}),
 ("undated-petition-rescission", None, "Petition for rescission of the $506,000,000 for Letcher prison", "No New Letcher Prison",
  "https://www.nonewletcherprison.com/", "fci-letcher", "dead", {"link_note": "The website address no longer works."}),
 ("2022-11-22-ohio-valley-resource-old-divides", "2022-11-22", "A proposed prison in Letcher County, Ky. reopens old divides", "Ohio Valley ReSource",
  "https://ohiovalleyresource.org/2022/11/22/a-proposed-prison-in-letcher-county-ky-reopens-old-divides/", "fci-letcher", "dead", {"link_note": "Page not found."}),
 ("undated-social-justice-journal-future-in-balance", None, "A future in the balance: the fight against the carceral state in Central Appalachia", "Social Justice Journal",
  "https://socialjusticejournal.org/a-future-in-the-balance-the-fight-against-the-carceral-state-in-central-appalachia/", "further-reading", "dead",
  {"link_note": "Page not found.", "_old": OLD_HOME, "_note": "Was the only link on the old home page (on the words 'fifth federal prison')."}),
 ("undated-warren-revolving-door", None, "Warren leads colleagues investigating the revolving door between federal agencies and the private detention industry", "U.S. Senator Elizabeth Warren",
  "https://www.warren.senate.gov/oversight/reports/warren-leads-colleagues-investigating-the-revolving-door-between-federal-agencies-and-the-private-detention-industry", "further-reading", "dead", {"link_note": "Page not found."}),
 # Further reading (old "Related news on prison impacts, incarceration, climate change & more")
 ("undated-invest-appalachia-climate", None, "Climate resilience in Central Appalachia: impacts and opportunities", "Invest Appalachia",
  "https://www.investappalachia.org/climate-analysis", "further-reading", "ok",
  {"_note": "As of 2026-10-10 this redirects to investappalachia.org/resourced-resilience/; the content may have moved."}),
 ("undated-truthout-environmental-health", None, "Federal agencies ignore environmental health risks for millions of prisoners", "Truthout",
  "https://truthout.org/articles/federal-agencies-ignore-environmental-health-risks-for-millions-of-prisoners/", "further-reading", "ok", {}),
 ("undated-doj-prison-reform", None, "Prison reform: reducing recidivism by strengthening the Federal Bureau of Prisons", "U.S. Department of Justice (archive)",
  "https://www.justice.gov/archives/prison-reform", "further-reading", "ok", {"_note": "Text-fragment suffix (#:~:text=...) removed from the original link."}),
 ("undated-oregon-business-prosperity", None, "Prisons don’t bring prosperity to rural towns", "Oregon Business",
  "https://oregonbusiness.com/4176-prisons-dont-bring-prosperity-to-rural-towns/", "further-reading", "ok", {}),
 ("undated-the-hill-crumbling-prisons", None, "We need a well-designed plan to repair or replace our crumbling federal prisons", "The Hill",
  "https://thehill.com/opinion/criminal-justice/3866946-we-need-a-well-designed-plan-to-repair-or-replace-our-crumbling-federal-prisons/", "further-reading", "ok", {}),
 ("undated-corrections1-census", None, "Census Bureau will count federal inmates as residents", "Corrections1",
  "https://www.corrections1.com/federal-prison/articles/census-bureau-will-count-federal-inmates-as-residents-KkgWTj1itQv9QHEt/", "further-reading", "ok", {}),
 ("2022-12-12-marshall-project-addiction-medications", "2022-12-12", "Federal prisons were told to provide addiction medications. Instead, they punish people who use them.", "The Marshall Project",
  "https://www.themarshallproject.org/2022/12/12/suboxone-federal-prison-opioid-addiction-treatment-overdose", "further-reading", "ok", {}),
 ("undated-the-hill-change-in-leadership", None, "To fix our prison system, we need far more than a change in leadership", "The Hill",
  "https://thehill.com/opinion/criminal-justice/586981-to-fix-our-prison-system-we-need-far-more-than-a-change-in/", "further-reading", "ok", {}),
 ("undated-wsj-inland-flooding", None, "Flooding hits American towns far from oceans and big rivers", "The Wall Street Journal",
  "https://www.wsj.com/articles/flooding-inland-climate-change-kentucky-3ed2c7fb", "further-reading", "ok",
  {"_note": "CLC's 2024 letter to the BOP describes this as a June 2023 article; exact date not confirmed. Search parameters removed from the link."}),
]


def q(v):
    return json.dumps(v, ensure_ascii=False)


for slug, date, title, source, url, section, status, extra in ITEMS:
    lines = ["---", f"title: {q(title)}"]
    if date:
        lines.append(f"date: {date}")
    lines += [f"source: {q(source)}", f"url: {q(url)}", f"section: {section}", f"link_status: {status}"]
    if status == "dead":
        lines.append(f"link_checked: {CHECKED}")
        lines.append(f"link_note: {q(extra['link_note'])}")
    for k in ("summary", "image", "image_alt"):
        if k in extra:
            lines.append(f"{k}: {q(extra[k])}")
    lines.append(f"original_source_url: {q(extra.get('_old', OLD_NEWS))}")
    lines.append("---")
    if "_note" in extra:
        lines.append(f"<!-- Migration note: {extra['_note']} -->")
    os.makedirs(os.path.join("src", "content", "news"), exist_ok=True)
    with open(os.path.join("src", "content", "news", f"{slug}.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
print(len(ITEMS), "items written")
