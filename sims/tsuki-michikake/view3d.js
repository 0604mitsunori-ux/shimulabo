// 月の満ち欠け 3D（上の「月齢」「時刻」のスライダーと連動。大きさと距離は誇張）
import { THREE, createView, mat, earthTexture, lonlat, EARTH_ROT_Y } from '../../assets/three/sim3d.js';
const $ = id => document.getElementById(id);
const RE = 2, RM = 0.6, D = 14, PI = Math.PI;
const v = createView($('view3d'), {
  views: { top: { tgt: [5, 0, 0], dist: 40, th: 0, ph: 1.45 }, side: { tgt: [0, 0, 0], dist: 44, th: 0.5, ph: 0.35 }, earth: { tgt: [0, 0, 0], dist: 10, th: 0, ph: 0 } },
  camRow: '#camRow3d', bg: 0x05080f, shadows: false, minDist: 3, maxDist: 120,
});
const { scene, sun } = v;
v.hemi.intensity = 0.05; sun.intensity = 2.4; sun.position.set(100, 0, 0);
{ const p = []; for (let i = 0; i < 1400; i++) { const u = new THREE.Vector3().randomDirection().multiplyScalar(300 + Math.random() * 100); p.push(u.x, u.y, u.z); }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(p, 3)); scene.add(new THREE.Points(g, new THREE.PointsMaterial({ color: 0xffffff, size: 1, sizeAttenuation: false }))); }
// 太陽の光の向き（左から右へ流れる光の筋）
const sunBall = new THREE.Mesh(new THREE.SphereGeometry(3, 32, 24), new THREE.MeshBasicMaterial({ color: 0xffd23f })); sunBall.position.set(23, 0, 0); scene.add(sunBall);
for (let i = -3; i <= 3; i++) { const l = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 8, 6), new THREE.MeshBasicMaterial({ color: 0xffe08a, transparent: true, opacity: 0.35 })); l.rotation.z = PI / 2; l.position.set(16.5, 0, i * 2.2); scene.add(l); }
// 地球（日本の赤い点つき）。自転は「時刻」で決まる
const earthG = new THREE.Group(); scene.add(earthG);
const earth = new THREE.Mesh(new THREE.SphereGeometry(RE, 64, 48), new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.9 })); earth.rotation.y = EARTH_ROT_Y; earthG.add(earth);
earthTexture({ sea: '#2f6ea8', land: '#9cbf7a' }).then(t => { earth.material.map = t; earth.material.needsUpdate = true; });
const jp = new THREE.Mesh(new THREE.SphereGeometry(0.13, 12, 10), new THREE.MeshBasicMaterial({ color: 0xff3b30 })); jp.position.copy(lonlat(135, 35, RE * 1.02)); earthG.add(jp);
const jpObj = new THREE.Object3D(); jpObj.position.copy(lonlat(135, 35, RE * 1.05)); earthG.add(jpObj);
// 月と、月の通り道
const moon = new THREE.Mesh(new THREE.SphereGeometry(RM, 48, 32), mat(0xd8d4ca, { roughness: 1 })); scene.add(moon);
const orbit = []; for (let i = 0; i <= 128; i++) { const a = i / 128 * 2 * PI; orbit.push(new THREE.Vector3(D * Math.cos(a), 0, -D * Math.sin(a))); }
{ const ln = new THREE.Line(new THREE.BufferGeometry().setFromPoints(orbit), new THREE.LineDashedMaterial({ color: 0x8fa3bf, dashSize: 0.5, gapSize: 0.4 })); ln.computeLineDistances(); scene.add(ln); }
v.label('太陽', [23, 3.4, 0], { sub: true });
v.label('地球', [0, -RE - 0.2, RE + 0.6]);
const lMoon = v.label('月', [0, 0, 0], { accent: true });
v.label('日本', [0, 0, 0], { obj: jpObj, sub: true });
let last = '';
v.onFrame(() => {
  const age = +$('age').value, hour = +$('hour').value, key = age + '/' + hour + '/' + document.querySelector('#camRow3d .on')?.dataset.v;
  const a = age / 29.53 * 2 * PI;                       // 月：太陽の向きから反時計回り
  moon.position.set(D * Math.cos(a), 0, -D * Math.sin(a));
  lMoon.at(moon.position.x, RM + 0.5, moon.position.z);
  earthG.rotation.y = ((hour - 12) / 24 * 360 - 45) * PI / 180;   // 正午に日本が太陽を向く
  // 「地球から見る」：地球のそばから月を見る（光っている部分＝その日の月の形）
  if (document.querySelector('#camRow3d .on')?.dataset.v === 'earth') {
    const u = moon.position.clone().normalize().negate();
    v.goal.tgt.copy(moon.position); v.goal.dist = D - RE - 1.2; v.goal.th = Math.atan2(u.x, u.z); v.goal.ph = 0.03;
  }
  if (key !== last) {
    last = key;
    const nm = ($('sName') && $('sName').textContent) || '';
    $('hud3d').innerHTML = '月齢 <b>' + age.toFixed(1) + '</b> 日' + (nm && nm !== '—' ? '（' + nm + '）' : '') + '<br><span style="font-size:11.5px">「地球から見る」で、その日の月の形</span>';
  }
});
$('hud3d').style.display = '';
