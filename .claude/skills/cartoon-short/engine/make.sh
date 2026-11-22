#!/bin/bash
# One command: story.json -> voice -> sound -> page -> lint -> render -> frame sheet.
# usage: bash make.sh PROJECT_DIR [--own]
set -e
E="$(cd "$(dirname "$0")" && pwd)"; P="$(cd "$1" && pwd)"; shift || true
python3 "$E/voice.py" "$P" "$@" 2>&1 | grep -v -i warn || true
[ -f "$P/work/timing.json" ] || { echo "voice step failed"; exit 1; }
python3 "$E/sfx.py" "$P"
python3 "$E/build.py" "$P"
cd "$P"
npx -y hyperframes lint site
mkdir -p renders
OUT="renders/$(date +%H%M%S).mp4"
npx -y hyperframes render site -o "$OUT" > work/render.log 2>&1 || { tail -20 work/render.log; exit 1; }
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT")
for i in 0 1 2 3 4 5 6 7 8 9; do
  ffmpeg -nostdin -v error -y -ss "$(python3 -c "print(round($D*($i+.5)/10,2))")" -i "$OUT" -vframes 1 -vf scale=270:-1 "work/sheet_$i.png"
done
ffmpeg -v error -y $(for i in 0 1 2 3 4 5 6 7 8 9; do printf -- "-i work/sheet_$i.png "; done) \
  -filter_complex "xstack=inputs=10:layout=0_0|w0_0|w0+w1_0|w0+w1+w2_0|w0+w1+w2+w3_0|0_h0|w0_h0|w0+w1_h0|w0+w1+w2_h0|w0+w1+w2+w3_h0" work/sheet.jpg
rm -f work/sheet_*.png
echo "DONE: $P/$OUT  (check $P/work/sheet.jpg)"
