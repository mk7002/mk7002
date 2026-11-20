#!/usr/bin/env python3
"""Generates the SVG assets for the profile README.

Edit the data below, then run:  python3 assets/generate.py
"""
import os
import textwrap
from xml.sax.saxutils import escape

OUT = os.path.dirname(os.path.abspath(__file__))

# ---- design tokens -------------------------------------------------------
BG = "#07090D"
PANEL = "#0D1117"
BORDER = "#1F2630"
TEXT = "#E6EDF3"
MUTED = "#8B949E"
DIM = "#4B5563"
CYAN = "#22D3EE"
VIOLET = "#A78BFA"
GREEN = "#3FB950"

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Inter', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'JetBrains Mono', Menlo, Consolas, monospace"

STYLE = f"""<style>
  .sans {{ font-family: {SANS}; }}
  .mono {{ font-family: {MONO}; }}
  .cursor {{ animation: blink 1.1s steps(1) infinite; }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
  .fade {{ animation: fade 1.2s ease-out both; }}
  @keyframes fade {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: none; }} }}
</style>"""


def write(name, body, w, h):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
           f'viewBox="0 0 {w} {h}" fill="none">\n{STYLE}\n{body}\n</svg>\n')
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote", name)


def grid_pattern(pid, step=24, color=BORDER, opacity=0.55):
    return (f'<pattern id="{pid}" width="{step}" height="{step}" patternUnits="userSpaceOnUse">'
            f'<circle cx="1" cy="1" r="1" fill="{color}" opacity="{opacity}"/></pattern>')


# ---- header --------------------------------------------------------------
def header():
    w, h = 1280, 340
    body = f"""<defs>
  {grid_pattern("dots")}
  <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{VIOLET}"/>
  </linearGradient>
  <radialGradient id="glowA" cx="0.85" cy="0.1" r="0.6">
    <stop offset="0" stop-color="{VIOLET}" stop-opacity="0.28"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="glowB" cx="0.05" cy="1" r="0.55">
    <stop offset="0" stop-color="{CYAN}" stop-opacity="0.18"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/>
  </radialGradient>
  <clipPath id="frame"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18"/></clipPath>
</defs>
<g clip-path="url(#frame)">
  <rect width="{w}" height="{h}" fill="{BG}"/>
  <rect width="{w}" height="{h}" fill="url(#dots)"/>
  <rect width="{w}" height="{h}" fill="url(#glowA)"/>
  <rect width="{w}" height="{h}" fill="url(#glowB)"/>
  <!-- window chrome -->
  <rect width="{w}" height="44" fill="{PANEL}" opacity="0.85"/>
  <line x1="0" y1="44" x2="{w}" y2="44" stroke="{BORDER}"/>
  <circle cx="28" cy="22" r="6" fill="#FF5F57"/><circle cx="48" cy="22" r="6" fill="#FEBC2E"/><circle cx="68" cy="22" r="6" fill="#28C840"/>
  <text x="{w/2}" y="27" text-anchor="middle" class="mono" font-size="13" fill="{MUTED}">milind@mumbai: ~/engineering</text>
  <!-- content -->
  <g>
    <text x="64" y="104" class="mono" font-size="15" fill="{DIM}">// senior software engineer · mobile</text>
    <text x="62" y="172" class="sans" font-size="64" font-weight="800" fill="{TEXT}" letter-spacing="-1.5">Milind Keni</text>
    <text x="64" y="214" class="sans" font-size="24" font-weight="600" fill="url(#accent)">Mobile SDKs · Cross-platform plugins · On-device ML</text>
    <text x="64" y="278" class="mono" font-size="17">
      <tspan fill="{GREEN}">➜</tspan><tspan fill="{CYAN}">  ~</tspan><tspan fill="{TEXT}">  ./ship --android --ios --flutter --rn --unity</tspan><tspan class="cursor" fill="{VIOLET}"> ▍</tspan>
    </text>
  </g>
  <!-- right-side code motif -->
  <g class="mono" font-size="14" fill="{DIM}" opacity="0.9">
    <text x="900" y="100">@WebEngage</text>
    <text x="900" y="124"><tspan fill="{VIOLET}">class</tspan> <tspan fill="{TEXT}">Engineer</tspan> {{</text>
    <text x="924" y="148"><tspan fill="{VIOLET}">val</tspan> years = <tspan fill="{CYAN}">6</tspan></text>
    <text x="924" y="172"><tspan fill="{VIOLET}">val</tspan> base  = <tspan fill="{GREEN}">"Mumbai"</tspan></text>
    <text x="924" y="196"><tspan fill="{VIOLET}">val</tspan> loves = <tspan fill="{GREEN}">"offline-first"</tspan></text>
    <text x="900" y="220">}}</text>
  </g>
  <rect x="0" y="{h-3}" width="{w}" height="3" fill="url(#accent)"/>
</g>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" stroke="{BORDER}" stroke-width="1.5"/>"""
    write("header.svg", body, w, h)


# ---- metrics strip -------------------------------------------------------
METRICS = [
    ("6+", "years shipping mobile"),
    ("280+", "SDK commits @ WebEngage"),
    ("120K+", "Play Store installs"),
    ("24+", "production apps shipped"),
]


def metrics():
    w, h = 1280, 132
    cw = w / len(METRICS)
    cells = []
    for i, (num, label) in enumerate(METRICS):
        x = i * cw
        cx = x + cw / 2
        sep = f'<line x1="{x}" y1="28" x2="{x}" y2="{h-28}" stroke="{BORDER}"/>' if i else ""
        cells.append(f"""{sep}
  <text x="{cx}" y="68" text-anchor="middle" class="sans" font-size="40" font-weight="800" fill="url(#accent)">{escape(num)}</text>
  <text x="{cx}" y="98" text-anchor="middle" class="mono" font-size="13" fill="{MUTED}" letter-spacing="0.5">{escape(label.upper())}</text>""")
    body = f"""<defs>
  <linearGradient id="accent" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{VIOLET}"/>
  </linearGradient>
</defs>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="16" fill="{PANEL}" stroke="{BORDER}" stroke-width="1.5"/>
{''.join(cells)}"""
    write("metrics.svg", body, w, h)


# ---- section headers -----------------------------------------------------
SECTIONS = [
    ("about", "01", "About"),
    ("stack", "02", "Stack"),
    ("sdks", "03", "Open-source SDKs"),
    ("projects", "04", "Featured builds"),
    ("playstore", "05", "Live on Google Play"),
    ("archive", "06", "Archive"),
]


def section(slug, num, title):
    w, h = 1280, 64
    tw = len(title) * 13.5 + 120
    body = f"""<defs>
  <linearGradient id="line" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{CYAN}" stop-opacity="0.9"/>
    <stop offset="0.5" stop-color="{VIOLET}" stop-opacity="0.5"/>
    <stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/>
  </linearGradient>
</defs>
<text x="0" y="40" class="mono" font-size="15" fill="{CYAN}">// {num}</text>
<text x="56" y="41" class="sans" font-size="24" font-weight="700" fill="#C9D1D9" letter-spacing="0.3">{escape(title)}</text>
<rect x="{tw}" y="34" width="{w - tw}" height="1.5" fill="url(#line)"/>"""
    write(f"section-{slug}.svg", body, w, h)


# ---- project cards -------------------------------------------------------
CARDS = [
    # slug, index, kicker, title, description, chips, accent, footer
    ("mocable", "01", "DEV TOOL · LIVE", "Mocable",
     "Self-hosted, multi-user mock REST API service. Any method, :param and wildcard routes, "
     "templated responses, custom status, headers and delay, plus a live request inspector.",
     ["PHP 8", "MySQL", "JavaScript"], CYAN, "mocable.lokihomelab.in ↗"),
    ("notifynow", "02", "DEV TOOL · LIVE", "Notify Now",
     "Push-notification testing tool for mobile developers. Send test pushes to Android (FCM v1) "
     "and iOS (APNs, .p8 JWT) from one screen, with reusable payload templates.",
     ["Flutter Web", "FCM", "APNs"], "#F472B6", "push.lokihomelab.in ↗"),
    ("facegallery", "03", "ANDROID · ON-DEVICE ML", "Face Gallery",
     "Offline gallery in the style of Google Photos, with on-device face grouping: ML Kit detection, "
     "5-point alignment and MobileFaceNet embeddings. 0% wrong faces on LFW.",
     ["Kotlin", "Compose", "ML Kit", "LiteRT", "Room"], GREEN, "view source →"),
    ("chess", "04", "ANDROID · GAME ENGINE", "Chess Trainer",
     "Bots at levels 1–10 with a live coach: threats, the opponent's plan, hints and move grades. "
     "The chess engine is written from scratch. Glass and 3D board styles.",
     ["Kotlin", "Compose", "Custom engine"], "#FBBF24", "view source →"),
    ("friday", "05", "DESKTOP · AI AGENT", "FRIDAY",
     "macOS AI desktop assistant powered by Claude. It edits files, runs builds and uses Git through "
     "a permissioned, audited tool layer, and keeps its memory in Markdown.",
     ["Electron", "React", "TypeScript", "Claude API"], VIOLET, "view source →"),
    ("apklab", "06", "DESKTOP · ANDROID TOOLING", "APKLab",
     "macOS desktop app to pull and push APKs between your computer and connected "
     "Android devices, with no command line needed.",
     ["Flutter", "macOS", "ADB"], "#60A5FA", "view source →"),
]


def card(slug, idx, kicker, title, desc, chips, accent, footer):
    w, h = 620, 260
    lines = textwrap.wrap(desc, 66)[:3]
    desc_svg = "".join(
        f'<text x="32" y="{132 + i*23}" class="sans" font-size="15" fill="{MUTED}">{escape(l)}</text>'
        for i, l in enumerate(lines))
    chip_svg, cx = [], 32
    for c in chips:
        cw = len(c) * 7.6 + 22
        chip_svg.append(
            f'<rect x="{cx}" y="{h-58}" width="{cw}" height="26" rx="13" fill="{BG}" stroke="{BORDER}"/>'
            f'<text x="{cx + cw/2}" y="{h-40.5}" text-anchor="middle" class="mono" font-size="12" fill="#C9D1D9">{escape(c)}</text>')
        cx += cw + 8
    body = f"""<defs>
  <radialGradient id="glow" cx="1" cy="0" r="0.9">
    <stop offset="0" stop-color="{accent}" stop-opacity="0.22"/><stop offset="1" stop-color="{accent}" stop-opacity="0"/>
  </radialGradient>
  {grid_pattern("dots", 20, BORDER, 0.35)}
  <clipPath id="c"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="16"/></clipPath>
</defs>
<g clip-path="url(#c)">
  <rect width="{w}" height="{h}" fill="{PANEL}"/>
  <rect width="{w}" height="{h}" fill="url(#dots)"/>
  <rect width="{w}" height="{h}" fill="url(#glow)"/>
  <rect width="{w}" height="3" fill="{accent}"/>
</g>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="16" stroke="{BORDER}" stroke-width="1.5"/>
<text x="32" y="46" class="mono" font-size="12" fill="{accent}" letter-spacing="1.2">{escape(kicker)}</text>
<text x="{w-32}" y="46" text-anchor="end" class="mono" font-size="12" fill="{DIM}">{idx}</text>
<text x="31" y="92" class="sans" font-size="30" font-weight="800" fill="{TEXT}" letter-spacing="-0.5">{escape(title)}</text>
{desc_svg}
{''.join(chip_svg)}
<text x="{w-32}" y="{h-40.5}" text-anchor="end" class="mono" font-size="12" fill="{accent}">{escape(footer)}</text>"""
    write(f"card-{slug}.svg", body, w, h)


# ---- footer --------------------------------------------------------------
def footer():
    w, h = 1280, 90
    body = f"""<defs>
  <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{VIOLET}"/>
  </linearGradient>
</defs>
<rect x="0" y="0" width="{w}" height="1.5" fill="url(#accent)" opacity="0.6"/>
<text x="{w/2}" y="52" text-anchor="middle" class="mono" font-size="15" fill="{MUTED}">
  <tspan fill="{GREEN}">➜</tspan>  open to conversations about <tspan fill="{TEXT}">mobile SDKs</tspan>, <tspan fill="{TEXT}">Flutter/RN plugins</tspan> &amp; <tspan fill="{TEXT}">Android</tspan><tspan class="cursor" fill="{VIOLET}"> ▍</tspan>
</text>"""
    write("footer.svg", body, w, h)


if __name__ == "__main__":
    header()
    metrics()
    for s in SECTIONS:
        section(*s)
    for c in CARDS:
        card(*c)
    footer()
