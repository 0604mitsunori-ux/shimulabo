// 人の体のつくりと働き 3D（上の図の①血液の循環・②呼吸・③消化と吸収を、体の中の立体の模式図にする）
// 上の図の状態（心臓の拍動・血液の粒・呼吸のリズム・食べ物の位置）をそのまま読んで動かす。体の正面が手前（＋z）、図の左＝体の右（−x）
import { THREE, createView } from '../../assets/three/sim3d.js';
const $ = id => document.getElementById(id);
const B = window.__body;
const PI = Math.PI;
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const lerp = (a, b, f) => a + (b - a) * f;
const bump = (p, a, b) => (p >= a && p <= b) ? Math.sin(PI * (p - a) / (b - a)) : 0;
const P3 = (a) => a.isVector3 ? a.clone() : new THREE.Vector3(a[0], a[1], a[2]);
const cv = (pts) => new THREE.CatmullRomCurve3(pts.map(P3), false, 'centripetal');

const v = createView($('view3d'), {
  views: { persp: { tgt: [0, 0, 0], dist: 20, th: 0.42, ph: 0.14 }, front: { tgt: [0, 0, 0], dist: 20, th: 0, ph: 0.04 }, side: { tgt: [0, 0, 0], dist: 20, th: PI / 2 - 0.06, ph: 0.08 } },
  camRow: '#camRow3d', bg: 0xf8fafc, shadows: false, minDist: 4, maxDist: 70,
});
const { scene } = v;
const SM = v.mobile;
// スマホは枠が正方形に近いので、場面ごとに近づける（m）
// 場面ごとのカメラ（注視点・距離＝ななめ／正面／横）
const CAM = { J: { tgt: [0, 0.4, 0], d: [27, 26, 25], m: 0.86 }, K: { tgt: [3.4, 1.9, 0], d: [20, 19, 17], m: 0.8 }, S: { tgt: [2.0, 0.6, 0], d: [27, 26, 24], m: 0.86 } };

// ---- 道具 ----
const sphGeo = new THREE.SphereGeometry(1, 28, 18), dotGeo = new THREE.SphereGeometry(1, 12, 8), cylGeo = new THREE.CylinderGeometry(1, 1, 1, 14);
const std = (c, o) => new THREE.MeshStandardMaterial(Object.assign({ color: c, roughness: 0.6 }, o || {}));
const glass = (c, op, o) => new THREE.MeshStandardMaterial(Object.assign({ color: c, roughness: 0.5, transparent: true, opacity: op, depthWrite: false }, o || {}));
function ell(c, r, mat, parent) { const m = new THREE.Mesh(sphGeo, mat); m.scale.set(r[0], r[1], r[2]); m.position.set(c[0], c[1], c[2]); parent.add(m); return m; }
function tubeC(curve, r, mat, parent, segs) { const m = new THREE.Mesh(new THREE.TubeGeometry(curve, segs || 64, r, 10, false), mat); parent.add(m); return m; }
const tube = (pts, r, mat, parent, segs) => tubeC(cv(pts), r, mat, parent, segs);
// 色が場所で変わる管（fn(u)＝0〜1 で c0→c1）
function tubeGrad(curve, r, c0, c1, fn, parent, op, segs) {
  const T = segs || 80, g = new THREE.TubeGeometry(curve, T, r, 10, false), n = g.attributes.position.count, cols = new Float32Array(n * 3), a = new THREE.Color(c0), b = new THREE.Color(c1), c = new THREE.Color();
  for (let i = 0; i <= T; i++) { c.copy(a).lerp(b, clamp(fn(i / T), 0, 1)); for (let j = 0; j <= 10; j++) { const k = (i * 11 + j) * 3; cols[k] = c.r; cols[k + 1] = c.g; cols[k + 2] = c.b; } }
  g.setAttribute('color', new THREE.BufferAttribute(cols, 3));
  const m = new THREE.Mesh(g, op ? glass(0xffffff, op, { vertexColors: true }) : std(0xffffff, { vertexColors: true })); parent.add(m); return m;
}
// 毛細血管らしい細かいうねり
function wig(pts, amp, N) {
  const c = cv(pts), out = []; N = N || 64;
  for (let i = 0; i <= N; i++) { const u = i / N, p = c.getPointAt(u), w = amp * Math.sin(u * N * 0.95) * Math.sin(PI * u); p.x += w * 0.7; p.y += w; p.z += w * 0.6 * Math.cos(u * N * 0.7); out.push(p); }
  return cv(out);
}
function inst(geo, mat, n) { const m = new THREE.InstancedMesh(geo, mat, n); m.instanceMatrix.setUsage(THREE.DynamicDrawUsage); m.frustumCulled = false; return m; }
const M4 = new THREE.Matrix4(), Q0 = new THREE.Quaternion(), S3 = new THREE.Vector3(), C3 = new THREE.Color();
function putAt(m, i, p, r) { S3.set(r, r, r); M4.compose(p, Q0, S3); m.setMatrixAt(i, M4); }
function hideFrom(m, i, n) { S3.set(0, 0, 0); for (; i < n; i++) { M4.compose(new THREE.Vector3(0, -99, 0), Q0, S3); m.setMatrixAt(i, M4); } m.instanceMatrix.needsUpdate = true; }
const BLUE = new THREE.Color(37 / 255, 99 / 255, 235 / 255), RED = new THREE.Color(220 / 255, 38 / 255, 38 / 255);
function bloodCol(f) { return C3.copy(BLUE).lerp(RED, clamp(f, 0, 1)); }
// 体の輪郭（うすい皮ふ色）
const skin = glass(0xfdba74, 0.07);
function bodyShell(parent, o) {
  if (o.head) { ell([0, o.head[0], 0], [o.head[1], o.head[1] * 1.12, o.head[1]], skin, parent); const nk = new THREE.Mesh(cylGeo, skin); nk.scale.set(0.5, o.head[0] - o.head[1] - o.torso[0] - o.torso[2] / 2 - o.torso[1] + 0.9, 0.45); nk.position.set(0, (o.head[0] - o.head[1] + o.torso[0] + o.torso[2] / 2 + o.torso[1] - 0.6) / 2, 0); parent.add(nk); }
  const t = new THREE.Mesh(new THREE.CapsuleGeometry(o.torso[1], o.torso[2], 8, 28), skin); t.scale.z = 0.52; t.position.y = o.torso[0]; parent.add(t);
  if (o.legs) [-1, 1].forEach(s => { const l = new THREE.Mesh(new THREE.CapsuleGeometry(0.75, 2.6, 6, 16), skin); l.position.set(s * 0.95, o.legs, 0); parent.add(l); });
}
const G = { J: new THREE.Group(), K: new THREE.Group(), S: new THREE.Group() };
Object.values(G).forEach(g => { g.visible = false; scene.add(g); });
const L = {};
const lab = (k, t, o) => { const l = v.label(t, [0, 0, 0], o || {}); l.show = false; (L[k] = L[k] || []).push(l); return l; };
const s6t = (s6, a, b) => (s6 ? a : b);

// ================= ① 血液の循環 =================
const GJ = G.J, VEN = 0x93c5fd, ART = 0xfca5a5;
bodyShell(GJ, { head: [5.4, 1.1], torso: [-0.6, 2.5, 4.4], legs: -6.6 });
const RAc = [-0.85, 0.95, 0.15], RVc = [-0.4, -0.25, 0.45], LAc = [0.75, 1.05, -0.35], LVc = [0.55, -0.35, 0.05], AV = [0.2, 0.85, 0.35];
const RAr = [0.55, 0.55, 0.5], RVr = [0.68, 0.78, 0.58], LAr = [0.55, 0.5, 0.5], LVr = [0.78, 0.88, 0.68];
const mRA = ell(RAc, RAr, glass(0x60a5fa, 0.45), GJ), mRV = ell(RVc, RVr, glass(0x60a5fa, 0.45), GJ), mLA = ell(LAc, LAr, glass(0xf87171, 0.45), GJ), mLV = ell(LVc, LVr, glass(0xef4444, 0.5), GJ);
[-1, 1].forEach(s => ell([s * 2.1, 2.4, -0.2], [1.2, 1.8, 1.1], glass(0xf9a8d4, 0.2), GJ));
ell([-1.5, -1.6, 0.35], [1.25, 0.6, 0.8], glass(0xc2410c, 0.28), GJ);   // 肝臓
ell([0.1, -3.05, 0.55], [1.3, 0.75, 0.6], glass(0xfacc15, 0.22), GJ);    // 小腸
[-1, 1].forEach(s => ell([s * 1.38, -2.32, -1.0], [0.36, 0.6, 0.3], glass(0x8b5cf6, 0.4), GJ));   // 腎臓
// 血液の通り道（上の図の道すじと、区切り＝毛細血管の始まりと終わりをそろえる）
const H1P = [0, 1, 2, 3].map(k => {
  const sx = k % 2 === 0 ? -1 : 1, q = 0.35 + 0.22 * k;
  const pre = [RAc, [-0.75, 0.35, 0.4], RVc, [-0.05, 0.35, 0.7], [0.0, 1.55, 0.55], [sx * 0.45, 2.0, 0.3], [sx * 1.05, 2.25, 0.1]];
  const bed = [[sx * 1.05, 2.25, 0.1], [sx * (1.3 + 0.2 * q), 2.6 + 0.6 * q, 0.4], [sx * (1.7 + 0.4 * q), 3.0 + 1.0 * q, 0.25], [sx * (2.3 + 0.5 * q), 2.9 + 0.7 * q, -0.1], [sx * (2.4 + 0.5 * q), 2.2 + 0.2 * q, -0.4], [sx * (1.8 + 0.2 * q), 1.7, -0.55], [sx * 1.15, 1.85, -0.5]];
  const post = [[sx * 1.15, 1.85, -0.5], sx < 0 ? [-0.3, 1.45, -0.75] : [0.95, 1.45, -0.55], LAc, [0.7, 0.4, -0.1], LVc, [0.3, 0.25, 0.3], AV];
  return { sx, pre, bed, post, cPre: cv(pre), cBed: wig(bed, 0.05), cPost: cv(post) };
});
const A0 = [AV, [0.15, 1.6, 0.35], [0.2, 2.2, 0.0]], DESC = A0.concat([[0.45, 2.05, -0.6], [0.5, 1.2, -0.95]]), IVC = [[-0.6, -0.6, -0.5], [-0.75, 0.4, -0.1], RAc];
function lane(k, s) {
  let pre, bed, post;
  if (k === 0) { pre = A0.concat([[0.3, 3.4, 0.0], [0.35, 4.5, 0.1], [0.5, 4.8, 0.2]]); bed = [[0.5, 4.8, 0.2], [0.75, 5.4, 0.3], [0.3, 6.0, 0.4], [-0.3, 6.0, 0.3], [-0.75, 5.4, 0.2], [-0.5, 4.8, 0.1]]; post = [[-0.5, 4.8, 0.1], [-0.45, 4.0, 0.0], [-0.6, 3.0, 0.0], [-0.85, 2.0, 0.1], [-0.85, 1.5, 0.15], RAc]; }
  else if (k === 1) { pre = DESC.concat([[0.5, -1.0, -0.95], [0.45, -2.0, -0.7], [0.6, -2.6, 0.2], [0.9, -2.9, 0.6]]); bed = [[0.9, -2.9, 0.6], [0.5, -3.4, 0.75], [0.0, -2.8, 0.8], [-0.4, -3.4, 0.7], [-0.7, -2.8, 0.6], [-0.9, -2.2, 0.45], [-1.3, -1.6, 0.5], [-1.9, -1.4, 0.4], [-1.5, -1.2, 0.1]]; post = [[-1.5, -1.2, 0.1], [-0.9, -1.0, -0.4]].concat(IVC); }
  else if (k === 2) { pre = DESC.concat([[0.5, -1.6, -0.95], [s * 0.9, -2.05, -1.0], [s * 1.15, -2.0, -1.0]]); bed = [[s * 1.15, -2.0, -1.0], [s * 1.5, -1.85, -1.05], [s * 1.62, -2.35, -1.0], [s * 1.48, -2.8, -0.95], [s * 1.15, -2.6, -0.9]]; post = [[s * 1.15, -2.6, -0.9]].concat(s > 0 ? [[0.35, -2.55, -0.85]] : [], [[-0.6, -2.45, -0.8]], IVC); }
  else { pre = DESC.concat([[0.5, -1.0, -0.95], [0.5, -3.6, -0.8], [0.2, -4.4, -0.5], [s * 0.9, -5.4, -0.1], [s * 0.95, -6.3, 0.1]]); bed = [[s * 0.95, -6.3, 0.1], [s * 1.25, -6.9, 0.2], [s * 0.95, -7.6, 0.3], [s * 0.65, -6.9, 0.2], [s * 0.85, -6.3, -0.1]]; post = [[s * 0.85, -6.3, -0.1], [s * 0.75, -5.4, -0.35], [-0.3, -4.4, -0.6], [-0.6, -3.0, -0.7]].concat(IVC); }
  return { pre, bed, post, cPre: cv(pre), cBed: wig(bed, k === 1 ? 0.04 : 0.05), cPost: cv(post) };
}
const H2P = [[lane(0, 1)], [lane(1, 1)], [lane(2, -1), lane(2, 1)], [lane(3, -1), lane(3, 1)]];
// 血管（動脈＝赤・静脈＝青。肺動脈は静脈血なので青、肺静脈は赤）と毛細血管（色が変わる）
const vMat = { a: std(ART, { roughness: 0.45 }), v: std(VEN, { roughness: 0.45 }) };
H1P.slice(0, 2).forEach(p => { tube(p.pre.slice(3), 0.085, vMat.v, GJ); tube(p.post.slice(0, 3), 0.085, vMat.a, GJ); });
H1P.forEach(p => tubeGrad(p.cBed, 0.032, VEN, ART, u => u * 1.7, GJ));
H2P.forEach(ls => ls.forEach(p => { tube(p.pre, 0.085, vMat.a, GJ); tube(p.post.slice(0, -1), 0.085, vMat.v, GJ); tubeGrad(p.cBed, 0.032, ART, VEN, u => u * 1.5, GJ); }));
// 血液の粒（上の図の100粒をそのまま。黄色＝養分、灰色＝不要な物）
const NP = B.parts.length;
const bDots = inst(dotGeo, std(0xffffff, { roughness: 0.35 }), NP), nDots = inst(dotGeo, std(0xeab308), NP), wDots = inst(dotGeo, std(0x6b7280), NP);
GJ.add(bDots, nDots, wDots);
const tmpV = new THREE.Vector3();
function posJ(p, i, out) {
  const P = p.h ? B.H2[p.k] : B.H1[p.k], a0 = p.h ? P.c0 : P.o0, a1 = p.h ? P.c1 : P.o1;
  const C = p.h ? H2P[p.k][(p.k >= 2) ? (i & 1) : 0] : H1P[p.k];
  if (p.d < a0) return C.cPre.getPointAt(clamp(p.d / a0, 0, 1), out);
  if (p.d < a1) return C.cBed.getPointAt(clamp((p.d - a0) / (a1 - a0), 0, 1), out);
  return C.cPost.getPointAt(clamp((p.d - a1) / (P.len - a1), 0, 1), out);
}
const lJ = {
  heart: lab('J', '心臓', { accent: true }), lung: lab('J', '肺'), head: lab('J', '脳など'), liver: lab('J', ''), si: lab('J', '小腸'), kid: lab('J', ''), leg: lab('J', 'あし など'),
  ao: lab('J', '', { sub: true }), vc: lab('J', '', { sub: true }), pa: lab('J', '', { sub: true }), pv: lab('J', '', { sub: true }),
  ra: lab('J', '右心房', { sub: true }), rv: lab('J', '右心室', { sub: true }), la: lab('J', '左心房', { sub: true }), lv: lab('J', '左心室', { sub: true }),
};
function frameJ(st) {
  const ph = st.cph % 1, aS = 1 - 0.07 * bump(ph, 0, 0.13), vS = 1 - 0.08 * bump(ph, 0.15, 0.5), s6 = st.s6;
  [[mRA, RAr, aS], [mLA, LAr, aS], [mRV, RVr, vS], [mLV, LVr, vS]].forEach(([m, r, s]) => m.scale.set(r[0] * s, r[1] * s, r[2] * s));
  const parts = B.parts;
  for (let i = 0; i < NP; i++) {
    const p = parts[i]; posJ(p, i, tmpV);
    putAt(bDots, i, tmpV, 0.1); bDots.setColorAt(i, bloodCol(B.oxy(p)));
    tmpV.y += 0.1; tmpV.x += 0.08; putAt(nDots, i, tmpV, p.nut ? 0.055 : 0); tmpV.x -= 0.16; putAt(wDots, i, tmpV, p.ws ? 0.055 : 0);
  }
  bDots.instanceMatrix.needsUpdate = true; bDots.instanceColor.needsUpdate = true; nDots.instanceMatrix.needsUpdate = true; wDots.instanceMatrix.needsUpdate = true;
  lJ.heart.at(0.1, -1.35, 0.7); lJ.lung.at(-2.1, 4.35, 0); lJ.head.at(1.45, 5.5, 0);
  lJ.liver.set(s6t(s6, 'かん臓', '肝臓')); lJ.liver.at(-2.15, -1.55, 0.6); lJ.si.at(0.9, -3.95, 0.7); lJ.kid.set(s6t(s6, 'じん臓', '腎臓')); lJ.kid.at(1.55, -1.6, -1.0); lJ.leg.at(0.95, -7.95, 0.3);
  lJ.ao.set(s6t(s6, '全身へ', '大動脈')); lJ.ao.at(0.75, 3.0, 0); lJ.vc.set(s6t(s6, '全身から', '大静脈')); lJ.vc.at(-0.8, 3.6, 0);
  lJ.pa.set(s6t(s6, '肺へ', '肺動脈')); lJ.pa.at(-0.45, 2.0, 0.6); lJ.pv.set(s6t(s6, '肺から', '肺静脈')); lJ.pv.at(1.55, 2.05, -0.5);
  lJ.ra.at(-1.35, 0.85, 0.5); lJ.rv.at(-0.75, -0.75, 0.9); lJ.la.at(1.5, 0.9, -0.2); lJ.lv.at(1.2, -0.55, 0.5);
  Object.values(lJ).forEach(l => { l.show = true; }); [lJ.ra, lJ.rv, lJ.la, lJ.lv].forEach(l => { l.show = !s6; }); lJ.heart.show = s6 || SM; if (SM) [lJ.liver, lJ.kid, lJ.si].forEach(l => { l.show = false; });
  const Q = st.hr * st.sv;
  return '心拍数 <b>' + st.hr + '回</b> × <b>' + st.sv + 'mL</b> ＝ 1分間に <b>' + (Q / 1000).toFixed(1) + ' L</b>（目安）'
    + (SM ? '' : '<br>' + s6t(s6, '赤＝酸素が多い血液、青＝二酸化炭素が多い血液。肺をめぐる道と全身をめぐる道', '赤＝動脈血、青＝静脈血。肺循環（心臓→肺→心臓）と体循環（心臓→全身→心臓）') + '（正面から見て左が体の右・模式図）');
}

// ================= ② 呼吸 =================
const GK = G.K;
{ const t = new THREE.Mesh(new THREE.CapsuleGeometry(2.95, 3.3, 8, 28), skin); t.scale.z = 0.56; t.position.y = 0.95; GK.add(t); const nk = new THREE.Mesh(cylGeo, skin); nk.scale.set(0.55, 1.2, 0.5); nk.position.y = 5.3; GK.add(nk); }
const AIRP = [-1, 1].map(s => cv([[0, 5.7, 0.25], [0, 2.55, 0.1], [s * 0.55, 2.1, 0.05], [s * 1.05, 1.55, 0], [s * 1.4, 1.0, -0.05]]));
tube([[0, 5.7, 0.25], [0, 2.55, 0.1]], 0.2, glass(0x94a3b8, 0.45), GK);
for (let y = 5.5; y > 2.8; y -= 0.3) { const r = new THREE.Mesh(new THREE.TorusGeometry(0.21, 0.025, 6, 20), std(0xcbd5e1)); r.rotation.x = PI / 2; r.position.set(0, y, 0.25 - (5.7 - y) * 0.15 / 3.15); GK.add(r); }
[-1, 1].forEach(s => tube([[0, 2.6, 0.1], [s * 0.55, 2.1, 0.05], [s * 1.05, 1.55, 0], [s * 1.4, 1.0, -0.05]], 0.13, glass(0x94a3b8, 0.45), GK));
const LTOP = 3.55, LRY = 2.25;
const lungs = [-1, 1].map(s => {
  const g = new THREE.Group(); g.position.set(s * 1.6, LTOP, -0.1); GK.add(g);
  ell([0, -LRY, 0], [1.1, LRY, 1.05], glass(0xf9a8d4, 0.3), g);
  const inn = -s, b0 = [inn * 0.2, -2.55, 0.05], br = glass(0xa1a1aa, 0.6);
  [[b0, [-inn * 0.05, -1.4, 0.05], [-inn * 0.3, -0.5, 0]], [b0, [-inn * 0.35, -2.3, 0.1], [-inn * 0.75, -2.0, 0.05]], [b0, [0, -3.3, 0.05], [-inn * 0.25, -3.9, 0]], [[-inn * 0.05, -1.4, 0.05], [-inn * 0.55, -1.0, 0.1]], [[0, -3.3, 0.05], [inn * 0.3, -3.8, 0.15]]]
    .forEach(p => tube(p, 0.045, br, g, 16));
  return g;
});
const kHeart = ell([0.45, -0.2, 0.45], [0.62, 0.75, 0.55], std(0xfda4af), GK); kHeart.rotation.z = 0.5;
const dia = new THREE.Mesh(new THREE.SphereGeometry(1, 40, 14, 0, 2 * PI, 0, PI / 2), new THREE.MeshStandardMaterial({ color: 0xfb923c, roughness: 0.6, transparent: true, opacity: 0.42, side: THREE.DoubleSide, depthWrite: false }));
dia.position.y = -2.6; GK.add(dia);
const ribs = new THREE.Group(); GK.add(ribs);
{ const rm = std(0xeadcc6, { roughness: 0.8, transparent: true, opacity: 0.8 });
  for (let k = 0; k < 6; k++) { const y0 = 3.15 - k * 0.72; [-1, 1].forEach(s => { const pts = []; for (let i = 0; i <= 14; i++) { const a = 0.22 + 2.05 * i / 14; pts.push([s * 2.85 * Math.sin(a), y0 - 0.22 * (i / 14), -1.5 * Math.cos(a)]); } tube(pts, 0.045, rm, ribs, 40); }); }
  for (let y = 3.4; y > -2.6; y -= 0.42) { const b = new THREE.Mesh(cylGeo, rm); b.scale.set(0.2, 0.32, 0.2); b.position.set(0, y, -1.55); ribs.add(b); }
  const st = new THREE.Mesh(cylGeo, rm); st.scale.set(0.16, 3.0, 0.08); st.position.set(0, 1.7, 1.42); ribs.add(st); }
// 肺胞の拡大（上の図の右側をそのまま立体に）
const ZK = new THREE.Group(); ZK.position.set(7.2, 1.5, 0); GK.add(ZK);
const KA = 1.7 / 66, CX0 = 372, CX1 = 568, inWin = x => x >= CX0 && x <= CX1, mapA = (x, y, z) => new THREE.Vector3((x - B.AC[0]) * KA, -(y - B.AC[1]) * KA, z || 0);
const alv = ell([0, 0, 0], [1.9, 1.9, 1.9], glass(0xfbcfe8, 0.26, { side: THREE.DoubleSide }), ZK);
[[408, 126, 20], [396, 166, 17], [532, 100, 21], [560, 136, 18], [512, 72, 15]].forEach(c => { const m = ell([0, 0, 0], [c[2] * KA, c[2] * KA, c[2] * KA], glass(0xfbcfe8, 0.2), ZK); m.position.copy(mapA(c[0], c[1], -0.5)); });
tube([[372, 40], [386, 66], [404, 86], [424, 101], [438, 114]].map(p => mapA(p[0], p[1], 0)), 11 * KA, glass(0xf9a8d4, 0.4), ZK, 24);
const capSs = []; for (let d = 0; d <= B.CAP.len; d += 3) { if (inWin(B.at(B.CAP, d)[0])) capSs.push(d); }
const capS0 = capSs[0], capS1 = capSs[capSs.length - 1];
const capCurve = cv(capSs.map(d => { const q = B.at(B.CAP, d); return mapA(q[0], q[1], 0); }));
const capF = s => clamp((s - B.CAP0) / (B.CAP1 - B.CAP0) * 1.6, 0, 1);
tubeGrad(capCurve, 9 * KA, 0xbfdbfe, 0xfecaca, u => capF(lerp(capS0, capS1, u)), ZK, 0.55, 120);
const NR = B.rbc.length, rbcM = inst(dotGeo, std(0xffffff, { roughness: 0.4 }), NR); ZK.add(rbcM);
// 酸素（オレンジ2つ）と二酸化炭素（黒＋灰2つ）の粒：気管の中の空気と、拡大図の中の分子
const NO = 40, NC = 40;
const o2M = inst(dotGeo, std(0xea580c), NO * 2), cC = inst(dotGeo, std(0x1f2937), NC), cS = inst(dotGeo, std(0x94a3b8), NC * 2), airM = inst(dotGeo, std(0xcbd5e1), 20);
GK.add(o2M, cC, cS, airM);
let nO = 0, nCc = 0, nAir = 0;
const wv = new THREE.Vector3(), ax = new THREE.Vector3(1, 0, 0);
function addO2(p, r) { if (nO >= NO) return; putAt(o2M, nO * 2, wv.copy(p).addScaledVector(ax, -r * 0.9), r); putAt(o2M, nO * 2 + 1, wv.copy(p).addScaledVector(ax, r * 0.9), r); nO++; }
function addCO2(p, r) { if (nCc >= NC) return; putAt(cC, nCc, p, r * 0.95); putAt(cS, nCc * 2, wv.copy(p).addScaledVector(ax, -r * 1.5), r); putAt(cS, nCc * 2 + 1, wv.copy(p).addScaledVector(ax, r * 1.5), r); nCc++; }
const dash = new THREE.Line(new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(2.3, 0.4, 0.7), new THREE.Vector3(7.2 - 1.85, 1.5, 0)]), new THREE.LineDashedMaterial({ color: 0x38bdf8, dashSize: 0.2, gapSize: 0.14 }));
dash.computeLineDistances(); GK.add(dash);
const spot = new THREE.Mesh(new THREE.TorusGeometry(0.28, 0.03, 6, 24), std(0x38bdf8)); spot.position.set(2.3, 0.4, 0.7); GK.add(spot);
const zi = i => 0.75 * Math.sin(i * 2.17 + 0.6);
const lK = {
  tr: lab('K', '気管'), br: lab('K', '気管支', { sub: true }), lung: lab('K', '肺'), heart: lab('K', '心臓', { sub: true }), dia: lab('K', '横隔膜'), rib: lab('K', '', { sub: true }),
  alv: lab('K', '', { accent: true }), cap: lab('K', '毛細血管', { sub: true }), air: lab('K', '', { accent: true }),
};
function frameK(st) {
  const Bb = st.B, b = Bb.b, amp = st.amp, s6 = st.s6, ex = 0.05 * b * amp, ey = 0.08 * b * amp;
  lungs.forEach(g => g.scale.set(1 + ex, 1 + ey, 1 + ex));
  const apex = -1.05 - 0.38 * b * Math.min(1.6, amp); dia.scale.set(2.85, apex + 2.6, 1.55);
  const rk = 1 + 0.03 * b * amp; ribs.scale.set(rk, 1, rk);
  const side = Math.abs(Math.sin(v.cam.th)) > 0.75; ZK.visible = dash.visible = spot.visible = !side;
  nO = nCc = nAir = 0;
  // 気管の空気
  B.air.forEach(a => { const P = a.sd ? B.AWR : B.AWL, p = AIRP[a.sd].getPointAt(clamp(a.s / P.len, 0, 1), tmpV); const isO = Bb.inh ? a.k % 5 === 0 : a.k % 6 === 0, isC = !Bb.inh && a.k % 4 === 2;
    if (isO) addO2(p, 0.05); else if (isC) addCO2(p, 0.045); else if (nAir < 20) putAt(airM, nAir++, p, 0.05); });
  // 拡大図の中
  if (!side) {
    const toW = (p) => p.multiplyScalar(1).add(ZK.position);
    B.o2.forEach((m, i) => { if (m.st === 'wait' || !inWin(m.x)) return; const z = m.st === 'air' ? zi(i) : m.st === 'x' ? zi(i) * (1 - m.t) : 0; addO2(toW(mapA(m.x, m.y, z)), 0.075); });
    B.co2.forEach((m, i) => { if (m.st === 'wait' || !inWin(m.x)) return; const z = m.st === 'air' || m.st === 'go' ? zi(i + 7) : m.st === 'x' ? zi(i + 7) * m.t : 0; addCO2(toW(mapA(m.x, m.y, z)), 0.065); });
    const R = st.R * KA; alv.scale.set(R, R, R);
    B.rbc.forEach((c, i) => { const q = B.at(B.CAP, c.s); putAt(rbcM, i, mapA(q[0], q[1], 0), inWin(q[0]) ? 0.15 : 0); rbcM.setColorAt(i, bloodCol(capF(c.s))); });
    rbcM.instanceMatrix.needsUpdate = true; rbcM.instanceColor.needsUpdate = true;
  }
  hideFrom(o2M, nO * 2, NO * 2); hideFrom(cC, nCc, NC); hideFrom(cS, nCc * 2, NC * 2); hideFrom(airM, nAir, 20);
  lK.tr.at(0.35, 4.6, 0.3); lK.br.at(1.05, 2.05, 0.1); lK.lung.at(-1.6, LTOP + 0.35, 0); lK.heart.at(0.55, 0.75, 0.6);
  lK.dia.at(2.2, -2.15, 1.0); lK.rib.set('ろっ骨'); lK.rib.at(-2.75, 2.55, 0.6);
  lK.alv.set(s6t(s6, '肺胞（拡大）', '肺胞（拡大・イメージ）')); lK.alv.at(7.2, 3.5, 0); lK.cap.at(7.2, -1.05, 0.4);
  lK.air.set(Bb.inh ? s6t(s6, '↓ すう', '↓ 吸う') : '↑ はく'); lK.air.at(1.0, 5.75, 0.25);
  Object.values(lK).forEach(l => { l.show = true; }); lK.dia.show = !s6; lK.br.show = !s6; lK.alv.show = lK.cap.show = !side; lK.air.show = !SM;
  const V = st.br * st.tv;
  return (Bb.inh ? s6t(s6, 'すっている', '吸っている') : 'はいている') + '・1分間に <b>' + st.br + '回</b> × <b>' + st.tv.toLocaleString('ja-JP') + 'mL</b> ＝ <b>' + (V / 1000).toFixed(1) + ' L</b>'
    + (SM ? '' : '<br>' + s6t(s6, 'オレンジ2つの粒＝酸素、黒と灰色＝二酸化炭素。肺はむねとおなかの間のまくが下がるとふくらむ', 'オレンジ2つ＝酸素、黒と灰色＝二酸化炭素。横隔膜が下がり、ろっ骨が広がると肺がふくらむ') + '（模式図）');
}

// ================= ③ 消化と吸収 =================
const GS = G.S, mS = (x, y, z) => new THREE.Vector3((x - 120) / 22, (160 - y) / 22, z || 0);
bodyShell(GS, { head: [(160 - 26) / 22, 1.0], torso: [-1.85, 2.9, 5.6] });
const SP = B.SP, zMap = [
  () => 0.75,
  (i, n) => lerp(0.55, 0.15, i / (n - 1)) - 0.35 * Math.sin(PI * i / (n - 1)),
  (i) => 0.42 + 0.14 * Math.sin(i * 1.3),
  (i, n) => lerp(0.35, 0.3, i / (n - 1)),
  (i) => 0.3 + 0.28 * Math.sin(i * 1.15),
  () => 0.05,
  (i, n) => lerp(0.05, -0.1, i / (n - 1)),
];
const SC = SP.map((P, s) => { const pts = P.pts.filter((p, i, a) => i === 0 || Math.hypot(p[0] - a[i - 1][0], p[1] - a[i - 1][1]) > 0.5); return pts.length < 2 ? null : cv(pts.map((p, i) => mS(p[0], p[1], zMap[s](i, pts.length)))); });
const org = {};
org.mouth = ell([0, 0, 0], [0.3, 0.12, 0.12], std(0xbe123c), GS); org.mouth.position.copy(mS(120, 40, 0.92));
const glands = [104, 136].map(x => { const m = ell([0, 0, 0], [0.2, 0.15, 0.15], glass(0x7dd3fc, 0.7), GS); m.position.copy(mS(x, 52, 0.35)); return m; });
org.eso = tubeC(SC[1], 0.13, glass(0xfca5a5, 0.6), GS, 40);
org.sto = ell([0, 0, 0], [1.0, 0.95, 0.62], glass(0xfecdd3, 0.5), GS); org.sto.position.copy(mS(152, 134, 0.42)); org.sto.rotation.z = -0.5;
org.pyl = tube([mS(140, 151, 0.4), mS(134, 153, 0.36), mS(129, 152, 0.34)], 0.22, glass(0xfecdd3, 0.5), GS, 10);
org.liv = ell([0, 0, 0], [1.75, 0.68, 1.0], glass(0xe8a87c, 0.78), GS); org.liv.position.copy(mS(96, 119, 0.3)); org.liv.rotation.z = 0.13;
org.gal = ell([0, 0, 0], [0.22, 0.32, 0.2], glass(0x86efac, 0.92), GS); org.gal.position.copy(mS(106, 141, 0.85));
tube([mS(108, 148, 0.8), mS(111, 155, 0.6), mS(113, 160, 0.4)], 0.045, std(0x16a34a), GS, 12);
org.pan = tube([[122, 166], [146, 162], [168, 156]].map(p => mS(p[0], p[1], -0.35)), 0.19, glass(0xfde68a, 0.9), GS, 20);
const siPts = []; [3, 4].forEach(s => { const c = SC[s]; for (let i = 0; i <= 60; i++) siPts.push(c.getPointAt(i / 60)); });
org.si = tubeC(cv(siPts.filter((p, i) => i === 0 || p.distanceTo(siPts[i - 1]) > 1e-3)), 0.17, glass(0xfda4af, 0.55), GS, 260);
org.li = tubeC(SC[5], 0.3, glass(0xfdba74, 0.5), GS, 120);
org.rec = tubeC(SC[6], 0.2, glass(0xfdba74, 0.5), GS, 16);
const GLOW = { 1: ['eso'], 2: ['sto', 'pyl'], 3: ['liv', 'gal', 'pan', 'si'], 4: ['si'], 5: ['li'] };
const food = new THREE.Mesh(sphGeo, std(0xa16207, { transparent: true })); GS.add(food);
const foodHalo = new THREE.Mesh(sphGeo, glass(0xffffff, 0.45)); GS.add(foodHalo);
const drops = inst(dotGeo, std(0xffffff), 12); GS.add(drops);
// 柔毛の拡大
const ZS = new THREE.Group(); ZS.position.set(5.6, -1.8, 0); GS.add(ZS);
{ const vm = new THREE.Mesh(new THREE.CapsuleGeometry(0.85, 3.0, 8, 24), glass(0xfecdd3, 0.38, { side: THREE.DoubleSide })); ZS.add(vm);
  const cm = std(0xdc2626, { roughness: 0.5 });
  [0.4, -0.4].forEach(z => { tube([[-0.55, -2.2, z], [-0.55, 1.2, z], [0, 1.85, z], [0.55, 1.2, z], [0.55, -2.2, z]], 0.05, cm, ZS, 40);
    for (let y = -1.6; y < 1.2; y += 0.55) tube([[-0.55, y, z], [-0.2, y + 0.2, z * 1.15], [0.2, y - 0.1, z * 1.15], [0.55, y + 0.12, z]], 0.028, cm, ZS, 12); });
  tube([[0, -2.3, 0], [0, 1.55, 0]], 0.09, std(0x84cc16), ZS, 8); }
const absM = inst(dotGeo, std(0xffffff), 12); ZS.add(absM);
const dashS = new THREE.Line(new THREE.BufferGeometry().setFromPoints([mS(150, 226, 0.6), new THREE.Vector3(5.6 - 0.95, -1.8, 0)]), new THREE.LineDashedMaterial({ color: 0x38bdf8, dashSize: 0.2, gapSize: 0.14 }));
dashS.computeLineDistances(); GS.add(dashS);
const lS = {
  mouth: lab('S', '口'), eso: lab('S', '食道', { sub: true }), sto: lab('S', '胃'), liv: lab('S', ''), gal: lab('S', '', { sub: true }), pan: lab('S', 'すい臓', { sub: true }),
  si: lab('S', '小腸'), li: lab('S', '大腸'), anus: lab('S', '', { sub: true }), food: lab('S', '食べ物', { accent: true }),
  vil: lab('S', ''), vcap: lab('S', '', { sub: true }), lym: lab('S', 'リンパ管', { sub: true }),
};
const ABS_C = [0xeab308, 0x3b82f6, 0xfb923c];
function frameS(st) {
  const s6 = st.s6, sg = B.stg(st.dp), s = sg[0], u = sg[1], T = st.T, Lv = B.lvls(s, u);
  Object.entries(org).forEach(([k, m]) => { if (!m.material.emissive) return; const on = (GLOW[s] || []).includes(k); m.material.emissive.setHex(on ? 0xf59e0b : 0x000000); m.material.emissiveIntensity = on ? 0.45 : 0; });
  // 食べ物
  let fp;
  if (s === 0) { fp = mS(120, 41, 0.78); const r = 0.26 * (1 + 0.18 * Math.sin(T * 12)); food.scale.set(r, r, r); }
  else { fp = SC[s].getPointAt(clamp(u, 0, 1)); food.scale.set(0.24, 0.24, 0.24); }
  food.position.copy(fp); foodHalo.position.copy(fp); foodHalo.scale.setScalar(food.scale.x * 1.35);
  food.material.opacity = s === 6 ? 1 - 0.8 * u : 1; foodHalo.visible = s !== 6;
  // 消化液のしずく
  const ph = (T * 1.6) % 1; let nd = 0; const dc = new THREE.Color();
  const drop = (p, c, r) => { putAt(drops, nd, p, r || 0.07); drops.setColorAt(nd, dc.setHex(c)); nd++; };
  if (s === 0) glands.forEach(g => drop(new THREE.Vector3().lerpVectors(g.position, org.mouth.position, ph), 0x38bdf8));
  if (s === 2) for (let k = 0; k < 5; k++) { const a = k * 1.26 + T; drop(mS(152 + 16 * Math.cos(a) * (1 - ph * 0.5), 136 + 10 * Math.sin(a) * (1 - ph * 0.5), 0.42 + 0.25 * Math.sin(a * 1.7)), 0x22d3ee); }
  if (s === 3) { drop(mS(lerp(108, 113, ph), lerp(148, 160, ph), lerp(0.8, 0.4, ph)), 0x16a34a, 0.08); drop(mS(lerp(130, 116, ph), lerp(163, 166, ph), lerp(-0.3, 0.3, ph)), 0xd97706, 0.08); }
  if (s === 4) for (let k = 0; k < 6; k++) { const q = SC[4].getPointAt(((k / 6 + ph / 6) % 1)); q.y += 0.2; drop(q, 0xdb2777, 0.06); }
  if (s === 5) for (let k = 0; k < 4; k++) { const q = SC[5].getPointAt(((k / 4 + ph / 4) % 1)); q.x += ph * 0.3; q.y += ph * 0.3; q.z += ph * 0.5; drop(q, 0x3b82f6, 0.07); }
  hideFrom(drops, nd, 12); if (drops.instanceColor) drops.instanceColor.needsUpdate = true;
  // 柔毛：吸収しているとき、糖・アミノ酸は毛細血管へ、脂肪は中央のリンパ管へ
  const side = Math.abs(Math.sin(v.cam.th)) > 0.75; ZS.visible = dashS.visible = !side;
  const absorbing = Lv[0] > 3 && Lv[0] < 4 || Lv[1] > 3 && Lv[1] < 4 || Lv[2] > 2 && Lv[2] < 3;
  let na = 0;
  if (absorbing && !side) for (let i = 0; i < 12; i++) {
    const kind = i % 3, f = (T * 0.45 + i / 12) % 1, sx = (i % 2 ? 1 : -1), y0 = -1.5 + (i * 0.37) % 2.6, p = new THREE.Vector3();
    if (kind < 2) { if (f < 0.4) p.set(sx * lerp(1.5, 0.55, f / 0.4), y0, 0.4); else p.set(sx * 0.55, lerp(y0, -2.2, (f - 0.4) / 0.6), 0.4); }
    else { if (f < 0.45) p.set(sx * lerp(1.5, 0, f / 0.45), y0, lerp(0.6, 0, f / 0.45)); else p.set(0, lerp(y0, -2.3, (f - 0.45) / 0.55), 0); }
    putAt(absM, na, p, 0.09); absM.setColorAt(na, dc.setHex(ABS_C[kind])); na++;
  }
  hideFrom(absM, na, 12); if (absM.instanceColor) absM.instanceColor.needsUpdate = true;
  // 名前
  lS.mouth.at(-0.55, 5.6, 0.9); lS.mouth.show = s !== 0; lS.eso.at(-0.55, 2.9, 0.1); lS.sto.at(2.55, 1.75, 0.5); lS.liv.set(s6t(s6, 'かん臓', '肝臓')); lS.liv.at(-1.9, 2.25, 0.6);
  lS.gal.set(s6t(s6, 'たんのう', '胆のう')); lS.gal.at(-1.15, 0.45, 0.9); lS.pan.at(2.35, 0.15, -0.3);
  lS.si.at(0.1, -2.0, 0.8); lS.li.at(-2.55, -1.3, 0.2); lS.anus.set(s6t(s6, 'こう門', '肛門')); lS.anus.at(0.55, -7.2, 0);
  lS.food.at(fp.x, fp.y + 0.3, fp.z); lS.vil.set(s6t(s6, 'じゅう毛（拡大）', '柔毛（拡大）')); lS.vil.at(5.9, 0.95, 0); lS.vcap.set(s6t(s6, '毛細血管（→かん臓へ）', '毛細血管（→肝臓へ）')); lS.vcap.at(5.6, -4.25, 0.4); lS.lym.at(5.6, -4.95, 0);
  Object.values(lS).forEach(l => { if (l !== lS.mouth) l.show = true; }); lS.food.show = s !== 6 || u < 0.6; [lS.vil, lS.vcap, lS.lym].forEach(l => { l.show = !side; });
  return 'いま：<b>' + B.PLACE()[s] + '</b>・はたらく消化液：<b>' + B.JUICE_S()[s] + '</b>' + (SM ? '' : '<br>' + B.DESC()[s] + '（形と大きさは模式図）');
}

// ---- 毎フレーム ----
const hud = $('hud3d'); hud.style.display = '';
if (SM) { hud.style.fontSize = '11px'; hud.style.padding = '3px 6px'; hud.style.left = hud.style.top = '6px'; }
const FN = { J: frameJ, K: frameK, S: frameS };
let cur = '', lastHtml = '';
v.onFrame(() => {
  const st = B.st(), key = st.mode;
  if (key !== cur) {
    Object.keys(G).forEach(k => { G[k].visible = k === key; (L[k] || []).forEach(l => { l.show = false; }); });
    const c = CAM[key]; ['persp', 'front', 'side'].forEach((k, i) => { v.views[k].tgt = c.tgt; v.views[k].dist = c.d[i] * (SM ? c.m : 1); });
    v.setView('persp', !cur); cur = key;
  }
  const html = FN[key](st);
  if (html !== lastHtml) { hud.innerHTML = html; lastHtml = html; }
});
