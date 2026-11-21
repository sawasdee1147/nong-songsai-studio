/* art.js — ภาพประกอบ SVG ของช่อง "น้องสงสัย" (วาดด้วยโค้ด ลายเส้นตาม show bible)
   ขอบเข้ม #2B2B2B หนา มุมมน สีเรียบ ไม่มีไล่เฉด
   ทุกฟังก์ชันคืนสตริง SVG ในพิกัดท้องถิ่น (จุดศูนย์กลาง 0,0) */
(function () {
  const K = "#2B2B2B", Y = "#FFD84D", O = "#FF8C69", OD = "#E0704F", P = "#FF9AA2",
    SK = "#FFE0C2", B = "#9ED8FF", M = "#7FD6C2", RED = "#F05A50", W = "#FFFFFF";
  const ART = { K, Y, O, OD, P, SK, B, M, RED, W };

  /* ---------- พริก ---------- */
  ART.chiliBody = () => `
    <path d="M -70 -150 C -102 -50 -86 70 -26 150 C 0 190 46 210 82 196 C 46 176 32 140 42 90 C 62 0 90 -80 72 -150 Q 0 -185 -70 -150 Z" fill="${RED}" stroke="${K}" stroke-width="8" stroke-linejoin="round"/>
    <path d="M -48 -118 C -64 -60 -58 10 -38 58" fill="none" stroke="${W}" stroke-width="10" stroke-linecap="round" opacity=".45"/>
    <path d="M 4 -176 Q 4 -235 54 -256" fill="none" stroke="${K}" stroke-width="24" stroke-linecap="round"/>
    <path d="M 4 -176 Q 4 -235 54 -256" fill="none" stroke="${M}" stroke-width="12" stroke-linecap="round"/>
    <path d="M -68 -150 Q -40 -196 0 -180 Q 40 -196 72 -150 Q 36 -162 0 -146 Q -36 -162 -68 -150 Z" fill="${M}" stroke="${K}" stroke-width="7" stroke-linejoin="round"/>`;

  // หน้าพริก (ตาที่ y -78, ปากที่ y -30)
  ART.chiliFace = (f) => {
    const lid = (x) => `<path d="M ${x - 15} -80 Q ${x} -62 ${x + 15} -80 Z" fill="${K}"/><path d="M ${x - 17} -80 L ${x + 17} -81" stroke="${K}" stroke-width="7" stroke-linecap="round"/><circle cx="${x + 5}" cy="-74" r="3" fill="${W}"/>`;
    const dot = (x) => `<ellipse cx="${x}" cy="-78" rx="10" ry="13" fill="${K}"/><circle cx="${x + 4}" cy="-83" r="4" fill="${W}"/>`;
    const happy = (x) => `<path d="M ${x - 14} -74 Q ${x} -92 ${x + 14} -74" fill="none" stroke="${K}" stroke-width="7" stroke-linecap="round"/>`;
    const brow = (d) => `<path d="${d}" fill="none" stroke="${K}" stroke-width="6" stroke-linecap="round"/>`;
    const smirk = `<path d="M -30 -28 Q 0 -10 28 -40" fill="none" stroke="${K}" stroke-width="7" stroke-linecap="round"/>`;
    if (f === "smug") return lid(-32) + lid(28) + brow("M -48 -104 L -18 -100") + brow("M 12 -104 Q 28 -116 44 -106") + smirk;
    if (f === "wink") return dot(-32) + `<path d="M 16 -86 L 40 -78 L 16 -70" fill="none" stroke="${K}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>` + brow("M 12 -104 Q 28 -116 44 -106") +
      `<path d="M -30 -36 Q 0 -6 26 -40 Z" fill="${K}" stroke="${K}" stroke-width="5" stroke-linejoin="round"/>`;
    if (f === "hot") return `<circle cx="-32" cy="-78" r="15" fill="${W}" stroke="${K}" stroke-width="5"/><circle cx="28" cy="-78" r="15" fill="${W}" stroke="${K}" stroke-width="5"/><circle cx="-32" cy="-78" r="5" fill="${K}"/><circle cx="28" cy="-78" r="5" fill="${K}"/>` +
      `<ellipse cx="-2" cy="-26" rx="16" ry="20" fill="${K}"/>`;
    if (f === "laugh") return happy(-32) + happy(28) + `<path d="M -30 -40 Q 0 0 28 -42 Z" fill="${K}" stroke="${K}" stroke-width="5" stroke-linejoin="round"/><path d="M -12 -24 Q 0 -14 12 -26" fill="#FF7B8A"/>`;
    return dot(-32) + dot(28) + smirk;
  };
  ART.chiliArmsShrug = () => {
    const a = (d) => `<path d="${d}" fill="none" stroke="${K}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/><path d="${d}" fill="none" stroke="${RED}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>`;
    return a("M -78 -10 L -122 -30 L -136 -72") + a("M 70 -10 L 116 -30 L 130 -72");
  };

  /* ---------- หน้ากากไฟ ---------- */
  ART.flameMask = () => `
    <path d="M -126 6 C -150 -80 -120 -150 -86 -196 C -80 -156 -66 -146 -54 -156 C -56 -214 -24 -256 10 -290 C 14 -238 40 -214 56 -204 C 72 -236 92 -248 110 -258 C 104 -204 146 -132 132 -62 C 126 -22 116 0 104 12 Q 0 34 -126 6 Z" fill="${O}" stroke="${K}" stroke-width="8" stroke-linejoin="round"/>
    <path d="M -86 0 C -102 -60 -80 -110 -56 -136 C -50 -110 -36 -104 -26 -112 C -28 -158 -6 -188 16 -214 C 20 -176 38 -160 52 -152 C 62 -174 74 -182 86 -190 C 84 -150 110 -98 96 -46 C 92 -20 84 -6 76 2 Q 0 18 -86 0 Z" fill="${Y}" stroke="${K}" stroke-width="5" stroke-linejoin="round"/>
    <path d="M -56 -92 L -10 -78 L -16 -60 Q -40 -54 -58 -70 Z" fill="${K}"/>
    <path d="M 52 -94 L 8 -78 L 14 -60 Q 38 -54 56 -72 Z" fill="${K}"/>
    <circle cx="-24" cy="-70" r="5" fill="${W}"/><circle cx="22" cy="-70" r="5" fill="${W}"/>
    <path d="M -126 -40 L -160 -48 M 130 -40 L 164 -50" stroke="${K}" stroke-width="7" stroke-linecap="round"/>`;

  /* ---------- เปลวไฟ ---------- */
  ART.flame = () => `
    <path d="M 0 -160 C 54 -96 96 -54 90 22 C 86 86 44 116 0 116 C -44 116 -88 86 -90 22 C -92 -30 -54 -52 -42 -104 C -22 -74 -10 -64 0 -160 Z" fill="${O}" stroke="${K}" stroke-width="8" stroke-linejoin="round"/>
    <path d="M 0 -70 C 30 -36 52 -10 48 36 C 46 70 24 86 0 86 C -24 86 -48 70 -48 36 C -48 6 -28 -6 -20 -36 C -10 -20 -4 -14 0 -70 Z" fill="${Y}" stroke="${K}" stroke-width="5" stroke-linejoin="round"/>`;

  /* ---------- โมเลกุลแคปไซซิน (หัวกลม หางยาว หน้ากวน) ---------- */
  ART.molecule = () => {
    const tail = "M 28 18 L 62 4 L 94 28 L 126 10 L 158 34 L 190 16 L 214 40";
    return `
    <path d="${tail}" fill="none" stroke="${K}" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="${tail}" fill="none" stroke="${OD}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="94" cy="28" r="9" fill="${Y}" stroke="${K}" stroke-width="4"/>
    <circle cx="158" cy="34" r="9" fill="${Y}" stroke="${K}" stroke-width="4"/>
    <circle cx="0" cy="0" r="40" fill="${Y}" stroke="${K}" stroke-width="7"/>
    <path d="M -24 -6 Q -14 6 -4 -6 Z" fill="${K}"/><path d="M -26 -6 L -2 -7" stroke="${K}" stroke-width="5" stroke-linecap="round"/>
    <path d="M 6 -6 Q 16 6 26 -6 Z" fill="${K}"/><path d="M 4 -7 L 28 -6" stroke="${K}" stroke-width="5" stroke-linecap="round"/>
    <path d="M -24 -20 L -6 -18 M 8 -20 Q 18 -27 28 -20" fill="none" stroke="${K}" stroke-width="4" stroke-linecap="round"/>
    <path d="M -14 14 Q 2 24 18 8" fill="none" stroke="${K}" stroke-width="5" stroke-linecap="round"/>
    <ellipse cx="-26" cy="10" rx="7" ry="4" fill="${P}"/>`;
  };

  /* ---------- สมองการ์ตูน ---------- */
  ART.brainShape = () => `
    <path d="M -172 22 C -204 -60 -142 -132 -80 -120 C -60 -172 22 -178 52 -130 C 112 -162 184 -110 168 -40 C 212 0 184 92 122 96 C 102 142 20 142 -10 112 C -60 142 -152 122 -152 72 C -182 62 -186 42 -172 22 Z" fill="${P}" stroke="${K}" stroke-width="8" stroke-linejoin="round"/>
    <path d="M -96 -66 Q -66 -96 -34 -68 M 22 -96 Q 54 -66 96 -86 M -134 14 Q -104 -6 -76 22 M 84 40 Q 118 18 140 54 M 4 -124 Q -12 -90 6 -60" fill="none" stroke="${K}" stroke-width="5" stroke-linecap="round" opacity=".55"/>`;
  ART.brainFace = (f) => {
    const dot = (x) => `<ellipse cx="${x}" cy="10" rx="10" ry="13" fill="${K}"/><circle cx="${x + 4}" cy="5" r="4" fill="${W}"/>`;
    if (f === "panic") return `<circle cx="-40" cy="10" r="20" fill="${W}" stroke="${K}" stroke-width="5"/><circle cx="40" cy="10" r="20" fill="${W}" stroke="${K}" stroke-width="5"/><circle cx="-40" cy="10" r="6" fill="${K}"/><circle cx="40" cy="10" r="6" fill="${K}"/>
      <path d="M -62 -22 L -22 -16 M 62 -22 L 22 -16" stroke="${K}" stroke-width="6" stroke-linecap="round"/>
      <path d="M -26 58 q 9 -12 18 0 t 18 0 t 18 0" fill="none" stroke="${K}" stroke-width="6" stroke-linecap="round"/>`;
    if (f === "q") return dot(-38) + dot(38) + `<ellipse cx="0" cy="54" rx="9" ry="10" fill="${K}"/>`;
    return dot(-38) + dot(38) + `<path d="M -22 46 Q 0 62 22 46" fill="none" stroke="${K}" stroke-width="6" stroke-linecap="round"/>`;
  };
  ART.brainArmsUp = () => {
    const a = (d) => `<path d="${d}" fill="none" stroke="${K}" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/><path d="${d}" fill="none" stroke="${P}" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>`;
    return a("M -120 40 L -170 -40 L -150 -140") + a("M 120 40 L 170 -40 L 150 -140");
  };

  /* ---------- ประตู TRPV1 บนปลายประสาท (ประตูแยกชิ้นเพื่อเปิด/ปิด) ---------- */
  ART.gate = (id, sign = true) => `
    <g id="${id}-dl"><rect x="-50" y="-92" width="52" height="184" rx="10" fill="${B}" stroke="${K}" stroke-width="7"/><path d="M -36 -60 L -36 60" stroke="${K}" stroke-width="5" stroke-linecap="round" opacity=".5"/></g>
    <g id="${id}-dr"><rect x="-2" y="-92" width="52" height="184" rx="10" fill="${B}" stroke="${K}" stroke-width="7"/><path d="M 36 -60 L 36 60" stroke="${K}" stroke-width="5" stroke-linecap="round" opacity=".5"/></g>
    <rect x="-108" y="-112" width="62" height="224" rx="22" fill="${M}" stroke="${K}" stroke-width="7"/>
    <rect x="46" y="-112" width="62" height="224" rx="22" fill="${M}" stroke="${K}" stroke-width="7"/>
    <circle cx="-77" cy="-20" r="13" fill="${K}"/><path d="M -77 -20 L -77 8" stroke="${K}" stroke-width="10" stroke-linecap="round"/>
    ${sign ? `<rect x="-96" y="-182" width="192" height="64" rx="18" fill="${Y}" stroke="${K}" stroke-width="7"/>
    <text x="0" y="-136" text-anchor="middle" font-family="Noto Sans Thai, sans-serif" font-weight="900" font-size="42" fill="${K}">TRPV1</text>` : ""}`;

  // ปลายประสาท: ผนังเยื่อหุ้มแนวนอน (ด้านบน = ข้างนอก) ตัวประสาทสีชมพูด้านล่าง
  ART.nerveBody = (w, h) => `
    <path d="M ${-w / 2} 20 Q ${-w / 2} -20 ${-w / 2 + 50} -20 L ${w / 2 - 50} -20 Q ${w / 2} -20 ${w / 2} 20 L ${w / 2} ${h - 80} Q ${w / 2} ${h} ${w / 2 - 110} ${h + 20} Q 70 ${h + 40} 70 ${h + 140} L 70 ${h + 700} L -70 ${h + 700} L -70 ${h + 140} Q -70 ${h + 40} ${-w / 2 + 110} ${h + 20} Q ${-w / 2} ${h} ${-w / 2} ${h - 80} Z" fill="${P}" stroke="${K}" stroke-width="8" stroke-linejoin="round"/>
    <path d="M ${-w / 2 + 30} 10 L ${w / 2 - 30} 10" stroke="${OD}" stroke-width="10" stroke-linecap="round" stroke-dasharray="2 26"/>`;

  /* ---------- เทอร์โมมิเตอร์ ---------- */
  ART.thermo = (id) => `
    <rect x="-34" y="-270" width="68" height="440" rx="34" fill="${W}" stroke="${K}" stroke-width="8"/>
    <g id="${id}-merc"><rect x="-15" y="-240" width="30" height="420" rx="15" fill="${RED}"/></g>
    <circle cx="0" cy="200" r="58" fill="${RED}" stroke="${K}" stroke-width="8"/>
    <circle cx="-18" cy="184" r="12" fill="${W}" opacity=".6"/>
    <path d="M 34 -200 L 58 -200 M 34 -140 L 50 -140 M 34 -80 L 58 -80 M 34 -20 L 50 -20 M 34 40 L 58 40 M 34 100 L 50 100" stroke="${K}" stroke-width="6" stroke-linecap="round"/>`;

  /* ---------- ไอคอนคน + ฟองความคิด ---------- */
  ART.person = () => `
    <path d="M -110 200 Q -110 60 0 60 Q 110 60 110 200 Z" fill="${M}" stroke="${K}" stroke-width="8" stroke-linejoin="round"/>
    <circle cx="0" cy="-10" r="70" fill="${SK}" stroke="${K}" stroke-width="8"/>
    <circle cx="-24" cy="-16" r="8" fill="${K}"/><circle cx="24" cy="-16" r="8" fill="${K}"/>
    <path d="M -16 20 Q 0 30 16 20" fill="none" stroke="${K}" stroke-width="6" stroke-linecap="round"/>`;
  ART.bubble = (rx, ry) => `
    <ellipse cx="0" cy="0" rx="${rx}" ry="${ry}" fill="${W}" stroke="${K}" stroke-width="8"/>`;

  /* ---------- กากบาทแดง ---------- */
  ART.cross = (s = 120) => `
    <path d="M ${-s} ${-s} L ${s} ${s} M ${s} ${-s} L ${-s} ${s}" stroke="${K}" stroke-width="44" stroke-linecap="round"/>
    <path d="M ${-s} ${-s} L ${s} ${s} M ${s} ${-s} L ${-s} ${s}" stroke="${RED}" stroke-width="26" stroke-linecap="round"/>`;

  /* ---------- ลิ้น ---------- */
  ART.tongue = () => `
    <path d="M -180 -130 L 180 -130 L 180 30 C 180 160 96 210 0 210 C -96 210 -180 160 -180 30 Z" fill="${P}" stroke="${K}" stroke-width="8" stroke-linejoin="round"/>
    <path d="M 0 -110 L 0 120" stroke="${K}" stroke-width="6" stroke-linecap="round" opacity=".45"/>
    <path d="M -200 -130 L 200 -130" stroke="${K}" stroke-width="10" stroke-linecap="round"/>
    <circle cx="-90" cy="-40" r="7" fill="${W}" opacity=".7"/><circle cx="-60" cy="40" r="6" fill="${W}" opacity=".7"/><circle cx="80" cy="-20" r="7" fill="${W}" opacity=".7"/><circle cx="96" cy="70" r="6" fill="${W}" opacity=".7"/>`;

  /* ---------- ไฟเตือนบนหัว ---------- */
  ART.beacon = (id) => `
    <rect x="-60" y="-10" width="120" height="30" rx="10" fill="${K}"/>
    <path id="${id}-lamp" d="M -46 -10 L -46 -60 Q 0 -110 46 -60 L 46 -10 Z" fill="${RED}" stroke="${K}" stroke-width="7" stroke-linejoin="round"/>
    <g id="${id}-rays"><path d="M -80 -70 L -110 -90 M 80 -70 L 110 -90 M 0 -110 L 0 -146 M -56 -110 L -74 -136 M 56 -110 L 74 -136" stroke="${RED}" stroke-width="10" stroke-linecap="round"/></g>`;

  /* ---------- เหรียญ (วาดเองแบบเรียบ ไม่เลียนแบบเหรียญจริง) ---------- */
  ART.medal = () => `
    <path d="M -70 -300 L -30 -130 M 70 -300 L 30 -130" stroke="${K}" stroke-width="40" stroke-linecap="round"/>
    <path d="M -70 -300 L -30 -130" stroke="${B}" stroke-width="24" stroke-linecap="round"/>
    <path d="M 70 -300 L 30 -130" stroke="${O}" stroke-width="24" stroke-linecap="round"/>
    <circle cx="0" cy="0" r="150" fill="${Y}" stroke="${K}" stroke-width="9"/>
    <circle cx="0" cy="0" r="118" fill="none" stroke="${K}" stroke-width="5" stroke-dasharray="4 14" stroke-linecap="round"/>
    <path d="M -50 -68 L -38 -92 L -26 -68 L -52 -84 L -24 -84 Z M 26 -68 L 38 -92 L 50 -68 L 24 -84 L 52 -84 Z" fill="${W}" stroke="${K}" stroke-width="3" stroke-linejoin="round"/>`;

  ART.sparkle = (s = 1) => `<path transform="scale(${s})" d="M0 -30 L7 -7 L30 0 L7 7 L0 30 L-7 7 L-30 0 L-7 -7Z" fill="${W}" stroke="${K}" stroke-width="4" stroke-linejoin="round"/>`;

  window.ART = ART;
})();
