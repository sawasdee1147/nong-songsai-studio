#!/usr/bin/env python3
"""มิกซ์เสียงพากย์ + เสียงประกอบ (จาก sfx/) แล้วปรับความดังรวม

ใช้:
  python3 tools/audio/mix.py <voice.wav> <sfx_cues.json> <out.wav> [--sfx-dir sfx] [--tail 0] [--lufs -14]

sfx_cues.json: [{"sfx": "pop", "at": 1.23, "gain_db": -20}, ...]
  - at = วินาทีในไทม์ไลน์ (0 = ต้น voice.wav)
  - gain_db ค่าเริ่มต้น -20 (เทียบกับ peak ของไฟล์ sfx ที่ -3 dBFS)
--tail: เพิ่มความยาวท้าย (วินาที) เช่น ช่วงท่าปิดที่ไม่มีเสียงพูด
"""
import argparse, json, os, subprocess, sys, tempfile, wave
import numpy as np

SR = 44100


def load(path):
    with wave.open(path, "rb") as w:
        if w.getframerate() != SR or w.getnchannels() != 1 or w.getsampwidth() != 2:
            raise SystemExit(f"{path}: ต้องเป็น WAV 44.1kHz mono 16-bit")
        return np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(np.float64) / 32768


def save(path, x):
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype("<i2").tobytes())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("voice")
    ap.add_argument("cues")
    ap.add_argument("out")
    ap.add_argument("--sfx-dir", default="sfx")
    ap.add_argument("--tail", type=float, default=0.0)
    ap.add_argument("--lufs", type=float, default=-14.0)
    a = ap.parse_args()

    voice = load(a.voice)
    cues = json.load(open(a.cues, encoding="utf-8"))
    end = len(voice) / SR + a.tail
    for c in cues:
        p = os.path.join(a.sfx_dir, f"{c['sfx']}.wav")
        if not os.path.exists(p):
            raise SystemExit(f"ไม่พบเสียงประกอบ {p} — สร้างด้วย tools/sfx/make_sfx.py เท่านั้น")
        end = max(end, c["at"] + len(load(p)) / SR)
    mixbuf = np.zeros(int(np.ceil(end * SR)) + 1)
    mixbuf[: len(voice)] += voice
    for c in cues:
        s = load(os.path.join(a.sfx_dir, f"{c['sfx']}.wav")) * 10 ** (c.get("gain_db", -20) / 20)
        i = int(round(c["at"] * SR))
        mixbuf[i: i + len(s)] += s[: len(mixbuf) - i]

    with tempfile.TemporaryDirectory() as td:
        raw = os.path.join(td, "raw.wav")
        save(raw, mixbuf * 0.7)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw,
                        "-af", f"loudnorm=I={a.lufs}:TP=-1.5:LRA=11",
                        "-ar", str(SR), "-ac", "1", "-c:a", "pcm_s16le", a.out], check=True)
    print(f"mix -> {a.out}  ({end:.2f}s, {len(cues)} sfx cues)")


if __name__ == "__main__":
    main()
