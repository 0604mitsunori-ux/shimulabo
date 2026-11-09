// 電流と磁界 3D（上の図の4つの実験を立体の模型にし、上の図の状態＝電流・向き・角度・磁石の位置をそのまま読んで動かす）
// ①②③はページの座標（x＝東、y＝北、z＝上）をそのまま使う（3Dでは x, z, −y）。④は上の図の横から見た配置（20px＝1）
import { THREE, createView } from '../../assets/three/sim3d.js';
const $ = id => document.getElementById(id);
const D = window.__denki;
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const V = (x, y, z) => new THREE.Vector3(x, z, -y);
const COL = { cur: 0xf97316, fld: 0x2563eb, frc: 0x16a34a, N: 0xdc2626, S: 0x2563eb, coil: 0xb45309, lead: 0x94a3b8, wire: 0x57534e };
const PI = Math.PI, UP = new THREE.Vector3(0, 1, 0);

const v = createView($('view3d'), {
  views: { persp: { tgt: [0, 0, 0], dist: 30, th: 0.55, ph: 0.5 }, front: { tgt: [0, 0, 0], dist: 28, th: 0, ph: 0.08 }, top: { tgt: [0, 0, 0], dist: 30, th: 0, ph: 1.45 } },
  camRow: '#camRow3d', bg: 0xf8fafc, shadows: false, minDist: 4, maxDist: 90,
});
const { scene } = v;
const SM = v.mobile;
const ZF = SM ? 0.88 : 1;
// 場面ごとのカメラ（注視点・距離）
const CAM = {
  wire: { tgt: [1.6, 0.6, 0], d: [30, 28, 30] }, coil: { tgt: [0, 0.6, 0], d: [27, 25, 27] }, mag: { tgt: [0, 2.6, 0.5], d: [30, 28, 30] },
  swing: { tgt: [0.2, 4.6, 0], d: [36, 33, 34], a: [-0.5, 0.26] }, motor: { tgt: [0, -0.6, 1.2], d: [25, 24, 26] }, move: { tgt: [2.2, 1.6, 0], d: [28, 26, 28] }, gen: { tgt: [1.6, 2.2, 0], d: [28, 26, 28] },
};

// ---- 道具 ----
const boxGeo = new THREE.BoxGeometry(1, 1, 1), cylGeo = new THREE.CylinderGeometry(1, 1, 1, 12), coneGeo = new THREE.ConeGeometry(1, 1, 14), ballGeo = new THREE.SphereGeometry(1, 12, 8);
const std = (c, o) => new THREE.MeshStandardMaterial(Object.assign({ color: c, roughness: 0.65 }, o || {}));
function boxM(x0, x1, y0, y1, z0, z1, col, parent) { const m = new THREE.Mesh(boxGeo, std(col)); m.scale.set(x1 - x0, z1 - z0, y1 - y0); m.position.set((x0 + x1) / 2, (z0 + z1) / 2, -(y0 + y1) / 2); parent.add(m); return m; }
function setSeg(m, a, b, r) { const d = new THREE.Vector3().subVectors(b, a), L = d.length(); m.visible = L > 1e-4; if (!m.visible) return; m.position.copy(a).addScaledVector(d, 0.5); m.scale.set(r, L, r); m.quaternion.setFromUnitVectors(UP, d.multiplyScalar(1 / L)); }
function segM(col, parent) { const m = new THREE.Mesh(cylGeo, std(col, { roughness: 0.5 })); parent.add(m); return m; }
function tubeOf(pts, r, col, parent, closed) { const m = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts, !!closed), Math.max(8, pts.length * 2), r, 8, !!closed), std(col, { roughness: 0.5 })); parent.add(m); return m; }
function polyTube(pts, r, col, parent) { const g = new THREE.Group(); for (let i = 1; i < pts.length; i++) setSeg(segM(col, g), pts[i - 1], pts[i], r); parent.add(g); return g; }
function mkArrow(col, parent) {
  const mat = std(col, { roughness: 0.4 }), g = new THREE.Group(), sh = new THREE.Mesh(cylGeo, mat), hd = new THREE.Mesh(coneGeo, mat); g.add(sh, hd); parent.add(g);
  g.set = (a, b, r) => { const d = new THREE.Vector3().subVectors(b, a), L = d.length(); g.visible = L > 0.05; if (!g.visible) return; const u = d.clone().multiplyScalar(1 / L), h = Math.min(L * 0.5, r * 4.5);
    setSeg(sh, a, b.clone().addScaledVector(u, -h), r); hd.position.copy(b).addScaledVector(u, -h / 2); hd.scale.set(r * 2.3, h, r * 2.3); hd.quaternion.setFromUnitVectors(UP, u); };
  return g;
}
// 電流の粒（道すじに沿って等間隔に流す）
function mkDots(n, r, parent) { const m = new THREE.InstancedMesh(ballGeo, std(COL.cur, { roughness: 0.4, emissive: 0x7c2d12, emissiveIntensity: 0.25 }), n); m.count = 0; parent.add(m); return m; }
const _M = new THREE.Matrix4(), _S = new THREE.Vector3(), _Q = new THREE.Quaternion();
function flowDots(m, pts, gap, off, r) {
  const L = [0]; for (let i = 1; i < pts.length; i++) L.push(L[i - 1] + pts[i].distanceTo(pts[i - 1]));
  const tot = L[L.length - 1]; let n = 0; if (tot < 0.01) { m.count = 0; return; }
  const o = ((off % gap) + gap) % gap; let j = 1;
  for (let s = o; s < tot && n < m.instanceMatrix.count; s += gap) { while (j < L.length - 1 && L[j] < s) j++; const t = (s - L[j - 1]) / Math.max(1e-6, L[j] - L[j - 1]);
    _S.lerpVectors(pts[j - 1], pts[j], t); _M.compose(_S, _Q, new THREE.Vector3(r, r, r)); m.setMatrixAt(n++, _M); }
  m.count = n; m.instanceMatrix.needsUpdate = true;
}
function compass(R, hl, parent) {
  const g = new THREE.Group(); parent.add(g);
  const disk = new THREE.Mesh(new THREE.CylinderGeometry(R, R, 0.14, 28), std(hl ? 0xfffbe6 : 0xffffff)); disk.position.y = 0.07; g.add(disk);
  const rim = new THREE.Mesh(new THREE.TorusGeometry(R, 0.05, 6, 32), std(hl ? 0xca8a04 : 0x64748b)); rim.rotation.x = PI / 2; rim.position.y = 0.15; g.add(rim);
  const nd = new THREE.Group(); nd.position.y = 0.22; g.add(nd);
  const L = R * 0.84, w = R * 0.22, half = (col, s) => { const m = new THREE.Mesh(new THREE.ConeGeometry(w, L, 4), std(col)); m.rotation.z = -s * PI / 2; m.position.x = s * L / 2; m.scale.x = 0.35; nd.add(m); };   // 平たい針（上下にうすく）
  half(COL.N, 1); half(0xe2e8f0, -1);
  g.needle = nd; return g;
}
const groups = {}; ['wire', 'coil', 'mag', 'swing', 'motor', 'move', 'gen'].forEach(k => { groups[k] = new THREE.Group(); groups[k].visible = false; scene.add(groups[k]); });
const L = {};   // 場面ごとの文字
const lab = (k, t, o) => { const l = v.label(t, [0, 0, 0], o || {}); (L[k] = L[k] || []).push(l); return l; };

// ================= ① 共通：厚紙（板）と方位磁針 =================
const BX = D.BX, BY = D.BY;
function board(parent) {
  boxM(-BX, BX, -BY, BY, -0.45, 0, 0xf3ecd9, parent);
  const n = new THREE.Group(); parent.add(n);
  mkArrow(0xa8a29e, n).set(V(-BX + 0.9, BY - 2.6, 0.05), V(-BX + 0.9, BY - 0.7, 0.05), 0.07);
}
const clip = [new THREE.Plane(new THREE.Vector3(-1, 0, 0), BX), new THREE.Plane(new THREE.Vector3(1, 0, 0), BX), new THREE.Plane(new THREE.Vector3(0, 0, -1), BY), new THREE.Plane(new THREE.Vector3(0, 0, 1), BY)];

// ---------------- ① まっすぐな導線 ----------------
const W = groups.wire, RX = 10.5, ZT = 6.4, ZB = -5.3;
board(W);
segM(COL.wire, W).userData.k = 0; setSeg(W.children[W.children.length - 1], V(0, 0, ZB), V(0, 0, ZT), 0.16);
polyTube([V(0, 0, ZT), V(RX, 0, ZT), V(RX, 0, ZB), V(0, 0, ZB)], 0.07, COL.lead, W);
const wBat = new THREE.Group(); W.add(wBat); { const b = new THREE.Mesh(cylGeo, std(0x111827)); b.scale.set(0.55, 2.2, 0.55); wBat.add(b); const c = new THREE.Mesh(cylGeo, std(0xca8a04)); c.scale.set(0.56, 0.5, 0.56); c.name = 'plus'; wBat.add(c); wBat.position.copy(V(RX, 0, 0.3)); }
const wDots = mkDots(60, 0.17, W), wCompass = D.CPW.map(() => compass(0.82, false, W)), wProbe = compass(1.1, true, W);
const wLines = new THREE.Group(); W.add(wLines);
const wArrow = mkArrow(COL.cur, W);
const lWcur = lab('wire', '電流', { accent: true }), lWfld = lab('wire', '磁力線（磁界の向き）'), lWbat = lab('wire', '電源', { sub: true }), lWprobe = lab('wire', '方位磁針（赤＝N極）', { sub: true }), lWn = lab('wire', '北', { sub: true });
let wKey = '';
function buildWireLines(I, s) {
  wLines.children.slice().forEach(c => { wLines.remove(c); c.geometry.dispose(); });
  if (I <= 0) return;
  const st = 0.6 / I, matB = std(COL.fld, { clippingPlanes: clip }), matF = std(COL.fld, { transparent: true, opacity: 0.28, depthWrite: false }), cone = new THREE.ConeGeometry(0.17, 0.5, 12);
  let k = 0;
  for (let lr = Math.log(0.72); lr < Math.log(9.6); lr += st, k++) {
    const r = Math.exp(lr), pts = []; for (let j = 0; j < 72; j++) { const t = j / 72 * 2 * PI; pts.push(new THREE.Vector3(r * Math.cos(t), 0.04, -r * Math.sin(t))); }
    wLines.add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts, true), 72, 0.035, 5, true), matB));
    if (r < 3.2) [-3.4, 3.4].forEach(h => { const q = pts.map(p => new THREE.Vector3(p.x, h, p.z)); wLines.add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(q, true), 72, 0.025, 4, true), matF)); });   // 板の上と下にも同じ円（どの高さにも磁界がある）
    if (r > 1.5) [0.55 + 0.9 * k, 0.55 + 0.9 * k + PI].forEach(t0 => { const x = r * Math.cos(t0), y = r * Math.sin(t0); if (Math.abs(x) > BX - 0.4 || Math.abs(y) > BY - 0.4) return;
      const c = new THREE.Mesh(cone, matB); c.position.set(x, 0.06, -y); c.quaternion.setFromUnitVectors(UP, new THREE.Vector3(-Math.sin(t0) * s, 0, -Math.cos(t0) * s)); wLines.add(c); });
  }
}
function wire(st) {
  const I = st.I, s = st.dirI;
  if (wKey !== I + '|' + s) { wKey = I + '|' + s; buildWireLines(I, s); }
  wBat.getObjectByName('plus').position.y = s > 0 ? -0.85 : 0.85;   // ＋極（電流は＋極から出る）
  flowDots(wDots, I > 0 ? [V(0, 0, ZB), V(0, 0, ZT), V(RX, 0, ZT), V(RX, 0, ZB), V(0, 0, ZB)] : [], 1.1, st.wo * 0.045, 0.17);
  D.CPW.forEach((c, i) => { const g = wCompass[i]; g.position.copy(V(c[0], c[1], 0)); g.needle.rotation.y = st.nd['w' + i] || 0; });
  wProbe.position.copy(V(st.probe[0], st.probe[1], 0)); wProbe.needle.rotation.y = st.nd.wp || 0;
  wArrow.set(V(-0.6, 0, s > 0 ? 2.4 : 4.6), V(-0.6, 0, s > 0 ? 4.6 : 2.4), 0.09); wArrow.visible = I > 0;
  lWcur.at(-0.6, 3.5, 0); lWcur.show = I > 0;
  lWfld.at(3.3, 0.3, -3.3); lWfld.show = I > 0;
  lWbat.at(RX, 1.8, 0); lWbat.show = true; lWprobe.at(st.probe[0], 1.6, -st.probe[1]); lWprobe.show = !SM; lWn.at(-BX + 0.9, 0.4, -(BY - 0.3)); lWn.show = true;
  return '電流 <b>' + I.toFixed(1) + ' A</b>・' + (s > 0 ? '下から上へ' : '上から下へ')
    + (SM ? '' : '<br>磁力線は導線を中心にした円（上から見て' + (s > 0 ? '反時計回り' : '時計回り') + '）。板の上や下でも同じ形<br><span style="font-size:11px;color:#64748b">' + (st.earth ? '方位磁針は地球の磁界（北向き）も受けています' : '地球の磁界は小さいとして、導線の磁界だけで向きを決めています') + '</span>');
}

// ---------------- ① コイル ----------------
const CO = groups.coil, CN = D.CN, CL = D.CL, CA = D.CA, ZL = 4.6;
board(CO);
{ const pts = [], n = CN * 40; for (let k = 0; k <= n; k++) { const t = 2 * PI * CN * k / n; pts.push(V(-CL / 2 + CL * t / (2 * PI * CN), -CA * Math.cos(t), CA * Math.sin(t))); }
  CO.userData.helix = pts; tubeOf(pts, 0.1, COL.coil, CO); }
CO.userData.path = [V(-1.7, -CA, ZL), V(-CL / 2, -CA, ZL), ...CO.userData.helix, V(CL / 2, -CA, ZL), V(1.7, -CA, ZL)];
polyTube([V(-CL / 2, -CA, 0), V(-CL / 2, -CA, ZL), V(-1.7, -CA, ZL)], 0.08, COL.coil, CO); polyTube([V(1.7, -CA, ZL), V(CL / 2, -CA, ZL), V(CL / 2, -CA, 0)], 0.08, COL.coil, CO);
const cBat = new THREE.Group(); CO.add(cBat); { const b = new THREE.Mesh(cylGeo, std(0x111827)); b.scale.set(0.5, 3.4, 0.5); b.rotation.z = PI / 2; cBat.add(b); const c = new THREE.Mesh(cylGeo, std(0xca8a04)); c.scale.set(0.51, 0.5, 0.51); c.rotation.z = PI / 2; c.name = 'plus'; cBat.add(c); cBat.position.copy(V(0, -CA, ZL)); }
const cDots = mkDots(90, 0.15, CO), cCompass = D.CPC.map(() => compass(0.72, false, CO)), cProbe = compass(1.1, true, CO), cLines = new THREE.Group(); CO.add(cLines);
const lCN = lab('coil', 'N極', { accent: true }), lCS = lab('coil', 'S極', { accent: true }), lCbat = lab('coil', '電源', { sub: true }), lCfld = lab('coil', '磁力線', { sub: true });
let cKey = '';
function traceCoil() {
  cLines.children.slice().forEach(c => { cLines.remove(c); if (c.geometry !== coneC) c.geometry.dispose(); });
  const list = D.coilList(1), B = (x, y) => { const b = D.Bsum(list, x, y), m = Math.hypot(b[0], b[1]) || 1; return [b[0] / m, b[1] / m]; };
  const matB = std(COL.fld, { clippingPlanes: clip }), matF = std(COL.fld, { transparent: true, opacity: 0.25, depthWrite: false, clippingPlanes: clip });
  [-2.9, -1.4, -0.95, -0.5, 0.5, 0.95, 1.4, 2.9].forEach(y0 => {
    const run = sgn => { const out = []; let x = 0, y = y0; const h = 0.06 * sgn;
      for (let n = 0; n < 2400; n++) { const a = B(x, y), b = B(x + a[0] * h / 2, y + a[1] * h / 2); x += b[0] * h; y += b[1] * h; out.push([x, y]);
        if (Math.abs(x) > BX + 0.3 || Math.abs(y) > BY + 0.3) return { pts: out, closed: false };
        if (n > 60 && Math.hypot(x, y - y0) < 0.07) return { pts: out, closed: true }; }
      return { pts: out, closed: false }; };
    const f = run(1); let pts = f.pts; if (!f.closed) pts = run(-1).pts.reverse().concat([[0, y0]], f.pts);
    if (pts.length < 4) return;
    const P3 = pts.filter((_, i) => i % 3 === 0).map(p => new THREE.Vector3(p[0], 0.05, -p[1]));
    cLines.add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(P3, false), P3.length, 0.035, 5, false), matB));
    [PI / 3, 2 * PI / 3].forEach(ph => { const q = P3.map(p => new THREE.Vector3(p.x, -p.z * Math.sin(ph), p.z * Math.cos(ph))); cLines.add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(q, false), q.length, 0.025, 4, false), matF)); });
    [0.2, 0.45, 0.7, 0.95].forEach(u => { const i = Math.floor(u * (P3.length - 2)), a = P3[i], b = P3[i + 1]; if (Math.abs(a.x) > BX - 0.4 || Math.abs(a.z) > BY - 0.4) return;
      const c = new THREE.Mesh(coneC, matB); c.position.copy(a); c.quaternion.setFromUnitVectors(UP, b.clone().sub(a).normalize()); cLines.add(c); });
  });
}
const coneC = new THREE.ConeGeometry(0.17, 0.5, 12);
function coil(st) {
  const I = st.I, s = st.dirI;
  if (cKey !== String(s)) { cKey = String(s); traceCoil(); }
  cLines.visible = I > 0;
  cBat.getObjectByName('plus').position.x = s > 0 ? -1.45 : 1.45;   // 電流は＋極から出る
  flowDots(cDots, I > 0 ? CO.userData.path : [], 0.9, st.wo * 0.04, 0.15);
  D.CPC.forEach((c, i) => { const g = cCompass[i]; g.position.copy(V(c[0], c[1], 0)); g.needle.rotation.y = st.nd['c' + i] || 0; });
  cProbe.position.copy(V(st.probe[0], st.probe[1], 0)); cProbe.needle.rotation.y = st.nd.cp || 0;
  const lN = s > 0; lCN.at(lN ? -CL / 2 - 1.2 : CL / 2 + 1.2, 1.4, 0); lCS.at(lN ? CL / 2 + 1.2 : -CL / 2 - 1.2, 1.4, 0); lCN.show = lCS.show = I > 0;
  lCN.el.style.background = '#dc2626'; lCN.el.style.borderColor = '#dc2626'; lCS.el.style.background = '#2563eb'; lCS.el.style.borderColor = '#2563eb';
  lCbat.at(0, ZL + 0.9, CA); lCbat.show = true; lCfld.at(0, 0.3, -4.6); lCfld.show = I > 0 && !SM;
  return '電流 <b>' + I.toFixed(1) + ' A</b>・' + (I > 0 ? (s > 0 ? '左' : '右') + 'のはしがN極' : '電流が流れていない')
    + (SM ? '' : '<br>コイルの中では磁力線がほぼ平行（棒磁石と同じ形の磁界）<br><span style="font-size:11px;color:#64748b">濃い線＝板の上、うすい線＝板をななめに切った面（模式）</span>');
}

// ---------------- ② 電磁石 ----------------
const MG = groups.mag, CY = 4, CR = 0.6, X0 = -6.6, X1 = 6.6, C0 = -3.7, C1 = 4.4;
boxM(-12, 12, -5, 5, -0.4, 0, 0xf3ecd9, MG);
[-4.4, 5.6].forEach(x => boxM(x - 0.2, x + 0.2, -0.2, 0.2, 0, CY - CR, 0x9ca3af, MG));
const coreM = new THREE.Mesh(new THREE.CylinderGeometry(CR, CR, X1 - X0, 28), std(0x9ca3af, { metalness: 0.4, roughness: 0.45, transparent: true })); coreM.rotation.z = PI / 2; coreM.position.set(0, CY, 0); MG.add(coreM);
const coreGhost = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.CylinderGeometry(CR, CR, X1 - X0, 12)), new THREE.LineBasicMaterial({ color: 0x9ca3af, transparent: true, opacity: 0.6 })); coreGhost.rotation.z = PI / 2; coreGhost.position.set(0, CY, 0); MG.add(coreGhost);
let mCoil = null, mKey = '';
const clipGeo = new THREE.TorusGeometry(0.18, 0.035, 6, 18), clipMat = std(0x64748b, { metalness: 0.5, roughness: 0.35 });
const clips = new THREE.InstancedMesh(clipGeo, clipMat, 64); clips.count = 0; MG.add(clips);
{ const pile = new THREE.InstancedMesh(clipGeo, std(0x94a3b8, { metalness: 0.4, roughness: 0.4 }), 24); let r = 7; const rr = () => { r = (r * 9301 + 49297) % 233280; return r / 233280; };
  for (let i = 0; i < 24; i++) { _Q.setFromEuler(new THREE.Euler(PI / 2, 0, rr() * 6.28)); _M.compose(new THREE.Vector3(-10.4 + rr() * 4.2, 0.05, -1.4 + rr() * 2.8), _Q, new THREE.Vector3(1, 2.2, 1)); pile.setMatrixAt(i, _M); } MG.add(pile); }
const mCells = [0, 1].map(() => { const g = new THREE.Group(); const b = new THREE.Mesh(cylGeo, std(0x1f2937)); b.scale.set(0.55, 2.6, 0.55); b.rotation.z = PI / 2; g.add(b); const c = new THREE.Mesh(cylGeo, std(0xca8a04)); c.scale.set(0.56, 0.5, 0.56); c.rotation.z = PI / 2; c.name = 'plus'; g.add(c); MG.add(g); return g; });
const mLever = segM(0x334155, MG); boxM(5.4, 6.6, -3.0, -2.6, 0, 0.12, 0x475569, MG);
polyTube([V(C0, 0, CY - CR), V(C0, 0, 0.1), V(C0, -2.8, 0.1), V(-2.2, -2.8, 0.1)], 0.06, 0x475569, MG);
polyTube([V(2.2, -2.8, 0.1), V(5.5, -2.8, 0.1)], 0.06, 0x475569, MG); polyTube([V(6.6, -2.8, 0.1), V(8, -2.8, 0.1), V(8, 0, 0.1), V(C1, 0, 0.1), V(C1, 0, CY - CR)], 0.06, 0x475569, MG);
const mComp = compass(1.1, false, MG); boxM(9.0, 9.4, -0.2, 0.2, 0, CY - 0.4, 0x9ca3af, MG); mComp.position.set(9.2, CY - 0.4, 0);
const lMN = lab('mag', 'N極', { accent: true }), lMS = lab('mag', 'S極', { accent: true }), lMclip = lab('mag', '', { accent: true }), lMcore = lab('mag', '鉄しん', { sub: true }), lMturn = lab('mag', ''), lMbat = lab('mag', 'かん電池', { sub: true }), lMsw = lab('mag', 'スイッチ', { sub: true }), lMcomp = lab('mag', '方位磁針', { sub: true });
const ANCH = [[X0 - 0.12, CY + 0.45, 0.8], [X0 - 0.12, CY + 0.1, 0.6], [X0 - 0.12, CY - 0.25, 0.42]]; for (let i = 0; i < 7; i++) ANCH.push([X0 + 0.25 + i * 0.33, CY - CR, 0.2 - i * 0.055]);
function mag(st) {
  const N = st.N, nb = st.nb, on = st.swOn, s = st.dirI, ns = Math.round(Math.max(0, st.shown)), rc = CR + 0.18 + (N - 50) / 250 * 0.45;
  const key = N + ''; if (key !== mKey) { mKey = key; if (mCoil) { MG.remove(mCoil); mCoil.geometry.dispose(); }
    const turns = Math.round(Math.min(64, 12 + N / 5)), pts = []; for (let k = 0; k <= turns * 24; k++) { const t = k / 24 * 2 * PI; pts.push(new THREE.Vector3(C0 + (C1 - C0) * k / (turns * 24), CY + rc * Math.sin(t), rc * Math.cos(t))); }
    mCoil = new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), turns * 24, 0.06 + (N - 50) / 250 * 0.05, 6, false), std(COL.coil, { roughness: 0.45, metalness: 0.2 })); MG.add(mCoil); }
  coreM.visible = st.core; coreGhost.visible = !st.core;
  // クリップ（上の図と同じ順に、鉄しんの左はしにつく）
  for (let n = 0; n < Math.min(ns, 64); n++) { const c = ANCH[n % ANCH.length], k = Math.floor(n / ANCH.length), th = c[2] + 0.05 * k, x = c[0] - Math.sin(th) * 0.75 * k, y = c[1] - Math.cos(th) * 0.75 * k;
    _Q.setFromEuler(new THREE.Euler(0, (n % 3 - 1) * 0.5, -th)); _M.compose(new THREE.Vector3(x + Math.sin(th) * 0.4, y - Math.cos(th) * 0.4, ((n * 37) % 5 - 2) * 0.13), _Q, new THREE.Vector3(1, 2.2, 1)); clips.setMatrixAt(n, _M); }
  clips.count = Math.min(ns, 64); clips.instanceMatrix.needsUpdate = true;
  mCells.forEach((g, i) => { g.visible = i < nb; g.position.set(nb === 1 ? 0 : (i ? 1.45 : -1.45), 0.55, 2.8); g.getObjectByName('plus').position.x = s > 0 ? -1.05 : 1.05; });
  setSeg(mLever, V(5.5, -2.8, 0.15), on ? V(6.6, -2.8, 0.2) : V(6.2, -2.8, 1.1), 0.07);
  mComp.needle.rotation.y = -(st.nd.m2 == null ? -PI / 2 : st.nd.m2);
  const leftN = s > 0; lMN.at(leftN ? X0 - 0.3 : X1 + 0.3, CY + 1.2, 0); lMS.at(leftN ? X1 + 0.3 : X0 - 0.3, CY + 1.2, 0); lMN.show = lMS.show = on;
  lMN.el.style.background = '#dc2626'; lMN.el.style.borderColor = '#dc2626'; lMS.el.style.background = '#2563eb'; lMS.el.style.borderColor = '#2563eb';
  lMclip.set(on ? 'クリップ ' + ns + 'こ' : '電流が流れていない'); lMclip.at(SM ? -12.6 : -10.8, CY - (SM ? 2.6 : 1.6), 0); lMclip.show = true;
  lMcore.set(st.core ? '鉄しん' : '鉄しんなし'); lMcore.at(-4.6, CY - 0.9, 1.0); lMcore.show = !SM;
  lMturn.set(N + '回まき'); lMturn.at((C0 + C1) / 2, CY + rc + 0.5, 0); lMturn.show = true;
  lMbat.at(0, 1.3, 2.8); lMbat.show = true; lMsw.at(6, 1.2, 2.8); lMsw.show = !SM; lMcomp.at(9.2, CY + 0.9, 0); lMcomp.show = !SM;
  return 'まき数 <b>' + N + '回</b>・かん電池 ' + nb + '個' + (st.core ? '' : '・鉄しんなし') + (on ? '・クリップ <b>' + ns + '</b>こ' : '・スイッチ切')
    + (SM ? '' : '<br>電流の向きを反対にすると、N極とS極が入れかわる');
}

// ---------------- ③ ぶらんこ実験 ----------------
const SW = groups.swing, PX = 1.2, LP = 10.4, WY = 2.4, NC = 0xef4444, SCc = 0x3b82f6;
boxM(-6, 8, -4, 4, -3.4, -2.8, 0xe9d5b0, SW);
boxM(-4.75, -4.25, -0.25, 0.25, -2.8, 11.2, 0x94a3b8, SW); boxM(-4.75, PX + 0.25, -0.25, 0.25, 10.8, 11.2, 0x94a3b8, SW); boxM(PX - 0.25, PX + 0.25, -2.9, 2.9, 10.4, 10.8, 0x94a3b8, SW);
const sBot = boxM(-1.6, 4.8, -1.5, 1.5, -2.8, -1.2, SCc, SW), sTop = boxM(-1.6, 4.8, -1.5, 1.5, 1.2, 2.8, NC, SW); boxM(4.8, 6.4, -1.5, 1.5, -2.8, 2.8, 0x9ca3af, SW);
const sFld = [[0, -0.8], [1.8, -0.8], [0, 0.8], [1.8, 0.8], [3.4, 0]].map(() => mkArrow(COL.fld, SW));
const sSeg = [segM(COL.coil, SW), segM(COL.coil, SW), segM(COL.coil, SW)];
polyTube([V(PX, -WY, LP), V(PX, -WY, 13.2), V(PX, -0.9, 13.2)], 0.06, COL.lead, SW); polyTube([V(PX, 0.9, 13.2), V(PX, WY, 13.2), V(PX, WY, LP)], 0.06, COL.lead, SW);
const sBat = new THREE.Group(); SW.add(sBat); { const b = new THREE.Mesh(cylGeo, std(0x111827)); b.scale.set(0.4, 1.8, 0.4); b.rotation.x = PI / 2; sBat.add(b); const c = new THREE.Mesh(cylGeo, std(0xca8a04)); c.scale.set(0.41, 0.4, 0.41); c.rotation.x = PI / 2; c.name = 'plus'; sBat.add(c); sBat.position.copy(V(PX, 0, 13.2)); }
const sDots = mkDots(40, 0.17, SW), sCur = mkArrow(COL.cur, SW), sFrc = mkArrow(COL.frc, SW);
const lSN = lab('swing', 'N極', { accent: true }), lSS = lab('swing', 'S極', { accent: true }), lSf = lab('swing', '力', { accent: true }), lSc = lab('swing', '電流', { accent: true }), lSb = lab('swing', '電源', { sub: true }), lSm = lab('swing', '磁界（N→S）', { sub: true });
function swing(st) {
  const I = st.I, sc = st.dirI, mu = st.magUp, sig = -sc * mu, phi = st.phi, xb = PX + LP * Math.sin(phi), zb = LP * (1 - Math.cos(phi));
  sTop.material.color.setHex(mu > 0 ? NC : SCc); sBot.material.color.setHex(mu > 0 ? SCc : NC);
  [[0, -0.8], [1.8, -0.8], [0, 0.8], [1.8, 0.8], [3.4, 0]].forEach((q, i) => sFld[i].set(V(q[0], q[1], mu * 1.05), V(q[0], q[1], -mu * 1.05), 0.06));
  const A = V(PX, -WY, LP), B = V(xb, -WY, zb), C = V(xb, WY, zb), Dd = V(PX, WY, LP);
  setSeg(sSeg[0], A, B, 0.08); setSeg(sSeg[1], B, C, 0.11); setSeg(sSeg[2], C, Dd, 0.08);
  sBat.getObjectByName('plus').position.z = sc > 0 ? 0.75 : -0.75;
  flowDots(sDots, I > 0 ? [A, B, C, Dd] : [], 1.0, st.so * 0.05, 0.17);
  sCur.set(V(xb, -1.3 * sc, zb - 0.7), V(xb, 1.3 * sc, zb - 0.7), 0.09); sCur.visible = I > 0;
  const Lf = 1.2 + 0.5 * I; sFrc.set(V(xb, 0, zb), V(xb + sig * Lf, 0, zb), 0.13); sFrc.visible = I > 0;
  lSN.at(3.4, mu > 0 ? 3.0 : -2.3, 1.7); lSS.at(3.4, mu > 0 ? -2.3 : 3.0, 1.7); lSN.show = lSS.show = true;
  lSN.el.style.background = '#dc2626'; lSN.el.style.borderColor = '#dc2626'; lSS.el.style.background = '#2563eb'; lSS.el.style.borderColor = '#2563eb';
  lSf.at(xb + sig * (Lf + 0.4), zb + 0.5, 0); lSf.show = I > 0; lSc.at(xb, zb - 1.3, -1.6 * sc); lSc.show = I > 0 && !SM; lSb.at(PX, 14.2, 0); lSb.show = true; lSm.at(6.6, 0.5, 1.6); lSm.show = !SM;
  return I > 0 ? '電流 <b>' + I.toFixed(1) + ' A</b>・導線は磁石の<b>' + (sig < 0 ? '外側' : '内側') + '</b>へ動く' + (SM ? '' : '<br>電流・磁界・力の向きは、たがいに直角（フレミングの左手の法則）') : '電流が0なので力ははたらかない';
}

// ---------------- ③ モーター ----------------
const MO = groups.motor, R = 2.9, YL = 3.0, CA2 = 0.95;
const moL = boxM(-6.0, -4.2, -3.2, 3.2, -3.2, 3.2, NC, MO), moR = boxM(4.2, 6.0, -3.2, 3.2, -3.2, 3.2, SCc, MO);
const moFld = []; [-2, 0, 2].forEach(y => [-2.4, -1.2, 0, 1.2, 2.4].forEach(z => { const m = new THREE.Mesh(cylGeo, std(COL.fld, { transparent: true, opacity: 0.22, depthWrite: false })); setSeg(m, V(-4.2, y, z), V(4.2, y, z), 0.025); MO.add(m); const c = new THREE.Mesh(coneGeo, std(COL.fld, { transparent: true, opacity: 0.55 })); c.scale.set(0.12, 0.36, 0.12); c.position.copy(V(2.9, y, z)); MO.add(c); moFld.push(c); }));
setSeg(segM(0x64748b, MO), V(0, -6.2, 0), V(0, 4.4, 0), 0.1);
const rot = new THREE.Group(); MO.add(rot);   // コイルと整流子（z軸＝ページのy軸のまわりに回る）
polyTube([new THREE.Vector3(R, 0, YL), new THREE.Vector3(R, 0, -YL), new THREE.Vector3(-R, 0, -YL), new THREE.Vector3(-R, 0, YL)], 0.13, COL.coil, rot);
const half = (a0, a1, z0, z1, col) => { const m = new THREE.Mesh(new THREE.CylinderGeometry(CA2, CA2, z1 - z0, 24, 1, false, a0, a1 - a0), std(col, { metalness: 0.3, roughness: 0.4, side: THREE.DoubleSide })); m.rotation.x = PI / 2; m.position.z = (z0 + z1) / 2; rot.add(m); return m; };
// 整流子（半分ずつ2つ）／リング（整流子なし）
const commP = [half(0.1 + PI / 2, PI - 0.1 + PI / 2, 4.3, 5.5, 0xfbbf24), half(PI + 0.1 + PI / 2, 2 * PI - 0.1 + PI / 2, 4.3, 5.5, 0xfb923c)];
const ringP = [half(0, 2 * PI, 4.35, 4.85, 0xfbbf24), half(0, 2 * PI, 5.15, 5.65, 0xfb923c)];
const leadA = polyTube([new THREE.Vector3(R, 0, YL), new THREE.Vector3(R * 0.35, 0, YL + 0.6), new THREE.Vector3(CA2, 0, 4.9)], 0.09, COL.coil, rot), leadD = polyTube([new THREE.Vector3(-R, 0, YL), new THREE.Vector3(-R * 0.35, 0, YL + 0.6), new THREE.Vector3(-CA2, 0, 4.9)], 0.09, COL.coil, rot);
const leadA2 = polyTube([new THREE.Vector3(R, 0, YL), new THREE.Vector3(R * 0.35, 0, YL + 0.6), new THREE.Vector3(CA2, 0, 4.6)], 0.09, COL.coil, rot), leadD2 = polyTube([new THREE.Vector3(-R, 0, YL), new THREE.Vector3(-R * 0.35, 0, YL + 0.6), new THREE.Vector3(-CA2, 0, 5.4)], 0.09, COL.coil, rot);
const brR = boxM(0.97, 1.75, -0.3, 0.3, -0.36, 0.36, 0x374151, MO), brL = boxM(-1.75, -0.97, -0.3, 0.3, -0.36, 0.36, 0x374151, MO);
const moBat = new THREE.Group(); MO.add(moBat); { const b = new THREE.Mesh(cylGeo, std(0x111827)); b.scale.set(0.45, 2.4, 0.45); b.rotation.z = PI / 2; moBat.add(b); const c = new THREE.Mesh(cylGeo, std(0xca8a04)); c.scale.set(0.46, 0.45, 0.46); c.rotation.z = PI / 2; c.name = 'plus'; moBat.add(c); moBat.position.copy(V(0, -5.1, -5.0)); }
let moLeads = null, moLK = '';
const moDots = mkDots(40, 0.16, MO), moF1 = mkArrow(COL.frc, MO), moF2 = mkArrow(COL.frc, MO), moC1 = mkArrow(COL.cur, MO), moC2 = mkArrow(COL.cur, MO);
const lMoL = lab('motor', 'N極', { accent: true }), lMoR = lab('motor', 'S極', { accent: true }), lMoF = lab('motor', '力', { accent: true }), lMoC = lab('motor', '整流子', { sub: true }), lMoB = lab('motor', 'ブラシ', { sub: true }), lMoBat = lab('motor', '電源', { sub: true });
function motor(st) {
  const I = st.I, sc = st.dirI, mu = st.magUp, al = st.alpha, comm = st.comm;
  moL.material.color.setHex(mu > 0 ? NC : SCc); moR.material.color.setHex(mu > 0 ? SCc : NC);
  moFld.forEach(c => { c.quaternion.setFromUnitVectors(UP, new THREE.Vector3(mu, 0, 0)); });
  rot.rotation.z = al;
  commP.forEach(m => { m.visible = comm; }); ringP.forEach(m => { m.visible = !comm; }); leadA.visible = leadD.visible = comm; leadA2.visible = leadD2.visible = !comm;
  const yR = comm ? -4.9 : -4.6, yLb = comm ? -4.9 : -5.4; brR.position.z = -yR; brL.position.z = -yLb;
  if (moLK !== String(comm)) { moLK = String(comm); if (moLeads) MO.remove(moLeads); moLeads = new THREE.Group(); MO.add(moLeads);
    polyTube([V(1.75, yR, 0), V(2.6, yR, 0), V(2.6, -5.1, -5.0), V(1.2, -5.1, -5.0)], 0.06, COL.lead, moLeads); polyTube([V(-1.75, yLb, 0), V(-2.6, yLb, 0), V(-2.6, -5.1, -5.0), V(-1.2, -5.1, -5.0)], 0.06, COL.lead, moLeads); }
  moBat.getObjectByName('plus').position.x = sc > 0 ? 1.0 : -1.0;
  const Px = R * Math.cos(al), Pz = R * Math.sin(al), pDir = comm ? (Px >= 0 ? 1 : -1) * sc : st.pSide * sc;
  const A = V(Px, -YL, Pz), B = V(Px, YL, Pz), Cc = V(-Px, YL, -Pz), Dd = V(-Px, -YL, -Pz);
  flowDots(moDots, I > 0 ? (pDir > 0 ? [A, B, Cc, Dd] : [Dd, Cc, B, A]) : [], 1.0, st.so * 0.05 * Math.sign(pDir || 1), 0.16);
  moC1.set(V(Px * 1.15, -1.5 - 0.8 * pDir, Pz * 1.15), V(Px * 1.15, -1.5 + 0.8 * pDir, Pz * 1.15), 0.08); moC2.set(V(-Px * 1.15, -1.5 + 0.8 * pDir, -Pz * 1.15), V(-Px * 1.15, -1.5 - 0.8 * pDir, -Pz * 1.15), 0.08); moC1.visible = moC2.visible = I > 0;
  const Lf = 1.1 + 0.34 * I; moF1.set(V(Px, 0.6, Pz), V(Px, 0.6, Pz - pDir * mu * Lf), 0.12); moF2.set(V(-Px, 0.6, -Pz), V(-Px, 0.6, -Pz + pDir * mu * Lf), 0.12); moF1.visible = moF2.visible = I > 0;
  const up = -pDir * mu > 0; lMoF.at(up ? Px : -Px, (up ? Pz : -Pz) + Lf + 0.5, -0.6); lMoF.show = I > 0;
  lMoL.at(-5.1, -2.0, 3.3); lMoR.at(5.1, -2.0, 3.3); lMoL.set(mu > 0 ? 'N極' : 'S極'); lMoR.set(mu > 0 ? 'S極' : 'N極'); lMoL.show = lMoR.show = true;
  [[lMoL, mu > 0], [lMoR, mu < 0]].forEach(([l, n]) => { l.el.style.background = n ? '#dc2626' : '#2563eb'; l.el.style.borderColor = n ? '#dc2626' : '#2563eb'; });
  lMoC.set(comm ? '整流子' : 'リング（整流子なし）'); lMoC.at(0, -1.5, 5.2); lMoC.show = true; lMoB.at(1.4, 0.7, -yR); lMoB.show = !SM; lMoBat.at(0, -4.0, 5.1); lMoBat.show = true;
  const rps = Math.abs(st.omega) / (2 * PI);
  return (rps < 0.02 ? '止まっている' : '手前から見て<b>' + (st.omega < 0 ? '時計回り' : '反時計回り') + '</b>・毎秒 ' + rps.toFixed(2) + ' 回転')
    + (SM ? '' : '<br>' + (comm ? '整流子とブラシが、半回転ごとにコイルの電流の向きを切りかえる' : '整流子がないと、半回転で力が反対向きになり、行ったり来たりして止まる'));
}

// ---------------- ④ 電磁誘導・発電機（共通のコイルと検流計） ----------------
const X4 = px => (px - 300) / 20, Y4 = py => (190 - py) / 20, CX4 = 432, CL4 = 170, CR4 = 44, NT4 = 11;
function coil4(parent) {
  const x0 = X4(CX4 - CL4 / 2), x1 = X4(CX4 + CL4 / 2), r = CR4 / 20, pts = [], n = NT4 * 32;
  for (let k = 0; k <= n; k++) { const t = k / 32 * 2 * PI; pts.push(new THREE.Vector3(x0 + (x1 - x0) * k / n, r * Math.cos(t), r * Math.sin(t))); }
  tubeOf(pts, 0.12, COL.coil, parent);
  const yt = Y4(122), gx = X4(CX4), path = [new THREE.Vector3(x1, r, 0), new THREE.Vector3(x1, yt, 0), new THREE.Vector3(gx + 1.9, yt, 0), new THREE.Vector3(gx + 1.9, Y4(106), 0)];
  const path2 = [new THREE.Vector3(gx - 1.9, Y4(106), 0), new THREE.Vector3(gx - 1.9, yt, 0), new THREE.Vector3(x0, yt, 0), new THREE.Vector3(x0, r, 0)];
  polyTube(path, 0.06, COL.lead, parent); polyTube(path2, 0.06, COL.lead, parent);
  // 検流計
  const gv = new THREE.Group(); gv.position.set(gx, Y4(106) + 1.6, 0); parent.add(gv);
  const body = new THREE.Mesh(boxGeo, std(0xf1f5f9)); body.scale.set(4.2, 3.0, 1.2); gv.add(body);
  const face = new THREE.Mesh(new THREE.CircleGeometry(1.7, 32, PI / 2 - 0.95, 1.9), new THREE.MeshBasicMaterial({ color: 0xffffff })); face.position.set(0, -1.1, 0.61); gv.add(face);
  const ndl = new THREE.Group(); ndl.position.set(0, -1.1, 0.66); gv.add(ndl); const nm = new THREE.Mesh(boxGeo, std(0xdc2626)); nm.scale.set(0.07, 1.55, 0.04); nm.position.y = 0.78; ndl.add(nm);
  const dots = mkDots(50, 0.15, parent);
  return { x0, x1, r, path: path.concat(path2), ndl, dots };
}
function bar4(parent, Lb, h) { const g = new THREE.Group(); parent.add(g); const a = new THREE.Mesh(boxGeo, std(NC)), b = new THREE.Mesh(boxGeo, std(SCc)); a.scale.set(Lb / 2, h, h); b.scale.set(Lb / 2, h, h); a.position.x = Lb / 4; b.position.x = -Lb / 4; g.add(a, b); g.ends = [a, b]; return g; }
const MV = groups.move, cm = coil4(MV), mvBar = bar4(MV, 8, 1.7);
const lMvN = lab('move', 'N', { accent: true }), lMvS = lab('move', 'S', { accent: true }), lMvG = lab('move', '検流計', { sub: true }), lMvL = lab('move', '', { accent: true }), lMvR = lab('move', '', { accent: true }), lMvC = lab('move', 'コイル', { sub: true });
function poles4(lL, lR, x0, x1, r, iNow) { const on = Math.abs(iNow) > 0.15, lN = iNow > 0; lL.set(lN ? 'N' : 'S'); lR.set(lN ? 'S' : 'N'); lL.at(x0 - 0.8, r + 0.5, 0); lR.at(x1 + 0.8, r + 0.5, 0); lL.show = lR.show = on;
  [[lL, lN], [lR, !lN]].forEach(([l, n]) => { l.el.style.background = n ? '#dc2626' : '#2563eb'; l.el.style.borderColor = n ? '#dc2626' : '#2563eb'; }); }
function moveWord(st) { if (Math.abs(st.vS) < 6) return '止まっている'; return (st.magN > 0 ? 'N極' : 'S極') + (st.vS > 0 ? 'を近づけている' : 'を遠ざけている'); }
function move(st) {
  const x = X4(st.mX), fl = st.magN; mvBar.position.set(x, 0, 0); mvBar.ends[0].material.color.setHex(fl > 0 ? NC : SCc); mvBar.ends[1].material.color.setHex(fl > 0 ? SCc : NC);
  cm.ndl.rotation.z = -clamp(st.ndl, -11, 11) * 0.09;
  flowDots(cm.dots, Math.abs(st.iNow) > 0.15 ? cm.path : [], 1.0, st.so * 0.05, 0.15);
  lMvN.at(x + (fl > 0 ? 3 : -3), 1.3, 0); lMvS.at(x + (fl > 0 ? -3 : 3), 1.3, 0); lMvN.show = lMvS.show = true;
  lMvN.el.style.background = '#dc2626'; lMvN.el.style.borderColor = '#dc2626'; lMvS.el.style.background = '#2563eb'; lMvS.el.style.borderColor = '#2563eb';
  poles4(lMvL, lMvR, cm.x0, cm.x1, cm.r, st.iNow); lMvG.at(X4(CX4), Y4(106) + 3.4, 0); lMvG.show = true; lMvC.at((cm.x0 + cm.x1) / 2, -cm.r - 0.4, 0); lMvC.show = !SM;
  const a = Math.abs(st.ndl);
  return '磁石：<b>' + moveWord(st) + '</b>・針：' + (a < 0.15 ? '0' : (st.ndl > 0 ? '右' : '左') + 'に ' + a.toFixed(1) + ' 目もり')
    + (SM ? '' : '<br>' + (Math.abs(st.iNow) > 0.15 ? 'コイルの左はしが' + (st.iNow > 0 ? 'N' : 'S') + '極になり、' + (st.vS > 0 ? '近づく磁石をしりぞける' : '遠ざかる磁石を引きとめる') : 'コイルの中の磁界が変化したときだけ電流が流れる'));
}
const GE = groups.gen, cg = coil4(GE), geBar = bar4(GE, 6.6, 1.5);
geBar.position.set(X4(212), 0, 0);
{ const ax = new THREE.Mesh(cylGeo, std(0x475569)); ax.scale.set(0.25, 2.6, 0.25); ax.rotation.x = PI / 2; ax.position.set(X4(212), 0, -0.6); GE.add(ax); }
const leds = [[-1.1, 0xef4444], [1.1, 0x22c55e]].map(([dx, c]) => { const m = new THREE.Mesh(new THREE.SphereGeometry(0.42, 20, 14), std(c, { emissive: c, emissiveIntensity: 0, transparent: true, opacity: 0.9 })); m.position.set(X4(212) + dx, 4.6, 0); GE.add(m); return m; });
const lGeN = lab('gen', 'N', { accent: true }), lGeS = lab('gen', 'S', { accent: true }), lGeG = lab('gen', '検流計', { sub: true }), lGeL = lab('gen', '', { accent: true }), lGeR = lab('gen', '', { accent: true }), lGeLED = lab('gen', '赤LED・緑LED（反対向き）', { sub: true });
function gen(st) {
  const th = st.theta, fl = st.magN; geBar.rotation.z = th; geBar.ends[0].material.color.setHex(fl > 0 ? NC : SCc); geBar.ends[1].material.color.setHex(fl > 0 ? SCc : NC);
  cg.ndl.rotation.z = -clamp(st.ndl, -11, 11) * 0.09;
  flowDots(cg.dots, Math.abs(st.iNow) > 0.15 ? cg.path : [], 1.0, st.so * 0.05, 0.15);
  const red = clamp((st.iNow - 0.5) / 4, 0, 1), grn = clamp((-st.iNow - 0.5) / 4, 0, 1); leds[0].material.emissiveIntensity = red * 1.6; leds[1].material.emissiveIntensity = grn * 1.6;
  const gx = X4(212), c = Math.cos(th), s = Math.sin(th), e = 3.9 * (fl > 0 ? 1 : -1);
  lGeN.at(gx + c * e, s * e + 0.8, 0); lGeS.at(gx - c * e, -s * e + 0.8, 0); lGeN.show = lGeS.show = true;
  lGeN.el.style.background = '#dc2626'; lGeN.el.style.borderColor = '#dc2626'; lGeS.el.style.background = '#2563eb'; lGeS.el.style.borderColor = '#2563eb';
  poles4(lGeL, lGeR, cg.x0, cg.x1, cg.r, st.iNow); lGeG.at(X4(CX4), Y4(106) + 3.4, 0); lGeG.show = true; lGeLED.at(gx, 6.4, 0); lGeLED.show = !SM;
  const f = +($('rps') ? $('rps').value : 1), fq = st.playing ? f : 0;
  return (st.playing ? '毎秒 <b>' + fq.toFixed(1) + '</b> 回転＝<b>' + fq.toFixed(1) + ' Hz</b>の交流' : '止まっている（上の図で指で回せます）')
    + (SM ? '' : '<br>磁石が半回転するごとに、コイルに流れる電流の向きが変わる（赤と緑のLEDが交互に光る）');
}

// ---- 毎フレーム ----
const hud = $('hud3d'); hud.style.display = '';
if (SM) { hud.style.fontSize = '11px'; hud.style.padding = '3px 6px'; hud.style.left = hud.style.top = '6px'; }
const FN = { wire, coil, mag, swing, motor, move, gen };
let cur = '';
v.onFrame(() => {
  const st = D.st(), key = st.m === 'm1' ? (st.v === 'coil' ? 'coil' : 'wire') : st.m === 'm2' ? 'mag' : st.m === 'm3' ? (st.v === 'motor' ? 'motor' : 'swing') : (st.v === 'gen' ? 'gen' : 'move');
  if (key !== cur) {
    Object.keys(groups).forEach(k => { groups[k].visible = k === key; (L[k] || []).forEach(l => { l.show = false; }); });
    const c = CAM[key]; ['persp', 'front', 'top'].forEach((k, i) => { v.views[k].tgt = c.tgt; v.views[k].dist = c.d[i] * ZF; }); v.views.persp.th = c.a ? c.a[0] : 0.55; v.views.persp.ph = c.a ? c.a[1] : 0.5;
    v.setView('persp', !cur); cur = key;
  }
  hud.innerHTML = FN[key](st);
});
