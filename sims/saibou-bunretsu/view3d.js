// 細胞分裂 3D（上の図と同じ「段階 p」の式で、立体の細胞の中の染色体を動かす）
// 1 = 100px（上の図と同じ比率）。x＝図の左右、y＝図の上下（上が+）、z＝奥行き（模式）。染色体は少し太く・長めに描く
import { THREE, createView } from '../../assets/three/sim3d.js';
const $ = id => document.getElementById(id);
const C = window.__cell;
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const lerp = (a, b, t) => a + (b - a) * t;
const sm = f => { f = clamp(f, 0, 1); return f * f * (3 - 2 * f); };
const S = 0.01, CW = 3.0, CH = 1.84, CD = 1.5, K = 1.25, RAD = 0.032, G = 4.4;
const RED = 0xe11d48, BLUE = 0x2563eb, GREEN = 0x16a34a;
const CHR = [{ len: 36, col: RED }, { len: 36, col: BLUE }, { len: 22, col: RED }, { len: 22, col: BLUE }];
const SC = [[-26, -18, 0.6], [22, -22, -0.9], [-18, 24, 1.9], [26, 16, 0.3]], YY = [-58, 20, -20, 58];
const PAIR = [[-11, -30], [11, -30], [11, 30], [-11, 30]], SIDE = [-1, 1, 1, -1];
// 奥行き（模式）：分裂前はばらばら → ③では中央の「面」に広がって並ぶ（正面からは1列、横からは面に見える）
const Z0 = [0.28, -0.22, 0.05, -0.3], ZM = [0.22, 0.34, -0.34, -0.22], ZP = [0.2, 0.2, -0.2, -0.2];

const ZF = matchMedia('(max-width:640px)').matches ? 0.85 : 1;   // スマホは少し近づける
const v = createView($('view3d'), {
  views: {
    persp: { tgt: [0, 0, 0], dist: 7.4 * ZF, th: 0.5, ph: 0.32 },
    front: { tgt: [0, 0, 0], dist: 7.0 * ZF, th: 0, ph: 0 },
    side: { tgt: [0, 0, 0], dist: 6.4 * ZF, th: Math.PI / 2 - 0.14, ph: 0.14 },
  },
  camRow: '#camRow3d', bg: 0xf1f5f9, shadows: false, minDist: 1.5, maxDist: 20,
});
const { scene } = v;
const SM = v.mobile;
const cellG = new THREE.Group(), kenG = new THREE.Group(); scene.add(cellG, kenG);

// ---- 細胞（植物の細胞なので箱の形） ----
const boxGeo = new THREE.BoxGeometry(1, 1, 1), edgeGeo = new THREE.EdgesGeometry(boxGeo);
function mkCell() {
  const g = new THREE.Group();
  g.add(new THREE.Mesh(boxGeo, new THREE.MeshBasicMaterial({ color: 0xd9f99d, transparent: true, opacity: 0.3, depthWrite: false })));
  g.add(new THREE.LineSegments(edgeGeo, new THREE.LineBasicMaterial({ color: 0x65a30d, transparent: true })));
  cellG.add(g); return g;
}
const cells = [mkCell(), mkCell()];
function setCell(c, x0, x1, a) { c.visible = a > 0.01 && x1 - x0 > 0.01; c.position.set((x0 + x1) / 2, 0, 0); c.scale.set(Math.max(0.001, x1 - x0), CH, CD); c.children[0].material.opacity = 0.3 * a; c.children[1].material.opacity = a; }
// 仕切り（中央にできる）
const plateMat = new THREE.MeshBasicMaterial({ color: 0x84cc16, transparent: true, opacity: 0.6, side: THREE.DoubleSide, depthWrite: false });
const vPlate = new THREE.Mesh(boxGeo, plateMat), hPlates = [new THREE.Mesh(boxGeo, plateMat), new THREE.Mesh(boxGeo, plateMat)];
cellG.add(vPlate, ...hPlates);
const setV = f => { vPlate.visible = f > 0.01; vPlate.scale.set(0.03, CH * Math.max(f, 0.001), CD * Math.max(f, 0.001)); };
const setH = (m, x, f) => { m.visible = f > 0.01; m.position.set(x, 0, 0); m.scale.set(1.5 * Math.max(f, 0.001), 0.03, CD * Math.max(f, 0.001)); };

// ---- 核と、細い糸のように広がった染色体 ----
function prng(seed) { let a = seed >>> 0; return () => { a = (a + 0x6D2B79F5) >>> 0; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
const thrMats = [RED, BLUE, RED, BLUE].map(c => new THREE.MeshStandardMaterial({ color: c, transparent: true, roughness: 0.6 }));
const thrGeos = []; { const r = prng(7); for (let i = 0; i < 4; i++) { const pts = []; let a = r() * 6.28, rad = 0.3 + 0.35 * r(), z = (r() - 0.5) * 0.6;
  for (let j = 0; j < 10; j++) { a += 0.5 + r() * 0.9; rad = clamp(rad + (r() - 0.5) * 0.35, 0.15, 0.72); z = clamp(z + (r() - 0.5) * 0.5, -0.6, 0.6); pts.push(new THREE.Vector3(Math.cos(a) * rad, Math.sin(a) * rad, z * Math.sqrt(Math.max(0, 1 - rad * rad)))); }
  thrGeos.push(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 80, 0.02, 5, false)); } }
const nucMats = [0, 1, 2].map(() => new THREE.MeshStandardMaterial({ color: 0x94a3b8, transparent: true, opacity: 0.3, depthWrite: false, roughness: 0.7 }));
const nucs = nucMats.map(m => { const n = new THREE.Mesh(new THREE.SphereGeometry(1, 32, 20), m); cellG.add(n); return n; });
const thrGs = [0, 1].map(() => { const g = new THREE.Group(); thrGeos.forEach((geo, i) => g.add(new THREE.Mesh(geo, thrMats[i]))); cellG.add(g); return g; });
function nucleus(n, x, r, a) { const m = nucs[n]; m.visible = a > 0.01; m.position.set(x * S, 0, 0); m.scale.setScalar(Math.max(0.001, r * S)); m.material.opacity = 0.3 * a; }
function threads(n, x, r, a) { const g = thrGs[n]; g.visible = a > 0.01; g.position.set(x * S, 0, 0); g.scale.setScalar(Math.max(0.001, r * S)); thrMats.forEach(m => { m.opacity = a; }); }

// ---- 染色体（複製された2本がくっついた X の形／分かれた1本） ----
const geoCache = new Map();
function chromGeo(len, bend) {
  const L = Math.round(len), B = Math.round(bend * 20) / 20, key = L + '|' + B; let g = geoCache.get(key);
  if (!g) { const l = L * S * 0.5 * K, sx = Math.sin(B) * l, cy = Math.cos(B) * l;
    const curve = new THREE.CatmullRomCurve3([new THREE.Vector3(sx, cy, 0), new THREE.Vector3(sx * 0.42, cy * 0.5, 0), new THREE.Vector3(0, 0, 0), new THREE.Vector3(sx * 0.42, -cy * 0.5, 0), new THREE.Vector3(sx, -cy, 0)]);
    g = new THREE.TubeGeometry(curve, 24, RAD, 8, false); geoCache.set(key, g); }
  return g;
}
const mk = c => new THREE.MeshStandardMaterial({ color: c, roughness: 0.45, transparent: true });
const mats = { [RED]: mk(RED), [BLUE]: mk(BLUE) }, matsF = { [RED]: mk(RED), [BLUE]: mk(BLUE), [GREEN]: mk(GREEN) };
const pool = [], dots = [];
for (let i = 0; i < 12; i++) { const m = new THREE.Mesh(chromGeo(36, 0), mats[RED]); cellG.add(m); pool.push(m); }
const dotMat = new THREE.MeshStandardMaterial({ color: 0x334155, transparent: true });
for (let i = 0; i < 4; i++) { const d = new THREE.Mesh(new THREE.SphereGeometry(0.036, 12, 8), dotMat); cellG.add(d); dots.push(d); }
let used = 0, usedDot = 0;
// x, y は上の図と同じ「中心からのずれ（px）」、z は奥行き（3Dの単位）
function chromatid(x, y, z, len, rot, bend, col, a, F) {
  if (a <= 0.01) return; const m = pool[used++]; if (!m) return;
  m.visible = true; m.geometry = chromGeo(len, bend); m.material = (F ? matsF : mats)[col];
  m.position.set(x * S, -y * S, z); m.rotation.set(0, 0, -rot);
}
function xchrom(x, y, z, len, rot, col, a) {
  const c = Math.cos(rot), s = Math.sin(rot);
  chromatid(x - G * c, y - G * s, z, len, rot, -0.35, col, a); chromatid(x + G * c, y + G * s, z, len, rot, 0.35, col, a);
  if (a > 0.3) { const d = dots[usedDot++]; if (d) { d.visible = true; d.position.set(x * S, -y * S, z); } }
}

// ---- 減数分裂のあと：受精 ----
const egg = new THREE.Mesh(new THREE.SphereGeometry(0.7, 40, 24), new THREE.MeshStandardMaterial({ color: 0xfdba74, transparent: true, opacity: 0.3, depthWrite: false, roughness: 0.7 }));
const spermHead = new THREE.Mesh(new THREE.SphereGeometry(1, 24, 16), new THREE.MeshStandardMaterial({ color: 0xbef264, transparent: true, roughness: 0.6 }));
spermHead.scale.set(0.17, 0.12, 0.12);
const tailPos = new Float32Array(26 * 3), tail = new THREE.Line(new THREE.BufferGeometry(), new THREE.LineBasicMaterial({ color: 0x4d7c0f, transparent: true }));
tail.geometry.setAttribute('position', new THREE.BufferAttribute(tailPos, 3));
cellG.add(egg, spermHead, tail);

// ---- 顕微鏡モード：タマネギの根の先端（半分に切った模式。先端ほど細胞が小さく、根元ほど長い） ----
const RW = 0.12, YTIP = -1.5, YTOP = 1.8, NCOL = 5, NLAY = 2;
const rowH = y => RW * (1 + 3 * clamp((y - YTIP) / 2.9, 0, 1));   // A≒1、B≒2倍、C≒4倍（上の表と同じ目安）
const zoneY = L => -((L.y0 + L.y1) / 2 - 244) * S;
{
  const seg = [], nucP = [], divP = [], R = prng(5);
  let y = YTIP;
  while (y < YTOP - 0.05) {
    const h = Math.min(rowH(y), YTOP - y), rate = y < -0.85 ? 0.22 : (y < 0.25 ? 0.05 : 0);
    for (let c = 0; c < NCOL; c++) for (let l = 0; l < NLAY; l++) {
      const x0 = (c - NCOL / 2) * RW, z0 = -l * RW - RW, x1 = x0 + RW, z1 = z0 + RW, y1 = y + h;
      [[x0, y, z1, x1, y, z1], [x0, y1, z1, x1, y1, z1], [x0, y, z1, x0, y1, z1], [x1, y, z1, x1, y1, z1], [x0, y1, z0, x1, y1, z0], [x0, y1, z0, x0, y1, z1], [x1, y1, z0, x1, y1, z1]].forEach(s => seg.push(...s));
      const cx = x0 + RW / 2, cy = y + h / 2, cz = z0 + RW / 2;
      if (R() < rate) divP.push([cx, cy, cz, Math.floor(R() * 3)]); else nucP.push([cx, cy, cz]);
    }
    y += h;
  }
  const lg = new THREE.BufferGeometry(); lg.setAttribute('position', new THREE.Float32BufferAttribute(seg, 3));
  kenG.add(new THREE.LineSegments(lg, new THREE.LineBasicMaterial({ color: 0xc084a8, transparent: true, opacity: 0.75 })));
  const nm = new THREE.InstancedMesh(new THREE.SphereGeometry(0.026, 12, 8), new THREE.MeshStandardMaterial({ color: 0xbe185d, roughness: 0.6 }), nucP.length);
  const M = new THREE.Matrix4(); nucP.forEach((p, i) => { M.makeTranslation(p[0], p[1], p[2]); nm.setMatrixAt(i, M); }); kenG.add(nm);
  // 分裂中の細胞：染色体が見える／中央に並ぶ／両端へ分かれる（濃い紫）
  const bars = []; divP.forEach(p => { if (p[3] === 0) { for (let k = 0; k < 4; k++) bars.push([p[0] + (k % 2 - 0.5) * 0.04, p[1] + (k < 2 ? -0.02 : 0.02), p[2], 0.015, 0.035]); }
    else if (p[3] === 1) bars.push([p[0], p[1], p[2], 0.085, 0.022]); else { bars.push([p[0], p[1] - 0.035, p[2], 0.08, 0.018]); bars.push([p[0], p[1] + 0.035, p[2], 0.08, 0.018]); } });
  const bm = new THREE.InstancedMesh(new THREE.BoxGeometry(1, 1, 1), new THREE.MeshStandardMaterial({ color: 0x701a75, roughness: 0.5 }), bars.length);
  const q = new THREE.Quaternion(), sc = new THREE.Vector3(), ps = new THREE.Vector3();
  bars.forEach((b, i) => { M.compose(ps.set(b[0], b[1], b[2]), q, sc.set(b[3], b[4], b[3] * 0.8)); bm.setMatrixAt(i, M); }); kenG.add(bm);
  // 根の皮（半分に切った筒）と根冠
  const skin = new THREE.Mesh(new THREE.CylinderGeometry(0.4, 0.4, YTOP - YTIP, 40, 1, true, Math.PI / 2, Math.PI), new THREE.MeshStandardMaterial({ color: 0xfef3c7, transparent: true, opacity: 0.45, side: THREE.DoubleSide, depthWrite: false }));
  skin.position.y = (YTOP + YTIP) / 2; kenG.add(skin);
  const cap = new THREE.Mesh(new THREE.SphereGeometry(0.4, 40, 16, Math.PI / 2, Math.PI, Math.PI / 2, Math.PI / 2), new THREE.MeshStandardMaterial({ color: 0xfcd34d, transparent: true, opacity: 0.55, side: THREE.DoubleSide, depthWrite: false }));
  cap.scale.y = 0.8; cap.position.y = YTIP; kenG.add(cap);
}
const zoneMat = new THREE.MeshBasicMaterial({ color: 0x0e7490, transparent: true, opacity: 0.12, depthWrite: false });
const zones = C.LOCS.map(L => { const h = Math.abs(L.y1 - L.y0) * S, g = new THREE.Group();
  g.add(new THREE.Mesh(boxGeo, zoneMat)); g.add(new THREE.LineSegments(edgeGeo, new THREE.LineBasicMaterial({ color: 0x0e7490 })));
  g.position.set(0, zoneY(L), -0.2); g.scale.set(0.9, h, 0.5); kenG.add(g); return g; });

// ---- 文字 ----
const lNuc = v.label('核', [0, 0, 0]), lChr = v.label('染色体', [0, 0, 0]), lPlate = v.label('仕切り', [0, 0, 0], { sub: true });
const lCnt = [0, 1, 2, 3].map(() => v.label('4本', [0, 0, 0], { accent: true }));
const lEgg = v.label('卵：2本', [0, 0, 0]), lSp = v.label('精子：2本', [0, 0, 0]), lZy = v.label('受精卵：4本', [0, 0, 0], { accent: true });
const zNames = SM ? ['A 先端付近', 'B 少し上', 'C 根元に近い'] : ['A 根の先端付近（成長点）', 'B 先端から少し上', 'C 根元に近いところ'];
const lZone = C.LOCS.map((L, i) => v.label(zNames[i], [0.62, zoneY(L) + 0.1, 0]));
const lCap = v.label('根冠', [0.5, YTIP - 0.25, 0], { sub: true }), lUp = v.label('↑ 根元のほう', [0, YTOP + 0.12, -0.2], { sub: true });
const hud = $('hud3d'); hud.style.display = '';
if (SM) { hud.style.fontSize = '11px'; hud.style.padding = '3px 6px'; hud.style.left = hud.style.top = '6px'; }

// ---- 体細胞分裂（上の図の drawTai と同じ動き） ----
function tai(p) {
  const k = Math.min(5, Math.floor(p)), e = sm(p - k), out = { nuc: null, chr: null, plate: 0, cnt: [] };
  let wd = CW / 2;
  if (p < 5) { setCell(cells[0], -CW / 2, CW / 2, 1); setCell(cells[1], 0, 0, 0); out.plate = k < 3 ? 0 : (k === 3 ? e * 0.6 : lerp(0.6, 1, e)); }
  else { wd = lerp(CW / 2, CW * 0.92, e); setCell(cells[0], -wd, 0, 1); setCell(cells[1], 0, wd, 1); }
  setV(out.plate); setH(hPlates[0], 0, 0); setH(hPlates[1], 0, 0);
  nucleus(0, 0, 0, 0); nucleus(1, 0, 0, 0); nucleus(2, 0, 0, 0); threads(0, 0, 0, 0); threads(1, 0, 0, 0);
  if (k === 0) { nucleus(0, 0, 62, 1 - e); threads(0, 0, 62, 1 - e); if (e < 0.5) out.nuc = [0, 0.62]; }
  if (k === 3) { nucleus(0, -75, 44, e * 0.7); nucleus(1, 75, 44, e * 0.7); }
  if (k === 4) { nucleus(0, -75, 44, lerp(0.7, 1, e)); nucleus(1, 75, 44, lerp(0.7, 1, e)); threads(0, -75, 44, e); threads(1, 75, 44, e); if (e > 0.5) out.nuc = [-0.75, 0.44]; }
  if (k === 5) { const r = lerp(44, 52, e); nucleus(0, -wd * 50, r, 1); nucleus(1, wd * 50, r, 1); threads(0, -wd * 50, r, 1); threads(1, wd * 50, r, 1); out.nuc = [-wd / 2, r * S]; }
  const a = k === 0 ? e : (k === 4 ? 1 - e : 1); mats[RED].opacity = mats[BLUE].opacity = a; dotMat.opacity = 1;
  for (let i = 0; i < 4; i++) { const c = CHR[i];
    if (k === 0) xchrom(SC[i][0], SC[i][1], Z0[i], c.len * (1.6 - 0.6 * e), SC[i][2], c.col, e);
    else if (k === 1) xchrom(lerp(SC[i][0], 0, e), lerp(SC[i][1], YY[i], e), lerp(Z0[i], ZM[i], e), c.len, lerp(SC[i][2], 0, e), c.col, 1);
    else if (k <= 4) for (let s = 0; s < 2; s++) { const dir = s ? 1 : -1, rot = s ? Math.PI : 0; let x, y, z, b;
      if (k === 2) { x = lerp(dir * G, dir * 100, e); y = YY[i] * lerp(1, 0.75, e); z = ZM[i] * lerp(1, 0.75, e); b = lerp(-0.35, 0.9, e); if (e < 0.08 && s === 0) { const d = dots[usedDot++]; if (d) { d.visible = true; d.position.set(0, -y * S, z); } } }
      else if (k === 3) { x = lerp(dir * 100, dir * 75, e); y = YY[i] * lerp(0.75, 0.45, e); z = ZM[i] * lerp(0.75, 0.45, e); b = lerp(0.9, 0.5, e); }
      else { x = dir * 75; y = YY[i] * 0.45; z = ZM[i] * 0.45; b = 0.5; }
      chromatid(x, y, z, c.len, rot, b, c.col, a); }
  }
  if (a > 0.5 && k <= 3) out.chr = pool[0].position;
  // 本数のバッジは細胞の外側の角に（染色体の名前と重ならないように）
  if (p >= 2.5 && p < 5) out.cnt = [[-CW / 2 + 0.3, '4本'], [CW / 2 - 0.3, '4本']];
  else if (p >= 5) out.cnt = [[-wd + 0.3, '4本'], [wd - 0.3, '4本']];
  else out.cnt = [[-CW / 2 + 0.3, '4本']];
  out.cnt = out.cnt.map(c => [c[0], CH / 2 + 0.12, c[1]]);
  return out;
}

// ---- 減数分裂と受精（上の図の drawGen・drawFert と同じ動き） ----
function gen(p) {
  const k = Math.min(4, Math.floor(p)), e = sm(p - k), u = clamp(p - 4, 0, 1), out = { nuc: null, chr: null, plate: 0, cnt: [] };
  const aC = k < 4 ? 1 : 1 - sm(u / 0.35);
  setCell(cells[0], -CW / 2, CW / 2, aC); setCell(cells[1], 0, 0, 0);
  plateMat.opacity = 0.8 * aC;
  out.plate = (k < 2 ? 0 : (k === 2 ? e : 1)) * (aC > 0.01 ? 1 : 0); setV(out.plate);
  const hp = (k < 3 ? 0 : (k === 3 ? e : 1)) * (aC > 0.01 ? 1 : 0); setH(hPlates[0], -0.75, hp); setH(hPlates[1], 0.75, hp);
  nucleus(0, 0, 0, 0); nucleus(1, 0, 0, 0); nucleus(2, 0, 0, 0); threads(0, 0, 0, 0); threads(1, 0, 0, 0);
  if (k === 0) { nucleus(0, 0, 62, 1 - e); threads(0, 0, 62, 1 - e); if (e < 0.5) out.nuc = [0, 0.62]; }
  const a = (k === 0 ? e : 1) * aC; mats[RED].opacity = mats[BLUE].opacity = a; dotMat.opacity = aC;
  if (aC > 0.01) for (let i = 0; i < 4; i++) { const c = CHR[i], sd = SIDE[i], yq = i < 2 ? -16 : 16;
    if (k === 0) xchrom(lerp(SC[i][0], PAIR[i][0], e), lerp(SC[i][1], PAIR[i][1], e), lerp(Z0[i], ZP[i], e), c.len * (1.6 - 0.6 * e), lerp(SC[i][2], 0, e), c.col, e);
    else if (k === 1) xchrom(lerp(PAIR[i][0], sd * 100, e), PAIR[i][1] * lerp(1, 0.8, e), ZP[i] * lerp(1, 0.8, e), c.len, 0, c.col, a);
    else if (k === 2) xchrom(lerp(sd * 100, sd * 75, e), lerp(PAIR[i][1] * 0.8, yq, e), ZP[i] * 0.8, c.len, lerp(0, Math.PI / 2, e), c.col, a);
    else for (let s = 0; s < 2; s++) { const dir = s ? 1 : -1, x = sd * 75, y0 = yq + dir * G, y1 = dir * CH * 25 + (i < 2 ? -8 : 8), ee = k === 3 ? e : 1;
      chromatid(x, lerp(y0, y1, ee), ZP[i] * 0.8, c.len, s ? -Math.PI / 2 : Math.PI / 2, k === 3 ? 0.7 * Math.sin(Math.PI * e) : 0, c.col, a); }
  }
  if (a > 0.5) out.chr = pool[0].position;
  if (aC > 0.5) {
    if (p >= 2.5 && p < 3.5) out.cnt = [[-CW / 2 + 0.3, CH / 2 + 0.12, '2本'], [CW / 2 - 0.3, CH / 2 + 0.12, '2本']];
    else if (p >= 3.5) out.cnt = [[-1.23, CH / 4, '2本'], [1.23, CH / 4, '2本'], [-1.23, -CH / 4, '2本'], [1.23, -CH / 4, '2本']];
    else out.cnt = [[-CW / 2 + 0.3, CH / 2 + 0.12, '4本']];
  }
  // 受精
  const a1 = k === 4 ? sm(u / 0.35) : 0, mv = sm((u - 0.35) / 0.45), e3 = sm((u - 0.8) / 0.2), EX = -50, sx = lerp(190, EX + 78, mv);
  egg.visible = spermHead.visible = tail.visible = a1 > 0.01; out.fert = null;
  if (a1 > 0.01) {
    egg.position.set(EX * S, 0, 0); egg.material.opacity = 0.3 * a1;
    nucleus(2, EX, lerp(30, 42, e3), a1);
    matsF[RED].opacity = matsF[BLUE].opacity = matsF[GREEN].opacity = a1;
    chromatid(lerp(EX - 8, EX - 18, e3), 0, 0.02, 36, 0, 0, RED, a1, true); chromatid(lerp(EX + 8, EX + 6, e3), 0, -0.02, 22, 0, 0, BLUE, a1, true);
    const as = a1 * (1 - e3); spermHead.material.opacity = as; tail.material.opacity = as; spermHead.visible = tail.visible = as > 0.01;
    spermHead.position.set(sx * S, 0, 0);
    for (let i = 0; i <= 25; i++) { const w = i * 0.8 + u * 30; tailPos.set([(sx + 16 + i * 3) * S, Math.sin(w) * 4 * S, Math.cos(w) * 3 * S], i * 3); }
    tail.geometry.attributes.position.needsUpdate = true;
    chromatid(lerp(sx - 5, EX - 6, e3), 0, 0.02, lerp(20, 36, e3), 0, 0, GREEN, a1, true); chromatid(lerp(sx + 5, EX + 18, e3), 0, -0.02, lerp(13, 22, e3), 0, 0, GREEN, a1, true);
    out.fert = { a1, e3, EX: EX * S, sx: sx * S };
  }
  return out;
}

// ---- 毎フレーム ----
let lastMode = '', lastLoc = -1;
v.onFrame(() => {
  const st = C.st(), mode = st.mode, ken = mode === 'ken';
  if (mode !== lastMode) { if (lastMode) v.setView('persp'); if (mode === 'ken') { v.goal.tgt.set(0, 0.15, -0.1); v.goal.dist = 7.2 * ZF; v.goal.th = 0.45; v.goal.ph = 0.16; } lastMode = mode; lastLoc = -1; }
  cellG.visible = !ken; kenG.visible = ken;
  [lNuc, lChr, lPlate, lEgg, lSp, lZy, ...lCnt].forEach(l => { l.show = false; });
  lZone.forEach(l => { l.show = false; }); lCap.show = lUp.show = false;
  if (ken) {
    if (st.loc !== lastLoc) { if (lastLoc >= 0) { v.goal.tgt.set(0, zoneY(C.LOCS[st.loc]), -0.1); v.goal.dist = 3.4; } lastLoc = st.loc; }   // 場所を変えたら、その場所に近づく
    zones.forEach((z, i) => { z.visible = i === st.loc; });
    lZone.forEach((l, i) => { l.show = true; l.el.classList.toggle('acc', i === st.loc); }); lCap.show = lUp.show = true;
    const L = C.LOCS[st.loc], cs = C.CELLS[st.loc]; let tot = 0, dv = 0; cs.forEach(c => { if (c.inn) { tot++; if (c.st > 0) dv++; } });
    hud.innerHTML = SM ? '<b>' + L.s + '</b>・分裂中 ' + dv + '／' + tot + '個・長さ ' + L.len : '<b>' + L.name + '</b><br>上の視野で分裂中の細胞 <b>' + dv + '</b>個／' + tot + '個・細胞の長さ ' + L.len
      + (SM ? '' : '<br><span style="font-size:11px;color:#64748b">根を縦に半分に切った模式図。濃い紫＝分裂中の細胞</span>');
    return;
  }
  used = 0; usedDot = 0;
  const o = mode === 'gen' ? gen(st.p) : tai(st.p);
  if (mode !== 'gen') { egg.visible = spermHead.visible = tail.visible = false; plateMat.opacity = 0.8; }
  for (let i = used; i < pool.length; i++) pool[i].visible = false;
  for (let i = usedDot; i < dots.length; i++) dots[i].visible = false;
  // 文字
  if (o.nuc) { lNuc.at(o.nuc[0], o.nuc[1] + 0.06, 0); lNuc.show = true; }
  if (o.chr) { lChr.at(o.chr.x, o.chr.y + 0.32, o.chr.z); lChr.show = true; }
  if (o.plate > 0.3) { lPlate.at(0, -CH * o.plate / 2 - 0.05, 0); lPlate.show = true; }
  if (!(SM && (o.cnt || []).length > 2)) (o.cnt || []).forEach((c, i) => {   // スマホで4つ並ぶときは、上の表示（本数）だけにする
    const l = lCnt[i]; l.set(c[2]); l.at(c[0], c[1], CD / 2); l.show = true; });
  if (o.fert) { const f = o.fert;
    if (f.e3 < 0.5) { lEgg.at(f.EX, 0.78, 0); lEgg.show = true; lSp.at(f.sx + 0.3, 0.2, 0); lSp.show = f.sx > f.EX + 0.9; }
    else { lZy.at(f.EX, 0.78, 0); lZy.show = true; } }
  const L = mode === 'gen' ? C.GEN : C.TAI, it = L[Math.round(st.p)], chN = mode === 'gen' ? it.ch : 4;
  hud.innerHTML = SM ? '<b>' + it.s + '</b>・染色体' + chN + '本・細胞' + it.k + '個' : '<b>' + it.s + '</b>　1つの細胞の染色体 <b>' + chN + '</b>本・細胞 ' + it.k + '個'
    + (SM ? '' : ((mode === 'tai' && Math.round(st.p) === 2) || (mode === 'gen' && Math.round(st.p) === 1) ? '<br>「横から」で見ると、染色体が中央の面に広がって並んでいます' : '')
      + '<br><span style="font-size:11px;color:#64748b">立体の模式図（染色体は4本・少し太く描いています）</span>');
});
