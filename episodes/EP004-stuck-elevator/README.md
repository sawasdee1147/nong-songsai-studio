# EPxxx: <หัวข้อ>

| ขั้น | ไฟล์ | สถานะ |
|---|---|---|
| หัวข้อที่เลือก | `topic.md` | ⬜ |
| Fact sheet | `factsheet.md` | ⬜ |
| บท | `script.md`, `script.tts.txt` | ⬜ |
| ตรวจข้อเท็จจริง | `factcheck.md` | ⬜ |
| ตรวจบท (QA) | `qa-script.md` | ⬜ |
| ⛔ เจ้าของช่องเลือกฮุก/อนุมัติบท | — | ⬜ |
| เสียง | `audio/voice.wav`, `audio/timings.json`, `audio/mix.wav`, `audio/audio-report.md` | ⬜ |
| วิดีโอ | `video/renders/EPxxx.mp4`, `assets.md` | ⬜ |
| ตรวจคลิป (QA) | `qa-final.md` | ⬜ |
| การตลาด | `marketing.md` | ⬜ |
| ⛔ เจ้าของช่องอนุมัติโพสต์ | — | ⬜ |
| โพสต์แล้ว | ลิงก์: | ⬜ |

## โน้ตนิค: ต้องใส่ใน story.json (ฝ่ายภาพเพิ่ม "peek" ใน build.py 2026-11-23)
- บรรทัด "ก๊อก ก๊อก ก๊อก…" → `"bg": "elevator_hatch_up_knock"`
- บรรทัด "แสงไฟฉาย ส่องลงมา…" → `"bg": "elevator_hatch_up_open", "push": 1.12`, chars: N `{x:300,y:900,w:460}` ท่าตกใจ + `{"who":"Y","peek":"down","pose":{"eye":"norm","mo":"flat"}}`
- บรรทัดตุ้งแช่ "หน้าลุงยาม…โผล่มาจ้องคุณ" → `"jumpscare": {"who":"Y","peek":"down","bg":"elevator_hatch_up_open","pose":{"eye":"creepy","mo":"flatlow"}}`
- ฉาก shaft: ตัวละคร `{x:20,y:1000,w:380}` (เดิมโดนซับบัง)
- พิจารณา hairColor ของ Y เป็นเทา (หัวกลับแล้วผมดำดูเหมือนเครา)
