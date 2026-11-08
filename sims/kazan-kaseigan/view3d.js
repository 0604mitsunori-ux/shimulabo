// 火山の形と火成岩 3D（ページと同じ火山の形の式を回して立体に。手前（南東）の4分の1を切り取って中を見せる）
// 東＝+x、北＝-z、上＝+y。1 = ページの図の10px（大きさは実際の比率ではない：ページと同じ）
import { THREE, createView } from '../../assets/three/sim3d.js';
const $ = id => document.getElementById(id);
const K = window.__kazan;
const PX = 0.1, RG = 34, DEEP = 8;                 // 地面の円の半径・地下の深さ（単位）
const MC = { d: 48, rx: 90, ry: 21 };              // マグマだまり（ページと同じ：地表から48px下・横90・縦21）
const TOPPX = 150, BOTPX = DEEP / PX;              // 切り口の図の上端・下端（px）
const ease = t => t <= 0 ? 0 : (t >= 1 ? 1 : t * t * (3 - 2 * t));
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const CUT0 = 0, CUT1 = Math.PI / 2;               // 切り取る向き（南〜東の間）

const v = createView($('view3d'), {
  views: {
    persp: { tgt: [0, 3, 0], dist: 96, th: Math.PI / 4, ph: 0.36 },
    south: { tgt: [6, 3, 0], dist: 74, th: 0, ph: 0.04 },
    top: { tgt: [0, 0, 0], dist: 100, th: Math.PI / 4, ph: 1.42 },
  },
  camRow: '#camRow3d', bg: 0xcfe3f2, shadows: false, minDist: 12, maxDist: 160,
});
const { scene } = v;
if (v.mobile) { for (const k in v.views) v.views[k].dist *= 0.82; v.setView('persp', true); }   // スマホは少し寄る

// ---- 地面（切り取った4分の1をのぞく） ----
const ground = new THREE.Mesh(new THREE.CylinderGeometry(RG, RG, DEEP, 120, 1, false, CUT1, 2 * Math.PI - (CUT1 - CUT0)),
  [new THREE.MeshStandardMaterial({ color: 0x8a6a48, roughness: 1 }), new THREE.MeshStandardMaterial({ color: 0xb8c49a, roughness: 1 }), new THREE.MeshStandardMaterial({ color: 0x5b4330, roughness: 1 })]);
ground.position.y = -DEEP / 2 - 0.005; scene.add(ground);

// ---- 切り口の図（2面とも同じ図。ページの断面図と同じ描き方） ----
const FK = 3, FW = Math.round(RG / PX * FK), FH = Math.round((TOPPX + BOTPX) * FK);
const fcv = document.createElement('canvas'); fcv.width = FW; fcv.height = FH; const g = fcv.getContext('2d');
const ftex = new THREE.CanvasTexture(fcv); ftex.colorSpace = THREE.SRGBColorSpace; ftex.anisotropy = 4;
const cx = r => r * FK, cy = y => (TOPPX - y) * FK;   // r：中心からの距離px、y：地表からの高さpx（上が＋）
const rgb = c => 'rgb(' + c.map(Math.round).join(',') + ')';
const mixc = (a, b, t) => a.map((x, i) => x + (b[i] - x) * t);
function paintFace(q) {
  g.clearRect(0, 0, FW, FH);
  const gg = g.createLinearGradient(0, cy(0), 0, FH); gg.addColorStop(0, '#c9a77c'); gg.addColorStop(1, '#7c5c3e');
  g.fillStyle = gg; g.fillRect(0, cy(0), FW, FH - cy(0));
  g.strokeStyle = 'rgba(80,50,20,.22)'; g.lineWidth = FK; for (let y = -13; y > -BOTPX; y -= 13) { g.beginPath(); g.moveTo(0, cy(y)); g.lineTo(FW, cy(y)); g.stroke(); }
  // マグマだまり（半分）
  const mg = g.createRadialGradient(0, cy(-MC.d), 4 * FK, 0, cy(-MC.d), 92 * FK); mg.addColorStop(0, '#fde047'); mg.addColorStop(0.5, '#f97316'); mg.addColorStop(1, '#b91c1c');
  g.fillStyle = mg; g.beginPath(); g.ellipse(0, cy(-MC.d), MC.rx * FK, MC.ry * FK, 0, -Math.PI / 2, Math.PI / 2); g.closePath(); g.fill();
  // 火山の体
  const R = K.reach(q) + 6, rc = K.rockC(q), top = K.vh(0, q);
  g.beginPath(); g.moveTo(0, cy(0) + FK); for (let r = 0; r <= R; r += 2) g.lineTo(cx(r), cy(K.vh(r, q))); g.lineTo(cx(R), cy(0) + FK); g.closePath();
  const vg = g.createLinearGradient(0, cy(130), 0, cy(0)); vg.addColorStop(0, rgb(mixc(rc, [255, 255, 255], 0.18))); vg.addColorStop(1, rgb(rc)); g.fillStyle = vg; g.fill();
  const w = K.shW(q);
  if (w[1] > 0.05) {   // 成層火山：溶岩と火山灰がかさなった層
    g.save(); g.clip();
    for (let j = 1; j <= 4; j++) { const s = 1 - j * 0.18; g.beginPath(); let st = false; for (let r = 0; r <= 330; r += 3) { const hh = s * K.vh(r / s, q); if (hh < 1.5) { st = false; continue; } if (!st) { g.moveTo(cx(r), cy(hh)); st = true; } else g.lineTo(cx(r), cy(hh)); }
      g.strokeStyle = j % 2 ? 'rgba(255,255,255,' + (0.4 * w[1]).toFixed(2) + ')' : 'rgba(0,0,0,' + (0.28 * w[1]).toFixed(2) + ')'; g.lineWidth = 2 * FK; g.stroke(); }
    g.restore();
  }
  g.strokeStyle = 'rgba(15,23,42,.6)'; g.lineWidth = 1.5 * FK; g.beginPath(); for (let r = 0; r <= R; r += 2) { r ? g.lineTo(cx(r), cy(K.vh(r, q))) : g.moveTo(0, cy(K.vh(0, q))); } g.stroke();
  // 火道（半分の幅）
  g.fillStyle = '#ea580c'; g.fillRect(0, cy(top) - FK, 3 * FK, cy(-MC.d + MC.ry - 2) - cy(top) + FK);
  g.fillStyle = '#fed7aa'; g.fillRect(0, cy(top) - FK, 1 * FK, cy(-MC.d + MC.ry - 2) - cy(top) + FK);
  // ア・イの印
  const da = Math.min(64, K.reach(q) * 0.42);
  [[da, K.vh(da, q) - 7], [108, -MC.d]].forEach(([r, y]) => { g.fillStyle = '#fff'; g.strokeStyle = '#0f172a'; g.lineWidth = 1.6 * FK; g.beginPath(); g.arc(cx(r), cy(y), 6 * FK, 0, Math.PI * 2); g.fill(); g.stroke(); });
  ftex.needsUpdate = true;
  return { da };
}
function facePlane(dirX, dirZ) {   // 中心から (dirX, dirZ) の向きに伸びる切り口
  const geo = new THREE.BufferGeometry(), y0 = -DEEP, y1 = TOPPX * PX;
  geo.setAttribute('position', new THREE.Float32BufferAttribute([0, y0, 0, RG * dirX, y0, RG * dirZ, RG * dirX, y1, RG * dirZ, 0, y1, 0], 3));
  geo.setAttribute('uv', new THREE.Float32BufferAttribute([0, 0, 1, 0, 1, 1, 0, 1], 2)); geo.setIndex([0, 1, 2, 0, 2, 3]);
  const m = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ map: ftex, side: THREE.DoubleSide, alphaTest: 0.5 })); scene.add(m); return m;
}
facePlane(1, 0); facePlane(0, 1);
// 切り口のふち
const rim = new THREE.LineSegments(new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(0, -DEEP, 0), new THREE.Vector3(0, 0, 0), new THREE.Vector3(0, -DEEP, 0), new THREE.Vector3(RG, -DEEP, 0), new THREE.Vector3(0, -DEEP, 0), new THREE.Vector3(0, -DEEP, RG)]), new THREE.LineBasicMaterial({ color: 0x3f2d1e }));
scene.add(rim);

// ---- 火山の外側（ページの形 vh を回転） ----
let body = null;
const bodyMat = new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.95, metalness: 0, side: THREE.DoubleSide, flatShading: false });
function buildBody(q) {
  if (body) { scene.remove(body); body.geometry.dispose(); }
  const R = K.reach(q) + 6, pts = [];
  for (let r = 0; r <= R; r += 2) pts.push(new THREE.Vector2(Math.max(0.001, r * PX), K.vh(r, q) * PX + 0.01));
  const geo = new THREE.LatheGeometry(pts, 120, CUT1, 2 * Math.PI - (CUT1 - CUT0));
  const rc = K.rockC(q).map(c => c / 255), hmax = Math.max(0.1, ...pts.map(p => p.y)), pos = geo.attributes.position, col = new Float32Array(pos.count * 3), c = new THREE.Color();
  for (let i = 0; i < pos.count; i++) { const t = 0.18 * pos.getY(i) / hmax; c.setRGB(rc[0] + (1 - rc[0]) * t, rc[1] + (1 - rc[1]) * t, rc[2] + (1 - rc[2]) * t, THREE.SRGBColorSpace); col.set([c.r, c.g, c.b], i * 3); }
  geo.setAttribute('color', new THREE.BufferAttribute(col, 3)); geo.computeVertexNormals();
  body = new THREE.Mesh(geo, bodyMat); scene.add(body);
}

// ---- 溶岩の流れ（ねばりけが弱いほど長く流れる） ----
const lavaCv = document.createElement('canvas'); lavaCv.width = 64; lavaCv.height = 8;
{ const lg = lavaCv.getContext('2d'); lg.fillStyle = '#dc2626'; lg.fillRect(0, 0, 64, 8); lg.fillStyle = '#fde047'; lg.fillRect(0, 0, 22, 8); lg.fillStyle = '#f97316'; lg.fillRect(22, 0, 8, 8); }
const lavaTex = new THREE.CanvasTexture(lavaCv); lavaTex.wrapS = THREE.RepeatWrapping; lavaTex.colorSpace = THREE.SRGBColorSpace;
const lavaMat = new THREE.MeshBasicMaterial({ map: lavaTex, transparent: true });
const lavas = new THREE.Group(); scene.add(lavas);
const LAVA_DIRS = [Math.PI * 0.62, Math.PI * 0.95, Math.PI * 1.25, Math.PI * 1.55, Math.PI * 1.85];
function buildLava(q) {
  lavas.children.forEach(m => m.geometry.dispose()); lavas.clear();
  const wl = clamp(1 - q * 1.6, 0, 1); if (wl <= 0.03) return wl;
  const Lf = K.reach(q) * (0.35 + 0.6 * wl);
  LAVA_DIRS.forEach((a, k) => {
    const L = Lf * (0.75 + 0.25 * ((k * 0.37) % 1)), pts = [];
    for (let r = 0; r <= L; r += 4) { const wob = Math.sin(r * 0.04 + k) * 0.06; pts.push(new THREE.Vector3(r * PX * Math.sin(a + wob), K.vh(r, q) * PX + 0.12, r * PX * Math.cos(a + wob))); }
    if (pts.length < 2) return;
    const geo = new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), pts.length * 2, 0.32, 6, false);
    lavas.add(new THREE.Mesh(geo, lavaMat));
  });
  lavaMat.opacity = 0.55 + 0.45 * wl; lavaTex.repeat.set(Math.max(2, Lf / 18), 1);
  return wl;
}

// ---- 噴煙（火山灰・軽石）・火山弾・火砕流・溶岩のしぶき ----
const puffGeo = new THREE.SphereGeometry(1, 10, 8);
const ashMat = new THREE.MeshStandardMaterial({ color: 0xa8a29e, transparent: true, opacity: 0.5, depthWrite: false, roughness: 1 });
const NA = 90, ash = new THREE.InstancedMesh(puffGeo, ashMat, NA); ash.frustumCulled = false; scene.add(ash);
const flowMat = new THREE.MeshStandardMaterial({ color: 0x7a736c, transparent: true, opacity: 0.55, depthWrite: false, roughness: 1 });
const NF = 14, flow = new THREE.InstancedMesh(puffGeo, flowMat, NF); flow.frustumCulled = false; scene.add(flow);
const bombMat = new THREE.MeshStandardMaterial({ color: 0x1c1917, roughness: 0.9 });
const NB = 10, bombs = new THREE.InstancedMesh(puffGeo, bombMat, NB); bombs.frustumCulled = false; scene.add(bombs);
const NS = 40, sPos = new Float32Array(NS * 3), sGeo = new THREE.BufferGeometry(); sGeo.setAttribute('position', new THREE.BufferAttribute(sPos, 3));
const sparks = new THREE.Points(sGeo, new THREE.PointsMaterial({ color: 0xf97316, size: 0.35 })); sparks.frustumCulled = false; scene.add(sparks);
const M4 = new THREE.Matrix4(), Q0 = new THREE.Quaternion(), V3 = new THREE.Vector3(), SC = new THREE.Vector3();
const put = (im, i, x, y, z, s) => { M4.compose(V3.set(x, y, z), Q0, SC.set(s, s, s)); im.setMatrixAt(i, M4); };
const FLOW_DIR = Math.PI * 1.75;

// ---- 文字 ----
const lShape = v.label('', [0, 0, 0], { accent: true });
const lMag = v.label('マグマだまり', [6.5, -(MC.d + MC.ry * 0.6) * PX, 0.1]);
const lA = v.label(v.mobile ? 'ア（火山岩）' : 'ア 地表付近（火山岩）', [0, 0, 0]);
const lB = v.label(v.mobile ? 'イ（深成岩）' : 'イ 地下深く（深成岩）', [108 * PX, -MC.d * PX, 0.1]);
const BX = 108 * PX, BY = -MC.d * PX;
const lLava = v.label('溶岩が流れ出す', [0, 0, 0], { sub: true }), lAsh = v.label('火山灰・軽石', [0, 0, 0], { sub: true }), lFlow = v.label('火砕流', [0, 0, 0], { sub: true });
const hud = $('hud3d'); hud.style.display = '';
const SM = v.mobile; if (SM) { hud.style.fontSize = '11px'; hud.style.padding = '3px 6px'; hud.style.left = hud.style.top = '6px'; }   // スマホは短く（注意書きは下の説明文にある）
const txt = id => ($(id) ? $(id).textContent : '');

let qKey = '', wl = 0;
v.onFrame((t, dt) => {
  const s = K.st(), q = clamp(s.p, 0, 1), key = q.toFixed(3);
  if (key !== qKey) {
    qKey = key; buildBody(q); const f = paintFace(q); wl = buildLava(q);
    const top = K.vh(0, q) * PX, da = f.da;
    lA.at(da * PX, (K.vh(da, q) - 7) * PX, 0.1);
    lShape.at(0, Math.max(top, K.vh(13, q) * PX) + 1.6, 0);
  }
  // イの文字は、カメラから見えている方の切り口に置く（マグマだまりの文字と重ねない）
  const cp = v.camera.position; if (cp.x > 0.3 * Math.hypot(cp.x, cp.z)) lB.at(0.1, BY, BX); else lB.at(BX, BY, 0.1);
  const surf = $('cool') && $('cool').value === 'surf';
  lA.el.className = 'lbl' + (surf ? ' acc' : ''); lB.el.className = 'lbl' + (surf ? '' : ' acc');
  const fromTop = v.cam.ph > 1.1;   // 真上からは切り口が見えないので、地下の文字は出さない
  lA.show = lB.show = lMag.show = !fromTop;
  if (SM) { lA.show = lA.show && surf; lB.show = lB.show && !surf; lMag.show = lMag.show && surf; }   // スマホは選んでいる方だけ
  lShape.set(SM ? txt('sShape') : txt('sShape') + '（' + txt('sColor') + '）');
  // 噴火（ページの「噴火を止める」と連動）
  const tm = s.tm, er = s.erupting, top = K.vh(0, q), R = K.reach(q);
  const wa = er ? clamp((q - 0.22) / 0.5, 0, 1) : 0, wb = er ? clamp((q - 0.3) / 0.3, 0, 1) : 0, wp = er ? clamp((q - 0.7) / 0.15, 0, 1) : 0, wlv = er ? wl : 0;
  lavas.visible = wlv > 0.03; lavaTex.offset.x = -tm * 0.6;
  lLava.show = wlv > 0.35; if (lLava.show) { const d = R * 0.5, a = LAVA_DIRS[2]; lLava.at(d * PX * Math.sin(a), K.vh(d, q) * PX + 1, d * PX * Math.cos(a)); }
  ash.visible = wa > 0.03; ashMat.opacity = 0.35 + 0.35 * wa;
  if (ash.visible) {
    const Hp = (60 + 150 * wa) * PX;
    for (let i = 0; i < NA; i++) { const u = (tm * 0.2 + i / NA) % 1, a = i * 2.39996, sp = u * (1.2 + 2 * wa) * ((i * 0.618) % 1);
      put(ash, i, u * u * 5 + Math.cos(a) * sp, top * PX + 0.6 + u * Hp, Math.sin(a) * sp, (0.5 + u * (0.9 + 1.6 * wa)) * (u > 0.97 ? (1 - u) / 0.03 : 1)); }
    ash.instanceMatrix.needsUpdate = true;
  }
  lAsh.show = wa > 0.35 && !fromTop; lAsh.at(3, top * PX + (60 + 150 * wa) * PX * 0.6, 0);
  bombs.visible = wb > 0.05;
  if (bombs.visible) { for (let i = 0; i < NB; i++) {   // ページと同じ放物線（px）：横 (28+7i)·1.5u、高さ (70+14·(i%3))·1.5u − 135u²
      const u = (tm * 0.55 + i * 0.127) % 1, a = i * 1.9 + 0.4, rp = (28 + i * 7) * 1.5 * u, hp = top + (70 + (i % 3) * 14) * 1.5 * u - 135 * u * u;
      const under = hp < K.vh(rp, q); put(bombs, i, rp * PX * Math.sin(a), hp * PX, rp * PX * Math.cos(a), under ? 0.001 : 0.28); } bombs.instanceMatrix.needsUpdate = true; }
  flow.visible = wp > 0.05; flowMat.opacity = 0.55 * wp;
  if (flow.visible) { const u0 = (tm * 0.17) % 1; for (let j = 0; j < NF; j++) { const uu = u0 - j * 0.025; if (uu < 0) { put(flow, j, 0, -99, 0, 0.001); continue; } const d = uu * (R + 130); put(flow, j, d * PX * Math.sin(FLOW_DIR), K.vh(d, q) * PX + 0.5, d * PX * Math.cos(FLOW_DIR), (7 + j * 0.8 + uu * 12) * PX); } flow.instanceMatrix.needsUpdate = true; }
  lFlow.show = wp > 0.4; if (lFlow.show) { const d = (R + 100); lFlow.at(d * PX * Math.sin(FLOW_DIR), 1.5, d * PX * Math.cos(FLOW_DIR)); }
  sparks.visible = wlv > 0.03;
  if (sparks.visible) { for (let i = 0; i < NS; i++) { const u = (tm * 1.1 + i * 0.137) % 1, a = i * 2.4; sPos.set([Math.cos(a) * u * (0.6 + (i % 4) * 0.4), top * PX + Math.sin(u * Math.PI) * (0.8 + 1.6 * wlv), Math.sin(a) * u * (0.6 + (i % 4) * 0.4)], i * 3); } sGeo.attributes.position.needsUpdate = true; }
  if (SM) hud.innerHTML = 'ねばりけ <b>' + Math.round(q * 100) + '</b>・' + txt('sShape') + '<br>' + (surf ? 'ア→' : 'イ→') + txt('sRock') + '（' + txt('sTex') + '）';
  else hud.innerHTML = 'マグマのねばりけ：<b>' + Math.round(q * 100) + '</b><br>火山の形：' + txt('sShape') + '／噴火：' + txt('sErupt') + '<br>' + (surf ? 'ア 地表付近で急に冷える → ' : 'イ 地下深くでゆっくり冷える → ') + txt('sRock') + '（' + txt('sTex') + '）<br><span style="font-size:11px;color:#64748b">大きさは実際の比率ではありません</span>';
});
