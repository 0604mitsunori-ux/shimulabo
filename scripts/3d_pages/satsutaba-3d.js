import { THREE, createView, mat } from '../../assets/three/sim3d.js';
const $ = id => document.getElementById(id);
// 単位 cm。100万円の束＝16×7.6×1cm（1万円札100枚・約100g）
const BW = 16, BD = 7.6, BH = 1;
const v = createView($('view'), {
  views: { persp: { tgt: [0, 20, 0], dist: 260, th: 0.45, ph: 0.5 }, front: { tgt: [0, 50, 0], dist: 300, th: 0, ph: 0.05 }, top: { tgt: [0, 0, 0], dist: 300, th: 0, ph: 1.45 } },
  camRow: '#camRow', bg: 0xf3f1ea, minDist: 20, maxDist: 6000, far: 30000,
});
const { scene, sun } = v;
sun.position.set(-300, 600, 400); Object.assign(sun.shadow.camera, { left: -400, right: 400, top: 400, bottom: -400, far: 3000 }); sun.shadow.camera.updateProjectionMatrix();
const floor = new THREE.Mesh(new THREE.PlaneGeometry(20000, 20000), mat(0xd9d2c3, { roughness: 1 })); floor.rotation.x = -Math.PI / 2; floor.receiveShadow = true; scene.add(floor);
const MAXB = 10000;
const bundles = new THREE.InstancedMesh(new THREE.BoxGeometry(BW, BH * 0.98, BD), mat(0xcfc7a0, { roughness: 0.9 }), MAXB);
const bands = new THREE.InstancedMesh(new THREE.BoxGeometry(3.2, BH * 1.0, BD + 0.08), mat(0xf6f3ea, { roughness: 0.8 }), MAXB);
bundles.castShadow = bundles.receiveShadow = true; scene.add(bundles); scene.add(bands);
const loose = new THREE.Mesh(new THREE.BoxGeometry(BW, 1, BD), mat(0xd8d0a8)); loose.castShadow = true; scene.add(loose);
// 比べるもの：人（170cm）と2Lペットボトル
const person = new THREE.Group(); scene.add(person);
{ const b = new THREE.Mesh(new THREE.BoxGeometry(45, 125, 28), mat(0x2f7fc8)); b.position.y = 62; b.castShadow = true; person.add(b);
  const h = new THREE.Mesh(new THREE.SphereGeometry(20, 20, 16), mat(0xf1c9a5)); h.position.y = 150; h.castShadow = true; person.add(h); }
const bottle = new THREE.Mesh(new THREE.CylinderGeometry(5, 5, 31, 20), new THREE.MeshStandardMaterial({ color: 0x9fd0ee, transparent: true, opacity: 0.6, roughness: 0.2 })); bottle.castShadow = true; scene.add(bottle);
const lP = v.label('身長170cm', [0, 175, 0]), lB = v.label('2Lペットボトル', [0, 35, 0], { sub: true }), lS = v.label('', [0, 0, 0], { accent: true });
const AMTS = [[1e6, '100万円'], [1e7, '1,000万円'], [1e8, '1億円'], [1e9, '10億円']];
$('amts').innerHTML = AMTS.map(([a, t]) => '<button data-a="' + a + '"' + (a === 1e8 ? ' class="on"' : '') + '>' + t + '</button>').join('');
const yen = n => n >= 1e8 ? (n / 1e8).toLocaleString(undefined, { maximumFractionDigits: 4 }) + '億円' : n >= 1e4 ? (n / 1e4).toLocaleString() + '万円' : n + '円';
function update() {
  let amt = Math.max(0, Math.floor((+$('amt').value || 0) / 1e4) * 1e4);
  const notes = amt / 1e4, nb = Math.floor(notes / 100), rest = notes % 100;
  const shown = Math.min(nb, MAXB);
  // 並べ方：1段＝横2×奥5の10束、50段（50cm）ごとに山を増やして格子に並べる
  const PER = 10, LAY = 50, SX = BW * 2 + 6, SZ = BD * 5 + 6;
  const piles = Math.max(1, Math.ceil(shown / (PER * LAY))), cols = Math.ceil(Math.sqrt(piles));
  const m = new THREE.Matrix4();
  for (let i = 0; i < shown; i++) {
    const pile = Math.floor(i / (PER * LAY)), inP = i % (PER * LAY), lay = Math.floor(inP / PER), j = inP % PER;
    const px = (pile % cols) * SX - (cols - 1) * SX / 2, pz = Math.floor(pile / cols) * SZ - (Math.ceil(piles / cols) - 1) * SZ / 2;
    const x = px + (j % 2 - 0.5) * (BW + 0.4), z = pz + (Math.floor(j / 2) - 2) * (BD + 0.4), y = lay * BH + BH / 2;
    m.makeTranslation(x, y, z); bundles.setMatrixAt(i, m); bands.setMatrixAt(i, m);
  }
  bundles.count = shown; bands.count = shown; bundles.instanceMatrix.needsUpdate = true; bands.instanceMatrix.needsUpdate = true;
  const span = Math.max(SX * cols, 40), topY = Math.min(shown, PER * LAY) / PER * BH;
  loose.visible = rest > 0; loose.scale.y = Math.max(0.01, rest / 100); loose.position.set(span / 2 + 20, rest / 200, 0);
  person.position.set(-span / 2 - 110, 0, -150); bottle.position.set(-span / 2 - 12, 15.5, 25);
  lP.at(-span / 2 - 110, 175, -150); lB.at(-span / 2 - 12, 34, 25); lS.at(0, Math.max(topY, 2) + 6, 0); lS.set(yen(amt));
  const fit = Math.max(span * 1.2, 220);
  Object.assign(v.views.persp, { tgt: [-span * 0.15, 60, -10], dist: fit * 1.5 }); Object.assign(v.views.front, { tgt: [-span * 0.1, 60, 0], dist: fit * 1.2 }); Object.assign(v.views.top, { dist: fit * 1.4 });
  v.setView(document.querySelector('#camRow .on')?.dataset.v || 'persp');
  const kg = notes / 1000, hM = notes * 0.01 / 100, L = notes * BW * BD * 0.01 / 1000;
  $('big').textContent = kg >= 100 ? Math.round(kg).toLocaleString() : kg.toFixed(kg < 1 ? 2 : 1);
  $('sub').textContent = yen(amt) + '（1万円札 ' + notes.toLocaleString() + '枚）';
  $('sBundles').textContent = nb.toLocaleString() + ' 束' + (rest ? '＋' + rest + '枚' : '');
  $('sHeight').textContent = hM >= 1 ? '約 ' + hM.toLocaleString(undefined, { maximumFractionDigits: 1 }) + ' m' : '約 ' + (hM * 100).toFixed(1) + ' cm';
  $('sVolume').textContent = '約 ' + (L >= 10 ? Math.round(L).toLocaleString() : L.toFixed(1)) + ' L';
  $('hud').innerHTML = yen(amt) + '<br><b>' + $('big').textContent + '</b> kg' + (nb > MAXB ? '<br><span style="font-size:11px">※3Dは100億円分まで表示</span>' : '');
  $('resNote').innerHTML = amt >= 1e9 ? '<strong>' + yen(amt) + 'は約' + Math.round(kg).toLocaleString() + 'kg。</strong><br>大人1人ではとても運べない重さです。1列に積むと約' + hM.toLocaleString(undefined, { maximumFractionDigits: 1 }) + 'mにもなります。'
    : amt >= 1e8 ? '<strong>' + yen(amt) + 'は約' + kg.toFixed(1) + 'kg、体積は約' + Math.round(L) + 'L。</strong><br>1億円で2Lペットボトル6本分ほど。機内持ち込みサイズのスーツケースに入る大きさです。'
    : '<strong>' + yen(amt) + 'は約' + (kg < 1 ? Math.round(kg * 1000) + 'g' : kg.toFixed(1) + 'kg') + '。</strong><br>100万円の束は厚さ約1cm。金額を増やして、札束の山を育ててみてください。';
  window.SHARE = yen(amt) + 'を1万円札にすると約' + $('big').textContent + 'kg、積むと' + $('sHeight').textContent + '💴\n札束を3Dで積み上げてみた👇';
}
$('amt').addEventListener('input', update);
$('amts').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; $('amt').value = b.dataset.a; $('amts').querySelectorAll('button').forEach(x => x.classList.toggle('on', x === b)); update(); });
update(); v.setView('persp', true);
