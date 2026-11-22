# Thai voice-over, one clip per line, trimmed and joined with a short gap
# -> site/a/vo.wav + work/timing.json {"total": s, "lines": {"01": [start, end]}}.
# Engine from story.json "engine": "eleven" (recommended: ElevenLabs, sounds human; the user's OWN key in
# ELEVENLABS_API_KEY or ~/.elevenlabs_key, free plan works; picked automatically when a key exists),
# "gtts" (free Google voice, no key), "edge" (free Microsoft voice, flaky on some Thai text), "say" (macOS, Kanya).
# Own recording: put work/vo/01.wav, 02.wav ... and run with --own.
# usage: python3 voice.py PROJECT_DIR [--own]
import json, os, subprocess, sys

P = os.path.abspath(sys.argv[1]); OWN = "--own" in sys.argv
S = json.load(open(f"{P}/story.json")); V = f"{P}/work/vo"
os.makedirs(V, exist_ok=True); os.makedirs(f"{P}/site/a", exist_ok=True)
KEYFILE = os.path.expanduser("~/.elevenlabs_key")
EL_KEY = os.environ.get("ELEVENLABS_API_KEY") or (open(KEYFILE).read().strip() if os.path.exists(KEYFILE) else "")
ENGINE = S.get("engine", "eleven" if EL_KEY else "gtts"); SPEED = S.get("speed", 1.2 if ENGINE == "gtts" else 1.0)
GAP = 0.18
TRIM = "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse"


def run(*a):
    subprocess.run(a, check=True, capture_output=True)


def dur(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f],
                                capture_output=True, text=True).stdout)


def el(path, body=None):
    import urllib.request
    req = urllib.request.Request("https://api.elevenlabs.io" + path, data=body and json.dumps(body).encode(),
                                 headers={"xi-api-key": EL_KEY, "Content-Type": "application/json"})
    return urllib.request.urlopen(req, timeout=120).read()


def el_voice():
    v = S.get("voice") or os.environ.get("ELEVENLABS_VOICE_ID")
    if v: return v
    try:  # no voice chosen: first voice in the user's library
        return json.loads(el("/v1/voices"))["voices"][0]["voice_id"]
    except Exception:
        sys.exit('Set "voice" in story.json to an ElevenLabs voice ID (ElevenLabs > Voices > copy ID).')


def tts(text, out):
    if ENGINE == "eleven":
        if not EL_KEY: sys.exit("No ElevenLabs key: put it in ~/.elevenlabs_key, or set \"engine\": \"gtts\" in story.json.")
        open(out + ".mp3", "wb").write(el(f"/v1/text-to-speech/{VOICE}?output_format=mp3_44100_128",
                                          {"text": text, "model_id": S.get("model", "eleven_v3"), "seed": 42}))
        return out + ".mp3"
    if ENGINE == "gtts":
        from gtts import gTTS
        gTTS(text, lang="th").save(out + ".mp3"); return out + ".mp3"
    if ENGINE == "edge":
        run(sys.executable, "-m", "edge_tts", "--voice", S.get("voice", "th-TH-PremwadeeNeural"), "--text", text, "--write-media", out + ".mp3")
        return out + ".mp3"
    run("say", "-v", "Kanya", "-o", out + ".aiff", text); return out + ".aiff"


VOICE = el_voice() if ENGINE == "eleven" and not OWN else None
L = S["lines"]
parts, timing, t = [], {}, 0.15
for n, ln in enumerate(L, 1):
    k = f"{n:02d}"; raw = f"{V}/{k}.wav"; out = f"{V}/{k}_t.wav"
    if not OWN:
        try:
            run("ffmpeg", "-y", "-i", tts(ln["vo"], f"{V}/{k}"), "-ar", "48000", "-ac", "1", raw)
        except Exception as e:
            sys.exit(f"voice failed on line {k} ({ENGINE}): {e}\nTry again, set \"engine\" to another one in story.json, or record your own (--own).")
    run("ffmpeg", "-y", "-i", raw, "-af", f"{TRIM},atempo={SPEED}", "-ar", "48000", "-ac", "1", out)
    d = dur(out); timing[k] = [round(t, 3), round(t + d, 3)]; parts.append(out); t += d + GAP + ln.get("pause", 0)
# place every line at its exact start, then level to -16 LUFS
inputs = sum((["-i", p] for p in parts), [])
delays = ";".join(f"[{i}]adelay={int(timing[f'{i + 1:02d}'][0] * 1000)}[d{i}]" for i in range(len(parts)))
mix = "".join(f"[d{i}]" for i in range(len(parts))) + f"amix=inputs={len(parts)}:normalize=0,loudnorm=I=-13:TP=-1.5"
run("ffmpeg", "-y", *inputs, "-filter_complex", f"{delays};{mix}", "-ar", "48000", "-ac", "1", f"{P}/site/a/vo.wav")
total = round(t - GAP + 0.6, 3)
json.dump({"total": total, "lines": timing}, open(f"{P}/work/timing.json", "w"), indent=1)
print(f"voice ok ({'own' if OWN else ENGINE}): {len(parts)} lines, {total:.1f}s")
