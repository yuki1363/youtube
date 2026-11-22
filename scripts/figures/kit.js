// 図解キット v2「ゆるかわ」（図解画像生成部門）：部品を関数で呼び出してSVGを組み立てる。
// 使い方（各図のHTML）:
//   <script src="（相対パス）/scripts/figures/kit.js"></script>
//   <script>scene({step:"検査 1", title:"大きさと<em>厚み</em>", body: coin(540,700,110,{face:"smile"}) + ...});</script>
// 画面は 1080x1920。上 120〜420 がタイトル、下 1480〜1920 は字幕とShortsのボタン用に空ける。
// 作風：パステルカラー／こげ茶の太いふちどり（ステッカー風）／丸い角／モノに顔／キラキラ
// 部品はすべて自作の図形。実在のロゴ・キャラクターに似せない。

const K = {
  ol: "#5B3A29",            // ふちどり（こげ茶）
  ink: "#4A3428", muted: "#9A7B6A",
  accent: "#FF6B8B",        // 強調（ピンク）
  blue: "#5B9BFF", blueL: "#BFD9FF",
  green: "#3CC08A", greenL: "#C8F2DD",
  yellow: "#FFD45C", cream: "#FFF6E8", pink: "#FFD1DC", mint: "#C8F2E6", lav: "#E3D7FF",
};
const OLW = 7;              // ふちどりの太さ

const DEFS = `
<defs>
 <radialGradient id="kCoin" cx="35%" cy="30%" r="80%"><stop offset="0" stop-color="#FFF9D6"/><stop offset=".55" stop-color="#FFD45C"/><stop offset="1" stop-color="#F2A93B"/></radialGradient>
 <linearGradient id="kCoinEdge" x1="0" x2="1"><stop offset="0" stop-color="#FFE08A"/><stop offset="1" stop-color="#E0962F"/></linearGradient>
 <linearGradient id="kMetal" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#D9DEEA"/></linearGradient>
 <linearGradient id="kCopper" x1="0" x2="1"><stop offset="0" stop-color="#E9865A"/><stop offset=".5" stop-color="#FFC09A"/><stop offset="1" stop-color="#E9865A"/></linearGradient>
 <linearGradient id="kMachine" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FF9EB5"/><stop offset="1" stop-color="#FF7A98"/></linearGradient>
 <linearGradient id="kBlue" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9CC3FF"/><stop offset="1" stop-color="#5B9BFF"/></linearGradient>
 <linearGradient id="kMascot" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF3A8"/><stop offset="1" stop-color="#FFC94A"/></linearGradient>
 <radialGradient id="kBg" cx="50%" cy="30%" r="85%"><stop offset="0" stop-color="#FFFBF3"/><stop offset="1" stop-color="#FFE6EC"/></radialGradient>
 <filter id="kSh" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="12" stdDeviation="0" flood-color="#5B3A29" flood-opacity=".12"/></filter>
 <filter id="kShS" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="6" stdDeviation="0" flood-color="#5B3A29" flood-opacity=".14"/></filter>
 <filter id="kGlow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="8" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
 <pattern id="kDots" width="48" height="48" patternUnits="userSpaceOnUse"><circle cx="24" cy="24" r="3" fill="#FF9EB5" opacity=".16"/></pattern>
</defs>`;

const O = (w = OLW) => `stroke="${K.ol}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;

// ---------- 飾り ----------
function sparkle(x, y, s = 1, color = "#FFD45C") {
  return `<path transform="translate(${x},${y}) scale(${s})" d="M0,-30 C4,-8 8,-4 30,0 C8,4 4,8 0,30 C-4,8 -8,4 -30,0 C-8,-4 -4,-8 0,-30 Z" fill="${color}" ${O(4)}/>`;
}
function heart(x, y, s = 1, color = K.accent) {
  return `<path transform="translate(${x},${y}) scale(${s})" d="M0,18 C-28,-2 -26,-26 -10,-26 C-2,-26 0,-18 0,-14 C0,-18 2,-26 10,-26 C26,-26 28,-2 0,18 Z" fill="${color}" ${O(4)}/>`;
}

// ---------- 背景・タイトル ----------
function background() {
  const deco = [[90, 470, .8, "#FFD45C"], [990, 520, .6, "#9CC3FF"], [60, 1100, .5, "#FF9EB5"], [1020, 1250, .7, "#C8F2E6"], [960, 900, .4, "#FFD45C"]]
    .map(([x, y, s, c]) => sparkle(x, y, s, c)).join("");
  return `<rect width="1080" height="1920" fill="url(#kBg)"/><rect width="1080" height="1920" fill="url(#kDots)"/>
  <circle cx="1000" cy="380" r="240" fill="#FFE08A" opacity=".18"/><circle cx="60" cy="1350" r="220" fill="#C8F2E6" opacity=".35"/>${deco}`;
}

function titleBlock(step, title) {
  const stepSvg = step
    ? `<g filter="url(#kShS)"><rect x="${540 - (step.length * 22 + 50)}" y="130" width="${step.length * 44 + 100}" height="74" rx="37" fill="${K.accent}" ${O(5)}/></g>
       <text x="540" y="181" text-anchor="middle" font-size="42" font-weight="900" fill="#fff" letter-spacing="4">${step}</text>` : "";
  const t = title.replace(/<em>(.*?)<\/em>/g, `<tspan fill="${K.accent}">$1</tspan>`);
  const y = step ? 330 : 300;
  return `${stepSvg}
  <text x="540" y="${y}" text-anchor="middle" font-size="104" font-weight="900" fill="${K.ink}"
    stroke="#fff" stroke-width="26" stroke-linejoin="round" paint-order="stroke" filter="url(#kShS)">${t}</text>`;
}

// ---------- 顔（モノに付ける） ----------
// mood: smile / happy / sad / wow / q
function face(cx, cy, s = 1, mood = "smile") {
  const e = (x) => mood === "happy"
    ? `<path d="M${x - 9},2 Q${x},-10 ${x + 9},2" stroke="${K.ol}" stroke-width="6" fill="none" stroke-linecap="round"/>`
    : mood === "sad"
      ? `<ellipse cx="${x}" cy="0" rx="7" ry="9" fill="${K.ol}"/><path d="M${x - 10},-16 L${x + 8},-12" stroke="${K.ol}" stroke-width="4" stroke-linecap="round" transform="${x < 0 ? "" : `scale(-1,1) translate(${-2 * x},0)`}"/>`
      : `<ellipse cx="${x}" cy="0" rx="8" ry="11" fill="${K.ol}"/><circle cx="${x + 3}" cy="-4" r="3.5" fill="#fff"/>`;
  const m = mood === "wow" ? `<ellipse cx="0" cy="20" rx="8" ry="10" fill="${K.ol}"/>`
    : mood === "sad" ? `<path d="M-9,24 Q0,16 9,24" stroke="${K.ol}" stroke-width="5" fill="none" stroke-linecap="round"/>`
      : mood === "q" ? `<path d="M-8,20 L8,20" stroke="${K.ol}" stroke-width="5" stroke-linecap="round"/>`
        : `<path d="M-10,16 Q0,28 10,16" stroke="${K.ol}" stroke-width="5" fill="none" stroke-linecap="round"/>`;
  return `<g transform="translate(${cx},${cy}) scale(${s})">${e(-22)}${e(22)}${m}
    <ellipse cx="-38" cy="14" rx="11" ry="7" fill="#FF8FA8" opacity=".6"/><ellipse cx="38" cy="14" rx="11" ry="7" fill="#FF8FA8" opacity=".6"/></g>`;
}

// ---------- 部品 ----------
function floorShadow(cx, cy, rx, ry = rx * 0.16, op = 0.12) {
  return `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="${K.ol}" opacity="${op}"/>`;
}

// 硬貨。opt.face で顔（smile/happy/sad/wow/q）、opt.label で文字、opt.motion で動きの線
function coin(cx, cy, r, opt = {}) {
  const motion = opt.motion ? [0, 1, 2].map(i =>
    `<line x1="${cx - r - 30 - i * 8}" y1="${cy - r * 0.45 + i * r * 0.45}" x2="${cx - r - 120 + i * 8}" y2="${cy - r * 0.45 + i * r * 0.45}" stroke="${K.ol}" stroke-width="${Math.max(6, r * 0.07)}" stroke-linecap="round" opacity="${0.5 - i * 0.12}"/>`).join("") : "";
  const shadow = opt.shadow === false ? "" : floorShadow(cx, cy + r + 16, r * 0.8);
  const inner = opt.label
    ? `<text x="${cx}" y="${cy + r * 0.22}" text-anchor="middle" font-size="${r * 0.62}" font-weight="900" fill="#C47A1C">${opt.label}</text>`
    : opt.face === false ? "" : face(cx, cy + r * 0.05, r / 85, opt.face || "smile");
  return `${motion}${shadow}
  <g filter="url(#kShS)">
   <circle cx="${cx}" cy="${cy}" r="${r}" fill="url(#kCoin)" ${O(Math.max(5, r * 0.07))}/>
   <circle cx="${cx}" cy="${cy}" r="${r * 0.86}" fill="none" stroke="#E8A23A" stroke-width="${r * 0.1}"/>
   <circle cx="${cx}" cy="${cy}" r="${r * 0.86}" fill="none" stroke="#FFF3C4" stroke-width="${r * 0.03}" stroke-dasharray="${r * 0.05} ${r * 0.09}"/>
   <ellipse cx="${cx - r * 0.42}" cy="${cy - r * 0.48}" rx="${r * 0.2}" ry="${r * 0.11}" fill="#fff" opacity=".85" transform="rotate(-30 ${cx - r * 0.42} ${cy - r * 0.48})"/>
  </g>${inner}`;
}

function coinSide(cx, cy, w, h) {
  return `<g filter="url(#kShS)"><rect x="${cx - w / 2}" y="${cy - h / 2}" width="${w}" height="${h}" rx="${w * 0.45}" fill="url(#kCoinEdge)" ${O(6)}/>
  <rect x="${cx - w / 2 + w * 0.25}" y="${cy - h / 2 + 18}" width="${w * 0.18}" height="${h - 36}" rx="4" fill="#fff" opacity=".7"/></g>`;
}

function bottle(x, y, color) {
  return `<g><rect x="${x + 20}" y="${y - 24}" width="30" height="30" rx="10" fill="#fff" ${O(5)}/>
  <rect x="${x}" y="${y}" width="70" height="150" rx="28" fill="${color}" ${O(5)}/>
  <rect x="${x + 6}" y="${y + 58}" width="58" height="38" rx="10" fill="#fff" opacity=".85"/>
  <rect x="${x + 12}" y="${y + 14}" width="10" height="34" rx="5" fill="#fff" opacity=".7"/></g>`;
}

// 自販機（ロゴなし・顔つき）。x,y は左上、s は倍率（基準 幅560 高さ980）。mood で顔
function vendingMachine(x, y, s = 1, mood = "smile") {
  const bottles = ["#9CC3FF", "#FFB38A", "#8FE3B5", "#C9B3FF"].map((c, i) => bottle(62 + i * 114, 92, c)).join("");
  return `<g transform="translate(${x},${y}) scale(${s})">
  ${floorShadow(280, 1000, 320, 36)}
  <g filter="url(#kSh)"><rect x="0" y="0" width="560" height="980" rx="70" fill="url(#kMachine)" ${O(9)}/></g>
  <rect x="26" y="40" width="30" height="300" rx="15" fill="#fff" opacity=".35"/>
  <rect x="40" y="40" width="480" height="300" rx="40" fill="#FFF9F2" ${O(7)}/>
  ${bottles}
  ${[0, 1, 2, 3].map(i => `<circle cx="${97 + i * 114}" cy="290" r="14" fill="#FFD45C" ${O(4)}/>`).join("")}
  <rect x="60" y="380" width="440" height="230" rx="44" fill="#FFF9F2" ${O(7)}/>
  ${face(280, 480, 1.9, mood)}
  <rect x="390" y="650" width="120" height="150" rx="28" fill="#FFF9F2" ${O(6)}/>
  <rect x="430" y="675" width="40" height="100" rx="16" fill="#FFD45C" ${O(5)}/>
  <rect x="70" y="830" width="420" height="110" rx="40" fill="#FFF9F2" ${O(7)}/>
  <rect x="100" y="852" width="360" height="56" rx="24" fill="#8A6B5C"/>
  </g>`;
}

function rail(x1, y1, x2, y2, t = 40) {
  return `<g filter="url(#kSh)"><path d="M${x1},${y1} L${x2},${y2} L${x2},${y2 + t} L${x1},${y1 + t} Z" fill="url(#kMetal)" ${O(6)}/></g>
  <path d="M${x1 + 10},${y1 + 10} L${x2 - 10},${y2 + 10}" stroke="#fff" stroke-width="6" stroke-linecap="round"/>`;
}

function sensor(x, y, w = 150, h = 80, label = "") {
  return `<g filter="url(#kShS)"><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="30" fill="url(#kBlue)" ${O(6)}/></g>
  ${face(x + w / 2, y + h / 2, 0.55, "smile")}
  ${label ? label_(x + w / 2, y - 22, label, K.blue, 40) : ""}`;
}

function beam(x1, y1, x2, y2) {
  return `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="#BFD9FF" stroke-width="20" opacity=".7" stroke-linecap="round"/>
  <line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${K.blue}" stroke-width="6" stroke-dasharray="10 10" stroke-linecap="round"/>`;
}

// コイル：中心(cx,cy)、巻き数 n、幅 w、高さ h
function coil(cx, cy, n = 8, w = 300, h = 200) {
  const step = w / (n - 1);
  let s = `<rect x="${cx - w / 2 - 30}" y="${cy - h / 2 - 10}" width="${w + 60}" height="${h + 20}" rx="40" fill="#FFE3D3" ${O(6)} opacity=".9"/>`;
  for (let i = 0; i < n; i++) {
    const x = cx - w / 2 + i * step;
    s += `<rect x="${x - 15}" y="${cy - h / 2}" width="30" height="${h}" rx="15" fill="url(#kCopper)" ${O(5)}/>
      <rect x="${x - 7}" y="${cy - h / 2 + 14}" width="7" height="${h * 0.4}" rx="3.5" fill="#fff" opacity=".7"/>`;
  }
  return s;
}

function fieldLines(cx, cy, rings = [[220, 190], [310, 260], [400, 330]]) {
  return `<ellipse cx="${cx}" cy="${cy}" rx="${rings[0][0]}" ry="${rings[0][1]}" fill="#DCEBFF" opacity=".6"/>` +
    rings.map(([rx, ry], i) =>
      `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="none" stroke="${K.blue}" stroke-width="8" stroke-dasharray="2 22" stroke-linecap="round" opacity="${0.9 - i * 0.2}"/>`).join("");
}

function card(x, y, w, h, opt = {}) {
  const fill = opt.fill || "#fff";
  const stroke = opt.border || K.ol;
  return `<g filter="url(#kSh)"><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="44" fill="${fill}" stroke="${stroke}" stroke-width="7"/></g>`;
}

function pill(cx, cy, text, color = K.accent, size = 46) {
  const w = text.length * size + 64;
  return `<g filter="url(#kShS)"><rect x="${cx - w / 2}" y="${cy - size * 0.88}" width="${w}" height="${size * 1.76}" rx="${size * 0.88}" fill="${color}" ${O(5)}/></g>
  <text x="${cx}" y="${cy + size * 0.36}" text-anchor="middle" font-size="${size}" font-weight="900" fill="#fff">${text}</text>`;
}

function label_(x, y, text, color = K.ink, size = 46, anchor = "middle") {
  return `<text x="${x}" y="${y}" text-anchor="${anchor}" font-size="${size}" font-weight="900" fill="${color}"
    stroke="#fff" stroke-width="12" stroke-linejoin="round" paint-order="stroke">${text}</text>`;
}
const label = label_;

function arrow(x1, y1, x2, y2, color = K.ol, w = 14) {
  const a = Math.atan2(y2 - y1, x2 - x1), h = w * 2.4;
  const p = (ang) => `${x2 - h * Math.cos(a + ang)},${y2 - h * Math.sin(a + ang)}`;
  return `<line x1="${x1}" y1="${y1}" x2="${x2 - Math.cos(a) * h * 0.6}" y2="${y2 - Math.sin(a) * h * 0.6}" stroke="${color}" stroke-width="${w}" stroke-linecap="round"/>
  <polygon points="${x2},${y2} ${p(0.55)} ${p(-0.55)}" fill="${color}" stroke="${color}" stroke-width="6" stroke-linejoin="round"/>`;
}

function curvePath(d, color, w = 40) {
  return `<path d="${d}" fill="none" stroke="${K.ol}" stroke-width="${w + 14}" stroke-linecap="round"/>
  <path d="${d}" fill="none" stroke="${color}" stroke-width="${w}" stroke-linecap="round"/>
  <path d="${d}" fill="none" stroke="#fff" stroke-width="${w * 0.2}" stroke-linecap="round" stroke-dasharray="1 ${w * 1.4}" opacity=".9"/>`;
}

function check(cx, cy, r = 56) {
  return `<circle cx="${cx}" cy="${cy}" r="${r}" fill="${K.green}" ${O(6)}/>
  <path d="M${cx - r * 0.45},${cy} L${cx - r * 0.1},${cy + r * 0.38} L${cx + r * 0.5},${cy - r * 0.36}" fill="none" stroke="#fff" stroke-width="${r * 0.24}" stroke-linecap="round" stroke-linejoin="round"/>`;
}

function cross(cx, cy, r = 40) {
  return `<circle cx="${cx}" cy="${cy}" r="${r}" fill="${K.accent}" ${O(5)}/>
  <path d="M${cx - r * 0.38},${cy - r * 0.38} L${cx + r * 0.38},${cy + r * 0.38} M${cx + r * 0.38},${cy - r * 0.38} L${cx - r * 0.38},${cy + r * 0.38}" stroke="#fff" stroke-width="${r * 0.26}" stroke-linecap="round"/>`;
}

function bubble(cx, cy, r, text, color = K.accent, tail = "left") {
  const t = tail === "left" ? `M${cx - r * 0.5},${cy + r * 0.75} L${cx - r * 0.9},${cy + r * 1.25} L${cx - r * 0.1},${cy + r * 0.95}`
                            : `M${cx + r * 0.5},${cy + r * 0.75} L${cx + r * 0.9},${cy + r * 1.25} L${cx + r * 0.1},${cy + r * 0.95}`;
  return `<g filter="url(#kSh)"><path d="${t} Z" fill="#fff" ${O(7)}/><circle cx="${cx}" cy="${cy}" r="${r}" fill="#fff" ${O(7)}/>
  <path d="${t}" fill="#fff" stroke="none" transform="translate(0,-8)"/></g>
  <text x="${cx}" y="${cy + r * 0.36}" text-anchor="middle" font-size="${r * 1.05}" font-weight="900" fill="${color}">${text}</text>`;
}

// 小さなグラフ（イメージ図）。ok=true なら基準の帯の中に収まる山
function miniGraph(x, y, w, h, ok, title) {
  const color = ok ? K.green : K.accent;
  const peak = ok ? y + h * 0.42 : y + h * 0.04;
  const base = y + h * 0.82;
  return `${card(x, y - 90, w, h + 130, { fill: ok ? "#F1FCF6" : "#FFF1F4" })}
  ${pill(x + w / 2, y - 20, title, color, 40)}
  <rect x="${x + 40}" y="${y + h * 0.32}" width="${w - 80}" height="${h * 0.3}" rx="16" fill="${K.greenL}"/>
  <text x="${x + w - 52}" y="${y + h * 0.3 - 10}" text-anchor="end" font-size="28" font-weight="900" fill="${K.green}">基準</text>
  <path d="M${x + 40},${base} C${x + w * 0.35},${base} ${x + w * 0.35},${peak} ${x + w / 2},${peak} C${x + w * 0.65},${peak} ${x + w * 0.65},${base} ${x + w - 40},${base}"
    fill="none" stroke="${K.ol}" stroke-width="20" stroke-linecap="round"/>
  <path d="M${x + 40},${base} C${x + w * 0.35},${base} ${x + w * 0.35},${peak} ${x + w / 2},${peak} C${x + w * 0.65},${peak} ${x + w * 0.65},${base} ${x + w - 40},${base}"
    fill="none" stroke="${color}" stroke-width="11" stroke-linecap="round"/>`;
}

// オリジナルのナビゲーター「ビリ太」v2：まんまるの電気の子。頭に雷のアホ毛。mood: q / wow / point / happy
function mascot(cx, cy, s = 1, mood = "point") {
  const eye = (x) => mood === "happy"
    ? `<path d="M${x - 16},-4 Q${x},-24 ${x + 16},-4" stroke="${K.ol}" stroke-width="9" fill="none" stroke-linecap="round"/>`
    : `<ellipse cx="${x}" cy="-6" rx="17" ry="${mood === "wow" ? 24 : 21}" fill="${K.ol}"/>
       <circle cx="${x + 6}" cy="-14" r="7.5" fill="#fff"/><circle cx="${x - 6}" cy="4" r="3.5" fill="#fff"/>`;
  const mouth = mood === "wow" ? `<ellipse cx="0" cy="42" rx="13" ry="16" fill="#E85A70" ${O(5)}/>`
    : mood === "q" ? `<path d="M-12,40 Q0,34 12,40" stroke="${K.ol}" stroke-width="7" fill="none" stroke-linecap="round"/>`
      : `<path d="M-20,32 Q0,58 20,32 Z" fill="#E85A70" ${O(5)}/>`;
  const armR = mood === "point"
    ? `<path d="M92,0 Q132,-20 150,-58" stroke="${K.ol}" stroke-width="30" fill="none" stroke-linecap="round"/><path d="M92,0 Q132,-20 150,-58" stroke="#FFC94A" stroke-width="18" fill="none" stroke-linecap="round"/>`
    : `<path d="M92,20 Q124,40 128,74" stroke="${K.ol}" stroke-width="30" fill="none" stroke-linecap="round"/><path d="M92,20 Q124,40 128,74" stroke="#FFC94A" stroke-width="18" fill="none" stroke-linecap="round"/>`;
  const q = mood === "q" ? `<text x="120" y="-110" font-size="80" font-weight="900" fill="${K.accent}" stroke="#fff" stroke-width="10" paint-order="stroke">?</text>` : "";
  const wow = mood === "wow" ? sparkle(-120, -110, .8, "#FFD45C") + sparkle(125, -95, .6, "#9CC3FF") : "";
  return `<g transform="translate(${cx},${cy}) scale(${s})">
   ${floorShadow(0, 140, 95, 15)}
   <path d="M-92,20 Q-124,40 -128,74" stroke="${K.ol}" stroke-width="30" fill="none" stroke-linecap="round"/><path d="M-92,20 Q-124,40 -128,74" stroke="#FFC94A" stroke-width="18" fill="none" stroke-linecap="round"/>
   ${armR}
   <ellipse cx="-38" cy="118" rx="30" ry="22" fill="#FFC94A" ${O(6)}/><ellipse cx="38" cy="118" rx="30" ry="22" fill="#FFC94A" ${O(6)}/>
   <path d="M-6,-104 L20,-150 L4,-146 L24,-190 L-20,-132 L-2,-136 Z" fill="#FFE45C" ${O(6)}/>
   <ellipse cx="0" cy="0" rx="112" ry="106" fill="url(#kMascot)" ${O(8)} filter="url(#kShS)"/>
   <ellipse cx="-50" cy="-58" rx="26" ry="14" fill="#fff" opacity=".8" transform="rotate(-30 -50 -58)"/>
   <ellipse cx="-64" cy="26" rx="20" ry="12" fill="#FF8FA8" opacity=".65"/><ellipse cx="64" cy="26" rx="20" ry="12" fill="#FF8FA8" opacity=".65"/>
   ${eye(-36)}${eye(36)}${mouth}${q}${wow}
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
