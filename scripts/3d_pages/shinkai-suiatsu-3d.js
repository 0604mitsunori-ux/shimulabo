import { THREE, createView, mat, animNum } from '../../assets/three/sim3d.js';
const $ = id => document.getElementById(id);
// 深さ（m）→ 画面の高さ。浅いところを広く見せるため対数の目盛り（深さ0で y=0、1万mで約 -240）
const Y = d => -60 * Math.log10(1 + d / 10);
const MAXD = 10900;
const sl2d = s => Math.round((Math.pow(10, s / 1000 * Math.log10(1 + MAXD / 10)) - 1) * 10); // スライダー0〜1000 → 深さ
const d2sl = d => Math.round(Math.log10(1 + d / 10) / Math.log10(1 + MAXD / 10) * 1000);
const v = createView($('view'), {
  views: { follow: { tgt: [0, 0, 0], dist: 70, th: 0.6, ph: 0.12 }, wide: { tgt: [0, -120, 0], dist: 420, th: 0.6, ph: 0.05 } },
  camRow: '#camRow', bg: 0x9fd0ee, shadows: false, minDist: 20, maxDist: 900,
});
const { scene } = v;
v.hemi.intensity = 1.2;
// 海の柱（深さで色が暗くなる）：縦に細かく分けた輪切りを重ねる
const SURF = new THREE.Color(0x4aa3df), DEEP = new THREE.Color(0x02060f);
const colOf = d => SURF.clone().lerp(DEEP, Math.min(1, Math.log10(1 + d / 10) / 2.4));
for (let i = 0; i < 60; i++) {
  const d0 = sl2d(i / 60 * 1000), d1 = sl2d((i + 1) / 60 * 1000);
  const m = new THREE.Mesh(new THREE.BoxGeometry(40, Y(d0) - Y(d1), 40), new THREE.MeshBasicMaterial({ color: colOf((d0 + d1) / 2), transparent: true, opacity: 0.35, depthWrite: false }));
  m.position.y = (Y(d0) + Y(d1)) / 2; scene.add(m);
}
const sea = new THREE.Mesh(new THREE.PlaneGeometry(400, 400), new THREE.MeshBasicMaterial({ color: 0x6fb6e6, transparent: true, opacity: 0.5, side: THREE.DoubleSide }));
sea.rotation.x = -Math.PI / 2; scene.add(sea);
// 目印の深さ
const SPOTS = [[0, '海面', '海面'], [10, '10m（2気圧）', '10m'], [200, '約200m 光がほぼ届かない', '200m'], [3346, '3,346m タイタン最後の位置', 'タイタン'], [3840, '3,840m タイタニック号', 'タイタニック号'], [6500, '6,500m しんかい6500', 'しんかい6500'], [10900, '約10,900m マリアナ海溝', 'マリアナ海溝']];
for (const [d, t] of SPOTS) {
  const ring = new THREE.Mesh(new THREE.BoxGeometry(41, 0.3, 41), new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.5 }));
  ring.position.y = Y(d); scene.add(ring);
  v.label(t, [20, Y(d), 20], { sub: d === 10 || d === 3346 });
}
$('spots').innerHTML = SPOTS.map(([d, , s]) => '<button data-d="' + d + '">' + s + '</button>').join('');
// 風船（ボイルの法則で縮む）と、比べるための「元の大きさ」の輪
const balloon = new THREE.Mesh(new THREE.SphereGeometry(6, 40, 30), mat(0xd6352b, { roughness: 0.35, emissive: 0x401010 }));
scene.add(balloon);
const ghost = new THREE.Mesh(new THREE.SphereGeometry(6, 40, 30), new THREE.MeshBasicMaterial({ color: 0xffffff, wireframe: true, transparent: true, opacity: 0.25 }));
scene.add(ghost);
const knot = new THREE.Mesh(new THREE.ConeGeometry(0.8, 1.6, 12), mat(0xb02a22)); scene.add(knot);
const lb = v.label('', [0, 0, 0], { accent: true });

function update(fromSlider = true) {
  const d = sl2d(+$('d').value);
  const atm = 1 + d / 10, vol = 1 / atm, s = Math.cbrt(vol);
  const y = Y(d);
  balloon.position.set(0, y + 6, 0); balloon.scale.setScalar(Math.max(s, 0.06));
  ghost.position.copy(balloon.position);
  knot.position.set(0, y + 6 - 6 * Math.max(s, 0.06) - 0.6, 0);
  lb.at(0, y + 6 + 6 * Math.max(s, 0.06) + 1, 0); lb.set('深さ ' + d.toLocaleString() + 'm');
  v.scene.background = colOf(d).lerp(new THREE.Color(0x000000), 0.15);
  $('dL').textContent = d.toLocaleString() + ' m';
  animNum($('big'), parseFloat(($('big').textContent || '0').replace(/,/g, '')) || 0, atm, 400, atm < 100 ? 1 : 0);
  $('sub').textContent = '深さ ' + d.toLocaleString() + 'm（水面の大気圧1気圧を含む・目安）';
  const kg = atm * 1.0;
  $('sKg').textContent = kg >= 1000 ? '約' + (kg / 1000).toFixed(2) + 'トン' : '約' + (kg < 100 ? kg.toFixed(1) : Math.round(kg)) + 'kg';
  $('sVol').textContent = vol >= 0.1 ? Math.round(vol * 100) + '%（' + (1 / vol).toFixed(1) + '分の1）' : (1 / vol).toFixed(0) + '分の1';
  $('sLight').textContent = d < 200 ? 'まだ届く' : d < 1000 ? 'ほとんど届かない' : 'まっ暗（届かない）';
  $('hud').innerHTML = '深さ <b>' + d.toLocaleString() + '</b> m<br>水圧 <b>' + (atm < 100 ? atm.toFixed(1) : Math.round(atm)) + '</b> 気圧';
  const near = SPOTS.filter(([sd]) => sd <= d).pop();
  $('resNote').innerHTML = d >= 10000 ? '<strong>世界一深い海の底、指先に約1トン。</strong><br>軽自動車が指先に乗っているほどの重さです。風船の空気は約' + Math.round(atm) + '分の1まで押し縮められます。'
    : d >= 3000 ? '<strong>' + near[2] + 'のあたり。指先に約' + Math.round(kg) + 'kg。</strong><br>深い海で人が乗る耐圧殻は、圧力を均等に受けられる球の形がふつうです。'
    : d >= 10 ? '<strong>' + d + 'mで' + atm.toFixed(1) + '気圧。</strong><br>風船の体積は' + Math.round(vol * 100) + '%に。素潜りで耳が痛くなるのも、この圧力の差のせいです。'
    : '<strong>水面近く。</strong><br>たった10m潜るだけで、空気の量は半分に押し縮められます。スライダーを右へ動かしてみてください。';
  window.SHARE = '深さ' + d.toLocaleString() + 'mの水圧は約' + Math.round(atm).toLocaleString() + '気圧、指先1cm²に' + $('sKg').textContent + '🌊\n風船がどこまで縮むか3Dで見られる👇';
}
// 「潜る風船を追う」のときはカメラが風船についていく
v.onFrame(() => { if (document.querySelector('#camRow .on')?.dataset.v === 'follow') v.goal.tgt.y = balloon.position.y; });
$('d').addEventListener('input', () => update());
$('spots').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; $('d').value = d2sl(+b.dataset.d); update(); });
update();
