#!/usr/bin/env python3
"""ประกอบเสียงพากย์: ตัดความเงียบหัวท้ายแต่ละประโยค -> เว้นช่วง 0.2–0.4 วิ -> ต่อเป็นไฟล์เดียว -> timings.json

ใช้:
  python3 tools/audio/assemble.py <raw_dir> <out_dir> [--script script.tts.txt]
          [--gap-min 0.2] [--gap-max 0.4] [--seed 7] [--max-line 3.0] [--threshold -45]
          [--story story.json] [--target-lufs -15] [--max-adjust 5] [--no-loudnorm]

อินพุต: raw_dir/line_01.(mp3|wav), line_02..., เรียงตามเลข
ผลลัพธ์: out_dir/voice.wav, out_dir/timings.json, out_dir/trimmed/line_XX.wav

ต่อบรรทัด (หลังตัดเงียบ ก่อนต่อไฟล์):
- ฟิลเตอร์ radio: ถ้า story.json (ค่าเริ่มต้น = story.json ข้างไฟล์ --script หรือระบุ --story) บรรทัดที่ i มี "radio": true
  -> ลำโพงอินเตอร์คอม (bandpass 300-3400 Hz + ผิดเพี้ยนเล็กน้อย + เสียงซ่าเบาๆ หัว/ท้าย)
- ปรับความดังรายบรรทัดอัตโนมัติ: วัด LUFS (ffmpeg ebur128) แล้วปรับ gain เข้าหา --target-lufs (จำกัด ±--max-adjust dB,
  กันพีคเกิน -1 dBFS) ทำหลัง radio เพื่อให้บรรทัดวิทยุดังใกล้เคียงบรรทัดอื่น; ปิดด้วย --no-loudnorm
exit code 2 ถ้ามีประโยคยาวเกิน --max-line (ไฟล์ยังถูกสร้าง แต่ต้องส่งกลับนักเขียนบท)
"""
import argparse, glob, json, os, random, re, subprocess, sys, wave

SR = 44100


def trim_to_wav(src, dst, thr_db, rel_db=28.0, pad=0.03, tempo=1.0):
    """แปลงเป็น WAV mono แล้วตัดเงียบหัวท้ายด้วย RMS ทีละ 10ms
    ถือว่า "มีเสียงพูด" เมื่อ RMS สูงกว่าทั้ง thr_db (ค่าสัมบูรณ์) และ (RMS สูงสุดของประโยค − rel_db)
    จึงตัดหางเสียงเบา/เสียงหายใจที่ดังกว่า −45 dB แต่เบากว่าเสียงพูดมากได้
    """
    import numpy as np
    tmp = dst + ".full.wav"
    af = ["-af", f"atempo={tempo}"] if abs(tempo - 1.0) > 1e-6 else []
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, *af,
                    "-ac", "1", "-ar", str(SR), "-c:a", "pcm_s16le", tmp], check=True)
    with wave.open(tmp, "rb") as w:
        x = np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(np.float64) / 32768
    os.remove(tmp)
    hop = int(SR * 0.01)
    n = len(x) // hop
    if n == 0:
        y = x[:0]
    else:
        rms = np.sqrt(np.mean(x[: n * hop].reshape(n, hop) ** 2, axis=1) + 1e-12)
        db = 20 * np.log10(rms)
        thr = max(thr_db, db.max() - rel_db)
        active = db > thr
        # รวมช่วงเสียงที่ห่างกัน < 150ms แล้วทิ้งช่วงสั้น < 80ms (เสียงคลิก/หายใจที่หัวท้าย)
        runs, i = [], 0
        while i < n:
            if active[i]:
                j = i
                while j < n and active[j]:
                    j += 1
                if runs and i - runs[-1][1] < 15:
                    runs[-1][1] = j
                    runs[-1][2] += j - i
                else:
                    runs.append([i, j, j - i])
                i = j
            else:
                i += 1
        # นับเฉพาะเฟรมที่มีเสียงจริง (ไม่นับช่องว่างที่ถูกรวม)
        runs = [r for r in runs if r[2] >= 8] or runs
        if not runs:
            y = x[:0]
        else:
            a = max(0, runs[0][0] * hop - int(pad * SR))
            b = min(len(x), runs[-1][1] * hop + int(pad * SR))
            y = x[a:b]
            fade = min(int(0.01 * SR), len(y) // 2)
            if fade:
                ramp = np.linspace(0, 1, fade)
                y = y.copy(); y[:fade] *= ramp; y[-fade:] *= ramp[::-1]
    with wave.open(dst, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(y, -1, 1) * 32767).astype("<i2").tobytes())


def measure_lufs(path):
    """integrated LUFS ของไฟล์ (None ถ้าวัดไม่ได้/เงียบเกินไป)"""
    r = subprocess.run(["ffmpeg", "-nostdin", "-nostats", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.search(r"Integrated loudness:\s*I:\s*(-?[\d.]+) LUFS", r.stderr)
    if not m:
        return None
    v = float(m.group(1))
    return v if v > -69 else None


def radio_filter(path, seed=11):
    """ลำโพงอินเตอร์คอม: bandpass 300-3400 + soft clip + hiss หัว/ท้าย (เขียนทับ path)"""
    import numpy as np
    tmp = path + ".radio.wav"
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-loglevel", "error", "-i", path, "-af",
                    "highpass=f=300:poles=2,lowpass=f=3400:poles=2,volume=6dB,asoftclip=type=tanh,"
                    "highpass=f=300,lowpass=f=3400,equalizer=f=1500:t=q:w=1:g=3",
                    "-ac", "1", "-ar", str(SR), "-c:a", "pcm_s16le", tmp], check=True)
    with wave.open(tmp, "rb") as w:
        x = np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(np.float64) / 32768
    os.remove(tmp)
    r = np.random.default_rng(seed)
    def hiss(sec, lvl):
        n = int(sec * SR)
        h = r.standard_normal(n)
        h = np.convolve(h, np.ones(3) / 3, mode="same")  # ตัดเสียงแหลมสุด
        return h * lvl
    peak = float(np.max(np.abs(x))) or 1.0
    lvl = 0.05 * peak                      # ~ -26 dB ใต้พีค
    pre, post = hiss(0.09, lvl), hiss(0.14, lvl)
    pre *= np.linspace(0.3, 1, len(pre)); post *= np.linspace(1, 0, len(post)) ** 1.5
    bed = r.standard_normal(len(x)) * lvl * 0.35    # ซ่าเบาๆ ใต้เสียงพูด (ยาวเท่า x พอดี)
    y = np.concatenate([pre, x + bed, post])
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(y, -1, 1) * 32767).astype("<i2").tobytes())


def loudnorm_file(path, target, max_adj):
    """ปรับ gain ทั้งไฟล์เข้าหา target LUFS (±max_adj dB, พีคไม่เกิน -1 dBFS); คืน gain ที่ใช้ (dB) หรือ None"""
    import numpy as np
    lufs = measure_lufs(path)
    if lufs is None:
        return None
    with wave.open(path, "rb") as w:
        x = np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(np.float64) / 32768
    g = max(-max_adj, min(max_adj, target - lufs))
    pk = float(np.max(np.abs(x))) or 1e-9
    g = min(g, -1.0 - 20 * np.log10(pk))
    y = np.clip(x * 10 ** (g / 20), -1, 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((y * 32767).astype("<i2").tobytes())
    return round(float(g), 2)


def read_frames(path):
    with wave.open(path, "rb") as w:
        assert w.getframerate() == SR and w.getnchannels() == 1 and w.getsampwidth() == 2
        return w.readframes(w.getnframes())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("raw_dir")
    ap.add_argument("out_dir")
    ap.add_argument("--script")
    ap.add_argument("--gap-min", type=float, default=0.2)
    ap.add_argument("--gap-max", type=float, default=0.4)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--max-line", type=float, default=3.0)
    ap.add_argument("--threshold", type=float, default=-45.0, help="dB ระดับที่ถือว่าเงียบ (ค่าสัมบูรณ์)")
    ap.add_argument("--tempo", type=float, default=1.0,
                    help="เร่ง/ลดความเร็วเสียงพูด (คงระดับเสียง) เช่น 1.12 — ค่าประจำช่องอยู่ใน tools/audio/voice.json: tempo")
    ap.add_argument("--story", help="story.json (อ่าน radio/speaker ต่อบรรทัด) ค่าเริ่มต้น: story.json ข้างไฟล์ --script")
    ap.add_argument("--target-lufs", type=float, default=-15.0)
    ap.add_argument("--max-adjust", type=float, default=5.0)
    ap.add_argument("--no-loudnorm", action="store_true")
    ap.add_argument("--rel", type=float, default=28.0, help="dB ต่ำกว่าช่วงที่ดังที่สุดของประโยค ที่ถือว่าเงียบ")
    a = ap.parse_args()
    assert 0 <= a.gap_min <= a.gap_max

    files = sorted(glob.glob(os.path.join(a.raw_dir, "line_*.*")),
                   key=lambda p: int(re.search(r"line_(\d+)", p).group(1)))
    if not files:
        sys.exit(f"ไม่พบไฟล์ line_XX ใน {a.raw_dir}")
    texts = []
    if a.script:
        # ตัดแท็กอารมณ์ [xxx] ออกจากข้อความใน timings (ซับใช้ข้อความล้วน)
        texts = [re.sub(r"\[[^\]]*\]\s*", "", l).strip() for l in open(a.script, encoding="utf-8") if l.strip()]
        if len(texts) != len(files):
            print(f"WARNING: บทมี {len(texts)} บรรทัด แต่มีไฟล์เสียง {len(files)} ไฟล์", file=sys.stderr)

    story_lines = []
    sp = a.story or (os.path.join(os.path.dirname(os.path.abspath(a.script)), "story.json") if a.script else None)
    if sp and os.path.exists(sp):
        story_lines = json.load(open(sp, encoding="utf-8")).get("lines", [])
        if len(story_lines) != len(files):
            print(f"WARNING: story.json มี {len(story_lines)} บรรทัด แต่มีไฟล์เสียง {len(files)} ไฟล์ — ข้าม radio ถ้าเลขไม่ตรง",
                  file=sys.stderr)
    os.makedirs(os.path.join(a.out_dir, "trimmed"), exist_ok=True)
    rnd = random.Random(a.seed)
    out = bytearray()
    lines, too_long = [], []
    t = 0.0
    for k, src in enumerate(files):
        idx = int(re.search(r"line_(\d+)", src).group(1))
        dst = os.path.join(a.out_dir, "trimmed", f"line_{idx:02d}.wav")
        trim_to_wav(src, dst, a.threshold, a.rel, tempo=a.tempo)
        sl = story_lines[idx - 1] if idx - 1 < len(story_lines) else {}
        is_radio = bool(sl.get("radio"))
        if is_radio:
            radio_filter(dst)
        gain = None if a.no_loudnorm else loudnorm_file(dst, a.target_lufs, a.max_adjust)
        fr = read_frames(dst)
        n = len(fr) // 2
        if n == 0:
            sys.exit(f"ERROR: line_{idx:02d} เงียบทั้งไฟล์หลังตัด (threshold {a.threshold} dB)")
        if k > 0:
            gap = round(rnd.uniform(a.gap_min, a.gap_max), 3)
            gn = int(round(gap * SR))
            out += b"\x00\x00" * gn
            t += gn / SR
        start = t
        out += fr
        t += n / SR
        dur = n / SR
        entry = {"index": idx, "text": texts[idx - 1] if idx - 1 < len(texts) else "",
                 "start": round(start, 3), "end": round(t, 3), "duration": round(dur, 3)}
        if sl.get("speaker"):
            entry["speaker"] = sl["speaker"]
        if is_radio:
            entry["radio"] = True
        if gain is not None:
            entry["gain_db"] = gain
        if k > 0:
            entry["gap_before"] = gap
        lines.append(entry)
        if dur > a.max_line:
            too_long.append(entry)

    with wave.open(os.path.join(a.out_dir, "voice.wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(bytes(out))
    result = {"sample_rate": SR, "tempo": a.tempo, "total": round(t, 3), "gap_range": [a.gap_min, a.gap_max],
              "max_line": a.max_line, "lines": lines,
              "too_long": [e["index"] for e in too_long]}
    with open(os.path.join(a.out_dir, "timings.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    for e in lines:
        flag = "  ⚠️ เกิน" if e in too_long else ""
        extra = (f" gain{e['gain_db']:+.1f}" if "gain_db" in e else "") + (" RADIO" if e.get("radio") else "")
        print(f"[{e['index']:02d}] {e['start']:6.2f} → {e['end']:6.2f}  ({e['duration']:.2f}s){extra}{flag}  {e['text']}")
    print(f"ความยาวรวม: {t:.2f} วินาที · {len(lines)} ประโยค")
    if too_long:
        print(f"ประโยคที่เกิน {a.max_line}s: {', '.join(str(e['index']) for e in too_long)} → ส่งกลับนักเขียนบท",
              file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
