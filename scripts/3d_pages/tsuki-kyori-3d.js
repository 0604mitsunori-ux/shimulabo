import { THREE, createView, mat, earthTexture, EARTH_ROT_Y } from '../../assets/three/sim3d.js';
const $ = id => document.getElementById(id);
// 単位：地球の半径＝1（6,371km）
const KM = 1 / 6371, DM = 384400 * KM, RM = 1737.4 * KM;
const v = createView($('view'), {
  views: { all: { tgt: [DM / 2, 0, 0], dist: 95, th: 0.0, ph: 0.12 }, earth: { tgt: [0, 0, 0], dist: 7, th: 0.6, ph: 0.2 }, moon: { tgt: [DM, 0, 0], dist: 3, th: -0.6, ph: 0.2 } },
  camRow: '#camRow', bg: 0x04070d, shadows: false, minDist: 1.5, maxDist: 300,
});
const { scene, sun } = v;
v.hemi.intensity = 0.25; sun.intensity = 2.0; sun.position.set(-20, 10, 60);
{ const p = []; for (let i = 0; i < 1800; i++) { const u = new THREE.Vector3().randomDirection().multiplyScalar(800 + Math.random() * 300); p.push(u.x, u.y, u.z); }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(p, 3)); scene.add(new THREE.Points(g, new THREE.PointsMaterial({ color: 0xffffff, size: 1.1, sizeAttenuation: false }))); }
const earth = new THREE.Mesh(new THREE.SphereGeometry(1, 64, 48), new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.9, transparent: true }));
earth.rotation.y = EARTH_ROT_Y; scene.add(earth);
earthTexture({ sea: '#2f6ea8', land: '#9cbf7a' }).then(t => { earth.material.map = t; earth.material.needsUpdate = true; });
const moon = new THREE.Mesh(new THREE.SphereGeometry(RM, 48, 32), mat(0xbdbab2, { roughness: 1, transparent: true })); moon.position.x = DM; scene.add(moon);
v.label('地球（直径12,742km）', [0, 1.15, 0], { accent: true }); v.label('月（直径3,474km）', [DM, RM + 0.15, 0], { accent: true });
const distLbl = v.label('平均 約38万4,400km', [DM / 2, -7, 0]);
// 距離の線
const line = new THREE.Line(new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(0, -1.4 * 0 - 7, 0), new THREE.Vector3(DM, -7, 0)]), new THREE.LineDashedMaterial({ color: 0x8fa3bf, dashSize: 0.6, gapSize: 0.4 })); line.computeLineDistances(); scene.add(line);
// 並べる：地球30個
const earths = new THREE.InstancedMesh(new THREE.SphereGeometry(1, 24, 16), mat(0x5d8fc4, { roughness: 0.8 }), 30);
{ const m = new THREE.Matrix4(); for (let i = 0; i < 30; i++) { m.makeTranslation(2 + 2 * i + 1 - 1, 0, 0); earths.setMatrixAt(i, m); } } scene.add(earths);
const earthsLbl = v.label('地球が30個並ぶ', [31, 1.6, 0]);
// 並べる：惑星（地球の中心から順に、直径を足していく）
const PL = [['水星', 4879, 0x9c9a95], ['金星', 12104, 0xe0c89a], ['火星', 6779, 0xc46a43], ['木星', 139820, 0xd2b48c], ['土星', 116460, 0xe3d1a0], ['天王星', 50724, 0x9fd6dc], ['海王星', 49244, 0x4f78d6]];
const planets = new THREE.Group(); scene.add(planets); const plLbl = [];
{ let x = 0; PL.forEach(([n, d, c]) => { const r = d / 2 * KM; x += r; const s = new THREE.Mesh(new THREE.SphereGeometry(r, 48, 32), mat(c, { roughness: 0.8 })); s.position.x = x; planets.add(s);
  if (n === '土星') { const ring = new THREE.Mesh(new THREE.RingGeometry(r * 1.25, r * 2.2, 64), new THREE.MeshStandardMaterial({ color: 0xcdbb8c, side: THREE.DoubleSide, transparent: true, opacity: 0.7 })); ring.rotation.x = Math.PI / 2 - 0.45; ring.position.x = x; planets.add(ring); }
  plLbl.push(v.label(n, [x, r + 0.3, 0], { sub: n === '水星' || n === '火星' })); x += r; }); }
// 光の点
const photon = new THREE.Mesh(new THREE.SphereGeometry(0.25, 16, 12), new THREE.MeshBasicMaterial({ color: 0xfff3a0 })); scene.add(photon);
const glow = new THREE.PointLight(0xfff3a0, 3, 12); photon.add(glow);
let mode = 'none', lt = 0;
function setMode(m) {
  mode = m; earths.visible = m === 'earths'; earthsLbl.show = m === 'earths';
  planets.visible = m === 'planets'; plLbl.forEach(l => l.show = m === 'planets');
  photon.visible = m === 'light'; lt = 0;
  const dim = m === 'planets' ? 0.25 : 1; earth.material.opacity = dim; moon.material.opacity = dim;
  $('modes').querySelectorAll('button').forEach(b => b.classList.toggle('on', b.dataset.m === m));
  $('resNote').innerHTML = {
    none: '<strong>教科書の図より、ずっと遠い。</strong><br>地球の直径の約30倍も離れています。上のボタンで、地球や惑星を並べてみてください。',
    earths: '<strong>地球がちょうど30個ほど並ぶ距離。</strong><br>384,400km÷12,742km≒30.2個です。',
    planets: '<strong>7つの惑星の直径を足すと約38万km。</strong><br>地球の中心から月の中心まで（約38.4万km）の中に収まります。木星と土星だけで半分以上です。',
    light: '<strong>光でも約1.28秒。</strong><br>光の点は本当の速さで飛んでいます。月を見るとき、私たちは約1.3秒前の月の光を見ています。',
  }[m];
}
v.onFrame((t, dt) => {
  if (mode !== 'light') return;
  lt = (lt + dt) % 2.2; const k = Math.min(1, lt / 1.282);
  photon.position.set(k * DM, 0, 0); photon.visible = lt < 1.6;
  $('hud').style.display = ''; $('hud').innerHTML = '光が出てから <b>' + Math.min(lt, 1.282).toFixed(2) + '</b> 秒';
});
function update() {
  const cm = +$('ball').value; $('ballL').textContent = cm + ' cm';
  const dist = cm * 384400 / 12742 / 100, mcm = cm * 3474 / 12742;
  $('big').textContent = '30';
  $('sub').textContent = '中心どうしの平均距離 約384,400km ÷ 地球の直径 12,742km';
  $('sBall').textContent = '約 ' + (dist >= 10 ? Math.round(dist) : dist.toFixed(1)) + ' m 先（月は直径' + mcm.toFixed(1) + 'cm）';
  $('sLight').textContent = '約 1.28 秒';
  $('sCar').textContent = '約 160 日（休まず走って）';
  window.SHARE = '地球を直径' + cm + 'cmのボールにすると、月は約' + (dist >= 10 ? Math.round(dist) : dist.toFixed(1)) + 'm先🌕\n地球と月の本当の距離を3Dで見られる👇';
}
$('modes').addEventListener('click', e => { const b = e.target.closest('button'); if (b) setMode(b.dataset.m); });
$('ball').addEventListener('input', update);
$('hud').style.display = 'none';
setMode('none'); update();
