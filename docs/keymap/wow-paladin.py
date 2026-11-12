"""Render docs/keymap/wow-paladin.svg: where each WoW paladin bind sits on the
Baseform GAME/GFN layers. Edit the tables below as you learn spells, then run:

    python3 docs/keymap/wow-paladin.py
"""
from html import escape
from pathlib import Path

# role -> (fill, stroke)
ROLES = {
    "rot":  ("#fde68a", "#b45309"),  # rotation
    "heal": ("#bbf7d0", "#15803d"),  # heals / defensives
    "cc":   ("#bfdbfe", "#1d4ed8"),  # control / utility
    "buff": ("#e9d5ff", "#7e22ce"),  # buffs, racials, travel
    "ui":   ("#e5e7eb", "#4b5563"),  # WoW windows
    "move": ("#f3f4f6", "#9ca3af"),  # movement / mode keys
    "free": ("#ffffff", "#d1d5db"),  # empty for now
}

# (key label, spell, role); "\n" splits lines
GAME_L = [
    [("TAB", "Target\nenemy", "cc"), ("Q", "Judgement", "rot"), ("W", "Forward", "move"), ("E", "Seal of\nRighteous.", "rot"), ("R", "Holy\nStrike", "rot")],
    [("1", "Holy\nLight", "heal"), ("A", "Strafe ←", "move"), ("S", "Back", "move"), ("D", "Strafe →", "move"), ("F", "Seal of the\nCrusader", "rot")],
    [("2", "Purify", "heal"), ("Z", "Hammer of\nJustice", "cc"), ("X", "lvl 44:\nHam. Wrath", "free"), ("C", "talent:\nConsecr.", "free"), ("V", "lvl 20:\nExorcism", "free")],
]
GAME_LT = [("SHIFT", "hold for\nShift tier", "move"), ("GFN", "hold for\nGFN tier", "move"), ("SPACE", "Jump", "move")]

GAME_R = [
    [("J", "", "free"), ("L", "Quest\nlog", "ui"), ("U", "Reputation", "ui"), ("Y", "", "free"), ("P", "Spellbook", "ui")],
    [("M", "Map", "ui"), ("N", "Talents", "ui"), ("B", "Bags", "ui"), ("I", "", "free"), ("O", "Social", "ui")],
    [("K", "Skills", "ui"), ("H", "Honor", "ui"), ("G", "Character", "ui"), (".", "", "free"), ("/", "/ chat", "ui")],
]
GAME_RT = [("CHAT", "Enter +\nexit game", "move"), ("SPACE", "Jump", "move"), ("ESC", "Close /\nmenu", "move")]

SHIFT_L = [
    [("S-TAB", "", "free"), ("S-Q", "Divine\nProtection", "heal"), ("W", "Forward", "move"), ("S-E", "", "free"), ("S-R", "", "free")],
    [("S-1", "", "free"), ("A", "Strafe ←", "move"), ("S", "Back", "move"), ("D", "Strafe →", "move"), ("S-F", "", "free")],
    [("S-2", "", "free"), ("S-Z", "", "free"), ("S-X", "", "free"), ("S-C", "", "free"), ("S-V", "", "free")],
]
SHIFT_LT = [("SHIFT", "held", "move"), ("—", "", "free"), ("—", "", "free")]

GFN_L = [
    [("EXIT", "Leave\ngame mode", "move"), ("3", "Lay on\nHands", "heal"), ("W", "Forward", "move"), ("4", "Blessing\nof Might", "buff"), ("5", "Devotion\nAura", "buff")],
    [("CHAT", "Enter +\nexit game", "move"), ("A", "Strafe ←", "move"), ("S", "Back", "move"), ("D", "Strafe →", "move"), ("6", "Cannibalize", "buff")],
    [("ESC", "Close /\nmenu", "move"), ("8", "Mount", "buff"), ("9", "Hearth", "buff"), ("0", "Food /\ndrink", "buff"), ("-", "", "free")],
]
GFN_LT = [("—", "", "free"), ("GFN", "held", "move"), ("SPACE", "Jump", "move")]

MOUSE = [("Button4", "Will of the\nForsaken", "buff"), ("Button5", "", "free")]

KW, KH, GAP = 104, 62, 6
PAD, HALF_GAP = 24, 36


def key(x, y, label, spell, role):
    fill, stroke = ROLES[role]
    dash = ' stroke-dasharray="4 3"' if role == "free" else ""
    out = [f'<rect x="{x}" y="{y}" width="{KW}" height="{KH}" rx="7" fill="{fill}" stroke="{stroke}" stroke-width="1.5"{dash}/>',
           f'<text x="{x + 6}" y="{y + 13}" class="k">{escape(label)}</text>']
    lines = spell.split("\n") if spell else []
    cy = y + KH / 2 + 8 - (len(lines) - 1) * 7.5
    for i, line in enumerate(lines):
        out.append(f'<text x="{x + KW / 2}" y="{cy + i * 15}" class="s" text-anchor="middle">{escape(line)}</text>')
    return "\n".join(out)


def half(x0, y0, rows, thumbs, thumbs_right=False):
    out = []
    for r, row in enumerate(rows):
        for c, k in enumerate(row):
            out.append(key(x0 + c * (KW + GAP), y0 + r * (KH + GAP), *k))
    ty = y0 + 3 * (KH + GAP) + 8
    tx0 = x0 if thumbs_right else x0 + 2 * (KW + GAP)
    for i, k in enumerate(thumbs):
        out.append(key(tx0 + i * (KW + GAP), ty, *k))
    return "\n".join(out)


HALF_W = 5 * KW + 4 * GAP
BLOCK_H = 4 * (KH + GAP) + 8 + 40
W = PAD * 2 + HALF_W * 2 + HALF_GAP

parts, y = [], PAD


def title(text, sub=""):
    global y
    parts.append(f'<text x="{PAD}" y="{y + 18}" class="h">{escape(text)}</text>')
    if sub:
        parts.append(f'<text x="{PAD}" y="{y + 36}" class="sub">{escape(sub)}</text>')
    y += 48


title("GAME — tap Q+W+F", "Left hand on the keyboard. Right half = WoW windows when your hand leaves the mouse.")
parts.append(half(PAD, y, GAME_L, GAME_LT))
parts.append(half(PAD + HALF_W + HALF_GAP, y, GAME_R, GAME_RT, thumbs_right=True))
y += BLOCK_H

title("SHIFT tier — hold left outer thumb", "Same keys with Shift held. Empty slots are room to grow.")
parts.append(half(PAD, y, SHIFT_L, SHIFT_LT))
y += BLOCK_H

title("GFN tier — hold left middle thumb", "Situational spells, buffs and travel. Movement keys still work.")
parts.append(half(PAD, y, GFN_L, GFN_LT))
mx = PAD + HALF_W + HALF_GAP
parts.append(f'<text x="{mx}" y="{y + 13}" class="h2">Mouse side buttons</text>')
for i, k in enumerate(MOUSE):
    parts.append(key(mx + i * (KW + GAP), y + 22, *k))

ly = y + 22 + KH + 28
parts.append(f'<text x="{mx}" y="{ly}" class="h2">Colors</text>')
legend = [("rot", "Rotation"), ("heal", "Heals / defensive"), ("cc", "Control / target"), ("buff", "Buffs / racial / travel"), ("ui", "WoW windows"), ("move", "Movement / mode"), ("free", "Empty, fills as you level")]
for i, (role, name) in enumerate(legend):
    fill, stroke = ROLES[role]
    yy = ly + 12 + i * 22
    parts.append(f'<rect x="{mx}" y="{yy}" width="16" height="16" rx="3" fill="{fill}" stroke="{stroke}"/>')
    parts.append(f'<text x="{mx + 24}" y="{yy + 13}" class="s">{escape(name)}</text>')
y += BLOCK_H + 40

H = y + PAD
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>
text {{ font-family: -apple-system, "Helvetica Neue", Arial, sans-serif; fill: #111827; }}
.h {{ font-size: 17px; font-weight: 700; }}
.h2 {{ font-size: 14px; font-weight: 700; }}
.sub {{ font-size: 12px; fill: #4b5563; }}
.k {{ font-size: 10px; font-weight: 700; fill: #6b7280; }}
.s {{ font-size: 12.5px; }}
</style>
<rect width="100%" height="100%" fill="#ffffff"/>
{chr(10).join(parts)}
</svg>
'''
Path(__file__).with_name("wow-paladin.svg").write_text(svg)
print(f"wrote wow-paladin.svg ({W}x{H})")
