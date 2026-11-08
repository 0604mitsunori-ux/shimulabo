import { THREE, createView, mat } from '../../assets/three/sim3d.js';
const $ = id => document.getElementById(id);
const v = createView($('view'), {
  views: { front: { tgt: [0, 300, 0], dist: 1500, th: 0.25, ph: 0.12 }, low: { tgt: [0, 300, 0], dist: 900, th: 0.5, ph: -0.05 }, far: { tgt: [0, 300, 0], dist: 2600, th: 0.7, ph: 0.35 } },
  camRow: '#camRow', bg: 0xdfe9f2, far: 20000, minDist: 5, maxDist: 8000, fog: [6000, 16000],
});
const { scene, sun } = v;
sun.position.set(-800, 1500, 900); Object.assign(sun.shadow.camera, { left: -1200, right: 1200, top: 1200, bottom: -1200, far: 5000 }); sun.shadow.camera.updateProjectionMatrix();
const ground = new THREE.Mesh(new THREE.PlaneGeometry(20000, 20000), mat(0xc5ccb6, { roughness: 1 })); ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true; scene.add(ground);
const add = (g, m, x, y, z) => { const o = new THREE.Mesh(g, m); o.position.set(x, y, z); o.castShadow = true; return o; };
// それぞれの形（高さ H は公表値、形は模式）。w は並べるときの幅
const B = {
  me: { n: 'あなた', w: 2, mk(h) { const g = new THREE.Group(), c = mat(0x2f7fc8); g.add(add(new THREE.CylinderGeometry(h * 0.13, h * 0.13, h * 0.72, 16), c, 0, h * 0.36, 0)); g.add(add(new THREE.SphereGeometry(h * 0.12, 16, 12), mat(0xf1c9a5), 0, h * 0.86, 0)); return g; } },
  daibutsu: { n: '奈良の大仏', H: 15, w: 16, mk(h) { const g = new THREE.Group(), c = mat(0x6b5a3a, { metalness: 0.4, roughness: 0.5 }); g.add(add(new THREE.CylinderGeometry(h * 0.18, h * 0.42, h * 0.62, 24), c, 0, h * 0.31, 0)); g.add(add(new THREE.SphereGeometry(h * 0.17, 20, 16), c, 0, h * 0.78, 0)); return g; } },
  liberty: { n: '自由の女神', H: 93, w: 40, mk(h) { const g = new THREE.Group(), st = mat(0xb9ad97), gr = mat(0x6fb5a0); g.add(add(new THREE.BoxGeometry(28, 47, 28), st, 0, 23.5, 0)); g.add(add(new THREE.CylinderGeometry(4, 8, 36, 16), gr, 0, 65, 0)); g.add(add(new THREE.SphereGeometry(3.4, 16, 12), gr, 0, 85, 0)); g.add(add(new THREE.CylinderGeometry(0.9, 0.9, 12, 8), gr, 4, 86, 0)); g.add(add(new THREE.ConeGeometry(1.6, 3, 10), mat(0xf0c040, { emissive: 0x806000 }), 4, 93 - 1.5, 0)); return g; } },
  kurobe: { n: '黒部ダム', H: 186, w: 120, mk(h) { const g = new THREE.Group(); g.add(add(new THREE.BoxGeometry(110, h, 14), mat(0xdcd8cf), 0, h / 2, 0)); return g; } },
  harukas: { n: 'あべのハルカス', H: 300, w: 80, mk(h) { const g = new THREE.Group(), c = mat(0xaab7c4, { metalness: 0.3, roughness: 0.4 }); [[70, 0, 120], [56, 120, 230], [44, 230, 300]].forEach(([w, y0, y1]) => g.add(add(new THREE.BoxGeometry(w, y1 - y0, 50), c, 0, (y0 + y1) / 2, 0))); return g; } },
  eiffel: { n: 'エッフェル塔', H: 330, w: 125, mk(h) { const g = new THREE.Group(), c = mat(0x7a5a3c); const t = add(new THREE.CylinderGeometry(4, 88, 300, 4, 1, true), c, 0, 150, 0); t.material = mat(0x7a5a3c, { side: THREE.DoubleSide, wireframe: false }); g.add(t); g.add(add(new THREE.BoxGeometry(70, 6, 70), c, 0, 58, 0)); g.add(add(new THREE.BoxGeometry(42, 5, 42), c, 0, 116, 0)); g.add(add(new THREE.CylinderGeometry(1.2, 1.2, 30, 6), c, 0, 315, 0)); return g; } },
  tokyotower: { n: '東京タワー', H: 333, w: 100, mk(h) { const g = new THREE.Group(); const red = mat(0xd6352b), wh = mat(0xf2f2f2); const seg = [[0, 60, 46, 36, red], [60, 125, 36, 24, wh], [125, 150, 24, 18, red], [150, 225, 18, 9, wh], [225, 253, 9, 5, red], [253, 333, 3, 0.8, wh]]; seg.forEach(([y0, y1, r0, r1, m], i) => g.add(add(new THREE.CylinderGeometry(r1, r0, y1 - y0, 4, 1), i % 2 ? wh : red, 0, (y0 + y1) / 2, 0))); g.add(add(new THREE.BoxGeometry(34, 10, 34), wh, 0, 150, 0)); g.add(add(new THREE.BoxGeometry(18, 6, 18), wh, 0, 250, 0)); return g; } },
  skytree: { n: '東京スカイツリー', H: 634, w: 100, mk(h) { const g = new THREE.Group(), c = mat(0xe4ecf2, { metalness: 0.2, roughness: 0.5 }); g.add(add(new THREE.CylinderGeometry(9, 34, 495, 16), c, 0, 247.5, 0)); g.add(add(new THREE.CylinderGeometry(22, 22, 20, 24), c, 0, 350, 0)); g.add(add(new THREE.CylinderGeometry(17, 17, 12, 24), c, 0, 450, 0)); g.add(add(new THREE.CylinderGeometry(3, 7, 139, 12), c, 0, 564.5, 0)); return g; } },
  burj: { n: 'ブルジュ・ハリファ', H: 828, w: 120, mk(h) { const g = new THREE.Group(), c = mat(0xb8c4cf, { metalness: 0.5, roughness: 0.3 }); const st = [[0, 160, 48], [160, 320, 40], [320, 460, 32], [460, 560, 24], [560, 640, 16], [640, 700, 10], [700, 828, 3]]; st.forEach(([y0, y1, r], i) => g.add(add(new THREE.CylinderGeometry(r * 0.85, r, y1 - y0, 3 + 3 * (i < 4 ? 1 : 3)), c, 0, (y0 + y1) / 2, 0))); return g; } },
};
const ORDER = ['me', 'daibutsu', 'liberty', 'kurobe', 'harukas', 'eiffel', 'tokyotower', 'skytree', 'burj'];
const DEF = { me: 1, liberty: 1, tokyotower: 1, skytree: 1, burj: 1 };
$('picks').innerHTML = ORDER.filter(k => k !== 'me').map(k => '<label><input type="checkbox" data-k="' + k + '"' + (DEF[k] ? ' checked' : '') + '> ' + B[k].n + '（' + B[k].H + 'm）</label>').join('');
const grp = new THREE.Group(); scene.add(grp);
let labels = [];
function update() {
  const me = +$('me').value / 100; $('meL').textContent = $('me').value + ' cm';
  grp.clear(); labels.forEach(l => { l.show = false; l.el.remove(); }); labels = [];
  const ks = ['me', ...ORDER.filter(k => k !== 'me' && $('picks').querySelector('[data-k="' + k + '"]').checked)];
  const items = ks.map(k => ({ k, H: k === 'me' ? me : B[k].H, w: B[k].w }));
  const tw = items.reduce((a, b) => a + b.w + 40, 0); let x = -tw / 2;
  items.forEach(it => { x += it.w / 2 + 20; const o = B[it.k].mk(it.H); o.position.x = x; grp.add(o); labels.push(v.label(B[it.k].n + ' ' + (it.k === 'me' ? $('me').value + 'cm' : it.H + 'm'), [x, it.H + 4, 0], { accent: it.k === 'me' })); x += it.w / 2 + 20; });
  const maxH = Math.max(...items.map(i => i.H));
  const fit = Math.max(maxH, tw * 0.55);
  Object.assign(v.views.front, { tgt: [0, maxH * 0.45, 0], dist: fit * 2.1 }); Object.assign(v.views.low, { tgt: [0, maxH * 0.55, 0], dist: fit * 1.4 }); Object.assign(v.views.far, { tgt: [0, maxH * 0.4, 0], dist: fit * 3.2 });
  v.setView(document.querySelector('#camRow .on')?.dataset.v || 'front');
  const s = items.filter(i => i.k !== 'me').sort((a, b) => b.H - a.H);
  if (!s.length) { $('big').textContent = '—'; return; }
  const t = s[0];
  $('big').textContent = t.H.toLocaleString();
  $('sub').textContent = B[t.k].n + '（並べた ' + s.length + ' つの中で）';
  $('sPeople').textContent = '約 ' + Math.round(t.H / me).toLocaleString() + ' 人分';
  $('sView').textContent = '約 ' + Math.round(3.57 * Math.sqrt(t.H)) + ' km 先まで';
  $('sRatio').textContent = s[1] ? B[s[1].k].n + 'より ' + (t.H - s[1].H).toLocaleString() + 'm 高い' : '—';
  $('resNote').innerHTML = '<strong>' + B[t.k].n + 'は、身長' + $('me').value + 'cmのあなたの約' + Math.round(t.H / me).toLocaleString() + '人分。</strong><br>てっぺんからは、空気の曲がりを考えなければ約' + Math.round(3.57 * Math.sqrt(t.H)) + 'km先の地平線まで見える計算です。チェックを入れ替えて比べてみてください。';
  window.SHARE = B[t.k].n + '（' + t.H + 'm）は、身長' + $('me').value + 'cmの私の約' + Math.round(t.H / me).toLocaleString() + '人分🗼\n世界の塔を3Dで並べて高さ比べ👇';
}
$('picks').addEventListener('change', update); $('me').addEventListener('input', update);
update(); v.setView('front', true);
