#!/usr/bin/env python3
"""Generate assets__generated__stats.svg from the GitHub GraphQL API.

Uses only the Python standard library. Reads:
  GITHUB_TOKEN  token used for the API calls (PROFILE_TOKEN is preferred if set)
  GH_USER       GitHub login (defaults to the repository owner)

Run with --placeholder to write the neutral card that ships with the repository,
or --sample to render obviously-labelled sample numbers for design previews.
"""
import datetime as dt
import html
import json
import os
import sys
import urllib.request
from pathlib import Path

OUT = Path(__file__).resolve().parent / "assets__generated__stats.svg"
INK, PANEL, LINE, TEXT, MUTED = "#080D1C", "#111B38", "#26345F", "#E8ECFF", "#93A0C8"
CYAN, VIOLET, AMBER = "#4CC9F0", "#8B7CFF", "#FFB547"
SANS = "Inter, 'Segoe UI', -apple-system, 'Helvetica Neue', Arial, sans-serif"

QUERY = """
query($login: String!) {
  user(login: $login) {
    followers { totalCount }
    repositories(ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC, first: 100) {
      totalCount
      nodes { stargazerCount }
    }
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      contributionCalendar {
        totalContributions
        weeks { contributionDays { contributionCount date } }
      }
    }
  }
}
"""


def fetch(login, token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json", "User-Agent": "profile-stats"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        payload = json.load(r)
    if "errors" in payload or not payload.get("data", {}).get("user"):
        raise SystemExit("GitHub API error: " + json.dumps(payload.get("errors", payload))[:500])
    u = payload["data"]["user"]
    cc = u["contributionsCollection"]
    days = [d for w in cc["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
    weekly = [sum(d["contributionCount"] for d in w["contributionDays"]) for w in cc["contributionCalendar"]["weeks"]]
    longest = cur = 0
    for d in days:
        cur = cur + 1 if d["contributionCount"] else 0
        longest = max(longest, cur)
    today = dt.date.today().isoformat()
    streak, seen_today = 0, False
    for d in reversed(days):
        if d["date"] > today:
            continue
        if d["contributionCount"]:
            streak += 1
        elif d["date"] == today and not seen_today:
            seen_today = True  # today may simply not have a contribution yet
        else:
            break
    return {
        "contributions": cc["contributionCalendar"]["totalContributions"],
        "commits": cc["totalCommitContributions"],
        "prs": cc["totalPullRequestContributions"],
        "streak": streak,
        "longest": longest,
        "repos": u["repositories"]["totalCount"],
        "stars": sum(n["stargazerCount"] for n in u["repositories"]["nodes"]),
        "followers": u["followers"]["totalCount"],
        "weekly": weekly,
    }


def esc(s):
    return html.escape(str(s), quote=True)


def render(data=None, tag=None):
    W, H = 1000, 300
    f = f'font-family="{SANS}"'
    d = data or {}
    def v(k):
        return "–" if data is None else f"{d[k]:,}"
    big = [("contributions", "Contributions, last 12 months", CYAN), ("commits", "Commits", VIOLET),
           ("prs", "Pull requests", CYAN), ("streak", "Current streak (days)", AMBER)]
    small = [("repos", "Public repositories"), ("stars", "Stars received"), ("followers", "Followers"), ("longest", "Longest streak (days)")]
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t">'
         f'<title id="t">GitHub activity summary for the last 12 months</title>',
         f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="{PANEL}" stroke="{LINE}"/>']
    colw = (W - 60) / 4
    for i, (k, label, col) in enumerate(big):
        x = 30 + i * colw
        o.append(f'<rect x="{x:.0f}" y="28" width="3" height="52" rx="1.5" fill="{col}"/>'
                 f'<text x="{x+14:.0f}" y="66" {f} font-size="38" font-weight="700" fill="{TEXT}">{v(k)}</text>'
                 f'<text x="{x+14:.0f}" y="88" {f} font-size="12.5" fill="{MUTED}">{esc(label)}</text>')
    for i, (k, label) in enumerate(small):
        x = 30 + i * colw
        o.append(f'<text x="{x+14:.0f}" y="128" {f} font-size="19" font-weight="600" fill="{TEXT}">{v(k)}</text>'
                 f'<text x="{x+14:.0f}" y="146" {f} font-size="12" fill="{MUTED}">{esc(label)}</text>')
    # weekly contribution bars
    bx, by, bw, bh = 30, 252, W - 60, 76
    o.append(f'<line x1="{bx}" x2="{bx+bw}" y1="{by}" y2="{by}" stroke="{LINE}"/>')
    weekly = d.get("weekly") or [0] * 53
    top = max(max(weekly), 1)
    step = bw / len(weekly)
    for i, n in enumerate(weekly):
        h = 3 if data is None else max(3, n / top * bh)
        op = ".35" if data is None else (".9" if n else ".25")
        o.append(f'<rect x="{bx+i*step+1.2:.1f}" y="{by-h:.1f}" width="{step-2.4:.1f}" height="{h:.1f}" rx="2" fill="{CYAN}" fill-opacity="{op}"/>')
    foot = tag or ("Refreshed by GitHub Actions on " + dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d") + " UTC. Bars show contributions per week.") if data else \
        "Placeholder. This card is replaced with live numbers the first time the Profile stats workflow runs."
    if tag: foot = tag
    o.append(f'<text x="{bx}" y="{H-14}" {f} font-size="11.5" fill="{MUTED}">{esc(foot)}</text>')
    o.append("</svg>")
    return "".join(o)


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    if "--placeholder" in sys.argv:
        OUT.write_text(render(None), encoding="utf-8"); print("placeholder written"); return
    if "--sample" in sys.argv:
        import random; random.seed(3)
        sample = dict(contributions=0, commits=0, prs=0, streak=0, longest=0, repos=0, stars=0, followers=0,
                      weekly=[random.choice([0, 0, 1, 3, 6, 9, 14]) for _ in range(53)])
        target = Path(sys.argv[sys.argv.index("--sample") + 1])
        sample.update(contributions=sum(sample["weekly"]), commits=212, prs=9, streak=4, longest=17, repos=9, stars=2, followers=5)
        target.write_text(render(sample, tag="SAMPLE NUMBERS FOR DESIGN PREVIEW ONLY. The live card uses your real GitHub data."), encoding="utf-8"); return
    token = os.environ.get("PROFILE_TOKEN") or os.environ.get("GITHUB_TOKEN")
    user = os.environ.get("GH_USER") or os.environ.get("GITHUB_REPOSITORY_OWNER") or "Anima-Das"
    if not token:
        raise SystemExit("Set GITHUB_TOKEN (or PROFILE_TOKEN) before running.")
    OUT.write_text(render(fetch(user, token)), encoding="utf-8")
    print("wrote", OUT)


if __name__ == "__main__":
    main()
