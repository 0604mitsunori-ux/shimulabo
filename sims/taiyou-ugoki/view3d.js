// 太陽の動き 3D（透明半球。上の「日付」「時刻」「場所」と連動。東＝+x、北＝-z、上＝+y）
import { THREE, createView, mat } from '../../assets/three/sim3d.js';
const $ = id => document.getElementById(id);
const R = 10, PI = Math.PI, DEG = PI / 180;
const LAT = { tokyo: 35.7, sapporo: 43.1, naha: 26.2, equator: 0, pole: 90 };
const v = createView($('view3d'), {
  views: { persp: { tgt: [0, 2.5, 0], dist: 34, th: 0.39, ph: 0.45 }, top: { tgt: [0, 0, 0], dist: 34, th: 0, ph: 1.45 }, east: { tgt: [0, 3, 0], dist: 32, th: PI / 2, ph: 0.08 } },
  camRow: '#camRow3d', bg: 0x9cc7e8, minDist: 8, maxDist: 90,
});
const { scene, sun } = v;
Object.assign(sun.shadow.camera, { left: -14, right: 14, top: 14, bottom: -14, near: 1, far: 120 }); sun.shadow.camera.updateProjectionMatrix();
const ground = new THREE.Mesh(new THREE.CircleGeometry(R, 96), mat(0xc5ccb6, { roughness: 1 })); ground.rotation.x = -PI / 2; ground.receiveShadow = true; scene.add(ground);
const outer = new THREE.Mesh(new THREE.RingGeometry(R, 60, 96), mat(0xb3bba3, { roughness: 1 })); outer.rotation.x = -PI / 2; outer.position.y = -0.01; outer.receiveShadow = true; scene.add(outer);
// 方位の線と文字
for (const [a, t] of [[0, '南'], [PI / 2, '東'], [PI, '北'], [-PI / 2, '西']]) {
  const ln = new THREE.Mesh(new THREE.BoxGeometry(0.04, 0.02, R), new THREE.MeshBasicMaterial({ color: 0x7d8590 })); ln.position.set(Math.sin(a) * R / 2, 0.02, Math.cos(a) * R / 2); ln.rotation.y = a; scene.add(ln);
  v.label(t, [Math.sin(a) * (R + 0.8), 0.2, Math.cos(a) * (R + 0.8)], { accent: t === '南' });
}
// 透明半球
const dome = new THREE.Mesh(new THREE.SphereGeometry(R, 64, 32, 0, 2 * PI, 0, PI / 2), new THREE.MeshStandardMaterial({ color: 0xffffff, transparent: true, opacity: 0.16, depthWrite: false, side: THREE.DoubleSide, roughness: 0.2 }));
scene.add(dome);
const domeLines = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.SphereGeometry(R * 1.001, 12, 6, 0, 2 * PI, 0, PI / 2), 1), new THREE.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.35 })); scene.add(domeLines);
// 中心の棒（影が地面に落ちる）
const stick = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 2.4, 12), mat(0x5b4a3a)); stick.position.y = 1.2; stick.castShadow = true; scene.add(stick);
const sunBall = new THREE.Mesh(new THREE.SphereGeometry(0.55, 24, 18), new THREE.MeshBasicMaterial({ color: 0xffb020 })); scene.add(sunBall);
const lSun = v.label('', [0, 0, 0], { accent: true });
function dirOf(lat, dec, H) {   // 方位ベクトル（東・上・南）
  const f = lat * DEG, d = dec * DEG, h = H * DEG;
  const e = -Math.cos(d) * Math.sin(h), n = Math.sin(d) * Math.cos(f) - Math.cos(d) * Math.cos(h) * Math.sin(f), u = Math.sin(d) * Math.sin(f) + Math.cos(d) * Math.cos(h) * Math.cos(f);
  return new THREE.Vector3(e, u, -n);
}
const decOf = day => {   // 太陽の赤緯（2026年・正午ごろ、黄経の近似式）
  const n = 9496.5 + (day - 1) + 0.125, g = (357.528 + 0.9856003 * n) * DEG, L = (280.46 + 0.9856474 * n) * DEG + (1.915 * Math.sin(g) + 0.02 * Math.sin(2 * g)) * DEG;
  return Math.asin(Math.sin(23.44 * DEG) * Math.sin(L)) / DEG; };
function path(lat, dec, color, dashed) {
  const pts = []; for (let i = 0; i <= 288; i++) { const p = dirOf(lat, dec, -180 + i * 1.25); if (p.y >= -0.005) pts.push(p.multiplyScalar(R * 1.002)); }
  const g = new THREE.BufferGeometry().setFromPoints(pts.length ? pts : [new THREE.Vector3()]);
  const l = new THREE.Line(g, dashed ? new THREE.LineDashedMaterial({ color, dashSize: 0.35, gapSize: 0.25 }) : new THREE.LineBasicMaterial({ color, linewidth: 2 }));
  if (dashed) l.computeLineDistances(); return l;
}
let grp = new THREE.Group(); scene.add(grp);
const hours = new THREE.Group(); scene.add(hours);
let last = '';
v.onFrame(() => {
  const day = +$('day').value, hour = +$('hour').value, loc = $('loc').value, lat = LAT[loc] ?? 35.7;
  const key = day + '/' + hour + '/' + loc; if (key === last) return; last = key;
  const dec = decOf(day);
  scene.remove(grp); grp = new THREE.Group(); scene.add(grp);
  grp.add(path(lat, 23.44, 0xff6b6b, true), path(lat, 0, 0xffffff, true), path(lat, -23.44, 0x6fa8ff, true));
  const main = path(lat, dec, 0xff8c00, false); main.material.linewidth = 3; grp.add(main);
  hours.clear();
  for (let h = 0; h < 24; h++) { const p = dirOf(lat, dec, (h - 12) * 15); if (p.y < 0) continue; const d = new THREE.Mesh(new THREE.SphereGeometry(0.11, 10, 8), new THREE.MeshBasicMaterial({ color: 0xffffff })); d.position.copy(p.multiplyScalar(R * 1.003)); hours.add(d); }
  const s = dirOf(lat, dec, (hour - 12) * 15), alt = Math.asin(Math.max(-1, Math.min(1, s.y))) / DEG;
  sunBall.position.copy(s).multiplyScalar(R * 1.01); sunBall.visible = alt > -1;
  sun.position.copy(s).multiplyScalar(50); sun.intensity = alt > 0 ? 1.3 : 0; v.hemi.intensity = alt > 0 ? 0.95 : 0.35;
  v.scene.background.set(alt > 6 ? 0x9cc7e8 : alt > -4 ? 0xe8b48a : 0x1a2440);
  lSun.at(sunBall.position.x, sunBall.position.y + 0.9, sunBall.position.z); lSun.set('太陽 ' + (alt > 0 ? '高さ' + alt.toFixed(1) + '°' : '地平線の下'));
  const noon = 90 - Math.abs(lat - dec);
  $('hud3d').innerHTML = '北緯' + lat + '° ・ 南中高度 <b>' + noon.toFixed(1) + '</b>°<br><span style="font-size:11.5px">赤の点線＝夏至・白＝春分秋分・青＝冬至</span>';
});
$('hud3d').style.display = '';
