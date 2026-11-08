// 太陽系 3D（上の図と同じ8つの惑星を、同じ角度・同じ速さ（実際の公転周期の比）で回す）
// 上が北。北の上から見て反時計回り（実際の回る向き）。距離は「上の図と同じ（圧縮）」と「本当の距離の比率」を切りかえ。大きさは誇張
import { THREE, createView } from '../../assets/three/sim3d.js';
const $ = id => document.getElementById(id);
const S = window.__solar;
const NAME = ['水星', '金星', '地球', '火星', '木星', '土星', '天王星', '海王星'];
const AU = [0.39, 0.72, 1.00, 1.52, 5.20, 9.54, 19.2, 30.1];          // ページの表（天文単位）
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));

const v = createView($('view3d'), {
  views: {
    persp: { tgt: [0, 0, 0], dist: 74, th: 0.5, ph: 0.55 },
    top: { tgt: [0, 0, 0], dist: 88, th: 0, ph: 1.45 },
    side: { tgt: [0, 0, 0], dist: 74, th: 0.3, ph: 0.06 },
  },
  camRow: '#camRow3d', bg: 0x05060f, shadows: false, minDist: 6, maxDist: 200,
});
const { scene } = v;
v.hemi.intensity = 0.35; v.sun.intensity = 0;
const light = new THREE.PointLight(0xfff4d6, 3.2, 0, 0); scene.add(light);

// ---- 星（背景） ----
{ const n = 900, pos = new Float32Array(n * 3); for (let i = 0; i < n; i++) { const u = Math.random() * 2 - 1, a = Math.random() * Math.PI * 2, r = 400, c = Math.sqrt(1 - u * u); pos.set([r * c * Math.cos(a), r * u, r * c * Math.sin(a)], i * 3); }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  scene.add(new THREE.Points(g, new THREE.PointsMaterial({ color: 0xffffff, size: 1.2, sizeAttenuation: false, transparent: true, opacity: 0.6 }))); }

// ---- 太陽 ----
const sun = new THREE.Mesh(new THREE.SphereGeometry(1, 40, 24), new THREE.MeshBasicMaterial({ color: 0xffd36b })); scene.add(sun);
const gcv = document.createElement('canvas'); gcv.width = gcv.height = 128; { const g = gcv.getContext('2d'), gr = g.createRadialGradient(64, 64, 0, 64, 64, 64); gr.addColorStop(0, 'rgba(255,240,170,.9)'); gr.addColorStop(0.35, 'rgba(251,191,36,.35)'); gr.addColorStop(1, 'rgba(251,146,60,0)'); g.fillStyle = gr; g.fillRect(0, 0, 128, 128); }
const glow = new THREE.Sprite(new THREE.SpriteMaterial({ map: new THREE.CanvasTexture(gcv), depthWrite: false, transparent: true })); scene.add(glow);

// ---- 惑星・軌道 ----
const planets = S.P.map((p, i) => {
  const m = new THREE.Mesh(new THREE.SphereGeometry(1, 32, 20), new THREE.MeshStandardMaterial({ color: p[2], roughness: 0.8 })); scene.add(m);
  let ring = null;
  if (i === 5) { ring = new THREE.Mesh(new THREE.RingGeometry(1.35, 2.25, 64), new THREE.MeshBasicMaterial({ color: 0xd9c08a, side: THREE.DoubleSide, transparent: true, opacity: 0.75 })); ring.rotation.x = -Math.PI / 2 + 0.47; m.add(ring); }   // 土星の輪（傾き約27°）
  const pts = []; for (let k = 0; k <= 128; k++) { const a = k / 128 * Math.PI * 2; pts.push(new THREE.Vector3(Math.cos(a), 0, -Math.sin(a))); }
  const orbit = new THREE.LineLoop(new THREE.BufferGeometry().setFromPoints(pts), new THREE.LineBasicMaterial({ color: i === 2 ? 0x60a5fa : 0xffffff, transparent: true, opacity: i === 2 ? 0.55 : 0.18 })); scene.add(orbit);
  const lbl = v.label(NAME[i], [0, 0, 0], { sub: i === 0 || i === 1 || i === 3 });
  return { m, orbit, lbl, p, sub: i === 0 || i === 1 || i === 3 };
});

// ---- 距離の切りかえ（3Dの下にボタン） ----
const row = document.createElement('div'); row.className = 'pick-row'; row.style.marginTop = '8px';
row.innerHTML = '<button data-m="page" class="on">見やすい距離（上の図と同じ）</button><button data-m="real">本当の距離の比率</button>';
$('camRow3d').after(row);
let mode = 'page', k = 0;
row.querySelectorAll('button').forEach(b => b.addEventListener('click', () => { mode = b.dataset.m; row.querySelectorAll('button').forEach(x => x.classList.toggle('on', x === b)); }));

const hud = $('hud3d'); hud.style.display = '';
const SM = v.mobile; if (SM) { hud.style.fontSize = '11px'; hud.style.padding = '3px 6px'; hud.style.left = hud.style.top = '6px'; }
const PRI = [2, 4, 5, 7, 6, 3, 1, 0];   // 名前を残す順
let a0 = null;
v.onFrame((t, dt) => {
  const s = S.st(); k += ((mode === 'real' ? 1 : 0) - k) * Math.min(1, dt * 3);
  const sunR = 1.5 * (1 - k) + 0.18 * k; sun.scale.setScalar(sunR); glow.scale.setScalar(sunR * (5 - 2 * k));
  const showOrbit = !$('orbit') || +$('orbit').value > 0;
  planets.forEach((q, i) => {
    const r = (q.p[0] / 10) * (1 - k) + AU[i] * 26 / 30.1 * k, a = s.ang[i], size = q.p[1] * 0.085 * (1 - k * 0.7);
    q.m.position.set(r * Math.cos(a), 0, -r * Math.sin(a)); q.m.scale.setScalar(size);
    q.orbit.scale.setScalar(r); q.orbit.visible = showOrbit;
    q.lbl.at(q.m.position.x, size + 0.4, q.m.position.z);
    q.lbl.show = !(k > 0.5 && (i === 0 || i === 1 || i === 3)) && (v.cam.ph > 0.3 || i === 2);   // 本当の距離では内側が太陽の近くにかたまる・横からは重なるので、地球だけ名前を出す
  });
  // 名前どうし・左上の表示と重なるときは、大事な順（地球→木星→土星→…）に残して、あとの方を隠す
  v.camera.updateMatrixWorld();
  const W = v.el.clientWidth, H = v.el.clientHeight, fs = SM ? 11 : 12.5, placed = [{ x: hud.offsetLeft + hud.offsetWidth / 2, y: hud.offsetTop + hud.offsetHeight / 2, w: hud.offsetWidth, h: hud.offsetHeight }];
  PRI.forEach(i => { const q = planets[i]; if (!q.lbl.show || (SM && q.sub)) return;
    const s = q.lbl.p.clone().project(v.camera), w = q.lbl.el.textContent.length * fs + (SM ? 10 : 14), h = fs + (SM ? 6 : 9), x = (s.x + 1) / 2 * W, y = (1 - s.y) / 2 * H - h * 0.6;
    if (placed.some(b => Math.abs(b.x - x) < (b.w + w) / 2 + 4 && Math.abs(b.y - y) < (b.h + h) / 2 + 4)) q.lbl.show = false; else placed.push({ x, y, w, h }); });
  if (a0 === null) a0 = s.ang[2];
  const yr = (s.ang[2] - a0) / (2 * Math.PI), f1 = x => x < 10 ? x.toFixed(1) : Math.round(x).toLocaleString('ja-JP');
  hud.innerHTML = SM ? '地球 <b>' + f1(yr) + '</b> 年' + (s.playing ? '' : '（停止中）') + '・水星 ' + f1(yr / S.P[0][3]) + '周・木星 ' + (yr / S.P[4][3]).toFixed(2) + '周'
    : '地球が回った年数：<b>' + f1(yr) + '</b> 年' + (s.playing ? '' : '（一時停止中）')
    + '<br>そのあいだに 水星 ' + f1(yr / S.P[0][3]) + '周・木星 ' + (yr / S.P[4][3]).toFixed(2) + '周・海王星 ' + (yr / S.P[7][3]).toFixed(3) + '周'
    + (SM ? '' : '<br><span style="font-size:11px;color:#94a3b8">' + (k > 0.5 ? '距離は本当の比率（大きさは誇張）' : '距離は見やすく圧縮・大きさは誇張') + '</span>');
});
