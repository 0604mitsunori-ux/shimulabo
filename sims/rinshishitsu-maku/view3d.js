// リン脂質 3D：ミセル・脂質二重層・小胞（手前を切り取る）・水面の単分子膜
// 上の2D（粗いモデルの計算）そのものではなく、「できあがる形」の模式図。頭＝親水性（水側）、尾＝疎水性（水を避ける側）
// 上の選択（尾の本数・水面のあり/なし・はじめの状態）を window.__lip から読んで場面を切り替える
import { THREE, createView } from '../../assets/three/sim3d.js';
const $ = id => document.getElementById(id);
const SM = matchMedia('(max-width:640px)').matches, ZM = SM ? 0.86 : 1;
const v = createView($('view3d'), {
  views: {
    persp: { tgt: [0, 0, 0], dist: 42 * ZM, th: 0.62, ph: 0.34 },
    side: { tgt: [0, 0, 0], dist: 42 * ZM, th: Math.PI / 2, ph: 0.03 },
    cut: { tgt: [0, 0, 0], dist: 38 * ZM, th: 0, ph: 0.03 },
  },
  camRow: '#camRow3d', bg: 0xf1f5f9, shadows: false, minDist: 8, maxDist: 120,
});
const { scene } = v;
v.hemi.intensity = 1.05; v.sun.intensity = 1.2; v.sun.position.set(20, 40, 50);
const clamp = (x, a, b) => Math.max(a, Math.min(b, x)), sm = t => t <= 0 ? 0 : t >= 1 ? 1 : t * t * (3 - 2 * t);

// ---- 部品（頭＝赤い球、尾＝黄色の棒。上の図と同じ色） ----
const N = 520, HL = 0.45, TL = 2.0;
const heads = new THREE.InstancedMesh(new THREE.SphereGeometry(0.52, 14, 10), new THREE.MeshStandardMaterial({ color: 0xe0483e, roughness: 0.5 }), N);
const tailM = new THREE.MeshStandardMaterial({ color: 0xe6b422, roughness: 0.6 });
const tA = new THREE.InstancedMesh(new THREE.CylinderGeometry(0.16, 0.16, TL, 6), tailM, N), tB = new THREE.InstancedMesh(new THREE.CylinderGeometry(0.16, 0.16, TL, 6), tailM, N);
[heads, tA, tB].forEach(m => { m.frustumCulled = false; scene.add(m); });
// 水（粒は描かず、うすい青の箱で表す）
const box = new THREE.Mesh(new THREE.BoxGeometry(1, 1, 1), new THREE.MeshBasicMaterial({ color: 0x93c5fd, transparent: true, opacity: 0.22, depthWrite: false, side: THREE.DoubleSide }));
scene.add(box);

function fib(n) { const o = [], g = Math.PI * (3 - Math.sqrt(5)); for (let i = 0; i < n; i++) { const y = 1 - (i + 0.5) * 2 / n, r = Math.sqrt(Math.max(0, 1 - y * y)), a = i * g; o.push(new THREE.Vector3(r * Math.cos(a), y, -Math.abs(r * Math.sin(a)) * (Math.sin(a) > 0 ? -1 : 1))); } return o; }
const V = (x, y, z) => new THREE.Vector3(x, y, z);

// ---- 場面ごとの「できあがる形」 ----
let T = [], main = 0, tails = 2, cy = 0, YS = 9.5, cur = '', f = 0;
const sp = [], sd = [], ph = [], dl = [];
for (let i = 0; i < N; i++) { sp.push(V(0, 0, 0)); sd.push(V(0, 1, 0)); ph.push(Math.random() * 6.28); dl.push(Math.random()); }
function scatter(air) { for (let i = 0; i < N; i++) { sp[i].set((Math.random() - 0.5) * 24, (air ? YS - 2 : 10) - Math.random() * 19, (Math.random() - 0.5) * 11); sd[i].set(Math.random() - 0.5, Math.random() - 0.5, Math.random() - 0.5).normalize(); dl[i] = Math.random(); } }
function build(kind, air) {
  T = []; cy = air ? (kind === 'ves' ? -3.2 : -2.5) : 0; YS = kind === 'mono' ? 2 : (kind === 'ves' ? 10.5 : 9.5);
  if (kind === 'mic') [[-7.6, 1.6, 0], [0.4, -2.6, 1.5], [8, 2, -1]].forEach(c => fib(64).forEach(u => T.push({ p: u.clone().multiplyScalar(2.7).add(V(c[0], c[1] + cy, c[2])), d: u.clone().negate() })));       // 尾を内側にした1層の球
  if (kind === 'bil') for (let s = -1; s <= 1; s += 2) for (let i = 0; i < 12; i++) for (let j = 0; j < 9; j++) T.push({ p: V((i - 5.5) * 1.15 + (j % 2) * 0.57 - 0.28, cy + s * (HL + TL + 0.08), (j - 4) * 1.02), d: V(0, -s, 0) });   // 尾どうしが向かい合う2層
  if (kind === 'ves') {   // 二重層が閉じた球。手前半分（z>0）を切り取る
    fib(650).forEach(u => { if (u.z <= 0.02) T.push({ p: u.clone().multiplyScalar(8.5).add(V(0, cy, 0)), d: u.clone().negate() }); });
    fib(118).forEach(u => { if (u.z <= 0.02) T.push({ p: u.clone().multiplyScalar(3.6).add(V(0, cy, 0)), d: u.clone() }); });
  }
  main = T.length;
  if (air) { const nx = 16, nz = kind === 'mono' ? 9 : 5; for (let i = 0; i < nx; i++) for (let j = 0; j < nz; j++) T.push({ p: V((i - (nx - 1) / 2) * 1.15 + (j % 2) * 0.57 - 0.28, YS - 0.3, (j - (nz - 1) / 2) * 1.02), d: V(0, 1, 0) }); }   // 水面：頭が水側、尾が空気側
}

// ---- 文字 ----
const lName = v.label('', [0, 0, 0], { accent: true }), lHead = v.label(SM ? '頭（親水性）' : '親水性の頭（水になじむ）', [0, 0, 0]), lTail = v.label(SM ? '尾（疎水性）' : '疎水性の尾（水を避ける）', [0, 0, 0]);
const lWater = v.label('水', [0, 0, 0], { sub: true }), lAir = v.label('空気', [0, 0, 0], { sub: true }), lIn = v.label(SM ? '内側も水' : '内側にも水がある', [0, 0, 0], { sub: true }), lMono = v.label('単分子膜', [0, 0, 0], { sub: true });
const NAME = { mic: ['ミセル', 'ミセル（尾を内側にした1層の球）'], bil: ['脂質二重層', '脂質二重層（尾どうしが向かい合う2層の膜）'], ves: ['小胞', '小胞（二重層が閉じた袋・手前を切り取り）'], mono: ['単分子膜', '単分子膜（頭は水側・尾は空気側）'] };
const hud = $('hud3d'); if (hud) { hud.style.display = ''; if (SM) { hud.style.fontSize = '11px'; hud.style.padding = '3px 6px'; hud.style.left = hud.style.top = '6px'; } }
let kindNow = 'bil';
function setScene(kind, type, air) {
  kindNow = kind; tails = type; build(kind, air); scatter(air); f = 0;
  if (air) { box.scale.set(30, 26, 15); box.position.set(0, YS - 13, 0); } else { box.scale.set(30, 24, 15); box.position.set(0, 0, 0); }
  { const ty = air && kind !== 'mono' ? 0.8 : 0, k = (air && kind !== 'mono' ? 1.24 : kind === 'mono' ? 0.8 : 1) * ZM, B = { persp: 42, side: 42, cut: 38 };   // 場面に合わせてカメラの距離と高さを直す
    for (const n in B) { v.views[n].tgt[1] = ty; v.views[n].dist = B[n] * k; } const b = document.querySelector('#camRow3d button.on'); v.setView(b ? b.dataset.v : 'persp'); }
  const h = T[kind === 'bil' ? main - 1 : 0];
  lHead.at(h.p.x, h.p.y + (kind === 'mono' ? -1.6 : 0.5), h.p.z); lTail.at(h.p.x + h.d.x * 1.6 + (kind === 'bil' ? -3 : 0), h.p.y + h.d.y * 1.6 + (kind === 'mono' ? 1.4 : 0), h.p.z + h.d.z * 1.6);
  if (kind === 'mic') { lHead.at(-7.6, cy + 1.6 + 3.3, 0); lTail.at(-7.6, cy + 1.6 - 0.4, 0); }
  if (kind === 'ves') { lHead.at(-6.2, cy + 6.4, 0); lTail.at(4.4, cy + 4.6, 0); }
  lName.set(NAME[kind][SM ? 0 : 1]);
  lName.at(kind === 'mic' ? (SM ? 3 : 7) : 0,kind === 'mono' ? YS + 4.2 : cy + ({ mic: 6.4, bil: 4.6, ves: 10 })[kind] - (kind === 'ves' && air ? 0.2 : 0), 0);
  lIn.at(0, cy - 0.6, 0); lIn.show = kind === 'ves';
  lWater.at(SM ? 8 : 11.5, air ? YS - 3 : 9, 0); lAir.at(SM ? 8 : 11.5, YS + 2.6, 0); lAir.show = air;
  lMono.at(SM ? -3 : 3, YS + 2.4, 0); lMono.show = air && kind !== 'mono';
}

// ---- 「もう一度」ボタン（3Dの下に足す） ----
const row = document.createElement('div'); row.className = 'pick-row'; row.style.marginTop = '8px';
row.innerHTML = '<button>↺ ばらばらの状態から、もう一度集める</button>';
const camRow = $('camRow3d'); if (camRow) camRow.after(row);
row.querySelector('button').addEventListener('click', () => { scatter(cur.endsWith('true')); f = 0; });

// ---- 毎フレーム ----
const m4 = new THREE.Matrix4(), q = new THREE.Quaternion(), qI = new THREE.Quaternion(), UP = V(0, 1, 0), ZA = V(0, 0, 1), XA = V(1, 0, 0), P = V(0, 0, 0), D = V(0, 0, 0), C = V(0, 0, 0), sideV = V(0, 0, 0), ONE = V(1, 1, 1);
const ZERO = new THREE.Matrix4().makeScale(0, 0, 0);
v.onFrame((t, dt) => {
  const Lp = window.__lip && window.__lip.L && window.__lip.L() && window.__lip.L().P;
  const type = Lp ? Lp.type : 2, air = Lp ? !!Lp.air : false, st = $('start') ? $('start').value : '';
  const kind = (st === 'drop' && air) ? 'mono' : type === 1 ? 'mic' : st === 'ves' ? 'ves' : 'bil';
  const key = kind + type + air;
  if (key !== cur) { cur = key; setScene(kind, type, air); }
  f = Math.min(1, f + dt / 8);
  for (let i = 0; i < N; i++) {
    if (i >= T.length) { heads.setMatrixAt(i, ZERO); tA.setMatrixAt(i, ZERO); tB.setMatrixAt(i, ZERO); continue; }
    const u = sm(clamp(f * 1.6 - dl[i] * 0.6, 0, 1)), w = 1 - u, a = ph[i];
    P.copy(sp[i]); P.x += Math.sin(t * 0.7 + a) * 1.4; P.y += Math.cos(t * 0.6 + a * 1.7) * 1.2; P.z += Math.sin(t * 0.5 + a * 2.3) * 1.2;
    if (air && P.y > YS - 1.2) P.y = YS - 1.2;
    P.lerp(T[i].p, u);
    P.x += Math.sin(t * 5 + a * 3) * 0.07 * u; P.y += Math.cos(t * 4.3 + a * 5) * 0.07 * u; P.z += Math.sin(t * 4.7 + a * 7) * 0.07 * u;   // できた後の熱のゆれ
    D.copy(sd[i]); D.x += Math.sin(t * 1.1 + a) * 0.9; D.y += Math.cos(t * 0.9 + a * 2) * 0.9; D.z += Math.sin(t * 1.3 + a * 3) * 0.9; D.normalize();
    D.lerp(T[i].d, u); D.x += Math.sin(t * 3.1 + a * 2) * 0.09 * u; D.y += Math.sin(t * 2.9 + a * 6) * 0.09 * u; D.z += Math.cos(t * 2.7 + a * 4) * 0.09 * u;
    if (D.lengthSq() < 1e-6) D.copy(T[i].d); D.normalize();
    m4.compose(P, qI, ONE); heads.setMatrixAt(i, m4);
    q.setFromUnitVectors(UP, D);
    sideV.crossVectors(D, Math.abs(D.z) > 0.9 ? XA : ZA).normalize();
    if (tails === 2) {
      C.copy(P).addScaledVector(D, HL + TL / 2).addScaledVector(sideV, 0.25); m4.compose(C, q, ONE); tA.setMatrixAt(i, m4);
      C.addScaledVector(sideV, -0.5); m4.compose(C, q, ONE); tB.setMatrixAt(i, m4);
    } else { C.copy(P).addScaledVector(D, HL + TL / 2); m4.compose(C, q, ONE); tA.setMatrixAt(i, m4); tB.setMatrixAt(i, ZERO); }
  }
  heads.instanceMatrix.needsUpdate = tA.instanceMatrix.needsUpdate = tB.instanceMatrix.needsUpdate = true;
  const done = f >= 1;
  lHead.show = lTail.show = f > 0.75; lName.show = f > 0.6; lIn.show = kindNow === 'ves' && f > 0.75;
  if (hud) hud.innerHTML = '<b>' + NAME[kindNow][0] + '</b>：' + (done ? 'できあがり（熱でゆれ続ける）' : '分子が集まっているところ…') + (SM ? '' : '<br>尾が' + tails + '本の分子・' + (air ? '水面あり' : '水中') + '（上の選択と連動）<br><span style="font-size:11px;color:#64748b">できあがる形の模式図です（上の図の計算結果そのものではありません）</span>');
});
