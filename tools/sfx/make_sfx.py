#!/usr/bin/env python3
"""สร้างเสียงประกอบทั้งหมดจากโค้ด (ไม่มีลิขสิทธิ์ภายนอก) -> WAV 44.1kHz mono 16-bit

ใช้: python3 tools/sfx/make_sfx.py sfx/
ผลลัพธ์ deterministic (seed คงที่) — รันซ้ำได้ไฟล์เดิม
"""
import sys, os, wave
import numpy as np

SR = 44100
rng = np.random.default_rng(1147)


def t(dur):
    return np.arange(int(SR * dur)) / SR


def env(n, attack=0.005, release=None, curve=4.0):
    """attack เชิงเส้น + decay แบบ exponential"""
    x = np.arange(n) / SR
    a = np.clip(x / max(attack, 1e-4), 0, 1)
    dur = n / SR
    d = np.exp(-curve * x / dur) if release is None else np.exp(-x / release)
    return a * d


def sine_sweep(f0, f1, dur, log=True):
    tt = t(dur)
    if log:
        f = f0 * (f1 / f0) ** (tt / dur)
    else:
        f = f0 + (f1 - f0) * tt / dur
    phase = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(phase)


def noise(dur):
    return rng.standard_normal(int(SR * dur))


def lowpass(x, cutoff):
    # one-pole lowpass
    a = np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i, v in enumerate(x):
        acc = (1 - a) * v + a * acc
        y[i] = acc
    return y


def bandpass_sweep(x, f0, f1):
    # lowpass sweep minus slower lowpass -> crude moving band
    n = len(x)
    cut = f0 * (f1 / f0) ** (np.arange(n) / n)
    y = np.empty_like(x)
    lp1 = lp2 = 0.0
    for i, v in enumerate(x):
        a1 = np.exp(-2 * np.pi * cut[i] / SR)
        a2 = np.exp(-2 * np.pi * cut[i] * 0.35 / SR)
        lp1 = (1 - a1) * v + a1 * lp1
        lp2 = (1 - a2) * v + a2 * lp2
        y[i] = lp1 - lp2
    return y


def norm(x, peak_db=-3.0):
    p = np.max(np.abs(x)) or 1.0
    return x / p * (10 ** (peak_db / 20))


# ---------- เสียงแต่ละตัว ----------

def pop():
    x = sine_sweep(900, 220, 0.09) * env(int(SR * 0.09), 0.002, curve=6)
    return norm(x)


def boing():
    d = 0.45
    tt = t(d)
    f = 180 + 120 * np.sin(2 * np.pi * 9 * tt) * np.exp(-5 * tt) + 80 * np.exp(-6 * tt)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(tt), 0.003, curve=4)
    return norm(x)


def glint():
    # ประกายเลนส์แว่น: กระดิ่งเสียงสูงสองชั้น + shimmer
    d = 0.6
    tt = t(d)
    x = np.zeros_like(tt)
    for k, (f, dl) in enumerate([(2637, 0.0), (3520, 0.06), (5274, 0.12)]):
        s = int(dl * SR)
        seg = np.sin(2 * np.pi * f * tt[: len(tt) - s]) * np.exp(-7 * tt[: len(tt) - s])
        seg += 0.3 * np.sin(2 * np.pi * f * 2.01 * tt[: len(tt) - s]) * np.exp(-12 * tt[: len(tt) - s])
        x[s:] += seg * (0.9 - 0.2 * k)
    return norm(x)


def ding():
    # "ถูกต้อง / ปิ๊ง!"
    d = 0.9
    tt = t(d)
    x = sum(a * np.sin(2 * np.pi * f * tt) * np.exp(-r * tt)
            for f, a, r in [(1046.5, 1.0, 4), (2093, 0.4, 6), (3139.5, 0.2, 8), (1568, 0.3, 5)])
    return norm(x * env(len(tt), 0.002, curve=0.0001))


def whoosh():
    d = 0.5
    x = bandpass_sweep(noise(d), 300, 4000)
    w = np.sin(np.pi * np.arange(len(x)) / len(x)) ** 2
    return norm(x * w)


def swoosh_down():
    d = 0.45
    x = bandpass_sweep(noise(d), 4000, 250)
    w = np.sin(np.pi * np.arange(len(x)) / len(x)) ** 1.5
    return norm(x * w)


def bubble():
    # ฟองน้ำ 1 ฟอง: sine ที่ pitch ไต่ขึ้นเร็ว
    d = 0.12
    x = sine_sweep(500, 1400, d) * env(int(SR * d), 0.003, curve=5)
    return norm(x)


def bubbles():
    d = 1.2
    out = np.zeros(int(SR * d))
    for _ in range(9):
        b = bubble() * rng.uniform(0.35, 1.0)
        f = rng.uniform(0.7, 1.5)
        idx = (np.arange(int(len(b) / f)) * f).astype(int)
        b = b[idx[idx < len(b)]]
        s = int(rng.uniform(0, d - 0.15) * SR)
        out[s:s + len(b)] += b
    return norm(out)


def splash():
    d = 0.8
    n = noise(d)
    x = lowpass(n, 2500) * env(len(n), 0.004, curve=6)
    x += 0.4 * bubbles()[: len(x)]
    return norm(x)


def tick():
    d = 0.03
    x = noise(d) * env(int(SR * d), 0.0005, curve=12)
    return norm(lowpass(x, 6000))


def thud():
    d = 0.35
    x = sine_sweep(140, 45, d) * env(int(SR * d), 0.002, curve=7)
    x += 0.3 * lowpass(noise(d), 400) * env(int(SR * d), 0.001, curve=14)
    return norm(x)


def riser():
    d = 1.0
    x = sine_sweep(200, 1200, d) * 0.5 + 0.5 * bandpass_sweep(noise(d), 400, 6000)
    w = (np.arange(int(SR * d)) / (SR * d)) ** 2
    return norm(x * w)


def blip_talk():
    # เสียงพูดแบบการ์ตูนสั้นๆ (ใช้ตอนตัวละคร "อืม?")
    d = 0.18
    tt = t(d)
    f = 520 + 160 * np.sin(2 * np.pi * 7 * tt)
    sq = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR))
    return norm(lowpass(sq, 2500) * env(len(tt), 0.005, curve=3))


def wrong():
    # "ผิด" — สองโน้ตลง
    a = sine_sweep(392, 380, 0.16) * env(int(SR * 0.16), 0.003, curve=3)
    b = sine_sweep(330, 300, 0.3) * env(int(SR * 0.3), 0.003, curve=3)
    sq = lambda x: np.tanh(3 * x)
    return norm(np.concatenate([sq(a), np.zeros(int(SR * 0.03)), sq(b)]))


SFX = {
    "pop": (pop, "ของโผล่/เด้งขึ้นจอ"),
    "boing": (boing, "ตัวละครเด้ง ท่าซนๆ"),
    "glint": (glint, "เลนส์แว่นแวบ (ท่าดันแว่น/แว่นแวบ)"),
    "ding": (ding, "ปิ๊ง! เข้าใจแล้ว / เฉลย"),
    "whoosh": (whoosh, "เปลี่ยนฉาก / ของพุ่งเข้า"),
    "swoosh_down": (swoosh_down, "ของตก / ซูมออก"),
    "bubble": (bubble, "ฟองน้ำ 1 ฟอง"),
    "bubbles": (bubbles, "ฟองน้ำหลายฟอง (ใต้น้ำ)"),
    "splash": (splash, "จุ่มน้ำ / น้ำกระเซ็น"),
    "tick": (tick, "ข้อความ/ไอคอนขึ้นทีละอัน"),
    "thud": (thud, "ตกใจ / ข้อเท็จจริงหนักๆ"),
    "riser": (riser, "สร้างความลุ้นก่อนเฉลย"),
    "blip_talk": (blip_talk, "ตัวละคร 'อืม?' แบบการ์ตูน"),
    "wrong": (wrong, "ผิด! / ความเชื่อผิด"),
}


def write_wav(path, x):
    y = np.clip(x, -1, 1)
    pcm = (y * 32767).astype("<i2")
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "sfx"
    os.makedirs(out, exist_ok=True)
    for name, (fn, desc) in SFX.items():
        x = fn()
        write_wav(os.path.join(out, f"{name}.wav"), x)
        print(f"{name:12s} {len(x)/SR:5.2f}s  {desc}")


if __name__ == "__main__":
    main()
