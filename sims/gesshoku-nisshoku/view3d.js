// 月食・日食 3D（地球の半径＝1、太陽・地球・月の大きさと距離は実際の比率。上の「見るとき」「月齢（時間）」「通り道のずれ」「月までの距離」と連動）
import { THREE, createView, mat, earthTexture, EARTH_ROT_Y } from '../../assets/three/sim3d.js';
const $ = id => document.getElementById(id);
const RM = 1737.4 / 6378.14, DS = 149597870 / 6378.14, RS = 696000 / 6378.14, PI = Math.PI, DEG = PI / 180;
const DIST = { mean: 384400, near: 356500, far: 406700 }, NSPD = { mean: 0.5458, near: 0.5858, far: 0.5058 };   // 影に対する月の速さ（地球半径/時）
const v = createView($('view3d'), {
  views: { moon: { tgt: [60, 0, 0], dist: 3.2, th: -PI / 2, ph: 0.02 }, side: { tgt: [30, 0, 0], dist: 62, th: 0.02, ph: 0.3 }, earth: { tgt: [0, 0, 0], dist: 5, th: -PI / 2 + 0.4, ph: 0.15 } },
  camRow: '#camRow3d', bg: 0x05080f, shadows: false, minDist: 1.5, maxDist: 400, near: 0.05,
});
const { scene, sun } = v;
v.hemi.intensity = 0.04; sun.intensity = 2.3; sun.position.set(-500, 0, 0);
{ const p = []; for (let i = 0; i < 1400; i++) { const u = new THREE.Vector3().randomDirection().multiplyScalar(1500 + Math.random() * 300); p.push(u.x, u.y, u.z); }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(p, 3)); scene.add(new THREE.Points(g, new THREE.PointsMaterial({ color: 0xffffff, size: 1, sizeAttenuation: false }))); }
// 太陽は遠すぎるので、方向を示す光の球を置く（大きさは見かけの大きさに合わせる）
const sunBall = new THREE.Mesh(new THREE.SphereGeometry(RS * 1000 / DS, 32, 24), new THREE.MeshBasicMaterial({ color: 0xffd23f })); sunBall.position.set(-1000, 0, 0); scene.add(sunBall);
const earth = new THREE.Mesh(new THREE.SphereGeometry(1, 64, 48), new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.9 })); earth.rotation.y = EARTH_ROT_Y; scene.add(earth);
earthTexture({ sea: '#2f6ea8', land: '#9cbf7a' }).then(t => { earth.material.map = t; earth.material.needsUpdate = true; });
const moonMat = new THREE.MeshStandardMaterial({ color: 0xd8d4ca, roughness: 1, emissive: 0x000000 });
const moon = new THREE.Mesh(new THREE.SphereGeometry(RM, 48, 32), moonMat); scene.add(moon);
// 円すい（頂点の側を t=1）。r0＝根元の半径、len＝長さ
function cone(color, op) { const m = new THREE.Mesh(new THREE.ConeGeometry(1, 1, 64, 1, true), new THREE.MeshBasicMaterial({ color, transparent: true, opacity: op, depthWrite: false, side: THREE.DoubleSide })); scene.add(m); return m; }
const eUmbra = cone(0x6f8fc0, 0.38), ePen = cone(0x6f8fc0, 0.12), mUmbra = cone(0x6f8fc0, 0.45), mPen = cone(0x6f8fc0, 0.12);
function setCone(m, base, dir, r0, len, flare) {   // flare：半影は先へ行くほど広がる
  m.geometry.dispose();
  m.geometry = flare ? new THREE.CylinderGeometry(r0 + len * flare, r0, len, 64, 1, true) : new THREE.ConeGeometry(r0, len, 64, 1, true);
  m.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir);   // 円すいの頂点（+y）を dir の向きへ
  m.position.copy(base).addScaledVector(dir, len / 2);
}
const lMoon = v.label('月', [0, 0, 0], { accent: true }), lE = v.label('地球', [0, 1.3, 0]);
v.label('← 太陽の方向', [-6, 2, 0], { sub: true });
const lShadow = v.label('地球の本影', [30, 1.2, 0]);
let last = '';
v.onFrame(() => {
  const side = $('side').value, t = +$('t').value, beta = +$('beta').value, dk = $('dist').value || 'mean';
  const key = [side, t, beta, dk, document.querySelector('#camRow3d .on')?.dataset.v].join('/');
  if (key === last) return; last = key;
  const D = DIST[dk] / 6378.14, pi = Math.asin(6378.14 / DIST[dk]) / DEG, g = beta / pi, along = -NSPD[dk] * t;
  const sx = side === 'full' ? 1 : -1;
  moon.position.set(sx * Math.sqrt(Math.max(1, D * D - g * g - along * along)), g, along);
  lMoon.at(moon.position.x, moon.position.y + RM + 0.3, moon.position.z);
  // 地球の本影・半影（太陽と反対の +x 向き）
  const ex = new THREE.Vector3(1, 0, 0), Lu = DS / (RS - 1);
  setCone(eUmbra, new THREE.Vector3(0, 0, 0), ex, 1, Lu, 0);
  setCone(ePen, new THREE.Vector3(0, 0, 0), ex, 1, 80, (RS + 1) / DS);
  // 月の本影・半影（月から +x 向き）
  const mu = (DS - moon.position.x) * RM / (RS - RM);
  setCone(mUmbra, moon.position, ex, RM, mu, 0);
  setCone(mPen, moon.position, ex, RM, side === 'new' ? Math.abs(moon.position.x) + 4 : 20, (RS + RM) / DS);
  mUmbra.visible = mPen.visible = side === 'new'; eUmbra.visible = ePen.visible = side === 'full';
  lShadow.show = side === 'full';
  // 月食：月が本影に入っている割合で赤銅色に
  let note = '';
  if (side === 'full') {
    const x = moon.position.x, rU = 1 - x / Lu, rP = 1 + x * (RS + 1) / DS, dd = Math.hypot(moon.position.y, moon.position.z);
    const inU = Math.max(0, Math.min(1, (rU + RM - dd) / (2 * RM))), inP = Math.max(0, Math.min(1, (rP + RM - dd) / (2 * RM)));
    moonMat.color.setRGB(0.85 - 0.25 * inU - 0.1 * inP, 0.83 - 0.6 * inU - 0.12 * inP, 0.79 - 0.68 * inU - 0.12 * inP);
    moonMat.emissive.setRGB(0.25 * inU, 0.05 * inU, 0.02 * inU);
    note = inU >= 0.999 ? '本影の中（皆既）' : inU > 0 ? '本影に一部入っている' : inP > 0 ? '半影だけに入っている' : '影の外';
  } else {
    moonMat.color.setRGB(0.85, 0.83, 0.79); moonMat.emissive.setRGB(0, 0, 0);
    const reach = mu - Math.abs(moon.position.x) + 1;
    note = reach > 0 ? '月の本影が地球に届く長さ（皆既日食になりうる）' : '月の本影が地球まで届かない（金環日食になりうる）';
  }
  if (document.querySelector('#camRow3d .on')?.dataset.v === 'moon') { v.goal.tgt.copy(moon.position); v.goal.th = side === 'full' ? -PI / 2 : PI / 2; }
  $('hud3d').innerHTML = (side === 'full' ? '満月のころ' : '新月のころ') + '・月まで約' + Math.round(DIST[dk] / 1e4) + '万km<br><span style="font-size:11.5px">' + note + '</span>';
});
$('hud3d').style.display = '';
