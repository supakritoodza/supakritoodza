"""Generate GT3 / BMW M themed SVG assets for GitHub profile README."""
import math, os, sys

OUT = sys.argv[1]
os.makedirs(f"{OUT}/assets", exist_ok=True)

# ---- data (from repo scan) ----
NAME = "SUPAKRIT ODTHON"
ROLE = "FULL-STACK DEVELOPER"
TEAM = "LOOKSOCIAL"
NUMBER = "11"
COMMITS = 928
REPOS = 8
LANGS = 7
ROOKIE = 2021
STANDINGS = [  # (language, team/role, share %, colour)
    ("GO", "BACKEND", 43.8, "#00ADD8"),
    ("TYPESCRIPT", "FULL-STACK", 39.4, "#3178C6"),
    ("PYTHON", "BACKEND / DATA", 8.2, "#FFD43B"),
    ("HTML / CSS", "WEB", 5.1, "#E34F26"),
    ("JAVASCRIPT", "FRONTEND", 1.3, "#F7DF1E"),
    ("SQL", "DATABASE", 1.0, "#336791"),
    ("VUE", "FRONTEND", 1.0, "#42B883"),
]

# ---- theme ----
THEME = os.environ.get("THEME", "bmw")
THEMES = {
    # accent, secondary, redline, stripes, bg, carbon, fg, muted, border, tile
    "bmw": ("#81C4FF", "#16588E", "#E7222E", ("#81C4FF", "#16588E", "#E7222E"), "#0B0E13", "#141922", "#F5F7FA", "#8A94A6", "#2A3240", "#0F141C"),
    "nismo": ("#FF1E2D", "#C8C8C8", "#E60012", ("#E60012", "#F5F5F5", "#E60012"), "#0A0A0A", "#151515", "#F5F5F5", "#8C8C8C", "#2E2E2E", "#121212"),
}
LB, DB, RED, STRIPES, BG, BG2, FG, MUTED, BORDER, TILE = THEMES[THEME]
ROW1, ROW2, TRACK, GAUGE = {"bmw": ("#121821", "#0E131A", "#1A212C", "#07090D"), "nismo": ("#171717", "#111111", "#242424", "#050505")}[THEME]
if THEME == "nismo":  # monochrome + red standings
    STANDINGS = [(l, t, p, ("#E60012", "#F5F5F5", "#B5B5B5")[i] if i < 3 else "#6E6E6E") for i, (l, t, p, c) in enumerate(STANDINGS)]
FONT = "'Arial Black','Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "'SF Mono','Menlo','Consolas',monospace"

CARBON = f"""<pattern id="carbon" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
<rect width="8" height="8" fill="{BG}"/><rect width="4" height="4" fill="{BG2}"/><rect x="4" y="4" width="4" height="4" fill="{BG2}"/></pattern>"""


def stripes(x, y, w, h, gap=0, skew=-20, cls=""):
    """Three M stripes, each w wide."""
    out = []
    for i, c in enumerate(STRIPES):
        out.append(f'<rect class="{cls}" x="{x + i * (w + gap)}" y="{y}" width="{w}" height="{h}" fill="{c}" transform="skewX({skew})"/>')
    return "\n".join(out)


def svg(w, h, body, style="", title=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{title}">
<title>{title}</title>
<defs>{CARBON}
<linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="{BG}" stop-opacity="0"/><stop offset="1" stop-color="{BG}" stop-opacity=".95"/></linearGradient>
<clipPath id="card"><rect width="{w}" height="{h}" rx="14"/></clipPath>
</defs>
<style>text{{font-family:{FONT}}} .mono{{font-family:{MONO}}} {style}
@media (prefers-reduced-motion: reduce){{*{{animation:none!important}}}}</style>
<g clip-path="url(#card)">
<rect width="{w}" height="{h}" fill="url(#carbon)"/>
{body}
</g>
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="14" fill="none" stroke="{BORDER}"/>
</svg>"""


def write(name, s):
    open(f"{OUT}/assets/{name}", "w").write(s)


# ================= HEADER =================
lights = []
lkf = []
for i in range(5):
    on = 5 + i * 7
    lkf.append(f"@keyframes l{i}{{0%,{on - 1}%{{fill:#2B0A0C}}{on}%,44%{{fill:{RED}}}45%,100%{{fill:#2B0A0C}}}}"
               f".l{i}{{animation:l{i} 7s infinite}}")
    cx = 70 + i * 46
    lights.append(f'<rect x="{cx - 19}" y="290" width="38" height="38" rx="6" fill="#05070A" stroke="{BORDER}"/>'
                  f'<circle class="l{i}" cx="{cx}" cy="309" r="13" fill="#2B0A0C"/>')

header_style = "\n".join(lkf) + f"""
@keyframes slide{{from{{transform:translateX(-900px)}}to{{transform:translateX(0)}}}}
.band{{animation:slide 1.4s cubic-bezier(.2,.8,.2,1) both}}
@keyframes go{{0%,44%{{opacity:0}}46%,92%{{opacity:1}}100%{{opacity:0}}}}
.go{{animation:go 7s infinite}}
@keyframes rise{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:none}}}}
.r1{{animation:rise .8s .2s both}} .r2{{animation:rise .8s .45s both}} .r3{{animation:rise .8s .7s both}}
@keyframes speed{{0%{{transform:translateX(1300px)}}100%{{transform:translateX(-400px)}}}}
.sp{{animation:speed 1.6s linear infinite}}
"""
speed = "".join(
    f'<rect class="sp" style="animation-delay:{d}s" x="0" y="{y}" width="{w}" height="2" fill="{c}" opacity=".35"/>'
    for y, w, d, c in [(40, 220, 0, LB), (70, 140, .5, FG), (250, 260, .9, LB), (270, 120, .3, FG), (232, 180, 1.2, RED)])
thai_flag = ''.join(f'<rect x="0" y="{y}" width="36" height="{h}" fill="{c}"/>' for y, h, c in
                    [(0, 4, "#A51931"), (4, 4, "#F4F5F8"), (8, 8, "#2D2A4A"), (16, 4, "#F4F5F8"), (20, 4, "#A51931")])
header = f"""
{speed}
<g class="band"><g transform="translate(560,0)">{stripes(120, -20, 46, 400, gap=10)}</g></g>
<rect x="560" width="640" height="360" fill="url(#fade)" opacity=".35"/>
<!-- number plate -->
<g transform="translate(930,70)">
  <rect width="220" height="170" rx="18" fill="{FG}" transform="skewX(-8)"/>
  <rect x="10" y="10" width="200" height="150" rx="12" fill="none" stroke="{BG}" stroke-width="3" transform="skewX(-8)"/>
  <text x="96" y="138" text-anchor="middle" font-size="128" font-style="italic" fill="{BG}" letter-spacing="-6">{NUMBER}</text>
</g>
<g transform="translate(60,0)">
  <text class="r1 mono" x="0" y="78" font-size="16" fill="{LB}" letter-spacing="6">// DRIVER PROFILE</text>
  <text class="r2" x="0" y="150" font-size="64" font-style="italic" fill="{FG}" letter-spacing="1">{NAME}</text>
  <g class="r3">
    <rect x="0" y="176" width="8" height="34" fill="{LB}"/><rect x="12" y="176" width="8" height="34" fill="{DB}"/><rect x="24" y="176" width="8" height="34" fill="{RED}"/>
    <text x="48" y="203" font-size="26" font-style="italic" fill="{FG}">{ROLE}</text>
    <text class="mono" x="48" y="240" font-size="16" fill="{MUTED}" letter-spacing="3">TEAM {TEAM}</text>
    <g transform="translate(250,226)">{thai_flag}</g>
    <text class="mono" x="296" y="245" font-size="16" fill="{MUTED}" letter-spacing="3">THA</text>
  </g>
</g>
{''.join(lights)}
<text class="go" x="320" y="318" font-size="22" font-style="italic" fill="{FG}">LIGHTS OUT AND AWAY WE GO</text>
<text class="go" x="320" y="318" font-size="22" font-style="italic" fill="none" stroke="{RED}" stroke-width=".6" dx="2" dy="2" opacity=".6">LIGHTS OUT AND AWAY WE GO</text>
"""
write("header.svg", svg(1200, 360, header, header_style, f"{NAME} - #{NUMBER} - {ROLE}"))

# ================= TELEMETRY =================
cx, cy, R = 210, 200, 140
ticks = []
for i in range(0, 91):
    a = math.radians(225 - i * 3)  # 270 deg sweep
    major = i % 10 == 0
    r1 = R - (22 if major else 10)
    col = RED if i >= 70 else (FG if major else MUTED)
    ticks.append(f'<line x1="{cx + r1 * math.cos(a):.1f}" y1="{cy - r1 * math.sin(a):.1f}" x2="{cx + R * math.cos(a):.1f}" y2="{cy - R * math.sin(a):.1f}" stroke="{col}" stroke-width="{3 if major else 1.4}"/>')
    if major:
        rl = R - 42
        ticks.append(f'<text x="{cx + rl * math.cos(a):.1f}" y="{cy - rl * math.sin(a) + 7:.1f}" text-anchor="middle" font-size="18" font-style="italic" fill="{RED if i >= 70 else FG}">{i // 10}</text>')


def arc(r, a0, a1):
    p0 = (cx + r * math.cos(math.radians(a0)), cy - r * math.sin(math.radians(a0)))
    p1 = (cx + r * math.cos(math.radians(a1)), cy - r * math.sin(math.radians(a1)))
    large = 1 if abs(a0 - a1) > 180 else 0
    return f"M{p0[0]:.1f},{p0[1]:.1f} A{r},{r} 0 {large} 1 {p1[0]:.1f},{p1[1]:.1f}"


tel_style = f"""
@keyframes needle{{0%{{transform:rotate(-135deg)}}35%{{transform:rotate(95deg)}}42%{{transform:rotate(78deg)}}50%{{transform:rotate(100deg)}}58%{{transform:rotate(84deg)}}100%{{transform:rotate(92deg)}}}}
.needle{{transform-origin:{cx}px {cy}px;animation:needle 3.2s cubic-bezier(.3,.7,.2,1) both}}
@keyframes shift{{0%,30%{{fill:{BORDER}}}32%,100%{{fill:{RED}}}}}
.shift rect{{animation:shift 3.2s both}}
@keyframes rise{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:none}}}}
.t1{{animation:rise .6s .3s both}}.t2{{animation:rise .6s .5s both}}.t3{{animation:rise .6s .7s both}}.t4{{animation:rise .6s .9s both}}
"""
shift = "".join(f'<rect style="animation-delay:{i * .12}s" x="{cx - 66 + i * 28}" y="16" width="20" height="10" rx="3"/>' for i in range(5))
tiles = [
    ("TOTAL LAPS", f"{COMMITS}", "commits", LB),
    ("RACES ENTERED", f"{REPOS}", "repositories", LB),
    ("ENGINES", f"{LANGS}", "languages", DB),
    ("ROOKIE SEASON", f"{ROOKIE}", "on github", RED),
]
tile_svg = []
for i, (lab, val, sub, c) in enumerate(tiles):
    x, y = 430 + (i % 2) * 380, 50 + (i // 2) * 130
    tile_svg.append(f"""<g transform="translate({x},{y})"><g class="t{i + 1}">
<rect width="350" height="110" rx="10" fill="{TILE}" stroke="{BORDER}"/><rect width="6" height="110" rx="3" fill="{c}"/>
<text class="mono" x="26" y="32" font-size="14" letter-spacing="3" fill="{MUTED}">{lab}</text>
<text x="26" y="88" font-size="50" font-style="italic" fill="{FG}">{val}</text>
<text class="mono" x="{36 + len(val) * 36}" y="86" font-size="15" fill="{MUTED}">{sub}</text></g></g>""")
telemetry = f"""
<text class="mono" x="430" y="30" font-size="14" letter-spacing="5" fill="{LB}">// LIVE TELEMETRY</text>
<g class="shift">{shift}</g>
<circle cx="{cx}" cy="{cy}" r="{R + 14}" fill="{GAUGE}" stroke="{BORDER}" stroke-width="2"/>
<path d="{arc(R + 4, 225, -45)}" fill="none" stroke="{TRACK}" stroke-width="6"/>
<path d="{arc(R + 4, 225 - 210, -45)}" fill="none" stroke="{RED}" stroke-width="6"/>
{''.join(ticks)}
<text x="{cx}" y="{cy + 70}" text-anchor="middle" font-size="40" font-style="italic" fill="{FG}">{COMMITS}</text>
<text class="mono" x="{cx}" y="{cy + 94}" text-anchor="middle" font-size="12" letter-spacing="3" fill="{MUTED}">COMMITS x1</text>
<text class="mono" x="{cx}" y="{cy - 40}" text-anchor="middle" font-size="11" letter-spacing="2" fill="{MUTED}">x1000 r/min</text>
<g class="needle"><path d="M{cx - 4},{cy} L{cx},{cy - R + 18} L{cx + 4},{cy} Z" fill="{RED}"/></g>
<circle cx="{cx}" cy="{cy}" r="14" fill="{BG2}" stroke="{FG}" stroke-width="2"/>
{''.join(tile_svg)}
"""
# ---- turbo boost strip ----
tel_style += f"""
@keyframes spin{{to{{transform:rotate(360deg)}}}}
.spin{{transform-box:fill-box;transform-origin:center;animation:spin .28s linear infinite}}
@keyframes boost{{0%{{transform:scaleX(.04)}}60%{{transform:scaleX(1)}}62%{{transform:scaleX(.12)}}100%{{transform:scaleX(.04)}}}}
.boost{{transform-box:fill-box;transform-origin:left;animation:boost 3.2s cubic-bezier(.5,0,.9,.6) infinite}}
@keyframes blur{{0%{{opacity:0}}60%{{opacity:.9}}62%,100%{{opacity:0}}}}
.blur{{animation:blur 3.2s infinite}}
@keyframes bov{{0%,61%{{opacity:0;transform:translateX(-10px)}}63%{{opacity:1;transform:none}}80%{{opacity:.8}}90%,100%{{opacity:0;transform:translateX(16px)}}}}
.bov{{animation:bov 3.2s infinite}}
"""
blades = "".join(f'<path d="M0,0 C6,-6 10,-14 8,-22" fill="none" stroke="{FG}" stroke-width="3" stroke-linecap="round" transform="rotate({a})"/>' for a in range(0, 360, 45))
segs = "".join(f'<line x1="{560 + i * 46}" y1="352" x2="{560 + i * 46}" y2="358" stroke="{MUTED}" stroke-width="1.5"/>'
               f'<text class="mono" x="{560 + i * 46}" y="372" text-anchor="middle" font-size="10" fill="{MUTED}">{i * .2:.1f}</text>' for i in range(0, 11, 2))
telemetry = telemetry.replace("{TILE}", TILE)
telemetry += f"""
<g transform="translate(430,302)"><rect width="730" height="74" rx="10" fill="{TILE}" stroke="{BORDER}"/></g>
<g transform="translate(470,339)">
  <circle r="28" fill="#050505" stroke="{MUTED}" stroke-width="3"/>
  <circle class="blur" r="22" fill="none" stroke="{RED}" stroke-width="6" opacity="0"/>
  <g class="spin"><circle r="22" fill="none"/>{blades}</g>
  <circle r="5" fill="{RED}"/>
</g>
<text class="mono" x="520" y="328" font-size="13" letter-spacing="3" fill="{MUTED}">TURBO BOOST</text>
<text class="mono" x="660" y="328" font-size="11" letter-spacing="2" fill="{LB}">BAR</text>
<rect x="560" y="336" width="460" height="12" rx="6" fill="{TRACK}"/>
<defs><linearGradient id="bg2" x1="0" x2="1"><stop offset="0" stop-color="{MUTED}"/><stop offset=".7" stop-color="{FG}"/><stop offset="1" stop-color="{RED}"/></linearGradient></defs>
<rect class="boost" x="560" y="336" width="460" height="12" rx="6" fill="url(#bg2)"/>
{segs}
<text class="bov" x="1046" y="352" font-size="24" font-style="italic" fill="{FG}">PSSHH</text>
"""
write("telemetry.svg", svg(1200, 380, telemetry, tel_style, f"Telemetry: {COMMITS} commits, {REPOS} repositories, {LANGS} languages"))

# ================= STANDINGS =================
rows = []
top = STANDINGS[0][2]
st_style = """@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
.bar{transform-box:fill-box;transform-origin:left;animation:grow 1.2s cubic-bezier(.2,.8,.2,1) both}
@keyframes rise{from{opacity:0;transform:translateX(-12px)}to{opacity:1;transform:none}}"""
for i, (lang, team, pct, c) in enumerate(STANDINGS):
    y = 96 + i * 50
    pos_fill = [("#D4AF37"), ("#C0C0C0"), ("#CD7F32")][i] if i < 3 else TRACK
    pos_txt = BG if i < 3 else FG
    bw = max(6, 560 * pct / top)
    rows.append(f"""<g style="animation:rise .5s {.1 + i * .08:.2f}s both">
<rect x="40" y="{y}" width="1120" height="42" rx="6" fill="{ROW1 if i % 2 == 0 else ROW2}"/>
<rect x="40" y="{y}" width="56" height="42" rx="6" fill="{pos_fill}"/>
<text x="68" y="{y + 30}" text-anchor="middle" font-size="20" font-style="italic" fill="{pos_txt}">P{i + 1}</text>
<rect x="110" y="{y + 8}" width="5" height="26" fill="{c}"/>
<text x="128" y="{y + 29}" font-size="19" font-style="italic" fill="{FG}">{lang}</text>
<text class="mono" x="330" y="{y + 27}" font-size="13" letter-spacing="2" fill="{MUTED}">{team}</text>
<rect x="500" y="{y + 15}" width="560" height="12" rx="6" fill="{TRACK}"/>
<rect class="bar" style="animation-delay:{.3 + i * .08:.2f}s" x="500" y="{y + 15}" width="{bw:.1f}" height="12" rx="6" fill="{c}"/>
<text x="1140" y="{y + 29}" text-anchor="end" font-size="19" font-style="italic" fill="{FG}">{pct:.1f}%</text></g>""")
standings = f"""
<text class="mono" x="40" y="44" font-size="14" letter-spacing="5" fill="{LB}">// CHAMPIONSHIP STANDINGS</text>
{''.join(f'<text class="mono" x="{x}" y="78" font-size="12" letter-spacing="2" fill="{MUTED}">{t}</text>' for x, t in [(44, "POS"), (128, "ENGINE"), (330, "CLASS"), (500, "SHARE OF COMMITS")])}
<g transform="translate(1040,22)">{stripes(0, 0, 18, 34, gap=4)}</g>
{''.join(rows)}
"""
write("standings.svg", svg(1200, 96 + len(STANDINGS) * 50 + 24, standings, st_style, "Language championship standings"))

# ================= DIVIDER =================
sq = 12
checks = "".join(f'<rect x="{x * sq}" y="{y * sq}" width="{sq}" height="{sq}" fill="{FG if (x + y) % 2 == 0 else BG}"/>'
                 for x in range(0, 1200 // sq + 2) for y in range(2))
div = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="24" viewBox="0 0 1200 24">
<style>@keyframes run{{from{{transform:translateX(0)}}to{{transform:translateX(-{sq * 2}px)}}}}.c{{animation:run .6s linear infinite}}
@media (prefers-reduced-motion: reduce){{*{{animation:none!important}}}}</style>
<g class="c">{checks}</g>
<rect x="0" width="190" height="24" fill="{BG}"/>
<g>{''.join(f'<rect x="{12 + i * 58}" width="50" height="24" fill="{c}" transform="skewX(-25)"/>' for i, c in enumerate(STRIPES))}</g>
</svg>"""
write("divider.svg", div)
print("ok")

# ================= DRIVER CARD =================
SEASONS = 2026 - ROOKIE + 1
card_style = """@keyframes rise{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
.c1{animation:rise .7s .2s both}.c2{animation:rise .7s .4s both}.c3{animation:rise .7s .6s both}
@keyframes scan{0%{transform:translateY(-40px)}100%{transform:translateY(420px)}}
.scan{animation:scan 3.5s linear infinite}
@keyframes speed{0%{transform:translateX(450px)}100%{transform:translateX(-250px)}}
.sp{animation:speed 1.4s linear infinite}
@keyframes glint{0%,70%{opacity:.15}80%{opacity:.8}100%{opacity:.15}}
.glint{animation:glint 3s infinite}"""
facts = [("TEAM", TEAM), ("NATIONALITY", "THAILAND"), ("CLASS", "FULL-STACK GT3"), ("ENGINE", "GO + TYPESCRIPT")]
nums = [("SEASONS", SEASONS), ("RACES", REPOS), ("LAPS", COMMITS), ("PODIUMS", 3)]
fact_svg = "".join(f'<text class="mono" x="0" y="{i * 28}" font-size="13" letter-spacing="3" fill="{MUTED}">{k}</text>'
                   f'<text x="190" y="{i * 28}" font-size="18" font-style="italic" fill="{FG}">{v}</text>' for i, (k, v) in enumerate(facts))
num_svg = "".join(f'<g transform="translate({i * 150},0)"><rect width="134" height="74" rx="8" fill="{TILE}" stroke="{BORDER}"/>'
                  f'<text x="67" y="42" text-anchor="middle" font-size="30" font-style="italic" fill="{FG}">{v}</text>'
                  f'<text class="mono" x="67" y="62" text-anchor="middle" font-size="11" letter-spacing="2" fill="{MUTED}">{k}</text></g>'
                  for i, (k, v) in enumerate(nums))
driver = f"""
<g transform="translate(860,0)">{stripes(120, -10, 40, 440, gap=10)}</g>
<g transform="translate(60,0)">
  <g class="c1"><text class="mono" x="0" y="62" font-size="14" letter-spacing="5" fill="{LB}">// DRIVER LICENCE · GT3 CLASS</text>
  <text x="0" y="122" font-size="52" font-style="italic" fill="{FG}">SUPAKRIT <tspan fill="{LB}">ODTHON</tspan></text>
  <g transform="translate(0,146)"><rect width="84" height="40" rx="6" fill="{FG}" transform="skewX(-8)"/>
  <text x="40" y="32" text-anchor="middle" font-size="30" font-style="italic" fill="{BG}">#{NUMBER}</text></g>
  <g transform="translate(110,148)">{thai_flag.replace('width="36"', 'width="54"').replace('height="4"', 'height="6"').replace('height="8"', 'height="12"')}<rect width="54" height="36" fill="none" stroke="{BORDER}"/></g></g>
  <g transform="translate(0,224)"><g class="c2">{fact_svg}</g></g>
  <g transform="translate(0,334)"><g class="c3">{num_svg}</g></g>
</g>
"""
write("driver.svg", svg(1200, 420, driver, card_style, f"Driver card: {NAME} #{NUMBER}"))

# ================= SEASON AWARDS =================
AWARDS = [  # (tier, title, value, caption)
    ("gold", "ENDURANCE", f"{COMMITS}", "career commits"),
    ("gold", "POLE POSITION", "GO", "43.8% of all laps"),
    ("silver", "LAP RECORD", "436", "commits in one race"),
    ("silver", "DOUBLE STINT", "83%", "go + typescript"),
    ("bronze", "POLYGLOT", f"{LANGS}", "languages raced"),
    ("bronze", "VETERAN", f"{SEASONS}", f"seasons since {ROOKIE}"),
]
TIER = {"gold": "#D4AF37", "silver": "#C0C6CC", "bronze": "#C07A3A"}
aw_style = """@keyframes rise{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}"""
cw = 1120 / len(AWARDS)
cols = []
for i, (tier, title, val, cap) in enumerate(AWARDS):
    x = 40 + i * cw
    sep = f'<line x1="{x:.0f}" y1="78" x2="{x:.0f}" y2="226" stroke="{BORDER}"/>' if i else ""
    cols.append(f"""{sep}<g transform="translate({x + 24:.0f},0)"><g style="animation:rise .5s {.1 + i * .07:.2f}s both">
<rect y="78" width="28" height="3" fill="{TIER[tier]}"/>
<text class="mono" x="0" y="106" font-size="11" letter-spacing="2" fill="{TIER[tier]}">{i + 1:02d} · {tier.upper()}</text>
<text x="0" y="160" font-size="42" font-style="italic" fill="{FG}">{val}</text>
<text x="0" y="190" font-size="15" font-style="italic" fill="{FG}">{title}</text>
<text class="mono" x="0" y="212" font-size="12" fill="{MUTED}">{cap}</text></g></g>""")
awards = f"""
<text class="mono" x="40" y="44" font-size="14" letter-spacing="5" fill="{LB}">// SEASON AWARDS</text>
<g transform="translate(1040,22)">{stripes(0, 0, 18, 34, gap=4)}</g>
{''.join(cols)}
"""
write("trophies.svg", svg(1200, 256, awards, aw_style, "Season awards: " + ", ".join(f"{t} {v}" for _, t, v, _ in AWARDS)))
print("ok2")
