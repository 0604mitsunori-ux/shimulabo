// 膜輸送 3D（細胞膜の一部を立体に。上が細胞外・下が細胞内。大きさ・形は誇張した模式）
// 上の2D（window.__yuso）の粒・タンパク質・ゲート・ATP・速さ・一時停止をそのまま読んで立体に置く。
// 膜タンパク質は手前の列に並べ、手前のリン脂質を切り取って断面が見えるようにしている
import { THREE, createView } from '../../assets/three/sim3d.js';
const $ = id => document.getElementById(id);
const Y = window.__yuso;
const K = 0.05, W = 640, MT = 180, MB = 216, MID = (MT + MB) / 2, DZ = 4.4, PZ = 3.0;   // 2Dの1px = 0.05
const X3 = x => (x - W / 2) * K, Y3 = y => (MID - y) * K;
const SM = matchMedia('(max-width:640px)').matches;
const v = createView($('view3d'), {
  views: {
    persp: { tgt: [0, 0, 0], dist: 42, th: 0.5, ph: 0.3 },
    side: { tgt: [0, 0, 0], dist: 37, th: 0, ph: 0 },
    top: { tgt: [0, 0, 0], dist: 38, th: 0, ph: 1.42 },
  },
  camRow: '#camRow3d', bg: 0xf1f5f9, shadows: false, minDist: 8, maxDist: 120,
});
const { scene } = v;
v.sun.position.set(20, 40, 50); v.sun.intensity = 1.3;
const O = new THREE.Object3D();
const pm = (c, o = {}) => new THREE.MeshStandardMaterial({ color: c, roughness: 0.5, ...o });

// ---- 細胞外（青）・細胞内（黄）の奥の壁 ----
const wall = (c, y) => { const m = new THREE.Mesh(new THREE.PlaneGeometry(32, 9), new THREE.MeshBasicMaterial({ color: c })); m.position.set(0, y, -DZ - 0.4); scene.add(m); };
wall(0xe3eefc, 5.35); wall(0xfdf6cf, -5.35);

// ---- リン脂質の二重層（頭＝赤、尾＝黄。熱でゆれる） ----
const SPX = 0.62, cols = Math.floor(32 / SPX), rows = Math.floor(2 * DZ / SPX) + 1, lip = [];
for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) for (const s of [1, -1])
  lip.push({ x: (c - (cols - 1) / 2) * SPX + (r % 2 ? SPX / 4 : -SPX / 4), z: (r - (rows - 1) / 2) * SPX, s, ph: Math.random() * 6.283, on: true });
const NL = lip.length;
const heads = new THREE.InstancedMesh(new THREE.SphereGeometry(0.25, 10, 8), pm(0xe0483e), NL);
const tails = new THREE.InstancedMesh(new THREE.CylinderGeometry(0.045, 0.045, 0.6, 5), pm(0xe6b422), NL * 2);
heads.frustumCulled = tails.frustumCulled = false; scene.add(heads, tails);
function drawLipids(t) {
  for (let i = 0; i < NL; i++) {
    const L = lip[i];
    if (!L.on) { O.position.set(0, 0, 0); O.rotation.set(0, 0, 0); O.scale.setScalar(0.0001); O.updateMatrix(); heads.setMatrixAt(i, O.matrix); tails.setMatrixAt(2 * i, O.matrix); tails.setMatrixAt(2 * i + 1, O.matrix); continue; }
    const wx = Math.sin(t * 2.3 + L.ph) * 0.07, wz = Math.cos(t * 1.9 + L.ph * 1.7) * 0.07, wy = Math.sin(t * 3.1 + L.ph * 2.3) * 0.04;
    O.scale.setScalar(1); O.rotation.set(0, 0, 0); O.position.set(L.x + wx, L.s * (0.72 + wy), L.z + wz); O.updateMatrix(); heads.setMatrixAt(i, O.matrix);
    for (let k = 0; k < 2; k++) {
      const sw = Math.sin(t * 2.7 + L.ph * 3 + k * 1.3) * 0.2;
      O.position.set(L.x + wx * 0.6 + (k ? 0.09 : -0.09), L.s * 0.36, L.z + wz * 0.6); O.rotation.set(sw * 0.6, 0, sw); O.updateMatrix(); tails.setMatrixAt(2 * i + k, O.matrix);
    }
  }
  heads.instanceMatrix.needsUpdate = true; tails.instanceMatrix.needsUpdate = true;
}

// ---- 粒（O₂・K⁺・Na⁺・グルコース。色は上の図と同じ） ----
const SPC = { o2: { c: 0xdc2626, r: 5 }, k: { c: 0xea580c, r: 6 }, na: { c: 0x7c3aed, r: 5.5 }, glc: { c: 0x16a34a, r: 6.5 } };
const CAP = 600, sphG = new THREE.SphereGeometry(1, 14, 10), hexG = new THREE.CylinderGeometry(1, 1, 0.7, 6); hexG.rotateX(Math.PI / 2);
const PM = {};
for (const k in SPC) { const m = new THREE.InstancedMesh(k === 'glc' ? hexG : sphG, pm(SPC[k].c, { roughness: 0.35 }), CAP); m.count = 0; m.frustumCulled = false; scene.add(m); PM[k] = m; }
const recs = new WeakMap();

// ---- 膜タンパク質（チャネル＝筒、担体・ポンプ＝2つのかたまりが傾いて向きを変える） ----
const PG = new THREE.Group(); scene.add(PG);
const subG = new THREE.CylinderGeometry(0.42, 0.42, 2.3, 14), gateG = new THREE.CylinderGeometry(0.5, 0.5, 0.35, 16), lobeG = new THREE.CylinderGeometry(0.5, 0.5, 2.3, 18);
let P3 = [], sig = '', tl = 0, lastHud = '';
const plab = Array.from({ length: 5 }, () => { const l = v.label('', [0, 0, 0]); l.show = false; return l; });
const pname = q => q.ty === 'ch' ? (q.sp === 'k' ? 'K⁺' : 'Na⁺') + 'チャネル' : q.ty === 'ca' ? '担体' : (SM ? 'ポンプ' : 'ナトリウムポンプ');
function build(prots) {
  PG.clear(); P3 = [];
  prots.forEach(q => {
    const g = new THREE.Group(); g.position.set(X3(q.x), 0, PZ); PG.add(g);
    const o = { g, gk: 0 };
    if (q.ty === 'ch') {
      const col = q.sp === 'k' ? 0xfb923c : 0xa78bfa;
      for (let a = 0; a < 6; a++) { const th = a * Math.PI / 3 + Math.PI / 6, front = Math.sin(th) > 0.3;
        const m = new THREE.Mesh(subG, pm(col, front ? { transparent: true, opacity: 0.22, depthWrite: false } : {})); m.position.set(Math.cos(th) * 0.86, 0, Math.sin(th) * 0.86); g.add(m); }
      o.gate = new THREE.Mesh(gateG, pm(q.sp === 'k' ? 0x9a3412 : 0x5b21b6)); o.gate.position.y = 0.35; g.add(o.gate); o.R = 1.5;
    } else {
      const pu = q.ty === 'pu', dx = pu ? 1.25 : 0.9;
      o.mat = pm(pu ? 0xfda4af : 0x86efac, { emissive: 0xffc400, emissiveIntensity: 0 });
      o.L = new THREE.Mesh(lobeG, o.mat); o.Rt = new THREE.Mesh(lobeG, o.mat);
      o.L.position.x = -dx; o.Rt.position.x = dx; o.L.scale.set(pu ? 1.25 : 0.95, pu ? 1.18 : 1, 1.7); o.Rt.scale.copy(o.L.scale); g.add(o.L, o.Rt); o.R = pu ? 2.2 : 1.65;
      if (pu) { o.atp = new THREE.Mesh(sphG, new THREE.MeshBasicMaterial({ color: 0xffc400, transparent: true, opacity: 0.85 })); o.atp.position.set(0, -2.0, 0); o.atp.scale.setScalar(0.001); g.add(o.atp); }
    }
    P3.push(o);
  });
  for (const L of lip) L.on = !prots.some((q, i) => { const dx = L.x - X3(q.x), R = P3[i].R; return dx * dx + (L.z - PZ) ** 2 < R * R || (Math.abs(dx) < R * 0.85 && L.z > PZ); });
  plab.forEach((l, i) => { const q = prots[i]; l.show = !!q && !(SM && prots.length > 3 && i % 2); if (q) { l.set(pname(q)); l.at(X3(q.x), 1.9, PZ); } });
}

// ---- 文字 ----
v.label(SM ? '細胞外' : '細胞外（上）', [-13, 8.3, 0], { sub: true });
v.label(SM ? '細胞内' : '細胞内（下）', [13, -8.3, 0], { sub: true });
const lLip = v.label(SM ? '脂質二重層' : 'リン脂質の二重層', [-13.5, 1.5, -DZ + 1]);
const lAtp = v.label('ATP → ADP＋リン酸', [0, -2.9, PZ], { accent: true }); lAtp.show = false;
const hud = $('hud3d'); hud.style.display = '';
if (SM) { hud.style.fontSize = '11px'; hud.style.padding = '3px 6px'; hud.style.left = hud.style.top = '6px'; }
const NAME = { diff: '単純拡散', chan: 'チャネル', carr: '担体', pump: 'ナトリウムポンプ', cell: '細胞のようす' };
const KIND = { diff: '受動輸送（ATPを使わない）', chan: '受動輸送（ATPを使わない）', carr: '受動輸送（ATPを使わない）', pump: '能動輸送（ATPを使う）', cell: '受動輸送＋能動輸送' };

// ---- 毎フレーム ----
v.onFrame((t, dt) => {
  const S = Y.st(), run = S.paused ? 0 : (S.spd || 1);
  tl += dt * run;
  const s0 = S.mode + '#' + S.prots.map(q => q.ty + q.sp + q.x).join('|');
  if (s0 !== sig) { sig = s0; build(S.prots); }
  drawLipids(tl);
  // タンパク質の形（2Dの状態と同じ）
  S.prots.forEach((q, i) => {
    const o = P3[i]; if (!o) return; const f = q.ph === 'flip' ? Math.min(1, q.t / 0.6) : 0;
    if (q.ty === 'ch') { o.gk += ((S.gateOpen ? 0 : 1) - o.gk) * Math.min(1, dt * 10); o.gate.visible = o.gk > 0.02; o.gate.scale.set(Math.max(0.01, o.gk), 1, Math.max(0.01, o.gk)); }
    else if (q.ty === 'ca') { const s = q.ph === 'flip' ? (q.from === 'o' ? 1 - 2 * f : -1 + 2 * f) : (q.side === 'o' ? 1 : -1); o.L.rotation.z = 0.28 * s; o.Rt.rotation.z = -0.28 * s; }
    else { const s = q.ph === 'flip' ? (q.side === 'i' ? f : 1 - f) : (q.side === 'o' ? 1 : 0), e = (S.flashT > 0 && S.flashX === q.x) ? Math.min(1, S.flashT / 0.9) : 0;
      o.L.rotation.z = 0.3 * (2 * s - 1); o.Rt.rotation.z = -0.3 * (2 * s - 1); o.mat.emissiveIntensity = e * 0.9; o.atp.scale.setScalar(0.001 + e * 0.8); }
  });
  lAtp.show = S.flashT > 0; if (lAtp.show) lAtp.at(X3(S.flashX), -2.9, PZ);
  // 粒
  const n = { o2: 0, k: 0, na: 0, glc: 0 };
  for (const p of S.parts) {
    let r = recs.get(p); if (!r) { r = { zb: (Math.random() * 2 - 1) * (DZ - 0.6), ph: Math.random() * 6.283, w: 0 }; recs.set(p, r); }
    const inP = p.st === 'bound' || (p.st === 'cross' && p.sp !== 'o2');
    let wT = inP ? 1 : 0;
    if (!inP) for (const q of S.prots) {   // 入口に近づいた粒は、タンパク質のある列へ寄る
      const ok = q.ty === 'ch' ? (q.sp === p.sp && S.gateOpen) : q.ty === 'ca' ? p.sp === 'glc' : (p.sp === 'na' || p.sp === 'k'); if (!ok) continue;
      wT = Math.max(wT, 1 - Math.hypot(p.x - q.x, p.y - (p.y < MID ? MT : MB)) / 55);
    }
    r.w += (wT - r.w) * Math.min(1, dt * run * (wT > r.w ? 9 : 1.2));
    const zf = Math.max(-DZ + 0.5, Math.min(DZ - 0.5, r.zb + Math.sin(tl * 0.6 + r.ph) * 0.7)), z = zf + (PZ - zf) * r.w;
    const i = n[p.sp]++; if (i >= CAP) continue;
    const rr = SPC[p.sp].r * K * 1.05, o2 = p.sp === 'o2';
    O.position.set(X3(p.x), Y3(p.y), z); O.rotation.set(0, 0, o2 ? r.ph + tl * 1.5 : 0); O.scale.set(o2 ? rr * 1.45 : rr, o2 ? rr * 0.8 : rr, o2 ? rr * 0.8 : rr); O.updateMatrix(); PM[p.sp].setMatrixAt(i, O.matrix);
  }
  for (const k in PM) { PM[k].count = Math.min(CAP, n[k]); PM[k].instanceMatrix.needsUpdate = true; }
  // 左上の表示
  const m = S.mode;
  let h = '<b>' + NAME[m] + '</b>：' + KIND[m];
  if (m === 'pump' || m === 'cell') h += '<br>ATP 使った数 <b>' + S.used + '</b>・残り <b>' + S.atp + '</b>' + (SM ? '' : '<br>ATP 1個で、Na⁺ 3個を外へ・K⁺ 2個を内へ');
  else if (m === 'chan') h += '<br>' + (S.gateOpen ? 'チャネルは<b>開</b>：濃度の高い側 → 低い側へ' : 'チャネルは<b>閉</b>：イオンは通れない');
  else if (!SM) h += '<br>' + (m === 'diff' ? 'リン脂質のすき間を、濃度の高い側 → 低い側へ' : '担体が形を変えて、1個ずつ運ぶ（高い側 → 低い側へ）');
  if (S.paused) h += '<br>一時停止中';
  if (h !== lastHud) { lastHud = h; hud.innerHTML = h; }
});
