#!/usr/bin/env python3
"""Profile hero banner v2 — animated, self-contained SVG (dark + light).

Effects (all SMIL / CSS inside the SVG, so they work through <img>):
  * drifting aurora blobs
  * twinkling starfield
  * HUD scan beam + corner ticks
  * typewriter reveal of the code card, looping
  * travelling highlight across the name
  * streaming divider (divider.svg)
"""
import pathlib
import random
from xml.sax.saxutils import escape

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1120, 380
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
SANS = "ui-sans-serif,-apple-system,'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif"

CYCLE = 16.0  # code-card loop, seconds

PALETTE = {
    "dark": dict(
        bg1="#05070E", bg2="#0A1220", bg3="#0E1729",
        text="#EAF0FA", sub="#93A5C0", faint="#5F7288",
        accent="#22D3EE", accent2="#8B5CF6", accent3="#14B8A6",
        card="rgba(10,17,30,0.72)", stroke="rgba(255,255,255,0.11)",
        grid="rgba(255,255,255,0.05)", chip="rgba(34,211,238,0.09)",
        chipText="#7DD3FC", chipStroke="rgba(34,211,238,0.30)",
        glow1="rgba(34,211,238,0.24)", glow2="rgba(139,92,246,0.24)",
        glow3="rgba(20,184,166,0.20)",
        kw="#C084FC", punct="#7C8CA6", str="#6EE7B7", ident="#E2E8F5",
        shadow="0.45", star="#BFE9F5", scan="rgba(34,211,238,0.55)",
        shine="#FFFFFF", shineOp="0.45",
    ),
    "light": dict(
        bg1="#FFFFFF", bg2="#F3F7FF", bg3="#E6EEFC",
        text="#0B1220", sub="#4E5D77", faint="#8494AC",
        accent="#0891B2", accent2="#7C3AED", accent3="#0D9488",
        card="rgba(255,255,255,0.94)", stroke="rgba(11,18,32,0.13)",
        grid="rgba(11,18,32,0.055)", chip="rgba(8,145,178,0.07)",
        chipText="#0E7490", chipStroke="rgba(8,145,178,0.24)",
        glow1="rgba(34,211,238,0.28)", glow2="rgba(139,92,246,0.18)",
        glow3="rgba(20,184,166,0.16)",
        kw="#7C3AED", punct="#64748B", str="#047857", ident="#16213A",
        shadow="0.16", star="#7DD3FC", scan="rgba(8,145,178,0.35)",
        shine="#0891B2", shineOp="0.30",
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

TX, TY, TW, TH = 616, 56, 432, 268


def keyframes_type(i):
    """width keyTimes/values for a staggered typewriter reveal inside CYCLE."""
    start = (0.6 + i * 0.62) / CYCLE
    end = start + 0.30 / CYCLE
    kt = f"0;{start:.3f};{end:.3f};0.94;1"
    return kt, "0;0;420;420;0"


def terminal(p):
    x, y, cw, ch = TX, TY, TW, TH
    out = [
        f'<clipPath id="cardClip"><rect x="{x+2}" y="{y+2}" width="{cw-4}" height="{ch-4}" rx="15"/></clipPath>',
        '<g filter="url(#cardShadow)">',
        f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="16" fill="{p["card"]}" stroke="{p["stroke"]}" stroke-width="1.5"/>',
        "</g>",
        # animated border sheen
        f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="16" fill="none" stroke="url(#edge)" stroke-width="1.6" opacity="0.9"/>',
        f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="16" fill="none" stroke="{p["accent"]}" stroke-width="2.2" '
        f'stroke-dasharray="170 1300" stroke-linecap="round" opacity="0.7">'
        f'<animate attributeName="stroke-dashoffset" values="1470;0" dur="6s" repeatCount="indefinite"/></rect>',
        f'<line x1="{x}" y1="{y+44}" x2="{x+cw}" y2="{y+44}" stroke="{p["stroke"]}" stroke-width="1"/>',
    ]
    for i, dot in enumerate(["#FF5F57", "#FEBC2E", "#28C840"]):
        out.append(f'<circle cx="{x+22+i*18}" cy="{y+23}" r="4.6" fill="{dot}" opacity="0.9"/>')
    out.append(
        f'<text x="{x+76}" y="{y+27}" font-family="{MONO}" font-size="11.5" fill="{p["faint"]}" '
        f'letter-spacing="0.3">profile.ts</text>'
    )
    out.append(
        f'<circle cx="{x+cw-24}" cy="{y+23}" r="3.4" fill="{p["accent"]}">'
        f'<animate attributeName="opacity" values="0.25;1;0.25" dur="2.4s" repeatCount="indefinite"/></circle>'
        f'<text x="{x+cw-34}" y="{y+27}" text-anchor="end" font-family="{MONO}" font-size="10.5" '
        f'fill="{p["faint"]}" letter-spacing="0.8">LIVE</text>'
    )

    body = []
    base = y + 78
    for idx, line in enumerate(CODE):
        ly = base + idx * 27
        kt, vals = keyframes_type(idx)
        body.append(
            f'<clipPath id="ln{idx}"><rect x="{x+40}" y="{ly-14}" width="0" height="26">'
            f'<animate attributeName="width" values="{vals}" keyTimes="{kt}" dur="{CYCLE}s" '
            f'repeatCount="indefinite" calcMode="linear"/></rect></clipPath>'
        )
        body.append(
            f'<text x="{x+34}" y="{ly+4}" text-anchor="end" font-family="{MONO}" font-size="10" '
            f'fill="{p["faint"]}" opacity="0.45">{idx+1}</text>'
        )
        spans = "".join(f'<tspan fill="{p[k]}">{escape(v)}</tspan>' for k, v in line)
        body.append(
            f'<text xml:space="preserve" x="{x+50}" y="{ly+4}" font-family="{MONO}" font-size="13" '
            f'fill="{p["ident"]}" clip-path="url(#ln{idx})">{spans}</text>'
        )

    cy = base + 5 * 27
    body.append(
        f'<rect x="{x+72}" y="{cy-7}" width="7.5" height="16" rx="1" fill="{p["accent"]}">'
        f'<animate attributeName="opacity" values="1;1;0;0;1" dur="1.4s" repeatCount="indefinite"/></rect>'
    )
    # status bar
    bar_y = y + ch - 26
    body.append(f'<line x1="{x+1}" y1="{bar_y}" x2="{x+cw-1}" y2="{bar_y}" stroke="{p["stroke"]}" stroke-width="1"/>')
    body.append(
        f'<text x="{x+18}" y="{bar_y+17}" font-family="{MONO}" font-size="10" fill="{p["accent"]}" '
        f'letter-spacing="0.5">↯ main</text>'
        f'<text x="{x+96}" y="{bar_y+17}" font-family="{MONO}" font-size="10" fill="{p["faint"]}" '
        f'letter-spacing="0.6">TypeScript</text>'
        f'<text x="{x+cw-18}" y="{bar_y+17}" text-anchor="end" font-family="{MONO}" font-size="10" '
        f'fill="{p["faint"]}" letter-spacing="0.6">UTF-8 · LF</text>'
    )

    # scanlines overlay
    body.append(
        f'<rect x="{x}" y="{y+44}" width="{cw}" height="{ch-44}" fill="url(#scanlines)" opacity="0.5"/>'
    )

    out.append('<g clip-path="url(#cardClip)">')
    out.append("\n".join(body))
    # sweep highlight inside the card
    out.append(
        f'<rect x="{x-160}" y="{y}" width="140" height="{ch}" fill="url(#sheen)" opacity="0.38">'
        f'<animate attributeName="x" values="{x-160};{x+cw}" dur="7s" begin="2s" repeatCount="indefinite"/></rect>'
    )
    out.append("</g>")
    return "\n".join(out)


def stars(p, n=46, seed=7):
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        sx = rnd.uniform(24, W - 24)
        sy = rnd.uniform(20, H - 20)
        r = rnd.choice([0.7, 0.9, 1.1, 1.4, 1.8])
        dur = round(rnd.uniform(2.4, 6.5), 2)
        dly = round(rnd.uniform(0, 4), 2)
        op = round(rnd.uniform(0.25, 0.85), 2)
        out.append(
            f'<circle cx="{sx:.0f}" cy="{sy:.0f}" r="{r}" fill="{p["star"]}" opacity="{op}">'
            f'<animate attributeName="opacity" values="{op};0.08;{op}" dur="{dur}s" begin="{dly}s" '
            f'repeatCount="indefinite"/></circle>'
        )
    return "\n".join(out)


def build(mode):
    p = PALETTE[mode]
    p = dict(p)
    # token aliases
    p["p"] = p["punct"]

    chips, cx = [], 84
    for label in CHIPS:
        w = 20 + len(label) * 11.6
        chips.append(
            f'<g><rect x="{cx}" y="252" width="{w:.0f}" height="30" rx="15" fill="{p["chip"]}" stroke="{p["chipStroke"]}"/>'
            f'<text x="{cx+w/2:.0f}" y="272" text-anchor="middle" font-family="{SANS}" font-size="12" '
            f'font-weight="600" fill="{p["chipText"]}">{label}</text></g>'
        )
        cx += w + 10

    stats = [("REPOS", "7"), ("STARS", "16"), ("SINCE", "2015")]
    stats_svg, sx = [], 84
    for k, v in stats:
        stats_svg.append(
            f'<text x="{sx}" y="344" font-family="{MONO}" font-size="11" letter-spacing="2" fill="{p["faint"]}">{k}</text>'
            f'<text x="{sx+len(k)*8+12}" y="344" font-family="{MONO}" font-size="12" font-weight="600" fill="{p["accent"]}">{v}</text>'
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
      <stop offset="62%" stop-color="{p['text']}"/>
      <stop offset="100%" stop-color="{p['accent']}"/>
    </linearGradient>
    <linearGradient id="shine" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{p['shine']}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{p['shine']}" stop-opacity="{p['shineOp']}"/>
      <stop offset="100%" stop-color="{p['shine']}" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{p['accent']}"/>
      <stop offset="100%" stop-color="{p['accent2']}" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="edge" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{p['accent']}" stop-opacity="0.75"/>
      <stop offset="45%" stop-color="{p['accent2']}" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="{p['accent']}" stop-opacity="0.6"/>
    </linearGradient>

    <linearGradient id="sheen" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{p['accent']}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{p['accent']}" stop-opacity="0.12"/>
      <stop offset="100%" stop-color="{p['accent']}" stop-opacity="0"/>
    </linearGradient>

    <linearGradient id="beam" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{p['scan']}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{p['scan']}" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="{p['scan']}" stop-opacity="0"/>
    </linearGradient>

    <radialGradient id="g1" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{p['glow1']}"/>
      <stop offset="100%" stop-color="{p['glow1']}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="g2" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{p['glow2']}"/>
      <stop offset="100%" stop-color="{p['glow2']}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="g3" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{p['glow3']}"/>
      <stop offset="100%" stop-color="{p['glow3']}" stop-opacity="0"/>
    </radialGradient>

    <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">
      <path d="M32 0H0V32" fill="none" stroke="{p['grid']}" stroke-width="1"/>
    </pattern>
    <pattern id="scanlines" width="4" height="4" patternUnits="userSpaceOnUse">
      <rect width="4" height="1.2" fill="{p['accent']}" opacity="0.05"/>
    </pattern>

    <filter id="cardShadow" x="-25%" y="-25%" width="150%" height="160%">
      <feDropShadow dx="0" dy="18" stdDeviation="24" flood-color="#000" flood-opacity="{p['shadow']}"/>
    </filter>
    <filter id="nameGlow" x="-20%" y="-40%" width="140%" height="180%">
      <feGaussianBlur stdDeviation="14"/>
    </filter>
    <clipPath id="nameClip">
      <text x="82" y="160" font-family="{SANS}" font-size="60" font-weight="800" letter-spacing="-1.4">liuxing7954</text>
    </clipPath>
    <filter id="softGlow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="7"/>
    </filter>
  </defs>

  <rect width="{W}" height="{H}" fill="url(#bg)"/>

  <!-- aurora -->
  <g>
    <ellipse cx="140" cy="80" rx="430" ry="300" fill="url(#g1)">
      <animate attributeName="cx" values="140;220;140" dur="19s" repeatCount="indefinite"/>
      <animate attributeName="cy" values="80;130;80" dur="23s" repeatCount="indefinite"/>
    </ellipse>
    <ellipse cx="980" cy="300" rx="400" ry="270" fill="url(#g2)">
      <animate attributeName="cx" values="980;900;980" dur="21s" repeatCount="indefinite"/>
      <animate attributeName="cy" values="300;250;300" dur="17s" repeatCount="indefinite"/>
    </ellipse>
    <ellipse cx="640" cy="380" rx="520" ry="220" fill="url(#g3)">
      <animate attributeName="cx" values="640;740;640" dur="26s" repeatCount="indefinite"/>
    </ellipse>
  </g>

  <rect width="{W}" height="{H}" fill="url(#grid)" opacity="0.55"/>
  {stars(p)}

  <!-- HUD scan beam -->
  <rect x="0" y="-1" width="{W}" height="90" fill="url(#beam)" opacity="0.35">
    <animate attributeName="y" values="-90;{H}" dur="9s" begin="1.5s" repeatCount="indefinite"/>
  </rect>

  <rect x="1" y="1" width="{W-2}" height="{H-2}" fill="none" stroke="{p['stroke']}" stroke-width="2"/>

  <g fill="none" stroke="{p['accent']}" stroke-width="2.4" stroke-linecap="round">
    <path d="M22 46V22h24">
      <animate attributeName="opacity" values="0.35;0.85;0.35" dur="3.6s" repeatCount="indefinite"/>
    </path>
    <path d="M{W-22} {H-46}v24h-24">
      <animate attributeName="opacity" values="0.85;0.35;0.85" dur="3.6s" repeatCount="indefinite"/>
    </path>
  </g>

  <circle cx="86" cy="76" r="3.6" fill="{p['accent']}">
    <animate attributeName="r" values="3.2;4.4;3.2" dur="2s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.55;1;0.55" dur="2s" repeatCount="indefinite"/>
  </circle>
  <text x="100" y="80" font-family="{MONO}" font-size="11.5" letter-spacing="3.2" fill="{p['accent']}">GITHUB PROFILE</text>
  <text x="286" y="80" font-family="{MONO}" font-size="11" letter-spacing="1.4" fill="{p['faint']}">/ SINCE 2015</text>

  <!-- name with breathing glow -->
  <text x="84" y="162" font-family="{SANS}" font-size="60" font-weight="800" letter-spacing="-1.4"
        fill="{p['accent']}" filter="url(#nameGlow)" opacity="0.28">liuxing7954
    <animate attributeName="opacity" values="0.22;0.42;0.22" dur="5.5s" repeatCount="indefinite"/>
  </text>
  <text x="82" y="160" font-family="{SANS}" font-size="60" font-weight="800" letter-spacing="-1.4" fill="url(#name)">liuxing7954</text>
  <g clip-path="url(#nameClip)">
    <rect x="-240" y="88" width="150" height="104" fill="url(#shine)">
      <animate attributeName="x" values="-240;1140" dur="6.5s" begin="0.8s" repeatCount="indefinite"/>
    </rect>
  </g>

  <text x="84" y="198" font-family="{SANS}" font-size="18" font-weight="500" fill="{p['sub']}">Java 后端 · 微信生态 · AI 工具链</text>
  <rect x="84" y="216" width="160" height="3" rx="1.5" fill="url(#rule)">
    <animate attributeName="width" values="88;176;88" dur="5s" repeatCount="indefinite"/>
  </rect>

  {''.join(chips)}

  <line x1="84" y1="316" x2="592" y2="316" stroke="{p['stroke']}" stroke-width="1"/>
  {''.join(stats_svg)}

  {terminal(p)}
</svg>
"""


DIVIDER = """<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="22" viewBox="0 0 1120 22" role="img" aria-label="">
  <defs>
    <linearGradient id="d" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="1120" y2="0">
      <stop offset="0%" stop-color="{a}" stop-opacity="0"/>
      <stop offset="22%" stop-color="{a}" stop-opacity="0.35"/>
      <stop offset="50%" stop-color="{b}" stop-opacity="0.55"/>
      <stop offset="78%" stop-color="{a}" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="{a}" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="dot" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="{b}" stop-opacity="0.95"/>
      <stop offset="100%" stop-color="{b}" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <line x1="0" y1="11" x2="1120" y2="11" stroke="url(#d)" stroke-width="1.1"/>
  <g>
    <circle cx="-40" cy="11" r="12" fill="url(#dot)" opacity="0.5">
      <animate attributeName="cx" values="-20;1140;-20" dur="11s" repeatCount="indefinite"/>
    </circle>
    <circle cx="-40" cy="11" r="2.6" fill="{b}">
      <animate attributeName="cx" values="-20;1140;-20" dur="11s" repeatCount="indefinite"/>
    </circle>
  </g>
</svg>
"""


for mode in ("dark", "light"):
    path = OUT / f"banner-{mode}.svg"
    path.write_text(build(mode), encoding="utf-8")
    print("wrote", path)

for mode in ("dark", "light"):
    p = PALETTE[mode]
    (OUT / f"divider-{mode}.svg").write_text(
        DIVIDER.format(a=p["accent"], b=p["accent2"]), encoding="utf-8"
    )
    print("wrote", OUT / f"divider-{mode}.svg")
