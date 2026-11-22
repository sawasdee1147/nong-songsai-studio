# Self-made bed + sound effects (numpy synthesis, no copyrighted audio) -> site/a/*.wav
# usage: python3 sfx.py PROJECT_DIR   (mood from story.json: "dark" = drone+crickets, "warm" = soft pad)
import json, os, sys, wave
import numpy as np

P = os.path.abspath(sys.argv[1]); A = f"{P}/site/a"; os.makedirs(A, exist_ok=True)
MOOD = json.load(open(f"{P}/story.json")).get("mood", "dark")
SR = 48000; rng = np.random.default_rng(7)


def save(name, x):
    x = x / (np.abs(x).max() + 1e-9) * .89
    with wave.open(f"{A}/{name}", "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x * 32767).astype(np.int16).tobytes())


def lp(x, k):  # cheap one-pole lowpass, k in (0,1)
    y = np.empty_like(x); s = 0.
    for i, v in enumerate(x): s += k * (v - s); y[i] = s
    return y


def env(n, a, r):
    e = np.ones(n); ai, ri = max(1, int(a * SR)), max(1, int(r * SR))
    e[:ai] = np.linspace(0, 1, ai); e[-ri:] *= np.linspace(1, 0, ri); return e


T = int(json.load(open(f"{P}/work/timing.json"))["total"]) + 4; t = np.arange(T * SR) / SR
if MOOD == "warm":
    bed = sum(np.sin(2 * np.pi * f * t) * g for f, g in [(130.8, 1), (164.8, .7), (196, .6), (261.6, .3)])
    bed *= .6 + .4 * np.sin(2 * np.pi * t / 9) ** 2
else:
    bed = sum(np.sin(2 * np.pi * f * t + p) * g for f, p, g in [(36.7, 0, 1), (36.9, 1, .8), (55.0, .5, .45), (73.6, 2, .25)])
    bed *= .55 + .45 * np.sin(2 * np.pi * t / 17) ** 2
    bed += lp(rng.standard_normal(len(t)), .004) * 3
    for c in range(T * 4):
        s = int((c / 4 + rng.random() * .2) * SR); n = int(.06 * SR)
        if s + n < len(t) and rng.random() > .3:
            bed[s:s + n] += np.sin(2 * np.pi * 4400 * np.arange(n) / SR) * np.hanning(n) * .04
save("bed.wav", bed * env(len(t), 1.5, 2))

n = int(.35 * SR); u = np.arange(n) / SR
save("thump.wav", np.sin(2 * np.pi * 70 * u * (1 - u)) * np.exp(-u * 18) + lp(rng.standard_normal(n), .3) * np.exp(-u * 60) * .6)
n = int(.8 * SR); u = np.arange(n) / SR; v = np.clip(u - .22, 0, None)
save("heart.wav", np.sin(2 * np.pi * 50 * u) * np.exp(-u * 25) + np.sin(2 * np.pi * 45 * v) * np.exp(-v * 28) * (u > .22) * .7)
n = int(1.1 * SR); u = np.arange(n) / SR
save("creak.wav", lp(np.sin(2 * np.pi * (180 + 60 * np.sin(2 * np.pi * 3 * u)) * u) * (rng.random(n) * .5 + .5) * env(n, .1, .4), .2))
n = int(2.5 * SR); u = np.arange(n) / SR
save("sting.wav", sum(np.sin(2 * np.pi * f * u) for f in [220, 233.1, 311.1, 466.2]) * (u / 2.5) ** 2 * env(n, .01, .08))
n = int(.45 * SR); u = np.arange(n) / SR  # whoosh: noise with rising-then-falling lowpass
save("whoosh.wav", lp(rng.standard_normal(n), .08) * np.sin(np.pi * u / .45) ** 2)
n = int(.12 * SR); u = np.arange(n) / SR
save("pop.wav", np.sin(2 * np.pi * (900 - 3000 * u) * u) * np.exp(-u * 45))
n = int(.06 * SR); u = np.arange(n) / SR
save("tick.wav", np.sin(2 * np.pi * 2400 * u) * np.exp(-u * 120))
n = int(1.6 * SR); u = np.arange(n) / SR  # boom: low hit for the twist
save("boom.wav", np.sin(2 * np.pi * 48 * u) * np.exp(-u * 3) + lp(rng.standard_normal(n), .05) * np.exp(-u * 8) * 2)
print("sfx ok:", MOOD)
