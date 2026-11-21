# รายการไฟล์ที่ใช้ในคลิป (ลิขสิทธิ์) — EP001 ทำไมกินพริกแล้วรู้สึกร้อน?

ไฟล์คลิป: `video/renders/EP001-chili-heat.mp4` (1080×1920, 30fps, 44.03 วิ, H.264 + AAC)

| ไฟล์ | ประเภท | ที่มา | ใบอนุญาต | ใช้เชิงพาณิชย์ได้ |
|---|---|---|---|---|
| `video/assets/lib/kid.js` (คัดลอกจาก `character/kid.js`) | ตัวละคร | สร้างเองในโปรเจกต์ | ของช่อง | ✅ |
| `video/assets/lib/art.js` | ภาพประกอบ SVG (พริก หน้ากากไฟ โมเลกุล สมอง ประตู TRPV1 เทอร์โมมิเตอร์ ลิ้น เหรียญวาดเอง ฯลฯ) | วาดด้วยโค้ดในโปรเจกต์ (ฝ่ายภาพ) | ของช่อง | ✅ |
| `video/index.html`, `video/compositions/*.html` | โปรเจกต์ตัดต่อ HyperFrames | สร้างเองในโปรเจกต์ | ของช่อง | ✅ |
| `audio/mix.wav` → `video/assets/audio/mix.wav` | เสียงพากย์ + SFX ที่มิกซ์แล้ว | ฝ่ายเสียง (ElevenLabs + tools/sfx) | ตามแถวด้านล่าง | ✅ |
| `audio/raw/*` (เสียงพากย์) | เสียงพากย์ | ElevenLabs (แพ็กเกจ: Starter ขึ้นไป (เจ้าของช่องยืนยัน 2026-11-21)) | ตามแพ็กเกจ (ใบอนุญาตเชิงพาณิชย์) | ✅ |
| `sfx/*.wav` (swoosh_down, wrong, glint, pop, tick, riser, thud, whoosh, boing, bubble, ding) | เสียงประกอบ | `tools/sfx/make_sfx.py` (สร้างจากโค้ด) | ของช่อง | ✅ |
| `video/assets/fonts/noto-sans-thai-thai-{400,700,900}-normal.woff2` (คัดลอกจาก `assets/fonts/`) | ฟอนต์ Noto Sans Thai (ฝังในโปรเจกต์ ใช้ @font-face ไม่โหลดจาก CDN) | Google Fonts / Noto Project | SIL OFL 1.1 (`video/assets/fonts/OFL-LICENSE.txt`) | ✅ |
| `video/assets/fonts/noto-sans-latin-{700,900}-normal.woff2` | ฟอนต์ละติน/ตัวเลข/เครื่องหมาย Noto Sans (TRPV1, 40°C+, capsaicin, Nobel 2021 · David Julius, Ardem Patapoutian, ตัวเลข/! /" ในซับ) ฝังในโปรเจกต์ด้วย @font-face | npm `@fontsource/noto-sans@5.3.0` (Noto Project / Google) | SIL OFL 1.1 (`video/assets/fonts/OFL-LICENSE-noto-sans.txt`) | ✅ |
| `video/assets/lib/gsap.min.js` | ไลบรารีอนิเมชัน | npm `gsap@3.14.2` (`npm pack gsap@3.14.2` → `dist/gsap.min.js`) | GSAP Standard License ("no charge" ใช้เชิงพาณิชย์ได้) | ✅ |
| HyperFrames CLI 0.9.72 | เครื่องมือเรนเดอร์ (ไม่ได้ฝังในคลิป) | npm `hyperframes` | ตามใบอนุญาตของเครื่องมือ | ✅ |

หมายเหตุ
- ไม่มีภาพจากเว็บ ภาพถ่าย เพลง หรือเสียงภายนอก ภาพประกอบทุกชิ้นวาดเป็น SVG ด้วยโค้ด
- เหรียญในฉาก 13 วาดเองแบบเรียบ (วงกลมเหลือง + ริบบิ้น + ดาว) ไม่มีหน้าคน ไม่เลียนแบบเหรียญจริง/โลโก้/ตรา/ฟอนต์ของมูลนิธิโนเบล
- เครื่องหมาย "≠" ในป้าย "พริก ≠ ไฟ" วาดเป็น SVG ในโปรเจกต์ (ไม่มีในชุดอักษรของฟอนต์ที่ฝัง) จึงไม่มีตัวอักษรใดดึงจากฟอนต์ระบบ
- `kid.js` เพิ่มตัวเลือก `eye:"blink"` (ตาปิด ใช้กะพริบ) ตามคำสั่งโปรดิวเซอร์ ไม่เปลี่ยนลายเส้น/สีของท่าเดิม
- โปรเจกต์ไม่มีลิงก์ http ภายนอก ทุกไฟล์โหลดจากในโฟลเดอร์ `video/`
