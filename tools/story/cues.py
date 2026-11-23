#!/usr/bin/env python3
"""วางเสียงประกอบอัตโนมัติจาก story.json + timings.json -> audio/sfx_cues.json (ใช้กับ tools/audio/mix.py)

ใช้: python3 tools/story/cues.py episodes/<EP>
กติกา (ปรับเพิ่มต่อบรรทัดได้ด้วย "sfx": [["thud", 0.2], "pop"] ใน story.json — ตัวเลข = วินาทีหลังเริ่มบรรทัด):
- เปลี่ยนฉาก -> whoosh (เบา) · นาฬิกา -> tick · การ์ด -> pop · ฉากสั่น -> thud
- ตุ้งแช่ (jumpscare) -> sting + thud ดังกว่าปกติ
- ตัวละครดิ้น (struggle) -> heartbeat ทุก 0.95 วิ
- ฉาก bg=elevator_hatch_up_knock -> knock (ก๊อก×3 บนฝาเหล็ก, ดังกว่า ambient เป็นจุดสำคัญ) ตอน +0.1 วิ ที่ -1 dB (ใกล้ระดับเสียงพูด; คาดว่าอยู่ในบรรทัด "silent" ไม่ทับคำพูด) — ข้ามถ้าบรรทัดนั้นระบุ knock/knock_one เองใน "sfx"
- ไฟกะพริบ (flicker ในฉาก/บรรทัด) -> flicker_buzz ทุกครั้งที่ไฟดับ (จังหวะเดียวกับภาพ จาก tools/story/flicker.py)
- ตัวละครค่อยๆ โผล่ (enter: fade) -> riser · ท่าปิด -> glint ตอนเลนส์แวบ (+1.3 วิ) · การ์ดตอนหน้า -> ding
"""
import json, sys
import flicker as FL

EP = sys.argv[1]
S = json.load(open(f"{EP}/story.json", encoding="utf-8"))
TL = json.load(open(f"{EP}/audio/timings.json", encoding="utf-8"))["lines"]
cues = []
add = lambda s, at, g=-22: cues.append({"sfx": s, "at": round(max(0, at), 3), "gain_db": g})
for i, ln in enumerate(S["lines"]):
    t = TL[i]["start"]; sc = ln.get("scene")
    if sc and i > 0: add("whoosh", t - .15, -26)
    if sc and sc.get("shake"): add("thud", t + .05, -18)
    if sc and any(c.get("enter") == "fade" for c in sc.get("chars", [])): add("riser", t - .2, -24)
    manual = {x if isinstance(x, str) else x[0] for x in ln.get("sfx", [])}
    if sc and sc.get("bg") == "elevator_hatch_up_knock" and not manual & {"knock", "knock_one"}: add("knock", t + .1, -1)
    if ln.get("clock"): add("tick", t, -20)
    if sc and any(c.get("struggle") for c in sc.get("chars", [])):
        end = TL[i]["end"]; k = t + .1
        while k < end: add("heartbeat", k, -16); k += .95
    if ln.get("jumpscare"): add("sting", t - .03, -12); add("thud", t, -14)
    if ln.get("card"): add("pop", t + .25, -20)
    if ln.get("outro"): add("glint", t + 1.3, -18)
    for x in ln.get("sfx", []):
        name, off = (x, 0) if isinstance(x, str) else x
        add(name, t + off, -20)
# ไฟกะพริบ: ใช้ตารางจังหวะเดียวกับ build.py (ช่วงเดียวกัน: ถึงบรรทัด flicker ถัดไป/ฉากถัดไป)
L = S["lines"]; starts = [i for i, ln in enumerate(L) if "scene" in ln or i == 0]
for k, i in enumerate(starts):
    j1 = starts[k + 1] if k + 1 < len(starts) else len(L)
    b = TL[j1]["start"] - .05 if j1 < len(L) else TL[-1]["end"] + 4
    sc = L[i].get("scene", {})
    fl = [(j, sc.get("flicker") if j == i and sc.get("flicker") else L[j].get("flicker")) for j in range(i, j1)]
    fl = [x for x in fl if x[1]]
    for n, (j, v) in enumerate(fl):
        end = TL[fl[n + 1][0]]["start"] - .05 if n + 1 < len(fl) else b
        for a, _, lv in FL.events(TL[j]["start"], end, FL.opts(v, j)): add("flicker_buzz", a, -24 if lv > .5 else -30)
if S.get("next"): add("ding", TL[-1]["end"] + .2, -20)
json.dump(cues, open(f"{EP}/audio/sfx_cues.json", "w"), indent=1)
print(f"cues ok: {len(cues)} จุด")
