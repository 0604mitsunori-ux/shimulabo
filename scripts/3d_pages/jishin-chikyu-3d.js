import { THREE, createView, earthTexture, lonlat, EARTH_ROT_Y } from '../../assets/three/sim3d.js';
const $ = id => document.getElementById(id);
const R = 6, DEG = Math.PI / 180, RE = 6371;
const v = createView($('view'), {
  views: { japan: { tgt: [0, 0, 0], dist: 19, th: 142 * DEG, ph: 30 * DEG }, pacific: { tgt: [0, 0, 0], dist: 22, th: -170 * DEG, ph: -5 * DEG }, andes: { tgt: [0, 0, 0], dist: 16, th: -70 * DEG, ph: -20 * DEG } },
  camRow: '#camRow', bg: 0x05080f, shadows: false, occlude: 6, minDist: 7, maxDist: 60,
});
const { scene, sun } = v;
v.hemi.intensity = 0.9; sun.intensity = 0.8; sun.position.set(50, 40, 60);
const globe = new THREE.Mesh(new THREE.SphereGeometry(R, 96, 64), new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.95, transparent: true, opacity: 0.55, depthWrite: false, side: THREE.FrontSide }));
globe.rotation.y = EARTH_ROT_Y; globe.renderOrder = 2; scene.add(globe);
earthTexture({ sea: '#244d78', land: '#8fb36f', line: 'rgba(30,50,20,.7)' }).then(t => { globe.material.map = t; globe.material.needsUpdate = true; });
// 核（外核の境目 約2,900km）
const core = new THREE.Mesh(new THREE.SphereGeometry(R * (RE - 2900) / RE, 48, 32), new THREE.MeshBasicMaterial({ color: 0x7a3b1d, transparent: true, opacity: 0.25 })); scene.add(core);
// 深さ700kmの殻（地震が起きる限界の目安）
const shell = new THREE.Mesh(new THREE.SphereGeometry(R * (RE - 700) / RE, 64, 48), new THREE.MeshBasicMaterial({ color: 0x7fa6d6, wireframe: true, transparent: true, opacity: 0.06 })); scene.add(shell);
const grp = new THREE.Group(); scene.add(grp);
let DATA = [], period = 'month';
const colOf = d => { const c = new THREE.Color(); c.setHSL(Math.max(0, Math.min(0.66, d / 650 * 0.66)), 0.9, 0.55); return c; };
const lbls = [];
function draw() {
  grp.clear(); lbls.forEach(l => { l.show = false; l.el.remove(); }); lbls.length = 0;
  const ex = $('ex').checked ? 5 : 1;
  globe.material.opacity = $('clear').checked ? 0.25 : 0.55;
  shell.scale.setScalar((RE - 700 * ex) / (RE - 700));
  const geo = new THREE.SphereGeometry(1, 10, 8);
  const inst = new THREE.InstancedMesh(geo, new THREE.MeshBasicMaterial({ color: 0xffffff }), DATA.length);
  const m = new THREE.Matrix4(), q = new THREE.Quaternion();
  DATA.forEach((e, i) => {
    const r = R * Math.max(0.05, (RE - e.depth * ex) / RE), p = lonlat(e.lon, e.lat, r), s = 0.04 * Math.pow(1.5, e.mag - 4.5) + 0.045;
    m.compose(p, q, new THREE.Vector3(s, s, s)); inst.setMatrixAt(i, m); inst.setColorAt(i, colOf(e.depth));
  });
  inst.instanceMatrix.needsUpdate = true; if (inst.instanceColor) inst.instanceColor.needsUpdate = true;
  grp.add(inst);
  const top = DATA.slice().sort((a, b) => b.mag - a.mag).slice(0, 3);
  top.forEach(e => { const p = lonlat(e.lon, e.lat, R * Math.max(0.05, (RE - e.depth * ex) / RE)); lbls.push(v.label('M' + e.mag.toFixed(1), [p.x, p.y, p.z], { accent: true })); });
  // 結果
  const n = DATA.length;
  $('big').textContent = n.toLocaleString();
  $('sub').textContent = (period === 'week' ? 'この1週間' : 'この30日') + 'のマグニチュード4.5以上（USGS）';
  if (!n) return;
  const mx = top[0], dp = DATA.reduce((a, b) => b.depth > a.depth ? b : a);
  const jp = DATA.filter(e => e.lat > 20 && e.lat < 50 && e.lon > 120 && e.lon < 155);
  $('sMax').textContent = 'M' + mx.mag.toFixed(1) + '（' + mx.place + '）';
  $('sDeep').textContent = Math.round(dp.depth) + 'km（' + dp.place + '）';
  $('sJp').textContent = jp.length + ' 件';
  const deepJp = jp.filter(e => e.depth >= 300).length;
  $('resNote').innerHTML = '<strong>深さ300km以上の深い地震は ' + DATA.filter(e => e.depth >= 300).length + ' 件' + (deepJp ? '（うち日本の周り ' + deepJp + ' 件）' : '') + '。</strong><br>「日本」の視点で地球を少し回すと、日本海の下へ向かって震源が深くなっていく並びが見えます。沈み込む太平洋プレートに沿って起きている地震です。';
  $('hud').innerHTML = '<span style="font-size:11.5px">● 赤：浅い → 黄・緑 → 青：深い（700km）<br>茶色の球＝核（深さ約2,900kmより下）</span>';
  window.SHARE = (period === 'week' ? 'この1週間' : 'この30日') + '、世界でM4.5以上の地震は' + n + '件。最大はM' + mx.mag.toFixed(1) + '、最も深い震源は' + Math.round(dp.depth) + 'km🌐\n地球を透かして震源を3Dで見られる👇';
}
async function load() {
  $('sub').textContent = '読み込み中…';
  try {
    const j = await (await fetch('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_' + period + '.geojson')).json();
    DATA = j.features.map(f => ({ lon: f.geometry.coordinates[0], lat: f.geometry.coordinates[1], depth: Math.max(0, f.geometry.coordinates[2] || 0), mag: f.properties.mag || 4.5, place: (f.properties.place || '').replace(/^\d+ km [NSEW]+ of /, '') }));
  } catch (e) { DATA = []; $('sub').textContent = '⚠️ USGSのデータを取得できませんでした。時間をおいて再度お試しください。'; }
  draw();
}
$('period').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; period = b.dataset.p; $('period').querySelectorAll('button').forEach(x => x.classList.toggle('on', x === b)); load(); });
$('ex').addEventListener('change', draw); $('clear').addEventListener('change', draw);
load();
