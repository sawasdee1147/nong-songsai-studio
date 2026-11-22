# ตัวละคร: น้องสงสัย

ไลบรารีวาดตัวละครเป็น SVG ด้วยโค้ด ทุกท่าประกอบจากชิ้นส่วนชุดเดียวกัน จึงขยับเป็นอนิเมชั่นได้โดยไม่ต้องวาดใหม่

- `kid.js` — ไลบรารีหลัก (ห้ามแก้ลายเส้น/สีโดยไม่ได้รับอนุมัติจากเจ้าของช่อง)
- `sheet.html` / `sheet.png` — แผ่นตัวละคร (ท่ามาตรฐานทั้งหมด)
- `outro-push-glasses.html` / `.mp4` / `.gif` — ท่าปิดคลิปประจำตัว (ดันแว่น)

## วิธีใช้

```html
<script src="kid.js"></script>
<script>
  el.innerHTML = kid({ eye: "cool", brow: "cool", mo: "smirk", arm: "left", push: 1, gdy: -5, glint: 1 });
</script>
```

`kid(options)` คืนค่าเป็นสตริง `<svg>` (viewBox `20 -40 260 400`, สัดส่วนกว้าง:สูง ≈ 0.65)

| option | ค่า | ความหมาย |
|---|---|---|
| `eye` | `norm` `up` `smug` `shock` `spark` `laugh` `side` `wink` `cool` `sad` `blink` | ตา (`cool` = ตาแอ๊คครึ่งปิด, `blink` = ตาปิดโค้งลง ใช้ทำกะพริบตา 3–4 เฟรม) |
| `brow` | `norm` `smug` `up` `shock` `worry` `cool` `none` | คิ้ว |
| `mo` | `smile` `o` `smirk` `shock` `grin` `tongue` `flat` `flatlow` `wobble` | ปาก |
| `ah` | `?` `!` `zig` `droop` `heart` | ผมชี้ (สงสัย / เข้าใจแล้ว / ตกใจ / เบื่อ / เขิน) |
| `gl` | `norm` `glare` `askew` `down` `none` | แว่น (เลนส์แวบ / เบี้ยว / เลื่อนลงจมูก) |
| `arm` | `down` `chin` `up` `point` `belly` `shrug` `cover` `left` | แขน (`left` = แขนซ้ายอย่างเดียว ใช้คู่กับ `push`) |
| `push` | 0–1 | แขนขวายกขึ้นดันแว่น (0 = ลง, 1 = นิ้วแตะกลางแว่น) |
| `gdy` | ตัวเลข | เลื่อนแว่นขึ้นลง (บวก = ไหลลง) |
| `glint` | 0–1+ | ขนาดประกายดาวบนเลนส์ |
| `tilt` | องศา | เอียงตัว |
| `front` | true/false | วาดแขนทับหน้า (ท่าเอามือแตะหน้า) |
| `extra` | SVG string | ของประกอบเพิ่ม เช่น เหงื่อ ประกาย เครื่องหมายคำถาม |

## ท่ามาตรฐาน (preset)

| ท่า | ใช้ตอน | options |
|---|---|---|
| สงสัย | ฮุกเปิดคลิป | `{eye:"up",brow:"up",mo:"o",arm:"chin",front:true}` |
| กวนๆ (แว่นแวบ) | "รู้ป่าว~ ไม่บอกหรอก" | `{gl:"glare",eye:"smug",brow:"smug",mo:"smirk",arm:"shrug",tilt:5}` |
| ตกใจ | ข้อเท็จจริงแปลกๆ | `{gl:"askew",eye:"shock",brow:"shock",mo:"shock",ah:"zig",arm:"up"}` |
| ปิ๊ง! | เฉลย | `{eye:"spark",brow:"none",mo:"grin",ah:"!",arm:"point"}` |
| หัวเราะ | หลังแกล้งคนดู | `{eye:"laugh",brow:"none",mo:"grin",arm:"belly",tilt:-6,front:true}` |
| แลบลิ้น | ปิดแบบซนๆ | `{eye:"wink",brow:"none",mo:"tongue",arm:"point",tilt:6}` |
| มองข้ามแว่น | "เธอก็สงสัยใช่มั้ยล่ะ" | `{gl:"down",eye:"side",brow:"none",mo:"flatlow",ah:"droop"}` |
| ดันแว่น | **ท่าปิดคลิปประจำตัว** | `{eye:"cool",brow:"cool",mo:"smirk",arm:"left",push:1,gdy:-5,glint:1}` |
| เขินๆ | โดนจับได้ว่าผิด | `{eye:"sad",brow:"worry",mo:"wobble",ah:"heart",arm:"cover",front:true}` |

ดูจังหวะดันแว่นแบบเต็มได้ที่ฟังก์ชัน `draw(t)` ใน `outro-push-glasses.html`

## ตัวละครอื่นในเรื่อง (เพิ่ม 2026-11-22 — เจ้าของช่องอนุมัติ)
`kid()` วาดตัวละครใหม่ในลายเส้นเดียวกันได้ ค่าเริ่มต้นทั้งหมด = น้องสงสัย (ตรวจแล้วว่าภาพเหมือนเดิมทุกพิกเซล)

| option | ค่า | ความหมาย |
|---|---|---|
| `skin` | `nong` `light` `tan` `dark` `ghost` หรือ hex | สีผิว (`ghost` = ผีซีด ไม่มีแก้มแดง) |
| `hair` | `nong` `short` `spiky` `long` `bun` `bald` | ทรงผม (`nong` = ทรงน้องสงสัย) |
| `hairColor` | hex | สีผม |
| `top` | hex | สีเสื้อ |
| `pocket`, `strings` | true/false | กระเป๋าหน้าท้อง / เชือกฮู้ด (ตัวละครอื่นควรปิดทั้งคู่ ให้ต่างจากน้องสงสัย) |
| `eye` เพิ่ม | `sleep` `creepy` | หลับ / ตาดำล้วนแบบหลอน |
| `ah` เพิ่ม | `none` | ไม่มีผมชี้ — **ผมชี้ ? และแว่นกลมสงวนไว้ให้น้องสงสัยเท่านั้น** ตัวละครอื่นใช้ `ah:"none"` และ `gl:"none"` |

ตัวอย่าง: `kid({skin:"tan",hair:"short",hairColor:"#3A2A20",top:"#4F6FA8",gl:"none",ah:"none",pocket:false,strings:false})`
