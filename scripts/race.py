"""Render the contribution calendar as a race track with a GT car lapping it.

Usage: GITHUB_TOKEN=... python3 scripts/race.py <login> <out.svg>
"""
import json, os, sys, urllib.request
from datetime import datetime, timezone

LOGIN, OUT = sys.argv[1], sys.argv[2]
QUERY = """query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{
totalContributions weeks{contributionDays{date weekday contributionCount contributionLevel}}}}}}"""

req = urllib.request.Request(
    "https://api.github.com/graphql",
    data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
    headers={"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}", "Content-Type": "application/json"},
)
cal = json.load(urllib.request.urlopen(req))["data"]["user"]["contributionsCollection"]["contributionCalendar"]
weeks = cal["weeks"]

# ---- theme (NISMO) ----
BG, BG2, FG, MUTED, RED = "#0A0A0A", "#151515", "#F5F5F5", "#8C8C8C", "#E60012"
LEVEL = {"NONE": "#1C1C1C", "FIRST_QUARTILE": "#5C0A10", "SECOND_QUARTILE": "#8E0B16",
         "THIRD_QUARTILE": "#C3001C", "FOURTH_QUARTILE": "#FF1E2D"}
FONT = "'Arial Black','Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "'SF Mono','Menlo','Consolas',monospace"

CELL, GAP = 14, 4
P = CELL + GAP
COLS = len(weeks)
X0, Y0 = 40 + (1120 - COLS * P) // 2, 78
W, H = 1200, Y0 + 7 * P + 62
T = 20  # lap time, seconds
DRIVE = 0.9  # fraction of lap spent driving; rest is cool-down at the line


def center(c, r):
    return X0 + c * P + CELL / 2, Y0 + r * P + CELL / 2


# serpentine route: down even columns, up odd columns
pts = []
for c in range(COLS):
    rows = range(7) if c % 2 == 0 else range(6, -1, -1)
    pts += [center(c, r) for r in rows]
route = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
last = len(pts) - 1

cells, eat = [], []
for c, wk in enumerate(weeks):
    for d in wk["contributionDays"]:
        r = d["weekday"]
        x, y = X0 + c * P, Y0 + r * P
        lvl = d["contributionLevel"]
        tip = f'{d["date"]}: {d["contributionCount"]} contributions'
        if lvl == "NONE":
            cells.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3" fill="{LEVEL[lvl]}"><title>{tip}</title></rect>')
            continue
        k = c * 7 + (r if c % 2 == 0 else 6 - r)
        at = k / last * DRIVE * 100
        i = len(eat)
        eat.append(f"@keyframes e{i}{{0%,{at:.2f}%{{fill:{LEVEL[lvl]}}}{min(at + .4, 99):.2f}%,98%{{fill:{LEVEL['NONE']}}}100%{{fill:{LEVEL[lvl]}}}}}"
                   f".e{i}{{animation:e{i} {T}s linear infinite}}")
        cells.append(f'<rect class="e{i}" x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3" fill="{LEVEL[lvl]}"><title>{tip}</title></rect>')

# kerbs above and below the track
kx0, kx1 = X0 - 14, X0 + COLS * P + 10
kerb = lambda y: "".join(f'<rect x="{x}" y="{y}" width="12" height="8" fill="{RED if (x - kx0) // 12 % 2 == 0 else FG}"/>'
                         for x in range(kx0, kx1, 12))
# chequered start/finish line just left of the first column
flag = "".join(f'<rect x="{X0 - 14 + (j % 2) * 5}" y="{Y0 + i * 5}" width="5" height="5" fill="{FG}"/>'
               for i in range(0, (7 * P) // 5) for j in [i % 2])

# top-down GT car, nose pointing +x, centred on the origin
car = f"""<g id="car">
<ellipse cx="0" cy="0" rx="20" ry="12" fill="#000" opacity=".45" transform="translate(2,3)"/>
<rect x="-14" y="-11" width="7" height="4" rx="1.5" fill="#111"/><rect x="-14" y="7" width="7" height="4" rx="1.5" fill="#111"/>
<rect x="7" y="-11" width="7" height="4" rx="1.5" fill="#111"/><rect x="7" y="7" width="7" height="4" rx="1.5" fill="#111"/>
<path d="M-17,-8 C-17,-10 -12,-9 -6,-9 L10,-8 C16,-7 20,-4 20,0 C20,4 16,7 10,8 L-6,9 C-12,9 -17,10 -17,8 Z" fill="{FG}"/>
<path d="M-17,-2.5 H20 V2.5 H-17 Z" fill="{RED}"/>
<path d="M-4,-6 C2,-6 6,-4 6,0 C6,4 2,6 -4,6 C-6,4 -6,-4 -4,-6 Z" fill="#101820"/>
<rect x="-21" y="-10" width="4" height="20" rx="1" fill="#111"/>
<rect x="18" y="-9" width="3" height="18" rx="1" fill="{RED}"/>
<text x="-10" y="2.6" text-anchor="middle" font-size="6" font-family="{FONT}" fill="{BG}">11</text>
</g>"""

updated = datetime.now(timezone.utc).strftime("%Y-%m-%d")
svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{cal['totalContributions']} contributions in the last year">
<title>{cal['totalContributions']} contributions in the last year</title>
<defs><pattern id="carbon" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
<rect width="8" height="8" fill="{BG}"/><rect width="4" height="4" fill="{BG2}"/><rect x="4" y="4" width="4" height="4" fill="{BG2}"/></pattern>
<clipPath id="card"><rect width="{W}" height="{H}" rx="14"/></clipPath></defs>
<style>text{{font-family:{FONT}}}.mono{{font-family:{MONO}}}
{''.join(eat)}
@media (prefers-reduced-motion: reduce){{*{{animation:none!important}}}}</style>
<g clip-path="url(#card)">
<rect width="{W}" height="{H}" fill="url(#carbon)"/>
<text class="mono" x="40" y="40" font-size="14" letter-spacing="5" fill="{RED}">// RACE TRACK · LAST 12 MONTHS</text>
<text x="{W - 40}" y="42" text-anchor="end" font-size="22" font-style="italic" fill="{FG}">{cal['totalContributions']:,} <tspan font-size="13" fill="{MUTED}">LAPS</tspan></text>
<rect x="{kx0}" y="{Y0 - 18}" width="{kx1 - kx0}" height="{7 * P + 28}" rx="6" fill="#111"/>
{kerb(Y0 - 18)}{kerb(Y0 + 7 * P + 2)}
{flag}
{''.join(cells)}
<use href="#car"><animateMotion dur="{T}s" repeatCount="indefinite" rotate="auto" path="{route}"
 keyPoints="0;1;1" keyTimes="0;{DRIVE};1" calcMode="linear"/></use>
<defs>{car}</defs>
<g class="mono" font-size="11" fill="{MUTED}">
<text x="40" y="{H - 18}" letter-spacing="2">LESS</text>
{''.join(f'<rect x="{84 + i * 18}" y="{H - 29}" width="{CELL}" height="{CELL}" rx="3" fill="{c}"/>' for i, c in enumerate(LEVEL.values()))}
<text x="{84 + 5 * 18 + 6}" y="{H - 18}" letter-spacing="2">MORE</text>
<text x="{W - 40}" y="{H - 18}" text-anchor="end" letter-spacing="2">UPDATED {updated}</text>
</g>
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="none" stroke="#2E2E2E"/>
</svg>"""
open(OUT, "w").write(svg)
print(f"{OUT}: {cal['totalContributions']} contributions, {len(eat)} active days, {COLS} weeks")
