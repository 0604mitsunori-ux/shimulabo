import { THREE, createView, earthTexture, lonlat, EARTH_ROT_Y } from '../../assets/three/sim3d.js';
const $ = id => document.getElementById(id);
const R = 5, DEG = Math.PI / 180;
const v = createView($('view'), {
  views: { sun: { tgt: [0, 0, 0], dist: 24, th: 0, ph: 0 }, japan: { tgt: [0, 0, 0], dist: 20, th: 139.7 * DEG, ph: 35.7 * DEG }, north: { tgt: [0, 0, 0], dist: 22, th: 139.7 * DEG, ph: 1.45 } },
  camRow: '#camRow', bg: 0x05080f, shadows: false, occlude: 5, minDist: 8, maxDist: 60,
});
const { scene, sun } = v;
v.hemi.intensity = 0.06; sun.intensity = 2.2;
// 星
{ const p = []; for (let i = 0; i < 1500; i++) { const u = new THREE.Vector3().randomDirection().multiplyScalar(300 + Math.random() * 200); p.push(u.x, u.y, u.z); }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(p, 3)); scene.add(new THREE.Points(g, new THREE.PointsMaterial({ color: 0xffffff, size: 1.1, sizeAttenuation: false }))); }
const globe = new THREE.Mesh(new THREE.SphereGeometry(R, 96, 64), new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.9 }));
globe.rotation.y = EARTH_ROT_Y; scene.add(globe);
earthTexture({ sea: '#2f6ea8', land: '#9cbf7a', line: 'rgba(40,60,30,.6)' }).then(t => { globe.material.map = t; globe.material.needsUpdate = true; });
// 夜の側に薄い青の明かり（真っ暗で形が消えないように）
const night = new THREE.Mesh(new THREE.SphereGeometry(R * 1.002, 64, 48), new THREE.MeshBasicMaterial({ color: 0x0a1630, transparent: true, opacity: 0.0 })); scene.add(night);
const atmo = new THREE.Mesh(new THREE.SphereGeometry(R * 1.04, 64, 48), new THREE.MeshBasicMaterial({ color: 0x6fb6ff, transparent: true, opacity: 0.08, side: THREE.BackSide })); scene.add(atmo);
// 太陽の直下点のしるしと、境目の輪
const sunDot = new THREE.Mesh(new THREE.SphereGeometry(0.16, 16, 12), new THREE.MeshBasicMaterial({ color: 0xffd23f })); scene.add(sunDot);
const ringPts = []; for (let i = 0; i <= 128; i++) { const a = i / 128 * Math.PI * 2; ringPts.push(new THREE.Vector3(Math.cos(a), 0, Math.sin(a)).multiplyScalar(R * 1.006)); }
const term = new THREE.Line(new THREE.BufferGeometry().setFromPoints(ringPts), new THREE.LineBasicMaterial({ color: 0xffb347 })); scene.add(term);
// 地軸
const axis = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, R * 2.6, 8), new THREE.MeshBasicMaterial({ color: 0xbfc8d6 })); scene.add(axis);
const CITIES = [['東京', 139.69, 35.69, 9], ['ロンドン', -0.13, 51.51, 0], ['ニューヨーク', -74.0, 40.71, -5], ['シドニー', 151.21, -33.87, 10], ['北極', 0, 89.5, null], ['南極', 0, -89.5, null]];
const cityLbl = CITIES.map(([n, lo, la]) => { const p = lonlat(lo, la, R * 1.01); const d = new THREE.Mesh(new THREE.SphereGeometry(0.07, 10, 8), new THREE.MeshBasicMaterial({ color: 0xffffff })); d.position.copy(p); scene.add(d); return v.label(n, [p.x, p.y, p.z], { sub: n === 'ロンドン' || n === 'シドニー' }); });

const MD = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
const doyStr = d => { let m = 0; while (d >= MD[m]) { d -= MD[m]; m++; } return (m + 1) + '月' + (d + 1) + '日'; };
const hm = h => { const m = Math.round(h * 60) % 1440; return Math.floor(m / 60) + ':' + String(m % 60).padStart(2, '0'); };
const DAYS = [['春分', 78], ['夏至', 171], ['秋分', 265], ['冬至', 355]];
$('days').innerHTML = DAYS.map(([n, d]) => '<button data-d="' + d + '">' + n + '（' + doyStr(d) + '）</button>').join('');
function setNow() { const n = new Date(), j = new Date(n.getTime() + 9 * 3600e3); const y0 = Date.UTC(j.getUTCFullYear(), 0, 1); $('doy').value = Math.min(364, Math.floor((j.getTime() - y0) / 864e5)); $('hr').value = Math.round((j.getUTCHours() + j.getUTCMinutes() / 60) * 4) / 4; }
function alt(lon, lat, sLon, dec) { const H = (lon - sLon) * DEG; return Math.asin(Math.sin(lat * DEG) * Math.sin(dec * DEG) + Math.cos(lat * DEG) * Math.cos(dec * DEG) * Math.cos(H)) / DEG; }
let hrF = 0;
function update() {
  const N = +$('doy').value, jst = +$('hr').value + hrF;
  const dec = -23.44 * Math.cos(2 * Math.PI * (N + 10) / 365);
  let sLon = -15 * ((jst - 9) - 12); sLon = ((sLon + 540) % 360) - 180;
  const sd = lonlat(sLon, dec, 1);
  sun.position.copy(sd).multiplyScalar(100); sun.target.position.set(0, 0, 0);
  sunDot.position.copy(sd).multiplyScalar(R * 1.01);
  term.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), sd);
  v.views.sun.th = sLon * DEG; v.views.sun.ph = dec * DEG;
  $('doyL').textContent = doyStr(N); $('hrL').textContent = hm(jst);
  const res = CITIES.map(([n, lo, la, tz], i) => { const a = alt(lo, la, sLon, dec); cityLbl[i].set(n + (a > -0.83 ? ' ☀️' : ' 🌙') + (tz != null ? ' ' + hm(((jst - 9 + tz) % 24 + 24) % 24) : '')); return a; });
  const tA = res[0];
  $('big').textContent = tA.toFixed(1);
  $('sub').textContent = doyStr(N) + ' ' + hm(jst) + '（日本時間）の東京';
  $('sTokyo').textContent = tA > -0.83 ? '昼（太陽が出ている）' : '夜（太陽が沈んでいる）';
  $('sDecl').textContent = (dec >= 0 ? '北緯 ' : '南緯 ') + Math.abs(dec).toFixed(1) + '°';
  $('sPolar').textContent = Math.abs(dec) < 1 ? 'どちらの極もなし' : dec > 0 ? '北極圏で白夜・南極圏で極夜' : '北極圏で極夜・南極圏で白夜';
  $('hud').innerHTML = doyStr(N) + ' <b>' + hm(jst) + '</b><br><span style="font-size:11.5px">黄色の点＝太陽が真上</span>';
  $('resNote').innerHTML = tA > 60 ? '<strong>東京の太陽はとても高い位置に。</strong><br>夏至のころの正午は、東京でも太陽の高さが約78°になります。'
    : tA > -0.83 ? '<strong>東京は昼。太陽の高さは' + tA.toFixed(1) + '°。</strong><br>「時間を進める」を押すと、昼と夜の境目（オレンジの線）が西へ動いていきます。'
    : '<strong>東京は夜。</strong><br>地球の反対側、ロンドンやニューヨークの昼と夜も、地球儀のラベルで確かめてみてください。';
  window.SHARE = doyStr(N) + ' ' + hm(jst) + '、東京の太陽の高さは' + tA.toFixed(1) + '°🌍\n地球のどこが昼でどこが夜か、3Dの地球儀で見られる👇';
}
let playing = false;
$('playBtn').onclick = () => { playing = !playing; $('playBtn').textContent = playing ? '❚❚ 止める' : '▶ 時間を進める'; };
$('nowBtn').onclick = () => { setNow(); hrF = 0; update(); };
v.onFrame((t, dt) => {
  if (!playing) return;
  let h = +$('hr').value + dt * 2.4; let d = +$('doy').value;
  if (h >= 24) { h -= 24; d = (d + 1) % 365; $('doy').value = d; }
  $('hr').value = h; hrF = h - +$('hr').value; update();
});
$('doy').addEventListener('input', update); $('hr').addEventListener('input', () => { hrF = 0; update(); });
$('days').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; $('doy').value = b.dataset.d; update(); });
setNow(); update(); v.setView("sun", true);
