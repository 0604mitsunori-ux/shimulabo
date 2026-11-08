import { THREE, createView, mat, water, animNum } from '../../assets/three/sim3d.js';
const $ = id => document.getElementById(id);
// 単位は m。z＋が湖（上流）。アーチの中心は下流側 (0,0,-200)、半径300〜318m
const RC = 200, R1 = 300, R2 = 318, TH = 0.66, HDAM = 186;
const v = createView($('view'), {
  views: { down: { tgt: [0, 90, 60], dist: 820, th: Math.PI - 0.15, ph: 0.3 }, up: { tgt: [0, 90, 60], dist: 900, th: 0.3, ph: 0.4 }, side: { tgt: [0, 90, 60], dist: 560, th: Math.PI / 2, ph: 0.05 } },
  camRow: '#camRow', far: 8000, fog: [1800, 4200], minDist: 120, maxDist: 3000,
});
const { scene, sun } = v;
sun.position.set(-400, 700, -300); sun.shadow.camera.left = -700; sun.shadow.camera.right = 700; sun.shadow.camera.top = 700; sun.shadow.camera.bottom = -700; sun.shadow.camera.far = 3000;
// 谷（V字の岩壁と谷底）を断面の形で押し出す
const rock = mat(0x9c9486, { roughness: 1, flatShading: true }), rock2 = mat(0x8a8275, { roughness: 1, flatShading: true });
function wall(sign) {
  const s = new THREE.Shape();
  const P = [[30, -10], [200, 215], [900, 260], [900, -10]];
  P.forEach(([x, y], i) => i ? s.lineTo(sign * x, y) : s.moveTo(sign * x, y));
  const g = new THREE.ExtrudeGeometry(s, { depth: 2200, bevelEnabled: false });
  const m = new THREE.Mesh(g, sign > 0 ? rock : rock2); m.position.z = -900; m.castShadow = m.receiveShadow = true; scene.add(m);
  return m;
}
const wR = wall(1), wL = wall(-1);
// カメラが横（岩の中）に入るときは、谷の真ん中で切った断面を見せる
const cutR = new THREE.Plane(new THREE.Vector3(-1, 0, 0), -6), cutL = new THREE.Plane(new THREE.Vector3(1, 0, 0), -6);
v.onFrame(() => { const c = v.camera.position; v.renderer.clippingPlanes = (c.x > 150 && c.y < 300) ? [cutR] : (c.x < -150 && c.y < 300) ? [cutL] : []; });
const floor = new THREE.Mesh(new THREE.BoxGeometry(1800, 20, 2200), rock2); floor.position.set(0, -20, 200); floor.receiveShadow = true; scene.add(floor);
// 下流の川
const river = new THREE.Mesh(new THREE.BoxGeometry(50, 2, 900), water(0.7, 0x5a9fd6)); river.position.set(0, -8, -650); scene.add(river);
// アーチダム（輪の一部を押し出す）。下へ行くほど厚い
function arch(r1, r2, t0, t1) {
  const s = new THREE.Shape(); const n = 48;
  for (let i = 0; i <= n; i++) { const a = t0 + (t1 - t0) * i / n; const x = r2 * Math.sin(a), z = r2 * Math.cos(a) - RC; i ? s.lineTo(x, z) : s.moveTo(x, z); }
  for (let i = n; i >= 0; i--) { const a = t0 + (t1 - t0) * i / n; s.lineTo(r1 * Math.sin(a), r1 * Math.cos(a) - RC); }
  return s;
}
const concrete = mat(0xdcd8cf, { roughness: 0.9 });
const dam = new THREE.Group(); scene.add(dam);
for (let k = 0; k < 6; k++) {   // 6段で厚さを変える
  const y0 = HDAM * k / 6, y1 = HDAM * (k + 1) / 6, th = 40 - 30 * (k / 5);
  const g = new THREE.ExtrudeGeometry(arch(R2 - th, R2, -TH - 0.3, TH + 0.3), { depth: y1 - y0, bevelEnabled: false });
  g.rotateX(Math.PI / 2); g.translate(0, y1, 0);
  const m = new THREE.Mesh(g, concrete); m.castShadow = m.receiveShadow = true; dam.add(m);
}
// 湖（アーチの外側から上流へ）
const ws = new THREE.Shape(); { const n = 48;
  for (let i = 0; i <= n; i++) { const a = -TH - 0.3 + (2 * TH + 0.6) * i / n; const x = R2 * Math.sin(a), z = R2 * Math.cos(a) - RC; i ? ws.lineTo(x, z) : ws.moveTo(x, z); }
  ws.lineTo(900, 1300); ws.lineTo(-900, 1300); }
const wg = new THREE.ExtrudeGeometry(ws, { depth: 1, bevelEnabled: false }); wg.rotateX(Math.PI / 2); wg.translate(0, 1, 0);
const lake = new THREE.Mesh(wg, water(0.62, 0x3f86c8)); scene.add(lake);
// 水圧の矢印（アーチの頂点の上流側の面、深さに比例）
const arrows = [];
const aMat = new THREE.MeshStandardMaterial({ color: 0x1f6fc2, emissive: 0x1f6fc2, emissiveIntensity: 0.35 });
for (let i = 0; i < 9; i++) {
  const g = new THREE.Group();
  const shaft = new THREE.Mesh(new THREE.CylinderGeometry(2.6, 2.6, 1, 12), aMat); shaft.rotation.x = Math.PI / 2; g.add(shaft);
  const head = new THREE.Mesh(new THREE.ConeGeometry(7, 16, 16), aMat); head.rotation.x = -Math.PI / 2; g.add(head);
  scene.add(g); arrows.push({ g, shaft, head });
}
const probe = new THREE.Mesh(new THREE.SphereGeometry(7, 20, 14), new THREE.MeshStandardMaterial({ color: 0xd6352b, emissive: 0xd6352b, emissiveIntensity: 0.3 })); scene.add(probe);
const zFace = R2 - RC + 4;
v.label('黒部ダム（堤高186m）', [0, HDAM + 20, zFace - 30], { accent: true });
const lbLake = v.label('黒部湖', [-120, 160, 600]);
const lbProbe = v.label('', [0, 0, 0]);

function lab() { $('lvL').textContent = $('lv').value + ' m'; $('dpL').textContent = $('dp').value + ' m'; }
function update() {
  let lv = +$('lv').value, dp = +$('dp').value;
  if (dp > lv) { dp = lv; $('dp').value = dp; }
  lab();
  lake.scale.y = Math.max(0.01, lv); lake.visible = lv > 0.5;
  lbLake.at(-120, lv + 10, 600);
  arrows.forEach((a, i) => {
    const y = lv * (i + 0.5) / arrows.length, d = lv - y, L = Math.max(0.01, d * 0.9);
    a.g.visible = lv > 2; a.shaft.scale.y = L; a.shaft.position.z = L / 2 + 14; a.head.position.z = 6;
    a.g.position.set(-14, y, zFace);
  });
  probe.position.set(-14, lv - dp, zFace + 8); probe.visible = lv > 0;
  lbProbe.at(-14, lv - dp, zFace + 8); lbProbe.set('深さ ' + dp + 'm');
  const kgcm = dp * 0.1, mpa = dp * 9.81 / 1000;
  animNum($('big'), +($('big').textContent) || 0, kgcm, 400, 1);
  $('sub').textContent = '水位 ' + lv + 'm の湖で、水面から ' + dp + 'm の深さ';
  $('sP').textContent = mpa.toFixed(2) + ' MPa';
  $('sTatami').textContent = '約 ' + Math.round(kgcm * 16200 / 1000).toLocaleString() + ' トン';
  $('sAtm').textContent = '約 ' + (mpa / 0.101325).toFixed(1) + ' 倍';
  $('hud').innerHTML = '水位 <b>' + lv + '</b> m<br>底の水圧 <b>' + (lv * 0.1).toFixed(1) + '</b> kg/cm²';
  $('resNote').innerHTML = dp >= 150 ? '<strong>深さ' + dp + 'mでは、指先に約' + Math.round(kgcm) + 'kg。</strong><br>小学生1人分ほどの重さが、指先の面積だけにかかっている計算です。ダムの下ほど壁が厚いのはこのためです。'
    : dp >= 50 ? '<strong>深さ' + dp + 'mで、1cm²あたり約' + kgcm.toFixed(1) + 'kg。</strong><br>深さが2倍になると、水圧も2倍になります。'
    : '<strong>浅いところの水圧はまだ小さめ。</strong><br>スライダーで深くすると、矢印の長さ（水圧）がまっすぐ比例して伸びます。';
  window.SHARE = '黒部ダムの水深' + dp + 'mの水圧は、指先1cm²に約' + kgcm.toFixed(1) + 'kg🏞️\n3Dでダムに水をためて試せる👇';
}
$('lv').addEventListener('input', update); $('dp').addEventListener('input', update);
update();
