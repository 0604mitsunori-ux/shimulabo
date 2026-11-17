// 歯車 3D（軸が平行な「平歯車」の模型。モジュール m＝0.25 … ピッチ円（かみ合いの基準の円）の直径＝m×歯数）
// 回転の角度は上の2Dと同じ a を使う：左（原動車）＝正面から見て時計回りに a、右（従動車）＝反対向きに a×左の歯数÷右の歯数
// 歯の形はインボリュート曲線（圧力角20°）。となり合うピッチ円が接する位置に置き、歯とすき間が向かい合うように位相を合わせているので、かみ合ったまま回る
// 「歯車3つ」は3Dだけの実験（まん中の歯車＝アイドラーは回る向きを変えるだけ）
import { THREE, createView } from '../../assets/three/sim3d.js';
const $ = id => document.getElementById(id);
const D = window.__gears;   // ページのJSに1行足して出している（回転の角度 a・一時停止）
const TAU = Math.PI * 2, M = 0.25, PA = 20 * Math.PI / 180, T = 0.8, BT = 0.04, BS = 0.03;
const C_L = 0x5eead4, C_R = 0xa78bfa, C_M = 0xfbbf24;   // 左・右は上の図と同じ色
const clamp = (x, a, b) => Math.max(a, Math.min(b, x)), frac = x => x - Math.floor(x);

const el = $('view3d');
const views = {
  persp: { tgt: [0, 0, T / 2], dist: 16, th: 0.55, ph: 0.3 },
  front: { tgt: [0, 0, T / 2], dist: 16, th: 0, ph: 0 },
  top: { tgt: [0, 0, T / 2], dist: 16, th: 0, ph: 1.3 },
  mesh: { tgt: [0, 0, T / 2], dist: 5.2, th: 0.42, ph: 0.3 },
};
const v = createView(el, { views, camRow: '#camRow3d', bg: 0x0b1020, shadows: true, minDist: 1.6, maxDist: 90, near: 0.1, far: 400 });
const SM = v.mobile;
v.hemi.intensity = 0.85; v.sun.intensity = 1.5;
v.sun.shadow.bias = -0.0006; v.sun.shadow.normalBias = 0.02;
const G = new THREE.Group(); v.scene.add(G);

// ---- 歯車の形（インボリュート歯形） ----
function gearGeo(z, off) {
  const rp = M * z / 2, rb = rp * Math.cos(PA), ra = rp + 0.92 * M, rf = rp - 1.2 * M, pitch = TAU / z;
  const inv = x => Math.tan(x) - x;
  const half = Math.PI / (2 * z) * 0.93;                                   // ピッチ円上の歯の厚みの半分（7%だけすき間をあける）
  const beta = r => half + inv(PA) - inv(Math.acos(Math.min(1, rb / r)));   // 半径 r での、歯の中心から歯面までの角度
  const r0 = Math.max(rb, rf + 0.04 * M);
  const bRoot = beta(r0) - (z < 17 ? 0.2 * half * (17 - z) / 9 : 0);       // 歯数が少ないときは歯の根もとを少し細く（模式）
  const NF = 5, pts = [];
  const P = (r, a) => pts.push(new THREE.Vector2(r * Math.cos(a), r * Math.sin(a)));
  for (let i = 0; i < z; i++) {
    const c = off + i * pitch;
    P(rf, c - bRoot);
    if (r0 > rf + 1e-6) P(r0, c - beta(r0));
    for (let k = 1; k <= NF; k++) { const r = r0 + (ra - r0) * k / NF; P(r, c - beta(r)); }
    P(ra, c);
    for (let k = NF; k >= 1; k--) { const r = r0 + (ra - r0) * k / NF; P(r, c + beta(r)); }
    if (r0 > rf + 1e-6) P(r0, c + beta(r0));
    P(rf, c + bRoot);
    P(rf, c + pitch / 2);
  }
  const shape = new THREE.Shape(pts);
  const rIn = 0.78, rOut = rf - 0.42;                                       // 大きい歯車は軽くする穴をあける（回っているのが分かりやすい）
  if (rOut - rIn > 0.62) {
    const nh = z >= 30 ? 6 : 5, rc = (rIn + rOut) / 2, rh = Math.min((rOut - rIn) / 2, rc * Math.sin(Math.PI / nh) * 0.74);
    for (let k = 0; k < nh; k++) { const a = (k + 0.5) * TAU / nh, h = new THREE.Path(); h.absarc(rc * Math.cos(a), rc * Math.sin(a), rh, 0, TAU, true); shape.holes.push(h); }
  }
  const geo = new THREE.ExtrudeGeometry(shape, { depth: T - 2 * BT, bevelEnabled: true, bevelThickness: BT, bevelSize: BS, bevelOffset: -BS, bevelSegments: 1, curveSegments: 14 });
  geo.translate(0, 0, BT);
  return { geo, rp, ra, rf };
}

// ---- 部品 ----
const stripeM = new THREE.MeshStandardMaterial({ color: 0x0b1020, roughness: 0.7 });
const steel = new THREE.MeshStandardMaterial({ color: 0xd5dbe3, roughness: 0.32, metalness: 0.35 });
function makeGear(color) {
  const g = new THREE.Group(); G.add(g);
  const body = new THREE.Mesh(new THREE.BufferGeometry(), new THREE.MeshStandardMaterial({ color, roughness: 0.45, metalness: 0.12 }));
  body.castShadow = body.receiveShadow = true; g.add(body);
  const stripe = new THREE.Mesh(new THREE.BoxGeometry(1, 0.1, 0.04), stripeM); g.add(stripe);   // 目印の線（上の図の黒い線と同じ向き）
  const boss = new THREE.Mesh(new THREE.CylinderGeometry(0.4, 0.4, 0.14, 28), new THREE.MeshStandardMaterial({ color: new THREE.Color(color).multiplyScalar(0.72), roughness: 0.5, metalness: 0.12 }));
  boss.rotation.x = Math.PI / 2; boss.position.z = T + 0.07; boss.castShadow = true; g.add(boss);
  return { g, body, stripe, z: 0, off: -1, rp: 0, ra: 0, rf: 0, x: 0, s: -1, c: 0 };
}
function makeShaft() {   // 軸と、台との間のつば
  const g = new THREE.Group(); G.add(g);
  const a = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.2, T + 0.75, 24), steel); a.rotation.x = Math.PI / 2; a.position.z = T / 2 + 0.075; a.castShadow = true; g.add(a);
  const c = new THREE.Mesh(new THREE.CylinderGeometry(0.32, 0.32, 0.3, 24), steel); c.rotation.x = Math.PI / 2; c.position.z = -0.15; g.add(c);
  return g;
}
const gL = makeGear(C_L), gR = makeGear(C_R), gM = makeGear(C_M);
const shL = makeShaft(), shR = makeShaft(), shM = makeShaft();
// 左（原動車）のハンドル（模式）。目印の線と同じ向きに付ける
const crank = new THREE.Group(); crank.position.z = T + 0.36; gL.g.add(crank);
const armM = new THREE.MeshStandardMaterial({ color: 0xe2e8f0, roughness: 0.4, metalness: 0.3 });
const arm = new THREE.Mesh(new THREE.BoxGeometry(1, 0.22, 0.12), armM); arm.castShadow = true; crank.add(arm);
const armHub = new THREE.Mesh(new THREE.CylinderGeometry(0.27, 0.27, 0.12, 24), armM); armHub.rotation.x = Math.PI / 2; crank.add(armHub);
const knob = new THREE.Mesh(new THREE.CylinderGeometry(0.15, 0.15, 0.62, 20), new THREE.MeshStandardMaterial({ color: 0xf97316, roughness: 0.5 })); knob.rotation.x = Math.PI / 2; knob.castShadow = true; crank.add(knob);
// 台（うしろの板と下の台）
const plate = new THREE.Mesh(new THREE.BoxGeometry(1, 1, 0.3), new THREE.MeshStandardMaterial({ color: 0x27344f, roughness: 0.9 })); plate.position.z = -0.45; plate.receiveShadow = true; G.add(plate);
const base = new THREE.Mesh(new THREE.BoxGeometry(1, 0.3, 2.4), new THREE.MeshStandardMaterial({ color: 0x1b2438, roughness: 0.9 })); base.receiveShadow = true; base.castShadow = true; G.add(base);

function setTeeth(o, z, off) {
  if (o.z === z && o.off === off) return;
  const r = gearGeo(z, off); o.body.geometry.dispose(); o.body.geometry = r.geo;
  o.z = z; o.off = off; o.rp = r.rp; o.ra = r.ra; o.rf = r.rf;
  const r0 = 0.4, r1 = Math.max(r0 + 0.2, off === 0 ? r.ra - 0.08 : r.rf - 0.06);   // 0°の向きに歯があるときは、その歯の先まで線を引く
  o.stripe.scale.x = r1 - r0; o.stripe.position.set((r0 + r1) / 2, 0, T + 0.012);
  if (o === gL) { const L = clamp(0.78 * r.rp, 0.72, 2.1); arm.scale.x = L; arm.position.x = L / 2; knob.position.set(L, 0, 0.37); }
}

// ---- 回る向きの矢印（歯車の上・手前に置く。回さない） ----
const AR = new THREE.Group(); G.add(AR);
const arM = new THREE.MeshBasicMaterial({ color: 0xfde047 });
function arrow(R, cw, s, x) {   // cw＝正面から見て時計回り
  const g = new THREE.Group(); g.position.set(x, 0, T + 0.25);
  const a0 = 62 * Math.PI / 180, a1 = 118 * Math.PI / 180, hl = 0.44 * s, hA = hl / R;
  const arc = new THREE.Mesh(new THREE.TorusGeometry(R, 0.055 * s, 8, 28, a1 - a0 - hA * 0.9), arM); arc.rotation.z = cw ? a0 + hA * 0.9 : a0; g.add(arc);
  const th = cw ? a0 + hA / 2 : a1 - hA / 2;
  const head = new THREE.Mesh(new THREE.ConeGeometry(0.17 * s, hl, 14), arM); head.position.set(R * Math.cos(th), R * Math.sin(th), 0); head.rotation.z = cw ? th + Math.PI : th; g.add(head);
  return g;
}

// ---- 文字 ----
const labL = v.label('', [0, 0, 0]), labR = v.label('', [0, 0, 0]), labM = v.label('', [0, 0, 0]);
const hud = $('hud3d'); hud.style.display = ''; hud.style.top = 'auto'; hud.style.bottom = '10px';   // 歯車の上の文字と重ならないよう、左下に置く
if (SM) { hud.style.fontSize = '11px'; hud.style.padding = '3px 6px'; hud.style.left = '6px'; hud.style.bottom = '6px'; hud.style.lineHeight = '1.45'; }
const B = (t) => '<b style="font-size:1.3em">' + t + '</b>';

// ---- 3Dの下のボタン（歯車の数・全画面） ----
const row = document.createElement('div'); row.className = 'pick-row'; row.style.margin = '8px 0 6px';
row.innerHTML = '<button type="button" data-n="2" class="on">歯車2つ（上の図と同じ）</button><button type="button" data-n="3">歯車3つにする（まん中にアイドラー）</button><button type="button" data-fs="1">⛶ 3Dを全画面（電子黒板用）</button>';
$('camRow3d').after(row);
const midBox = document.createElement('div'); midBox.style.cssText = 'display:none;margin:0 0 8px;';
midBox.innerHTML = '<div style="display:flex;justify-content:space-between;font-size:13px;font-weight:700;"><label for="g3dTm" style="margin:0;">まん中の歯数（3Dだけの実験）</label><span id="g3dTmL" style="font-weight:800;color:var(--teal-d);">18</span></div><input type="range" id="g3dTm" min="8" max="40" value="18" step="1" style="width:100%;" aria-label="まん中の歯車の歯数">';
row.after(midBox);
const tmIn = midBox.querySelector('#g3dTm'), tmL = midBox.querySelector('#g3dTmL');
tmIn.addEventListener('input', () => { tmL.textContent = tmIn.value; });
let mode3 = false, curView = 'persp';
row.querySelectorAll('button[data-n]').forEach(b => b.addEventListener('click', () => {
  mode3 = b.dataset.n === '3'; midBox.style.display = mode3 ? '' : 'none';
  row.querySelectorAll('button[data-n]').forEach(x => x.classList.toggle('on', x === b));
}));
document.querySelectorAll('#camRow3d button').forEach(b => b.addEventListener('click', () => { curView = b.dataset.v; }));
// 全画面（電子黒板用）。全画面の間は文字を大きくし、枠の中に「終わる」ボタンを出す
const fsBtn = row.querySelector('[data-fs]'), reqFs = el.requestFullscreen || el.webkitRequestFullscreen;
const exitBtn = document.createElement('button'); exitBtn.type = 'button'; exitBtn.textContent = '✕ 全画面を終わる';
exitBtn.style.cssText = 'display:none;position:absolute;right:8px;top:8px;padding:8px 12px;font-size:14px;font-weight:700;border:1px solid var(--line);border-radius:6px;background:#fff;color:var(--ink);cursor:pointer;';
el.appendChild(exitBtn);
const fsEl = () => document.fullscreenElement || document.webkitFullscreenElement;
const exitFs = () => { const f = document.exitFullscreen || document.webkitExitFullscreen; if (f && fsEl()) f.call(document); };
if (!reqFs) fsBtn.style.display = 'none';
else fsBtn.addEventListener('click', () => { if (fsEl()) exitFs(); else { try { const p = reqFs.call(el); if (p && p.catch) p.catch(() => {}); } catch (e) { /* 全画面にできない端末ではそのまま */ } } });
exitBtn.addEventListener('click', exitFs);
function onFs() {
  const fs = fsEl() === el;
  exitBtn.style.display = fs ? '' : 'none';
  hud.style.fontSize = fs ? '20px' : (SM ? '11px' : '');
  [labL, labR, labM].forEach(l => { l.el.style.fontSize = fs ? '18px' : ''; });
}
document.addEventListener('fullscreenchange', onFs); document.addEventListener('webkitfullscreenchange', onFs);

// ---- 並べ方（歯数が変わったときだけ作り直す） ----
let chain = [gL, gR], lay = { s: 1, raMax: 1 }, first = true;
function layout(t1, t2, tm) {
  setTeeth(gL, t1, 0);
  setTeeth(gR, t2, t2 % 2 ? Math.PI / t2 : 0);   // 上の図と同じ回転の式のまま歯がかみ合うよう、歯数が奇数のときは歯を半分ずらして作る
  if (mode3) setTeeth(gM, tm, 0);
  chain = mode3 ? [gL, gM, gR] : [gL, gR];
  gM.g.visible = shM.visible = mode3;
  // 中心の位置：となり合うピッチ円が接する
  const n = chain.length, xs = [0];
  for (let k = 1; k < n; k++) xs.push(xs[k - 1] + chain[k - 1].rp + chain[k].rp);
  const left = -chain[0].ra, right = xs[n - 1] + chain[n - 1].ra, mid = (left + right) / 2, W = right - left;
  const raMax = Math.max(...chain.map(o => o.ra)), s = clamp(W / 9.5, 0.75, 1.7);
  chain.forEach((o, k) => { o.x = xs[k] - mid; o.g.position.x = o.x; });
  shL.position.x = gL.x; shR.position.x = gR.x; shM.position.x = gM.x;
  // 位相：回る向きは1つごとに反対。q＝（歯の位置＋回転のずれ）を歯1つ分＝1 として数えたもの
  // 左の歯車の歯がまっすぐ右を向いたとき、右の歯車のすき間がまっすぐ左を向くようにする
  let q = 0; gL.s = -1; gL.c = 0;
  for (let k = 1; k < n; k++) {
    const o = chain[k]; o.s = -chain[k - 1].s;
    if (!mode3) o.c = -Math.PI / o.z;                                                // 上の図と同じ式
    else o.c = (frac(o.z / 2 - 0.5 - q) - o.off * o.z / TAU) * TAU / o.z;
    q = frac((o.off + o.c) * o.z / TAU);
  }
  // 台
  const mx = 0.7 + 0.2 * s, my = 0.5 + 0.45 * s;
  plate.scale.set(W + 2 * mx, 2 * (raMax + my), 1);
  base.scale.set(W + 2 * mx + 0.6, 1, 1); base.position.set(0, -(raMax + my) - 0.15, 0.3);
  // 矢印
  AR.children.slice().forEach(g => { g.children.forEach(m => m.geometry.dispose()); AR.remove(g); });
  chain.forEach(o => AR.add(arrow(o.ra + 0.3 * s, o.s < 0, s, o.x)));
  // 光と影の範囲
  const R = W / 2 + 3;
  v.sun.position.set(-0.35 * R - 4, 0.9 * R + 8, 1.2 * R + 10); v.sun.target.position.set(0, 0, 0);
  const sc = v.sun.shadow.camera; sc.left = -R; sc.right = R; sc.top = R; sc.bottom = -R; sc.near = 1; sc.far = 4 * R + 60; sc.updateProjectionMatrix();
  // カメラ（全体が入る距離）
  const Vh = raMax + 0.8 + 0.6 * s, D0 = Math.max(Vh * 1.06 / 0.3153, (W / 2 + mx + 0.3) * 1.05 / 0.5045);
  views.persp.dist = D0 * 1.1; views.front.dist = D0; views.top.dist = D0 * 0.95;
  views.mesh.tgt = [chain[0].x + chain[0].rp, 0, T / 2];
  v.goal.tgt.set(...views[curView].tgt); v.goal.dist = views[curView].dist;
  if (first) { v.cam.tgt.copy(v.goal.tgt); v.cam.dist = v.goal.dist; first = false; }
  lay = { s, raMax };
}

// ---- 毎フレーム ----
let lastKey = '', lastHud = '', lastLab = '';
v.onFrame(() => {
  const t1 = +$('t1').value || 24, t2 = +$('t2').value || 12, tm = +tmIn.value || 18;
  const key = (mode3 ? 3 : 2) + '|' + t1 + '|' + t2 + '|' + tm;
  if (key !== lastKey) { lastKey = key; lastLab = ''; layout(t1, t2, tm); }
  const st = D ? D.st() : { a: 0, paused: false }, a = st.a;
  for (const o of chain) o.g.rotation.z = o.s * a * t1 / o.z + o.c;   // 左：-a（時計回り）／右：+a×t1÷t2 − π÷t2（上の図と同じ）

  // 文字（真上から見るときは、歯車の奥に置く）
  const topish = v.cam.ph > 0.95, lk = key + topish;
  if (lk !== lastLab) {
    lastLab = lk;
    const at = (l, o) => { if (topish) l.at(o.x, o.ra * 0.2, -1.0 - 0.3 * lay.s); else l.at(o.x, o.ra + 0.3 * lay.s + 0.25, T); };
    at(labL, gL); at(labR, gR); at(labM, gM); labM.show = mode3;
    labL.set(SM ? '原動車 ' + t1 + '歯' : '原動車（左）' + t1 + '歯');
    labR.set(SM ? '従動車 ' + t2 + '歯' : '従動車（右）' + t2 + '歯');
    labM.set(SM ? 'まん中 ' + tm + '歯' : 'まん中（アイドラー）' + tm + '歯');
  }

  // 数字はページの表示をそのまま読む（上の図と必ず同じになる）
  const r = +$('rpm').value, rTxt = isFinite(r) ? String(r) : '—', r2 = ($('rpm2').textContent || '').replace(/\s*rpm$/, ''), ratio = $('ratio').textContent || '';
  const n1 = a / TAU, rev = z => (n1 * t1 / z).toFixed(1), pz = st.paused ? (SM ? '　⏸' : '　⏸ 一時停止中') : '';
  let h;
  if (!mode3) {
    h = SM
      ? '左' + B(t1) + '歯 ' + rTxt + 'rpm → 右' + B(t2) + '歯 ' + B(r2) + 'rpm<br>左' + rev(t1) + '回転・右' + rev(t2) + '回転' + pz
      : '原動車（左）' + B(t1) + '歯・' + rTxt + ' rpm　→　従動車（右）' + B(t2) + '歯・' + B(r2) + ' rpm<br>速度伝達比 ' + ratio + '　回る向き：左と右は反対<br>回転カウンター　左 ' + rev(t1) + '回転／右 ' + rev(t2) + '回転' + pz;
  } else {
    h = SM
      ? '左' + t1 + '→中' + tm + '→右' + t2 + '歯　右 ' + B(r2) + 'rpm<br>右は左と同じ向き（中は反対）' + pz
      : '歯車3つ（3Dだけの実験）　左 ' + B(t1) + '歯 → まん中 ' + B(tm) + '歯 → 右 ' + B(t2) + '歯<br>右の回転数 ' + B(r2) + ' rpm（歯車2つのときと同じ）・右は左と同じ向きに回る<br>回転カウンター　左 ' + rev(t1) + '／まん中 ' + rev(tm) + '／右 ' + rev(t2) + ' 回転' + pz;
  }
  if (h !== lastHud) { lastHud = h; hud.innerHTML = h; }
});
window.__g3d = { gears: () => chain.map(o => ({ z: o.z, rot: o.g.rotation.z, x: o.x, s: o.s, c: o.c, off: o.off })) };   // 確かめるとき用
