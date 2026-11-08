// 星の動き 3D（東京の星空。上の「日付」「時刻」「注目する星」と連動。東＝+x、北＝-z、上＝+y）
import { THREE, createView } from '../../assets/three/sim3d.js';
const $ = id => document.getElementById(id);
const H = window.__hoshi || {};
const ST = H.ST || [], CO = H.CO || [], LAT = H.LAT || 35.6581, LON = H.LON || 139.7414;
const R = 50, PI = Math.PI, DEG = PI / 180, EYE = 1.5;
const v = createView($('view3d'), {
  views: { south: { tgt: [0, EYE, 0], dist: 0.6, th: PI, ph: -0.45 }, north: { tgt: [0, EYE, 0], dist: 0.6, th: 0, ph: -0.45 }, east: { tgt: [0, EYE, 0], dist: 0.6, th: -PI / 2, ph: -0.4 }, west: { tgt: [0, EYE, 0], dist: 0.6, th: PI / 2, ph: -0.4 }, out: { tgt: [0, 0, 0], dist: 175, th: 0.7, ph: 0.3 } },
  camRow: '#camRow3d', bg: 0x070c1c, shadows: false, fov: 60, minDist: 0.3, maxDist: 400,
});
const { scene } = v;
v.hemi.intensity = 0.6;
const ground = new THREE.Mesh(new THREE.CircleGeometry(R, 96), new THREE.MeshStandardMaterial({ color: 0x1b2a1f, roughness: 1, side: THREE.DoubleSide })); ground.rotation.x = -PI / 2; scene.add(ground);
const ring = new THREE.Mesh(new THREE.TorusGeometry(R, 0.12, 6, 128), new THREE.MeshBasicMaterial({ color: 0x5b6b5f })); ring.rotation.x = PI / 2; scene.add(ring);
for (const [a, t] of [[0, '南'], [PI / 2, '東'], [PI, '北'], [-PI / 2, '西']]) v.label(t, [Math.sin(a) * R * 0.97, 1.5, Math.cos(a) * R * 0.97], { accent: true });
// 天球（外から見るときだけ見える網）と、北極星の向きの軸
const sphere = new THREE.LineSegments(new THREE.EdgesGeometry(new THREE.SphereGeometry(R, 24, 12), 1), new THREE.LineBasicMaterial({ color: 0x3a4f7a, transparent: true, opacity: 0.35 })); scene.add(sphere);
const poleDir = new THREE.Vector3(0, Math.sin(LAT * DEG), -Math.cos(LAT * DEG));
const axis = new THREE.Mesh(new THREE.CylinderGeometry(0.25, 0.25, R * 2.4, 8), new THREE.MeshBasicMaterial({ color: 0xfacc15, transparent: true, opacity: 0.55 }));
axis.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), poleDir); scene.add(axis);
const lAxis = v.label('天の北極（北極星のすぐ近く）', [poleDir.x * R * 1.15, poleDir.y * R * 1.15, poleDir.z * R * 1.15], { sub: true });
// 星
const COLS = { r: 0xffb08a, b: 0xbcd4ff, y: 0xfff1a8, w: 0xffffff };
function dirOf(ra, dec, lst) {
  const f = LAT * DEG, d = dec * DEG, h = (lst - ra) * DEG;
  const e = -Math.cos(d) * Math.sin(h), n = Math.sin(d) * Math.cos(f) - Math.cos(d) * Math.cos(h) * Math.sin(f), u = Math.sin(d) * Math.sin(f) + Math.cos(d) * Math.cos(h) * Math.cos(f);
  return new THREE.Vector3(e, u, -n);
}
const bins = [[-2, 0.5, 8], [0.5, 1.5, 6], [1.5, 2.5, 4.5], [2.5, 9, 3.2]].map(([a, b, size]) => {
  const idx = ST.map((s, i) => i).filter(i => ST[i][2] >= a && ST[i][2] < b);
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(new Float32Array(idx.length * 3), 3));
  g.setAttribute('color', new THREE.Float32BufferAttribute(idx.flatMap(i => new THREE.Color(COLS[ST[i][3]] || 0xffffff).toArray()), 3));
  const p = new THREE.Points(g, new THREE.PointsMaterial({ size, sizeAttenuation: false, vertexColors: true })); scene.add(p); return { idx, g };
});
const segs = []; CO.forEach(c => c[1].forEach(chain => { for (let k = 0; k + 1 < chain.length; k++) segs.push([chain[k], chain[k + 1]]); }));
const lineG = new THREE.BufferGeometry(); lineG.setAttribute('position', new THREE.Float32BufferAttribute(new Float32Array(segs.length * 6), 3));
scene.add(new THREE.LineSegments(lineG, new THREE.LineBasicMaterial({ color: 0x7aa2e8, transparent: true, opacity: 0.55 })));
const coLbl = CO.map(c => v.label(c[0], [0, 0, 0], { sub: true }));
// 注目する星と、その1日の道すじ
const mark = new THREE.Mesh(new THREE.SphereGeometry(0.9, 16, 12), new THREE.MeshBasicMaterial({ color: 0xfacc15 })); scene.add(mark);
let trail = new THREE.Line(new THREE.BufferGeometry(), new THREE.LineDashedMaterial({ color: 0xfacc15, dashSize: 1.2, gapSize: 0.8 })); scene.add(trail);
const lStar = v.label('', [0, 0, 0], { accent: true });
const JD0 = 2461041.5;   // 2026-01-01 0時（世界時）
let last = '';
v.onFrame(() => {
  const day = +$('day').value, hour = +$('hour').value, sel = +$('star').value, vw = document.querySelector('#camRow3d .on')?.dataset.v;
  const key = day + '/' + hour + '/' + sel + '/' + vw; if (key === last) return; last = key;
  const jd = JD0 + (day - 1) + (hour - 9) / 24, lst = ((280.46061837 + 360.98564736629 * (jd - 2451545) + LON) % 360 + 360) % 360;
  const P = ST.map(s => dirOf(s[0], s[1], lst).multiplyScalar(R * 0.995));
  bins.forEach(b => { const a = b.g.attributes.position.array; b.idx.forEach((i, k) => { a[k * 3] = P[i].x; a[k * 3 + 1] = P[i].y; a[k * 3 + 2] = P[i].z; }); b.g.attributes.position.needsUpdate = true; });
  const la = lineG.attributes.position.array; segs.forEach(([a, b], k) => { la.set([P[a].x, P[a].y, P[a].z, P[b].x, P[b].y, P[b].z], k * 6); }); lineG.attributes.position.needsUpdate = true;
  CO.forEach((c, k) => { const p = P[c[2]]; coLbl[k].at(p.x, p.y + 2, p.z); coLbl[k].show = p.y > 0 && vw !== 'out'; });
  const s = ST[sel]; if (s) {
    mark.position.copy(P[sel]); lStar.at(P[sel].x, P[sel].y + 3, P[sel].z); lStar.set((s[4] || '注目の星') + (P[sel].y < 0 ? '（地平線の下）' : ''));
    const pts = []; for (let i = 0; i <= 96; i++) pts.push(dirOf(s[0], s[1], lst + i * 3.75).multiplyScalar(R * 0.99));
    trail.geometry.dispose(); trail.geometry = new THREE.BufferGeometry().setFromPoints(pts); trail.computeLineDistances();
  }
  const inside = vw !== 'out'; sphere.visible = !inside; lAxis.show = !inside;
  const hh = Math.floor(hour), mm = Math.round((hour - hh) * 60);
  $('hud3d').innerHTML = (($('dayL') && $('dayL').textContent) || '') + ' <b>' + hh + ':' + String(mm).padStart(2, '0') + '</b><br><span style="font-size:11.5px">黄色の点線＝注目する星の1日の道すじ</span>';
});
$('hud3d').style.display = '';
