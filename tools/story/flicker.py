"""ไฟกะพริบแบบหลอดไฟจะเสีย — ตารางจังหวะใช้ร่วมกันระหว่าง build.py (ภาพ) และ cues.py (เสียงไฟช็อต)

จังหวะสุ่มแต่ deterministic (random.Random(seed)) -> เรนเดอร์ซ้ำได้ผลเท่าเดิมทุกครั้ง, ภาพกับเสียงตรงกันเสมอ
ความปลอดภัยผู้ไวแสง: เป็นการ "หรี่มืด" ทับฉาก (ไม่ใช่แฟลชขาว) และจุดเริ่มดับแต่ละครั้งห่างกัน ≥ 0.36 วิ
  -> ไม่เกิน 3 ครั้งในหน้าต่าง 1 วินาทีใดๆ (เกณฑ์ WCAG 2.3.1)
"""
import random

MIN_GAP = 0.36   # วินาที ระหว่างจุดเริ่มดับ 2 ครั้ง (≤ 3 ครั้ง/วินาที)
MAX_RATE = 2.5   # ครั้ง/วินาที (เฉลี่ย) สูงสุดที่ยอมให้ตั้ง


def opts(v, i):
    """ค่าใน story.json -> dict ค่าตั้ง; v = true | ตัวเลข (วินาที) | {"dur","rate","depth","seed","delay"}"""
    o = {"dur": None, "rate": 1.6, "depth": 0.72, "seed": 101 + i, "delay": 0.1}
    if isinstance(v, (int, float)) and not isinstance(v, bool): o["dur"] = float(v)
    elif isinstance(v, dict): o.update({k: v[k] for k in v if k in o})
    o["rate"] = max(0.3, min(float(o["rate"]), MAX_RATE)); o["depth"] = max(0.2, min(float(o["depth"]), 0.85))
    return o


def events(t0, t1, o):
    """-> [(ดับ, ติด, ระดับมืด 0..depth)] ระหว่าง t0..t1 (สั้นลงได้ด้วย o["dur"])
    ชนิดการดับ: วูบสั้น (หลอดกระตุก) / วูบครึ่งเดียว (ไฟตก) / ดับนาน (เกือบเสีย)"""
    if o["dur"]: t1 = min(t1, t0 + o["dur"])
    r = random.Random(o["seed"]); d = o["depth"]; ev = []
    t = t0 + o["delay"]
    while True:
        k = r.random()
        if k < .22:   off, lv = r.uniform(.38, .62), d          # ดับนาน
        elif k < .45: off, lv = r.uniform(.07, .12), d * .55    # วูบครึ่งเดียว
        else:         off, lv = r.uniform(.09, .2), d           # วูบสั้น
        if t + off > t1 - .08: break
        ev.append((round(t, 3), round(t + off, 3), round(lv, 3)))
        t += max(MIN_GAP, off + .16, r.uniform(.5, 1.5) / o["rate"])
    return ev
