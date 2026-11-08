// 金星の満ち欠け 3D（上の「日付」と連動。太陽を中心に、北極の上から見て反時計回り。大きさは誇張）
import { THREE, createView, mat, earthTexture, EARTH_ROT_Y } from '../../assets/three/sim3d.js';
const $ = id => document.getElementById(id);
const RE = 10, RV = 7.23, PI = Math.PI, DEG = PI / 180;
const v = createView($('view3d'), {
  views: { top: { tgt: [0, 0, 0], dist: 34, th: 0, ph: 1.45 }, side: { tgt: [0, 0, 0], dist: 36, th: 0.5, ph: 0.4 }, earth: { tgt: [0, 0, 0], dist: 5, th: 0, ph: 0 } },
  camRow: '#camRow3d', bg: 0x05080f, shadows: false, minDist: 1.5, maxDist: 120,
});
const { scene } = v;
v.hemi.intensity = 0.04; v.sun.intensity = 0;
const light = new THREE.PointLight(0xffffff, 3.2, 0, 0); scene.add(light);
{ const p = []; for (let i = 0; i < 1400; i++) { const u = new THREE.Vector3().randomDirection().multiplyScalar(300 + Math.random() * 100); p.push(u.x, u.y, u.z); }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(p, 3)); scene.add(new THREE.Points(g, new THREE.PointsMaterial({ color: 0xffffff, size: 1, sizeAttenuation: false }))); }
const sunBall = new THREE.Mesh(new THREE.SphereGeometry(1.6, 32, 24), new THREE.MeshBasicMaterial({ color: 0xffd23f })); scene.add(sunBall);
const ring = r => { const pts = []; for (let i = 0; i <= 128; i++) { const a = i / 128 * 2 * PI; pts.push(new THREE.Vector3(r * Math.cos(a), 0, -r * Math.sin(a))); } const l = new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), new THREE.LineDashedMaterial({ color: 0x8fa3bf, dashSize: 0.5, gapSize: 0.4 })); l.computeLineDistances(); scene.add(l); };
ring(RE); ring(RV);
const venus = new THREE.Mesh(new THREE.SphereGeometry(0.7, 48, 32), mat(0xf0dfb0, { roughness: 0.9 })); scene.add(venus);
const earth = new THREE.Mesh(new THREE.SphereGeometry(0.75, 48, 32), new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.9 })); earth.rotation.y = EARTH_ROT_Y; scene.add(earth);
earthTexture({ sea: '#2f6ea8', land: '#9cbf7a' }).then(t => { earth.material.map = t; earth.material.needsUpdate = true; });
const sight = new THREE.Line(new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(), new THREE.Vector3()]), new THREE.LineBasicMaterial({ color: 0xfacc15, transparent: true, opacity: 0.6 })); scene.add(sight);
v.label('太陽', [0, 2.4, 0]);
const lV = v.label('金星', [0, 0, 0], { accent: true }), lE = v.label('地球', [0, 0, 0]);
let last = '';
v.onFrame(() => {
  const s = window.__sim2d; if (!s) return;
  const vw = document.querySelector('#camRow3d .on')?.dataset.v, key = s.lv + '/' + s.le + '/' + vw;
  if (key === last) return; last = key;
  const pv = new THREE.Vector3(RV * Math.cos(s.lv * DEG), 0, -RV * Math.sin(s.lv * DEG)), pe = new THREE.Vector3(RE * Math.cos(s.le * DEG), 0, -RE * Math.sin(s.le * DEG));
  venus.position.copy(pv); earth.position.copy(pe);
  lV.at(pv.x, 1.2, pv.z); lE.at(pe.x, 1.3, pe.z);
  sight.geometry.setFromPoints([pe, pv]);
  const dist = pe.distanceTo(pv);
  if (vw === 'earth') { const u = pe.clone().sub(pv).normalize(); v.goal.tgt.copy(pv); v.goal.dist = Math.min(dist - 1.2, 4.5); v.goal.th = Math.atan2(u.x, u.z); v.goal.ph = 0.02; }
  const el = Math.acos(Math.max(-1, Math.min(1, pv.clone().sub(pe).normalize().dot(pe.clone().negate().normalize())))) / DEG;
  $('hud3d').innerHTML = '太陽と金星の離れ（離角）<b>' + el.toFixed(0) + '</b>°<br><span style="font-size:11.5px">地球〜金星 ' + (dist / RE).toFixed(2) + '天文単位（近いほど大きく見える）</span>';
});
$('hud3d').style.display = '';
