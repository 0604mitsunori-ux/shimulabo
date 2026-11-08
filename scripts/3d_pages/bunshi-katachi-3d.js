import { THREE, createView, mat } from '../../assets/three/sim3d.js';
const $ = id => document.getElementById(id);
const v = createView($('view'), {
  views: { front: { tgt: [0, 0, 0], dist: 9, th: 0.35, ph: 0.25 }, top: { tgt: [0, 0, 0], dist: 9, th: 0, ph: 1.4 }, side: { tgt: [0, 0, 0], dist: 9, th: Math.PI / 2, ph: 0.05 } },
  camRow: '#camRow', bg: 0xf3f1ea, shadows: false, minDist: 4, maxDist: 30,
});
v.hemi.intensity = 1.1; v.sun.intensity = 1.3;
const EL = { H: [0xf4f4f4, 0.32, 1.2], C: [0x3a3f45, 0.45, 1.7], N: [0x3c6fd8, 0.45, 1.55], O: [0xd6352b, 0.45, 1.52], F: [0x8fcf45, 0.42, 1.47], B: [0xf0a0a0, 0.45, 1.92], S: [0xe8c23a, 0.55, 1.8] };
const n = (x, y, z) => new THREE.Vector3(x, y, z).normalize();
// NH3：3本の結合が軸と α の角をなし、互いに107°（cos²α＝(cos107°＋0.5)/1.5）
const aN = Math.acos(Math.sqrt((Math.cos(107 * Math.PI / 180) + 0.5) / 1.5));
const tri = (a, y) => [0, 1, 2].map(k => n(Math.sin(a) * Math.cos(k * 2.094), y * Math.cos(a), Math.sin(a) * Math.sin(k * 2.094)));
const hw = 104.5 / 2 * Math.PI / 180;
const MOLS = {
  H2O: { name: '水 H₂O', c: 'O', a: 'H', dirs: [n(Math.sin(hw), -Math.cos(hw), 0), n(-Math.sin(hw), -Math.cos(hw), 0)], lps: [n(0, 0.58, 0.82), n(0, 0.58, -0.82)], ang: 104.5, shape: '折れ線形', pol: 'あり（極性分子）', len: 1.6 },
  NH3: { name: 'アンモニア NH₃', c: 'N', a: 'H', dirs: tri(aN, -1), lps: [n(0, 1, 0)], ang: 107, shape: '三角すい形', pol: 'あり（極性分子）', len: 1.65 },
  CH4: { name: 'メタン CH₄', c: 'C', a: 'H', dirs: [n(1, 1, 1), n(1, -1, -1), n(-1, 1, -1), n(-1, -1, 1)], lps: [], ang: 109.5, shape: '正四面体形', pol: 'なし（無極性分子）', len: 1.7 },
  CO2: { name: '二酸化炭素 CO₂', c: 'C', a: 'O', dirs: [n(1, 0, 0), n(-1, 0, 0)], lps: [], ang: 180, shape: '直線形', pol: 'なし（無極性分子）', len: 1.9, dbl: true },
  BF3: { name: '三フッ化ホウ素 BF₃', c: 'B', a: 'F', dirs: [0, 1, 2].map(k => n(Math.cos(k * 2.094 + 1.571), 0, Math.sin(k * 2.094 + 1.571))), lps: [], ang: 120, shape: '正三角形（平面）', pol: 'なし（無極性分子）', len: 2.0 },
  SF6: { name: '六フッ化硫黄 SF₆', c: 'S', a: 'F', dirs: [n(1, 0, 0), n(-1, 0, 0), n(0, 1, 0), n(0, -1, 0), n(0, 0, 1), n(0, 0, -1)], lps: [], ang: 90, shape: '正八面体形', pol: 'なし（無極性分子）', len: 2.1 },
};
$('mols').innerHTML = Object.entries(MOLS).map(([k, m], i) => '<button data-m="' + k + '"' + (i === 0 ? ' class="on"' : '') + '>' + m.name + '</button>').join('');
const root = new THREE.Group(); v.scene.add(root);
const labels = [];
let cur = 'H2O';
function cyl(a, b, r, color) {
  const d = b.clone().sub(a), L = d.length();
  const m = new THREE.Mesh(new THREE.CylinderGeometry(r, r, L, 20), mat(color, { roughness: 0.5 }));
  m.position.copy(a).addScaledVector(d, 0.5); m.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), d.normalize()); return m;
}
function build() {
  root.clear(); labels.forEach(l => { l.el.remove(); }); labels.length = 0;
  const M = MOLS[cur], fill = $('fill').checked;
  const [cc, cr, cv] = EL[M.c], [ac, ar, av] = EL[M.a];
  const sc = fill ? 1 : 0.55;
  const center = new THREE.Mesh(new THREE.SphereGeometry(fill ? cv * 0.75 : cr, 40, 30), mat(cc, { roughness: 0.35 })); root.add(center);
  M.dirs.forEach(d => {
    const p = d.clone().multiplyScalar(M.len);
    const at = new THREE.Mesh(new THREE.SphereGeometry(fill ? av * 0.75 : ar, 36, 26), mat(ac, { roughness: 0.35 })); at.position.copy(p); root.add(at);
    if (!fill) {
      if (M.dbl) { const off = new THREE.Vector3(0, 0.09, 0); root.add(cyl(off.clone(), p.clone().add(off), 0.07, 0x9aa0a6)); root.add(cyl(off.clone().negate(), p.clone().sub(off), 0.07, 0x9aa0a6)); }
      else root.add(cyl(new THREE.Vector3(), p, 0.1, 0x9aa0a6));
    }
  });
  if ($('lp').checked) M.lps.forEach(d => {
    const lobe = new THREE.Mesh(new THREE.SphereGeometry(0.42, 30, 20), new THREE.MeshStandardMaterial({ color: 0x8a6fd1, transparent: true, opacity: 0.35, depthWrite: false }));
    lobe.scale.set(1, 1.7, 1); lobe.position.copy(d).multiplyScalar(1.05); lobe.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), d); root.add(lobe);
    [-0.12, 0.12].forEach(o => { const e = new THREE.Mesh(new THREE.SphereGeometry(0.07, 12, 8), new THREE.MeshBasicMaterial({ color: 0x5b3fb0 })); const side = new THREE.Vector3(1, 0, 0); if (Math.abs(d.x) > 0.9) side.set(0, 0, 1); e.position.copy(d).multiplyScalar(1.15).addScaledVector(side, o); root.add(e); });
  });
  // 角度の弧（最初の2本の結合のあいだ）
  if (M.ang < 180) {
    const a = M.dirs[0], b = M.dirs[1], pts = [];
    for (let i = 0; i <= 30; i++) { const q = new THREE.Vector3().copy(a).lerp(b, i / 30).normalize().multiplyScalar(0.75); pts.push(q); }
    const arc = new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), new THREE.LineBasicMaterial({ color: 0xc4442b, linewidth: 2 })); root.add(arc);
    const mid = a.clone().add(b).normalize().multiplyScalar(0.95);
    labels.push(v.label(M.ang + '°', [mid.x, mid.y, mid.z], { accent: true }));
  }
  labels.push(v.label(M.c, [0, 0, 0]));
  labels.forEach(l => l.obj = null);
  // 回るグループについていくラベル
  labels.forEach(l => { const o = new THREE.Object3D(); o.position.copy(l.p); root.add(o); l.obj = o; });
  $('big').textContent = M.ang;
  $('sub').textContent = M.name;
  $('sShape').textContent = M.shape;
  $('sLp').textContent = M.lps.length + ' 組';
  $('sPol').textContent = M.pol;
  $('resNote').innerHTML = {
    H2O: '<strong>非共有電子対が2組。</strong><br>2組が強く押し合うので、正四面体の109.5°から104.5°まで縮み、折れ曲がった形になります。この形のおかげで水は極性をもち、いろいろな物を溶かせます。',
    NH3: '<strong>非共有電子対が1組。</strong><br>上の1組に押されて、結合の角度は109.5°から107°に。窒素を頂点にした三角すいの形です。',
    CH4: '<strong>4組とも結合に使われている。</strong><br>4組が同じ強さで押し合い、正四面体の頂点の向き（109.5°）にきれいに並びます。',
    CO2: '<strong>二重結合が2本、まっすぐ反対向き。</strong><br>C=Oそれぞれには電荷のかたよりがあっても、左右で打ち消し合うので、分子全体には極性がありません。',
    BF3: '<strong>電子対が3組だけ。</strong><br>3組がいちばん離れる向きは平面の120°。ホウ素は外側の電子が少ない原子です。',
    SF6: '<strong>6組が押し合うと正八面体。</strong><br>上下・左右・前後の6方向に、90°ずつ並びます。',
  }[cur];
  window.SHARE = M.name + 'の形は「' + M.shape + '」、結合角は' + M.ang + '°⚛️\n分子の形を3Dでくるくる回して見られる👇';
}
$('mols').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; cur = b.dataset.m; $('mols').querySelectorAll('button').forEach(x => x.classList.toggle('on', x === b)); build(); });
$('lp').addEventListener('change', build); $('fill').addEventListener('change', build);
v.onFrame((t, dt) => { if ($('spin').checked) root.rotation.y += dt * 0.4; });
$('hud').innerHTML = '<span style="font-size:12px">⚪H ⚫C 🔵N 🔴O 🟢F 🌸B 🟡S ・ 紫＝非共有電子対</span>';
build();
