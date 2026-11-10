#!/usr/bin/env python3
"""Generate the profile hero banner (dark + light) as self-contained SVG."""
import pathlib
from xml.sax.saxutils import escape

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1120, 360
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
SANS = "ui-sans-serif,-apple-system,'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif"

PALETTE = {
    "dark": dict(
        bg1="#070A12", bg2="#0C1524", bg3="#101B2E",
        text="#EAF0FA", sub="#8FA1BC", faint="#5F7288",
        accent="#22D3EE", accent2="#8B5CF6",
        card="rgba(255,255,255,0.045)", stroke="rgba(255,255,255,0.10)",
        grid="rgba(255,255,255,0.045)", chip="rgba(34,211,238,0.10)",
        chipText="#7DD3FC", chipStroke="rgba(34,211,238,0.26)",
        glow1="rgba(34,211,238,0.20)", glow2="rgba(139,92,246,0.18)",
        kw="#C084FC", punct="#7C8CA6", str="#6EE7B7", ident="#DCE6F5",
        shadow="0.26",
    ),
    "light": dict(
        bg1="#FFFFFF", bg2="#F4F7FE", bg3="#E9EFFB",
        text="#0B1220", sub="#54637C", faint="#8494AC",
        accent="#0891B2", accent2="#7C3AED",
        card="rgba(255,255,255,0.98)", stroke="rgba(11,18,32,0.14)",
        grid="rgba(11,18,32,0.05)", chip="rgba(8,145,178,0.08)",
        chipText="#0E7490", chipStroke="rgba(8,145,178,0.22)",
        glow1="rgba(34,211,238,0.20)", glow2="rgba(139,92,246,0.13)",
        kw="#7C3AED", punct="#64748B", str="#047857", ident="#1E293B",
        shadow="0.16",
    ),
}

CHIPS = ["Java · Spring", "TypeScript", "微信小程序", "AI Agent"]

CODE = [
    [("kw", "const"), ("punct", " "), ("ident", "profile"), ("punct", " = {")],
    [("punct", "  stack:"), ("punct", " ["), ("str", '"Java"'), ("punct", ", "), ("str", '"Spring"'), ("punct", "],")],
    [("punct", "  lang:"), ("punct", "  ["), ("str", '"TypeScript"'), ("punct", ", "), ("str", '"SQL"'), ("punct", "],")],
    [("punct", "  ship:"), ("punct", "  "), ("str", '"微信小程序 · Agent 工具"'), ("punct", ",")],
    [("punct", "  motto:"), ("punct", " "), ("str", '"把重复劳动交给机器"'), ("punct", ",")],
    [("punct", "};")],
]

TX, TY, TW, TH = 628, 44, 420, 268


def terminal(p):
    x, y, cw, ch = TX, TY, TW, TH
    out = [
        '<g filter="url(#softShadow)">',
        f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="16" fill="{p["card"]}" stroke="{p["stroke"]}" stroke-width="1.5"/>',
        "</g>",
        f'<line x1="{x}" y1="{y+44}" x2="{x+cw}" y2="{y+44}" stroke="{p["stroke"]}" stroke-width="1"/>',
    ]
    for i, dot in enumerate(["#FF5F57", "#FEBC2E", "#28C840"]):
        out.append(f'<circle cx="{x+22+i*18}" cy="{y+23}" r="4.6" fill="{dot}" opacity="0.9"/>')
    out.append(
        f'<text x="{x+76}" y="{y+27}" font-family="{MONO}" font-size="11.5" fill="{p["faint"]}" '
        f'letter-spacing="0.3">profile.ts</text>'
    )

    base = y + 76
    for idx, line in enumerate(CODE):
        ly = base + idx * 27
        out.append(
            f'<text x="{x+34}" y="{ly+4}" text-anchor="end" font-family="{MONO}" font-size="10" '
            f'fill="{p["faint"]}" opacity="0.45">{idx+1}</text>'
        )
        spans = "".join(f'<tspan fill="{p[k]}">{escape(v)}</tspan>' for k, v in line)
        out.append(
            f'<text xml:space="preserve" x="{x+50}" y="{ly+4}" font-family="{MONO}" '
            f'font-size="12.5" fill="{p["ident"]}">{spans}</text>'
        )

    cy = base + 5 * 27
    out.append(
        f'<rect x="{x+72}" y="{cy-7}" width="7" height="15" rx="1" fill="{p["accent"]}">'
        f'<animate attributeName="opacity" values="1;1;0;0;1" dur="1.5s" repeatCount="indefinite"/></rect>'
    )
    return "\n".join(out)


def build(mode):
    p = PALETTE[mode]

    chips, cx = [], 84
    for label in CHIPS:
        w = 20 + len(label) * 11.6
        chips.append(
            f'<g><rect x="{cx}" y="246" width="{w:.0f}" height="30" rx="15" fill="{p["chip"]}" stroke="{p["chipStroke"]}"/>'
            f'<text x="{cx+w/2:.0f}" y="266" text-anchor="middle" font-family="{SANS}" font-size="12" '
            f'font-weight="600" fill="{p["chipText"]}">{label}</text></g>'
        )
        cx += w + 10

    stats = [("REPOS", "6"), ("STARS", "16"), ("SINCE", "2015")]
    stats_svg, sx = [], 84
    for k, v in stats:
        stats_svg.append(
            f'<text x="{sx}" y="330" font-family="{MONO}" font-size="11" letter-spacing="2" fill="{p["faint"]}">{k}</text>'
            f'<text x="{sx+len(k)*8+12}" y="330" font-family="{MONO}" font-size="12" font-weight="600" fill="{p["accent"]}">{v}</text>'
        )
        sx += 112

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="liuxing7954 — Java 后端 / 微信生态 / AI 工具链">
  <title>liuxing7954</title>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{p['bg1']}"/>
      <stop offset="55%" stop-color="{p['bg2']}"/>
      <stop offset="100%" stop-color="{p['bg3']}"/>
    </linearGradient>
    <linearGradient id="name" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{p['text']}"/>
      <stop offset="68%" stop-color="{p['text']}"/>
      <stop offset="100%" stop-color="{p['accent']}"/>
    </linearGradient>
    <linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{p['accent']}"/>
      <stop offset="100%" stop-color="{p['accent2']}" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="g1" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{p['glow1']}"/>
      <stop offset="100%" stop-color="{p['glow1']}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="g2" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{p['glow2']}"/>
      <stop offset="100%" stop-color="{p['glow2']}" stop-opacity="0"/>
    </radialGradient>
    <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">
      <path d="M32 0H0V32" fill="none" stroke="{p['grid']}" stroke-width="1"/>
    </pattern>
    <filter id="softShadow" x="-25%" y="-25%" width="150%" height="160%">
      <feDropShadow dx="0" dy="16" stdDeviation="22" flood-color="#000" flood-opacity="{p['shadow']}"/>
    </filter>
  </defs>

  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <rect width="{W}" height="{H}" fill="url(#grid)" opacity="0.5"/>
  <ellipse cx="130" cy="70" rx="420" ry="280" fill="url(#g1)"/>
  <ellipse cx="1000" cy="320" rx="380" ry="260" fill="url(#g2)"/>
  <rect x="1" y="1" width="{W-2}" height="{H-2}" fill="none" stroke="{p['stroke']}" stroke-width="2"/>

  <g fill="none" stroke="{p['accent']}" stroke-width="2.4" stroke-linecap="round" opacity="0.7">
    <path d="M22 46V22h24"/><path d="M{W-22} {H-46}v24h-24"/>
  </g>

  <text x="84" y="80" font-family="{MONO}" font-size="11.5" letter-spacing="3.2" fill="{p['accent']}">GITHUB PROFILE</text>
  <text x="278" y="80" font-family="{MONO}" font-size="11" letter-spacing="1.4" fill="{p['faint']}">/ SINCE 2015</text>

  <text x="82" y="160" font-family="{SANS}" font-size="60" font-weight="800" letter-spacing="-1.4" fill="url(#name)">liuxing7954</text>
  <text x="84" y="198" font-family="{SANS}" font-size="18" font-weight="500" fill="{p['sub']}">Java 后端 · 微信生态 · AI 工具链</text>
  <rect x="84" y="216" width="160" height="3" rx="1.5" fill="url(#rule)"/>

  {''.join(chips)}

  <line x1="84" y1="306" x2="600" y2="306" stroke="{p['stroke']}" stroke-width="1"/>
  {''.join(stats_svg)}

  {terminal(p)}
</svg>
"""


for mode in ("dark", "light"):
    path = OUT / f"banner-{mode}.svg"
    path.write_text(build(mode), encoding="utf-8")
    print("wrote", path)
