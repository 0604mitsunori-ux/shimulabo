// ほねときん肉 3D（上の「うで」の図＝うでの曲げのばしを、立体の模型にする）
// 上の図の座標（px）を 1/20 にしてそのまま使う：図の右＝＋x（うでの内側）、図の上＝＋y、手前＝＋z。原点は上うでのまん中
// ひじの角度・ちぢむ/ゆるむ（cin）・おもり（wt）は上の図の値を読む。きん肉の太さと色は上の図（drawArm）の式と同じ
import { THREE, createView, mat } from '../../assets/three/sim3d.js';
const $ = id => document.getElementById(id);
const A = window.__hone;
const PI = Math.PI, K = 1 / 20;
const clamp = (x, a, b) => Math.max(a, Math.min(b, x));
const S2 = A ? A.S : { x: 150, y: 86 }, E2 = A ? A.E : { x: 150, y: 254 }, LF = A ? A.LF : 140;
const st = () => A ? A.st() : { mode: 'arm', ang: +$('ang').value, dir: 1, cin: 1, wt: false };
const OY = (S2.y + E2.y) / 2;
const P = (x, y, z) => new THREE.Vector3((x - S2.x) * K, (OY - y) * K, z || 0);   // 上の図の点（px）→ 3D
const Lc = (n, f, z) => new THREE.Vector3(n * K, -f * K, z || 0);                  // 前うでの中の点（n＝内側へ、f＝手先へ。px）
const SM = innerWidth < 520, m = SM ? 0.64 : 1;   // スマホは枠が正方形に近いので近づける

// 模型の大きさ：たて 約21（うでをのばしたとき）× よこ 約13（90°に曲げたとき）
const v = createView($('view3d'), {
  views: { persp: { tgt: [3.2, -3.6, 0], dist: 40 * m, th: 0.5, ph: 0.14 }, front: { tgt: [3.2, -3.6, 0], dist: 38 * m, th: 0, ph: 0 }, outer: { tgt: [2.4, -3.6, 0], dist: 38 * m, th: -1.1, ph: 0.12 },
    elbow: { tgt: [0.3, -4.2, 0], dist: SM ? 13 : 15, th: 0.55, ph: 0.12 } },   // ひじの関節（けんがほねにつく所）に近づく
  camRow: '#camRow3d', bg: 0xe9eef3, shadows: false, minDist: 10, maxDist: 90,
});
const { scene } = v;

// ---- 材料と道具 ----
const mBone = mat(0xece4cf, { roughness: 0.7 }), mTend = mat(0xfafaf9, { roughness: 0.6 }), mSkin = mat(0xfde4cc, { roughness: 0.8 });
const mI = mat(0xdc2626, { roughness: 0.55 }), mO = mat(0xfbb6c1, { roughness: 0.55 }), mIron = mat(0x475569, { roughness: 0.5, metalness: 0.3 });
const mJoint = new THREE.MeshBasicMaterial({ color: 0x16a34a, depthTest: false, transparent: true, opacity: 0.9 });
const sph = new THREE.SphereGeometry(1, 24, 16), cyl = new THREE.CylinderGeometry(1, 1, 1, 16);
// きん肉の形（上の図と同じ：まん中が太く、両はしが細い。半径＝1−y²、長さ2）
const spGeo = new THREE.SphereGeometry(1, 28, 20);
{ const p = spGeo.attributes.position, nr = spGeo.attributes.normal, q = new THREE.Vector3();
  for (let i = 0; i < p.count; i++) { const x = p.getX(i), y = p.getY(i), z = p.getZ(i), h = Math.hypot(x, z), k = Math.sqrt(Math.max(0, 1 - y * y));
    p.setXYZ(i, x * k, y, z * k); if (h > 1e-6) { q.set(x / h, 2 * y, z / h).normalize(); nr.setXYZ(i, q.x, q.y, q.z); } }
  p.needsUpdate = true; nr.needsUpdate = true; spGeo.computeBoundingSphere(); }
const UP = new THREE.Vector3(0, 1, 0), tv = new THREE.Vector3();
function rod(parent, r, mt) { const o = new THREE.Mesh(cyl, mt); o.userData.r = r; parent.add(o); return o; }
function setRod(o, a, b) { tv.subVectors(b, a); const L = tv.length() || 1e-6; o.position.addVectors(a, b).multiplyScalar(0.5); o.scale.set(o.userData.r, L, o.userData.r); o.quaternion.setFromUnitVectors(UP, tv.divideScalar(L)); return o; }
function ball(parent, p, r, mt) { const o = new THREE.Mesh(sph, mt); o.scale.setScalar(r); o.position.copy(p); parent.add(o); return o; }
function belly(o, a, b, hw) { tv.subVectors(b, a); const L = tv.length() || 1e-6; o.position.addVectors(a, b).multiplyScalar(0.5); o.scale.set(hw, L / 2, hw * 1.15); o.quaternion.setFromUnitVectors(UP, tv.divideScalar(L)); }

// ---- 動かない部分：かた側の付け根・上うでのほね ----
const root = new THREE.Group(); scene.add(root);
const S = P(S2.x, S2.y), E = P(E2.x, E2.y);
{ const sc = new THREE.Mesh(sph, mBone); sc.position.copy(P(S2.x - 26, S2.y - 4, -0.15)); sc.scale.set(0.75, 1.7, 0.3); sc.rotation.z = -0.16; root.add(sc); }
setRod(rod(root, 0.35, mBone), P(S2.x, S2.y + 2), P(E2.x, E2.y - 8)); ball(root, P(S2.x, S2.y + 2), 0.5, mBone); ball(root, P(E2.x, E2.y - 8), 0.5, mBone);
// 関節のしるし（緑の輪。上の図の点線の円と同じ大きさ）
const jointG = new THREE.Group(); root.add(jointG);   // 「関節さがし」の間は、こたえになるので見せない
{ const rE = new THREE.Mesh(new THREE.TorusGeometry(21 * K, 0.045, 8, 48), mJoint); rE.position.copy(E); rE.renderOrder = 5; jointG.add(rE);
  const rS = new THREE.Mesh(new THREE.TorusGeometry(17 * K, 0.045, 8, 40), mJoint); rS.position.copy(S); rS.renderOrder = 5; jointG.add(rS); }

// ---- 前うで（ひじを中心に回る）：ほね2本・ひじの後ろのほね・手・おもり ----
const fg = new THREE.Group(); fg.position.copy(E); root.add(fg);
for (const sg of [1, -1]) { const a = Lc(4.5 * sg, 10), b = Lc(5 * sg, LF - 2); setRod(rod(fg, 0.175, mBone), a, b); ball(fg, a, 0.25, mBone); ball(fg, b, 0.25, mBone); }
setRod(rod(fg, 0.2, mBone), Lc(-4.5, 10), Lc(-12, -5)); ball(fg, Lc(-12, -5), 0.27, mBone);   // 外側のきん肉のけんがつく所
{ const hand = new THREE.Mesh(sph, mSkin); hand.position.copy(Lc(0, LF + 30)); hand.scale.set(1.1, 1.5, 0.6); fg.add(hand);
  const th = new THREE.Mesh(sph, mSkin); th.position.copy(Lc(21, LF + 18)); th.scale.set(0.4, 0.65, 0.36); th.rotation.z = 0.5; fg.add(th); }
const db = new THREE.Group(); db.position.copy(Lc(0, LF + 30)); db.visible = false; fg.add(db);
{ const bar = new THREE.Mesh(cyl, mIron); bar.scale.set(0.2, 3.4, 0.2); bar.rotation.z = PI / 2; db.add(bar);
  for (const sg of [1, -1]) { const w = new THREE.Mesh(cyl, mIron); w.scale.set(0.6, 0.8, 0.6); w.rotation.z = PI / 2; w.position.x = 1.9 * sg; db.add(w); } }
const boneTag = new THREE.Object3D(); boneTag.position.copy(Lc(0, LF * 0.62, 0.4)); fg.add(boneTag);

// ---- きん肉とけん（内側＝うでの前がわ、外側＝うでの後ろがわ） ----
const Oi = P(S2.x + 16, S2.y + 20), Oo = P(S2.x - 17, S2.y + 20), Li0 = Oi.distanceTo(P(E2.x + 9, E2.y + 34));
const bI = new THREE.Mesh(spGeo, mI), bO = new THREE.Mesh(spGeo, mO); root.add(bI, bO);
const tI1 = rod(root, 0.11, mTend), tI2 = rod(root, 0.11, mTend), tO1 = rod(root, 0.11, mTend), tO2 = rod(root, 0.11, mTend);
setRod(rod(root, 0.11, mTend), P(S2.x + 6, S2.y + 8), Oi); setRod(rod(root, 0.11, mTend), P(S2.x - 6, S2.y + 8), Oo);   // 上のはしは、かたの近くのほねにつく
ball(root, Oi, 0.11, mTend); ball(root, Oo, 0.11, mTend);
const jI = ball(root, Oi, 0.15, mTend), jO = ball(root, Oo, 0.15, mTend), kO = ball(root, Oo, 0.11, mTend);   // けんがほねにつく所／外側のけんの曲がり目

// ---- ラベル（言葉は上の図と同じ） ----
const lI = v.label('', [0, 0, 0], { accent: true }), lO = v.label('', [0, 0, 0]);
v.label('ほね', [0, 0, 0], { obj: boneTag });
const lJ = v.label(SM ? '関節' : '関節（ひじ）', [-3.4, -4.9, 0], { sub: true });
const lT = SM ? null : v.label('けん', [0, 0, 0], { sub: true });

const PALE = [0xfb, 0xb6, 0xc1], RED = [0xdc, 0x26, 0x26];
const mixHex = t => { t = clamp(t, 0, 1); const c = i => Math.round(PALE[i] + (RED[i] - PALE[i]) * t); return (c(0) << 16) | (c(1) << 8) | c(2); };
const f = new THREE.Vector3(), n = new THREE.Vector3(), a = new THREE.Vector3(), b = new THREE.Vector3(), c = new THREE.Vector3(), d = new THREE.Vector3(), Ii = new THREE.Vector3(), Io = new THREE.Vector3(), Bo = new THREE.Vector3();
let last = '';
v.onFrame(() => {
  const s = st(), ang = clamp(+s.ang || 90, 45, 180), cin = clamp(+s.cin || 0, 0, 1), wt = !!s.wt;
  const key = ang.toFixed(2) + '|' + cin.toFixed(3) + '|' + wt + '|' + s.dir + '|' + s.mode;
  if (key === last) return; last = key;
  const p = (180 - ang) * PI / 180, gb = (180 - ang) / 135, on = cin > 0.5;
  fg.rotation.z = p; f.set(Math.sin(p), -Math.cos(p), 0); n.set(Math.cos(p), Math.sin(p), 0);   // f＝前うでの向き、n＝内側の向き
  db.visible = wt;
  const quiz = s.mode === 'quiz'; jointG.visible = !quiz; lJ.show = !quiz;
  // 内側のきん肉：かたの近く → ひじの関節をまたいで、前うでのほねへ
  Ii.copy(E).addScaledVector(f, 34 * K).addScaledVector(n, 9 * K);
  const hwI = 7 + 7 * cin + (1 - Oi.distanceTo(Ii) / Li0) * 9 + (wt ? 3 * cin : 0), hwO = 7 + 7 * (1 - cin) - gb * 2;
  d.subVectors(Ii, Oi).normalize();
  a.copy(Oi).addScaledVector(d, 10 * K); b.copy(Ii).addScaledVector(d, -12 * K);
  belly(bI, a, b, hwI * K);
  lI.at((a.x + b.x) / 2 + hwI * K + 3.4, (a.y + b.y) / 2, 0.6);
  c.copy(a).addScaledVector(d, 6 * K); setRod(tI1, Oi, c);
  c.copy(b).addScaledVector(d, -6 * K); setRod(tI2, c, Ii); jI.position.copy(Ii);
  if (lT) lT.at((b.x + Ii.x) / 2 + 1.2, (b.y + Ii.y) / 2 - 0.2, 0.5);
  // 外側のきん肉：かたの近く → けんがひじの後ろを回って、前うでのほね（ひじの後ろのほね）へ
  Bo.set(Oo.x, (OY - (E2.y - 30 + gb * 10)) * K, 0);
  a.set(Oo.x, Oo.y - 10 * K, 0);
  belly(bO, a, Bo, hwO * K);
  lO.at(Oo.x - hwO * K - 3.4, (a.y + Bo.y) / 2, 0.6);
  c.set(Oo.x, a.y - 6 * K, 0); setRod(tO1, Oo, c);
  Io.copy(E).addScaledVector(n, -12 * K).addScaledVector(f, -5 * K);
  setRod(tO2, Bo, Io); jO.position.copy(Io); kO.position.copy(Bo);
  // 色（ちぢむ＝赤、ゆるむ＝うすい色）
  mI.color.setHex(mixHex(cin)); mO.color.setHex(mixHex(1 - cin));
  const sI = on ? 'ちぢむ' : 'ゆるむ', sO = on ? 'ゆるむ' : 'ちぢむ', deg = Math.round(ang) + '°';
  lI.set((SM ? '内側' : '内側のきん肉') + '：' + sI); lI.el.classList.toggle('acc', on);
  lO.set((SM ? '外側' : '外側のきん肉') + '：' + sO); lO.el.classList.toggle('acc', !on);
  $('hud3d').innerHTML = SM
    ? 'ひじ <b style="font-size:13px">' + deg + '</b>・内側 <b style="font-size:13px">' + sI + '</b>・外側 <b style="font-size:13px">' + sO + '</b>'
    : (s.dir > 0 ? 'うでを曲げるとき' : 'うでをのばすとき') + '　ひじの角度 <b>' + deg + '</b><br>内側のきん肉 <b>' + sI + '</b>／外側のきん肉 <b>' + sO + '</b>' + (wt ? '<br><span style="font-size:11.5px">おもりを持っている</span>' : '');
});
$('hud3d').style.display = '';
if (SM) { const h = $('hud3d'); h.style.fontSize = '11px'; h.style.padding = '3px 6px'; h.style.left = h.style.top = '6px'; }
