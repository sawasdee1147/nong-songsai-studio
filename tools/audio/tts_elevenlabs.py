#!/usr/bin/env python3
"""พากย์บททีละประโยคด้วย ElevenLabs Text-to-Speech API

ใช้:
  python3 tools/audio/tts_elevenlabs.py <script.tts.txt> <out_dir> [--only 3,7]

- อ่านบรรทัดละ 1 ประโยค (ข้ามบรรทัดว่าง) -> out_dir/line_01.mp3, line_02.mp3, ...
- voice_id / model / voice_settings อ่านจาก tools/audio/voice.json
- API key: ห้ามเขียนลงไฟล์ ระบบ proxy ของเซสชันแนบ credential ให้อัตโนมัติ
  (ถ้ารันบนเครื่องตัวเอง ให้ตั้ง env ELEVENLABS_API_KEY)
- หลายเสียง: ถ้ามี story.json ข้างไฟล์ script (หรือ --story) และบรรทัดที่ i มี "speaker": "Y" จะใช้
  voices["Y"] ใน voice.json (voice_id/voice_settings/... ทับค่าหลัก) — บรรทัดไม่มี speaker ใช้เสียงหลัก
  ต้องมีจำนวนบรรทัดใน story.json เท่ากับ script.tts.txt (ไม่เท่า = error) script.tts.txt ไม่ต้องมี marker
  พากย์เฉพาะบรรทัดลุง: ดูเลขบรรทัดจาก story.json แล้ว --only เช่น --only 5,9
  (ฟิลเตอร์ "radio": true ทำตอน assemble.py ไม่ใช่ตอนพากย์)
- บรรทัดเงียบ: story.json บรรทัดที่ i มี "silent": <วินาที> -> ข้าม ไม่เรียก API ไม่สร้างไฟล์ (assemble.py ใส่ความเงียบแทน)
  ใน script.tts.txt ยังต้องมีบรรทัดนั้น เช่น `[silent] ก๊อก ก๊อก ก๊อก…` เพื่อให้เลขบรรทัดตรง; ไม่ส่งเป็น previous/next_text
- ส่ง previous_text / next_text ให้ API เพื่อให้น้ำเสียงต่อเนื่องระหว่างประโยค
"""
import argparse, json, os, ssl, sys, time, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
API = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?output_format={fmt}"


def ssl_ctx():
    ctx = ssl.create_default_context()
    for ca in (os.environ.get("SSL_CERT_FILE"), os.environ.get("REQUESTS_CA_BUNDLE"), "/root/.ccr/ca-bundle.crt"):
        if ca and os.path.exists(ca):
            ctx.load_verify_locations(ca)
            break
    return ctx


def synth(text, prev_text, next_text, cfg, ctx):
    body = {
        "text": text,
        "model_id": cfg.get("model_id", "eleven_multilingual_v2"),
        "voice_settings": cfg.get("voice_settings", {}),
    }
    if cfg.get("language_code"):
        body["language_code"] = cfg["language_code"]
    # eleven_v3 ยังไม่รองรับ previous_text/next_text
    use_ctx = cfg.get("use_context", not body["model_id"].startswith("eleven_v3"))
    if use_ctx and prev_text:
        body["previous_text"] = prev_text
    if use_ctx and next_text:
        body["next_text"] = next_text
    if cfg.get("seed") is not None:
        body["seed"] = cfg["seed"]
    url = API.format(voice_id=cfg["voice_id"], fmt=cfg.get("output_format", "mp3_44100_128"))
    # ค่า placeholder — proxy จะแทนที่ด้วย key จริง; ถ้ามี env ก็ใช้ env
    key = os.environ.get("ELEVENLABS_API_KEY", "proxy-injected")
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), method="POST",
                                 headers={"Content-Type": "application/json", "Accept": "audio/mpeg",
                                          "xi-api-key": key})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=120) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", "replace")[:500]
            if e.code in (401, 403):
                sys.exit(f"ERROR {e.code}: ไม่มีสิทธิ์/ไม่มี API key สำหรับ api.elevenlabs.io — รายงานโปรดิวเซอร์\n{msg}")
            if e.code == 429 or e.code >= 500:
                time.sleep(2 ** attempt * 2)
                continue
            sys.exit(f"ERROR {e.code}: {msg}")
        except urllib.error.URLError as e:
            time.sleep(2 ** attempt * 2)
            last = e
    sys.exit(f"ERROR: เรียก API ไม่สำเร็จหลังลองหลายครั้ง: {last if 'last' in dir() else ''}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("out_dir")
    ap.add_argument("--only", help="พากย์ใหม่เฉพาะประโยค เช่น 3,7")
    ap.add_argument("--story", help="story.json (ค่าเริ่มต้น: ข้างไฟล์ script)")
    ap.add_argument("--voice-config", default=os.path.join(HERE, "voice.json"))
    a = ap.parse_args()

    cfg = json.load(open(a.voice_config, encoding="utf-8"))
    if not cfg.get("voice_id") or cfg["voice_id"].startswith("<"):
        sys.exit("ERROR: ยังไม่ได้ตั้ง voice_id ใน tools/audio/voice.json — ให้เจ้าของช่องเลือกเสียงก่อน")
    lines = [l.strip() for l in open(a.script, encoding="utf-8") if l.strip()]
    sp = a.story or os.path.join(os.path.dirname(os.path.abspath(a.script)), "story.json")
    speakers = [None] * len(lines)
    silent = [False] * len(lines)
    if os.path.exists(sp):
        sl = json.load(open(sp, encoding="utf-8")).get("lines", [])
        if len(sl) != len(lines):
            sys.exit(f"ERROR: story.json มี {len(sl)} บรรทัด แต่ script มี {len(lines)} บรรทัด — ไม่เท่ากัน")
        speakers = [l.get("speaker") for l in sl]
        silent = [bool(l.get("silent")) for l in sl]
        for sk in set(speakers) - {None}:
            if sk not in cfg.get("voices", {}):
                sys.exit(f"ERROR: speaker '{sk}' ไม่มีใน voices ของ voice.json")
    only = {int(x) for x in a.only.split(",")} if a.only else None
    os.makedirs(a.out_dir, exist_ok=True)
    ctx = ssl_ctx()
    total_chars = 0
    for i, text in enumerate(lines, 1):
        if only and i not in only:
            continue
        if silent[i - 1]:
            print(f"[{i:02d}] (silent — ข้าม) {text}")
            continue
        prev_t = lines[i - 2] if i > 1 and not silent[i - 2] else None
        next_t = lines[i] if i < len(lines) and not silent[i] else None
        c = dict(cfg)
        if speakers[i - 1]:
            c.update(cfg["voices"][speakers[i - 1]])
            c.pop("voices", None)
            prev_t = next_t = None  # เสียงต่างคน ไม่ส่งบริบทข้ามคน
        audio = synth(text, prev_t, next_t, c, ctx)
        path = os.path.join(a.out_dir, f"line_{i:02d}.mp3")
        with open(path, "wb") as f:
            f.write(audio)
        total_chars += len(text)
        print(f"[{i:02d}] {len(audio)/1024:6.1f} KB  {('<'+speakers[i-1]+'> ') if speakers[i-1] else ''}{text}")
    print(f"done: {total_chars} ตัวอักษร (≈ เครดิตที่ใช้ ขึ้นกับโมเดล)")


if __name__ == "__main__":
    main()
