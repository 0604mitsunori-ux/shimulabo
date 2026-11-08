import { THREE, createView, mat, water } from '../../assets/three/sim3d.js';
const $ = id => document.getElementById(id);
const v = createView($('view'), {
  views: { persp: { tgt: [2, 4, 0], dist: 46, th: 0.55, ph: 0.25 }, front: { tgt: [2, 5, 0], dist: 42, th: 0, ph: 0.02 }, low: { tgt: [2, 3, 0], dist: 22, th: 0.35, ph: 0.02 } },
  camRow: '#camRow', bg: 0xe3ebf1, minDist: 6, maxDist: 160,
});
const { scene, sun } = v;
sun.position.set(-30, 50, 40); Object.assign(sun.shadow.camera, { left: -40, right: 40, top: 40, bottom: -40 }); sun.shadow.camera.updateProjectionMatrix();
const ground = new THREE.Mesh(new THREE.PlaneGeometry(200, 200), mat(0xc5ccb6, { roughness: 1 })); ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true; scene.add(ground);
const road = new THREE.Mesh(new THREE.PlaneGeometry(200, 6), mat(0x9a9a96, { roughness: 1 })); road.rotation.x = -Math.PI / 2; road.position.set(0, 0.01, 9); road.receiveShadow = true; scene.add(road);
const box = (w, h, d, m, x, y, z, p = scene) => { const o = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), m); o.position.set(x, y, z); o.castShadow = o.receiveShadow = true; p.add(o); return o; };
// 2階建ての家（手前の壁を外した断面の模型。床の高さ：1階0.5m・2階3m）
const wall = mat(0xf2ede2), floorM = mat(0xc89b6a), roofM = mat(0x5b6670), inner = mat(0xe9e2d2);
const HX = -4;
box(9, 0.5, 8, mat(0xb9b2a3), HX, 0.25, 0);          // 基礎
box(9, 0.15, 8, floorM, HX, 0.55, 0);                // 1階の床
box(9, 0.3, 8, floorM, HX, 3.0, 0);                  // 2階の床
box(9, 5.5, 0.2, wall, HX, 2.75 + 0.5, -4);           // 奥の壁
box(0.2, 5.5, 8, wall, HX - 4.5, 3.25, 0); box(0.2, 5.5, 8, wall, HX + 4.5, 3.25, 0);
box(9, 0.2, 8, inner, HX, 6.0, 0);                   // 天井
const roof = new THREE.Mesh(new THREE.CylinderGeometry(0.01, 6.6, 2.2, 4, 1), roofM); roof.rotation.y = Math.PI / 4; roof.scale.set(1, 1, 0.9); roof.position.set(HX, 7.2, 0); roof.castShadow = true; scene.add(roof);
// 家具（目安）
box(2, 0.8, 0.9, mat(0x8a6b4f), HX - 2, 1.0, -2.5); box(1.2, 1.8, 0.6, mat(0x8a6b4f), HX + 2.5, 1.5, -3.4);
box(2, 0.5, 1.4, mat(0x9fb6d0), HX - 1.5, 3.4, -2.5);
// 人（170cm）と車
const person = new THREE.Group(); scene.add(person); person.position.set(4, 0, 5);
box(0.45, 1.25, 0.3, mat(0x2f7fc8), 0, 0.62, 0, person); const head = new THREE.Mesh(new THREE.SphereGeometry(0.2, 16, 12), mat(0xf1c9a5)); head.position.y = 1.5; head.castShadow = true; person.add(head);
const car = new THREE.Group(); scene.add(car); car.position.set(9, 0, 9);
box(4.5, 0.9, 1.75, mat(0xd6352b), 0, 0.65, 0, car); box(2.4, 0.6, 1.6, mat(0x3a4450), -0.2, 1.4, 0, car);
[[-1.5, 0.85], [1.5, 0.85], [-1.5, -0.85], [1.5, -0.85]].forEach(([x, z]) => { const w = new THREE.Mesh(new THREE.CylinderGeometry(0.33, 0.33, 0.2, 16), mat(0x222222)); w.rotation.x = Math.PI / 2; w.position.set(x, 0.33, z); car.add(w); });
// 5階建てのマンション（1階＝約3m）
for (let f = 0; f < 6; f++) box(7, f === 5 ? 0.4 : 0.3, 7, mat(0xcfd4d8), 14, 3 * f + 0.15, -5);
for (let f = 0; f < 5; f++) box(7, 2.7, 0.2, mat(0xe6e9ec), 14, 3 * f + 1.65, -8.4);
box(0.2, 15, 7, mat(0xe6e9ec), 10.5, 7.5, -5); box(0.2, 15, 7, mat(0xe6e9ec), 17.5, 7.5, -5);
// 目盛りの柱
for (let m = 0; m <= 20; m++) { const t = box(0.12, 0.02, 0.6, mat(m % 5 ? 0x7d8590 : 0x22262b), -17, m, 6); }
box(0.08, 20, 0.08, mat(0x22262b), -17, 10, 6);
[0.5, 3, 5, 10, 20].forEach(m => v.label(m + 'm', [-17, m, 6], { sub: m === 20 }));
v.label('1階の床 0.5m', [HX + 3, 0.6, 4], { sub: true }); v.label('2階の床 3m', [HX + 3, 3.1, 4]);
v.label('5階建て（1階＝約3m）', [14, 15.5, -5], { sub: true });
// 水
const W = new THREE.Mesh(new THREE.BoxGeometry(80, 1, 60), water(0.5, 0x4f7fb0)); W.position.y = 0.5; scene.add(W);
const lb = v.label('', [0, 0, 12], { accent: true });
const BANDS = [[0.5, '0.5m未満', '黄色', '#f7f5a9'], [3, '0.5〜3m', 'うすいピンク', '#ffd8c0'], [5, '3〜5m', 'ピンク', '#ffb7b7'], [10, '5〜10m', '濃いピンク', '#ff9191'], [20, '10〜20m', '赤紫', '#f285c9'], [1e9, '20m以上', '紫', '#dc7adc']];
$('levels').innerHTML = [[0.5, '0.5m'], [1, '1m'], [3, '3m'], [5, '5m'], [10, '10m']].map(([d, t]) => '<button data-d="' + d + '">' + t + '</button>').join('');
function update() {
  const d = +$('d').value;
  $('dL').textContent = d.toFixed(1) + ' m';
  W.scale.y = Math.max(0.001, d); W.position.y = d / 2; W.visible = d > 0.01;
  lb.at(0, d + 0.2, 12); lb.set('浸水 ' + d.toFixed(1) + 'm');
  const b = BANDS.find(x => d < x[0]);
  $('big').textContent = d.toFixed(1);
  $('sub').textContent = 'ハザードマップの区分：' + b[1];
  $('sHouse').textContent = d < 0.5 ? '床下浸水' : d < 3 ? '1階が床上浸水' : d < 5 ? '2階の床まで' : d < 7.5 ? '2階まで水没' : '屋根までのみこまれる';
  $('sPerson').textContent = d < 0.5 ? 'ひざより下' : d < 1.0 ? '腰のあたり' : d < 1.4 ? '胸のあたり' : d < 1.7 ? '首のあたり' : '頭の上まで';
  $('sColor').innerHTML = '<span style="display:inline-block;width:14px;height:14px;border:1px solid #aaa;vertical-align:-2px;background:' + b[3] + '"></span> ' + b[2];
  $('hud').innerHTML = '浸水 <b>' + d.toFixed(1) + '</b> m<br><span style="font-size:11.5px">' + b[1] + '（' + b[2] + '）</span>';
  $('resNote').innerHTML = d >= 5 ? '<strong>2階建ての家は2階まで水につかる深さ。</strong><br>自宅の2階へ逃げても安全ではありません。浸水が始まる前に、指定された避難場所や、もっと高い建物へ移動することが必要です。'
    : d >= 3 ? '<strong>2階の床まで水が来る深さ。</strong><br>「2階へ逃げる」では足りないことがあります。早めの避難を考えておきましょう。'
    : d >= 0.5 ? '<strong>1階が床上浸水する深さ。</strong><br>流れがあると大人でも歩いて逃げるのは危険です。車は浸水した道を走らないでください。'
    : '<strong>床下浸水の深さ。</strong><br>浅く見えても、水の流れや見えない側溝で足を取られることがあります。';
  window.SHARE = 'ハザードマップの「浸水' + d.toFixed(1) + 'm」は、2階建ての家だと「' + $('sHouse').textContent + '」🏠\n3Dの家に水を入れて確かめられる👇';
}
$('d').addEventListener('input', update);
$('levels').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; $('d').value = b.dataset.d; update(); });
update();
