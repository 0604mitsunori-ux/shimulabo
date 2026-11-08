import { THREE, createView, mat } from '../../assets/three/sim3d.js';
const $ = id => document.getElementById(id);
const v = createView($('view'), {
  views: { persp: { tgt: [0, 0.8, 0], dist: 14, th: 0.6, ph: 0.6 }, top: { tgt: [0, 0, 0], dist: 15, th: 0, ph: 1.45 }, side: { tgt: [0, 1, 0], dist: 13, th: 0.9, ph: 0.12 } },
  camRow: '#camRow', bg: 0xf3f1ea, minDist: 4, maxDist: 40,
});
const { scene } = v;
const ground = new THREE.Mesh(new THREE.PlaneGeometry(60, 60), new THREE.ShadowMaterial({ opacity: 0.12 })); ground.rotation.x = -Math.PI / 2; ground.position.y = -0.01; ground.receiveShadow = true; scene.add(ground);
const grid = new THREE.GridHelper(30, 30, 0xd8d3c6, 0xe6e2d8); grid.position.y = -0.005; scene.add(grid);
const COLS = [0x8ec5e8, 0xf2b880, 0xa8d5a2, 0xe8a5b8, 0xc7b8e8, 0xf0dc82, 0x9fd8d0];
const fmat = i => new THREE.MeshStandardMaterial({ color: COLS[i % COLS.length], roughness: 0.75, side: THREE.DoubleSide, polygonOffset: true, polygonOffsetFactor: 1 });
const edge = g => new THREE.LineSegments(new THREE.EdgesGeometry(g), new THREE.LineBasicMaterial({ color: 0x4a4f55 }));
const PI = Math.PI;

// 平らな面（XZ平面）。dir の向きに長さ len だけ伸び、幅 w。tri なら三角形
function faceGeo(w, len, tri) {
  const s = new THREE.Shape();
  if (tri) { s.moveTo(-w / 2, 0); s.lineTo(w / 2, 0); s.lineTo(0, len); }
  else { s.moveTo(-w / 2, 0); s.lineTo(w / 2, 0); s.lineTo(w / 2, len); s.lineTo(-w / 2, len); }
  const g = new THREE.ShapeGeometry(s); g.rotateX(PI / 2); return g;      // y=len → z=len
}
// ちょうつがい（親の局所座標の pos に、向き dir='+z'|'-z'|'+x'|'-x' へ伸びる面をつける）
function flap(parent, pos, dir, w, len, ci, fold, tri = false) {
  const hinge = new THREE.Group(); hinge.position.set(...pos); parent.add(hinge);
  const inner = new THREE.Group(); hinge.add(inner);
  inner.rotation.y = { '+z': 0, '-z': PI, '+x': PI / 2, '-x': -PI / 2 }[dir];
  const pivot = new THREE.Group(); inner.add(pivot);
  const g = faceGeo(w, len, tri);
  const m = new THREE.Mesh(g, fmat(ci)); m.castShadow = true; pivot.add(m); pivot.add(edge(g));
  return { hinge: pivot, fold, set(k) { pivot.rotation.x = -fold * k; }, child: pivot };   // 局所で +z へ伸び、-x回転で立ち上がる
}
function base(w, d, ci) {
  const g = new THREE.PlaneGeometry(w, d); g.rotateX(-PI / 2);
  const grp = new THREE.Group(); const m = new THREE.Mesh(g, fmat(ci)); m.receiveShadow = true; grp.add(m); grp.add(edge(g)); return grp;
}

const SHAPES = {
  cube: { name: '立方体', dims: [['a', '1辺', 4]] },
  box: { name: '直方体', dims: [['a', 'たて', 3], ['b', '横', 5], ['c', '高さ', 2]] },
  prism: { name: '三角柱', dims: [['s', '底面の1辺（正三角形）', 3], ['L', '長さ', 6]] },
  pyramid: { name: '四角すい', dims: [['a', '底面の1辺', 4], ['h', '高さ', 3]] },
  cyl: { name: '円柱', dims: [['r', '半径', 2], ['h', '高さ', 5]] },
  cone: { name: '円すい', dims: [['r', '半径', 3], ['h', '高さ', 4]] },
};
let cur = 'cube', model = null, K = 0;
$('shapes').innerHTML = Object.entries(SHAPES).map(([k, s], i) => '<button data-s="' + k + '"' + (i === 0 ? ' class="on"' : '') + '>' + s.name + '</button>').join('');
function dimsUI() {
  $('dims').innerHTML = SHAPES[cur].dims.map(([id, lab, val]) => '<div class="field"><div class="slider-head"><label for="dm_' + id + '">' + lab + '</label><span class="val" id="dm_' + id + 'L"></span></div><input type="range" id="dm_' + id + '" min="1" max="10" step="0.5" value="' + val + '"></div>').join('');
  $('dims').querySelectorAll('input').forEach(i => i.addEventListener('input', rebuild));
}
const D = id => +$('dm_' + id).value;

function buildPoly(S) {
  const root = new THREE.Group(); const flaps = [];
  if (cur === 'cube' || cur === 'box') {
    const a = cur === 'cube' ? D('a') : D('a'), b = cur === 'cube' ? D('a') : D('b'), c = cur === 'cube' ? D('a') : D('c');
    const w = a * S, d = b * S, h = c * S;
    root.add(base(w, d, 0));
    const fr = flap(root, [0, 0, d / 2], '+z', w, h, 1, PI / 2); flaps.push(fr);
    flaps.push(flap(root, [0, 0, -d / 2], '-z', w, h, 2, PI / 2));
    flaps.push(flap(root, [w / 2, 0, 0], '+x', d, h, 3, PI / 2));
    flaps.push(flap(root, [-w / 2, 0, 0], '-x', d, h, 4, PI / 2));
    flaps.push(flap(fr.child, [0, 0, h], '+z', w, d, 5, PI / 2));
  } else if (cur === 'prism') {
    const s = D('s') * S, L = D('L') * S;
    root.add(base(L, s, 0));
    flaps.push(flap(root, [0, 0, s / 2], '+z', L, s, 1, 2 * PI / 3));
    flaps.push(flap(root, [0, 0, -s / 2], '-z', L, s, 2, 2 * PI / 3));
    flaps.push(flap(root, [L / 2, 0, 0], '+x', s, s * Math.sqrt(3) / 2, 3, PI / 2, true));
    flaps.push(flap(root, [-L / 2, 0, 0], '-x', s, s * Math.sqrt(3) / 2, 4, PI / 2, true));
  } else if (cur === 'pyramid') {
    const a = D('a') * S, h = D('h') * S, l = Math.hypot(h, a / 2), fold = PI - Math.atan2(h, a / 2);
    root.add(base(a, a, 0));
    [['+z', [0, 0, a / 2]], ['-z', [0, 0, -a / 2]], ['+x', [a / 2, 0, 0]], ['-x', [-a / 2, 0, 0]]].forEach(([dir, p], i) => flaps.push(flap(root, p, dir, a, l, i + 1, fold, true)));
  }
  return { root, set(k) { flaps.forEach(f => f.set(k)); } };
}
// 円柱：側面の長方形が丸まり、上下の円がちょうつがいで立つ
function buildCyl(S) {
  const r = D('r') * S, h = D('h') * S, L = 2 * PI * r, NS = 64, NZ = 2;
  const g = new THREE.PlaneGeometry(L, h, NS, NZ); g.rotateX(-PI / 2);   // x＝周の向き、z＝高さの向き
  const flat = g.attributes.position.array.slice();
  const side = new THREE.Mesh(g, fmat(0)); side.castShadow = true;
  const root = new THREE.Group(); root.add(side);
  const caps = [1, -1].map((sg, i) => {
    const hinge = new THREE.Group(); hinge.position.set(0, 0, sg * h / 2); root.add(hinge);
    const cg = new THREE.CircleGeometry(r, 48); cg.rotateX(-PI / 2); cg.translate(0, 0, sg * r);
    const m = new THREE.Mesh(cg, fmat(i + 1)); m.castShadow = true; hinge.add(m); hinge.add(edge(cg));
    return { hinge, sg };
  });
  return { root, set(k) {
    const p = g.attributes.position.array, kap = k / r;
    for (let i = 0; i < p.length; i += 3) { const s = flat[i]; if (kap < 1e-5) { p[i] = s; p[i + 1] = 0; } else { p[i] = Math.sin(kap * s) / kap; p[i + 1] = (1 - Math.cos(kap * s)) / kap; } p[i + 2] = flat[i + 2]; }
    g.attributes.position.needsUpdate = true; g.computeVertexNormals();
    caps.forEach(c => c.hinge.rotation.x = -c.sg * k * PI / 2);
  } };
}
// 円すい：おうぎ形が丸まって円すいに。底面の円はふちの1点を軸にくるっと裏返って底になる
function buildCone(S) {
  const r = D('r') * S, hh = D('h') * S, l = Math.hypot(r, hh), PHI = 2 * PI * r / l, aF = Math.asin(r / l);
  const NR = 16, NP = 64, pos = [], idx = [], uv = [];
  for (let i = 0; i <= NR; i++) for (let j = 0; j <= NP; j++) { pos.push(0, 0, 0); uv.push(j / NP, i / NR); }
  for (let i = 0; i < NR; i++) for (let j = 0; j < NP; j++) { const a = i * (NP + 1) + j, b = a + NP + 1; idx.push(a, b, a + 1, b, b + 1, a + 1); }
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3)); g.setIndex(idx);
  const side = new THREE.Mesh(g, fmat(0)); side.castShadow = true;
  const root = new THREE.Group(); root.add(side);
  const hinge = new THREE.Group(); root.add(hinge);
  const cg = new THREE.CircleGeometry(r, 48); cg.rotateX(-PI / 2); cg.translate(r, 0, 0);
  const disk = new THREE.Mesh(cg, fmat(1)); disk.castShadow = true; hinge.add(disk); hinge.add(edge(cg));
  return { root, set(k) {
    const al = PI / 2 + (aF - PI / 2) * k, sa = Math.sin(al), ca = Math.cos(al), p = g.attributes.position.array;
    let n = 0;
    for (let i = 0; i <= NR; i++) { const rho = l * i / NR; for (let j = 0; j <= NP; j++) { const phi = -PHI / 2 + PHI * j / NP, th = phi / sa; p[n++] = rho * sa * Math.cos(th); p[n++] = (l - rho) * ca; p[n++] = rho * sa * Math.sin(th); } }
    g.attributes.position.needsUpdate = true; g.computeVertexNormals();
    hinge.position.set(l * sa, 0, 0); hinge.rotation.z = k * PI;
  } };
}
function calc() {
  const P = Math.PI; let A, V, F, ex;
  if (cur === 'cube') { const a = D('a'); A = 6 * a * a; V = a ** 3; F = 6; ex = '辺12本・頂点8個'; }
  if (cur === 'box') { const a = D('a'), b = D('b'), c = D('c'); A = 2 * (a * b + b * c + c * a); V = a * b * c; F = 6; ex = '向かい合う面は同じ形'; }
  if (cur === 'prism') { const s = D('s'), L = D('L'), t = Math.sqrt(3) / 4 * s * s; A = 2 * t + 3 * s * L; V = t * L; F = 5; ex = '底面積 ' + t.toFixed(2) + 'cm²'; }
  if (cur === 'pyramid') { const a = D('a'), h = D('h'), l = Math.hypot(h, a / 2); A = a * a + 2 * a * l; V = a * a * h / 3; F = 5; ex = '側面の三角形の高さ ' + l.toFixed(2) + 'cm'; }
  if (cur === 'cyl') { const r = D('r'), h = D('h'); A = 2 * P * r * r + 2 * P * r * h; V = P * r * r * h; F = 3; ex = '側面の横 ' + (2 * P * r).toFixed(2) + 'cm（＝円周）'; }
  if (cur === 'cone') { const r = D('r'), h = D('h'), l = Math.hypot(r, h); A = P * r * r + P * r * l; V = P * r * r * h / 3; F = 2; ex = 'おうぎ形の中心角 ' + (360 * r / l).toFixed(1) + '°（母線 ' + l.toFixed(2) + 'cm）'; }
  $('big').textContent = A.toFixed(2).replace(/\.00$/, '');
  $('sVol').textContent = V.toFixed(2).replace(/\.00$/, '') + ' cm³';
  $('sFaces').textContent = F + ' 面';
  $('sExtra').textContent = ex;
  $('sub').textContent = SHAPES[cur].name + '（' + SHAPES[cur].dims.map(([id, lab]) => lab + ' ' + D(id) + 'cm').join('・') + '）';
  $('resNote').innerHTML = {
    cube: '<strong>6つの正方形でできた展開図。</strong><br>立方体の展開図は全部で11種類。どの面とどの面が向かい合うかを、組み立てながら確かめてみましょう。',
    box: '<strong>表面積＝2×（たて×横＋横×高さ＋高さ×たて）。</strong><br>向かい合う面は同じ形なので、3種類の面が2枚ずつあります。',
    prism: '<strong>側面3枚が120°ずつ折れて、三角形の筒になる。</strong><br>体積は「底面積×高さ（長さ）」で、柱体ならどれも同じ考え方です。',
    pyramid: '<strong>側面の三角形4枚が、てっぺんの1点に集まる。</strong><br>体積は同じ底面・同じ高さの角柱の3分の1です。',
    cyl: '<strong>側面は長方形。横の長さは底面の円周と同じ。</strong><br>スライダーを動かすと、長方形がくるっと丸まって、ふたの円とぴったり合います。',
    cone: '<strong>側面はおうぎ形。中心角＝360°×半径÷母線。</strong><br>おうぎ形の弧の長さが、底面の円周とぴったり同じになるように丸まります。',
  }[cur];
  window.SHARE = SHAPES[cur].name + '（' + SHAPES[cur].dims.map(([id, lab]) => lab + D(id) + 'cm').join('・') + '）の表面積は' + $('big').textContent + 'cm²、体積は' + $('sVol').textContent + '📦\n展開図が3Dで組み立つ👇';
}
function rebuild() {
  SHAPES[cur].dims.forEach(([id]) => $('dm_' + id + 'L').textContent = D(id) + ' cm');
  if (model) scene.remove(model.root);
  const maxd = Math.max(...SHAPES[cur].dims.map(([id]) => D(id)));
  const S = 3.2 / maxd;
  model = cur === 'cyl' ? buildCyl(S) : cur === 'cone' ? buildCone(S) : buildPoly(S);
  scene.add(model.root); model.set(K); calc();
}
let playing = false;
$('playBtn').onclick = () => { if (K >= 1) K = 0; playing = !playing; $('playBtn').textContent = playing ? '❚❚ 止める' : '▶ 組み立てる'; };
$('k').addEventListener('input', () => { K = $('k').value / 1000; playing = false; $('playBtn').textContent = '▶ 組み立てる'; model.set(K); });
v.onFrame((t, dt) => { if (!playing) return; K = Math.min(1, K + dt / 3); $('k').value = Math.round(K * 1000); model.set(K); if (K >= 1) { playing = false; $('playBtn').textContent = '↺ もう一度'; } });
$('shapes').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; cur = b.dataset.s; $('shapes').querySelectorAll('button').forEach(x => x.classList.toggle('on', x === b)); dimsUI(); K = 0; $('k').value = 0; rebuild(); playing = true; $('playBtn').textContent = '❚❚ 止める'; });
dimsUI(); rebuild();
setTimeout(() => { playing = true; $('playBtn').textContent = '❚❚ 止める'; }, 800);
