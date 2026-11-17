// 電気回路 3D（上の図の回路を「机の上の実物」の模型にし、上の図の状態＝つなぎ方・電圧・抵抗・粒の位置をそのまま読んで動かす）
// ページの座標（px）をそのまま使う：20px＝1。x＝右、z＝手前（上の図の下）、y＝高さ。真上から見ると上の図と同じ向きになる
// 中2モードだけ「電圧を高さで見る」：導線を電位の高さ（1 V＝0.5）に持ち上げる。電源で上がり、抵抗で下がる坂道のモデル
import { THREE, createView } from '../../assets/three/sim3d.js';
const $ = id => document.getElementById(id);
const K = window.__kairo;                       // ページ側のフック（calc・paths・off・fmt・st）
if (!K) throw new Error('__kairo がありません');
const PI = Math.PI, U = 20, UP = new THREE.Vector3(0, 1, 0), XA = new THREE.Vector3(1, 0, 0);
const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
const COL = { wire: 0x334155, lead: 0x92400e, cur: 0xf97316, ele: 0x2563eb, r1: 0x7c3aed, r2: 0x059669, am: 0x0e7490, vm: 0xb45309, amber: 0xf59e0b, arrow: 0xd97706 };
const FF = '"Hiragino Sans","Hiragino Kaku Gothic ProN","Noto Sans JP","Yu Gothic UI","Yu Gothic",Meiryo,sans-serif';
const HW = 0.13;      // 机の上の導線の高さ
const WR = 0.06;      // 導線の太さ（半径）
const LR = 0.035;     // 電圧計につなぐ細い導線
const KV = 0.5;       // 高さのモデル：1 V ＝ 0.5
const C2 = [205, 200], C4 = [223, 277];   // 図の中心（px）：中2／小4

const VIEW = {
  chu2: { persp: { tgt: [0, 0.5, 0.2], dist: 31, th: 0.45, ph: 0.6 }, top: { tgt: [0, 0, 0], dist: 33, th: 0, ph: 1.45 }, side: { tgt: [0, 2.0, 0], dist: 30, th: 0.25, ph: 0.2 } },
  sho4: { persp: { tgt: [0, 0.8, 0], dist: 30, th: 0.45, ph: 0.6 }, top: { tgt: [0, 0, 0], dist: 31, th: 0, ph: 1.45 }, side: { tgt: [0, 1.2, 0], dist: 28, th: 0.25, ph: 0.2 } },
};
const el = $('view3d');
const v = createView(el, {
  views: { persp: { ...VIEW.chu2.persp }, top: { ...VIEW.chu2.top }, side: { ...VIEW.chu2.side } },
  camRow: '#camRow3d', bg: 0xf8fafc, shadows: false, minDist: 5, maxDist: 90,
});
const { scene } = v, SM = v.mobile, ZF = SM ? 0.94 : 1;

// ---- 形の部品 ----
const boxGeo = new THREE.BoxGeometry(1, 1, 1), cylGeo = new THREE.CylinderGeometry(1, 1, 1, 14), coneGeo = new THREE.ConeGeometry(1, 1, 16), ballGeo = new THREE.SphereGeometry(1, 16, 12);
const std = (c, o) => new THREE.MeshStandardMaterial(Object.assign({ color: c, roughness: 0.65 }, o || {}));
const _d = new THREE.Vector3(), _A = new THREE.Vector3(), _B = new THREE.Vector3();
function setSeg(m, a, b, r) { _d.subVectors(b, a); const L = _d.length(); m.visible = L > 1e-4; if (!m.visible) return; m.position.copy(a).addScaledVector(_d, 0.5); m.scale.set(r, L, r); m.quaternion.setFromUnitVectors(UP, _d.multiplyScalar(1 / L)); }
function mkArrow(col, parent) {
  const mt = std(col, { roughness: 0.4 }), g = new THREE.Group(), sh = new THREE.Mesh(cylGeo, mt), hd = new THREE.Mesh(coneGeo, mt); g.add(sh, hd); parent.add(g);
  const u = new THREE.Vector3(), e = new THREE.Vector3();
  g.set = (a, b, r) => { u.subVectors(b, a); const L = u.length(); g.visible = L > 0.3; if (!g.visible) return; u.multiplyScalar(1 / L); const h = Math.min(L * 0.5, r * 5);
    e.copy(b).addScaledVector(u, -h); setSeg(sh, a, e, r); hd.position.copy(b).addScaledVector(u, -h / 2); hd.scale.set(r * 2.6, h, r * 2.6); hd.quaternion.setFromUnitVectors(UP, u); };
  return g;
}
const GLOW = (() => { const c = document.createElement('canvas'); c.width = c.height = 128; const g = c.getContext('2d'); const gr = g.createRadialGradient(64, 64, 6, 64, 64, 64); gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = gr; g.fillRect(0, 0, 128, 128); const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t; })();
const mkHalo = (col, parent) => { const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: GLOW, color: col, transparent: true, opacity: 0, depthWrite: false, depthTest: false })); s.visible = false; parent.add(s); return s; };
// 計器の目もり板（真上から見ると回路図の Ⓐ・Ⓥ に見える）
function faceTex(ch, sub, css) {
  const c = document.createElement('canvas'); c.width = c.height = 192; const g = c.getContext('2d');
  g.fillStyle = '#ffffff'; g.beginPath(); g.arc(96, 96, 94, 0, 7); g.fill();
  g.strokeStyle = css; g.lineWidth = 9; g.beginPath(); g.arc(96, 96, 89, 0, 7); g.stroke();
  g.strokeStyle = '#64748b'; g.lineWidth = 3; g.beginPath(); g.arc(96, 104, 62, -PI / 2 - 0.96, -PI / 2 + 0.96); g.stroke();
  for (let k = -4; k <= 4; k++) { const t = -PI / 2 + k * 0.24, l = k % 2 ? 7 : 12; g.beginPath(); g.moveTo(96 + Math.cos(t) * (62 - l), 104 + Math.sin(t) * (62 - l)); g.lineTo(96 + Math.cos(t) * 62, 104 + Math.sin(t) * 62); g.stroke(); }
  g.fillStyle = css; g.textAlign = 'center'; g.font = 'bold 60px ' + FF; g.fillText(ch, sub ? 84 : 96, 166);
  if (sub) { g.font = 'bold 36px ' + FF; g.fillText(sub, 124, 174); }
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; return t;
}
function mkMeter(parent, ch, sub, hex, css) {
  const mg = new THREE.Group(); parent.add(mg);
  const body = new THREE.Mesh(boxGeo, std(hex, { roughness: 0.55 })); body.scale.set(1.9, 0.56, 1.9); body.position.y = 0.15; mg.add(body);
  const face = new THREE.Mesh(new THREE.CircleGeometry(0.84, 40), new THREE.MeshBasicMaterial({ map: faceTex(ch, sub, css) })); face.rotation.x = -PI / 2; face.position.y = 0.435; mg.add(face);
  const piv = new THREE.Group(); piv.position.set(0, 0.46, 0.07); mg.add(piv);
  const nd = new THREE.Mesh(boxGeo, new THREE.MeshBasicMaterial({ color: 0xdc2626 })); nd.scale.set(0.045, 0.02, 0.52); nd.position.z = -0.26; piv.add(nd);
  mg.needle = f => { piv.rotation.y = -(clamp(f, 0, 1.04) * 2 - 1) * 0.96; };   // 0＝左はし、1＝右はし（目もりいっぱい）
  return mg;
}
const rangeOf = (x, list) => { for (const r of list) if (x <= r * 1.0001) return r; return list[list.length - 1]; };

// 机
{ const desk = new THREE.Mesh(boxGeo, std(0xe8dcc6, { roughness: 0.9 })); desk.scale.set(26, 0.4, 22); desk.position.y = -0.2; scene.add(desk); }
const G2 = new THREE.Group(), G4 = new THREE.Group(); G2.visible = G4.visible = false; scene.add(G2, G4);
const P2 = (px, py, h, out) => (out || new THREE.Vector3()).set((px - C2[0]) / U, h, (py - C2[1]) / U);
const P4 = (px, py, h, out) => (out || new THREE.Vector3()).set((px - C4[0]) / U, h, (py - C4[1]) / U);

// 電流の粒（上の図の粒と同じ道・同じ位置）
const MAXD = 220, dots = new THREE.InstancedMesh(ballGeo, std(COL.cur, { roughness: 0.4, emissive: 0x7c2d12, emissiveIntensity: 0.25 }), MAXD);
dots.count = 0; dots.frustumCulled = false; scene.add(dots);
const _M = new THREE.Matrix4(), _S = new THREE.Vector3(), _Q = new THREE.Quaternion(), _R = new THREE.Vector3(0.15, 0.15, 0.15);
function flow(s, C, hOf) {
  const ps = K.paths(s); let n = 0;
  for (const p of ps) {
    const pts = p.pts; let L = 0; for (let i = 1; i < pts.length; i++) L += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]);
    const a = pts[0], z = pts[pts.length - 1], closed = a[0] === z[0] && a[1] === z[1];
    const gap = closed ? L / Math.max(1, Math.round(L / 18)) : 18, o = K.off[p.id] || 0;      // 上の図の drawDots と同じ間かく・同じずれ
    let i = 1, acc = 0, sl = Math.hypot(pts[1][0] - pts[0][0], pts[1][1] - pts[0][1]);
    for (let d = o; d < L - 0.5 && n < MAXD; d += gap) {
      while (i < pts.length - 1 && d > acc + sl) { acc += sl; i++; sl = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); }
      const t = sl > 0 ? (d - acc) / sl : 0, px = pts[i - 1][0] + (pts[i][0] - pts[i - 1][0]) * t, py = pts[i - 1][1] + (pts[i][1] - pts[i - 1][1]) * t;
      _S.set((px - C[0]) / U, hOf(p.id, d, px, py), (py - C[1]) / U); _M.compose(_S, _Q, _R); dots.setMatrixAt(n++, _M);
    }
  }
  dots.count = n; dots.instanceMatrix.needsUpdate = true;
}

// ================= 中2：抵抗の直列・並列 =================
// 点＝[x, y, 電位の名前]。V＝電源の＋側、M＝2つの抵抗の間（直列だけ）、0＝－側、d＝いつも机の上
const SUP_M = [55, 262, '0'], SUP_P = [55, 208, 'V'];
const TOPO = {
  ser: {
    wires: [[[55, 208, 'V'], [55, 95, 'V'], [165, 95, 'V']], [[225, 95, 'M'], [275, 95, 'M']], [[335, 95, '0'], [375, 95, '0'], [375, 375, '0'], [55, 375, '0'], [55, 262, '0']]],
    res: [{ k: 'r1', nm: 'R₁', a: [165, 95, 'V'], b: [225, 95, 'M'] }, { k: 'r2', nm: 'R₂', a: [275, 95, 'M'], b: [335, 95, '0'] }],
    am: [{ k: 'I', p: [105, 95, 'V'], sub: '' }],
    vm: [{ k: 'V1', nm: 'V₁', sub: '1', m: [195, 38], a: [165, 95, 'V'], b: [225, 95, 'M'] }, { k: 'V2', nm: 'V₂', sub: '2', m: [305, 38], a: [275, 95, 'M'], b: [335, 95, '0'] }],
    junc: [], mid: [250, 95, 'M'],
  },
  par: {
    wires: [[[55, 208, 'V'], [55, 95, 'V'], [145, 95, 'V'], [265, 95, 'V']], [[145, 95, 'V'], [145, 205, 'V'], [265, 205, 'V']], [[325, 95, '0'], [375, 95, '0'], [375, 205, '0']], [[325, 205, '0'], [375, 205, '0'], [375, 375, '0'], [55, 375, '0'], [55, 262, '0']]],
    res: [{ k: 'r1', nm: 'R₁', a: [265, 95, 'V'], b: [325, 95, '0'] }, { k: 'r2', nm: 'R₂', a: [265, 205, 'V'], b: [325, 205, '0'] }],
    am: [{ k: 'I', p: [100, 95, 'V'], sub: '' }, { k: 'I1', p: [190, 95, 'V'], sub: '1' }, { k: 'I2', p: [190, 205, 'V'], sub: '2' }],
    vm: [{ k: 'V1', nm: 'V₁', sub: '1', m: [295, 38], a: [265, 95, 'V'], b: [325, 95, '0'] }, { k: 'V2', nm: 'V₂', sub: '2', m: [295, 262], a: [265, 205, 'V'], b: [325, 205, '0'] }],
    junc: [[145, 95, 'V'], [375, 205, '0']], mid: null,
  },
};
// 粒の道のり（px）から、その場所の電位（V）を出す。上の図の paths() の道と同じ並び
function potAt(id, a, V, V2) {
  const lin = (x, x0, x1, v0, v1) => v0 + (v1 - v0) * clamp((x - x0) / (x1 - x0), 0, 1);
  if (id === 's') return a < 27 ? lin(a, -27, 27, 0, V) : a >= 1173 ? lin(a, 1173, 1227, 0, V) : a < 250 ? V : a < 310 ? lin(a, 250, 310, V, V2) : a < 360 ? V2 : a < 420 ? lin(a, 360, 420, V2, 0) : 0;
  if (id === 'pm') return a < 27 ? lin(a, -27, 27, 0, V) : V;
  if (id === 'p1') return a < 120 ? V : a < 180 ? lin(a, 120, 180, V, 0) : 0;
  if (id === 'p2') return a < 230 ? V : a < 290 ? lin(a, 230, 290, V, 0) : 0;
  if (id === 'pr') return a >= 603 ? lin(a, 603, 657, 0, V) : 0;
  return 0;
}
const WHITE = new THREE.Color(0xffffff), ORANGE = new THREE.Color(0xfb923c);

function buildChu2(kind) {
  const T = TOPO[kind], g = new THREE.Group(); g.visible = false; G2.add(g);
  const labs = [], lab = (t, o) => { const l = v.label(t, [0, 0, 0], o || {}); l.show = false; labs.push(l); return l; };
  const segs = [], joints = [];
  const seg = (a, b, r, col, cur) => { const m = new THREE.Mesh(cylGeo, std(col, { roughness: 0.5 })); g.add(m); segs.push({ m, a, b, r, cur: !!cur }); };
  const ball = (p, r, col) => { const m = new THREE.Mesh(ballGeo, std(col, { roughness: 0.5 })); m.scale.setScalar(r); g.add(m); joints.push({ m, p }); };
  T.wires.forEach(w => { for (let i = 1; i < w.length; i++) seg(w[i - 1], w[i], WR, COL.wire, true); for (let i = 1; i < w.length - 1; i++) ball(w[i], WR, COL.wire); });
  seg(SUP_M, SUP_P, WR, COL.wire, true);                  // 電源の中（高さのモデルでは上り坂）
  T.junc.forEach(p => ball(p, 0.19, COL.wire));           // 分かれ道・合流の点

  // 抵抗器（電力が大きいほど、上の図と同じ式でオレンジに光る）
  const res = T.res.map(r => {
    const rg = new THREE.Group(); g.add(rg);
    const bm = std(0xffffff, { roughness: 0.55, emissive: 0xfb923c, emissiveIntensity: 0 }), body = new THREE.Mesh(boxGeo, bm); rg.add(body);
    const cm = std(COL[r.k], { roughness: 0.5 }), c1 = new THREE.Mesh(boxGeo, cm), c2 = new THREE.Mesh(boxGeo, cm); rg.add(c1, c2);
    return { r, rg, bm, body, c1, c2, halo: mkHalo(0xfbbf24, g), lb: lab(''), arr: mkArrow(COL.arrow, g) };
  });
  // 電流計（導線の途中に入れる）
  const ams = T.am.map(a => { const post = new THREE.Mesh(cylGeo, std(0x94a3b8)); g.add(post); return { a, mg: mkMeter(g, 'A', a.sub, COL.am, '#0e7490'), post, lb: lab('') }; });
  // 電圧計（抵抗の両はしに、細い導線でつなぐ）
  const vms = T.vm.map(m => {
    const a1 = [m.a[0], m.m[1], 'd'], b1 = [m.b[0], m.m[1], 'd'];
    seg(m.a, a1, LR, COL.lead); seg(a1, [m.m[0] - 16, m.m[1], 'd'], LR, COL.lead); seg(m.b, b1, LR, COL.lead); seg(b1, [m.m[0] + 16, m.m[1], 'd'], LR, COL.lead);
    ball(a1, LR, COL.lead); ball(b1, LR, COL.lead);
    return { m, mg: mkMeter(g, 'V', m.sub, COL.vm, '#b45309'), lb: lab('') };
  });
  // 電源装置（奥が＋、手前が－）
  const sup = new THREE.Group(); P2(55, 235, 0, sup.position); g.add(sup);
  const supM = std(0x475569, { roughness: 0.6, transparent: true }), sb = new THREE.Mesh(boxGeo, supM); sb.scale.set(2.5, 1.3, 2.7); sb.position.y = 0.65; sup.add(sb);
  { const tp = new THREE.Mesh(cylGeo, std(0xdc2626)); tp.scale.set(0.2, 0.3, 0.2); tp.position.set(0, 1.45, -1.05); sup.add(tp);
    const tm = new THREE.Mesh(cylGeo, std(0x111827)); tm.scale.set(0.2, 0.3, 0.2); tm.position.set(0, 1.45, 1.05); sup.add(tm);
    const dl = new THREE.Mesh(cylGeo, std(0xe2e8f0)); dl.scale.set(0.36, 0.12, 0.36); dl.position.set(0.6, 1.36, 0); sup.add(dl); }
  const lSup = lab('', { accent: true }), lPl = lab('＋', { sub: true }), lMi = lab('－', { sub: true });
  const lift = mkArrow(COL.arrow, g);
  // 高さのモデルの「幕」（机から導線までをうすい色でぬる）
  const nq = segs.filter(x => x.cur).length + T.res.length, cpos = new Float32Array(nq * 18), cgeo = new THREE.BufferGeometry();
  cgeo.setAttribute('position', new THREE.BufferAttribute(cpos, 3));
  const curtain = new THREE.Mesh(cgeo, new THREE.MeshBasicMaterial({ color: COL.amber, transparent: true, opacity: 0, side: THREE.DoubleSide, depthWrite: false })); curtain.frustumCulled = false; curtain.visible = false; g.add(curtain);
  const lTop = lab('', { sub: true }), lMid = T.mid ? lab('', { sub: true }) : null, lBot = lab('0 V', { sub: true });

  function update(s, pot, hk) {
    const f = K.fmt, H = key => key === 'd' ? HW : HW + hk * KV * pot[key], tall = hk > 0.5;
    segs.forEach(x => setSeg(x.m, P2(x.a[0], x.a[1], H(x.a[2]), _A), P2(x.b[0], x.b[1], H(x.b[2]), _B), x.r));
    joints.forEach(j => P2(j.p[0], j.p[1], H(j.p[2]), j.m.position));
    // 幕
    let n = 0; const quad = (a, b) => { const ax = (a[0] - C2[0]) / U, az = (a[1] - C2[1]) / U, bx = (b[0] - C2[0]) / U, bz = (b[1] - C2[1]) / U, ha = H(a[2]), hb = H(b[2]);
      cpos.set([ax, 0, az, bx, 0, bz, bx, hb, bz, ax, 0, az, bx, hb, bz, ax, ha, az], n); n += 18; };
    segs.forEach(x => { if (x.cur) quad(x.a, x.b); }); res.forEach(x => quad(x.r.a, x.r.b));
    cgeo.attributes.position.needsUpdate = true; curtain.visible = hk > 0.01; curtain.material.opacity = 0.2 * hk;
    // 抵抗器
    res.forEach((x, i) => {
      const r = x.r, a = P2(r.a[0], r.a[1], H(r.a[2]), _A), b = P2(r.b[0], r.b[1], H(r.b[2]), _B);
      _d.subVectors(b, a); const L = _d.length();
      x.rg.position.copy(a).addScaledVector(_d, 0.5); x.rg.position.y += 0.24; x.rg.quaternion.setFromUnitVectors(XA, _d.multiplyScalar(1 / L));
      x.body.scale.set(L - 0.24, 0.72, 0.92); x.c1.scale.set(0.14, 0.86, 1.06); x.c2.scale.set(0.14, 0.86, 1.06); x.c1.position.x = -L / 2 + 0.07; x.c2.position.x = L / 2 - 0.07;
      const Vr = i ? s.V2 : s.V1, Ir = i ? s.I2 : s.I1, Rr = i ? s.R2 : s.R1, bb = Math.min(1, Math.sqrt(Math.max(0, Vr * Ir) / 7.2));   // 明るさは上の図と同じ式（電力）
      x.bm.color.copy(WHITE).lerp(ORANGE, bb * 0.85); x.bm.emissiveIntensity = bb * 0.7;
      x.halo.visible = bb > 0.02; x.halo.position.copy(x.rg.position); x.halo.scale.setScalar(2.4 + 4.4 * bb); x.halo.material.opacity = 0.15 + 0.55 * bb;
      if (tall) x.lb.at(x.rg.position.x, x.rg.position.y + 0.75, x.rg.position.z); else x.lb.at(x.rg.position.x, HW, x.rg.position.z + 1.6);   // 机の上では手前（上の図と同じく抵抗の下）に出す
      x.lb.show = true;
      x.lb.set(tall ? r.nm + ' ' + f(Vr) + (SM ? ' V↓' : ' V 下がる') : r.nm + ' ' + f(Rr) + ' Ω');
      // 下がる高さの矢印（抵抗の出口側）
      const hi = H(r.a[2]), lo = H(r.b[2]); _A.set(b.x + 0.35, hi, b.z + 0.55); _B.set(b.x + 0.35, lo + 0.04, b.z + 0.55); x.arr.set(_A, _B, 0.07); if (!(tall && hi - lo > 0.45)) x.arr.visible = false;
    });
    // 電流計
    ams.forEach(x => { const h = H(x.a.p[2]), val = s[x.a.k]; P2(x.a.p[0], x.a.p[1], h, x.mg.position);
      x.mg.needle(val / rangeOf(val, [0.05, 0.5, 5, 50]));
      _A.set(x.mg.position.x, 0, x.mg.position.z); _B.set(x.mg.position.x, h - 0.13, x.mg.position.z); setSeg(x.post, _A, _B, 0.05); if (h < 0.5) x.post.visible = false;
      x.lb.at(x.mg.position.x, h + 0.75, x.mg.position.z); x.lb.set(f(val) + ' A'); x.lb.show = true; });
    // 電圧計
    vms.forEach(x => { const val = s[x.m.k]; P2(x.m.m[0], x.m.m[1], HW, x.mg.position); x.mg.needle(val / rangeOf(val, [3, 15]));
      x.lb.at(x.mg.position.x, HW + 0.75, x.mg.position.z); x.lb.set(x.m.nm + ' ' + f(val) + ' V'); x.lb.show = !(SM && tall); });   // スマホの高さ表示では、抵抗の札（何V下がる）にまとめる
    // 電源
    supM.opacity = 1 - 0.66 * hk; supM.depthWrite = hk < 0.5;
    const hv = H('V');
    lSup.at(sup.position.x, Math.max(2.1, hv + 0.75), sup.position.z); lSup.set(tall ? '電源 ' + f(s.V) + (SM ? ' V↑' : ' V 上がる') : '電源 ' + f(s.V) + ' V'); lSup.show = true;
    lPl.at(sup.position.x + 0.9, 1.6, sup.position.z - 1.05); lMi.at(sup.position.x + 0.9, 1.6, sup.position.z + 1.05); lPl.show = lMi.show = !tall;
    _A.set(sup.position.x - 1.7, 0.02, sup.position.z); _B.set(sup.position.x - 1.7, hv, sup.position.z); lift.set(_A, _B, 0.07); if (!(tall && hv > 0.6)) lift.visible = false;
    // 高さの数字
    P2(55, 150, hv + 0.2, lTop.p); lTop.set(f(s.V) + ' V'); lTop.show = tall && s.V > 0;
    if (lMid) { P2(T.mid[0], T.mid[1], H('M') + 0.2, lMid.p); lMid.set(f(s.V2) + ' V'); lMid.show = tall && s.V > 0; }
    P2(375, 300, HW + 0.2, lBot.p); lBot.show = tall;
  }
  return { g, labs, update };
}
const CH = { ser: buildChu2('ser'), par: buildChu2('par') };

// ================= 小4：かん電池のつなぎ方 =================
function galvTex() {     // けん流計の目もり（上の図の galv() と同じ並び。1px＝4）
  const c = document.createElement('canvas'); c.width = 416; c.height = 256; const g = c.getContext('2d');
  g.fillStyle = '#ffffff'; g.fillRect(0, 0, 416, 256); g.strokeStyle = '#475569'; g.lineWidth = 8; g.strokeRect(4, 4, 408, 248);
  const cx = 208, cy = 216, R = 160; g.strokeStyle = '#94a3b8'; g.lineWidth = 6; g.beginPath(); g.arc(cx, cy, R, -PI / 2 - PI / 3, -PI / 2 + PI / 3); g.stroke();
  for (let k = -5; k <= 5; k++) { const t = -PI / 2 + k * PI / 15, l = (k % 5 === 0) ? 36 : 20; g.beginPath(); g.moveTo(cx + Math.cos(t) * (R - l), cy + Math.sin(t) * (R - l)); g.lineTo(cx + Math.cos(t) * R, cy + Math.sin(t) * R); g.stroke(); }
  g.fillStyle = '#64748b'; g.textAlign = 'center'; g.font = '40px ' + FF; g.fillText('0', cx, cy - R - 12); g.fillText('0.5', cx - 172, cy - 92); g.fillText('0.5', cx + 172, cy - 92);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 4; return t;
}
function buildSho4() {
  const g = G4, AX = 1.0;     // AX＝かん電池のじくの高さ
  const labs = [], lab = (t, o) => { const l = v.label(t, [0, 0, 0], o || {}); l.show = false; labs.push(l); return l; };
  const wm = parent => { const m = new THREE.Mesh(cylGeo, std(COL.wire, { roughness: 0.5 })); parent.add(m); return m; };
  const jb = (px, py, r, parent) => { const b = new THREE.Mesh(ballGeo, std(COL.wire, { roughness: 0.5 })); b.scale.setScalar(r); P4(px, py, HW, b.position); parent.add(b); };
  const line = (pts, parent) => { for (let i = 1; i < pts.length; i++) setSeg(wm(parent), P4(pts[i - 1][0], pts[i - 1][1], HW, _A), P4(pts[i][0], pts[i][1], HW, _B), WR); for (let i = 1; i < pts.length - 1; i++) jb(pts[i][0], pts[i][1], WR, parent); };
  line([[430, 340], [430, 150], [266, 150]], g); line([[234, 150], [70, 150], [70, 212]], g); line([[70, 278], [70, 340]], g); jb(430, 340, WR, g); jb(70, 340, WR, g);
  const wR = wm(g), wL = wm(g);                       // かん電池につながる左右の導線（つなぎ方で長さが変わる）
  const parG = new THREE.Group(); g.add(parG);        // へい列つなぎのときだけ出る導線
  line([[165, 340], [165, 400], [195, 400]], parG); line([[305, 400], [335, 400], [335, 340]], parG); jb(165, 340, 0.19, parG); jb(335, 340, 0.19, parG);
  // かん電池（金色の帯とでっぱりが＋極）と電池ボックス
  function mkCell() {
    const cg = new THREE.Group(); g.add(cg); const inner = new THREE.Group(); cg.add(inner);
    const body = new THREE.Mesh(new THREE.CylinderGeometry(0.9, 0.9, 5.1, 28), std(0x1f2937, { roughness: 0.45 })); body.rotation.z = PI / 2; body.position.set(-0.2, AX, 0); inner.add(body);
    const band = new THREE.Mesh(new THREE.CylinderGeometry(0.912, 0.912, 1.3, 28), std(0xca8a04, { roughness: 0.4 })); band.rotation.z = PI / 2; band.position.set(1.3, AX, 0); inner.add(band);
    const nub = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.35, 0.4, 18), std(0x9ca3af, { roughness: 0.35, metalness: 0.4 })); nub.rotation.z = PI / 2; nub.position.set(2.55, AX, 0); inner.add(nub);
    const base = new THREE.Mesh(boxGeo, std(0x64748b)); base.scale.set(6.0, 0.1, 2.1); base.position.y = 0.05; cg.add(base);
    [-1, 1].forEach(sg => { const pl = new THREE.Mesh(boxGeo, std(0xb6bcc6, { roughness: 0.35, metalness: 0.5 })); pl.scale.set(0.12, 1.5, 1.3); pl.position.set(sg * 2.86, 0.75, 0); cg.add(pl); });
    return { cg, inner, lp: lab('＋'), lm: lab('－') };
  }
  const cA = mkCell(), cB = mkCell();
  // 豆電球（ソケットつき）
  const bulb = new THREE.Group(); P4(250, 150, 0, bulb.position); g.add(bulb);
  { const sock = new THREE.Mesh(cylGeo, std(0x94a3b8)); sock.scale.set(0.85, 0.45, 0.85); sock.position.y = 0.225; bulb.add(sock);
    const screw = new THREE.Mesh(cylGeo, std(0xb8bec8, { metalness: 0.5, roughness: 0.35 })); screw.scale.set(0.42, 0.6, 0.42); screw.position.y = 0.75; bulb.add(screw);
    [-1, 1].forEach(sg => { const lg = new THREE.Mesh(cylGeo, std(0x78716c)); bulb.add(lg); setSeg(lg, _A.set(sg * 0.16, 1.05, 0), _B.set(sg * 0.3, 2.0, 0), 0.025); }); }
  const glassM = new THREE.MeshStandardMaterial({ color: 0xf8fafc, roughness: 0.15, transparent: true, opacity: 0.6, emissive: 0xfde047, emissiveIntensity: 0 });
  const glass = new THREE.Mesh(new THREE.SphereGeometry(1.2, 28, 20), glassM); glass.position.y = 2.05; bulb.add(glass);
  const filM = std(0x78716c, { emissive: 0xea580c, emissiveIntensity: 0 }), fil = new THREE.Mesh(new THREE.TorusGeometry(0.3, 0.035, 8, 20), filM); fil.position.y = 2.0; bulb.add(fil);
  const bHalo = mkHalo(0xfde047, bulb); bHalo.position.y = 2.05;
  const G_OFF = new THREE.Color(0xf8fafc), G_ON = new THREE.Color(0xfde047), F_OFF = new THREE.Color(0x78716c), F_ON = new THREE.Color(0xea580c);
  // モーター（じくを上に向け、プロペラを真上から見ると上の図と同じ）
  const motor = new THREE.Group(); P4(250, 150, 0, motor.position); g.add(motor);
  { const mb = new THREE.Mesh(cylGeo, std(0xcbd5e1, { roughness: 0.4, metalness: 0.3 })); mb.scale.set(1.2, 1.4, 1.2); mb.position.y = 0.7; motor.add(mb);
    const sh = new THREE.Mesh(cylGeo, std(0x334155)); sh.scale.set(0.12, 0.9, 0.12); sh.position.y = 1.85; motor.add(sh); }
  const prop = new THREE.Group(); prop.position.y = 2.25; motor.add(prop);
  { const hub = new THREE.Mesh(ballGeo, std(0x334155)); hub.scale.setScalar(0.3); prop.add(hub);
    for (let k = 0; k < 3; k++) { const arm = new THREE.Group(); arm.rotation.y = k * 2 * PI / 3; prop.add(arm);
      const bl = new THREE.Mesh(ballGeo, std(0x2563eb, { transparent: true, opacity: 0.8, roughness: 0.4 })); bl.scale.set(0.45, 0.05, 1.1); bl.position.z = -1.2; arm.add(bl); } }
  // 回る向きの矢印（上の図と同じ弧）
  const A0 = -PI * 0.82, A1 = -PI * 0.18, RA = 2.8, arcPts = [];
  for (let k = 0; k <= 16; k++) { const t = A0 + (A1 - A0) * k / 16; arcPts.push(new THREE.Vector3(RA * Math.cos(t), 2.25, RA * Math.sin(t))); }
  motor.add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(arcPts), 32, 0.06, 8), std(0x2563eb)));
  const heads = [[A1, 1], [A0, -1]].map(([e, dir]) => { const h = new THREE.Mesh(coneGeo, std(0x2563eb)); h.scale.set(0.3, 0.7, 0.3); h.position.set(RA * Math.cos(e), 2.25, RA * Math.sin(e));
    h.quaternion.setFromUnitVectors(UP, new THREE.Vector3(-Math.sin(e) * dir, 0, Math.cos(e) * dir)); motor.add(h); return h; });
  // けん流計（箱の上の面が目もり）
  const gal = new THREE.Group(); P4(70, 245, 0, gal.position); g.add(gal);
  { const gb = new THREE.Mesh(boxGeo, std(0xe2e8f0, { roughness: 0.5 })); gb.scale.set(5.4, 0.9, 3.4); gb.position.y = 0.45; gal.add(gb);
    const gf = new THREE.Mesh(new THREE.PlaneGeometry(5.2, 3.2), new THREE.MeshBasicMaterial({ map: galvTex() })); gf.rotation.x = -PI / 2; gf.position.y = 0.905; gal.add(gf); }
  const gp = new THREE.Group(); gp.position.set(0, 0.94, 1.1); gal.add(gp);
  { const gn = new THREE.Mesh(boxGeo, new THREE.MeshBasicMaterial({ color: 0xdc2626 })); gn.scale.set(0.09, 0.03, 1.75); gn.position.z = -0.875; gp.add(gn);
    const hb = new THREE.Mesh(cylGeo, new THREE.MeshBasicMaterial({ color: 0x334155 })); hb.scale.set(0.16, 0.06, 0.16); gp.add(hb); }
  // 電流の向きの矢じるし（上の図と同じ3か所）
  const tips = [[430, 250, 0, 0, -1], [350, 150, -1, 0, 0], [110, 340, 1, 0, 0]].map(([px, py, dx, dy, dz]) => { const c = new THREE.Mesh(coneGeo, std(COL.cur, { roughness: 0.4 })); c.scale.set(0.3, 0.75, 0.3); P4(px, py, HW, c.position); g.add(c); return { c, d: new THREE.Vector3(dx, dy, dz) }; });
  const lLoad = lab('', { sub: true }), lGal = lab(''), lDir = lab('電流の向き', { sub: true });

  function update(s, st) {
    const f = K.fmt, pr = !st.rev, ser = s.bat === 'ser', par = s.bat === 'par', xL = ser ? 140 : 195, xR = ser ? 360 : 305;
    setSeg(wR, P4(xR, 340, HW, _A), P4(430, 340, HW, _B), WR); setSeg(wL, P4(70, 340, HW, _A), P4(xL, 340, HW, _B), WR);
    parG.visible = par;
    P4(ser ? 195 : 250, 340, 0, cA.cg.position); cB.cg.visible = s.bat !== 'one'; P4(ser ? 305 : 250, ser ? 340 : 400, 0, cB.cg.position);
    [cA, cB].forEach(c => { c.inner.rotation.y = pr ? 0 : PI; const on = c.cg.visible, sg = pr ? 1 : -1;
      c.lp.at(c.cg.position.x + sg * 2.45, 2.15, c.cg.position.z); c.lm.at(c.cg.position.x - sg * 2.45, 2.15, c.cg.position.z); c.lp.show = c.lm.show = on; });
    const bulbOn = s.load === 'bulb'; bulb.visible = bulbOn; motor.visible = !bulbOn;
    const b = Math.min(1, Math.sqrt(s.P / (4 * K.E1 * K.E1 / K.RL)));       // 明るさは上の図と同じ式
    glassM.color.copy(G_OFF).lerp(G_ON, b > 0.02 ? Math.min(1, 0.35 + 0.65 * b) : 0); glassM.emissiveIntensity = b * 0.9;
    filM.color.copy(F_OFF).lerp(F_ON, b); filM.emissiveIntensity = b * 1.5;
    bHalo.visible = bulbOn && b > 0.02; bHalo.scale.setScalar(3 + 4 * b); bHalo.material.opacity = 0.25 + 0.6 * b;
    prop.rotation.y = -st.ang;                                                // 上の図のプロペラと同じ角度
    heads[0].visible = pr; heads[1].visible = !pr;
    gp.rotation.y = -clamp(s.I * (pr ? 1 : -1) / 0.5, -1.15, 1.15) * PI / 3;   // はりのふれ（上の図と同じ式）
    tips.forEach(t => { _d.copy(t.d).multiplyScalar(pr ? 1 : -1); t.c.quaternion.setFromUnitVectors(UP, _d); });
    lLoad.set(bulbOn ? '豆電球' : 'モーター'); lLoad.at(bulb.position.x, bulbOn ? 3.6 : 3.0, bulb.position.z); lLoad.show = true;
    lGal.set((SM ? '' : 'けん流計 ') + f(s.I) + ' A'); lGal.at(gal.position.x, 1.5, gal.position.z); lGal.show = true;
    P4(430, 250, 0.9, lDir.p); lDir.show = true;
  }
  // 粒の高さ：かん電池とけん流計の中を通る
  const hOf = (s) => { const ser = s.bat === 'ser', par = s.bat === 'par', x0 = ser ? 140 : 195, x1 = ser ? 360 : 305;
    return (id, d, px, py) => ((Math.abs(py - 340) < 0.5 || (par && Math.abs(py - 400) < 0.5)) && px >= x0 - 1 && px <= x1 + 1) ? AX : (Math.abs(px - 70) < 0.5 && py > 212 && py < 278) ? 0.45 : HW; };
  return { g, labs, update, hOf };
}
const S4 = buildSho4();

// ================= 「電圧を高さで見る」ボタン =================
let hOn = false, hk = 0, cur = '';
const tg = document.createElement('button'); tg.type = 'button'; tg.id = 'hgt3d';
tg.style.cssText = 'position:absolute;left:8px;bottom:8px;z-index:3;padding:' + (SM ? '6px 9px' : '8px 12px') + ';font-size:' + (SM ? '12px' : '13px') + ';font-weight:800;border:1px solid var(--teal);border-radius:6px;background:#fff;color:var(--teal-d);cursor:pointer;box-shadow:0 1px 4px rgba(20,24,29,.12)';
el.appendChild(tg);
const tgText = () => { tg.textContent = hOn ? (SM ? '↩ 机の上にもどす' : '↩ 机の上の回路にもどす') : (SM ? '⛰ 電圧を高さで見る' : '⛰ 電圧を高さで見る（坂道のモデル）'); tg.setAttribute('aria-pressed', hOn ? 'true' : 'false'); };
function setH(on, moveCam) { hOn = on; tgText(); if (moveCam) v.setView(on ? 'side' : 'persp'); }
tg.addEventListener('click', () => setH(!hOn, true));
tgText();
{ const sb = document.querySelector('#camRow3d button[data-v="side"]'); if (sb) sb.addEventListener('click', () => { if (cur !== 'sho4' && !hOn) setH(true, false); }); }

function applyViews(mode, snap) {
  const V = VIEW[mode]; for (const k in V) Object.assign(v.views[k], { tgt: V[k].tgt.slice(), dist: V[k].dist * ZF, th: V[k].th, ph: V[k].ph });
  const b = document.querySelector('#camRow3d button.on'); v.setView(b ? b.dataset.v : 'persp', snap);
}

// ---- 画面左上の説明 ----
const hud = $('hud3d'); hud.style.display = '';
if (SM) { hud.style.fontSize = '11px'; hud.style.padding = '3px 6px'; hud.style.left = hud.style.top = '6px'; hud.style.maxWidth = '92%'; }
function hud2(s, st) {
  const f = K.fmt, nm = s.ser ? '直列回路' : '並列回路';
  if (!(s.V > 0)) return nm + '：電圧が <b>0 V</b> なので電流は流れない';
  if (hk > 0.5) {
    const e = st.ele ? '<br>※青い粒は電子。－の電気をもつので、電流の向きとは逆に動く' : '';
    return s.ser ? '高さ＝電圧：<b>' + f(s.V) + ' V</b> ＝ ' + f(s.V1) + ' V ＋ ' + f(s.V2) + ' V' + (SM ? '' : '<br>R₁とR₂で下がる高さの合計が、電源の電圧になる（電流はどこも ' + f(s.I) + ' A）' + e)
                 : '高さ＝電圧：R₁もR₂も <b>' + f(s.V) + ' V</b> 下がる' + (SM ? '' : '<br>電流は ' + f(s.I1) + ' A と ' + f(s.I2) + ' A に分かれ、合わせて ' + f(s.I) + ' A' + e);
  }
  return nm + '：全体の電流 <b>' + f(s.I) + ' A</b>' + (SM ? '' : '<br>全体の抵抗 ' + f(s.R) + ' Ω・' + (st.ele ? '青い粒＝電子（－極から＋極へ）' : 'オレンジの粒＝電流（＋極から－極へ）'));
}
function hud4(s, st) {
  const f = K.fmt, bulbOn = s.load === 'bulb';
  const nm = { one: 'かん電池1個', ser: 'かん電池2個の直列つなぎ', par: 'かん電池2個のへい列つなぎ' }[s.bat];
  const msg = s.bat === 'one' ? 'これを「1個のとき」として、つなぎ方をくらべよう' : s.bat === 'ser' ? (bulbOn ? '電流が大きくなり、豆電球が明るくなる' : '電流が大きくなり、モーターが速く回る') : '電流の大きさは1個のときと同じ。かん電池は長持ち';
  return (SM ? { one: '1個', ser: '直列つなぎ', par: 'へい列つなぎ' }[s.bat] : nm) + '：電流 <b>' + f(s.I) + ' A</b>' + (SM ? '' : '<br>' + msg + '（けん流計のはりは' + (st.rev ? '左' : '右') + 'にふれる）');
}

// ---- 毎フレーム ----
const sm = { V: 0, V2: 0, init: false }, pot = { V: 0, M: 0, 0: 0 };
v.onFrame((t, dt) => {
  const s = K.calc(), st = K.st(), m4 = s.mode === 'sho4', key = m4 ? 'sho4' : (s.ser ? 'ser' : 'par');
  if (key !== cur) {
    const first = !cur, modeChanged = first || (key === 'sho4') !== (cur === 'sho4');
    G2.visible = !m4; G4.visible = m4; CH.ser.g.visible = key === 'ser'; CH.par.g.visible = key === 'par';
    [CH.ser, CH.par, S4].forEach(o => o.labs.forEach(l => { l.show = false; }));
    tg.style.display = m4 ? 'none' : '';
    if (modeChanged) applyViews(m4 ? 'sho4' : 'chu2', first);
    cur = key;
  }
  const want = hOn && !m4 ? 1 : 0; hk += (want - hk) * (1 - Math.pow(0.001, dt)); if (Math.abs(want - hk) < 0.003) hk = want;
  if (m4) {
    S4.update(s, st);
    dots.material.color.setHex(COL.cur); dots.material.emissive.setHex(0x7c2d12);
    flow(s, C4, S4.hOf(s));
    hud.innerHTML = hud4(s, st);
  } else {
    const tv2 = s.ser ? s.V2 : 0, kk = sm.init ? 1 - Math.pow(0.0004, dt) : 1; sm.init = true;
    sm.V += (s.V - sm.V) * kk; sm.V2 += (tv2 - sm.V2) * kk;      // 高さはなめらかに変える（数字は上の図と同じ値をそのまま出す）
    pot.V = sm.V; pot.M = sm.V2;
    CH[key].update(s, pot, hk);
    dots.material.color.setHex(st.ele ? COL.ele : COL.cur); dots.material.emissive.setHex(st.ele ? 0x1e3a8a : 0x7c2d12);
    flow(s, C2, (id, d) => HW + hk * KV * potAt(id, d, sm.V, sm.V2));
    hud.innerHTML = hud2(s, st);
  }
});
