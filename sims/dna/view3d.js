// DNA二重らせん 3D（1 = 1nm。直径約2nm・塩基対10個で1回転・1回転約3.4nm＝ページの表と同じ値）
// 2本の鎖（糖とリン酸）を塩基のペア（A–T、G–C）がつなぐ右巻きのらせん。上の「回転スピード」と連動
// 「ほどいてコピー」で、ほどけた鎖それぞれに相手の塩基が組んで同じDNAが2つできる様子（はしごの形にのばした模式）
import { THREE, createView } from '../../assets/three/sim3d.js';
const $ = id => document.getElementById(id);
const D = window.__dna;
const N = 24, RISE = 0.34, TW = Math.PI / 5, R = 1.0, OFF = Math.PI * 0.83;   // 塩基対24個・1個ごとに0.34nm・36°・半径1nm・2本の鎖のずれ（溝ができる。模式）
const SEQ = 'ATGCGTACCAGGATCCTAGCTTAC', PAIR = { A: 'T', T: 'A', G: 'C', C: 'G' };
const BC = { A: 0xf97316, T: 0xfacc15, G: 0x22c55e, C: 0xa78bfa };
const S1 = 0xf43f5e, S2 = 0x22d3ee, NEWC = 0xe2e8f0;
const clamp = (v, a, b) => Math.max(a, Math.min(b, v)), sm = t => t <= 0 ? 0 : t >= 1 ? 1 : t * t * (3 - 2 * t);
const Y0 = -(N - 1) * RISE / 2;

const ZM = matchMedia('(max-width:640px)').matches ? 0.8 : 1;   // スマホは少し近づけて、模型を大きく見せる
const v = createView($('view3d'), {
  views: {
    persp: { tgt: [0, 0, 0], dist: 21 * ZM, th: 0.35, ph: 0.22 },
    side: { tgt: [0, 0, 0], dist: 20 * ZM, th: 0, ph: 0 },
    top: { tgt: [0, 0, 0], dist: 16 * ZM, th: 0, ph: 1.42 },
  },
  camRow: '#camRow3d', bg: 0x0b1020, shadows: false, minDist: 4, maxDist: 60,
});
const { scene } = v;
v.hemi.intensity = 0.8; v.sun.intensity = 1.6; v.sun.position.set(20, 30, 40);
const G = new THREE.Group(); scene.add(G);
const M = c => new THREE.MeshStandardMaterial({ color: c, roughness: 0.45, metalness: 0.05 });

// ---- 部品 ----
const ballG = new THREE.SphereGeometry(0.17, 16, 12), plateG = new THREE.BoxGeometry(1, 0.08, 0.34), hbG = new THREE.CylinderGeometry(0.025, 0.025, 1, 6);
const hbM = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.85 });
function nuc(strandColor, base) {   // 1つのヌクレオチド＝リン酸の玉＋塩基の板
  const ball = new THREE.Mesh(ballG, M(strandColor)), plate = new THREE.Mesh(plateG, M(BC[base]));
  G.add(ball); G.add(plate); return { ball, plate, base, p: new THREE.Vector3() };
}
const hbonds = (n) => Array.from({ length: n }, () => { const m = new THREE.Mesh(hbG, hbM); G.add(m); return m; });
const pairs = [...SEQ].map((b, i) => ({
  o1: nuc(S1, b), o2: nuc(S2, PAIR[b]),          // もとの2本
  n1: nuc(NEWC, PAIR[b]), n2: nuc(NEWC, b),      // コピーで新しくできる2本（左右に1本ずつ）
  hb: hbonds(b === 'A' || b === 'T' ? 2 : 3), hb1: hbonds(b === 'A' || b === 'T' ? 2 : 3), hb2: hbonds(b === 'A' || b === 'T' ? 2 : 3),
}));
const tube = (c) => { const m = new THREE.Mesh(new THREE.BufferGeometry(), M(c)); G.add(m); return m; };
const t1 = tube(S1), t2 = tube(S2), tn1 = tube(NEWC), tn2 = tube(NEWC);
function setTube(m, pts) {
  m.geometry.dispose();
  if (pts.length < 2) { m.visible = false; m.geometry = new THREE.BufferGeometry(); return; }
  m.visible = true; m.geometry = new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), pts.length * 8, 0.1, 8, false);
}
const Q = new THREE.Quaternion(), UP = new THREE.Vector3(0, 1, 0), XA = new THREE.Vector3(1, 0, 0), T = new THREE.Vector3(), Dv = new THREE.Vector3();
function placePlate(n, from, to, gap, s) {   // from（リン酸）から相手の方へ、真ん中のすき間の手前までのびる板
  Dv.subVectors(to, from); const L = Dv.length(), len = Math.max(0.01, L / 2 - gap - 0.12); Dv.normalize();
  n.plate.position.copy(from).addScaledVector(Dv, 0.12 + len / 2);
  n.plate.quaternion.setFromUnitVectors(XA, Dv); n.plate.scale.set(len, s, s);
}
function placeHB(list, a, b, gap, on) {   // 水素結合（白い短い線）：AとTは2本、GとCは3本
  Dv.subVectors(b, a); const L = Dv.length(); Dv.normalize();
  const mid = T.addVectors(a, b).multiplyScalar(0.5), side = new THREE.Vector3().crossVectors(Dv, UP).normalize();
  list.forEach((m, k) => { m.visible = on; if (!on) return; const o = (k - (list.length - 1) / 2) * 0.11;
    m.position.copy(mid).addScaledVector(side, o); m.quaternion.setFromUnitVectors(UP, Dv); m.scale.set(1, gap * 2 + 0.04, 1); });
}

// ---- 寸法の線（模型の外。回さない） ----
const dimM = new THREE.LineBasicMaterial({ color: 0x94a3b8 });
const lineOf = pts => { const l = new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts.map(p => new THREE.Vector3(...p))), dimM); scene.add(l); return l; };
const yb = Y0 - 0.7, x0 = 1.85;
const dimD = lineOf([[-R, yb, 0], [R, yb, 0]]), dimD2 = lineOf([[-R, yb - 0.15, 0], [-R, yb + 0.15, 0]]), dimD3 = lineOf([[R, yb - 0.15, 0], [R, yb + 0.15, 0]]);
const yt = Y0, dimP = lineOf([[x0, yt, 0], [x0, yt + 10 * RISE, 0]]), dimP2 = lineOf([[x0 - 0.15, yt, 0], [x0 + 0.15, yt, 0]]), dimP3 = lineOf([[x0 - 0.15, yt + 10 * RISE, 0], [x0 + 0.15, yt + 10 * RISE, 0]]);
const dims = [dimD, dimD2, dimD3, dimP, dimP2, dimP3];

// ---- 文字 ----
const SM = v.mobile;
const anchor = () => { const o = new THREE.Object3D(); G.add(o); return o; };
const aBack = anchor(), aAT = anchor(), aGC = anchor(), aOld = anchor(), aNew = anchor(), aFork = anchor();
const lBack = v.label(SM ? '糖とリン酸の鎖' : '糖とリン酸の鎖（2本）', [0, 0, 0], { obj: aBack });
const lAT = v.label(SM ? 'A–T 結合2本' : 'A–T（水素結合2本）', [0, 0, 0], { obj: aAT }), lGC = v.label(SM ? 'G–C 結合3本' : 'G–C（水素結合3本）', [0, 0, 0], { obj: aGC });
const lDia = v.label('直径 約2nm', [0, yb - 0.1, 0], { sub: true }), lPitch = v.label('1回転 約3.4nm（塩基対10個）', [x0 + 0.6, yt + 10 * RISE + 0.1, 0], { sub: true });
const lOld = v.label('もとの鎖', [0, 0, 0], { obj: aOld }), lNew = v.label('新しくできる鎖', [0, 0, 0], { obj: aNew, accent: true }), lFork = v.label('ここでほどける', [0, 0, 0], { obj: aFork, sub: true });
const hud = $('hud3d'); hud.style.display = '';
if (SM) { hud.style.fontSize = '11px'; hud.style.padding = '3px 6px'; hud.style.left = hud.style.top = '6px'; }

// ---- 「ほどいてコピー」のボタン（3Dの下に足す） ----
const row = document.createElement('div'); row.className = 'pick-row'; row.style.marginTop = '8px';
row.innerHTML = '<button data-m="helix" class="on">ふつうのらせん</button><button data-m="copy">ほどいてコピーする（複製）</button>';
$('camRow3d').after(row);
let mode = 'helix', f = 0, rot = 0, lastP = null, settle = 0, lastKey = '';
row.querySelectorAll('button').forEach(b => b.addEventListener('click', () => {
  mode = b.dataset.m; f = 0; settle = 0; row.querySelectorAll('button').forEach(x => x.classList.toggle('on', x === b));
  if (mode === 'copy') v.setView('side');
}));

// ---- 毎フレーム ----
const hp = (i, a) => new THREE.Vector3(R * Math.cos(a), Y0 + i * RISE, -R * Math.sin(a));   // 右巻き（下から上へ、上から見て左回り）
const P1 = [], P2 = [], PN1 = [], PN2 = [];
v.onFrame((t, dt) => {
  // 回転：ページの p と同じだけ回す（コピー中は正面で止める）
  const p = D.st().p; if (lastP === null) lastP = p; const dp = p - lastP; lastP = p;
  if (mode === 'helix') rot += dp;
  else { const goal = Math.round(rot / (2 * Math.PI)) * 2 * Math.PI; rot += (goal - rot) * Math.min(1, dt * 4); settle += dt; if (settle > 0.8) f = Math.min(1, f + dt / 9); }
  G.rotation.y = rot;
  const copy = mode === 'copy', key = mode + f.toFixed(4) + (v.cam.ph < 1.1);
  if (key === lastKey) return;   // 形が変わらないときは作り直さない（回転は G.rotation だけ）
  lastKey = key;
  P1.length = P2.length = PN1.length = PN2.length = 0;
  let firstNew = -1;
  pairs.forEach((q, i) => {
    const u = copy ? sm((f * (N + 8) - (N - 1 - i)) / 6) : 0;          // 上からほどける
    const s = copy ? clamp((u - 0.45) / 0.45, 0, 1) : 0;               // 新しいヌクレオチドがつく
    const a = i * TW, y = Y0 + i * RISE;
    const h1 = hp(i, a), h2 = hp(i, a + OFF);
    const l1 = new THREE.Vector3(-3.2, y, 0), l2 = new THREE.Vector3(3.2, y, 0), m1 = new THREE.Vector3(-1.2, y, 0), m2 = new THREE.Vector3(1.2, y, 0);
    q.o1.p.lerpVectors(h1, l1, u); q.o2.p.lerpVectors(h2, l2, u);
    q.n1.p.copy(m1).add(new THREE.Vector3(0, 0, 2.2 * (1 - s))); q.n2.p.copy(m2).add(new THREE.Vector3(0, 0, 2.2 * (1 - s)));
    const tg1 = new THREE.Vector3().lerpVectors(h2, m1, u), tg2 = new THREE.Vector3().lerpVectors(h1, m2, u);
    q.o1.ball.position.copy(q.o1.p); q.o2.ball.position.copy(q.o2.p);
    placePlate(q.o1, q.o1.p, tg1, 0.07, 1); placePlate(q.o2, q.o2.p, tg2, 0.07, 1);
    placeHB(q.hb, q.o1.p, q.o2.p, 0.07, u < 0.05);
    [q.n1, q.n2].forEach(n => { n.ball.visible = n.plate.visible = s > 0.01; n.ball.position.copy(n.p); n.ball.scale.setScalar(Math.max(0.01, s)); });
    if (s > 0.01) { placePlate(q.n1, q.n1.p, q.o1.p, 0.07, s); placePlate(q.n2, q.n2.p, q.o2.p, 0.07, s); if (firstNew < 0) firstNew = i; PN1.push(q.n1.p.clone()); PN2.push(q.n2.p.clone()); }
    placeHB(q.hb1, q.o1.p, q.n1.p, 0.07, s > 0.92); placeHB(q.hb2, q.n2.p, q.o2.p, 0.07, s > 0.92);
    P1.push(q.o1.p.clone()); P2.push(q.o2.p.clone());
  });
  setTube(t1, P1); setTube(t2, P2); setTube(tn1, PN1.reverse()); setTube(tn2, PN2.reverse());
  // 文字
  aBack.position.copy(P1[N - 2]).add(new THREE.Vector3(0, 0.35, 0));
  const iAT = 15, iGC = 6;   // ページの例と同じ並びのうち、見やすい段
  aAT.position.lerpVectors(P1[iAT], P2[iAT], 0.5).add(new THREE.Vector3(0, 0.2, 0)); aGC.position.lerpVectors(P1[iGC], P2[iGC], 0.5).add(new THREE.Vector3(0, 0.2, 0));
  lAT.show = lGC.show = !copy && v.cam.ph < 1.1; lBack.show = !copy;
  dims.forEach(d => { d.visible = !copy && v.cam.ph < 1.1; }); lDia.show = !copy && v.cam.ph < 1.1; lPitch.show = !copy && v.cam.ph < 1.1;
  const done = copy ? pairs.filter((q, i) => sm((f * (N + 8) - (N - 1 - i)) / 6) > 0.98).length : 0;
  lOld.show = copy && done > 2; lNew.show = copy && firstNew >= 0 && done > (SM ? 7 : 2); lFork.show = copy && done > 0 && done < N;
  if (copy) { const k = N - 1 - Math.min(N - 1, 2); aOld.position.copy(pairs[k].o1.p).add(new THREE.Vector3(0, 0.3, 0)); aNew.position.copy(pairs[SM ? k - 5 : k].n2.p).add(new THREE.Vector3(0, 0.3, 0));   // スマホは2つの文字が重ならないよう、少し下に
    const fi = clamp(N - 1 - done, 0, N - 1); aFork.position.set(0, Y0 + fi * RISE + 0.3, 0); }
  const chip = (b) => '<span style="display:inline-block;width:10px;height:10px;border-radius:2px;margin:0 2px 0 6px;background:#' + BC[b].toString(16).padStart(6, '0') + '"></span>' + b;
  hud.innerHTML = copy
    ? 'ほどけた塩基対：<b>' + done + '</b> / ' + N + (SM ? '' : '<br>AにはT、GにはCだけが組むので、同じ並びのDNAが2つできる<br><span style="font-size:11px;color:#94a3b8">ほどけた所は、はしごの形にのばして描いています（模式）</span>')
    : '回転スピード <b>' + ($('spd') ? $('spd').value : '') + '</b>' + (SM ? '' : '（上のスライダーと連動）') + '<br>' + chip('A') + chip('T') + chip('G') + chip('C')
      + (SM ? '' : '<br><span style="font-size:11px;color:#94a3b8">原子の細かい形は省いた模式です</span>');
});
