---
name: cartoon-short
description: Make one finished Thai cartoon story video (9:16) from just a topic. The user types a story idea; this skill writes the script with the 4-move formula, voices it with a free Thai voice, draws every scene in code (flat 2.5D characters, cream fact cards, clock chip, big Kanit captions), adds self-made sound, and renders the MP4. Use when the user says "ทำการ์ตูน", "การ์ตูนเล่าเรื่อง", "cartoon short", or gives a story topic to turn into a cartoon.
---

# Cartoon Short (by Editarae)

The user gives a topic. You deliver ONE finished MP4. Do every step yourself, without asking, except step 2.

Any kind of story works: horror, comedy, history, true crime, life lesson, love, business. What stays fixed is the
art style (flat 2.5D shaded characters, cream fact cards, clock chip, big Kanit captions, grain). Never switch to
another visual style, AI images or stock footage; draw new props in the same flat style with `extra`.

## Setup check (once)
Run: `python3 -c "import numpy, gtts" && ffmpeg -version | head -1 && node -v`
Missing something? `pip3 install numpy gTTS`, install ffmpeg (Mac: `brew install ffmpeg`) and Node 18+ (nodejs.org).
HyperFrames is fetched by `npx` on first render.

**Voice (recommend ElevenLabs).** Ask once whether the user has an ElevenLabs account. ElevenLabs sounds like a real
person; the free gTTS voice is clearly robotic. The free ElevenLabs plan (elevenlabs.io, about 10,000 characters a
month, roughly 15-20 shorts) is enough to start. Tell the user to save their own API key themselves (never paste it
in chat): ElevenLabs > Developers > API Keys > create, then in Terminal
`echo 'THE_KEY' > ~/.elevenlabs_key`. With that file present the engine uses ElevenLabs (`eleven_v3`, speaks Thai)
automatically. No key: it falls back to the free gTTS voice; say so in one line and carry on.

## 1. Project folder
Make `cartoon-<short-topic-in-english>/` in the current directory. All files go there.

## 2. Script: the 4-move formula
Write the story in Thai (shorts: 6-10 lines, ~30-60 s), spoken to the viewer as "คุณ". Each line ≤ ~5 s when read aloud (~25 Thai syllables).

1. **Hook in ≤ 12 words, second person.** Line 1 must make the viewer ask a question. Strong default: "ถ้าคุณ… อย่า…" (a warning); for comedy or life stories, a surprising claim works too.
2. **A real number on screen.** 1-3 lines carry a fact card with a REAL number and a real source (study / agency /
   book, author + year). Never invent a number or a source. Not sure it is true? Drop the card. Add a clock chip on
   lines where time matters (it makes the story feel real).
3. **Twist at 60-75%** (`"twist": true` on that line): the thing the viewer trusted turns out wrong.
4. **Cliffhanger last line**: an open question, never a moral. The outro card says "ตอนหน้า…".

Rules for every line: link lines with แต่ / เลย / แล้ว (cause → effect, never "and then… and then"). Plant one small
clue early that the twist pays off. Show feelings through the body (freeze, stare, no blink), not with labels.

Show the user the script as a short table (line / caption / card source) and ask once: "โอเคไหม หรือแก้ตรงไหน".
After they agree, never ask again until the video is done.

## 3. Write story.json
Copy `example/story.json` from this skill and replace the content. Fields:

- `mood`: `"dark"` (horror, suspense, crime: drone) or `"warm"` (comedy, love, life, history: soft pad). `outro`: the end-card line.
- `engine`: `"eleven"` (default when `~/.elevenlabs_key` exists), `"gtts"` (free, robotic), `"edge"` (free Microsoft voice, sometimes fails on Thai), `"say"` (Mac offline).
  `voice`: ElevenLabs voice ID (ElevenLabs > Voices > copy ID); pick a Thai-capable voice that fits the story (warm, low, young…). Empty = first voice in the account.
- `cast`: any number, keys `A` `B` `C` …. `skin`: tan | light | dark | ghost. `hair`: short | long | bun | bald.
  `hair_color`, `shirt`: hex colors. Ghost = pale, never blinks.
- each line:
  - `vo`: what is spoken. Write numbers as words if the voice misreads digits.
  - `cap`: caption chunks split by `|`, 1-3 words each. `*` before a word = yellow key, `!` = red pill. One key per line max.
  - `en`: small English line under the caption.
  - `card`: `{"k": label, "n": "17", "u": unit, "s": one-line detail, "src": "Author et al. YEAR · Journal"}`.
  - `clock`: `{"t": "03:00", "s": "ตีสาม"}`. `sfx`: list of `heart thump creak tick boom` or `["heart", 0.8]` (offset s).
  - `twist`: true on the twist line. `pause`: extra silence after the line (s).
  - `scene`:
    - `bg`: room_night | room_day | village_dusk | street_night | forest_night | office_day | office_night | dark
    - `chars`: list of `{"who": "A", "x": 540, "y": 1150, "s": 1.3, "face": ..., "look": "left|right", "flip": bool, "talk": bool}`
      faces: neutral smile sad angry scared creepy sleep. Close-up = `s` 2.0-2.6 with y ~1000-1100, on bg `dark`.
      Two people: x ~300 and ~800, s 1.1-1.3. Keep faces above y 1350 (captions sit at 1420-1640).
    - `push`: camera zoom over the shot (default 1.14, twist 1.35). `shake`: true for a shock.
    - `extra`: optional raw SVG drawn behind the characters (a prop: door, phone, bowl). Simple shapes, flat colors.

Vary the shots: alternate wide (2 people) and close-up (1 face on `dark`). Never the same bg + framing twice in a row.

## 4. Make it
`bash <this skill>/engine/make.sh cartoon-<topic>`
It voices every line, makes the sound, builds the page, renders, and saves `work/sheet.jpg` (10 frames).

## 5. Check before you hand it over
Open `work/sheet.jpg` and look. Fix and re-run `make.sh` if:
- a card or the outro covers a face, or a face sits under the captions
- a caption runs off the screen edge (split the chunk smaller)
- two shots in a row look the same
Then listen: compare `work/vo/*_t.wav` against the script; if the voice misreads a word, respell it in `vo` and re-run.

Hand over: the MP4 path, the 1-line story, and the card sources. Tell the user they can post it as is.
