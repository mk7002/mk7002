#!/usr/bin/env python3
"""Builds the compact activity card from GitHub's public contribution calendars.

Outputs assets/activity.svg (12 months) and assets/activity-mobile.svg (6 months).
Run locally or from .github/workflows/update-stats.yml:  python3 scripts/update_stats.py
Standard library only; needs no token.
"""
import datetime as dt
import re
import urllib.request
from xml.sax.saxutils import escape as esc

from theme import ACCENT_GRADIENT, BG, BLUE, BORDER, DIM, MUTED, SURFACE, TEXT, VIOLET, write_svg

ACCOUNTS = ["mk7002", "MilindWebEngage"]  # personal + work account
ACCOUNTS_LABEL = "mk7002 + MilindWebEngage (work)"
LEVEL_COLORS = [SURFACE, "#2A1D5C", "#4527A0", VIOLET, BLUE]


def fetch_calendar(user):
    req = urllib.request.Request(f"https://github.com/users/{user}/contributions",
                                 headers={"User-Agent": "profile-readme-stats"})
    html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")
    id_to_date = {i: d for d, i in re.findall(r'data-date="(\d{4}-\d{2}-\d{2})"\s+id="([^"]+)"', html)}
    if not id_to_date:  # attribute order fallback
        id_to_date = dict(re.findall(r'id="([^"]+)"[^>]*data-date="(\d{4}-\d{2}-\d{2})"', html))
    counts = {}
    for cell_id, text in re.findall(r'<tool-tip[^>]*for="([^"]+)"[^>]*>([^<]*)</tool-tip>', html):
        if cell_id in id_to_date:
            m = re.match(r"(\d+)", text.replace(",", ""))
            counts[id_to_date[cell_id]] = int(m.group(1)) if m else 0
    if len(counts) < 300:
        raise SystemExit(f"Could not parse contribution calendar for {user} ({len(counts)} days)")
    return counts


def combined_calendar():
    total = {}
    for user in ACCOUNTS:
        for day, n in fetch_calendar(user).items():
            total[day] = total.get(day, 0) + n
    return total


def streaks(days):
    longest = run = 0
    for _, n in days:
        run = run + 1 if n else 0
        longest = max(longest, run)
    current = 0
    for i, (_, n) in enumerate(reversed(days)):
        if n:
            current += 1
        elif i == 0:
            continue  # today may not have activity yet
        else:
            break
    return longest, current


def grid(days, x0, y0, cell, gap, cuts):
    """Heatmap cells + month labels. Returns (svg, width, height)."""
    offset = (dt.date.fromisoformat(days[0][0]).weekday() + 1) % 7  # Sunday = row 0
    out, last_month = [], None
    for i, (day, n) in enumerate(days):
        col, row = divmod(i + offset, 7)
        x, y = x0 + col * (cell + gap), y0 + row * (cell + gap)
        lvl = 0 if n == 0 else 1 + sum(n > c for c in cuts)
        out.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="{cell * 0.22:.1f}" fill="{LEVEL_COLORS[lvl]}"><title>{n} on {day}</title></rect>')
        d = dt.date.fromisoformat(day)
        if row == 0 and d.day <= 7 and d.month != last_month:
            out.append(f'<text x="{x}" y="{y0 - 12}" class="mono" font-size="{cell * 0.72:.0f}" fill="{MUTED}">{d.strftime("%b")}</text>')
            last_month = d.month
    weeks = (len(days) + offset + 6) // 7
    return "".join(out), weeks * (cell + gap) - gap, 7 * (cell + gap) - gap


def card(name, days, stats, w, cell, gap, stat_cols, num_size, label_size, caption):
    pad = 36
    nonzero = sorted(n for _, n in days if n)
    cuts = [nonzero[int(len(nonzero) * q)] for q in (0.25, 0.5, 0.75)] if nonzero else [1, 2, 3]

    # stats block
    rows = (len(stats) + stat_cols - 1) // stat_cols
    cw = (w - 2 * pad) / stat_cols
    row_h = num_size + label_size + 30
    st = []
    for i, (num, label) in enumerate(stats):
        cx = pad + cw * (i % stat_cols)
        y = 64 + (i // stat_cols) * row_h + num_size * 0.8
        st.append(f'<text x="{cx}" y="{y}" class="sans" font-size="{num_size}" font-weight="800" fill="url(#accent)">{esc(num)}</text>'
                  f'<text x="{cx}" y="{y + label_size + 12}" class="mono" font-size="{label_size}" fill="{MUTED}" letter-spacing="1">{esc(label.upper())}</text>')
    grid_top = 64 + rows * row_h + 34
    cells, gw, gh = grid(days, pad, grid_top, cell, gap, cuts)
    h = grid_top + gh + 64

    ly = h - 30
    legend_x = w - pad - 5 * (cell * 0.8 + 4) - 40
    legend = (f'<text x="{legend_x - 8}" y="{ly}" text-anchor="end" class="mono" font-size="{label_size}" fill="{DIM}">Less</text>'
              + "".join(f'<rect x="{legend_x + i * (cell * 0.8 + 4)}" y="{ly - cell * 0.7}" width="{cell * 0.8}" height="{cell * 0.8}" rx="3" fill="{c}"/>'
                        for i, c in enumerate(LEVEL_COLORS))
              + f'<text x="{legend_x + 5 * (cell * 0.8 + 4) + 4}" y="{ly}" class="mono" font-size="{label_size}" fill="{DIM}">More</text>')
    body = f"""<defs>{ACCENT_GRADIENT}</defs>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="18" fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>
<text x="{pad}" y="44" class="mono" font-size="{label_size + 1}" fill="{BLUE}" letter-spacing="1.5">{esc(caption)}</text>
{''.join(st)}
{cells}
<text x="{pad}" y="{ly}" class="mono" font-size="{label_size}" fill="{DIM}">{esc(ACCOUNTS_LABEL)} · updated {dt.date.today().isoformat()}</text>
{legend}"""
    write_svg(name, body, w, h, f"{caption}: " + " · ".join(f"{n} {l}" for n, l in stats))


def summary(days):
    total = sum(n for _, n in days)
    active = sum(1 for _, n in days if n)
    longest, current = streaks(days)
    return [(f"{total:,}", "Contributions"), (str(active), "Active days"),
            (f"{longest}d", "Longest streak"), (f"{current}d", "Current streak")]


def main():
    cal = combined_calendar()
    today = dt.date.today().isoformat()
    days = sorted((d, n) for d, n in cal.items() if d <= today)
    year = days[-364:]
    card("activity.svg", year, summary(year), 1280, 18, 4, 4, 34, 12, "ACTIVITY · LAST 12 MONTHS")
    half = days[-182:]
    while dt.date.fromisoformat(half[0][0]).weekday() != 6:  # start on a Sunday
        half = half[1:]
    card("activity-mobile.svg", half, summary(half), 720, 21, 4, 2, 44, 15, "ACTIVITY · LAST 6 MONTHS")


if __name__ == "__main__":
    main()
