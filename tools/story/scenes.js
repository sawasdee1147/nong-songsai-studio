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
const PORE_ZOOM = () => { const id = `pzLens${++_pzN}`; return _sv(`<rect width="1080" height="1920" fill="#2E2A47"/>
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
      ${_mite(440, 660, -16, 1.05)}${_mite(650, 520, 8, .82)}${_mite(780, 870, 20, .95)}
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
  pore_zoom: PORE_ZOOM, // แว่นขยายส่องผิวหน้า + ไรรูขุมขนน่ารัก 3 ตัว (โทนมืด) เว้นมุมล่างซ้ายให้ตัวละคร x40 y880 w380
};

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
