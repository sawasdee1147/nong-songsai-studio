#!/usr/bin/env python3
"""story.json + audio/timings.json -> video/index.html (HyperFrames 1080x1920) ในลายเส้นของช่อง

ใช้: python3 tools/story/build.py episodes/<EP>
ต้องมี: <EP>/story.json, <EP>/audio/timings.json, <EP>/audio/mix.wav

story.json (ย่อ):
{
 "next": "ตอนหน้า: ...",                    # การ์ดตอนหน้า (ขึ้นตอนท้าย)
 "cast": {"G": {kid options}},             # ตัวละครเสริม; "N" = น้องสงสัย (ค่าเริ่มต้น)
 "lines": [ {                               # 1 บรรทัด = 1 บรรทัดใน script.tts.txt (เรียงตรงกัน)
   "cap": "ข้อความซับ *คำเน้น*",              # *...* = สีส้ม
   "scene": {"bg": "bedroom_night", "push": 1.08, "shake": false,
             "chars": [{"who": "N", "x": 300, "y": 700, "w": 460, "pose": {...}, "lying": false,
                        "enter": "fade", "blink": true}]},
   "card": {"k": "หัวข้อ", "n": "7.6", "u": "%", "src": "ผู้แต่ง ปี · วารสาร"},
   "clock": {"t": "03:00", "s": "ตีสาม"},
   "outro": true                            # บรรทัดปิด: น้องสงสัยดันแว่นกลางจอ (ใส่ที่บรรทัดแรกของท่าปิด)
 } ]
}
ฉากต่อเนื่อง: ถ้าบรรทัดไม่มี "scene" จะใช้ฉากของบรรทัดก่อนหน้าต่อ (ไม่ตัดภาพ)
"""
import json, os, shutil, sys, html

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EP = os.path.abspath(sys.argv[1])
S = json.load(open(f"{EP}/story.json", encoding="utf-8"))
TM = json.load(open(f"{EP}/audio/timings.json", encoding="utf-8"))
L = S["lines"]; TL = TM["lines"]
assert len(L) == len(TL), f"story.json มี {len(L)} บรรทัด แต่ timings มี {len(TL)}"
OUT = f"{EP}/video"; A = f"{OUT}/assets"
for d in ("lib", "fonts", "audio"): os.makedirs(f"{A}/{d}", exist_ok=True)

# ---------- คัดลอก asset (ทั้งหมดอยู่ในโปรเจกต์ ไม่มีลิงก์ภายนอก) ----------
shutil.copy(f"{ROOT}/character/kid.js", f"{A}/lib/kid.js")
shutil.copy(f"{ROOT}/tools/story/scenes.js", f"{A}/lib/scenes.js")
gsap = f"{ROOT}/tools/story/vendor/gsap.min.js"
shutil.copy(gsap, f"{A}/lib/gsap.min.js")
for f in os.listdir(f"{ROOT}/assets/fonts"):
    if f.endswith((".woff2", ".txt")): shutil.copy(f"{ROOT}/assets/fonts/{f}", f"{A}/fonts/{f}")
shutil.copy(f"{EP}/audio/mix.wav", f"{A}/audio/mix.wav")
import wave
with wave.open(f"{EP}/audio/mix.wav") as w: END = round(w.getnframes() / w.getframerate(), 3)

T = [ln["start"] for ln in TL]; E = [ln["end"] for ln in TL]
CAST = {"N": {}}; CAST.update(S.get("cast", {}))
H, J = [], []  # html, gsap

def esc(s): return html.escape(s, quote=True)

# เส้นเกร็ง + เหงื่อ รอบตัวละคร (พิกัดเดียวกับ kid.js) — ใช้กับ "struggle": true
STRAIN = ('<svg class="st" id="{id}s" viewBox="20 -40 260 400" style="position:absolute;inset:0;width:100%;height:100%">'
          '<g stroke="#2B2B2B" stroke-width="6" stroke-linecap="round" fill="none">'
          '<path d="M36 70 l-14 -10 M30 98 l-18 0 M36 126 l-14 10"/><path d="M264 70 l14 -10 M270 98 l18 0 M264 126 l14 10"/>'
          '<path d="M60 300 l-16 8 M70 322 l-12 14"/><path d="M240 300 l16 8 M230 322 l12 14"/></g>'
          '<path d="M236 92 Q248 114 236 122 Q224 114 236 92Z" fill="#9ED8FF" stroke="#2B2B2B" stroke-width="4"/>'
          '<path d="M70 104 Q80 122 70 129 Q60 122 70 104Z" fill="#9ED8FF" stroke="#2B2B2B" stroke-width="4"/></svg>')

# ---------- ฉาก ----------
scenes = []  # (sid, start_line, scene)
for i, ln in enumerate(L):
    if "scene" in ln or i == 0: scenes.append([i, ln.get("scene", {"bg": "cream"})])
for k, (i, sc) in enumerate(scenes):
    a = 0 if k == 0 else T[i] - .05
    b = (T[scenes[k + 1][0]] - .05) if k + 1 < len(scenes) else END
    sid = f"sc{k + 1}"
    figs = ""
    for j, c in enumerate(sc.get("chars", [])):
        opts = dict(CAST.get(c.get("who", "N"), {})); opts.update(c.get("pose", {}))
        cid = f"{sid}c{j}"
        if c.get("lying"):
            box = 'left:140px;top:735px;width:400px;height:616px;transform:rotate(-90deg)'
        else:
            w = c.get("w", 420); box = f'left:{c.get("x", 330)}px;top:{c.get("y", 700)}px;width:{w}px;height:{round(w * 400 / 260)}px'
        figs += (f'<div class="ch" id="{cid}" style="{box}"><div class="br" id="{cid}b">'
                 f'<div class="k" data-kid="{esc(json.dumps(opts, ensure_ascii=False))}"></div>'
                 + (f'<div class="k bl" id="{cid}x" data-kid="{esc(json.dumps({**opts, "eye": "blink"}, ensure_ascii=False))}"></div>' if c.get("blink", True) and opts.get("eye", "norm") not in ("sleep", "blink", "creepy", "laugh", "cool") else "")
                 + '</div>' + (STRAIN.format(id=cid) if c.get("struggle") else "") + '</div>')
        J.append(f'tl.fromTo("#{cid}b",{{scaleY:1}},{{scaleY:1.02,duration:1.2,yoyo:true,repeat:{max(0, int((b - a) / 1.2))},ease:"sine.inOut",transformOrigin:"50% 100%",immediateRender:false}},{a:.3f});')
        if c.get("struggle"):  # ดิ้นเป็นจังหวะ: สั่น 0.6 วิ พัก 0.35 วิ + เส้นเกร็งกะพริบ
            t = max(a, T[i]) + .1
            while t < b - .4:
                J.append(f'tl.fromTo("#{cid}b",{{x:-5,rotation:-1.2}},{{x:5,rotation:1.2,duration:.05,yoyo:true,repeat:11,ease:"none",immediateRender:false}},{t:.3f});'
                         f'tl.set("#{cid}s",{{opacity:1}},{t:.3f});tl.set("#{cid}s",{{opacity:.25}},{t + .6:.3f});')
                t += .95
        if c.get("enter") == "fade":
            J.append(f'tl.fromTo("#{cid}",{{opacity:0}},{{opacity:1,duration:.7,ease:"power1.in",immediateRender:false}},{max(a, T[i]):.3f});')
        t = a + .9
        while t < b - .3:
            J.append(f'blink("#{cid}x",{t:.3f});'); t += 2.9
    blanket = '<div class="blanket"></div>' if any(c.get("lying") for c in sc.get("chars", [])) else ""
    H.append(f'<div class="L" id="{sid}"><div class="cam"><div class="bgw" data-bg="{sc.get("bg", "cream")}"></div>{figs}{blanket}</div></div>')
    J.append(f'show("#{sid}",{a:.3f},{b:.3f});tl.fromTo("#{sid} .cam",{{scale:1}},{{scale:{sc.get("push", 1.06)},duration:{b - a:.3f},ease:"none",immediateRender:false}},{a:.3f});')
    if sc.get("shake"):
        J.append(f'tl.fromTo("#{sid} .cam",{{x:-12}},{{x:12,duration:.05,yoyo:true,repeat:9,ease:"none",immediateRender:false}},{T[i]:.3f});')

# ---------- ท่าปิด: น้องสงสัยดันแว่น (ภาพทีละ 1/15 วิ) ----------
oi = next((i for i, ln in enumerate(L) if ln.get("outro")), None)
if oi is not None:
    t0 = T[oi]
    H.append(f'<div class="L" id="outro"><div class="bgw" data-bg="{L[oi].get("outro_bg", "cream")}"></div>'
             f'<div class="ch" id="op" style="left:250px;top:560px;width:580px;height:{round(580 * 400 / 260)}px"></div></div>')
    J.append(f'show("#outro",{t0 - .05:.3f},{END:.3f});')
    J.append(f'buildPush("#op",{t0:.3f},{END - t0:.3f});')

# ---------- การ์ดตัวเลข / นาฬิกา / ซับ ----------
for i, ln in enumerate(L):
    nxt = T[i + 1] - .05 if i + 1 < len(L) else END
    cd = ln.get("card")
    if cd:
        cid = f"cd{i + 1}"; ca = T[i] + .25; cb = min(max(E[i] + .9, ca + 2.2), END)  # ค้าง ≥ ~2 วิ
        H.append(f'<div class="card" id="{cid}"><div class="ck">{esc(cd["k"])}</div><div class="cn">{esc(cd["n"])}<small>{esc(cd.get("u", ""))}</small></div>'
                 f'<div class="cs">{esc(cd["src"])}</div></div>')
        J.append(f'card("#{cid}",{ca:.3f},{cb:.3f});')
    ck = ln.get("clock")
    if ck:
        kid_ = f"ck{i + 1}"
        H.append(f'<div class="chip" id="{kid_}"><b>{esc(ck["t"])}</b><span>{esc(ck.get("s", ""))}</span></div>')
        J.append(f'chip("#{kid_}",{T[i]:.3f},{min(max(E[i] + .5, T[i] + 2.2), END):.3f});')
    cap = esc(ln["cap"])
    parts = cap.split("*")
    capH = "".join(f'<span class="y">{p}</span>' if k % 2 else p for k, p in enumerate(parts))
    H.append(f'<div class="cap" id="cp{i + 1}"><div>{capH}</div></div>')
    J.append(f'show("#cp{i + 1}",{T[i] - .05:.3f},{min(nxt, E[i] + .5):.3f});')

if S.get("next"):
    H.append(f'<div class="card next" id="nextc"><div class="ck">ตอนหน้า</div><div class="nx">{esc(S["next"])}</div></div>')
    J.append(f'card("#nextc",{E[-1] + .2:.3f},{END:.3f});')

CSS = """
@font-face{font-family:"NST";font-weight:700;src:url("assets/fonts/noto-sans-thai-thai-700-normal.woff2") format("woff2")}
@font-face{font-family:"NST";font-weight:900;src:url("assets/fonts/noto-sans-thai-thai-900-normal.woff2") format("woff2")}
@font-face{font-family:"NS";font-weight:700;src:url("assets/fonts/noto-sans-latin-700-normal.woff2") format("woff2")}
@font-face{font-family:"NS";font-weight:900;src:url("assets/fonts/noto-sans-latin-900-normal.woff2") format("woff2")}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:#1B1E2E}
#root{position:absolute;inset:0;overflow:hidden;font-family:"NST","NS",sans-serif;color:#2B2B2B}
.L{position:absolute;inset:0;visibility:hidden;overflow:hidden}.cam{position:absolute;inset:0;transform-origin:50% 55%}
.bgw{position:absolute;inset:0}.ch{position:absolute}.br{position:absolute;inset:0}.k{position:absolute;inset:0}.k svg{width:100%;height:100%}
.bl{visibility:hidden}.blanket{position:absolute;inset:0}
.card{position:absolute;left:90px;top:230px;width:900px;padding:28px 40px 24px;border-radius:28px;background:#FFF8EC;border:6px solid #2B2B2B;box-shadow:10px 10px 0 #2B2B2B;opacity:0;z-index:15}
.card .ck{font-weight:700;font-size:38px}.card .cn{font-weight:900;font-size:130px;line-height:1.05;font-family:"NS","NST"}
.card .cn small{font-size:54px;margin-left:12px}.card .cs{font-weight:700;font-size:26px;color:#7a6f60;margin-top:6px;font-family:"NS","NST"}
.card.next{top:300px}.card .nx{font-weight:900;font-size:60px;line-height:1.35;margin-top:6px}
.chip{position:absolute;left:70px;top:230px;padding:12px 26px;border-radius:18px;background:#FFF8EC;border:5px solid #2B2B2B;box-shadow:6px 6px 0 #2B2B2B;display:flex;gap:14px;align-items:center;opacity:0;z-index:16}
.chip b{font-weight:900;font-size:50px;font-family:"NS","NST"}.chip span{font-weight:700;font-size:32px}
.cap{position:absolute;left:60px;right:140px;top:1440px;text-align:center;visibility:hidden;z-index:20}
.cap div{display:inline-block;background:#fff;border:6px solid #2B2B2B;border-radius:24px;padding:18px 30px 12px;font-weight:900;font-size:72px;line-height:1.42;box-shadow:8px 8px 0 #2B2B2B}
.cap .y{color:#E0704F}
"""

page = f"""<!doctype html><html lang="th"><head><meta charset="UTF-8"><meta name="viewport" content="width=1080, height=1920">
<!-- สร้างโดย tools/story/build.py จาก story.json — แก้ที่ story.json แทน -->
<script src="assets/lib/gsap.min.js"></script><script src="assets/lib/kid.js"></script><script src="assets/lib/scenes.js"></script>
<style>{CSS}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{END}" data-width="1080" data-height="1920">
<audio id="vo" src="assets/audio/mix.wav" data-start="0" data-duration="{END}" data-volume="1"></audio>
{chr(10).join(H)}
</div>
<script>
document.querySelectorAll("[data-kid]").forEach(e=>e.innerHTML=kid(JSON.parse(e.dataset.kid)));
document.querySelectorAll("[data-bg]").forEach(e=>e.innerHTML=(BG[e.dataset.bg]||BG.cream)());
document.querySelectorAll(".blanket").forEach(e=>e.innerHTML=BLANKET);
window.__timelines=window.__timelines||{{}};
const tl=gsap.timeline({{paused:true}});window.__timelines["main"]=tl;
const show=(e,a,b)=>{{tl.set(e,{{visibility:"visible"}},a);if(b!==undefined)tl.set(e,{{visibility:"hidden"}},b);}};
const blink=(e,a)=>{{tl.set(e,{{visibility:"visible"}},a);tl.set(e,{{visibility:"hidden"}},a+.12);}};
const card=(e,a,b)=>{{tl.fromTo(e,{{opacity:0,scale:1.12}},{{opacity:1,scale:1,duration:.35,ease:"back.out(1.7)",immediateRender:false}},a);tl.to(e,{{opacity:0,duration:.2}},b-.2);}};
const chip=(e,a,b)=>{{tl.fromTo(e,{{opacity:0,y:-30}},{{opacity:1,y:0,duration:.3,ease:"back.out(1.6)",immediateRender:false}},a);tl.to(e,{{opacity:0,duration:.2}},b-.2);}};
function buildPush(sel,t0,dur){{
  const box=document.querySelector(sel); const n=Math.ceil(Math.min(dur,4.0)*15);
  for(let f=0;f<=n;f++){{const d=document.createElement("div");d.className="k";d.style.visibility="hidden";
    d.innerHTML=kid(pushGlassesPose(Math.min(f/15,3.3)));box.appendChild(d);
    tl.set(d,{{visibility:"visible"}},t0+f/15); if(f<n) tl.set(d,{{visibility:"hidden"}},t0+(f+1)/15);}}
}}
{chr(10).join(J)}
tl.set({{}},{{}},{END});
</script></body></html>"""
open(f"{OUT}/index.html", "w", encoding="utf-8").write(page)
print(f"build ok: {len(scenes)} ฉาก, {len(L)} บรรทัด, {END:.2f}s -> {OUT}/index.html")
