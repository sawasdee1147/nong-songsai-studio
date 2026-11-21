
function pushArm(p){
  const lerp=(a,b)=>a+(b-a)*p;
  const s=[194,248], c=[lerp(210,226),lerp(280,214)], e=[lerp(204,154),lerp(302,182)];
  const d=`M${s[0]} ${s[1]} Q${c[0]} ${c[1]} ${e[0]} ${e[1]}`;
  let o=`<path d="${d}" fill="none" stroke="${INK}" stroke-width="22" stroke-linecap="round"/><path d="${d}" fill="none" stroke="${HOOD}" stroke-width="13" stroke-linecap="round"/>`;
  const fp=Math.max(0,(p-0.5)/0.5); // finger extends late
  if(fp>0){const fx=e[0]-3, fy=e[1]-6, tx=fx-2, ty=fy-30*fp;
    o+=`<path d="M${fx} ${fy} L${tx} ${ty}" stroke="${INK}" stroke-width="13" stroke-linecap="round"/><path d="M${fx} ${fy} L${tx} ${ty}" stroke="${SKIN}" stroke-width="5.5" stroke-linecap="round"/>`;}
  o+=`<ellipse cx="${e[0]}" cy="${e[1]}" rx="12" ry="11" fill="${SKIN}" stroke="${INK}" stroke-width="4.5"/>`;
  return o;
}

const INK="#2B2B2B", SKIN="#FFE0C2", HAIR="#2B2B2B", HOOD="#FF8C69", HOODD="#E0704F", CHEEK="#FF9AA2", YEL="#FFD84D";
const EY=152, L=118, R=182;
function star(x,y){let p="";for(let i=0;i<10;i++){const a=Math.PI/5*i-Math.PI/2,r=i%2?9:22;p+=`${x+r*Math.cos(a)},${y+r*Math.sin(a)} `}return `<polygon points="${p}" fill="${YEL}" stroke="${INK}" stroke-width="4" stroke-linejoin="round"/>`}
function eyes(t){
  const dot=(x,dx=0,dy=0)=>`<ellipse cx="${x+dx}" cy="${EY+dy}" rx="11" ry="14" fill="${INK}"/><circle cx="${x+dx+4}" cy="${EY+dy-5}" r="4" fill="#fff"/>`;
  const arc=(x,up=true)=>`<path d="M${x-14} ${EY+(up?4:-2)} Q${x} ${EY+(up?-12:10)} ${x+14} ${EY+(up?4:-2)}" fill="none" stroke="${INK}" stroke-width="6" stroke-linecap="round"/>`;
  switch(t){
    case "up": return dot(L,3,-5)+dot(R,3,-5);
    case "smug": return `<path d="M104 152 L132 152" stroke="${INK}" stroke-width="6" stroke-linecap="round"/>`+`<path d="M168 154 Q182 146 196 154" fill="none" stroke="${INK}" stroke-width="6" stroke-linecap="round"/>`;
    case "shock": return `<circle cx="${L}" cy="${EY}" r="17" fill="#fff" stroke="${INK}" stroke-width="5"/><circle cx="${R}" cy="${EY}" r="17" fill="#fff" stroke="${INK}" stroke-width="5"/><circle cx="${L}" cy="${EY}" r="5" fill="${INK}"/><circle cx="${R}" cy="${EY}" r="5" fill="${INK}"/>`;
    case "spark": return star(L,EY)+star(R,EY);
    case "laugh": return arc(L)+arc(R);
    case "side": return `<path d="M104 136 L132 136 M168 136 L196 136" stroke="${INK}" stroke-width="5" stroke-linecap="round"/>`+dot(L,-6,-8).replace(/ry="14"/g,'ry="8"')+dot(R,-6,-8).replace(/ry="14"/g,'ry="8"');
    case "wink": return dot(L)+`<path d="M168 148 L194 154 L168 160" fill="none" stroke="${INK}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>`;
    case "cool": return [L,R].map(x=>`<path d="M${x-13} ${EY} Q${x} ${EY+20} ${x+13} ${EY}Z" fill="${INK}"/><circle cx="${x+5}" cy="${EY+5}" r="3" fill="#fff"/><path d="M${x-15} ${EY} L${x+15} ${EY-1}" stroke="${INK}" stroke-width="6" stroke-linecap="round"/>`).join("");
    case "sad": return dot(L,0,3)+dot(R,0,3);
    case "blink": return arc(L,false)+arc(R,false); // ตาปิด (กะพริบ) วาดใต้ชั้นแว่นตามลำดับเดิม
    default: return dot(L)+dot(R);
  }
}

function glasses(t,dy=0,glint=0){
  if(t==="none") return "";
  if(dy||glint){const inner=glasses(t);const gl=glint?`<g transform="translate(${R+12} ${EY-14}) scale(${glint})"><path d="M0 -22 L5 -5 L22 0 L5 5 L0 22 L-5 5 L-22 0 L-5 -5Z" fill="#fff" stroke="${INK}" stroke-width="3"/></g>`:"";return `<g transform="translate(0 ${dy})">${inner}</g>`+gl;}
  const lens=(x)=>{
    const fill = t==="glare" ? `fill="#fff" fill-opacity=".97"` : `fill="#BDE6FF" fill-opacity=".18"`;
    let shine = t==="glare"
      ? `<path d="M${x-14} ${EY+6} L${x+4} ${EY-14} M${x-4} ${EY+12} L${x+14} ${EY-6}" stroke="#9ED8FF" stroke-width="5" stroke-linecap="round"/>`
      : `<path d="M${x-14} ${EY-6} Q${x-10} ${EY-14} ${x-2} ${EY-16}" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" opacity=".9"/>`;
    return `<circle cx="${x}" cy="${EY}" r="25" ${fill} stroke="${INK}" stroke-width="6.5"/>`+shine;
  };
  const g=`${lens(L)}${lens(R)}
    <path d="M143 ${EY-3} Q150 ${EY-9} 157 ${EY-3}" fill="none" stroke="${INK}" stroke-width="6" stroke-linecap="round"/>
    <path d="M93 ${EY-4} L64 ${EY+2} M207 ${EY-4} L236 ${EY+2}" stroke="${INK}" stroke-width="5" stroke-linecap="round"/>`;
  if(t==="askew") return `<g transform="rotate(-12 150 ${EY}) translate(0 6)">${g}</g>`;
  if(t==="down") return `<g transform="translate(150 182) scale(.78) translate(-150 -152)">${g}</g>`;
  return g;
}
function brows(t){
  const b=d=>`<path d="${d}" fill="none" stroke="${INK}" stroke-width="5" stroke-linecap="round"/>`;
  switch(t){
    case "smug": return b("M104 126 L130 130")+b("M168 122 Q182 112 198 120");
    case "up": return b("M104 124 Q117 118 130 124")+b("M170 124 Q183 118 196 124");
    case "shock": return b("M102 120 Q117 112 132 120")+b("M168 120 Q183 112 198 120");
    case "worry": return b("M104 128 L130 122")+b("M170 122 L196 128");
    case "cool": return b("M104 132 L130 131")+b("M168 126 Q183 118 198 126");
    case "none": return "";
    default: return b("M104 128 L130 126")+b("M170 124 L196 130");
  }
}
function mouth(t){
  switch(t){
    case "o": return `<ellipse cx="150" cy="192" rx="7" ry="8" fill="${INK}"/>`;
    case "smirk": return `<path d="M136 190 Q156 200 168 184" fill="none" stroke="${INK}" stroke-width="5" stroke-linecap="round"/>`;
    case "shock": return `<ellipse cx="150" cy="196" rx="13" ry="16" fill="${INK}"/><ellipse cx="150" cy="205" rx="7" ry="5" fill="#FF7B8A"/>`;
    case "grin": return `<path d="M128 184 Q150 220 172 184 Z" fill="${INK}" stroke="${INK}" stroke-width="4" stroke-linejoin="round"/><path d="M139 201 Q150 210 161 201" fill="#FF7B8A"/>`;
    case "tongue": return `<path d="M134 188 Q150 198 166 188" fill="none" stroke="${INK}" stroke-width="5" stroke-linecap="round"/><path d="M146 192 Q147 210 156 209 Q164 206 161 191" fill="#FF7B8A" stroke="${INK}" stroke-width="4"/>`;
    case "flatlow": return `<path d="M142 212 L160 210" stroke="${INK}" stroke-width="5" stroke-linecap="round"/>`;
    case "flat": return `<path d="M140 192 L162 190" stroke="${INK}" stroke-width="5" stroke-linecap="round"/>`;
    case "wobble": return `<path d="M136 194 q5 -6 10 0 t10 0 t10 0" fill="none" stroke="${INK}" stroke-width="5" stroke-linecap="round"/>`;
    default: return `<path d="M138 188 Q150 198 162 188" fill="none" stroke="${INK}" stroke-width="5" stroke-linecap="round"/>`;
  }
}
function ahoge(t){
  const p=d=>`<path d="${d}" fill="none" stroke="${HAIR}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>`;
  if(t==="!") return p("M150 48 L150 2")+`<circle cx="150" cy="-14" r="7" fill="${YEL}" stroke="${INK}" stroke-width="4"/>`;
  if(t==="zig") return p("M150 48 L138 30 L160 18 L142 0 L164 -14");
  if(t==="droop") return p("M150 48 C150 30 120 22 104 38 C96 46 102 58 112 56");
  if(t==="heart") return p("M150 48 L150 30")+`<path d="M150 28 C130 10 132 -8 150 2 C168 -8 170 10 150 28Z" fill="#FF7B8A" stroke="${INK}" stroke-width="4"/>`;
  return p("M128 18 C126 -12 178 -14 178 14 C178 34 152 32 152 48");
}
function arms(t){
  const sleeve=d=>`<path d="${d}" fill="none" stroke="${INK}" stroke-width="22" stroke-linecap="round"/><path d="${d}" fill="none" stroke="${HOOD}" stroke-width="13" stroke-linecap="round"/>`;
  const hand=(x,y)=>`<circle cx="${x}" cy="${y}" r="11" fill="${SKIN}" stroke="${INK}" stroke-width="4.5"/>`;
  const Ls=[106,248], Rs=[194,248];
  const arm=(s,c,e)=>sleeve(`M${s[0]} ${s[1]} Q${c[0]} ${c[1]} ${e[0]} ${e[1]}`)+hand(e[0],e[1]+ (e[1]>s[1]?6:-6));
  switch(t){
    case "chin": return arm(Ls,[86,280],[96,300])+arm(Rs,[230,250],[176,212]);
    case "up": return arm(Ls,[70,220],[66,180])+arm(Rs,[230,220],[234,180]);
    case "point": return arm(Ls,[86,280],[96,300])+arm(Rs,[236,240],[258,210]);
    case "belly": return arm(Ls,[100,290],[132,282])+arm(Rs,[200,290],[168,282]);
    case "shrug": return arm(Ls,[76,262],[66,236])+arm(Rs,[224,262],[234,236]);
    case "left": return arm(Ls,[90,280],[96,302]);
    case "cover": return arm(Ls,[90,220],[122,196])+arm(Rs,[210,220],[178,196]);
    default: return arm(Ls,[90,280],[96,302])+arm(Rs,[210,280],[204,302]);
  }
}
function kid({gdy=0,glint=0,push=0,gl="norm",eye="norm",brow="norm",mo="smile",ah="?",arm="down",extra="",tilt=0,front=false}){
  const head=`
   <circle cx="150" cy="140" r="90" fill="${SKIN}" stroke="${INK}" stroke-width="7"/>
   <path d="M62 150 C52 72 102 46 150 46 C200 46 250 72 238 150 C230 130 222 116 210 106 C202 122 186 124 172 112 C160 128 132 126 120 112 C108 126 86 132 62 150Z" fill="${HAIR}" stroke="${INK}" stroke-width="6" stroke-linejoin="round"/>
   <path d="M104 64 Q122 54 140 56" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round" opacity=".35"/>
   <ellipse cx="60" cy="160" rx="10" ry="16" fill="${SKIN}" stroke="${INK}" stroke-width="5"/>
   <ellipse cx="240" cy="160" rx="10" ry="16" fill="${SKIN}" stroke="${INK}" stroke-width="5"/>
   ${eyes(eye)}${glasses(gl,gdy,glint)}<g transform="translate(0 -9)">${brows(brow)}</g>${mouth(mo)}
   <ellipse cx="96" cy="178" rx="13" ry="7" fill="${CHEEK}" opacity=".75"/><ellipse cx="204" cy="178" rx="13" ry="7" fill="${CHEEK}" opacity=".75"/>`;
  const body=`
   <path d="M128 318 L126 340 L110 340 M172 318 L174 340 L190 340" fill="none" stroke="${INK}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
   <path d="M104 245 Q150 222 196 245 L204 312 Q150 328 96 312Z" fill="${HOOD}" stroke="${INK}" stroke-width="6" stroke-linejoin="round"/>
   <path d="M122 290 Q150 298 178 290 L176 306 Q150 312 124 306Z" fill="${HOODD}" stroke="${INK}" stroke-width="4"/>
   <path d="M138 236 L136 262 M162 236 L164 262" stroke="#fff" stroke-width="4" stroke-linecap="round"/>`;
  return `<svg viewBox="20 -40 260 400"><g transform="rotate(${tilt} 150 220)">
   <ellipse cx="150" cy="344" rx="66" ry="8" fill="#0002"/>
   ${body}${front?"":arms(arm)}${ahoge(ah)}${head}${front?arms(arm):""}${push?pushArm(push):""}${extra}</g></svg>`;
}
