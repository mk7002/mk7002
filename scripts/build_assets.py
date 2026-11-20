#!/usr/bin/env python3
"""Builds the static SVG assets (hero, metrics, section headers, timeline).

Edit the data below and run:  python3 scripts/build_assets.py
Activity graphs are built separately by scripts/update_stats.py.
"""
from xml.sax.saxutils import escape as esc

from theme import (BG, BLUE, BORDER, DIM, MUTED, SURFACE, TEXT, VIOLET, VIOLET_SOFT,
                   ACCENT_GRADIENT, panel, write_svg)

NAME = "Milind Keni"
KICKER = "SENIOR SOFTWARE ENGINEER  ·  WEBENGAGE"
TAGLINE = "Android & Cross-Platform Engineering"
TYPED = "building mobile SDKs, developer tools & AI agents"
PLATFORMS = "Android  ·  iOS  ·  Flutter  ·  React Native  ·  Cordova  ·  Capacitor"

METRICS = [
    ("8+", "Years in software"),
    ("280+", "Public SDK commits"),
    ("120K+", "Play Store installs"),
    ("24+", "Production apps"),
]

SECTIONS = [
    ("intro", "01", "Introduction"),
    ("stack", "02", "Technology stack"),
    ("expertise", "03", "Engineering expertise"),
    ("experience", "04", "Experience"),
    ("playstore", "05", "Published apps"),
    ("projects", "06", "Featured projects"),
    ("sideprojects", "07", "Side projects"),
    ("opensource", "08", "Open-source contributions"),
    ("exploring", "09", "Currently exploring"),
    ("activity", "10", "GitHub activity"),
]

# (company, role, start year as float, end year or None for present, label for dates)
ROLES = [
    ("Inspeero Technologies", "Android Developer", 2018.25, 2021.0, "Apr 2018 – Jan 2021"),
    ("Image Online", "Android Developer", 2021.0, 2022.6, "Jan 2021 – Aug 2022"),
    ("WebEngage", "Senior Software Engineer", 2022.6, None, "Aug 2022 – present"),
]
TIMELINE_END = 2026.9  # "now" on the axis


def typed_line(x, y, size, prompt_color, text, char_w):
    """Monospace line that types itself once, then leaves a blinking cursor.

    The base state is fully visible, so renderers without SMIL support show the whole line."""
    full = (len(text) + 2) * char_w
    return f"""<clipPath id="typeclip"><rect x="{x}" y="{y - size}" width="{full}" height="{size * 1.6}">
    <animate attributeName="width" values="0;{full}" dur="2.2s" begin="0.3s" fill="freeze"/>
  </rect></clipPath>
  <g clip-path="url(#typeclip)">
    <text x="{x}" y="{y}" class="mono" font-size="{size}"><tspan fill="{prompt_color}">&gt; </tspan><tspan fill="{TEXT}">{esc(text)}</tspan></text>
  </g>
  <rect x="{x + full + 4}" y="{y - size * 0.8}" width="{size * 0.5}" height="{size}" fill="{BLUE}">
    <animate attributeName="x" values="{x + 4};{x + full + 4}" dur="2.2s" begin="0.3s" fill="freeze"/>
    <animate attributeName="opacity" values="1;0;1" dur="1.1s" begin="2.5s" repeatCount="indefinite" calcMode="discrete"/>
  </rect>"""


def stack_layer(x, y, w, label, text, stroke):
    return f"""<rect x="{x}" y="{y}" width="{w}" height="66" rx="12" fill="{SURFACE}" fill-opacity="0.85" stroke="{stroke}" stroke-opacity="0.7"/>
  <text x="{x + 20}" y="{y + 26}" class="mono" font-size="11.5" fill="{DIM}" letter-spacing="1.5">{esc(label)}</text>
  <text x="{x + 20}" y="{y + 49}" class="sans" font-size="15" fill="{TEXT}">{esc(text)}</text>"""


def hero():
    w, h = 1280, 400
    defs, bg = panel(w, h, rx=20)
    lx, lw = 836, 384
    layers = [
        ("CROSS-PLATFORM", "Flutter · React Native · Cordova · Capacitor", VIOLET_SOFT),
        ("PLUGIN BRIDGE", "Method channels · Native modules · Plugins", VIOLET),
        ("NATIVE SDK", "Android (Kotlin / Java) · iOS (Swift / Obj-C)", BLUE),
    ]
    ys = [86, 170, 254]
    stack = "\n  ".join(stack_layer(lx, y, lw, l, t, c) for (l, t, c), y in zip(layers, ys))
    connectors = ""
    for y in (152, 236):
        cx = lx + lw / 2
        connectors += f"""<line x1="{cx}" y1="{y}" x2="{cx}" y2="{y + 18}" stroke="{BORDER}" stroke-width="2" stroke-dasharray="3 3"/>
  <circle cx="{cx}" cy="{y}" r="3" fill="{BLUE}"><animate attributeName="cy" values="{y};{y + 18}" dur="1.6s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0;1;0" dur="1.6s" repeatCount="indefinite"/></circle>
  """
    body = f"""{defs}
{bg}
<g>
  <text x="72" y="98" class="mono" font-size="15" fill="{BLUE}" letter-spacing="2">{esc(KICKER)}</text>
  <text x="68" y="182" class="sans" font-size="78" font-weight="800" fill="{TEXT}" letter-spacing="-2.5">{esc(NAME)}</text>
  <text x="72" y="232" class="sans" font-size="30" font-weight="650" fill="url(#accent)">{esc(TAGLINE)}</text>
  {typed_line(72, 296, 19, VIOLET_SOFT, TYPED, 11.45)}
  <text x="72" y="350" class="mono" font-size="13.5" fill="{MUTED}">{esc(PLATFORMS)}</text>
</g>
<g>
  {stack}
  {connectors}
</g>
<rect x="0" y="{h - 3}" width="{w}" height="3" fill="url(#accent)" opacity="0.9"/>"""
    write_svg("hero.svg", body, w, h, f"{NAME}: {TAGLINE}")


def hero_mobile():
    w, h = 720, 560
    defs, bg = panel(w, h, rx=24)
    body = f"""{defs}
{bg}
<text x="48" y="92" class="mono" font-size="19" fill="{BLUE}" letter-spacing="2">SENIOR SOFTWARE ENGINEER</text>
<text x="48" y="122" class="mono" font-size="19" fill="{BLUE}" letter-spacing="2">@ WEBENGAGE</text>
<text x="44" y="226" class="sans" font-size="88" font-weight="800" fill="{TEXT}" letter-spacing="-3">{esc(NAME)}</text>
<text x="48" y="290" class="sans" font-size="38" font-weight="650" fill="url(#accent)">Android &amp; Cross-Platform</text>
<text x="48" y="338" class="sans" font-size="38" font-weight="650" fill="url(#accent)">Engineering</text>
{typed_line(48, 418, 22, VIOLET_SOFT, "mobile SDKs · dev tools · AI agents", 13.25)}
<text x="48" y="484" class="mono" font-size="18" fill="{MUTED}">Android · iOS · Flutter · RN · Cordova</text>
<rect x="0" y="{h - 4}" width="{w}" height="4" fill="url(#accent)" opacity="0.9"/>"""
    write_svg("hero-mobile.svg", body, w, h, f"{NAME}: {TAGLINE}")


def metric_cell(cx, y, num, label, num_size, label_size):
    return f"""<text x="{cx}" y="{y}" text-anchor="middle" class="sans" font-size="{num_size}" font-weight="800" fill="url(#accent)">{esc(num)}</text>
  <text x="{cx}" y="{y + label_size * 2.1}" text-anchor="middle" class="mono" font-size="{label_size}" fill="{MUTED}" letter-spacing="1">{esc(label.upper())}</text>"""


def metrics():
    w, h = 1280, 140
    defs = f"<defs>{ACCENT_GRADIENT}</defs>"
    cw = w / len(METRICS)
    cells = []
    for i, (n, l) in enumerate(METRICS):
        if i:
            cells.append(f'<line x1="{i * cw}" y1="34" x2="{i * cw}" y2="{h - 34}" stroke="{BORDER}"/>')
        cells.append(metric_cell(i * cw + cw / 2, 74, n, l, 44, 13))
    body = f"""{defs}
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="16" fill="{SURFACE}" stroke="{BORDER}" stroke-width="1.5"/>
{chr(10).join(cells)}"""
    write_svg("metrics.svg", body, w, h, " · ".join(f"{n} {l}" for n, l in METRICS))


def metrics_mobile():
    w, h = 720, 320
    defs = f"<defs>{ACCENT_GRADIENT}</defs>"
    cells = [f'<line x1="{w / 2}" y1="36" x2="{w / 2}" y2="{h - 36}" stroke="{BORDER}"/>',
             f'<line x1="36" y1="{h / 2}" x2="{w - 36}" y2="{h / 2}" stroke="{BORDER}"/>']
    for i, (n, l) in enumerate(METRICS):
        cx = w / 4 + (i % 2) * w / 2
        cy = 88 + (i // 2) * h / 2
        cells.append(metric_cell(cx, cy, n, l, 56, 17))
    body = f"""{defs}
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="20" fill="{SURFACE}" stroke="{BORDER}" stroke-width="1.5"/>
{chr(10).join(cells)}"""
    write_svg("metrics-mobile.svg", body, w, h, " · ".join(f"{n} {l}" for n, l in METRICS))


def section(slug, num, title):
    w, h = 720, 56
    tx = 58
    line_x = tx + len(title) * 12.2 + 24
    body = f"""<defs>
  <linearGradient id="line" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{VIOLET}" stop-opacity="0.9"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/>
  </linearGradient>
</defs>
<rect x="0" y="14" width="44" height="28" rx="8" fill="{SURFACE}" stroke="{BORDER}"/>
<text x="22" y="33" text-anchor="middle" class="mono" font-size="13" font-weight="600" fill="{BLUE}">{num}</text>
<text x="{tx}" y="36.5" class="sans" font-size="22" font-weight="700" fill="{TEXT}">{esc(title)}</text>
<rect x="{line_x}" y="27.5" width="{w - line_x}" height="1.5" fill="url(#line)"/>"""
    write_svg(f"section-{slug}.svg", body, w, h, f"{num} {title}")

    # Phone variant: narrower viewBox so the title stays ~20px on a 390px screen.
    w, h, tx = 380, 48, 50
    line_x = tx + len(title) * 10.6 + 16
    body = f"""<defs>
  <linearGradient id="line" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{VIOLET}" stop-opacity="0.9"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/>
  </linearGradient>
</defs>
<rect x="0" y="10" width="38" height="28" rx="8" fill="{SURFACE}" stroke="{BORDER}"/>
<text x="19" y="29" text-anchor="middle" class="mono" font-size="12" font-weight="600" fill="{BLUE}">{num}</text>
<text x="{tx}" y="31" class="sans" font-size="19" font-weight="700" fill="{TEXT}">{esc(title)}</text>
""" + (f'<rect x="{line_x}" y="23.5" width="{w - line_x}" height="1.5" fill="url(#line)"/>' if line_x < w - 20 else "")
    write_svg(f"section-{slug}-mobile.svg", body, w, h, f"{num} {title}")


def timeline():
    w, h = 1280, 230
    x0, x1, y0, y1 = 80, 1200, 2018.0, 2027.0
    sx = lambda yr: x0 + (yr - y0) / (y1 - y0) * (x1 - x0)
    colors = [DIM, VIOLET_SOFT, BLUE]
    parts = []
    for yr in range(2018, 2027):
        x = sx(yr)
        parts.append(f'<line x1="{x}" y1="112" x2="{x}" y2="128" stroke="{BORDER}"/>'
                     f'<text x="{x}" y="152" text-anchor="middle" class="mono" font-size="14" fill="{DIM}">{yr}</text>')
    parts.insert(0, f'<rect x="{x0}" y="118" width="{x1 - x0}" height="4" rx="2" fill="{SURFACE}"/>')
    for (company, role, s, e, dates), col in zip(ROLES, colors):
        xs, xe = sx(s), sx(e or TIMELINE_END)
        fill = "url(#accent)" if e is None else col
        parts.append(f'<rect x="{xs + 2}" y="116" width="{xe - xs - 4}" height="8" rx="4" fill="{fill}"/>')
        parts.append(f'<circle cx="{xs + 2}" cy="120" r="6" fill="{BG}" stroke="{col}" stroke-width="2.5"/>')
        mid = (xs + xe) / 2
        parts.append(f'<text x="{mid}" y="70" text-anchor="middle" class="sans" font-size="23" font-weight="700" fill="{TEXT}">{esc(company)}</text>'
                     f'<text x="{mid}" y="98" text-anchor="middle" class="sans" font-size="17" fill="{MUTED}">{esc(role)}</text>'
                     f'<text x="{mid}" y="188" text-anchor="middle" class="mono" font-size="15" fill="{col if e else BLUE}">{esc(dates)}</text>')
    nx = sx(TIMELINE_END)
    parts.append(f'<circle cx="{nx}" cy="120" r="7" fill="{BLUE}"><animate attributeName="r" values="6;9;6" dur="2.4s" repeatCount="indefinite"/></circle>')
    body = f"""<defs>{ACCENT_GRADIENT}</defs>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="16" fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>
{chr(10).join(parts)}"""
    write_svg("timeline.svg", body, w, h, "Experience timeline: " + "; ".join(f"{c}, {r}, {d}" for c, r, _, _, d in ROLES))


def timeline_mobile():
    roles = list(reversed(ROLES))
    step, top = 132, 70
    w, h = 720, top + step * len(roles) + 10
    colors = [BLUE, VIOLET_SOFT, DIM]
    parts = [f'<line x1="64" y1="{top}" x2="64" y2="{top + step * (len(roles) - 1)}" stroke="{BORDER}" stroke-width="3"/>']
    for i, ((company, role, _, e, dates), col) in enumerate(zip(roles, colors)):
        y = top + i * step
        parts.append(f'<circle cx="64" cy="{y}" r="11" fill="{BG}" stroke="{col}" stroke-width="4"/>')
        parts.append(f'<text x="104" y="{y + 10}" class="sans" font-size="32" font-weight="700" fill="{TEXT}">{esc(company)}</text>'
                     f'<text x="104" y="{y + 46}" class="sans" font-size="22" fill="{MUTED}">{esc(role)}</text>'
                     f'<text x="104" y="{y + 78}" class="mono" font-size="19" fill="{col}">{esc(dates)}</text>')
    body = f"""<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="20" fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>
{chr(10).join(parts)}"""
    write_svg("timeline-mobile.svg", body, w, h, "Experience timeline: " + "; ".join(f"{c}, {r}, {d}" for c, r, _, _, d in ROLES))


if __name__ == "__main__":
    hero()
    hero_mobile()
    metrics()
    metrics_mobile()
    for s in SECTIONS:
        section(*s)
    timeline()
    timeline_mobile()


# ---------------------------------------------------------------------------
# Intro: Kotlin "profile.kt" editor card
# ---------------------------------------------------------------------------
import re as _re

KT_DESKTOP = [
    'object Milind : Engineer {',
    '    override val role       = "Senior Software Engineer @ WebEngage"',
    '    override val core       = "Android"                // since 2018, still today',
    '    override val experience = 8.years                  // since Apr 2018',
    '    override val platforms  = listOf("Android", "iOS", "Flutter", "React Native",',
    '                                     "Cordova", "Capacitor", "Unity")',
    '    override val focus      = listOf("Mobile SDKs", "Cross-platform plugins",',
    '                                     "Developer tools", "AI agents")',
    '}',
]
KT_MOBILE = [
    'object Milind : Engineer {',
    '  val role = "Senior Software Engineer"',
    '  val company = "WebEngage"',
    '  val core = "Android" // since 2018',
    '  val experience = 8.years // since 2018',
    '  val platforms = listOf(',
    '    "Android", "iOS", "Flutter",',
    '    "React Native", "Cordova",',
    '    "Capacitor", "Unity")',
    '  val focus = listOf(',
    '    "Mobile SDKs", "Plugins",',
    '    "Developer tools", "AI agents")',
    '}',
]
_KT = _re.compile(r'(//.*$)|("[^"]*")|\b(object|override|val)\b|\b(\d+)\b|\b(Milind|Engineer)\b|(\.years|listOf)')


def kt_line(line):
    out, pos = [], 0
    for m in _KT.finditer(line):
        if m.start() > pos:
            out.append((line[pos:m.start()], TEXT))
        color = [DIM, "#86EFAC", VIOLET_SOFT, BLUE, "#FDE68A", BLUE][[i for i in range(1, 7) if m.group(i)][0] - 1]
        out.append((m.group(0), color))
        pos = m.end()
    out.append((line[pos:], TEXT))
    return "".join(f'<tspan fill="{c}">{esc(t)}</tspan>' for t, c in out if t)


def intro_card(name, lines, w, size, lh, pad):
    bar = 46
    h = bar + pad + len(lines) * lh + pad - lh * 0.35
    rows = "\n".join(
        f'<text x="{pad + 34}" y="{bar + pad + i * lh}" class="mono" font-size="{size - 3}" fill="{DIM}" text-anchor="end">{i + 1}</text>'
        f'<text x="{pad + 56}" y="{bar + pad + i * lh}" class="mono" font-size="{size}" xml:space="preserve">{kt_line(l)}</text>'
        for i, l in enumerate(lines))
    body = f"""<defs><radialGradient id="g" cx="1" cy="0" r="0.8"><stop offset="0" stop-color="{VIOLET}" stop-opacity="0.18"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>
<clipPath id="c"><rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="16"/></clipPath></defs>
<g clip-path="url(#c)"><rect width="{w}" height="{h}" fill="{BG}"/><rect width="{w}" height="{h}" fill="url(#g)"/>
<rect width="{w}" height="{bar}" fill="{SURFACE}"/><line x1="0" y1="{bar}" x2="{w}" y2="{bar}" stroke="{BORDER}"/></g>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="16" stroke="{BORDER}" stroke-width="1.5"/>
<circle cx="26" cy="23" r="6" fill="#FF5F57"/><circle cx="46" cy="23" r="6" fill="#FEBC2E"/><circle cx="66" cy="23" r="6" fill="#28C840"/>
<rect x="92" y="10" width="{len('profile.kt') * 9 + 34}" height="36" rx="8" fill="{BG}"/>
<text x="109" y="33" class="mono" font-size="14" fill="{TEXT}">profile.kt</text>
{rows}"""
    write_svg(name, body, w, round(h), "profile.kt: " + " ".join(l.strip() for l in lines))


# ---------------------------------------------------------------------------
# WebEngage SDK contributions chart
# ---------------------------------------------------------------------------
SDK_ROWS = [  # platform, commits (None = no default-branch commits found), repo count
    ("Flutter", 137, 3), ("iOS", 97, 4), ("React Native · Expo", 39, 5),
    ("Cordova · Ionic · Capacitor", 13, 2), ("Unity", None, 3),
]


def sdk_chart(name, w, label_size, num_size, row_h, label_w, mobile=False):
    pad, top = 40, 92
    h = top + len(SDK_ROWS) * row_h + 34
    mx = max(c for _, c, _ in SDK_ROWS if c)
    rows = []
    for i, (plat, commits, repos) in enumerate(SDK_ROWS):
        y = top + i * row_h
        if mobile:
            ty, by, bx, bw = y, y + 22, pad, w - 2 * pad
        else:
            ty, by, bx, bw = y + 22, y + 8, pad + label_w, w - 2 * pad - label_w - 110
        rows.append(f'<text x="{pad}" y="{ty}" class="sans" font-size="{label_size}" font-weight="600" fill="{TEXT}">{esc(plat)}</text>')
        rows.append(f'<text x="{w - pad}" y="{ty}" text-anchor="end" class="mono" font-size="{label_size - 3}" fill="{DIM}">{repos} repos</text>')
        rows.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="14" rx="7" fill="{SURFACE}"/>')
        if commits:
            fw = max(14, bw * commits / mx)
            rows.append(f'<rect x="{bx}" y="{by}" width="{fw}" height="14" rx="7" fill="url(#accent)"/>')
            rows.append(f'<text x="{bx + fw + 10 if fw < bw - 70 else bx + fw - 10}" y="{by + 12}" '
                        f'text-anchor="{"start" if fw < bw - 70 else "end"}" class="mono" font-size="{num_size}" font-weight="700" '
                        f'fill="{TEXT if fw < bw - 70 else BG}">{commits}</text>')
        else:
            rows.append(f'<text x="{bx + 12}" y="{by + 12}" class="mono" font-size="{num_size}" fill="{MUTED}">contributor</text>')
    body = f"""<defs>{ACCENT_GRADIENT}</defs>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="18" fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>
<text x="{pad}" y="54" class="sans" font-size="{label_size + 10}" font-weight="800" fill="url(#accent)">280+ commits</text>
<text x="{pad + (label_size + 10) * 7.6 + 14}" y="54" class="sans" font-size="{label_size + 1}" fill="{MUTED}">{"" if mobile else "across 15 public WebEngage SDK repositories"}</text>
{chr(10).join(rows)}"""
    write_svg(name, body, w, h, "WebEngage SDK commits by platform: " + "; ".join(f"{p} {c or 'contributor'}" for p, c, _ in SDK_ROWS))


# ---------------------------------------------------------------------------
# Contact footer banner
# ---------------------------------------------------------------------------
def contact_footer(name, w, h, title_size, sub_size, lines):
    defs, bg = panel(w, h, rx=20)
    cy = h / 2 - (len(lines) - 1) * title_size * 0.6
    titles = "".join(
        f'<text x="{w / 2}" y="{cy + i * title_size * 1.15}" text-anchor="middle" class="sans" font-size="{title_size}" '
        f'font-weight="800" letter-spacing="-1.5" fill="{"url(#accent)" if i == len(lines) - 1 else TEXT}">{esc(t)}</text>'
        for i, t in enumerate(lines))
    sub_y = cy + len(lines) * title_size * 1.15 + sub_size * 0.6
    body = f"""{defs}
{bg}
<text x="{w / 2}" y="{cy - title_size * 1.25}" text-anchor="middle" class="mono" font-size="{sub_size - 2}" fill="{BLUE}" letter-spacing="2">MILIND KENI · MUMBAI, INDIA</text>
{titles}
<text x="{w / 2}" y="{sub_y}" text-anchor="middle" class="sans" font-size="{sub_size}" fill="{MUTED}">Mobile SDKs · Cross-platform engineering · Developer tooling</text>
<rect x="0" y="{h - 3}" width="{w}" height="3" fill="url(#accent)" opacity="0.9"/>"""
    write_svg(name, body, w, h, "Contact: " + " ".join(lines))


if __name__ == "__main__":
    intro_card("intro.svg", KT_DESKTOP, 1280, 19, 34, 36)
    intro_card("intro-mobile.svg", KT_MOBILE, 720, 24, 40, 30)
    sdk_chart("sdk.svg", 1280, 19, 15, 58, 330)
    sdk_chart("sdk-mobile.svg", 720, 24, 18, 82, 0, mobile=True)
    contact_footer("contact.svg", 1280, 300, 58, 19, ["Let's build something", "developers love."])
    contact_footer("contact-mobile.svg", 720, 420, 58, 22, ["Let's build", "something", "developers love."])
