# story.json + work/timing.json -> site/index.html (HyperFrames composition, 1080x1920).
# usage: python3 build.py PROJECT_DIR
import json, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from art import BG, DEFS, bust, cast_defs

P = os.path.abspath(sys.argv[1])
S = json.load(open(f"{P}/story.json")); TM = json.load(open(f"{P}/work/timing.json"))
L, CAST = S["lines"], S["cast"]
VO_END = TM["total"]
T = [TM["lines"][f"{n:02d}"][0] for n in range(1, len(L) + 1)]
E = [TM["lines"][f"{n:02d}"][1] for n in range(1, len(L) + 1)]
OUTRO = 2.2; END = round(VO_END + OUTRO, 3)

H, J, SFX = [], [], []  # html, gsap lines, (file, t, vol)
sfx = lambda f, t, v=.6: SFX.append((f, max(0, t), v))

for n, ln in enumerate(L):
    sid = f"s{n + 1}"; a = 0 if n == 0 else T[n] - .05; b = T[n + 1] - .05 if n + 1 < len(L) else END
    sc = ln.get("scene", {}); chars = sc.get("chars", [])
    figs = ""
    for j, c in enumerate(chars):
        who = c["who"]; hid = f"{sid}{who}{j}"
        x, y, s = c.get("x", 540), c.get("y", 1150), c.get("s", 1.3)
        figs += bust(hid, who, CAST[who], x, y, s, c.get("face", "neutral"), c.get("look", 0), c.get("flip", False))
        J.append(f'tl.fromTo("#{hid}b",{{scaleY:1}},{{scaleY:1.03,duration:1.1,yoyo:true,repeat:{int((b - a) / 1.1)},ease:"sine.inOut",transformOrigin:"50% 100%",immediateRender:false}},{a:.3f});')
        amp = 1.2 if CAST[who].get("skin") == "ghost" else 2.4
        J.append(f'tl.fromTo("#{hid}",{{rotation:-{amp}}},{{rotation:{amp},duration:1.4,yoyo:true,repeat:{int((b - a) / 1.4)},ease:"sine.inOut",transformOrigin:"50% 90%",immediateRender:false}},{a:.3f});')
        if CAST[who].get("skin") != "ghost" and c.get("face") not in ("creepy", "sleep"):
            t = a + .8
            while t < b - .3: J.append(f'blink("#{hid}",{t:.3f});'); t += 2.7
        if c.get("talk"):
            J.append(f'tl.to("#{hid}m",{{attr:{{d:"M-18 54 Q0 80 18 54"}},duration:.11,yoyo:true,repeat:{max(1, int((E[n] - T[n]) / .22) * 2 - 1)},ease:"none"}},{T[n]:.3f});')
    extra = f'<svg class="sv" viewBox="0 0 1080 1920">{sc.get("extra", "")}{figs}</svg>'
    H.append(f'<div class="L" id="{sid}"><div class="cam">{BG[sc.get("bg", "room_night")]()}{extra}</div></div>')
    J.append(f'show("#{sid}",{a:.3f},{b:.3f});cam("#{sid} .cam",{a:.3f},{b:.3f},{sc.get("push", 1.35 if ln.get("twist") else 1.14)});')
    if sc.get("shake"):
        J.append(f'tl.fromTo("#{sid} .cam",{{x:-14}},{{x:14,duration:.05,yoyo:true,repeat:9,ease:"none",immediateRender:false}},{T[n]:.3f});')
    if n: sfx("whoosh.wav", a - .12, .25)
    if ln.get("twist"):
        sfx("boom.wav", T[n], .8); sfx("sting.wav", T[n] - .05, .6)
        J.append(f'tl.fromTo("#{sid}",{{scale:1.18}},{{scale:1,duration:.35,ease:"expo.out",immediateRender:false}},{T[n]:.3f});'
                 f'tl.fromTo("#red",{{opacity:.5}},{{opacity:0,duration:.6}},{T[n]:.3f});')
    for f in ln.get("sfx", []):
        f, off = (f, 0) if isinstance(f, str) else f
        sfx(f"{f}.wav", T[n] + off, .8)
    cd = ln.get("card")
    if cd:
        ca, cb = T[n] + .35, min(E[n] + .35, b - .05); cid = f"cd{n + 1}"
        H.append(f'<div class="card" id="{cid}"><div class="k">{cd["k"]}</div><div class="n"><span id="{cid}n">{cd["n"]}</span><small>{cd.get("u", "")}</small></div>'
                 f'<div class="s">{cd.get("s", "")}</div><div class="src">{cd["src"]}</div></div>')
        J.append(f'card("#{cid}",{ca:.3f},{cb:.3f});')
        if str(cd["n"]).replace(",", "").isdigit(): J.append(f'count("#{cid}n",{int(str(cd["n"]).replace(",", ""))},{ca:.3f});')
        sfx("whoosh.wav", ca - .1, .2); sfx("pop.wav", ca + .02, .35)
    ck = ln.get("clock")
    if ck:
        J.append(f'clock("{ck["t"]}","{ck.get("s", "")}",{T[n]:.3f},{min(E[n] + .3, b):.3f});'); sfx("tick.wav", T[n], .5)
    # captions: "chunk|chunk|*yellow key|!red pill", one chunk at a time, timed by character share
    chunks = (ln.get("cap") or ln["vo"].replace(" ", "|")).split("|")
    def strip(c): return c.replace("*", "").replace("!", "")
    def mark(c):  # text before the marker stays white, the rest is the key
        for mk, cls in (("!", "r"), ("*", "y")):
            if mk in c: a, b = c.split(mk, 1); return f'{a}<span class="{cls}">{b}</span>'
        return c
    tot = sum(len(strip(c)) for c in chunks); x = T[n]
    for j, c in enumerate(chunks):
        nx = x + (E[n] - T[n]) * len(strip(c)) / tot; cid = f"c{n + 1}_{j}"
        H.append(f'<div class="th" id="{cid}">{mark(c)}</div>')
        J.append(f'show("#{cid}",{x - .05:.3f},{(nx - .05 if j < len(chunks) - 1 else E[n] + .12):.3f});'); x = nx
    if ln.get("en"):
        H.append(f'<div class="en" id="e{n + 1}">{ln["en"]}</div>'); J.append(f'show("#e{n + 1}",{T[n] - .05:.3f},{E[n] + .12:.3f});')

rnd = random.Random(3)
J.append('tl.to(".flk",{keyframes:[' + ",".join(f'{{opacity:{rnd.uniform(.45, 1):.2f},duration:{rnd.uniform(.1, .28):.2f}}}' for _ in range(int(END * 6))) + ']},0);')
J.append(f'tl.fromTo("#outro",{{opacity:0,y:60}},{{opacity:1,y:0,duration:.45,ease:"back.out(1.6)"}},{VO_END - .2:.3f});')
sfx("pop.wav", VO_END - .2, .4)
SFXH = "\n".join(f'<audio src="a/{f}" data-start="{t:.2f}" data-duration="{min(2.5, END - t):.2f}" data-volume="{v}"></audio>' for f, t, v in SFX)
CAPS = "".join(h for h in H if 'class="th"' in h or 'class="en"' in h)
BODY = "\n".join(h for h in H if 'class="th"' not in h and 'class="en"' not in h)

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#120c09}
#root{position:absolute;inset:0;overflow:hidden;font-family:'Kanit';color:#fff}
.L{position:absolute;inset:0;visibility:hidden;overflow:hidden}.cam{position:absolute;inset:0}
.sv{position:absolute;inset:0;width:1080px;height:1920px}
#cap{position:absolute;left:0;right:0;top:1420px;height:220px;text-align:center;z-index:20}
#cap .th{position:absolute;left:0;right:0;top:0;visibility:hidden;font:800 82px/1.25 'Kanit';color:#fff;white-space:nowrap;text-shadow:0 5px 0 rgba(0,0,0,.45),0 0 34px rgba(0,0,0,.7)}
#cap .y{color:#f3c94b}#cap .r{background:#d8392f;border-radius:14px;padding:0 18px;text-shadow:none}
#cap .en{position:absolute;left:0;right:0;top:122px;visibility:hidden;font:700 34px 'Inter Tight';color:#f1ece0;white-space:nowrap;text-shadow:0 3px 10px rgba(0,0,0,.8)}
.card{position:absolute;left:70px;top:170px;width:940px;padding:30px 40px 24px;border-radius:12px;background:#f0eadc;color:#17151a;box-shadow:0 18px 40px rgba(0,0,0,.5);opacity:0;z-index:15}
.card .k{font:700 34px 'Kanit';color:#3a342c}.card .n{font:800 128px/1.05 'Inter Tight';margin-top:4px;white-space:nowrap}
.card .n small{font:700 48px 'Kanit';margin-left:14px;color:#3a342c}
.card .s{font:600 30px 'Kanit';color:#2a2620;margin-top:6px}.card .src{font:500 22px 'Inter Tight';color:#8a8578;margin-top:10px}
.chip{position:absolute;left:60px;top:60px;padding:12px 24px;border-radius:14px;background:rgba(240,234,220,.95);color:#17151a;display:flex;gap:14px;align-items:center;z-index:16;opacity:0}
.chip b{font:800 44px 'Inter Tight'}.chip small{font:600 28px 'Kanit';color:#5a5348}.chip .dot{width:22px;height:22px;border-radius:50%;background:#2a2550;box-shadow:inset -7px -3px 0 #f3e9c8}
#red{position:absolute;inset:0;background:#c0261c;mix-blend-mode:multiply;opacity:0;z-index:12}
#outro{position:absolute;left:90px;right:90px;top:180px;padding:44px 40px;border-radius:22px;background:#f0eadc;color:#17151a;text-align:center;opacity:0;z-index:25;box-shadow:0 24px 60px rgba(0,0,0,.6)}
#outro b{display:block;font:800 52px 'Kanit'}#outro small{display:block;font:600 30px 'Kanit';color:#5a5348;margin-top:8px}
#grain{position:absolute;inset:0;z-index:30;pointer-events:none;mix-blend-mode:overlay}
"""
html = f"""<!doctype html><html lang="th"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080, height=1920">
<!-- generated by build.py from story.json, edit story.json instead -->
<link href="https://fonts.googleapis.com/css2?family=Kanit:wght@500;600;700;800;900&family=Inter+Tight:wght@500;600;700;800&display=block" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>{CSS}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{END}" data-width="1080" data-height="1920">
<audio src="a/vo.wav" data-start="0" data-duration="{END}" data-volume="1"></audio>
<audio src="a/bed.wav" data-start="0" data-duration="{END}" data-volume="0.28"></audio>
{SFXH}
<svg width="0" height="0" style="position:absolute"><defs>{DEFS}{cast_defs(CAST)}</defs></svg>
{BODY}
<div id="red"></div>
<div class="chip" id="clk"><span class="dot"></span><b id="clkt"></b><small id="clks"></small></div>
<div id="cap">{CAPS}</div>
<div id="outro"><b>{S.get("outro", "ติดตามตอนต่อไป")}</b></div>
<svg id="grain" viewBox="0 0 1080 1920"><filter id="gr"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="9"/><feColorMatrix values="0 0 0 0 .5 0 0 0 0 .5 0 0 0 0 .5 0 0 0 .22 0"/></filter><rect width="1080" height="1920" filter="url(#gr)"/></svg>
</div>
<script>
window.__timelines=window.__timelines||{{}};
gsap.set(".lid",{{scaleY:0,transformOrigin:"50% 0%"}});gsap.set(".kc",{{scaleY:1}});
const tl=gsap.timeline({{paused:true}});window.__timelines["main"]=tl;
const show=(e,a,b)=>{{tl.set(e,{{visibility:"visible"}},a);if(b!==undefined)tl.set(e,{{visibility:"hidden"}},b);}};
const cam=(e,a,b,z)=>{{const k=(a*7)%2<1?1:-1;tl.fromTo(e,{{scale:1.0,x:0}},{{scale:z,x:36*k,y:-20,duration:b-a,ease:"none",immediateRender:false}},a);}};
const card=(e,a,b)=>{{tl.fromTo(e,{{opacity:0,scale:1.15,filter:"blur(12px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:.45,ease:"back.out(1.7)",immediateRender:false}},a);
 tl.to(e,{{y:-10,rotation:-.6,duration:Math.max(.1,b-a-.7),ease:"none"}},a+.45);tl.to(e,{{opacity:0,y:-60,duration:.22,ease:"power2.in"}},b-.22);}};
const count=(e,n,a)=>{{const o={{v:0}};tl.to(o,{{v:n,duration:.8,ease:"power2.out",onUpdate:()=>{{document.querySelector(e).textContent=Math.round(o.v).toLocaleString("en-US");}}}},a);}};
const blink=(e,a)=>{{tl.to([e+"kl",e+"kr"],{{scaleY:1,duration:.06,yoyo:true,repeat:1,ease:"none"}},a);}};
const clock=(t,s,a,b)=>{{tl.set("#clkt",{{textContent:t}},a);tl.set("#clks",{{textContent:s}},a);tl.fromTo("#clk",{{opacity:0,y:-30}},{{opacity:1,y:0,duration:.35,ease:"back.out(1.6)",immediateRender:false}},a);tl.to("#clk",{{opacity:0,duration:.2}},b-.2);}};
{chr(10).join(J)}
tl.set({{}},{{}},{END});
</script></body></html>"""
k = [0]
def _id(m): k[0] += 1; return f'<audio id="m{k[0]}"'
import re
html = re.sub(r"<audio(?! id=)", _id, html)
open(f"{P}/site/index.html", "w").write(html)
print(f"build ok: {len(L)} scenes, {END:.1f}s -> {P}/site/index.html")
