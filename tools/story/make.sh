#!/bin/bash
# คำสั่งเดียว: เสียง (ที่พากย์แล้ว) -> เสียงประกอบ + ซาวด์คลอ -> หน้า HyperFrames -> lint -> render -> contact sheet
# ใช้: bash tools/story/make.sh episodes/<EP>
# ก่อนรัน: พากย์ด้วย tools/audio/tts_elevenlabs.py <EP>/script.tts.txt <EP>/audio/raw  (ทำครั้งเดียว ประหยัดเครดิต)
set -e
R="$(cd "$(dirname "$0")/../.." && pwd)"; EP="$(cd "$1" && pwd)"; cd "$R"
TEMPO=$(python3 -c "import json;print(json.load(open('tools/audio/voice.json'))['tempo'])")
MOOD=$(python3 -c "import json;print(json.load(open('$EP/story.json')).get('mood','dark'))")
TAIL=$(python3 -c "import json;s=json.load(open('$EP/story.json'));print(4.0 if any(l.get('outro') for l in s['lines']) else 1.5)")
python3 tools/audio/assemble.py "$EP/audio/raw" "$EP/audio" --script "$EP/script.tts.txt" --tempo "$TEMPO" --gap-min 0.2 --gap-max 0.22 || echo "⚠️ มีประโยคเกิน 3 วิ (ดูด้านบน)"
python3 tools/story/cues.py "$EP"
python3 tools/audio/mix.py "$EP/audio/voice.wav" "$EP/audio/sfx_cues.json" "$EP/audio/mix.wav" --tail "$TAIL" --bed "sfx/bed_$MOOD.wav"
python3 tools/story/build.py "$EP"
cd "$EP/video"
[ -f hyperframes.json ] || cp "$R/episodes/EP002-own-voice/video/hyperframes.json" .
hyperframes lint . | tail -3
mkdir -p renders
NAME=$(basename "$EP")
hyperframes render . -o "renders/$NAME.mp4" > render.log 2>&1 || { tail -20 render.log; exit 1; }
OUT="renders/$NAME.mp4"
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT")
mkdir -p frames
for i in $(seq 0 13); do
  ffmpeg -nostdin -v error -y -ss "$(python3 -c "print(round($D*($i+.5)/14,2))")" -i "$OUT" -frames:v 1 -vf scale=216:-1 "frames/s_$(printf %02d $i).png"
done
python3 -c "
from PIL import Image;import glob
fs=sorted(glob.glob('frames/s_*.png'));ims=[Image.open(f) for f in fs];w,h=ims[0].size
o=Image.new('RGB',(w*7,h*2),'white')
for k,im in enumerate(ims): o.paste(im,((k%7)*w,(k//7)*h))
o.save('frames/sheet.png')"
rm -f frames/s_*.png
ffmpeg -nostats -i "$OUT" -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|Peak):" | tail -2
echo "DONE: $EP/video/$OUT  (ตรวจ $EP/video/frames/sheet.png)"
