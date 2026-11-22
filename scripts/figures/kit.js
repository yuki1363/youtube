// 図解キット（図解画像生成部門）：部品を関数で呼び出してSVGを組み立てる。
// 使い方（各図のHTML）:
//   <script src="（相対パス）/scripts/figures/kit.js"></script>
//   <script>scene({step:"検査 1", title:"大きさと<em>厚み</em>", body: coin(540,700,110) + ...});</script>
// 画面は 1080x1920。上 120〜420 がタイトル、下 1480〜1920 は字幕とShortsのボタン用に空ける。
// 部品はすべて自作の図形。実在のロゴ・キャラクターは描かない。

const K = {
  ink: "#1E293B", muted: "#64748B", accent: "#EF4444", blue: "#2563EB", blueL: "#93C5FD",
  green: "#16A34A", gold: "#FBBF24",
};

const DEFS = `
<defs>
 <radialGradient id="kCoin" cx="35%" cy="30%" r="80%">
  <stop offset="0" stop-color="#FFF7C2"/><stop offset=".35" stop-color="#FCD34D"/><stop offset=".8" stop-color="#D97706"/><stop offset="1" stop-color="#92400E"/></radialGradient>
 <linearGradient id="kCoinEdge" x1="0" x2="1"><stop offset="0" stop-color="#FDE68A"/><stop offset=".5" stop-color="#D97706"/><stop offset="1" stop-color="#78350F"/></linearGradient>
 <linearGradient id="kMetal" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F8FAFC"/><stop offset=".5" stop-color="#CBD5E1"/><stop offset="1" stop-color="#94A3B8"/></linearGradient>
 <linearGradient id="kCopper" x1="0" x2="1"><stop offset="0" stop-color="#7C2D12"/><stop offset=".3" stop-color="#EA580C"/><stop offset=".5" stop-color="#FDBA74"/><stop offset=".7" stop-color="#EA580C"/><stop offset="1" stop-color="#7C2D12"/></linearGradient>
 <linearGradient id="kRed" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F87171"/><stop offset=".5" stop-color="#DC2626"/><stop offset="1" stop-color="#991B1B"/></linearGradient>
 <linearGradient id="kGlass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#E2E8F0"/></linearGradient>
 <linearGradient id="kBlue" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#60A5FA"/><stop offset="1" stop-color="#1D4ED8"/></linearGradient>
 <linearGradient id="kMascot" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FEF08A"/><stop offset="1" stop-color="#F59E0B"/></linearGradient>
 <filter id="kSh" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="18" stdDeviation="18" flood-color="#92400E" flood-opacity=".22"/></filter>
 <filter id="kShS" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="6" stdDeviation="6" flood-color="#1E293B" flood-opacity=".25"/></filter>
 <filter id="kGlow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="10" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
 <pattern id="kDots" width="36" height="36" patternUnits="userSpaceOnUse"><circle cx="18" cy="18" r="2.2" fill="#B45309" opacity=".10"/></pattern>
</defs>`;

// ---------- 背景・タイトル ----------
function background() {
  return `<rect width="1080" height="1920" fill="url(#kBg)"/>
  <radialGradient id="kBg" cx="50%" cy="35%" r="80%"><stop offset="0" stop-color="#FFFBF2"/><stop offset="1" stop-color="#FDE7C4"/></radialGradient>
  <rect width="1080" height="1920" fill="url(#kDots)"/>
  <circle cx="980" cy="420" r="260" fill="#FDBA74" opacity=".12"/><circle cx="80" cy="1300" r="220" fill="#FCA5A5" opacity=".10"/>`;
}

function titleBlock(step, title) {
  const stepSvg = step
    ? `<g filter="url(#kShS)"><rect x="${540 - (step.length * 22 + 50)}" y="135" width="${step.length * 44 + 100}" height="70" rx="35" fill="${K.ink}"/></g>
       <text x="540" y="183" text-anchor="middle" font-size="42" font-weight="900" fill="#fff" letter-spacing="4">${step}</text>` : "";
  // <em>〜</em> を赤くする。白いふちどりで背景から浮かせる
  const t = title.replace(/<em>(.*?)<\/em>/g, `<tspan fill="${K.accent}">$1</tspan>`);
  const y = step ? 330 : 300;
  return `${stepSvg}
  <text x="540" y="${y}" text-anchor="middle" font-size="104" font-weight="900" fill="${K.ink}"
    stroke="#fff" stroke-width="22" stroke-linejoin="round" paint-order="stroke" filter="url(#kShS)">${t}</text>`;
}

// ---------- 部品 ----------
function floorShadow(cx, cy, rx, ry = rx * 0.18, op = 0.18) {
  return `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="#7C2D12" opacity="${op}"/>`;
}

function coin(cx, cy, r, opt = {}) {
  const label = opt.label ? `<text x="${cx}" y="${cy + r * 0.2}" text-anchor="middle" font-size="${r * 0.6}" font-weight="900" fill="#92400E" opacity=".75">${opt.label}</text>` : "";
  const motion = opt.motion ? [0, 1, 2].map(i =>
    `<line x1="${cx - r - 40 - i * 10}" y1="${cy - r * 0.5 + i * r * 0.5}" x2="${cx - r - 140 + i * 10}" y2="${cy - r * 0.5 + i * r * 0.5}" stroke="#F59E0B" stroke-width="${r * 0.1}" stroke-linecap="round" opacity="${0.6 - i * 0.15}"/>`).join("") : "";
  const shadow = opt.shadow === false ? "" : floorShadow(cx, cy + r + 18, r * 0.8);
  return `${motion}${shadow}
  <g filter="url(#kShS)">
   <circle cx="${cx}" cy="${cy + r * 0.08}" r="${r}" fill="url(#kCoinEdge)"/>
   <circle cx="${cx}" cy="${cy}" r="${r}" fill="url(#kCoin)" stroke="#92400E" stroke-width="${r * 0.05}"/>
   <circle cx="${cx}" cy="${cy}" r="${r * 0.78}" fill="none" stroke="#B45309" stroke-width="${r * 0.05}" opacity=".55"/>
   <path d="M${cx - r * 0.5},${cy - r * 0.62} A${r * 0.8},${r * 0.8} 0 0 1 ${cx + r * 0.3},${cy - r * 0.72}" stroke="#fff" stroke-width="${r * 0.12}" fill="none" stroke-linecap="round" opacity=".7"/>
   ${label}
  </g>`;
}

function coinSide(cx, cy, w, h) {
  return `<g filter="url(#kShS)"><rect x="${cx - w / 2}" y="${cy - h / 2}" width="${w}" height="${h}" rx="${w * 0.3}" fill="url(#kCoinEdge)" stroke="#78350F" stroke-width="5"/>
  <rect x="${cx - w / 2 + w * 0.2}" y="${cy - h / 2 + 12}" width="${w * 0.2}" height="${h - 24}" rx="4" fill="#fff" opacity=".5"/></g>`;
}

function bottle(x, y, color, dark) {
  return `<g><rect x="${x + 18}" y="${y - 28}" width="34" height="34" rx="8" fill="${dark}"/>
  <path d="M${x + 10},${y} Q${x},${y + 20} ${x},${y + 45} L${x},${y + 140} Q${x},${y + 160} ${x + 20},${y + 160} L${x + 50},${y + 160} Q${x + 70},${y + 160} ${x + 70},${y + 140} L${x + 70},${y + 45} Q${x + 70},${y + 20} ${x + 60},${y} Z" fill="${color}"/>
  <rect x="${x}" y="${y + 60}" width="70" height="44" fill="#fff" opacity=".8"/>
  <rect x="${x + 10}" y="${y + 10}" width="10" height="130" rx="5" fill="#fff" opacity=".45"/></g>`;
}

// 自販機（ロゴなし）。x,y は左上、s は倍率（基準 幅560 高さ980）
function vendingMachine(x, y, s = 1) {
  const bottles = [["#38BDF8", "#0284C7"], ["#FB923C", "#EA580C"], ["#4ADE80", "#16A34A"], ["#C084FC", "#9333EA"]]
    .map((c, i) => bottle(60 + i * 115, 90, c[0], c[1])).join("");
  return `<g transform="translate(${x},${y}) scale(${s})">
  ${floorShadow(280, 1000, 330, 40, 0.22)}
  <g filter="url(#kSh)">
   <rect x="0" y="0" width="560" height="980" rx="48" fill="url(#kRed)"/>
   <rect x="0" y="0" width="560" height="980" rx="48" fill="none" stroke="#7F1D1D" stroke-width="6"/>
  </g>
  <rect x="14" y="14" width="40" height="950" rx="20" fill="#fff" opacity=".15"/>
  <rect x="40" y="40" width="480" height="480" rx="26" fill="url(#kGlass)" stroke="#7F1D1D" stroke-width="6"/>
  ${bottles}
  ${[0, 1, 2, 3].map(i => `<rect x="${72 + i * 115}" y="290" width="46" height="22" rx="11" fill="#F43F5E"/>`).join("")}
  <rect x="60" y="340" width="440" height="150" rx="16" fill="#E2E8F0"/>
  ${[0, 1, 2].map(i => `<rect x="${90 + i * 140}" y="370" width="100" height="90" rx="12" fill="#CBD5E1"/>`).join("")}
  <rect x="380" y="570" width="130" height="190" rx="18" fill="#1E293B"/>
  <rect x="405" y="590" width="80" height="44" rx="8" fill="#22C55E" opacity=".85"/>
  <rect x="428" y="660" width="34" height="80" rx="12" fill="#FBBF24"/>
  <rect x="60" y="820" width="440" height="110" rx="20" fill="#111827"/>
  <rect x="80" y="836" width="400" height="60" rx="12" fill="#374151"/>
  <rect x="330" y="610" width="30" height="120" rx="12" fill="#111827" opacity=".0"/>
  </g>`;
}

function rail(x1, y1, x2, y2, t = 40) {
  return `<g filter="url(#kSh)"><path d="M${x1},${y1} L${x2},${y2} L${x2},${y2 + t} L${x1},${y1 + t} Z" fill="url(#kMetal)" stroke="#64748B" stroke-width="4"/></g>
  <path d="M${x1},${y1 + 6} L${x2},${y2 + 6}" stroke="#fff" stroke-width="6" opacity=".8"/>`;
}

function sensor(x, y, w = 150, h = 74, label = "") {
  return `<g filter="url(#kShS)"><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="18" fill="url(#kBlue)"/></g>
  <circle cx="${x + w / 2}" cy="${y + h / 2}" r="14" fill="#BFDBFE" filter="url(#kGlow)"/>
  ${label ? `<text x="${x + w / 2}" y="${y - 20}" text-anchor="middle" font-size="40" font-weight="900" fill="${K.blue}">${label}</text>` : ""}`;
}

function beam(x1, y1, x2, y2) {
  return `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="#60A5FA" stroke-width="16" opacity=".25" stroke-linecap="round"/>
  <line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="#2563EB" stroke-width="5" stroke-dasharray="14 10" stroke-linecap="round"/>`;
}

// コイル：中心(cx,cy)、巻き数 n、幅 w、高さ h
function coil(cx, cy, n = 8, w = 300, h = 200) {
  const step = w / (n - 1);
  let back = "", front = "";
  for (let i = 0; i < n; i++) {
    const x = cx - w / 2 + i * step;
    back += `<path d="M${x - 8},${cy - h / 2} Q${x + 16},${cy} ${x - 8},${cy + h / 2}" stroke="#7C2D12" stroke-width="22" fill="none" stroke-linecap="round"/>`;
    front += `<path d="M${x},${cy - h / 2} Q${x - 24},${cy} ${x},${cy + h / 2}" stroke="url(#kCopper)" stroke-width="26" fill="none" stroke-linecap="round"/>
      <path d="M${x - 4},${cy - h / 2 + 14} Q${x - 22},${cy - 10} ${x - 10},${cy + 20}" stroke="#FED7AA" stroke-width="6" fill="none" stroke-linecap="round" opacity=".8"/>`;
  }
  return back + front;
}

function fieldLines(cx, cy, rings = [[220, 190], [310, 260], [400, 330]]) {
  return rings.map(([rx, ry], i) =>
    `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="none" stroke="${K.blue}" stroke-width="7" stroke-dasharray="20 14" opacity="${0.85 - i * 0.2}"/>`).join("")
    + `<ellipse cx="${cx}" cy="${cy}" rx="${rings[0][0]}" ry="${rings[0][1]}" fill="#93C5FD" opacity=".12"/>`;
}

function card(x, y, w, h, opt = {}) {
  const border = opt.border ? `stroke="${opt.border}" stroke-width="8"` : "";
  return `<g filter="url(#kSh)"><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="36" fill="#fff" ${border}/></g>`;
}

function pill(cx, cy, text, color = K.ink, size = 46) {
  const w = text.length * size + 60;
  return `<g filter="url(#kShS)"><rect x="${cx - w / 2}" y="${cy - size * 0.85}" width="${w}" height="${size * 1.7}" rx="${size * 0.85}" fill="${color}"/></g>
  <text x="${cx}" y="${cy + size * 0.35}" text-anchor="middle" font-size="${size}" font-weight="900" fill="#fff">${text}</text>`;
}

function label(x, y, text, color = K.ink, size = 46, anchor = "middle") {
  return `<text x="${x}" y="${y}" text-anchor="${anchor}" font-size="${size}" font-weight="900" fill="${color}"
    stroke="#fff" stroke-width="10" stroke-linejoin="round" paint-order="stroke">${text}</text>`;
}

function arrow(x1, y1, x2, y2, color = K.ink, w = 14) {
  const a = Math.atan2(y2 - y1, x2 - x1), h = w * 2.6;
  const p = (ang) => `${x2 - h * Math.cos(a + ang)},${y2 - h * Math.sin(a + ang)}`;
  return `<line x1="${x1}" y1="${y1}" x2="${x2 - Math.cos(a) * h * 0.6}" y2="${y2 - Math.sin(a) * h * 0.6}" stroke="${color}" stroke-width="${w}" stroke-linecap="round"/>
  <polygon points="${x2},${y2} ${p(0.5)} ${p(-0.5)}" fill="${color}" stroke="${color}" stroke-width="4" stroke-linejoin="round"/>`;
}

function curvePath(d, color, w = 40) {
  return `<path d="${d}" fill="none" stroke="${color}" stroke-width="${w + 14}" stroke-linecap="round" opacity=".18"/>
  <path d="${d}" fill="none" stroke="${color}" stroke-width="${w}" stroke-linecap="round"/>`;
}

function check(cx, cy, r = 56) {
  return `<circle cx="${cx}" cy="${cy}" r="${r}" fill="${K.green}" filter="url(#kShS)"/>
  <path d="M${cx - r * 0.5},${cy} L${cx - r * 0.12},${cy + r * 0.42} L${cx + r * 0.55},${cy - r * 0.4}" fill="none" stroke="#fff" stroke-width="${r * 0.26}" stroke-linecap="round" stroke-linejoin="round"/>`;
}

function cross(cx, cy, r = 40) {
  return `<circle cx="${cx}" cy="${cy}" r="${r}" fill="${K.accent}" filter="url(#kShS)"/>
  <path d="M${cx - r * 0.42},${cy - r * 0.42} L${cx + r * 0.42},${cy + r * 0.42} M${cx + r * 0.42},${cy - r * 0.42} L${cx - r * 0.42},${cy + r * 0.42}" stroke="#fff" stroke-width="${r * 0.28}" stroke-linecap="round"/>`;
}

function bubble(cx, cy, r, text, color = K.accent, tail = "left") {
  const t = tail === "left" ? `M${cx - r * 0.55},${cy + r * 0.7} L${cx - r * 0.95},${cy + r * 1.25} L${cx - r * 0.15},${cy + r * 0.92} Z`
                            : `M${cx + r * 0.55},${cy + r * 0.7} L${cx + r * 0.95},${cy + r * 1.25} L${cx + r * 0.15},${cy + r * 0.92} Z`;
  return `<g filter="url(#kSh)"><circle cx="${cx}" cy="${cy}" r="${r}" fill="#fff"/><path d="${t}" fill="#fff"/></g>
  <text x="${cx}" y="${cy + r * 0.36}" text-anchor="middle" font-size="${r * 1.05}" font-weight="900" fill="${color}">${text}</text>`;
}

// 小さなグラフ（イメージ図）。ok=true なら基準の帯の中に収まる山
function miniGraph(x, y, w, h, ok, title) {
  const color = ok ? K.green : K.accent;
  const peak = ok ? y + h * 0.42 : y + h * 0.02;
  const base = y + h * 0.82;
  return `${card(x, y - 80, w, h + 120, { border: ok ? "#BBF7D0" : "#FECACA" })}
  <text x="${x + w / 2}" y="${y - 10}" text-anchor="middle" font-size="44" font-weight="900" fill="${color}">${title}</text>
  <rect x="${x + 40}" y="${y + h * 0.32}" width="${w - 80}" height="${h * 0.3}" rx="8" fill="#DCFCE7"/>
  <text x="${x + w - 50}" y="${y + h * 0.3 - 8}" text-anchor="end" font-size="28" font-weight="700" fill="${K.green}">基準</text>
  <path d="M${x + 40},${base} C${x + w * 0.35},${base} ${x + w * 0.35},${peak} ${x + w / 2},${peak} C${x + w * 0.65},${peak} ${x + w * 0.65},${base} ${x + w - 40},${base}"
    fill="none" stroke="${color}" stroke-width="12" stroke-linecap="round"/>`;
}

// オリジナルのナビゲーター「ビリ太」：電気の玉に雷のアンテナ。mood: "q"(疑問) "wow"(驚き) "point"(説明)
function mascot(cx, cy, s = 1, mood = "point") {
  const eyes = mood === "wow"
    ? `<circle cx="-30" cy="-10" r="14" fill="${K.ink}"/><circle cx="30" cy="-10" r="14" fill="${K.ink}"/><ellipse cx="0" cy="40" rx="16" ry="20" fill="#7C2D12"/>`
    : mood === "q"
      ? `<circle cx="-30" cy="-8" r="11" fill="${K.ink}"/><circle cx="30" cy="-8" r="11" fill="${K.ink}"/><path d="M-18,38 Q0,30 18,38" stroke="#7C2D12" stroke-width="7" fill="none" stroke-linecap="round"/>`
      : `<path d="M-42,-8 Q-30,-22 -18,-8" stroke="${K.ink}" stroke-width="9" fill="none" stroke-linecap="round"/><path d="M18,-8 Q30,-22 42,-8" stroke="${K.ink}" stroke-width="9" fill="none" stroke-linecap="round"/><path d="M-24,28 Q0,54 24,28 Z" fill="#7C2D12"/>`;
  const armR = mood === "point" ? `<path d="M80,10 Q130,-10 160,-50" stroke="#F59E0B" stroke-width="20" fill="none" stroke-linecap="round"/><circle cx="162" cy="-52" r="16" fill="#FDE047"/>`
                                : `<path d="M82,20 Q120,40 130,80" stroke="#F59E0B" stroke-width="20" fill="none" stroke-linecap="round"/>`;
  return `<g transform="translate(${cx},${cy}) scale(${s})">
   ${floorShadow(0, 150, 90, 16, 0.2)}
   <path d="M-6,-130 L22,-170 L4,-168 L26,-212 L-14,-160 L4,-162 Z" fill="#FDE047" stroke="#B45309" stroke-width="6" stroke-linejoin="round"/>
   <line x1="0" y1="-96" x2="2" y2="-132" stroke="#B45309" stroke-width="8"/>
   <path d="M-82,20 Q-120,40 -130,80" stroke="#F59E0B" stroke-width="20" fill="none" stroke-linecap="round"/>
   ${armR}
   <circle cx="0" cy="0" r="100" fill="url(#kMascot)" stroke="#B45309" stroke-width="7" filter="url(#kShS)"/>
   <ellipse cx="-38" cy="-50" rx="28" ry="16" fill="#fff" opacity=".6" transform="rotate(-25 -38 -50)"/>
   <ellipse cx="-58" cy="22" rx="16" ry="10" fill="#FB7185" opacity=".55"/><ellipse cx="58" cy="22" rx="16" ry="10" fill="#FB7185" opacity=".55"/>
   ${eyes}
   <rect x="-40" y="96" width="24" height="50" rx="10" fill="#B45309"/><rect x="16" y="96" width="24" height="50" rx="10" fill="#B45309"/>
  </g>`;
}

function note(text, y = 1450) {
  return `<text x="540" y="${y}" text-anchor="middle" font-size="34" font-weight="700" fill="${K.muted}">${text}</text>`;
}

// 1枚を組み立てて body に描く
function scene({ step = "", title = "", body = "" }) {
  document.body.style.margin = "0";
  document.body.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920"
    style="font-family:'Noto Sans CJK JP','Noto Sans JP',sans-serif;display:block">${DEFS}${background()}${body}${titleBlock(step, title)}</svg>`;
}
