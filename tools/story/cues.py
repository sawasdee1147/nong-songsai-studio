#!/usr/bin/env python3
"""วางเสียงประกอบอัตโนมัติจาก story.json + timings.json -> audio/sfx_cues.json (ใช้กับ tools/audio/mix.py)

ใช้: python3 tools/story/cues.py episodes/<EP>
กติกา (ปรับเพิ่มต่อบรรทัดได้ด้วย "sfx": [["thud", 0.2], "pop"] ใน story.json — ตัวเลข = วินาทีหลังเริ่มบรรทัด):
- เปลี่ยนฉาก -> whoosh (เบา) · นาฬิกา -> tick · การ์ด -> pop · ฉากสั่น -> thud
- ตัวละครดิ้น (struggle) -> heartbeat ทุก 0.95 วิ
- ตัวละครค่อยๆ โผล่ (enter: fade) -> riser · ท่าปิด -> glint ตอนเลนส์แวบ (+1.3 วิ) · การ์ดตอนหน้า -> ding
"""
import json, sys

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
    if ln.get("clock"): add("tick", t, -20)
    if sc and any(c.get("struggle") for c in sc.get("chars", [])):
        end = TL[i]["end"]; k = t + .1
        while k < end: add("heartbeat", k, -16); k += .95
    if ln.get("card"): add("pop", t + .25, -20)
    if ln.get("outro"): add("glint", t + 1.3, -18)
    for x in ln.get("sfx", []):
        name, off = (x, 0) if isinstance(x, str) else x
        add(name, t + off, -20)
if S.get("next"): add("ding", TL[-1]["end"] + .2, -20)
json.dump(cues, open(f"{EP}/audio/sfx_cues.json", "w"), indent=1)
print(f"cues ok: {len(cues)} จุด")
