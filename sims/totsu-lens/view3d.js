// 凸レンズの像 3D（光学台の実験。上の「物体とレンズの距離」「焦点距離」「作図する光」「物体」「光の束」「レンズの上半分をかくす」と連動）
// 単位は cm。光軸＝x軸（物体が −x、スクリーンが +x＝上の図と同じ並び）、上＝+y、手前＝+z。像は光軸のまわりに180°回る＝上下左右が逆
import { THREE, createView, mat, water, COL } from '../../assets/three/sim3d.js';
const $ = id => document.getElementById(id);
const L = window.__lens || {};
const S = L.S || 7, X0 = L.X0 || 310, W = L.W || 640, HO = L.HO || 6, HL = (L.HL || 100) / S;   // 2Dと同じ定数（物体の高さ6cm、レンズの半径）
const fmt = L.fmt || (x => String(Math.round(x * 100) / 100));
const st = L.st || (() => { const f = +$('f').value, a = +$('a').value; if (Math.abs(a - f) < 1e-9) return { f, a, kind: 'none', b: Infinity, m: Infinity }; const b = a * f / (a - f); return { f, a, b, m: Math.abs(b / a), kind: b > 0 ? 'real' : 'virt' }; });
const PI = Math.PI, small = innerWidth < 520;
const X1 = -45, X2 = 50, RY = -(HL + 2), XE = (W - X0) / S, BMAX = (W - 10 - X0) / S, VMIN = -(X0 + 30) / S, YM = 200 / S;   // 台の端・台の高さ・2Dの画面の端
const v = createView($('view3d'), {
  views: { persp: { tgt: [8, -2, 0], dist: 120, th: 0.5, ph: 0.3 }, side: { tgt: [2.5, -1, 0], dist: 108, th: 0, ph: 0.03 }, front: { tgt: [18, -1, 0], dist: 58, th: PI / 2 - 0.32, ph: 0.1 } },
  camRow: '#camRow3d', minDist: 25, maxDist: 320, shadows: false, near: 1, far: 3000,
});
const { scene } = v;
// ---- 光学台・光軸・レンズ ----
const gray = mat(0x7d8590), dark = mat(0x4a5058);
const rail = new THREE.Mesh(new THREE.BoxGeometry(X2 - X1, 1, 3), mat(0xa9aeb6)); rail.position.set((X1 + X2) / 2, RY - 0.5, 0); scene.add(rail);
for (let c = X1; c <= X2; c += 5) { const t = new THREE.Mesh(new THREE.BoxGeometry(0.15, 0.06, c % 10 === 0 ? 3 : 1.5), dark); t.position.set(c, RY + 0.03, 0); scene.add(t); }
const postG = new THREE.CylinderGeometry(0.35, 0.35, 1, 10), baseG = new THREE.BoxGeometry(3, 1, 4.4);
function stand(top) { const g = new THREE.Group(), p = new THREE.Mesh(postG, gray), b = new THREE.Mesh(baseG, dark); p.scale.y = Math.max(0.01, top - RY); p.position.y = (top + RY) / 2; b.position.y = RY + 0.5; g.add(p, b); g.userData.post = p; scene.add(g); return g; }
stand(-HL); const objStand = stand(0), scrStand = stand(-12);
const cyl = new THREE.CylinderGeometry(1, 1, 1, 8), Yv = new THREE.Vector3(0, 1, 0), d = new THREE.Vector3(), p0 = new THREE.Vector3(), p1 = new THREE.Vector3(), p2 = new THREE.Vector3();
const segM = (c, op = 1) => new THREE.MeshBasicMaterial({ color: c, transparent: op < 1, opacity: op, depthWrite: op >= 1 });
function put(m, r, a, b) { d.subVectors(b, a); const len = d.length(); if (!(len > 1e-6) || !isFinite(len)) { m.visible = false; return; } m.visible = true; m.position.copy(a).addScaledVector(d, 0.5); m.quaternion.setFromUnitVectors(Yv, d.divideScalar(len)); m.scale.set(r, len, r); }
const axis = new THREE.Mesh(cyl, segM(0x7d8590, 0.8)); scene.add(axis); put(axis, 0.07, p0.set(X1, 0, 0), p1.set(X2, 0, 0));
const lens = new THREE.Mesh(new THREE.SphereGeometry(HL, 48, 24), water(0.38, 0x8fc7f0)); scene.add(lens);
const rim = new THREE.Mesh(new THREE.TorusGeometry(HL, 0.3, 8, 72), mat(COL.teal)); rim.rotation.y = PI / 2; scene.add(rim);
const cov = new THREE.Mesh(new THREE.CircleGeometry(HL + 0.8, 40, 0, PI), new THREE.MeshStandardMaterial({ color: 0xa16207, roughness: 0.9, side: THREE.DoubleSide })); cov.rotation.y = PI / 2; cov.position.x = 2.2; scene.add(cov);
const fDot = [-1, 1].map(() => { const m = new THREE.Mesh(new THREE.SphereGeometry(0.55, 16, 12), new THREE.MeshBasicMaterial({ color: 0xe6a700 })); scene.add(m); return m; });
const f2 = [-1, 1].map(() => { const m = new THREE.Mesh(new THREE.BoxGeometry(0.2, 1.8, 0.2), dark); scene.add(m); return m; });
// ---- 物体と像（平らな板。形の右＝世界の −z なので、スクリーン側から見ると上の「正面から見ると」と同じ向き） ----
const poly = (pts, m) => new THREE.Mesh(new THREE.ShapeGeometry(new THREE.Shape(pts.map(p => new THREE.Vector2(p[0] * HO, p[1] * HO)))), m);
function glyph(kind, M) {
  const g = new THREE.Group();
  if (kind === 'arrow') g.add(poly([[-.045, 0], [.045, 0], [.045, .76], [-.045, .76]], M(0xe08a00)), poly([[0, 1], [-.17, .74], [.17, .74]], M(0xe08a00)), poly([[.045, .66], [.42, .52], [.045, .38]], M(0xd6352b)));   // 矢印＋右向きの赤い旗
  else g.add(poly([[-.13, 0], [.13, 0], [.13, .64], [-.13, .64]], M(0xcdb67a)), poly([[.13, .4], [.2, .4], [.2, .64], [.13, .64]], M(0xb79a55)), poly([[0, .66], [-.085, .76], [-.06, .88], [0, 1], [.06, .88], [.085, .76]], M(0xf97316)));   // ろうそく＋右側のろうのたれ
  g.rotation.y = PI / 2; return g;
}
const KINDS = ['arrow', 'candle'];
function mkSet(tr) { const g = new THREE.Group(), ms = [], M = c => { const m = new THREE.MeshBasicMaterial({ color: c, side: THREE.DoubleSide, transparent: tr }); ms.push(m); return m; }; const o = { g, ms }; for (const k of KINDS) { o[k] = glyph(k, M); g.add(o[k]); } scene.add(g); return o; }
const oSet = mkSet(false), aSet = mkSet(true), bSet = mkSet(true), vSet = mkSet(true);
aSet.g.rotation.x = PI; bSet.g.rotation.x = PI;   // 実像：光軸のまわりに180°（上下左右が逆）
const scr = new THREE.Mesh(new THREE.PlaneGeometry(1, 1), new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.62, side: THREE.DoubleSide, depthWrite: false })); scr.rotation.y = PI / 2; scene.add(scr);
scr.add(new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.PlaneGeometry(1, 1)), new THREE.LineBasicMaterial({ color: 0x5b636d })));
// ---- 光（細い棒。作り直さず、位置と長さだけ変える） ----
const mkRay = (c, r, op, n) => { const m = segM(c, op), R = []; for (let i = 0; i < n; i++) { const s = new THREE.Mesh(cyl, i === 2 ? segM(c, 0.4) : m); s.visible = false; scene.add(s); R.push(s); } R.r = r; return R; };
const RAYS = [mkRay(0xe5484d, 0.2, 1, 3), mkRay(0x1fa34a, 0.2, 1, 3), mkRay(0x2f7fe0, 0.2, 1, 3)], FAN = [];
for (let i = 0; i < 12; i++) FAN.push(mkRay(0xe6a700, 0.08, 0.5, 2));
const off = R => R.forEach(s => { s.visible = false; });
// 物体の先 → レンズの上の点 (py,pz) → レンズで1回だけ曲がって右へ（2Dの outK と同じ式）
function ray(R, py, pz, s, xe, stop, back) {
  off(R); p0.set(-s.a, HO, 0); p1.set(0, py, pz);
  const over = Math.abs(py) > YM;
  if (over) { const t = (Math.sign(py) * YM - HO) / (py - HO); p1.set(-s.a * (1 - t), HO + (py - HO) * t, pz * t); }
  put(R[0], R.r, p0, p1); if (over || stop) return;
  const ky = (py - HO) / s.a - py / s.f, kz = pz / s.a - pz / s.f; let ex = xe, ey = py + ky * xe;
  if (Math.abs(ey) > YM) { ex = xe * (Math.sign(ey) * YM - py) / (ey - py); ey = py + ky * ex; }
  p2.set(ex, ey, pz + kz * ex); put(R[1], R.r, p1, p2);
  if (back && R[2]) { p2.set(s.b, s.m * HO, 0); put(R[2], R.r * 0.6, p1, p2); }   // 逆向きにのばした線（虚像）
}
const lObj = v.label('物体', [0, 0, 0]), lLens = v.label('凸レンズ', [0, HL + 1.2, 0]), lScr = v.label('スクリーン', [0, 0, 0]), lImg = v.label('', [0, 0, 0], { accent: true });
const lF = [-1, 1].map(() => v.label('F', [0, 0, 0], { sub: true })), lF2 = [-1, 1].map(() => v.label('2F', [0, 0, 0], { sub: true }));
if (!small) v.label('光軸', [X2 - 2, 0.4, 0], { sub: true });
const hud = $('hud3d'); let last = '';
v.onFrame(() => {
  const s = st(), kind = $('obj').value === 'candle' ? 'candle' : 'arrow', sel = $('rays').value, fan = !!s.fan, cover = !!s.cover;
  const key = [s.a, s.f, kind, sel, fan, cover].join('/'); if (key === last) return; last = key;
  const want = sel === 'all' ? [1, 2, 3] : sel === '12' ? [1, 2] : [+sel], showImg = want.length >= 2 || fan || cover, ia = cover ? 0.5 : 1;
  const real = s.kind === 'real', virt = s.kind === 'virt', scrOn = real && s.b <= BMAX, vOn = virt && s.b > VMIN, xe = scrOn ? s.b : XE;
  for (const o of [oSet, aSet, bSet, vSet]) for (const k of KINDS) o[k].visible = k === kind;
  // レンズ・焦点
  lens.scale.set((6 + 100 / s.f) / 2 / S / HL, 1, 1); cov.visible = cover; lLens.set(cover ? (small ? '上半分をかくす' : '凸レンズ（上半分を厚紙でかくす）') : '凸レンズ');
  [-1, 1].forEach((sd, i) => { fDot[i].position.x = sd * s.f; lF[i].at(sd * s.f, 0.9, 0); f2[i].position.x = sd * 2 * s.f; lF2[i].at(sd * 2 * s.f, 1.2, 0); lF2[i].show = !small; });
  // 物体
  oSet.g.position.x = -s.a; objStand.position.x = -s.a; lObj.at(-s.a, HO + 1.2, 0);
  // 実像とスクリーン（スクリーンは半透明。像は両面に見える）
  const hs = real ? Math.max(12, s.m * HO + 2) : 12, on = scrOn && showImg;
  scr.visible = on; scrStand.visible = on; aSet.g.visible = on; bSet.g.visible = on; lScr.show = on;
  if (on) {
    scr.position.x = s.b; scr.scale.set(2 * hs, 2 * hs, 1); scrStand.position.x = s.b;
    const p = scrStand.userData.post; p.visible = -hs > RY + 0.2; p.scale.y = Math.max(0.01, -hs - RY); p.position.y = (-hs + RY) / 2;
    aSet.g.position.x = s.b - 0.1; bSet.g.position.x = s.b + 0.1; aSet.g.scale.setScalar(s.m); bSet.g.scale.setScalar(s.m);
    for (const m of aSet.ms.concat(bSet.ms)) m.opacity = ia;
    lScr.at(s.b, hs + 1, 0);
  }
  // 虚像（物体と同じ側・同じ向き・半透明）
  vSet.g.visible = vOn && showImg;
  if (vOn) { vSet.g.position.x = s.b; vSet.g.scale.setScalar(s.m); for (const m of vSet.ms) m.opacity = 0.6 * ia; }
  lImg.show = (on || (vOn && showImg));
  if (on) { lImg.set('実像'); lImg.at(s.b, 2.4, 0); } else if (vOn) { lImg.set('虚像'); lImg.at(s.b, s.m * HO + 1.2, 0); }
  // 光：①光軸に平行 ②レンズの中心 ③焦点を通る（2Dと同じ3本）＋光の束
  const blocked = h => cover && h >= -0.5 / S, hs3 = [HO, 0, -HO * s.f / (s.a - s.f)];
  RAYS.forEach((R, i) => { if (want.indexOf(i + 1) < 0 || (i === 2 && s.kind === 'none')) { off(R); return; } ray(R, hs3[i], 0, s, xe, blocked(hs3[i]), vOn); });
  FAN.forEach((R, i) => { if (!(fan || cover)) { off(R); return; } const t = (i + 0.5) * PI / 6, py = 0.8 * HL * Math.cos(t), pz = 0.8 * HL * Math.sin(t); ray(R, py, pz, s, xe, blocked(py), false); });
  // HUD（数字と言葉は上の結果と同じ）
  const mm = Math.round(s.m * 100) / 100, head = '物体まで <b>' + fmt(s.a) + '</b> cm ・ '; let h;
  if (s.kind === 'none') h = head + '像は<b>できない</b><br><b>像なし</b>（物体が焦点の上）' + (small ? '' : '：光が平行に進むので、像はできない');
  else if (real) h = head + '像まで <b>' + fmt(s.b) + '</b> cm ・ <b>' + mm + '</b>倍<br><b>実像</b>（上下左右が逆向き）' + (scrOn ? '' : '：像は右の外（レンズから' + fmt(s.b) + ' cm）');
  else h = head + '像まで <b>' + fmt(-s.b) + '</b> cm' + (small ? '' : '（物体と同じ側）') + ' ・ <b>' + mm + '</b>倍<br><b>虚像</b>（物体と同じ向き）：スクリーンには映らない' + (vOn ? '' : '・像は左の外');
  if (!showImg && s.kind !== 'none') h += '<br><span style="font-size:11.5px">もう1本光をかくと、交わる点に像ができる</span>';
  if (cover) h += '<br><span style="font-size:11.5px">像は欠けずに暗くなる</span>';
  hud.innerHTML = h;
});
hud.style.display = '';
