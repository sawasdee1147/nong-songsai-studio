# Flat 2.5D cartoon art: characters (head r=100 at 0,0, bust down to y=470) + backgrounds (1080x1920 SVG).
# Everything is code-drawn SVG: no AI images, no stock, no copyright issues.

SKIN = {"tan": ("#e2a874", "#c08453", "#94603a"), "light": ("#f3d2b3", "#dcae88", "#ad7f5c"),
        "dark": ("#a8704a", "#7f4f31", "#55331f"), "ghost": ("#e6dccb", "#c9bfae", "#959a8c")}
MOUTH = {"neutral": "M-22 58 Q0 66 22 58", "smile": "M-28 52 Q0 76 28 52", "sad": "M-22 66 Q0 52 22 66",
         "angry": "M-22 64 Q0 54 22 64", "scared": "M-14 60 Q0 44 14 60 Q0 80 -14 60Z", "creepy": "M-36 48 Q0 90 36 48"}
TALK = "M-18 54 Q0 80 18 54"
BROW = {"neutral": ("M-56 -40 Q-36 -50 -16 -42", "M16 -42 Q36 -50 56 -40"),
        "smile": ("M-56 -44 Q-36 -54 -16 -46", "M16 -46 Q36 -54 56 -44"),
        "sad": ("M-56 -40 Q-36 -44 -16 -56", "M16 -56 Q36 -44 56 -40"),
        "scared": ("M-56 -46 Q-36 -52 -16 -60", "M16 -60 Q36 -52 56 -46"),
        "angry": ("M-58 -54 Q-36 -46 -14 -36", "M14 -36 Q36 -46 58 -54"),
        "creepy": ("M-56 -42 Q-36 -46 -16 -44", "M16 -44 Q36 -46 56 -42")}
HAIR_FRONT = {
    "short": '<path d="M-100 -8 C-104 -90 -40 -118 4 -116 C58 -116 108 -84 100 -10 C88 -52 60 -70 30 -74 C-10 -66 -60 -70 -100 -8Z" fill="{h}"/>',
    "long": '<path d="M-104 0 C-110 -96 -30 -122 8 -118 C70 -116 112 -80 104 2 C96 -40 70 -66 40 -72 C20 -50 -30 -40 -60 -44 C-80 -40 -96 -24 -104 0Z" fill="{h}"/>',
    "bun": '<path d="M-100 -14 C-100 -96 -40 -116 0 -116 C40 -116 100 -96 100 -14 C80 -60 40 -78 0 -78 C-40 -78 -80 -60 -100 -14Z" fill="{h}"/><circle cy="-128" r="40" fill="{h}"/>',
    "bald": '<ellipse cx="-30" cy="-62" rx="26" ry="12" fill="#fff" opacity=".18"/>',
}
HAIR_BACK = {"long": '<path d="M-118 -10 C-130 -130 130 -130 118 -10 L170 200 C120 240 -120 240 -170 200Z" fill="{h}"/>'}


def shade(hexc, f):
    c = [int(hexc[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{max(0, min(255, int(v * f))):02x}" for v in c)


def cast_defs(cast):
    """Per-character gradients: skin + shirt."""
    o = ""
    for cid, c in cast.items():
        a, b, d = SKIN[c.get("skin", "tan")]
        o += (f'<radialGradient id="sk{cid}" cx=".38" cy=".32" r=".8"><stop offset="0" stop-color="{a}"/>'
              f'<stop offset=".7" stop-color="{b}"/><stop offset="1" stop-color="{d}"/></radialGradient>')
        sh = c.get("shirt", "#3a4a76")
        o += (f'<linearGradient id="sh{cid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{sh}"/>'
              f'<stop offset="1" stop-color="{shade(sh, .5)}"/></linearGradient>')
    return o


def eyes(i, cid, pupil, look, closed=False):
    o = ""
    for side, ex in (("l", -36), ("r", 36)):
        o += (f'<ellipse cx="{ex}" cy="-4" rx="21" ry="25" fill="#f4f1ea"/>'
              f'<circle cx="{ex + look}" cy="-1" r="{pupil}" fill="#15121a"/><circle cx="{ex + look + 4}" cy="-6" r="3.2" fill="#fff" opacity=".85"/>'
              f'<ellipse id="{i}k{side}" cx="{ex}" cy="-4" rx="23" ry="27" fill="url(#sk{cid})" class="lid{" kc" if closed else ""}"/>')
    return o


def head(i, cid, c, face="neutral", look=0):
    """i = unique element id; face = neutral|smile|sad|angry|scared|creepy|sleep."""
    hair = c.get("hair_color", "#17131a")
    ghost = c.get("skin") == "ghost"
    closed = face == "sleep"
    f = "neutral" if closed else face
    pupil = {"scared": 7, "creepy": 15}.get(f, 14 if ghost else 11)
    lx = {"left": -10, "right": 10}.get(look, 0)
    sk = f"url(#sk{cid})"
    o = f'<g id="{i}" class="hd">'
    o += f'<ellipse cx="-98" cy="6" rx="16" ry="24" fill="{sk}"/><ellipse cx="98" cy="6" rx="16" ry="24" fill="{sk}"/>' if c.get("hair") != "long" else ""
    o += f'<circle r="100" fill="{sk}"/>' + HAIR_FRONT[c.get("hair", "short")].format(h=hair)
    if ghost:
        o += '<ellipse cx="-36" cy="22" rx="24" ry="9" fill="#7d8578" opacity=".35"/><ellipse cx="36" cy="22" rx="24" ry="9" fill="#7d8578" opacity=".35"/>'
    bl, br = BROW[f]
    o += "".join(f'<path d="{d}" stroke="{shade(hair, 1.4)}" stroke-width="7" fill="none" stroke-linecap="round"/>' for d in (bl, br))
    o += eyes(i, cid, pupil, lx, closed)
    o += '<path d="M-4 18 Q4 34 -8 38" stroke="#000" stroke-opacity=".28" stroke-width="5" fill="none" stroke-linecap="round"/>'
    fill = ' fill="#3a1416"' if f == "scared" else ' fill="none"'
    o += f'<path id="{i}m" d="{MOUTH[f]}" stroke="#5a2e22" stroke-width="7"{fill} stroke-linecap="round"/></g>'
    return o


def bust(i, cid, c, x, y, s, face="neutral", look=0, flip=False):
    hair = c.get("hair_color", "#17131a")
    sk = f"url(#sk{cid})"
    body = HAIR_BACK.get(c.get("hair"), "").format(h=hair)
    body += (f'<rect x="-34" y="70" width="68" height="80" fill="{sk}"/>'
             f'<path d="M-240 470 C-250 300 -200 170 -60 140 L60 140 C200 170 250 300 240 470Z" fill="url(#sh{cid})"/>'
             f'<path d="M-60 140 L0 220 L60 140" fill="{sk}"/>')
    fl = " scale(-1,1)" if flip else ""
    return (f'<g transform="translate({x},{y}) scale({s}){fl}"><g id="{i}b" class="bd">{body}</g>'
            f'{head(i, cid, c, face, look)}</g>')


# ---------- backgrounds (each returns a full-frame SVG) ----------
VIG = '<rect width="1080" height="1920" fill="url(#vig)"/>'


def _sv(inner):
    return f'<svg class="sv" viewBox="0 0 1080 1920">{inner}{VIG}</svg>'


def room(day=False, lamp=True, window=True):
    cols = ["#7a5a3e", "#856345", "#7d5d40", "#8a6848"] if day else ["#4b301e", "#553621", "#4e321f", "#583923"]
    walls = "".join(f'<rect x="{x}" y="0" width="90" height="1500" fill="{c}"/><rect x="{x}" y="0" width="3" height="1500" fill="#2a1a10" opacity=".6"/>'
                    for x, c in zip(range(0, 1080, 90), cols * 3))
    win = (f'<rect x="640" y="380" width="300" height="420" fill="url(#{"day" if day else "dusk"})"/>'
           '<rect x="640" y="380" width="300" height="420" fill="none" stroke="#2a1a10" stroke-width="22"/><rect x="779" y="380" width="22" height="420" fill="#2a1a10"/>') if window else ""
    lampg = ('<g transform="translate(260,330)"><circle class="flk" r="420" fill="url(#lampglow)"/><line x1="0" y1="-330" x2="0" y2="-40" stroke="#1b120c" stroke-width="5"/>'
             '<path d="M-40 -40 L40 -40 L52 60 L-52 60Z" fill="#ffcf7a" opacity=".95"/><path d="M-40 -40 L40 -40 L52 60 L-52 60Z" fill="none" stroke="#2a1a10" stroke-width="8"/></g>') if lamp and not day else ""
    lines = "".join(f'<rect x="0" y="{y}" width="1080" height="4" fill="#1d120b" opacity=".7"/>' for y in (1540, 1640, 1760, 1880))
    return _sv(f'{walls}{win}<rect y="1460" width="1080" height="460" fill="url(#floor)"/>{lines}{lampg}')


def village():
    return _sv('<rect width="1080" height="1920" fill="url(#dusk)"/><circle cx="250" cy="760" r="70" fill="#f6c27a" opacity=".9"/>'
               '<circle class="flk" cx="250" cy="760" r="320" fill="url(#lampglow)"/>'
               '<path d="M0 1050 Q200 1000 420 1040 Q640 990 860 1035 Q980 1015 1080 1030 L1080 1200 L0 1200Z" fill="#2a2036"/>'
               '<g fill="#18121d"><path d="M80 1130 L80 900 L40 900 L170 780 L300 900 L260 900 L260 1130Z"/>'
               '<path d="M880 1120 L880 920 L840 920 L960 820 L1070 920 L1040 920 L1040 1120Z"/>'
               '<path d="M420 1190 L420 860 L360 860 L540 640 L720 860 L660 860 L660 1190Z"/></g>'
               '<rect x="500" y="900" width="80" height="110" fill="#ffb25a"/><circle class="flk" cx="540" cy="955" r="260" fill="url(#lampglow)"/>'
               '<rect y="1190" width="1080" height="730" fill="url(#earth)"/>')


def street():
    bld = "".join(f'<rect x="{x}" y="{y}" width="{w}" height="{1300 - y}" fill="{c}"/>' for x, y, w, c in
                  [(0, 520, 260, "#1d1a2e"), (240, 360, 220, "#232038"), (450, 600, 200, "#1a1729"), (640, 300, 240, "#211e35"), (870, 480, 210, "#1c192c")])
    win = "".join(f'<rect x="{x}" y="{y}" width="34" height="46" fill="#ffcf7a" opacity="{o}"/>' for x, y, o in
                  [(40, 600, .8), (120, 700, .5), (290, 420, .9), (370, 520, .4), (300, 640, .7), (500, 680, .6), (690, 380, .8), (780, 480, .5), (700, 600, .9), (920, 560, .7), (1000, 680, .4)])
    lamp = ('<rect x="840" y="760" width="14" height="560" fill="#0e0c16"/><path d="M800 760 L900 760 L880 790 L820 790Z" fill="#0e0c16"/>'
            '<circle class="flk" cx="850" cy="800" r="380" fill="url(#lampglow)"/>')
    return _sv(f'<rect width="1080" height="1920" fill="url(#night)"/>{bld}{win}{lamp}<rect y="1300" width="1080" height="620" fill="#15131c"/>'
               + "".join(f'<rect x="{x}" y="1600" width="120" height="14" fill="#c9b878" opacity=".5"/>' for x in (60, 340, 620, 900)))


def forest():
    trees = "".join(f'<path d="M{x} 1400 L{x - w} 1400 L{x} {y} L{x + w} 1400Z" fill="{c}"/>' for x, y, w, c in
                    [(90, 560, 150, "#0f1a16"), (330, 700, 120, "#132019"), (560, 480, 170, "#0d1713"), (800, 640, 140, "#12201a"), (1010, 520, 160, "#0e1814")])
    return _sv('<rect width="1080" height="1920" fill="url(#night)"/><circle cx="780" cy="330" r="90" fill="#efe6c8"/>'
               '<circle cx="780" cy="330" r="300" fill="url(#moonglow)"/>' + trees +
               '<rect y="1380" width="1080" height="540" fill="url(#earth)"/><rect y="1240" width="1080" height="260" fill="#cfd6e0" opacity=".12"/>')


def office(night=False):
    wall = "#2b3040" if night else "#cfc6b4"
    glow = '<circle class="flk" cx="540" cy="1080" r="460" fill="url(#screenglow)"/>' if night else ""
    return _sv(f'<rect width="1080" height="1920" fill="{wall}"/><rect x="120" y="300" width="360" height="460" fill="url(#{"night" if night else "day"})"/>'
               '<rect x="120" y="300" width="360" height="460" fill="none" stroke="#3a3328" stroke-width="18"/>'
               f'{glow}<rect y="1420" width="1080" height="500" fill="#3a2e24"/><rect y="1400" width="1080" height="34" fill="#5a4636"/>'
               '<rect x="380" y="1060" width="320" height="200" rx="10" fill="#15161c"/><rect x="396" y="1076" width="288" height="168" fill="#5fb0ff" opacity=".75"/>'
               '<rect x="520" y="1260" width="40" height="140" fill="#15161c"/>')


def dark():
    return _sv('<rect width="1080" height="1920" fill="#0d0a0c"/><circle cx="540" cy="900" r="620" fill="url(#spot)"/>')


BG = {"room_night": lambda: room(), "room_day": lambda: room(day=True), "village_dusk": village, "street_night": street,
      "forest_night": forest, "office_day": lambda: office(), "office_night": lambda: office(True), "dark": dark}

DEFS = """
<radialGradient id="vig" cx=".5" cy=".45" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".7"/></radialGradient>
<radialGradient id="lampglow"><stop offset="0" stop-color="#ffb04a" stop-opacity=".55"/><stop offset="1" stop-color="#ffb04a" stop-opacity="0"/></radialGradient>
<radialGradient id="moonglow"><stop offset="0" stop-color="#efe6c8" stop-opacity=".35"/><stop offset="1" stop-color="#efe6c8" stop-opacity="0"/></radialGradient>
<radialGradient id="screenglow"><stop offset="0" stop-color="#5fb0ff" stop-opacity=".35"/><stop offset="1" stop-color="#5fb0ff" stop-opacity="0"/></radialGradient>
<radialGradient id="spot"><stop offset="0" stop-color="#3a2a22" stop-opacity="1"/><stop offset="1" stop-color="#0d0a0c" stop-opacity="0"/></radialGradient>
<linearGradient id="dusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1f1c44"/><stop offset=".55" stop-color="#5a3a62"/><stop offset=".8" stop-color="#c0645a"/><stop offset="1" stop-color="#e9a35e"/></linearGradient>
<linearGradient id="day" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7fb6e0"/><stop offset="1" stop-color="#e8e2c8"/></linearGradient>
<linearGradient id="night" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b0b1e"/><stop offset=".7" stop-color="#1e1b3a"/><stop offset="1" stop-color="#2c2445"/></linearGradient>
<linearGradient id="floor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4a2f1c"/><stop offset="1" stop-color="#20140b"/></linearGradient>
<linearGradient id="earth" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3d2c1c"/><stop offset="1" stop-color="#170f09"/></linearGradient>
"""
