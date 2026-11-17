// 状態変化 3D（上の図の容器を立体に。温度・状態・粒子の内わけ・ピストンの高さは、上の図の値をそのまま読む）
// 1 = 100px（上の図と同じ比率）。x＝図の左右、y＝図の上下（底が0）、z＝奥行き（上の図の48個を、奥に4列ならべた模式）
// 粒子の動きは見た目用の乱数。動かし方の式（ふるえの大きさ・液体のゆれ・気体の速さ）は上の図の step() と同じ
import { THREE, createView, mat } from '../../assets/three/sim3d.js';
const $ = id => document.getElementById(id);
const J = window.__joutai;
if (!J) throw new Error('joutai-henka: hook がありません');
const { NP, PD, PR, X0, X1, WC, FY, WALLTOP, PS } = J;
const DL = 4, N = NP * DL, U = 0.01;                       // 奥に4列 → 192個
const CX = X0 + WC / 2, DZ = DL * PD + PR, ZM = DZ / 2 - PR; // 奥行き（px）と、粒子の中心が動ける幅
const BW = WC * U, BH = (FY - WALLTOP) * U, BD = DZ * U;    // 容器 1.75 × 3.12 × 0.63
const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
const rnd = (a, b) => a + Math.random() * (b - a);
const SM = innerWidth < 520;

const TG = [0, BH * 0.51, 0];                              // 箱のまん中より少し上を見る（左上のHUDと重ならないように）
const v = createView($('view3d'), {
  views: {
    persp: { tgt: TG, dist: 8.2, th: 0.6, ph: 0.3 },
    front: { tgt: TG, dist: 7.6, th: 0, ph: 0 },
    top: { tgt: TG, dist: 5.0, th: 0, ph: 1.45 },
  },
  camRow: '#camRow3d', bg: 0xf1f5f9, shadows: false, minDist: 2, maxDist: 20,
});
const { scene } = v;

// ---- 容器（透明な箱）・底・ピストン ----
const boxGeo = new THREE.BoxGeometry(1, 1, 1), edgeGeo = new THREE.EdgesGeometry(boxGeo);
const lineMat = new THREE.LineBasicMaterial({ color: 0x64748b });
const glass = new THREE.Mesh(boxGeo, new THREE.MeshBasicMaterial({ color: 0x94a3b8, transparent: true, opacity: 0.07, depthWrite: false, side: THREE.DoubleSide }));
glass.scale.set(BW, BH, BD); glass.position.set(0, BH / 2, 0); scene.add(glass);
const rim = new THREE.LineSegments(edgeGeo, lineMat); rim.scale.copy(glass.scale); rim.position.copy(glass.position); scene.add(rim);
const floor = new THREE.Mesh(boxGeo, mat(0x94a3b8)); floor.scale.set(BW + 0.08, 0.04, BD + 0.08); floor.position.set(0, -0.02, 0); scene.add(floor);
const pist = new THREE.Group(); scene.add(pist);            // y＝ピストンの下の面
{ const plate = new THREE.Mesh(boxGeo, new THREE.MeshStandardMaterial({ color: 0xcbd5e1, transparent: true, opacity: 0.35, depthWrite: false, roughness: 0.6 }));
  plate.scale.set(BW - 0.02, 0.1, BD - 0.02); plate.position.y = 0.05;
  const pe = new THREE.LineSegments(edgeGeo, lineMat); pe.scale.copy(plate.scale); pe.position.y = 0.05;
  const rod = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 0.14, 12), mat(0x94a3b8)); rod.position.y = 0.17;
  const knob = new THREE.Mesh(boxGeo, mat(0x64748b)); knob.scale.set(0.26, 0.05, 0.26); knob.position.y = 0.265;
  pist.add(plate, pe, rod, knob); }
// 液体の層（うすい色）と、加熱中の炎
const liq = new THREE.Mesh(boxGeo, new THREE.MeshBasicMaterial({ color: 0x3b82f6, transparent: true, opacity: 0.13, depthWrite: false })); scene.add(liq);
const flame = new THREE.Mesh(new THREE.ConeGeometry(0.15, 0.36, 20), new THREE.MeshBasicMaterial({ color: 0xf97316 })); flame.position.set(0, -0.24, 0); flame.visible = false; scene.add(flame);

// ---- 粒子（1つの形・1つの色を N 個） ----
const mesh = new THREE.InstancedMesh(new THREE.SphereGeometry((PR - 0.5) * U, 16, 12), new THREE.MeshStandardMaterial({ color: 0x3b82f6, roughness: 0.45 }), N);
mesh.frustumCulled = false; mesh.instanceMatrix.setUsage(THREE.DynamicDrawUsage); scene.add(mesh);
const M = mesh.instanceMatrix.array;
for (let j = 0; j < N; j++) { const o = j * 16; M.fill(0, o, o + 16); M[o] = M[o + 5] = M[o + 10] = M[o + 15] = 1; }
// 位置と速さは上の図と同じ px（y は下向きが＋）。ph: 0＝固体 1＝液体 2＝気体
const px = new Float32Array(N), py = new Float32Array(N), pz = new Float32Array(N);
const vx = new Float32Array(N), vy = new Float32Array(N), vz = new Float32Array(N);
const ph = new Uint8Array(N), out = new Uint8Array(N), sx = new Float32Array(NP), sy = new Float32Array(NP);
const w = new Float32Array(N * 3), f = new Float32Array(N * 3);
for (let i = 0; i < N * 3; i++) { w[i] = rnd(5, 9); f[i] = rnd(0, 6.28); }
const ZL = d => (d - (DL - 1) / 2) * PD;                    // 奥の列の位置
const phaseOf = (i, s) => i < s.ns ? 0 : (PS[i].gr < s.ng ? 2 : 1);   // 上の図の粒子 i と同じ状態
function sites(s) { for (let i = 0; i < s.ns; i++) { const q = J.site(i); sx[i] = q[0]; sy[i] = q[1]; } }

function place(s) {
  const G = s.G; sites(s);
  for (let j = 0; j < N; j++) {
    const i = j % NP, k = ph[j] = phaseOf(i, s); vx[j] = vy[j] = vz[j] = 0; out[j] = 0;
    if (k === 0) { px[j] = sx[i]; py[j] = sy[i]; pz[j] = ZL((j / NP) | 0); continue; }
    px[j] = rnd(X0 + PR, X1 - PR); pz[j] = rnd(-ZM, ZM);
    if (k === 1) py[j] = rnd(G.lt + PR, G.lb - PR);
    else { py[j] = rnd(s.pistY + PR, G.top - PR); vx[j] = rnd(-1.4, 1.4); vy[j] = rnd(-1.4, 1.4); vz[j] = rnd(-1.4, 1.4); }
  }
}
function step(s, t) {
  const S = s.S, T = s.cur.T, G = s.G;
  const sf = clamp((T - S.lo) / (S.mp - S.lo), 0, 1), lf = clamp((T - S.mp) / (S.bp - S.mp), 0, 1), gf = clamp((T - S.bp) / (S.hi - S.bp), 0, 1);
  const A = 0.4 + 1.6 * sf, kick = 0.6 + 0.8 * lf, vg = 2.1 + 1.5 * gf;
  sites(s);
  for (let j = 0; j < N; j++) {
    const i = j % NP, k = phaseOf(i, s);
    if (k !== ph[j]) { if (k === 2) { vx[j] = rnd(-1, 1); vy[j] = -rnd(1.6, 2.6); vz[j] = rnd(-1, 1); } else { vx[j] *= 0.2; vy[j] *= 0.2; vz[j] *= 0.2; } ph[j] = k; }
    if (k === 0) {                                          // 固体：決まった場所で小さくふるえる
      const o = j * 3;
      px[j] += (sx[i] + A * Math.sin(t * w[o] + f[o]) - px[j]) * 0.3;
      py[j] += (sy[i] + A * Math.sin(t * w[o + 1] + f[o + 1]) - py[j]) * 0.3;
      pz[j] += (ZL((j / NP) | 0) + A * Math.sin(t * w[o + 2] + f[o + 2]) - pz[j]) * 0.3;
    } else if (k === 1) {                                   // 液体：下にたまり、ゆっくり動きまわる（層いっぱいに広がるよう、下向きの力は上の図より弱め）
      vx[j] = (vx[j] + (Math.random() - 0.5) * kick) * 0.86; vy[j] = (vy[j] + (Math.random() - 0.5) * kick + 0.02) * 0.86; vz[j] = (vz[j] + (Math.random() - 0.5) * kick) * 0.86;
      px[j] += vx[j]; py[j] += vy[j]; pz[j] += vz[j];
    } else {                                                // 気体：速くまっすぐ飛び、少しずつ向きが変わる
      const g = 1 + (vg / (Math.hypot(vx[j], vy[j], vz[j]) || 1) - 1) * 0.08;
      vx[j] = vx[j] * g + (Math.random() - 0.5) * 0.3; vy[j] = vy[j] * g + (Math.random() - 0.5) * 0.3; vz[j] = vz[j] * g + (Math.random() - 0.5) * 0.3;
      px[j] += vx[j]; py[j] += vy[j]; pz[j] += vz[j];
    }
  }
  // 重なりをほどく（液体どうし・液体と固体だけ。簡単な押しもどし）
  if (s.nl > 0) for (let a = 0; a < N; a++) {
    const ka = ph[a]; if (ka === 2) continue;
    for (let b = a + 1; b < N; b++) {
      const kb = ph[b]; if (kb === 2 || (ka === 0 && kb === 0)) continue;
      const dx = px[b] - px[a]; if (dx >= PD || dx <= -PD) continue;
      const dy = py[b] - py[a]; if (dy >= PD || dy <= -PD) continue;
      const dz = pz[b] - pz[a], d2 = dx * dx + dy * dy + dz * dz; if (d2 >= PD * PD) continue;
      const d = Math.sqrt(d2) || 0.01, ov = (PD - d) / d;
      if (ka === 1 && kb === 1) { const m = ov * 0.4; px[a] -= dx * m; py[a] -= dy * m; pz[a] -= dz * m; px[b] += dx * m; py[b] += dy * m; pz[b] += dz * m; }
      else if (ka === 1) { if (!out[a]) { const m = ov * 0.8; px[a] -= dx * m; py[a] -= dy * m; pz[a] -= dz * m; } }
      else if (!out[b]) { const m = ov * 0.8; px[b] += dx * m; py[b] += dy * m; pz[b] += dz * m; }
    }
  }
  // かべ・底・ピストン・層の境目
  const xa = X0 + PR, xb = X1 - PR, lt = G.lt + PR, lb = G.lb - PR, gt = s.pistY + PR, gb = G.top - PR;
  for (let j = 0; j < N; j++) {
    const k = ph[j]; if (k === 0) continue;
    if (px[j] < xa) { px[j] = xa; vx[j] = Math.abs(vx[j]); } else if (px[j] > xb) { px[j] = xb; vx[j] = -Math.abs(vx[j]); }
    if (pz[j] < -ZM) { pz[j] = -ZM; vz[j] = Math.abs(vz[j]); } else if (pz[j] > ZM) { pz[j] = ZM; vz[j] = -Math.abs(vz[j]); }
    if (k === 1) {
      out[j] = (py[j] < lt - 6 || py[j] > lb + 6) ? 1 : 0;   // 層の外にいる液体は、固体をすり抜けて層へもどる
      if (py[j] > lb) { const dd = py[j] - lb; py[j] = dd > 4 ? py[j] - dd * 0.3 : lb; vy[j] = -Math.abs(vy[j]) * 0.5; }
      else if (py[j] < lt) { const dd = lt - py[j]; if (dd > 8) { py[j] += dd * 0.12; vy[j] = Math.max(vy[j], 0); } else { vy[j] += dd * 0.2; if (dd > 3) py[j] = lt - 3; } }
    } else {
      if (py[j] < gt) { py[j] = gt; vy[j] = Math.abs(vy[j]); }
      if (py[j] > gb) { if (vy[j] > 0 && py[j] - vy[j] <= gb + 0.5) { py[j] = gb; vy[j] = -Math.abs(vy[j]); } else vy[j] = Math.min(vy[j], -1.2); }
      if (py[j] > FY - PR) { py[j] = FY - PR; vy[j] = -Math.abs(vy[j]); }
    }
  }
}

// ---- ラベル ----
const LX = BW / 2 + 0.34, Y3 = y => (FY - y) * U;
const lS = v.label('固体', [-LX, 0, 0]), lL = v.label('液体', [LX, 0, 0]), lG = v.label('気体', [-LX, 0, 0]);
const lP = v.label('ピストン', [0, 0, 0], { sub: true }), lRun = v.label('加熱中', [0.62, -0.42, 0], { accent: true });
const txt = id => { const e = $(id); return e ? e.textContent : ''; };
const hud = $('hud3d');
let acc = 0, simT = 0, lastSub = '', lastHud = '', lastRun = 0;
lRun.show = false;

v.onFrame((t, dt) => {
  const s = J.st(); if (!s.cur || !s.G) return;
  const G = s.G;
  if (s.S.n !== lastSub) {                                  // 物質を切りかえたら、色を変えて並べ直す
    lastSub = s.S.n; mesh.material.color.set(s.S.c); liq.material.color.set(s.S.c);
    place(s); for (let i = 0; i < 30; i++) step(s, simT += 1 / 60);
  }
  acc += dt; let n = 0; while (acc >= 1 / 60 && n < 4) { step(s, simT += 1 / 60); acc -= 1 / 60; n++; } if (n >= 4) acc = 0;
  for (let j = 0, o = 12; j < N; j++, o += 16) { M[o] = (px[j] - CX) * U; M[o + 1] = (FY - py[j]) * U; M[o + 2] = pz[j] * U; }
  mesh.instanceMatrix.needsUpdate = true;
  // ピストン・液体の層・炎（上の図と同じ高さ）
  const yp = Y3(s.pistY), yl0 = Y3(G.lb), yl1 = Y3(G.lt), yTop = Y3(G.top), ySol = Y3(G.bt);
  pist.position.y = yp;
  liq.visible = s.nl > 0; liq.position.y = (yl0 + yl1) / 2; liq.scale.set(BW - 0.01, Math.max(0.001, yl1 - yl0), BD - 0.01);
  flame.visible = s.run > 0; if (flame.visible) flame.scale.y = 1 + 0.12 * Math.sin(t * 20);
  if (s.run !== lastRun) { lastRun = s.run; lRun.show = s.run !== 0; if (s.run) lRun.set(s.run > 0 ? '加熱中' : '冷却中'); }
  const side = v.cam.ph < 1.1;                              // 真上からのときは、重なるので層の名前を消す
  lS.show = side && s.ns > 0; lL.show = side && s.nl > 0; lG.show = side && s.ng > 0;
  lS.at(-LX, (ySol + (s.S.ice ? yl1 : 0)) / 2 - 0.1, 0); lL.at(LX, (yl0 + yl1) / 2 - 0.1, 0); lG.at(-LX, (yp + yTop) / 2 - 0.1, 0);
  lP.show = side; lP.at(0, yp + 0.3, 0);
  // HUD：温度・状態・体積は、上の表示の文字をそのまま使う
  const tT = txt('sT'), tS = txt('sState'), tV = txt('sVol'), tL = J.longLabel(s.cur), key = s.S.n + '|' + tT + '|' + tS + '|' + tV + '|' + tL;
  if (key !== lastHud) {
    lastHud = key;
    hud.innerHTML = SM ? '<b>' + s.S.n + ' ' + tT + '</b>　<b>' + tS + '</b>'
      : '<b>' + s.S.n + '　' + tT + '</b>　状態：<b>' + tS + '</b><br><span style="font-size:11.5px">' + tL + '／体積（相対）' + tV + '</span>';
  }
});
hud.style.display = '';
