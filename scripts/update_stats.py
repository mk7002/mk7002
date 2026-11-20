#!/usr/bin/env python3
"""Builds the activity card and contribution heatmap from GitHub's public contribution calendars.

Run locally or from .github/workflows/update-stats.yml:  python3 scripts/update_stats.py
Standard library only; needs no token.
"""
import datetime as dt
import re
import urllib.request
from xml.sax.saxutils import escape as esc

from theme import (ACCENT_GRADIENT, BG, BLUE, BORDER, DIM, MUTED, SURFACE, TEXT, VIOLET,
                   write_svg)

ACCOUNTS = ["mk7002", "MilindWebEngage"]  # personal + work account
ACCOUNTS_LABEL = "mk7002 + MilindWebEngage (work)"
LEVEL_COLORS = [SURFACE, "#2A1D5C", "#4527A0", VIOLET, BLUE]


def fetch_calendar(user):
    req = urllib.request.Request(f"https://github.com/users/{user}/contributions",
                                 headers={"User-Agent": "profile-readme-stats"})
    html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")
    dates = dict(re.findall(r'data-date="(\d{4}-\d{2}-\d{2})"\s+id="([^"]+)"', html))
    if not dates:  # attribute order fallback
        dates = {d: i for i, d in re.findall(r'id="([^"]+)"[^>]*data-date="(\d{4}-\d{2}-\d{2})"', html)}
    id_to_date = {v: k for k, v in dates.items()}
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


def level(n, cuts):
    if n == 0:
        return 0
    return 1 + sum(n > c for c in cuts)


def heatmap(days, total, name="contributions.svg", cell=17, gap=4, caption_text=None):
    left, top = 64, 58
    first = dt.date.fromisoformat(days[0][0])
    offset = (first.weekday() + 1) % 7  # Sunday = row 0
    nonzero = sorted(n for _, n in days if n)
    cuts = [nonzero[int(len(nonzero) * q)] for q in (0.25, 0.5, 0.75)] if nonzero else [1, 2, 3]
    weeks = (len(days) + offset + 6) // 7
    w = left + weeks * (cell + gap) + 40
    h = top + 7 * (cell + gap) + 70
    rects, months, last_month = [], [], None
    for i, (day, n) in enumerate(days):
        col, row = divmod(i + offset, 7)
        x, y = left + col * (cell + gap), top + row * (cell + gap)
        rects.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="4" fill="{LEVEL_COLORS[level(n, cuts)]}">'
                     f'<title>{n} on {day}</title></rect>')
        d = dt.date.fromisoformat(day)
        if d.day <= 7 and row == 0 and d.month != last_month:
            months.append(f'<text x="{x}" y="{top - 14}" class="mono" font-size="13" fill="{MUTED}">{d.strftime("%b")}</text>')
            last_month = d.month
    labels = "".join(f'<text x="{left - 14}" y="{top + r * (cell + gap) + 13}" text-anchor="end" class="mono" font-size="12" fill="{DIM}">{t}</text>'
                     for r, t in ((1, "Mon"), (3, "Wed"), (5, "Fri")))
    ly = top + 7 * (cell + gap) + 32
    legend_x = w - 40 - 5 * (cell + gap) - 46
    legend = (f'<text x="{legend_x - 10}" y="{ly + 13}" text-anchor="end" class="mono" font-size="12" fill="{DIM}">Less</text>'
              + "".join(f'<rect x="{legend_x + i * (cell + gap)}" y="{ly}" width="{cell}" height="{cell}" rx="4" fill="{c}"/>'
                        for i, c in enumerate(LEVEL_COLORS))
              + f'<text x="{legend_x + 5 * (cell + gap) + 6}" y="{ly + 13}" class="mono" font-size="12" fill="{DIM}">More</text>')
    caption_text = caption_text or f"contributions in the last year · {ACCOUNTS_LABEL}"
    caption = (f'<text x="{left}" y="{ly + 13}" class="mono" font-size="13" fill="{MUTED}">'
               f'<tspan fill="{TEXT}" font-weight="700">{total:,}</tspan> {esc(caption_text)}</text>')
    body = f"""<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="16" fill="{BG}" stroke="{BORDER}" stroke-width="1.5"/>
{''.join(months)}{labels}
{''.join(rects)}
{caption}{legend}"""
    write_svg(name, body, w, h, f"{total} {caption_text}")


def stat_cells(stats, w, h, cols, num_size, label_size):
    rows = (len(stats) + cols - 1) // cols
    cw, rh = w / cols, (h - 70) / rows
    out = []
    for i, (num, label) in enumerate(stats):
        cx = cw * (i % cols) + cw / 2
        cy = 70 + rh * (i // cols) + rh / 2 + num_size * 0.15
        out.append(f'<text x="{cx}" y="{cy}" text-anchor="middle" class="sans" font-size="{num_size}" font-weight="800" fill="url(#accent)">{esc(num)}</text>'
                   f'<text x="{cx}" y="{cy + label_size * 2}" text-anchor="middle" class="mono" font-size="{label_size}" fill="{MUTED}" letter-spacing="1">{esc(label.upper())}</text>')
    return "".join(out)


def stats_card(stats, updated):
    for name, w, h, cols, ns, ls, ts in (("stats.svg", 1280, 200, 4, 42, 13, 14),
                                          ("stats-mobile.svg", 720, 380, 2, 54, 17, 18)):
        body = f"""<defs>{ACCENT_GRADIENT}</defs>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="18" fill="{SURFACE}" stroke="{BORDER}" stroke-width="1.5"/>
<text x="36" y="46" class="mono" font-size="{ts}" fill="{BLUE}" letter-spacing="1.5">LAST 12 MONTHS</text>
<text x="{w - 36}" y="46" text-anchor="end" class="mono" font-size="{ts - 2}" fill="{DIM}">updated {updated}</text>
{stat_cells(stats, w, h, cols, ns, ls)}"""
        write_svg(name, body, w, h, " · ".join(f"{n} {l}" for n, l in stats))


def main():
    cal = combined_calendar()
    today = dt.date.today().isoformat()
    days = sorted((d, n) for d, n in cal.items() if d <= today)[-371:]
    total = sum(n for _, n in days[-365:])
    active = sum(1 for _, n in days[-365:] if n)
    longest, current = streaks(days[-365:])
    stats = [(f"{total:,}", "Contributions"), (str(active), "Active days"),
             (f"{longest}d", "Longest streak"), (f"{current}d", "Current streak")]
    stats_card(stats, today)
    heatmap(days, total)
    recent = days[-182:]
    while dt.date.fromisoformat(recent[0][0]).weekday() != 6:  # start on a Sunday
        recent = recent[1:]
    heatmap(recent, sum(n for _, n in recent), "contributions-mobile.svg", cell=22, gap=5,
            caption_text="in the last 6 months")


if __name__ == "__main__":
    main()
