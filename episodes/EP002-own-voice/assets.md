# รายการไฟล์ที่ใช้ในคลิป (ลิขสิทธิ์) — EP002 ทำไมเสียงตัวเองในคลิปฟังแปลก?

ไฟล์คลิป: `video/renders/EP002-own-voice.mp4` (1080×1920, 30fps, 52.0 วิ (mix.wav 51.99 วิ), H.264 + AAC 48k สเตอริโอ, −14.0 LUFS / true peak −2.2 dBTP วัดจาก mp4 — บท v3, เสียงเร่ง 13%)

| ไฟล์ | ประเภท | ที่มา | ใบอนุญาต | ใช้เชิงพาณิชย์ได้ |
|---|---|---|---|---|
| `video/assets/lib/kid.js` (คัดลอกจาก `character/kid.js` รวม `eye:"blink"`) | ตัวละคร | สร้างเองในโปรเจกต์ | ของช่อง | ✅ |
| `video/assets/lib/art.js` | ภาพประกอบ SVG (หัวตัดขวางแบบเรียบ หูชั้นใน/คอเคลีย ที่อุดหู มือถือ ไมค์ ลำโพง กองกระดาษ คลื่น คลิปบอร์ด หลอดทดลอง นาฬิกาจับเวลา กระดานคะแนน ฯลฯ — ไม่มีโลโก้/ยี่ห้อ/หน้าคน) | วาดด้วยโค้ดในโปรเจกต์ (ฝ่ายภาพ) ต่อยอดจาก EP001 | ของช่อง | ✅ |
| `video/index.html`, `video/compositions/*.html` | โปรเจกต์ตัดต่อ HyperFrames | สร้างเองในโปรเจกต์ | ของช่อง | ✅ |
| `audio/mix.wav` → `video/assets/audio/mix.wav` | เสียงพากย์ + SFX ที่มิกซ์แล้ว (ไม่เพิ่ม gain ตอนเรนเดอร์) | ฝ่ายเสียง (ElevenLabs + tools/sfx) | ตามแถวด้านล่าง | ✅ |
| `audio/raw/*` (เสียงพากย์) | เสียงพากย์ | ElevenLabs (แพ็กเกจ: Starter ขึ้นไป (เจ้าของช่องยืนยัน 2026-11-21)) | ตามแพ็กเกจ (ใบอนุญาตเชิงพาณิชย์) | ✅ |
| `sfx/*.wav` (pop, thud, blip_talk, tick, glint, wrong, whoosh, ding, riser, boing) | เสียงประกอบ | `tools/sfx/make_sfx.py` (สร้างจากโค้ด) | ของช่อง | ✅ |
| `video/assets/fonts/noto-sans-thai-thai-{400,700,900}-normal.woff2` | ฟอนต์ไทย Noto Sans Thai (ฝังด้วย @font-face) | npm `@fontsource/noto-sans-thai@5.3.0` (ผ่าน `assets/fonts/`) | SIL OFL 1.1 (`video/assets/fonts/OFL-LICENSE.txt`) | ✅ |
| `video/assets/fonts/noto-sans-latin-{700,900}-normal.woff2` | ฟอนต์ละติน/ตัวเลข/เครื่องหมาย Noto Sans (ตัวเลข "2", "79%", "17%", "?", "!", "+", "=", ":", "…", เครื่องหมายคำพูด ในซับและป้าย) | npm `@fontsource/noto-sans@5.3.0` | SIL OFL 1.1 (`video/assets/fonts/OFL-LICENSE-noto-sans.txt`) | ✅ |
| `video/assets/lib/gsap.min.js` | ไลบรารีอนิเมชัน | npm `gsap@3.14.2` (`npm pack` → `dist/gsap.min.js`) | GSAP Standard License ("no charge" ใช้เชิงพาณิชย์ได้) | ✅ |
| HyperFrames CLI 0.9.72 | เครื่องมือเรนเดอร์ (ไม่ได้ฝังในคลิป) | npm `hyperframes` | ตามใบอนุญาตของเครื่องมือ | ✅ |

หมายเหตุ
- ไม่มีภาพจากเว็บ ภาพถ่าย เพลง หรือเสียงภายนอก ภาพประกอบทุกชิ้นวาดเป็น SVG ด้วยโค้ด
- ภาพหัวตัดขวางเป็นภาพแยก ไม่ได้ผ่าหัวตัวละคร · มือถือ/ไมค์/ลำโพง/กระดาษงานวิจัยไม่มีโลโก้ ยี่ห้อ หรือชื่อวารสาร
- ทุกตัวอักษรใช้ฟอนต์ที่ฝังในโปรเจกต์ ไม่พึ่งฟอนต์ระบบ · โปรเจกต์ไม่มีลิงก์ http ภายนอก
