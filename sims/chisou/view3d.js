// 地層のでき方と柱状図 3D（ページの断面図と同じ計算を使う。手前の面＝上の断面図、奥（北）へ160m分を立体に）
// 東＝+x、北＝-z、上＝+y。1 = 10m、高さは横の2.5倍（ページの断面図と同じ強調）。奥の地形の起伏は模式
import { THREE, createView, water } from '../../assets/three/sim3d.js';
const $ = id => document.getElementById(id);
const C = window.__chisou;
const S = 0.1, VE = 2.5, EB = 12, ETOP = 92, ZD = 160, BD = 35;          // m（EB＝立体の底の標高、BD＝ボーリングの深さ）
const X = x => (x - 200) * S, Y = e => (e - EB) * S * VE, Z = n => n * S;  // x：西→東 0〜400m、e：標高、n：0＝ボーリングの線、−が北
const ease = t => t <= 0 ? 0 : (t >= 1 ? 1 : t * t * (3 - 2 * t));
const f1 = v => (Math.round(v * 10) / 10).toFixed(1);
const TY = Object.assign({ b: { n: '古い岩石', c: '#a8a29e', d: '#78716c' } }, C.TY);

const v = createView($('view3d'), {
  views: {
    persp: { tgt: [0, 5, -7], dist: 60, th: 0.55, ph: 0.42 },
    south: { tgt: [0, 7, 0], dist: 52, th: 0, ph: 0.05 },
    top: { tgt: [0, 4, -8], dist: 56, th: 0, ph: 1.42 },
    nw: { tgt: [0, 5, -8], dist: 60, th: Math.PI + 0.65, ph: 0.4 },
  },
  camRow: '#camRow3d', bg: 0xe3edf5, shadows: false, minDist: 12, maxDist: 160,
});
const { scene } = v;

// ---- 柱状図と同じ記号の模様 ----
function tile(kind) {
  const k = 1.7, w = kind === 'g' ? 22 : (kind === 'b' ? 12 : 14), h = kind === 'g' ? 18 : (kind === 'b' ? 12 : 10);
  const c = document.createElement('canvas'); c.width = Math.round(w * k); c.height = Math.round(h * k);
  const g = c.getContext('2d'); g.scale(k, k);
  if (kind === 'b') { g.fillStyle = TY.b.c; g.fillRect(0, 0, w, h); g.strokeStyle = TY.b.d; g.lineWidth = 1; g.beginPath(); g.moveTo(0, h); g.lineTo(w, 0); g.moveTo(-w / 2, h / 2); g.lineTo(w / 2, -h / 2); g.moveTo(w / 2, h * 1.5); g.lineTo(w * 1.5, h / 2); g.stroke(); return c; }
  const q = TY[kind]; g.fillStyle = q.c; g.fillRect(0, 0, w, h); g.strokeStyle = q.d; g.fillStyle = q.d;
  if (kind === 'g') { g.lineWidth = 0.9; [[5, 5, 2.8], [14, 5, 1.8], [18, 13, 2.5], [9, 13, 1.7], [2, 15, 1.2]].forEach(o => { g.beginPath(); g.arc(o[0], o[1], o[2], 0, Math.PI * 2); g.stroke(); }); }
  else if (kind === 's') { [[2, 2], [7, 4], [11, 1.5], [4, 7], [10, 8], [13, 5.5], [1, 9]].forEach(o => { g.beginPath(); g.arc(o[0], o[1], 0.75, 0, Math.PI * 2); g.fill(); }); }
  else if (kind === 'm') { g.lineWidth = 0.9; g.beginPath(); g.moveTo(1, 3); g.lineTo(6, 3); g.moveTo(8, 8); g.lineTo(13, 8); g.stroke(); }
  else { g.lineWidth = 1; g.beginPath(); g.moveTo(2, 2); g.lineTo(4, 6); g.lineTo(6, 2); g.moveTo(9, 5); g.lineTo(11, 9); g.lineTo(13, 5); g.stroke(); }
  return c;
}
const TILE = { g: tile('g'), s: tile('s'), m: tile('m'), a: tile('a'), b: tile('b') };
function pats(ctx) { const o = {}; for (const k in TILE) o[k] = ctx.createPattern(TILE[k], 'repeat'); return o; }
function canvasTex(w, h) {
  const cv = document.createElement('canvas'); cv.width = w; cv.height = h;
  const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4;
  return { cv, g: cv.getContext('2d'), t };
}

// ---- 地形（ボーリングの線 n=0 ではページの地表とぴったり同じ。奥は模式の起伏を足す） ----
const Vb = (x, n) => { const w = -n / ZD; return w * (4.5 * Math.sin(x * 0.0204 + 0.9) + 2 * Math.sin(x * 0.05 + 2) - 1.5); };
function G3(x, n, s) {
  const tg = C.topMat(x);
  if (s.phase === 'sea' || s.phase === 'lift') return tg;
  const gl = Math.min(C.Hx(x) + Vb(x, n), tg - 0.3);
  return s.phase === 'erode' ? tg + (gl - tg) * ease(s.ero) : gl;
}
// ある x での「標高の区間 → 地層」の表（ページの column() と同じ考え方。-1＝古い岩石）
function bounds(x, s) {
  const out = [];
  C.blocks(x).forEach(bk => {
    const b = C.base(x, bk[0]);
    const add = (lo, hi, i) => { lo = Math.max(lo, bk[1]); hi = Math.min(hi, bk[2]); if (hi > lo + 1e-6) out.push([lo, hi, i]); };
    add(-1e9, b, -1);
    for (let i = 0; i < s.L.length; i++) add(b + s.BOT[i], b + s.BOT[i + 1], i);
  });
  return out;
}
const kindOf = (i, s) => i < 0 ? 'b' : s.L[i].t;
function layerAt(list, e) { for (const r of list) if (e >= r[0] && e < r[1]) return r[2]; return -2; }
const xf = (() => { const z0 = C.zc(0), sl = C.zc(1) - z0; return e => (e - z0) / sl; })();   // 断層の線：標高 e での x

// ---- 立体の面（テクスチャ） ----
const FW = 1024, FH = 512, SW = 410;
const fx = x => x / 400 * FW, fy = e => (ETOP - e) / (ETOP - EB) * FH;
const FR = canvasTex(FW, FH), SDW = canvasTex(SW, FH), SDE = canvasTex(SW, FH), TOP = canvasTex(512, 205);
const PF = pats(FR.g), PW = pats(SDW.g), PE = pats(SDE.g);
function paintFront(s) {
  const g = FR.g, hasF = C.hasF(), top = s.L.length ? s.L[s.L.length - 1].t : 'b';
  g.fillStyle = PF[top]; g.fillRect(0, 0, FW, FH);
  const band = (lo, hi) => { g.beginPath(); for (let x = -8; x <= 408; x += 4) { const px = fx(x), py = fy(hi(x)); x === -8 ? g.moveTo(px, py) : g.lineTo(px, py); } for (let x = 408; x >= -8; x -= 4) g.lineTo(fx(x), fy(lo(x))); g.closePath(); };
  (hasF ? [false, true] : [false]).forEach(hw => {
    g.save();
    if (hasF) { const ea = EB - 40, eb = ETOP + 40, ex = hw ? -60 : FW + 60; g.beginPath(); g.moveTo(ex, fy(ea)); g.lineTo(fx(xf(ea)), fy(ea)); g.lineTo(fx(xf(eb)), fy(eb)); g.lineTo(ex, fy(eb)); g.closePath(); g.clip(); }
    const bs = x => C.base(x, hw);
    band(() => EB - 60, bs); g.fillStyle = PF.b; g.fill();
    for (let i = 0; i < s.L.length; i++) { if (s.L[i].th <= 0.001) continue; const last = i === s.L.length - 1; band(x => bs(x) + s.BOT[i], x => last ? ETOP + 60 : bs(x) + s.BOT[i + 1]); g.fillStyle = PF[s.L[i].t]; g.fill(); }
    g.strokeStyle = 'rgba(30,41,59,.6)'; g.lineWidth = 1.6;
    for (let i = 0; i <= s.L.length; i++) { g.beginPath(); for (let x = -8; x <= 408; x += 4) { const px = fx(x), py = fy(bs(x) + s.BOT[i]); x === -8 ? g.moveTo(px, py) : g.lineTo(px, py); } g.stroke(); }
    g.restore();
  });
  if (hasF) { g.strokeStyle = '#dc2626'; g.lineWidth = 4; g.beginPath(); g.moveTo(fx(xf(EB - 40)), fy(EB - 40)); g.lineTo(fx(xf(ETOP + 40)), fy(ETOP + 40)); g.stroke(); }
  FR.t.needsUpdate = true;
}
function paintSide(T, P, x, s) {
  const g = T.g, list = bounds(x, s), top = s.L.length ? s.L[s.L.length - 1].t : 'b';
  g.fillStyle = P[top]; g.fillRect(0, 0, SW, FH);
  list.forEach(r => { const y0 = fy(Math.min(r[1], ETOP + 60)), y1 = fy(Math.max(r[0], EB - 60)); g.fillStyle = P[kindOf(r[2], s)]; g.fillRect(0, y0, SW, y1 - y0); });
  g.strokeStyle = 'rgba(30,41,59,.6)'; g.lineWidth = 1.6;
  list.forEach(r => { const y = fy(r[1]); if (y > 0 && y < FH) { g.beginPath(); g.moveTo(0, y); g.lineTo(SW, y); g.stroke(); } });
  T.t.needsUpdate = true;
}
const hex = h => [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)];
const RGB = {}; for (const k in TY) RGB[k] = hex(TY[k].c);
function paintTop(s) {
  const W = TOP.cv.width, H = TOP.cv.height, img = TOP.g.createImageData(W, H), d = img.data, land = s.phase === 'land' || s.phase === 'erode';
  const hasF = C.hasF(), idx = new Int16Array(W * H);
  for (let i = 0; i < W; i++) {
    const x = (i + 0.5) / W * 400, list = bounds(x, s), zc = hasF ? C.zc(x) : 0;
    for (let j = 0; j < H; j++) {
      const n = -(j + 0.5) / H * ZD, e = G3(x, n, s);
      let li = layerAt(list, e - 0.05); if (li === -2) li = s.L.length - 1;
      idx[j * W + i] = li;
      const c = RGB[kindOf(li, s)], p = (j * W + i) * 4;
      const gr = land ? 0.15 : 0;                      // 陸では草の色を少し混ぜる
      d[p] = c[0] * (1 - gr) + 120 * gr; d[p + 1] = c[1] * (1 - gr) + 160 * gr; d[p + 2] = c[2] * (1 - gr) + 90 * gr; d[p + 3] = 255;
      if (hasF && land && Math.abs(e - zc) < 1.3) { d[p] = 220; d[p + 1] = 38; d[p + 2] = 38; }
    }
  }
  for (let j = 1; j < H; j++) for (let i = 1; i < W; i++) { const q = j * W + i; if (idx[q] !== idx[q - 1] || idx[q] !== idx[q - W]) { const p = q * 4; d[p] *= 0.55; d[p + 1] *= 0.55; d[p + 2] *= 0.55; } }
  TOP.g.putImageData(img, 0, 0); TOP.t.needsUpdate = true;
}

// ---- 形（帯の面と地表の網） ----
function strip(N, at, faceMat) {   // at(t) → [x, n]。下＝立体の底、上＝地表
  const pos = new Float32Array((N + 1) * 2 * 3), uv = new Float32Array((N + 1) * 2 * 2), ix = [];
  for (let i = 0; i < N; i++) { const a = i * 2; ix.push(a, a + 2, a + 1, a + 1, a + 2, a + 3); }
  const geo = new THREE.BufferGeometry(); geo.setAttribute('position', new THREE.BufferAttribute(pos, 3)); geo.setAttribute('uv', new THREE.BufferAttribute(uv, 2)); geo.setIndex(ix);
  const mesh = new THREE.Mesh(geo, faceMat); scene.add(mesh);
  return {
    mesh, update(lo, hi, uvOf) {
      for (let i = 0; i <= N; i++) {
        const [x, n] = at(i / N), e0 = lo(x, n), e1 = Math.max(e0, hi(x, n)), a = i * 6, b = i * 4, u = uvOf ? uvOf(i / N) : 0;
        pos.set([X(x), Y(e0), Z(n), X(x), Y(e1), Z(n)], a);
        uv.set([u, (e0 - EB) / (ETOP - EB), u, (e1 - EB) / (ETOP - EB)], b);
      }
      geo.attributes.position.needsUpdate = true; geo.attributes.uv.needsUpdate = true; geo.computeVertexNormals(); geo.computeBoundingSphere();
    },
  };
}
const faceMat = (t, k) => new THREE.MeshBasicMaterial({ map: t, side: THREE.DoubleSide, color: new THREE.Color(k, k, k) });
const NX = 100, NZ = 40;
const fFront = strip(NX, t => [t * 400, 0], faceMat(FR.t, 1));
const fBack = strip(NX, t => [t * 400, -ZD], faceMat(FR.t, 0.8));
const fWest = strip(NZ, t => [0, -ZD + t * ZD], faceMat(SDW.t, 0.86));
const fEast = strip(NZ, t => [400, -ZD + t * ZD], faceMat(SDE.t, 0.86));
const bottom = new THREE.Mesh(new THREE.PlaneGeometry(40, 16), new THREE.MeshBasicMaterial({ color: 0x57534e, side: THREE.DoubleSide }));
bottom.rotation.x = -Math.PI / 2; bottom.position.set(0, 0, -8); scene.add(bottom);
// 地表の網
const tGeo = new THREE.BufferGeometry();
const tPos = new Float32Array((NX + 1) * (NZ + 1) * 3), tUv = new Float32Array((NX + 1) * (NZ + 1) * 2), tIx = [];
for (let j = 0; j <= NZ; j++) for (let i = 0; i <= NX; i++) { const k = j * (NX + 1) + i; tUv[k * 2] = i / NX; tUv[k * 2 + 1] = 1 - j / NZ; if (i < NX && j < NZ) tIx.push(k, k + NX + 1, k + 1, k + 1, k + NX + 1, k + NX + 2); }
tGeo.setAttribute('position', new THREE.BufferAttribute(tPos, 3)); tGeo.setAttribute('uv', new THREE.BufferAttribute(tUv, 2)); tGeo.setIndex(tIx);
const topMesh = new THREE.Mesh(tGeo, new THREE.MeshStandardMaterial({ map: TOP.t, roughness: 1, metalness: 0, side: THREE.DoubleSide }));
scene.add(topMesh);
// 立体のふち
const edgeGeo = new THREE.BufferGeometry(); edgeGeo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(16 * 3), 3));
scene.add(new THREE.LineSegments(edgeGeo, new THREE.LineBasicMaterial({ color: 0x334155 })));
// 海（海の底に積もっているとき）
const wMat = water(0.38, 0x2f86d6);
const wFront = strip(NX, t => [t * 400, 0], wMat), wBack = strip(NX, t => [t * 400, -ZD], wMat), wWest = strip(NZ, t => [0, -ZD + t * ZD], wMat), wEast = strip(NZ, t => [400, -ZD + t * ZD], wMat);
const wTop = new THREE.Mesh(new THREE.PlaneGeometry(40, 16), new THREE.MeshStandardMaterial({ color: 0x5aa7e8, transparent: true, opacity: 0.45, roughness: 0.2, depthWrite: false, side: THREE.DoubleSide }));
wTop.rotation.x = -Math.PI / 2; scene.add(wTop);
const seaE = () => 18 + (282 - C.seaY()) / (254 / 69);   // ページの海面（断面図の画素 → 標高）

// ---- ボーリングの柱（A〜D） ----
const cores = [0, 1, 2, 3].map(() => {
  const T = canvasTex(48, 256), P = pats(T.g);
  T.t.wrapT = THREE.ClampToEdgeWrapping;
  const m = new THREE.Mesh(new THREE.CylinderGeometry(0.42, 0.42, 1, 20), new THREE.MeshBasicMaterial({ map: T.t, color: 0xffffff }));
  // ふち取り（少し太い円柱の裏側だけを描く）
  const edge = new THREE.Mesh(new THREE.CylinderGeometry(0.5, 0.5, 1.02, 20), new THREE.MeshBasicMaterial({ color: 0x1e293b, side: THREE.BackSide }));
  m.add(edge);
  const ring = new THREE.Mesh(new THREE.TorusGeometry(0.55, 0.08, 8, 24), new THREE.MeshBasicMaterial({ color: 0x1e293b }));
  ring.rotation.x = Math.PI / 2; scene.add(m, ring);
  return { T, P, m, edge, ring, lbl: v.label('', [0, 0, 0]) };
});
function paintCore(c, x, g, s) {
  const G = c.T.g, list = bounds(x, s), h = 256, ey = e => (g - e) / BD * h;
  G.fillStyle = c.P.b; G.fillRect(0, 0, 48, h);
  list.forEach(r => { if (r[1] < g - BD || r[0] > g) return; const y0 = ey(Math.min(r[1], g)), y1 = ey(Math.max(r[0], g - BD)); G.fillStyle = c.P[kindOf(r[2], s)]; G.fillRect(0, y0, 48, y1 - y0); G.fillStyle = 'rgba(30,41,59,.7)'; G.fillRect(0, y1 - 1, 48, 2); });
  c.T.t.needsUpdate = true;
}

// ---- 降ってくる火山灰・積もる粒 ----
const NP = 360, pPos = new Float32Array(NP * 3), seed = Array.from({ length: NP }, (_, i) => [((i * 0.6180339) % 1), ((i * 0.7548776) % 1), ((i * 0.5698403) % 1)]);
const pGeo = new THREE.BufferGeometry(); pGeo.setAttribute('position', new THREE.BufferAttribute(pPos, 3));
const pMat = new THREE.PointsMaterial({ color: 0x57534e, size: 0.32, transparent: true, opacity: 0.8, depthWrite: false });
const pts = new THREE.Points(pGeo, pMat); pts.frustumCulled = false; scene.add(pts);

// ---- 文字 ----
const lAsh = v.label('火山灰の層（鍵層）', [0, 0, 0], { accent: true });
const lW = v.label('西', [0, 0, 0]), lE = v.label('東', [0, 0, 0]), lN = v.label('北', [0, 0, 0], { sub: true }), lSea = v.label('海面', [0, 0, 0], { sub: true });
const TITLE = { sea: '海の底で地層が積もる', lift: '大地が隆起して、海の底が陸になる', erode: '雨や川の水で地表がけずられる（侵食）', land: 'いまの土地（手前の面＝上の断面図）' };
const hud = $('hud3d'); hud.style.display = '';
const SM = v.mobile; if (SM) { hud.style.fontSize = '11px'; hud.style.padding = '3px 6px'; hud.style.left = hud.style.top = '6px'; }   // スマホは短く（注意書きは下の説明文にある）

let painted = '', coreKey = '', lastPaint = -1;
function refresh(s) {
  const lo = () => EB, hi = (x, n) => G3(x, n, s);
  fFront.update(lo, hi, t => t); fBack.update(lo, hi, t => t);
  fWest.update(lo, hi, t => t); fEast.update(lo, hi, t => t);
  paintFront(s); paintSide(SDW, PW, 0, s); paintSide(SDE, PE, 400, s); paintTop(s);
  for (let j = 0; j <= NZ; j++) for (let i = 0; i <= NX; i++) { const x = i / NX * 400, n = -j / NZ * ZD, k = (j * (NX + 1) + i) * 3; tPos[k] = X(x); tPos[k + 1] = Y(G3(x, n, s)); tPos[k + 2] = Z(n); }
  tGeo.attributes.position.needsUpdate = true; tGeo.computeVertexNormals(); tGeo.computeBoundingSphere();
  const ep = edgeGeo.attributes.position, cs = [[0, 0], [400, 0], [400, -ZD], [0, -ZD]];
  cs.forEach(([x, n], i) => { ep.setXYZ(i * 2, X(x), 0, Z(n)); ep.setXYZ(i * 2 + 1, X(x), Y(G3(x, n, s)), Z(n)); const [x2, n2] = cs[(i + 1) % 4]; ep.setXYZ(8 + i * 2, X(x), 0, Z(n)); ep.setXYZ(9 + i * 2, X(x2), 0, Z(n2)); });
  ep.needsUpdate = true; edgeGeo.computeBoundingSphere();
}
function refreshWater(s) {
  const es = seaE(), on = s.phase === 'sea' || s.phase === 'lift';
  [wFront, wBack, wWest, wEast].forEach(w => { w.mesh.visible = on; });
  wTop.visible = on && es > EB;
  if (!on) { lSea.show = false; return; }
  const lo = (x, n) => G3(x, n, s), hi = () => es;
  wFront.update(lo, hi); wBack.update(lo, hi); wWest.update(lo, hi); wEast.update(lo, hi);
  wTop.position.set(0, Y(es), -8);
  lSea.at(X(14), Y(es) + 0.2, 0); lSea.show = es > C.topMat(14) + 1;
}

v.onFrame(t => {
  const s = C.st(), land = s.phase === 'land';
  const key = [s.phase, s.L.map(l => l.t + l.th.toFixed(2)).join(','), s.fA.toFixed(2), s.fS.toFixed(2), s.k, s.U, s.lift.toFixed(3), s.ero.toFixed(3)].join('|');
  if (key !== painted && (t - lastPaint > 0.1 || t < lastPaint)) { painted = key; lastPaint = t; refresh(s); coreKey = ''; }
  refreshWater(s);
  // ボーリングの柱
  const ck = [painted, s.B.map(b => b.x).join(','), s.drill.toFixed(2), s.sel].join('|');
  if (ck !== coreKey) {
    coreKey = ck;
    s.B.forEach((b, i) => {
      const c = cores[i], g = G3(b.x, 0, s), dd = land ? s.drill : 0, on = land && dd > 0.001;
      c.m.visible = on; c.ring.visible = land; c.lbl.show = land;
      if (!land) return;
      paintCore(c, b.x, g, s);
      const top = Y(g), len = Math.max(0.001, (Y(g) - Y(g - BD)) * dd);
      c.m.scale.y = len; c.m.position.set(X(b.x), top - len / 2, 0.3);
      c.T.t.repeat.set(1, dd); c.T.t.offset.set(0, 1 - dd);
      c.ring.position.set(X(b.x), top + 0.05, 0.3); c.ring.material.color.set(i === s.sel ? 0xf59e0b : 0x1e293b); c.edge.material.color.set(i === s.sel ? 0xf59e0b : 0x1e293b);
      c.lbl.el.className = 'lbl' + (i === s.sel ? ' acc' : ''); c.lbl.set(v.mobile ? b.n : b.n + ' ' + f1(g) + 'm'); c.lbl.at(X(b.x), top + 0.4, 0);   // スマホは記号だけ（標高は上の図に出ている）
    });
  }
  // 鍵層の文字（手前の面で、地表より下に見えている所）
  const ia = C.ashIdx(); let ax = null, ae = 0;
  if (ia >= 0 && s.L[ia].th > 0.3) for (let x = 385; x >= 15; x -= 10) {
    if (land && s.B.some(b => Math.abs(b.x - x) < 40)) continue;
    for (const bk of C.blocks(x)) { const e = C.base(x, bk[0]) + s.BOT[ia + 1]; if (e > bk[1] && e < bk[2] && e < G3(x, 0, s) - 2 && e > EB + 2) { ax = x; ae = e; break; } }
    if (ax !== null) break;
  }
  lAsh.show = ax !== null && v.camera.position.z > 0; if (ax !== null) lAsh.at(X(ax), Y(ae), 0.1);   // 手前の面が見えているときだけ
  const gw = G3(0, 0, s), ge = G3(400, 0, s), gn = G3(200, -ZD, s);
  lW.at(X(0) - 1.4, Y(gw) * 0.5, 0); lE.at(X(400) + 1.4, Y(ge) * 0.5, 0); lN.at(0, Y(gn) + 0.6, Z(-ZD) - 1);
  // 降ってくるもの
  const es = seaE(), top = s.L.length ? s.L[s.L.length - 1] : null;
  if (s.erupt > 0) {
    pMat.color.set(0x57534e); pMat.opacity = 0.85 * Math.min(1, s.erupt / 0.5); pMat.size = 0.3;
    for (let i = 0; i < NP; i++) { const [a, b, c] = seed[i], x = a * 400, n = -b * ZD, gy = Y(G3(x, n, s)), q = (s.tm * 0.45 + c) % 1, y0 = Y(ETOP) + 4; pPos.set([X(x) + Math.sin(s.tm + i) * 0.3, y0 - q * (y0 - gy), Z(n)], i * 3); }
    pts.visible = true;
  } else if (s.depositing && s.phase === 'sea' && top && top.t !== 'a') {
    const sp = top.t === 'g' ? 0.95 : (top.t === 's' ? 0.6 : 0.32), nn = top.t === 'g' ? 120 : (top.t === 's' ? 220 : NP);
    pMat.color.set(TY[top.t].d); pMat.opacity = 0.75; pMat.size = top.t === 'g' ? 0.34 : (top.t === 's' ? 0.22 : 0.15);
    const tg = C.topMat(200);
    for (let i = 0; i < NP; i++) { const [a, b, c] = seed[i], q = (s.tm * sp + c) % 1; pPos.set(i < nn ? [X(a * 400), Y(es) - q * (Y(es) - Y(tg)), Z(-b * ZD)] : [0, -999, 0], i * 3); }
    pts.visible = true;
  } else pts.visible = false;
  pGeo.attributes.position.needsUpdate = true;
  hud.innerHTML = '<b style="font-size:14px">' + TITLE[s.phase] + '</b>' + (land ? '<br>地層の傾き：' + ($('sTilt') ? $('sTilt').textContent : '') : '') + (SM ? '' : '<br><span style="font-size:11px;color:#64748b">高さは横の約2.5倍・奥の起伏は模式</span>');
});
