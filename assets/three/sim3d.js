// シミュラボ 3Dシリーズ共通の舞台（2026-11-08〜）
// 使い方: import { THREE, createView } from '../../assets/three/sim3d.js';
//   const v = createView(document.getElementById('view'), { views: { all: {tgt:[0,0,0], dist:20, th:0.4, ph:0.3} }, bg: 0xe8e9eb });
//   v.scene.add(...); v.label('名前', [x,y,z], {accent:true}); v.onFrame((t, dt) => {...});
// ・ドラッグで回転（縦スクロールは邪魔しない）、ホイール/＋－で寄る、カメラのボタン（data-v）を自動でつなぐ
// ・見えていない間は描かない。WebGL が使えない端末では load 表示を差し替えて止まる
import * as THREE from './three.module.js';
export { THREE };

export const COL = { bg: 0xe8e9eb, concrete: 0xd9d5cc, soil: 0xcbb79a, grass: 0xc5ccb6, water: 0x3f8fd8, red: 0xd6352b, teal: 0x2c6b86, ink: 0x22262b };
export const mat = (color, o = {}) => new THREE.MeshStandardMaterial({ color, roughness: 0.85, metalness: 0, ...o });
export const water = (opacity = 0.55, color = COL.water) => new THREE.MeshStandardMaterial({ color, transparent: true, opacity, roughness: 0.25, depthWrite: false, side: THREE.DoubleSide });

export function createView(el, { views = {}, start, bg = COL.bg, fov = 35, near = 0.1, far = 5000, shadows = true, minDist = 1, maxDist = 1e5, camRow, fog, occlude = 0 } = {}) {
  let renderer;
  const load = el.querySelector('.load');
  try { renderer = new THREE.WebGLRenderer({ antialias: true }); }
  catch (e) { if (load) load.textContent = 'この端末では3D表示が使えません（計算は使えます）'; throw e; }
  const mobile = matchMedia('(max-width:640px)').matches;
  renderer.setPixelRatio(Math.min(2, window.devicePixelRatio || 1));
  renderer.localClippingEnabled = true;
  renderer.shadowMap.enabled = shadows; renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  el.prepend(renderer.domElement);
  const scene = new THREE.Scene();
  scene.background = bg == null ? null : new THREE.Color(bg);
  if (fog) scene.fog = new THREE.Fog(bg, fog[0], fog[1]);
  const camera = new THREE.PerspectiveCamera(fov, 16 / 10, near, far);
  const hemi = new THREE.HemisphereLight(0xffffff, 0xb8b2a6, 0.95); scene.add(hemi);
  const sun = new THREE.DirectionalLight(0xffffff, 1.1); sun.position.set(-30, 60, 40);
  sun.castShadow = shadows; sun.shadow.mapSize.set(mobile ? 1024 : 2048, mobile ? 1024 : 2048); sun.shadow.bias = -0.0004; sun.shadow.normalBias = 0.5;
  scene.add(sun); scene.add(sun.target);

  // ---- カメラ（注視点のまわりを回る） ----
  const cam = { tgt: new THREE.Vector3(), dist: 10, th: 0, ph: 0.3 }, goal = { tgt: new THREE.Vector3(), dist: 10, th: 0, ph: 0.3 };
  const row = camRow ? document.querySelector(camRow) : null;
  function setView(k, snap) {
    const v = views[k]; if (!v) return;
    goal.tgt.set(...v.tgt); goal.dist = v.dist; goal.th = v.th; goal.ph = v.ph;
    if (snap) { cam.tgt.copy(goal.tgt); cam.dist = goal.dist; cam.th = goal.th; cam.ph = goal.ph; }
    if (row) row.querySelectorAll('button').forEach(b => b.classList.toggle('on', b.dataset.v === k));
  }
  if (row) row.querySelectorAll('button').forEach(b => b.addEventListener('click', () => setView(b.dataset.v)));
  setView(start || Object.keys(views)[0], true);
  let drag = null;
  el.addEventListener('pointerdown', e => { if (e.target.closest('button')) return; drag = { x: e.clientX, y: e.clientY, th: goal.th, ph: goal.ph }; el.classList.add('drag'); });
  addEventListener('pointermove', e => { if (!drag) return; goal.th = drag.th - (e.clientX - drag.x) * 0.006; goal.ph = Math.max(-1.45, Math.min(1.45, drag.ph + (e.clientY - drag.y) * 0.004)); cam.th = goal.th; cam.ph = goal.ph; });
  const up = () => { drag = null; el.classList.remove('drag'); };
  addEventListener('pointerup', up); addEventListener('pointercancel', up);
  el.addEventListener('wheel', e => { e.preventDefault(); goal.dist = Math.max(minDist, Math.min(maxDist, goal.dist * (e.deltaY > 0 ? 1.12 : 0.89))); }, { passive: false });
  const zoom = document.createElement('div'); zoom.className = 'zoom';
  zoom.innerHTML = '<button aria-label="近づく">＋</button><button aria-label="離れる">－</button>';
  el.appendChild(zoom);
  zoom.children[0].onclick = () => goal.dist = Math.max(minDist, goal.dist * 0.8);
  zoom.children[1].onclick = () => goal.dist = Math.min(maxDist, goal.dist * 1.25);

  // ---- ラベル ----
  const labels = [];
  function label(text, pos, { accent = false, sub = false, obj = null } = {}) {
    const d = document.createElement('div'); d.className = 'lbl' + (accent ? ' acc' : '') + (sub ? ' sub' : ''); d.textContent = text; el.appendChild(d);
    const L = { el: d, p: new THREE.Vector3(...pos), obj, show: true, set(t) { d.textContent = t; }, at(x, y, z) { this.p.set(x, y, z); } };
    labels.push(L); return L;
  }

  const fns = [];
  const api = { THREE, scene, camera, renderer, sun, hemi, el, mobile, label, setView, cam, goal, onFrame: f => fns.push(f), views };
  function resize() { const w = el.clientWidth, h = el.clientHeight; if (!w || !h) return; renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix(); }
  new ResizeObserver(resize).observe(el); resize();
  let visible = true; new IntersectionObserver(es => { visible = es[0].isIntersecting; }).observe(el);
  const tmp = new THREE.Vector3(), tmp2 = new THREE.Vector3(); let last = 0;
  function step(now) {
    const dt = Math.max(0, Math.min(0.1, (now - (last || now)) / 1000)); last = now;
    const k = 1 - Math.pow(0.002, dt);
    cam.tgt.lerp(goal.tgt, k); cam.dist += (goal.dist - cam.dist) * k; cam.th += (goal.th - cam.th) * k; cam.ph += (goal.ph - cam.ph) * k;
    const D = cam.dist * Math.max(1, 1.6 / camera.aspect);
    camera.position.set(cam.tgt.x + D * Math.sin(cam.th) * Math.cos(cam.ph), cam.tgt.y + D * Math.sin(cam.ph), cam.tgt.z + D * Math.cos(cam.th) * Math.cos(cam.ph));
    camera.lookAt(cam.tgt);
    for (const f of fns) f(now / 1000, dt);
    renderer.render(scene, camera);
    const w = el.clientWidth, h = el.clientHeight;
    for (const l of labels) {
      if (l.obj) l.obj.getWorldPosition(tmp); else tmp.copy(l.p);
      // 球（原点・半径 occlude）の裏側にあるラベルは隠す
      const hidden = occlude && tmp.length() >= occlude * 0.98 && tmp.dot(tmp2.copy(camera.position).sub(tmp)) < 0;
      tmp.project(camera);
      const on = !hidden && l.show && tmp.z < 1 && Math.abs(tmp.x) < 0.97 && Math.abs(tmp.y) < 0.97;
      l.el.style.display = on ? '' : 'none';
      if (on) l.el.style.transform = `translate(${(tmp.x + 1) / 2 * w}px,${(1 - tmp.y) / 2 * h}px) translate(-50%,-110%)`;
    }
  }
  function frame(now) { requestAnimationFrame(frame); if (!visible) { last = now; return; } try { step(now); } catch (e) { window.__err = String(e && e.stack || e); } }
  api.step = step;
  if (load) load.remove();
  requestAnimationFrame(frame);
  window.__v3d = api;
  return api;
}

// 球面の点（緯度・経度 → xyz、y が北）
export function lonlat(lon, lat, r) {
  const a = lat * Math.PI / 180, b = lon * Math.PI / 180;
  return new THREE.Vector3(r * Math.cos(a) * Math.sin(b), r * Math.sin(a), r * Math.cos(a) * Math.cos(b));
}

// 世界地図の陸地を描いた正距円筒のテクスチャ（world-atlas 110m を読み、TopoJSON を自前でほどく）
export async function earthTexture({ w = 2048, sea = '#cfe3f2', land = '#b9c7a2', line = 'rgba(80,100,70,.55)', grid = true } = {}) {
  const cv = document.createElement('canvas'); cv.width = w; cv.height = w / 2;
  const g = cv.getContext('2d'); g.fillStyle = sea; g.fillRect(0, 0, w, w / 2);
  if (grid) { g.strokeStyle = 'rgba(255,255,255,.55)'; g.lineWidth = 1; for (let i = 0; i <= 12; i++) { g.beginPath(); g.moveTo(i * w / 12, 0); g.lineTo(i * w / 12, w / 2); g.stroke(); } for (let j = 0; j <= 6; j++) { g.beginPath(); g.moveTo(0, j * w / 12); g.lineTo(w, j * w / 12); g.stroke(); } }
  try {
    const topo = await (await fetch('https://cdn.jsdelivr.net/npm/world-atlas@2.0.2/land-110m.json')).json();
    const [sx, sy] = topo.transform.scale, [tx, ty] = topo.transform.translate;
    const arcs = topo.arcs.map(a => { let x = 0, y = 0; return a.map(([dx, dy]) => { x += dx; y += dy; return [x * sx + tx, y * sy + ty]; }); });
    const ring = idx => { const out = []; for (const i of idx) { const a = i < 0 ? arcs[~i].slice().reverse() : arcs[i]; out.push(...(out.length ? a.slice(1) : a)); } return out; };
    const X = lon => (lon + 180) / 360 * w, Y = lat => (90 - lat) / 180 * (w / 2);
    g.fillStyle = land; g.strokeStyle = line; g.lineWidth = 1.2;
    for (const geo of topo.objects.land.geometries) {
      const polys = geo.type === 'Polygon' ? [geo.arcs] : geo.arcs;
      for (const p of polys) {
        g.beginPath();
        for (const r of p) { const pts = ring(r); pts.forEach(([lo, la], i) => { const px = X(lo), py = Y(la); if (i && Math.abs(lo - pts[i - 1][0]) > 180) g.moveTo(px, py); else i ? g.lineTo(px, py) : g.moveTo(px, py); }); g.closePath(); }
        g.fill('evenodd'); g.stroke();
      }
    }
  } catch (e) { /* 地図が取れなくても、海と経緯線だけで描く */ }
  const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; return t;
}

// 球に貼るとき：three の SphereGeometry は u=0 が経度 -90°付近になるので、lonlat() と合わせるための回転
export const EARTH_ROT_Y = -Math.PI / 2;

// 数字を少しずつ動かす
export function animNum(el, from, to, dur = 700, dec = 0) { const t0 = performance.now(); (function s(n) { const p = Math.min(1, (n - t0) / dur), e = 1 - Math.pow(1 - p, 3), v = from + (to - from) * e; el.textContent = dec ? v.toFixed(dec) : Math.round(v).toLocaleString(); if (p < 1) requestAnimationFrame(s); })(performance.now()); }
