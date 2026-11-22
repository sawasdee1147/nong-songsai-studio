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
