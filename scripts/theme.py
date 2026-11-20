"""Shared design tokens and SVG helpers for the profile README assets."""
import os
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")

# Palette
BG = "#0B0D12"        # midnight black
SURFACE = "#171B2B"   # charcoal
BORDER = "#262B3D"
VIOLET = "#7C3AED"
VIOLET_SOFT = "#A78BFA"
BLUE = "#38BDF8"
TEXT = "#E5E7EB"
MUTED = "#9CA3AF"
DIM = "#6B7280"

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, Roboto, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'JetBrains Mono', Menlo, Consolas, monospace"

STYLE = f"""<style>
  .sans {{ font-family: {SANS}; }}
  .mono {{ font-family: {MONO}; }}
</style>"""

ACCENT_GRADIENT = f"""<linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{VIOLET_SOFT}"/><stop offset="0.45" stop-color="{VIOLET}"/><stop offset="1" stop-color="{BLUE}"/>
  </linearGradient>"""


def write_svg(name, body, w, h, title=None):
    t = f"<title>{escape(title)}</title>\n" if title else ""
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
           f'fill="none" role="img">\n{t}{STYLE}\n{body}\n</svg>\n')
    path = os.path.join(ASSETS, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote", os.path.relpath(path, ROOT))


def panel(w, h, rx=18, glow=True, clip_id="frame"):
    """Background panel: charcoal-on-black with a faint grid and corner glows."""
    glows = ""
    if glow:
        glows = f"""
  <rect width="{w}" height="{h}" fill="url(#glowV)"/>
  <rect width="{w}" height="{h}" fill="url(#glowB)"/>"""
    defs = f"""<defs>
  {ACCENT_GRADIENT}
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M40 0H0V40" stroke="{TEXT}" stroke-opacity="0.035"/>
  </pattern>
  <radialGradient id="glowV" cx="0.1" cy="0" r="0.75">
    <stop offset="0" stop-color="{VIOLET}" stop-opacity="0.32"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="glowB" cx="1" cy="1" r="0.7">
    <stop offset="0" stop-color="{BLUE}" stop-opacity="0.16"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/>
  </radialGradient>
  <clipPath id="{clip_id}"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{rx}"/></clipPath>
</defs>"""
    bg = f"""<g clip-path="url(#{clip_id})">
  <rect width="{w}" height="{h}" fill="{BG}"/>
  <rect width="{w}" height="{h}" fill="url(#grid)"/>{glows}
</g>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{rx}" stroke="{BORDER}" stroke-width="1.5"/>"""
    return defs, bg
