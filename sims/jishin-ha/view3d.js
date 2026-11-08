// 地震の伝わり方 P波・S波 3D（上の地図を地表にして、地下（深さ110km）までを箱にした模型）
// 東＝+x、北＝-z、上＝+y。1 = 10km（たて・横とも同じ縮尺。地図と観測点は上の図と同じ架空のもの）
// 波は震源から球の形に広がる → 地表では円、震源を通る断面（東西）では同心円に見える
import { THREE, createView } from '../../assets/three/sim3d.js';
const $ = id => document.getElementById(id);
const J = window.__jishin;
const S = 0.1, HW = 15, DB = 11;                    // 1km=0.1、地図300kmの半分、地下の深さ110km
const X = x => (x - 150) * S, Z = y => (y - 150) * S, Y = d => -d * S;
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const f1 = v => (Math.round(v * 10) / 10).toFixed(1);
const STC = ['#334155', '#2563eb', '#dc2626'];

const v = createView($('view3d'), {
  views: {
    persp: { tgt: [0, -3.5, 0], dist: 62, th: -0.55, ph: 0.36 },
    south: { tgt: [0, -4.5, 0], dist: 54, th: 0, ph: 0.06 },
    top: { tgt: [-2.5, 0, -1], dist: 64, th: 0, ph: 1.45 },
  },
  camRow: '#camRow3d', bg: 0xe6eef6, shadows: false, minDist: 10, maxDist: 140,
});
const { scene } = v;

// ---- 地表（上の地図と同じ。P波・S波が地表に届いた円もここに描く） ----
const MK = 2, MW = 300 * MK;
const mcv = document.createElement('canvas'); mcv.width = MW; mcv.height = MW; const mg = mcv.getContext('2d');
const mtex = new THREE.CanvasTexture(mcv); mtex.colorSpace = THREE.SRGBColorSpace; mtex.anisotropy = 4;
const map = new THREE.Mesh(new THREE.PlaneGeometry(2 * HW, 2 * HW), new THREE.MeshBasicMaterial({ map: mtex }));
map.rotation.x = -Math.PI / 2; map.position.y = 0.002; scene.add(map);
function circ(g, x, y, r) { g.beginPath(); g.arc(x, y, r, 0, Math.PI * 2); }
function paintMap(m, s, eew) {
  const g = mg, k = MK, cx = s.ex * k, cy = s.ey * k;
  g.fillStyle = '#dbeafe'; g.fillRect(0, 0, MW, MW);
  g.beginPath(); g.moveTo(0, 0); g.lineTo(MW, 0); g.lineTo(MW, MW); for (let j = J.COAST.length - 1; j >= 0; j--) g.lineTo(J.COAST[j][0] * k, J.COAST[j][1] * k); g.closePath();
  g.fillStyle = '#f7fee7'; g.fill(); g.strokeStyle = '#94a3b8'; g.lineWidth = 2.4; g.stroke();
  g.strokeStyle = 'rgba(100,116,139,.22)'; g.lineWidth = 2; for (let q = 50; q < 300; q += 50) { g.beginPath(); g.moveTo(q * k, 0); g.lineTo(q * k, MW); g.moveTo(0, q * k); g.lineTo(MW, q * k); g.stroke(); }
  g.fillStyle = '#64748b'; g.font = 'bold 26px sans-serif'; g.fillText('海', 14 * k, 290 * k);
  const rP = J.surfR(m.vp * s.t, m.d) * k, rS = J.surfR(m.vs * s.t, m.d) * k;
  if (rP > 0) { g.beginPath(); g.arc(cx, cy, rP, 0, Math.PI * 2); if (rS > 0) { g.moveTo(cx + rS, cy); g.arc(cx, cy, rS, 0, Math.PI * 2, true); } g.fillStyle = 'rgba(59,130,246,.2)'; g.fill(); }
  if (rS > 0) { circ(g, cx, cy, rS); g.fillStyle = 'rgba(239,68,68,.22)'; g.fill(); }
  g.lineWidth = 5; if (rP > 0) { circ(g, cx, cy, rP); g.strokeStyle = '#2563eb'; g.stroke(); } if (rS > 0) { circ(g, cx, cy, rS); g.strokeStyle = '#dc2626'; g.stroke(); }
  if (eew && s.t >= m.tal) { const rA = J.surfR(m.vs * m.tal, m.d) * k; if (rA > 0) { g.setLineDash([12, 8]); g.strokeStyle = '#7c3aed'; g.lineWidth = 4; circ(g, cx, cy, rA); g.stroke(); g.setLineDash([]); } }
  g.strokeStyle = '#b91c1c'; g.lineWidth = 6; g.beginPath(); g.moveTo(cx - 13, cy - 13); g.lineTo(cx + 13, cy + 13); g.moveTo(cx - 13, cy + 13); g.lineTo(cx + 13, cy - 13); g.stroke();
  g.strokeStyle = '#0f172a'; g.lineWidth = 4; g.beginPath(); g.moveTo(MW - 124, MW - 24); g.lineTo(MW - 24, MW - 24); g.stroke();
  g.fillStyle = '#0f172a'; g.font = 'bold 22px sans-serif'; g.textAlign = 'center'; g.fillText('50 km', MW - 74, MW - 34); g.textAlign = 'left';
  mtex.needsUpdate = true;
}

// ---- 地下の箱（うすい色のガラス） ----
const boxG = new THREE.BoxGeometry(2 * HW, DB, 2 * HW);
const glass = new THREE.Mesh(boxG, new THREE.MeshBasicMaterial({ color: 0xb08d63, transparent: true, opacity: 0.1, depthWrite: false, side: THREE.DoubleSide }));
glass.position.y = -DB / 2 - 0.01; glass.renderOrder = 3; scene.add(glass);
const edges = new THREE.LineSegments(new THREE.EdgesGeometry(boxG), new THREE.LineBasicMaterial({ color: 0x64748b }));
edges.position.copy(glass.position); scene.add(edges);
const floor = new THREE.Mesh(new THREE.PlaneGeometry(2 * HW, 2 * HW), new THREE.MeshBasicMaterial({ color: 0x9c8466, transparent: true, opacity: 0.35, depthWrite: false }));
floor.rotation.x = -Math.PI / 2; floor.position.y = -DB - 0.01; scene.add(floor);

// ---- 震源を通る断面（東西）：P波・S波は同心円に見える ----
const SK = 2, SW = 300 * SK, SH = DB * 10 * SK;
const scv = document.createElement('canvas'); scv.width = SW; scv.height = SH; const sg = scv.getContext('2d');
const stex = new THREE.CanvasTexture(scv); stex.colorSpace = THREE.SRGBColorSpace; stex.anisotropy = 4;
const sect = new THREE.Mesh(new THREE.PlaneGeometry(2 * HW, DB), new THREE.MeshBasicMaterial({ map: stex, side: THREE.DoubleSide, transparent: true, opacity: 0.92 }));
sect.position.y = -DB / 2; sect.renderOrder = 1; scene.add(sect);
function paintSect(m, s) {
  const g = sg, k = SK, cx = s.ex * k, cy = m.d * k;
  const gr = g.createLinearGradient(0, 0, 0, SH); gr.addColorStop(0, '#efe3cf'); gr.addColorStop(1, '#cdb697');
  g.fillStyle = gr; g.fillRect(0, 0, SW, SH);
  g.strokeStyle = 'rgba(90,60,30,.18)'; g.lineWidth = 2; for (let d = 20; d < DB * 10; d += 20) { g.beginPath(); g.moveTo(0, d * k); g.lineTo(SW, d * k); g.stroke(); }
  const right = s.ex < 150; g.fillStyle = '#6b5440'; g.font = 'bold 20px sans-serif'; g.textAlign = right ? 'right' : 'left';   // 深さの目もりは震央から遠い側に
  for (let d = 20; d < DB * 10; d += 20) g.fillText('深さ' + d + 'km', right ? SW - 8 : 8, d * k - 6);
  g.textAlign = 'left';
  const RP = m.vp * s.t * k, RS = m.vs * s.t * k;
  if (RP > 0) { g.beginPath(); g.arc(cx, cy, RP, 0, Math.PI * 2); if (RS > 0) { g.moveTo(cx + RS, cy); g.arc(cx, cy, RS, 0, Math.PI * 2, true); } g.fillStyle = 'rgba(59,130,246,.22)'; g.fill(); }
  if (RS > 0) { circ(g, cx, cy, RS); g.fillStyle = 'rgba(239,68,68,.25)'; g.fill(); }
  g.lineWidth = 5; if (RP > 0) { circ(g, cx, cy, RP); g.strokeStyle = '#2563eb'; g.stroke(); } if (RS > 0) { circ(g, cx, cy, RS); g.strokeStyle = '#dc2626'; g.stroke(); }
  g.setLineDash([8, 6]); g.strokeStyle = '#7f1d1d'; g.lineWidth = 2.5; g.beginPath(); g.moveTo(cx, 0); g.lineTo(cx, cy); g.stroke(); g.setLineDash([]);
  g.strokeStyle = '#334155'; g.lineWidth = 4; g.beginPath(); g.moveTo(0, 2); g.lineTo(SW, 2); g.stroke();
  stex.needsUpdate = true;
}

// ---- 波の先頭（球）：箱の外は切り取る ----
const clip = [new THREE.Plane(new THREE.Vector3(-1, 0, 0), HW), new THREE.Plane(new THREE.Vector3(1, 0, 0), HW), new THREE.Plane(new THREE.Vector3(0, 0, -1), HW),
  new THREE.Plane(new THREE.Vector3(0, 0, 1), HW), new THREE.Plane(new THREE.Vector3(0, -1, 0), 0), new THREE.Plane(new THREE.Vector3(0, 1, 0), DB)];
const shell = (color, opacity) => { const s = new THREE.Mesh(new THREE.SphereGeometry(1, 72, 40), new THREE.MeshStandardMaterial({ color, transparent: true, opacity, roughness: 0.55, side: THREE.DoubleSide, depthWrite: false, clippingPlanes: clip }));
  s.renderOrder = 2; scene.add(s); return s; };
const pShell = shell(0x3b82f6, 0.2), sShell = shell(0xef4444, 0.26);

// ---- 震源・震央・観測点 ----
const hypo = new THREE.Mesh(new THREE.SphereGeometry(0.42, 24, 16), new THREE.MeshBasicMaterial({ color: 0xdc2626 })); scene.add(hypo);
const hypoRing = new THREE.Mesh(new THREE.SphereGeometry(0.62, 24, 16), new THREE.MeshBasicMaterial({ color: 0xffffff, side: THREE.BackSide })); scene.add(hypoRing);
const stMat = STC.map(c => new THREE.MeshStandardMaterial({ color: c, roughness: 0.6 }));
const pins = J.ST.map(s => { const p = new THREE.Mesh(new THREE.ConeGeometry(0.55, 1.1, 3), stMat[0]); p.position.set(X(s.x), 0.55, Z(s.y)); scene.add(p); return p; });
const ring = new THREE.Mesh(new THREE.TorusGeometry(0.95, 0.12, 8, 40), new THREE.MeshBasicMaterial({ color: 0xf59e0b })); ring.rotation.x = Math.PI / 2; scene.add(ring);
const dGeo = new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(), new THREE.Vector3(1, 1, 1)]);
const dLine = new THREE.Line(dGeo, new THREE.LineDashedMaterial({ color: 0xd97706, dashSize: 0.6, gapSize: 0.35 })); dLine.renderOrder = 4; scene.add(dLine);

// ---- 文字 ----
const lEpi = v.label('震央', [0, 0, 0]);
const lHypo = v.label('震源', [0, 0, 0], { accent: true });
const lSt = J.ST.map(s => v.label(s.n, [X(s.x), 1.3, Z(s.y)]));
const lP = v.label('P波', [0, 0, 0], { sub: true }), lS = v.label('S波', [0, 0, 0], { sub: true });
const lSect = v.label('震源を通る断面（東西）', [0, 0, 0], { sub: true });
const hud = $('hud3d'); hud.style.display = '';
const SM = v.mobile; if (SM) { hud.style.fontSize = '11px'; hud.style.padding = '3px 6px'; hud.style.left = hud.style.top = '6px'; }   // スマホは短く（注意書きは下の説明文にある）

let key = '', pOn = false, sOn = false;
v.onFrame(() => {
  const s = J.st(), m = J.model(), eew = $('eew') && $('eew').value === 'on';
  const k2 = [s.ex, s.ey, s.t.toFixed(2), m.d, m.vp, m.vs, eew, s.sel].join('|');
  if (k2 === key) return;
  key = k2;
  paintMap(m, s, eew); paintSect(m, s);
  const hx = X(s.ex), hz = Z(s.ey), hy = Y(m.d);
  sect.position.set(0, -DB / 2, hz);
  hypo.position.set(hx, hy, hz); hypoRing.position.copy(hypo.position);
  const RP = m.vp * s.t * S, RS = m.vs * s.t * S;
  pShell.visible = RP > 0.05; pShell.position.copy(hypo.position); pShell.scale.setScalar(Math.max(RP, 0.01));
  sShell.visible = RS > 0.05; sShell.position.copy(hypo.position); sShell.scale.setScalar(Math.max(RS, 0.01));
  J.ST.forEach((st, i) => { const kk = s.t >= m.ts[i] ? 2 : (s.t >= m.tp[i] ? 1 : 0); pins[i].material = stMat[kk];
    lSt[i].el.className = 'lbl' + (i === s.sel ? ' acc' : ''); });
  const ss = J.ST[s.sel], sx = X(ss.x), sz = Z(ss.y);
  ring.position.set(sx, 0.06, sz);
  const pos = dGeo.attributes.position; pos.setXYZ(0, hx, hy, hz); pos.setXYZ(1, sx, 0.05, sz); pos.needsUpdate = true; dLine.computeLineDistances();
  lEpi.at(hx, 0.15, hz);
  lHypo.set(SM ? '震源' : '震源（深さ' + m.d + 'km）'); lHypo.at(hx, hy - 1.3, hz);
  // 断面の円の上に「P波」「S波」（地図の中心側・ななめ下の、箱の中に入っている点）
  const dir = s.ex < 150 ? 1 : -1;
  const put = (L, r, a0) => { if (r <= 0.5) { L.show = false; return; } const a = [a0, a0 - 0.5, a0 + 0.5, 0.15].find(a => { const x = s.ex + dir * r * Math.cos(a), d = m.d + r * Math.sin(a); return x > 8 && x < 292 && d > 4 && d < DB * 10 - 4; });
    L.show = a !== undefined; if (L.show) L.at(X(s.ex + dir * r * Math.cos(a)), Y(m.d + r * Math.sin(a)), hz + 0.05); };
  put(lP, m.vp * s.t, 0.75); put(lS, m.vs * s.t, 1.05); pOn = lP.show; sOn = lS.show;
  lSect.at(clamp(hx, -HW + 4, HW - 4), -DB - 1.1, hz);   // 箱の下（震源の真下）
  const i = s.sel, kk = s.t >= m.ts[i] ? 'S波が届いた（大きなゆれ＝主要動）' : (s.t >= m.tp[i] ? 'P波が届いた（小さなゆれ＝初期微動）' : 'まだゆれていない');
  if (SM) hud.innerHTML = '<b>' + f1(s.t) + '</b> 秒・深さ ' + m.d + ' km<br>' + ss.n + '地点：P波 ' + f1(m.tp[i]) + '秒・S波 ' + f1(m.ts[i]) + '秒後';
  else hud.innerHTML = '地震発生から <b>' + f1(s.t) + '</b> 秒　震源の深さ ' + m.d + ' km<br>' + ss.n + '地点（震源距離 ' + f1(m.D[i]) + ' km）：P波 ' + f1(m.tp[i]) + '秒後・S波 ' + f1(m.ts[i]) + '秒後<br>いま：' + kk +
    '<br><span style="font-size:11px;color:#64748b">波は球の形に広がり、地表では円に見えます（地図は架空）</span>';
});
// 真上からは震源と震央が重なるので、震源の文字と断面の文字は出さない
v.onFrame(() => { const top = v.cam.ph > 1.1; lHypo.show = !top; lSect.show = !top; lP.show = pOn && !top; lS.show = sOn && !top; });
