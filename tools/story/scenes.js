// ฉากและท่าพิเศษสำหรับคลิปแนวเล่าเรื่อง — ลายเส้นของช่อง: ขอบหมึกหนา สีเรียบ ไม่มีไล่เฉด
// ใช้คู่กับ character/kid.js  (ต้องโหลด kid.js ก่อน)
const SC_INK = "#2B2B2B";
const _sv = inner => `<svg width="1080" height="1920" viewBox="0 0 1080 1920" style="position:absolute;inset:0">${inner}</svg>`;

// ---------- เตียง (ใช้ร่วมกับท่านอน) ----------
const BED = `<g stroke="${SC_INK}" stroke-width="8" stroke-linejoin="round">
  <rect x="160" y="1090" width="600" height="200" rx="30" fill="#7A86B8"/>
  <rect x="150" y="930" width="330" height="200" rx="70" fill="#FFF8EC"/>
  <path d="M180 990 Q315 955 450 990" fill="none" stroke-width="5" opacity=".35"/>
  <path d="M150 1290 H770"/></g>`;
const BLANKET = _sv(`<g transform="translate(120 0) scale(.92 1)"><path d="M300 990 Q330 960 380 965 L680 975 Q706 978 706 1005 L700 1180 Q698 1200 676 1200 L310 1200 Q290 1198 292 1176Z" fill="#9AA6D8" stroke="${SC_INK}" stroke-width="8" stroke-linejoin="round"/><path d="M300 1012 Q490 1000 700 1015" fill="none" stroke="${SC_INK}" stroke-width="6"/></g>`);

// ---------- ไรรูขุมขน (pore_zoom) ----------
// ไร 1 ตัว: รูขุมขนอยู่ที่จุด (0,0) ตัวโผล่ขึ้นด้านบน  ขอบรูด้านหน้าบังโคนตัว
// (ตามผลตรวจข้อเท็จจริง: ไรไม่มีตา -> ไม่วาดตา; โผล่จากรูเท่านั้น ไม่เดินบนผิว)
const _PORE = "#4A2C36", _MITE = "#FFF6E2";
function _mite(x, y, rot = 0, s = 1) {
  const leg = (lx, ly, dx) => `<path d="M${lx} ${ly} l${dx} 6" stroke="${SC_INK}" stroke-width="15" stroke-linecap="round"/><path d="M${lx} ${ly} l${dx} 6" stroke="${_MITE}" stroke-width="6" stroke-linecap="round"/>`;
  let legs = ""; for (const ly of [-124, -110, -96, -82]) legs += leg(-20, ly, -16) + leg(20, ly, 16);
  return `<g transform="translate(${x} ${y}) rotate(${rot}) scale(${s})">
    <ellipse cx="0" cy="0" rx="40" ry="16" fill="${_PORE}" stroke="${SC_INK}" stroke-width="6"/>
    ${legs}
    <path d="M-21 8 L-23 -110 Q-23 -158 0 -158 Q23 -158 23 -110 L21 8Z" fill="${_MITE}" fill-opacity=".92" stroke="${SC_INK}" stroke-width="7" stroke-linejoin="round"/>
    <g fill="none" stroke="${SC_INK}" stroke-width="4" stroke-linecap="round" opacity=".3"><path d="M-17 -64 Q0 -58 17 -64"/><path d="M-17 -44 Q0 -38 17 -44"/><path d="M-17 -24 Q0 -18 17 -24"/></g>
    <ellipse cx="-14" cy="-117" rx="5" ry="3" fill="#FF9BA8" opacity=".8"/><ellipse cx="14" cy="-117" rx="5" ry="3" fill="#FF9BA8" opacity=".8"/>
    <path d="M-5 -118 Q0 -113 5 -118" fill="none" stroke="${SC_INK}" stroke-width="3.5" stroke-linecap="round"/>
    <path d="M-40 0 A40 16 0 0 0 40 0Z" fill="${_PORE}"/><path d="M-40 0 A40 16 0 0 0 40 0" fill="none" stroke="${SC_INK}" stroke-width="6"/></g>`;
}
const _pore = (x, y, rx = 38) => `<ellipse cx="${x}" cy="${y}" rx="${rx}" ry="${rx * .42}" fill="${_PORE}" stroke="${SC_INK}" stroke-width="6"/>`;
let _pzN = 0; // id ของ clipPath ต้องไม่ซ้ำ เมื่อใช้ฉากนี้หลายครั้งในหน้าเดียว
const PORE_ZOOM = (mites = true) => { const id = `pzLens${++_pzN}`; return _sv(`<rect width="1080" height="1920" fill="#2E2A47"/>
    <circle cx="600" cy="700" r="560" fill="#3B3352"/>
    <g fill="#26223B">${[[110,260,14],[260,1180,12],[90,620,10],[930,1240,14],[1000,300,11],[760,1500,12],[180,1620,10],[960,1700,13],[480,1320,9],[60,1020,11]].map(([x,y,r]) => `<ellipse cx="${x}" cy="${y}" rx="${r}" ry="${r * .5}"/>`).join("")}</g>
    <defs><clipPath id="${id}"><circle cx="600" cy="700" r="356"/></clipPath></defs>
    <g transform="rotate(-45 600 700)" stroke="${SC_INK}" stroke-width="8" stroke-linejoin="round">
      <rect x="575" y="1080" width="50" height="40" fill="#8A7AA8"/>
      <rect x="560" y="1115" width="80" height="270" rx="36" fill="#6B4E8A"/>
      <path d="M580 1160 V1340" stroke="#FFF8EC" stroke-width="8" stroke-linecap="round" opacity=".35"/></g>
    <g clip-path="url(#${id})">
      <rect x="220" y="320" width="760" height="760" fill="#F2CCA6"/>
      <g fill="none" stroke="${SC_INK}" stroke-width="5" stroke-linecap="round" opacity=".14">
        <path d="M250 760 Q420 720 560 770 T900 740"/><path d="M300 980 Q500 940 700 990"/><path d="M330 430 Q520 400 760 440"/></g>
      ${_pore(560, 950, 32)}${_pore(330, 840, 26)}
      ${_pore(860, 580, 30)}
      <path d="M860 580 Q870 470 960 360" fill="none" stroke="${SC_INK}" stroke-width="24" stroke-linecap="round"/>
      <path d="M860 580 Q870 470 960 360" fill="none" stroke="#5A3A2A" stroke-width="12" stroke-linecap="round"/>
      <path d="M330 840 Q290 760 230 720" fill="none" stroke="${SC_INK}" stroke-width="20" stroke-linecap="round"/>
      <path d="M330 840 Q290 760 230 720" fill="none" stroke="#5A3A2A" stroke-width="10" stroke-linecap="round"/>
      ${mites ? `${_mite(440, 660, -16, 1.05)}${_mite(650, 520, 8, .82)}${_mite(780, 870, 20, .95)}` : ""}
      <path d="M380 470 A300 300 0 0 1 520 380" fill="none" stroke="#fff" stroke-width="18" stroke-linecap="round" opacity=".35"/>
    </g>
    <circle cx="600" cy="700" r="373" fill="none" stroke="${SC_INK}" stroke-width="50"/>
    <circle cx="600" cy="700" r="373" fill="none" stroke="#FFD84D" stroke-width="30"/>
    <rect x="390" y="205" width="420" height="78" rx="39" fill="#FFF8EC" stroke="${SC_INK}" stroke-width="7"/>
    <text x="600" y="258" text-anchor="middle" font-family="NST" font-weight="900" font-size="42" fill="${SC_INK}">ขยายหลายร้อยเท่า</text>`); };

const BG = {
  bedroom_night: () => _sv(`<rect width="1080" height="1920" fill="#2E3553"/>
    <rect y="1250" width="1080" height="670" fill="#3B3046"/><path d="M0 1250 H1080" stroke="${SC_INK}" stroke-width="8"/>
    <g stroke="${SC_INK}" stroke-width="8" stroke-linejoin="round">
      <rect x="640" y="430" width="320" height="400" rx="16" fill="#4F6FA8"/><path d="M800 430 V830 M640 630 H960" fill="none"/>
      <circle cx="880" cy="520" r="44" fill="#FFF3C4"/>
      <rect x="820" y="1080" width="130" height="210" rx="12" fill="#5A4A6A"/>
      <rect x="850" y="1040" width="70" height="44" rx="8" fill="#FFD84D"/></g>
    <circle cx="885" cy="1040" r="170" fill="#FFD84D" opacity=".10"/>${BED}`),
  bedroom_day: () => _sv(`<rect width="1080" height="1920" fill="#FFE9C9"/>
    <rect y="1250" width="1080" height="670" fill="#E8C9A0"/><path d="M0 1250 H1080" stroke="${SC_INK}" stroke-width="8"/>
    <g stroke="${SC_INK}" stroke-width="8" stroke-linejoin="round">
      <rect x="640" y="430" width="320" height="400" rx="16" fill="#9ED8FF"/><path d="M800 430 V830 M640 630 H960" fill="none"/>
      <circle cx="880" cy="520" r="50" fill="#FFD84D"/></g>${BED}`),
  dark: () => _sv(`<rect width="1080" height="1920" fill="#1B1E2E"/><circle cx="540" cy="900" r="560" fill="#2E3553"/>`),
  cream: () => _sv(`<rect width="1080" height="1920" fill="#FFF8EC"/><circle cx="540" cy="900" r="560" fill="#FFE9C9"/>`),
  street_night: () => _sv(`<rect width="1080" height="1920" fill="#232845"/>
    <g stroke="${SC_INK}" stroke-width="8" stroke-linejoin="round">
      <rect x="0" y="520" width="300" height="780" fill="#353B5E"/><rect x="300" y="380" width="260" height="920" fill="#2F3454"/>
      <rect x="560" y="600" width="240" height="700" fill="#3A3F63"/><rect x="800" y="440" width="280" height="860" fill="#30355A"/>
      <rect x="60" y="620" width="60" height="70" fill="#FFD84D"/><rect x="380" y="480" width="60" height="70" fill="#FFD84D"/>
      <rect x="880" y="560" width="60" height="70" fill="#FFD84D"/>
      <rect x="0" y="1300" width="1080" height="620" fill="#2A2438"/></g>`),
  pore_zoom: () => PORE_ZOOM(true), // แว่นขยายส่องผิวหน้า + ไรรูขุมขนน่ารัก 3 ตัว (โทนมืด) เว้นมุมล่างซ้ายให้ตัวละคร x40 y880 w380
  pore_zoom_empty: () => PORE_ZOOM(false), // ฉากเดียวกันแต่ส่องแล้ว "ไม่เห็น" ไร (รูขุมขนว่าง)
};

// ---------- ลิฟต์ (EP004 "ลิฟต์ค้าง" + ซีรีส์ "ถ้าคุณ… จะรอดไหม") ----------
// เรียกผ่าน BG ได้ทั้งแบบมีเลขชั้นท้ายชื่อ: "elevator_inside_7", "elevator_lit_B1" (ไม่ระบุ = "14")
// ไม่มีโลโก้/ชื่อยี่ห้อลิฟต์ใดๆ ทั้งหมดวาดจากโค้ด
// พื้นที่ว่าง (ใช้ร่วมกันทุกฉากลิฟต์):
//   - ตัวละคร: กลาง-ล่าง x 300–780, y 720–1440 (แนะนำ chars {x:310, y:760, w:460}) ยืนหน้าประตู/ใต้ช่องหลังคา
//   - ซับ: build.py วางที่ y 1440–1700 (ขวาเว้น 140) — ช่วงนี้เป็นพื้นลิฟต์สีเรียบ ไม่มีรายละเอียดรก
//   - การ์ด/ชิปนาฬิกา: y 230–530 จะบังจอเลขชั้น (y 500–600) ชั่วคราว — ช่องหลังคา (y 240–430) ยังเห็นบางส่วน
const _EL = {
  lit:  { wall: "#C9CED8", side: "#B3BAC6", seam: "#9AA2B0", ceil: "#E4E7ED", floor: "#9C8B78", tile: "#857563",
          door: "#D8DCE3", frame: "#A3AAB7", lamp: "#FFF6D0", hatch: "#C2C8D2", digit: "#FF8C69", panel: "#D9DDE4", btn: "#F4F5F8" },
  dark: { wall: "#353B52", side: "#2B3045", seam: "#454D69", ceil: "#202436", floor: "#272331", tile: "#1E1B27",
          door: "#3E4560", frame: "#2F3550", lamp: "#2E3347", hatch: "#2A2F44", digit: "#FFB347", panel: "#3A4058", btn: "#4A5170" },
};
function ELEVATOR_INSIDE(floor = "14", lit = false) {
  const c = lit ? _EL.lit : _EL.dark, I = SC_INK, f = String(floor);
  // ตะเข็บสแตนเลสบนผนังข้าง (เส้นตรงตามทัศนมิติ จุดลับตากลางจอ)
  const lseam = x => `M${x} ${2.4 * x} V${1920 - 1.8 * x}`, rseam = x => `M${1080 - x} ${2.4 * x} V${1920 - 1.8 * x}`;
  const btn = (x, y, rx, ry, on) => `<ellipse class="el-btn" cx="${x}" cy="${y}" rx="${rx}" ry="${ry}" fill="${on ? "#FFD84D" : c.btn}" stroke="${I}" stroke-width="5"/>`;
  let btns = ""; for (let r = 0; r < 4; r++) btns += btn(80, 830 + r * 62, 19, 23, !lit && false) + btn(138, 840 + r * 56, 15, 20, false);
  return _sv(`<rect width="1080" height="1920" fill="${c.wall}"/>
  <g stroke="${I}" stroke-width="8" stroke-linejoin="round">
    <path d="M0 0 H1080 L880 480 H200Z" fill="${c.ceil}"/>
    <path d="M0 0 L200 480 V1560 L0 1920Z" fill="${c.side}"/>
    <path d="M1080 0 L880 480 V1560 L1080 1920Z" fill="${c.side}"/>
    <rect x="200" y="480" width="680" height="1080" fill="${c.wall}"/>
    <path d="M200 1560 H880 L1080 1920 H0Z" fill="${c.floor}"/></g>
  <g fill="none" stroke="${c.seam}" stroke-width="6" stroke-linecap="round">
    <path d="${lseam(70)} ${lseam(150)} ${rseam(70)} ${rseam(150)}"/>
    <path d="M260 500 V1540 M820 500 V1540"/></g>
  <g fill="none" stroke="${c.tile}" stroke-width="6"><path d="M150 1650 H930 M70 1790 H1010 M540 1560 V1920 M370 1560 L270 1920 M710 1560 L810 1920"/></g>
  <!-- ไฟเพดานหลัก (ด้านหน้า) -->
  <path class="el-mainlight" d="M300 40 H780 L740 170 H340Z" fill="${c.lamp}" stroke="${I}" stroke-width="7" stroke-linejoin="round"/>
  ${lit ? "" : `<path d="M330 70 L380 150 M560 60 L600 150" stroke="${c.seam}" stroke-width="5" stroke-linecap="round"/>`}
  <!-- ช่องหลังคา (hatch) -->
  <g class="el-hatch" stroke="${I}" stroke-linejoin="round">
    <path d="M360 240 H720 L700 430 H380Z" fill="${lit ? "#AEB5C1" : "#151827"}" stroke-width="8"/>
    <path d="M378 254 H702 L686 416 H394Z" fill="${c.hatch}" stroke-width="6"/>
    <path d="M520 330 H560" stroke-width="12" stroke-linecap="round"/>
    <g fill="${I}" stroke="none"><circle cx="398" cy="270" r="7"/><circle cx="682" cy="270" r="7"/><circle cx="410" cy="400" r="6"/><circle cx="670" cy="400" r="6"/></g></g>
  <!-- กรอบประตู + บานประตูคู่ -->
  <g stroke="${I}" stroke-width="8" stroke-linejoin="round">
    <rect x="318" y="618" width="444" height="942" fill="${c.frame}"/>
    <rect x="340" y="640" width="200" height="920" fill="${c.door}"/><rect x="540" y="640" width="200" height="920" fill="${c.door}"/></g>
  <g fill="none" stroke="${c.seam}" stroke-width="5" stroke-linecap="round" opacity=".7"><path d="M380 690 V1500 M700 690 V1500"/></g>
  <!-- จอเลขชั้นเหนือประตู -->
  <g class="el-display">
    <rect x="430" y="500" width="220" height="100" rx="16" fill="#17181F" stroke="${I}" stroke-width="7"/>
    <path d="M462 560 L482 528 L502 560Z" fill="${c.digit}"/>
    <text class="el-floor" x="580" y="578" text-anchor="middle" font-family="NS,NST" font-weight="900" font-size="72" fill="${c.digit}">${f}</text></g>
  <!-- แผงปุ่มผนังซ้าย: ลำโพงอินเตอร์คอม, ปุ่มชั้น, ปุ่มกระดิ่งฉุกเฉิน -->
  <g class="el-panel">
    <path d="M40 690 L172 742 V1222 L40 1296Z" fill="${c.panel}" stroke="${I}" stroke-width="7" stroke-linejoin="round"/>
    <g class="el-intercom" stroke="${I}" stroke-width="5" stroke-linecap="round"><path d="M64 735 L150 768 M64 755 L150 786 M64 775 L150 804"/></g>
    ${btns}
    ${lit ? "" : `<circle cx="96" cy="1150" r="62" fill="#FFD84D" opacity=".22"/>`}
    <g class="el-bell"><ellipse cx="96" cy="1150" rx="38" ry="44" fill="#FFD84D" stroke="${I}" stroke-width="6"/>
      <path d="M78 1166 Q80 1124 96 1122 Q112 1124 114 1166Z M90 1170 Q96 1180 102 1170" fill="#FF8C69" stroke="${I}" stroke-width="4" stroke-linejoin="round"/></g>
    <g class="el-intercom-btn"><ellipse cx="96" cy="1240" rx="24" ry="22" fill="#7FD6C2" stroke="${I}" stroke-width="5"/>
      <path d="M88 1232 Q96 1226 104 1232 M86 1244 Q96 1252 106 1244" fill="none" stroke="${I}" stroke-width="4" stroke-linecap="round"/></g></g>
  <!-- ราวจับผนังขวา -->
  <path d="M1080 1210 L880 1130" stroke="${I}" stroke-width="22" stroke-linecap="round"/><path d="M1080 1210 L880 1130" stroke="${lit ? "#E8EBF0" : "#5A6280"}" stroke-width="10" stroke-linecap="round"/>
  ${lit ? "" : `<!-- ไฟฉุกเฉินสีเหลืองอ่อน (มุมเพดานขวา) + ลำแสงจางๆ -->
  <path d="M800 150 L560 1920 H1080 V420Z" fill="#FFE9A8" opacity=".09"/>
  <rect class="el-emlight" x="760" y="110" width="110" height="56" rx="14" fill="#FFE9A8" stroke="${I}" stroke-width="7"/>
  <circle cx="815" cy="138" r="70" fill="#FFE9A8" opacity=".16"/>`}`);
}

// ---------- แผนภาพปล่องลิฟต์ (โหมดอธิบาย พื้นครีม) ----------
// hl: "" | "cables" | "brake" | "sheave" | "cw"  ไฮไลต์เหลือง (ภาพนิ่ง)  labels: ป้ายชื่อภาษาไทย
// ทุกชิ้นมี class ให้ GSAP จับได้: el-car el-cable el-sheave el-cw el-rail el-brake el-buffer
// พื้นที่ว่าง: มุมล่างซ้าย x 20–400, y 980–1440 ให้ตัวละครยืนชี้ (แนะนำ chars {x:20, y:1000, w:380})
//   ซับ y 1440+ เป็นพื้นครีมโล่ง | ป้าย (labels) อยู่คอลัมน์ซ้าย x 50–330, y 300–960
function ELEVATOR_SHAFT(hl = "", labels = false) {
  const I = SC_INK, Y = "#FFD84D";
  const SX = 677, SY = 330, R = [112, 120, 128, 136, 144];       // รอก + รัศมีของสายแต่ละเส้น
  const CAR = { x: 400, y: 620, w: 300, h: 380 }, CW = { x: 760, y: 1080, w: 90, h: 330 };
  const cable = r => `M${SX - r} ${CAR.y} V${SY} A${r} ${r} 0 0 1 ${SX + r} ${SY} V${CW.y}`;
  const cables = R.map(cable).join(" ");
  const halo = (on, s) => on ? s : "";
  const brake = x => `<g class="el-brake"><path d="M${x - 26} ${CAR.y + CAR.h - 60} h52 v70 h-52Z" fill="#7FD6C2" stroke="${I}" stroke-width="6" stroke-linejoin="round"/>
      <path d="M${x - 14} ${CAR.y + CAR.h - 46} l8 20 l-8 20 M${x + 14} ${CAR.y + CAR.h - 46} l-8 20 l8 20" fill="none" stroke="${I}" stroke-width="6" stroke-linejoin="round"/></g>`;
  const lab = (x, y, t, tx, ty) => `<g class="el-label"><path d="M${x + 140} ${y} L${tx} ${ty}" stroke="${I}" stroke-width="5" stroke-dasharray="2 12" stroke-linecap="round"/>
      <circle cx="${tx}" cy="${ty}" r="9" fill="${I}"/>
      <rect x="${x - 120}" y="${y - 36}" width="260" height="72" rx="36" fill="#FFF8EC" stroke="${I}" stroke-width="6"/>
      <text x="${x + 10}" y="${y + 14}" text-anchor="middle" font-family="NST" font-weight="900" font-size="40" fill="${I}">${t}</text></g>`;
  return _sv(`<rect width="1080" height="1920" fill="#FFF8EC"/>
  <g stroke="${I}" stroke-width="8" stroke-linejoin="round">
    <rect x="330" y="160" width="620" height="320" rx="10" fill="#FFE9C9"/>
    <rect x="330" y="480" width="620" height="1240" fill="#F1E3CC"/>
    <rect x="310" y="470" width="660" height="34" rx="8" fill="#D9C4A2"/>
    <rect x="300" y="1720" width="680" height="40" rx="8" fill="#D9C4A2"/></g>
  <!-- ราง (car rails 385/715, cw rails 745/865) -->
  <g class="el-rail">${[385, 715, 745, 865].map(x => `<rect x="${x - 7}" y="504" width="14" height="1216" fill="#B8BDC9" stroke="${I}" stroke-width="5"/>`).join("")}</g>
  <!-- มอเตอร์ + รอก -->
  <rect x="380" y="270" width="150" height="120" rx="18" fill="#9ED8FF" stroke="${I}" stroke-width="7"/>
  <path d="M530 330 H${SX}" stroke="${I}" stroke-width="16" stroke-linecap="round"/>
  ${halo(hl === "sheave", `<circle cx="${SX}" cy="${SY}" r="182" fill="${Y}" opacity=".55"/>`)}
  <g class="el-sheave"><circle cx="${SX}" cy="${SY}" r="152" fill="#C9CED8" stroke="${I}" stroke-width="8"/>
    <circle cx="${SX}" cy="${SY}" r="96" fill="#E4E7ED" stroke="${I}" stroke-width="6"/>
    <path d="M${SX - 96} ${SY} H${SX + 96} M${SX} ${SY - 96} V${SY + 96}" stroke="${I}" stroke-width="6"/>
    <circle cx="${SX}" cy="${SY}" r="22" fill="${I}"/></g>
  <!-- สายเหล็ก 5 เส้น -->
  ${halo(hl === "cables", `<path d="${cables}" fill="none" stroke="${Y}" stroke-width="40" stroke-linejoin="round" opacity=".8"/>`)}
  <path d="${cables}" fill="none" stroke="${I}" stroke-width="10"/>
  ${R.map(r => `<path class="el-cable" d="${cable(r)}" fill="none" stroke="${hl === "cables" ? "#FF8C69" : "#8A90A0"}" stroke-width="4"/>`).join("")}
  <!-- ตัวลิฟต์ -->
  <g class="el-car" stroke="${I}" stroke-linejoin="round">
    <rect x="${CAR.x - 10}" y="${CAR.y - 24}" width="${CAR.w + 20}" height="34" rx="10" fill="#D9C4A2" stroke-width="7"/>
    <rect x="${CAR.x}" y="${CAR.y}" width="${CAR.w}" height="${CAR.h}" rx="18" fill="#FF8C69" stroke-width="8"/>
    <rect x="${CAR.x + 50}" y="${CAR.y + 60}" width="${CAR.w - 100}" height="${CAR.h - 90}" rx="10" fill="#FFE0C2" stroke-width="6"/>
    <path d="M${CAR.x + CAR.w / 2} ${CAR.y + 60} V${CAR.y + CAR.h - 30}" stroke-width="6"/></g>
  <!-- เบรกนิรภัย (ก้ามจับราง) ซ้าย-ขวาของตัวลิฟต์ -->
  ${halo(hl === "brake", `<g fill="${Y}" opacity=".6"><circle cx="385" cy="${CAR.y + CAR.h - 25}" r="72"/><circle cx="715" cy="${CAR.y + CAR.h - 25}" r="72"/></g>
    <g stroke="${I}" stroke-width="6" stroke-linecap="round">${[385, 715].map(x => `<path d="M${x - 70} ${CAR.y + CAR.h - 100} l-24 -22 M${x + 70} ${CAR.y + CAR.h - 100} l24 -22 M${x - 82} ${CAR.y + CAR.h + 30} l-28 12 M${x + 82} ${CAR.y + CAR.h + 30} l28 12"/>`).join("")}</g>`)}
  ${brake(385)}${brake(715)}
  <!-- ตุ้มถ่วงน้ำหนัก -->
  ${halo(hl === "cw", `<rect x="${CW.x - 26}" y="${CW.y - 26}" width="${CW.w + 52}" height="${CW.h + 52}" rx="30" fill="${Y}" opacity=".6"/>`)}
  <g class="el-cw" stroke="${I}" stroke-linejoin="round">
    <rect x="${CW.x}" y="${CW.y}" width="${CW.w}" height="${CW.h}" rx="12" fill="#7A86B8" stroke-width="8"/>
    <path d="${[1, 2, 3, 4, 5].map(i => `M${CW.x} ${CW.y + i * CW.h / 6} H${CW.x + CW.w}`).join(" ")}" stroke-width="5"/></g>
  <!-- กันชนก้นบ่อ -->
  <g class="el-buffer" stroke="${I}" stroke-width="6" stroke-linejoin="round">
    <rect x="510" y="1640" width="80" height="80" rx="8" fill="#FFD84D"/><path d="M510 1660 H590 M510 1680 H590 M510 1700 H590" fill="none"/>
    <rect x="775" y="1660" width="60" height="60" rx="8" fill="#FFD84D"/></g>
  ${labels ? lab(170, 300, "รอก", SX - 152, SY) + lab(170, 560, "สายเหล็ก", SX - 128, 560) + lab(170, 760, "ตัวลิฟต์", CAR.x, 760)
    + lab(170, 960, "เบรกนิรภัย", 360, CAR.y + CAR.h - 25) + `<g class="el-label"><rect x="520" y="1440" width="220" height="72" rx="36" fill="#FFF8EC" stroke="${I}" stroke-width="6"/>
      <text x="630" y="1490" text-anchor="middle" font-family="NST" font-weight="900" font-size="40" fill="${I}">ตุ้มถ่วง</text>
      <path d="M740 1476 L${CW.x + 20} ${CW.y + CW.h - 20}" stroke="${I}" stroke-width="5" stroke-dasharray="2 12" stroke-linecap="round"/></g>` : ""}`);
}

// ---------- แหงนมองช่องหลังคาที่ปิดอยู่ (มืด น่ากลัว) ----------
// knock: true = เส้นสะเทือนรอบฝาช่อง (ใช้ตอน "มีเสียงเคาะจากข้างบน") | "open" = ฝาเปิด แสงไฟฉายส่องลงมา
// พื้นที่ว่าง: ตัวละครล่างกลาง x 300–780, y 1080–1440 (หันหน้าแหงนขึ้น) | ซับ y 1440+ เป็นผนังมืดเรียบ
function ELEVATOR_HATCH_UP(knock = false) {
  const I = SC_INK;
  return _sv(`<rect width="1080" height="1920" fill="#14161F"/>
  <g stroke="${I}" stroke-width="8" stroke-linejoin="round">
    <path d="M0 0 H1080 L900 220 H180Z" fill="#232838"/>
    <path d="M0 0 L180 220 V960 L0 1920Z" fill="#1C2030"/>
    <path d="M1080 0 L900 220 V960 L1080 1920Z" fill="#1C2030"/>
    <path d="M180 960 H900 L1080 1920 H0Z" fill="#2A2F44"/>
    <rect x="180" y="220" width="720" height="740" fill="#202436"/></g>
  <g fill="none" stroke="#2F3550" stroke-width="6" stroke-linecap="round">
    <path d="M90 110 V1440 M990 110 V1440 M300 220 V960 M780 220 V960"/></g>
  <!-- ขอบบนประตู (ไม่มีจอเลขชั้น: หัวตัวละครจะบัง) -->
  <rect x="250" y="1120" width="580" height="40" rx="8" fill="#2F3550" stroke="${I}" stroke-width="7"/>
  <!-- ไฟเพดานดับ -->
  <rect x="250" y="270" width="140" height="300" rx="18" fill="#2E3347" stroke="${I}" stroke-width="7"/>
  <rect x="690" y="270" width="140" height="300" rx="18" fill="#2E3347" stroke="${I}" stroke-width="7"/>
  <!-- ไฟฉุกเฉิน -->
  <circle cx="760" cy="860" r="90" fill="#FFE9A8" opacity=".14"/>
  <rect x="705" y="835" width="110" height="50" rx="14" fill="#FFE9A8" stroke="${I}" stroke-width="7"/>
  ${knock === "open" ? `<!-- ช่องหลังคาเปิด: ฝาพับขึ้นไปทางขวา + ลำแสงไฟฉายส่องลง (ตัวละครที่ "โผล่" ให้วางใน x 390–690, y 400–700) -->
  <path d="M380 1920 L470 560 H610 L760 1920Z" fill="#FFF3C4" opacity=".13"/>
  <rect x="390" y="400" width="300" height="300" rx="12" fill="#07080D" stroke="${I}" stroke-width="10"/>
  <circle cx="540" cy="560" r="86" fill="#FFF3C4" opacity=".55"/><circle cx="540" cy="560" r="44" fill="#FFF8DC" stroke="${I}" stroke-width="6"/>
  <path d="M690 400 L770 330 L770 630 L690 700Z" fill="#2A2F44" stroke="${I}" stroke-width="7" stroke-linejoin="round"/>` : `<!-- ช่องหลังคา (ปิด) -->
  ${knock ? `<rect x="370" y="380" width="340" height="340" rx="20" fill="#FFE9A8" opacity=".08"/>` : ""}
  <g class="el-hatch" stroke="${I}" stroke-linejoin="round">
    <rect x="390" y="400" width="300" height="300" rx="12" fill="#07080D" stroke-width="10"/>
    <rect x="404" y="414" width="272" height="272" rx="8" fill="#2A2F44" stroke-width="6"/>
    <path d="M420 430 L660 670 M660 430 L420 670" stroke="#353B52" stroke-width="10" stroke-linecap="round"/>
    <path d="M510 550 H570" stroke-width="16" stroke-linecap="round"/><path d="M510 550 H570" stroke="#4A5170" stroke-width="6" stroke-linecap="round"/>
    <g fill="${I}" stroke="none"><circle cx="424" cy="434" r="9"/><circle cx="656" cy="434" r="9"/><circle cx="424" cy="666" r="9"/><circle cx="656" cy="666" r="9"/></g></g>`}
  ${knock === true ? `<g class="el-knock" stroke="#FFE9A8" stroke-width="10" stroke-linecap="round" fill="none">
    <path d="M370 470 l-50 -20 M366 550 l-60 0 M370 630 l-50 20 M710 470 l50 -20 M714 550 l60 0 M710 630 l50 20"/>
    <path d="M470 380 l-14 -46 M540 376 v-50 M610 380 l14 -46"/></g>
    <g fill="#8A90A0">${[[455, 760, 6], [520, 800, 4], [600, 770, 5], [640, 830, 3], [480, 850, 4]].map(([x, y, r]) => `<circle cx="${x}" cy="${y}" r="${r}"/>`).join("")}</g>` : ""}`);
}

Object.assign(BG, {
  elevator_inside: () => ELEVATOR_INSIDE("14", false), // ตีสอง ไฟดับ เหลือไฟฉุกเฉิน
  elevator_lit: () => ELEVATOR_INSIDE("14", true),     // ห้องเดียวกัน ไฟสว่าง
  elevator_shaft: () => ELEVATOR_SHAFT(),
  elevator_shaft_labels: () => ELEVATOR_SHAFT("", true),
  elevator_shaft_cables: () => ELEVATOR_SHAFT("cables"),
  elevator_shaft_brake: () => ELEVATOR_SHAFT("brake"),
  elevator_shaft_sheave: () => ELEVATOR_SHAFT("sheave"),
  elevator_shaft_cw: () => ELEVATOR_SHAFT("cw"),
  elevator_hatch_up: () => ELEVATOR_HATCH_UP(false),
  elevator_hatch_up_knock: () => ELEVATOR_HATCH_UP(true),
  elevator_hatch_up_open: () => ELEVATOR_HATCH_UP("open"),
});
// เลขชั้นท้ายชื่อ: elevator_inside_<ชั้น>, elevator_lit_<ชั้น> (ฉาก hatch_up ไม่มีจอเลขชั้น)
// (build.py เรียก BG[ชื่อ]() ตรงๆ จึงลงทะเบียนชื่อไว้ล่วงหน้า: ชั้น 1–60, G, B1–B3, M)
for (const n of [...Array.from({ length: 60 }, (_, i) => String(i + 1)), "G", "B1", "B2", "B3", "M"]) {
  BG[`elevator_inside_${n}`] = () => ELEVATOR_INSIDE(n, false);
  BG[`elevator_lit_${n}`] = () => ELEVATOR_INSIDE(n, true);
}

// ---------- ท่าดันแว่นแบบทีละเวลา (ย้ายมาจาก character/outro-push-glasses.html) ----------
const _clamp = x => Math.max(0, Math.min(1, x));
const _seg = (t, a, b) => _clamp((t - a) / (b - a));
const _io = x => x < .5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2;
const _back = x => { const c1 = 1.9, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); };
function pushGlassesPose(t) { // t วินาทีนับจากเริ่มท่า (0..~3.8)
  const raise = _io(_seg(t, .5, 1.15)), lower = _io(_seg(t, 3.35, 3.8)), push = raise * (1 - lower);
  const pushUp = _back(_seg(t, 1.15, 1.35)), slip = _io(_seg(t, 3.4, 4.0));
  let gdy = 9 - 14 * pushUp * (t < 3.4 ? 1 : 0) + (t >= 3.4 ? -5 + 14 * slip : 0); if (t < 1.15) gdy = 9;
  const gp = _seg(t, 1.3, 1.5);
  const glint = t < 1.3 ? 0 : t < 3.4 ? (gp < 1 ? _back(gp) * 1.1 : 1 + .12 * Math.sin((t - 1.5) * 9)) : 1 - _seg(t, 3.4, 3.6);
  const cool = t >= 1.45 && t < 3.65;
  return { gl: (t > 1.3 && t < 1.5) ? "glare" : "norm", eye: cool ? "cool" : "norm", brow: cool ? "cool" : "norm",
           mo: cool ? "smirk" : "smile", arm: push > .02 ? "left" : "down", push: push > .02 ? push : 0, gdy, glint,
           tilt: cool ? -4 * _io(_seg(t, 1.45, 1.7)) : 0 };
}
