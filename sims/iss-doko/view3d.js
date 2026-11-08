// ISSはいまどこ 3D（地球とISSの高さを同じ縮尺で。1 = 1,000km）
// 位置は公開API（wheretheiss.at）。前後45分の位置をまとめて取り、そのあいだは時刻に合わせて動かす。昼と夜の境目もAPIの太陽の位置から
import { THREE, createView, earthTexture, lonlat, EARTH_ROT_Y } from '../../assets/three/sim3d.js';
const $ = id => document.getElementById(id);
const I = window.__iss;
const RE = 6.371, API = 'https://api.wheretheiss.at/v1/satellites/25544';
const D2R = Math.PI / 180, clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const num = n => Math.round(n).toLocaleString('ja-JP');

const v = createView($('view3d'), {
  views: {
    whole: { tgt: [0, 0, 0], dist: 34, th: 137 * D2R, ph: 36 * D2R },
    iss: { tgt: [0, 0, 0], dist: 9, th: 137 * D2R, ph: 36 * D2R },
    japan: { tgt: [0, 0, 0], dist: 26, th: 137 * D2R, ph: 36 * D2R },
  },
  camRow: '#camRow3d', bg: 0x05060f, shadows: false, minDist: 7.2, maxDist: 90, occlude: RE,   // 地球の裏側の文字は隠す
});
const { scene } = v;
v.hemi.intensity = 0.28; v.sun.intensity = 2.2;

// ---- 星・地球・大気 ----
{ const n = 900, pos = new Float32Array(n * 3); for (let i = 0; i < n; i++) { const u = Math.random() * 2 - 1, a = Math.random() * Math.PI * 2, r = 400, c = Math.sqrt(1 - u * u); pos.set([r * c * Math.cos(a), r * u, r * c * Math.sin(a)], i * 3); }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  scene.add(new THREE.Points(g, new THREE.PointsMaterial({ color: 0xffffff, size: 1.2, sizeAttenuation: false, transparent: true, opacity: 0.55 }))); }
const globe = new THREE.Mesh(new THREE.SphereGeometry(RE, 96, 64), new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.9 }));
globe.rotation.y = EARTH_ROT_Y; scene.add(globe);
earthTexture({ sea: '#1f4f86', land: '#6f9a5a', line: 'rgba(20,40,20,.5)' }).then(t => { globe.material.map = t; globe.material.needsUpdate = true; });
scene.add(new THREE.Mesh(new THREE.SphereGeometry(RE * 1.015, 64, 40), new THREE.MeshBasicMaterial({ color: 0x60a5fa, transparent: true, opacity: 0.12, side: THREE.BackSide })));

// ---- ISS（大きさは誇張）・あなたの場所 ----
const iss = new THREE.Group(); scene.add(iss);
{ const body = new THREE.Mesh(new THREE.BoxGeometry(0.05, 0.05, 0.16), new THREE.MeshStandardMaterial({ color: 0xe5e7eb, roughness: 0.5 }));
  const panel = new THREE.MeshStandardMaterial({ color: 0x1e3a8a, roughness: 0.4, metalness: 0.3, side: THREE.DoubleSide });
  iss.add(body); for (const s of [-1, 1]) { const p = new THREE.Mesh(new THREE.BoxGeometry(0.2, 0.005, 0.07), panel); p.position.x = s * 0.13; iss.add(p); }
  iss.scale.setScalar(1.6); }
const gcv = document.createElement('canvas'); gcv.width = gcv.height = 64; { const g = gcv.getContext('2d'), gr = g.createRadialGradient(32, 32, 0, 32, 32, 32); gr.addColorStop(0, 'rgba(255,255,255,.95)'); gr.addColorStop(0.3, 'rgba(250,204,21,.6)'); gr.addColorStop(1, 'rgba(250,204,21,0)'); g.fillStyle = gr; g.fillRect(0, 0, 64, 64); }
const glow = new THREE.Sprite(new THREE.SpriteMaterial({ map: new THREE.CanvasTexture(gcv), depthWrite: false, transparent: true })); glow.scale.setScalar(0.6); scene.add(glow);
const pin = new THREE.Mesh(new THREE.ConeGeometry(0.07, 0.24, 12), new THREE.MeshBasicMaterial({ color: 0xef4444 })); scene.add(pin);
const lineM = new THREE.LineDashedMaterial({ color: 0xfbbf24, dashSize: 0.12, gapSize: 0.08 });
const link = new THREE.Line(new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(), new THREE.Vector3(0, 1, 0)]), lineM); scene.add(link);
const pathF = new THREE.Line(new THREE.BufferGeometry(), new THREE.LineBasicMaterial({ color: 0xfacc15 })); scene.add(pathF);
const pathP = new THREE.Line(new THREE.BufferGeometry(), new THREE.LineDashedMaterial({ color: 0x94a3b8, dashSize: 0.15, gapSize: 0.12 })); scene.add(pathP);

// ---- 文字 ----
const SM = v.mobile;
const lIss = v.label('ISS', [0, 0, 0], { accent: true }), lYou = v.label('', [0, 0, 0]), lDist = v.label('', [0, 0, 0], { sub: true });
const lF = v.label('これから45分の通り道', [0, 0, 0], { sub: true });
const hud = $('hud3d'); hud.style.display = '';
if (SM) { hud.style.fontSize = '11px'; hud.style.padding = '3px 6px'; hud.style.left = hud.style.top = '6px'; }
hud.textContent = 'ISSの位置を取得中…';

// ---- データ ----
let track = [], cur = null, lastFetch = -1e9, failed = false, aimed = false, view = 'whole', loading = false, lastDrag = -1e9;
v.el.addEventListener('pointerdown', () => { lastDrag = performance.now(); });
async function getJSON(u) { const r = await fetch(u); if (!r.ok) throw new Error(r.status); return r.json(); }
async function load() {
  if (loading) return; loading = true; lastFetch = performance.now(); failed = false;
  try {
    const now = Math.floor(Date.now() / 1000), ts = Array.from({ length: 20 }, (_, i) => now + (i - 9.5) * 300 | 0);   // 5分おき・前後約47分
    const [a, b] = await Promise.all([getJSON(API + '/positions?units=kilometers&timestamps=' + ts.slice(0, 10).join(',')), getJSON(API + '/positions?units=kilometers&timestamps=' + ts.slice(10).join(','))]);
    track = [...a, ...b].sort((x, y) => x.timestamp - y.timestamp);
    try { cur = await getJSON(API + '?units=kilometers'); } catch (e) { cur = null; }
    buildPath();
  } catch (e) { failed = true; lastFetch = performance.now() - 19 * 60 * 1000; }   // 失敗したら1分後にもう一度
  loading = false;
}
const posOf = (lat, lon, alt) => lonlat(lon, lat, (6371 + alt) / 1000);
function buildPath() {
  const now = Date.now() / 1000, past = [], fut = [];
  track.forEach(p => { const q = posOf(p.latitude, p.longitude, p.altitude); (p.timestamp <= now ? past : fut).push(q); });
  if (past.length) fut.unshift(past[past.length - 1].clone());
  const smooth = pts => pts.length > 1 ? new THREE.CatmullRomCurve3(pts).getPoints(pts.length * 12) : pts;
  pathF.geometry.dispose(); pathF.geometry = new THREE.BufferGeometry().setFromPoints(smooth(fut));
  pathP.geometry.dispose(); pathP.geometry = new THREE.BufferGeometry().setFromPoints(smooth(past)); pathP.computeLineDistances();
}
['calcBtn', 'reloadBtn'].forEach(id => { const b = $(id); if (b) b.addEventListener('click', () => { lastFetch = -1e9; }); });   // ページで「見る」「更新」を押したら3Dも取り直す
$('camRow3d').querySelectorAll('button').forEach(b => b.addEventListener('click', () => { view = b.dataset.v; }));

// 時刻に合わせて、前後の点のあいだを球面でなめらかにつなぐ
const A = new THREE.Vector3(), B = new THREE.Vector3(), P = new THREE.Vector3(), Q = new THREE.Quaternion(), Q0 = new THREE.Quaternion();
function issAt(t) {
  if (track.length < 2) return null;
  let k = track.findIndex(p => p.timestamp > t); if (k <= 0) k = k === 0 ? 1 : track.length - 1;
  const p0 = track[k - 1], p1 = track[k], u = clamp((t - p0.timestamp) / (p1.timestamp - p0.timestamp), 0, 1);
  A.copy(lonlat(p0.longitude, p0.latitude, 1)); B.copy(lonlat(p1.longitude, p1.latitude, 1));
  Q.setFromUnitVectors(A, B); Q0.identity().slerp(Q, u); P.copy(A).applyQuaternion(Q0);
  const alt = p0.altitude + (p1.altitude - p0.altitude) * u, vel = p0.velocity + (p1.velocity - p0.velocity) * u;
  const lat = Math.asin(clamp(P.y, -1, 1)) / D2R, lon = Math.atan2(P.x, P.z) / D2R;
  return { pos: P.clone().multiplyScalar((6371 + alt) / 1000), dir: P.clone(), lat, lon, alt, vel, vis: (u < 0.5 ? p0 : p1).visibility, sun: [(u < 0.5 ? p0 : p1).solar_lat, (u < 0.5 ? p0 : p1).solar_lon] };
}
function hav(la1, lo1, la2, lo2) { const a = Math.sin((la2 - la1) * D2R / 2) ** 2 + Math.cos(la1 * D2R) * Math.cos(la2 * D2R) * Math.sin((lo2 - lo1) * D2R / 2) ** 2; return 2 * 6371 * Math.asin(Math.sqrt(a)); }

v.onFrame(() => {
  if (performance.now() - lastFetch > 20 * 60 * 1000 || (track.length && Date.now() / 1000 > track[track.length - 3].timestamp)) load();   // 見えているときだけ取りに行く
  const pf = I.PREFS[+($('pref') ? $('pref').value : 12)] || I.PREFS[12];
  const you = lonlat(pf[2], pf[1], RE + 0.06); pin.position.copy(you); pin.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), you.clone().normalize());
  lYou.set((SM ? '' : 'あなた：') + pf[0].replace(/\(.*\)/, '')); lYou.at(you.x, you.y, you.z);
  const s = issAt(Date.now() / 1000);
  [iss, glow, link, pathF, pathP].forEach(o => { o.visible = !!s; }); lIss.show = !!s; lDist.show = !!s; lF.show = !!s;
  if (!s) { hud.textContent = failed ? 'ISSの位置を取得できませんでした。時間をおいて「いまの位置に更新」を押してください。' : 'ISSの位置を取得中…'; return; }
  iss.position.copy(s.pos); glow.position.copy(s.pos); iss.lookAt(0, 0, 0);
  if (s.sun[0] != null) v.sun.position.copy(lonlat(s.sun[1], s.sun[0], 60));
  const pa = link.geometry.attributes.position; pa.setXYZ(0, you.x, you.y, you.z); pa.setXYZ(1, s.pos.x, s.pos.y, s.pos.z); pa.needsUpdate = true; link.computeLineDistances(); link.geometry.computeBoundingSphere();
  const ground = hav(pf[1], pf[2], s.lat, s.lon), dist = Math.sqrt(ground * ground + s.alt * s.alt);
  lIss.set('ISS（高度' + num(s.alt) + 'km）'); lIss.at(s.pos.x, s.pos.y, s.pos.z);
  lDist.set('直線 約' + num(dist) + 'km'); const mid = you.clone().add(s.pos).multiplyScalar(0.5); lDist.at(mid.x, mid.y, mid.z);
  const fp = pathF.geometry.attributes.position; if (fp && fp.count > 10) { const j = Math.min(fp.count - 1, Math.floor(fp.count * 0.75)); lF.at(fp.getX(j), fp.getY(j), fp.getZ(j)); }
  // カメラ：はじめてデータが来たら ISS の上に向ける。「ISSのそばから」は ISS についていく
  const th = Math.atan2(s.dir.x, s.dir.z), ph = Math.asin(clamp(s.dir.y, -1, 1));
  if (!aimed) { aimed = true; for (const k of ['whole', 'iss']) { v.views[k].th = th; v.views[k].ph = ph; } if (view !== 'japan') v.setView(view); }
  if (view === 'iss') { v.goal.tgt.copy(s.pos);   // ISSについていく（さわってから4秒は向きを変えない）
    if (performance.now() - lastDrag > 4000) { let t2 = th; while (t2 - v.goal.th > Math.PI) t2 -= 2 * Math.PI; while (t2 - v.goal.th < -Math.PI) t2 += 2 * Math.PI; v.goal.th += (t2 - v.goal.th) * 0.02; v.goal.ph += (ph - v.goal.ph) * 0.02; } }
  else v.goal.tgt.set(0, 0, 0);
  const day = s.vis === 'daylight';
  hud.innerHTML = 'ISSの高度 <b>' + num(s.alt) + '</b> km' + (SM ? '' : '（地球の半径の約' + (s.alt / 6371 * 100).toFixed(1) + '%）') + '<br>時速 ' + num(s.vel) + ' km・いま' + (day ? '昼の側' : '夜の側') + (SM ? '' : '（' + (day ? '太陽の光が当たっている' : '地球の影の中') + '）')
    + '<br>' + pf[0].replace(/\(.*\)/, '') + 'から 直線 約' + num(dist) + 'km'
    + (SM ? '' : '<br><span style="font-size:11px;color:#94a3b8">地球とISSの高さは同じ縮尺・ISSの大きさは誇張・位置：wheretheiss.at</span>');
});
