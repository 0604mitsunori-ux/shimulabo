// 舞台「断面」：サッカー場の下の調圧水槽・第1立坑・トンネル・排水機場・江戸川を z=0 で切った模型（単位 m）
// 数字は 01_事実メモ.md。立坑・トンネルの並び、ポンプの配置、地層の色は模式
import { THREE, C, mat } from './stage-lite.js';
import { soilMaterial, waterMaterial, box, halfCylY, halfTubeX, arrow, setArrow, person, sectionFace, extrudeZ, HP, flowDots } from './kit.js';

export const P = {
  X0: -400, X1: 520, Y0: -100, ZB: -160,
  tank: { x0: -88.5, x1: 88.5, y0: -22, y1: -4, zb: -39 },
  shaft: { x: 111, r: 15.8, w: 2.5, y0: -70, y1: -2 },
  tunnel: { y: -50, r: 5.3, x1: 520 },
  pump: { x0: -165.5, x1: -92, y0: -23.6, in0: -18 },
  river: { xl: -345, xr: -260, bed: -9, water: -3.5 },
  culvert: { y0: -9.4, y1: -4.4, x0: -262, x1: -165.5 },
};

export function build(stage) {
  const g = new THREE.Group();
  const T = P.tank, S = P.shaft, TU = P.tunnel, PU = P.pump, R = P.river, CV = P.culvert;
  const soilFace = soilMaterial(1.0), soilSide = soilMaterial(0.84), soilIn = soilMaterial(0.9), soilFront = soilMaterial(0.95);
  const soils = [soilFace, soilSide, soilIn, soilFront];
  const concrete = mat(C.concrete), concreteDark = mat(C.concreteDark), steel = mat(0x8d969e, { metalness: 0.35, roughness: 0.5 });
  const shellMat = mat(C.concrete, { side: THREE.DoubleSide });

  // ---- 土の切り口（くり抜く形） ----
  const SL = S.x - S.r, SR = S.x + S.r;
  sectionFace(g, { x0: P.X0, x1: P.X1, y0: P.Y0, y1: 0 }, [
    { rect: [T.x0, SL, T.y0, T.y1] },                       // 水槽＋立坑への開口
    { rect: [SL, SR, S.y0, S.y1] },                          // 立坑
    { rect: [SR - 1, P.X1 + 1, TU.y - TU.r, TU.y + TU.r] },  // トンネル
    { rect: [PU.x0 + 3.5, PU.x1, PU.in0, -1.2] },            // 排水機場の中
    { rect: [CV.x0, CV.x1 + 3.5, CV.y0 + 0.4, CV.y1 - 0.4] },// 排水樋管の中
    { poly: [[R.xl, 0.2], [R.xr, 0.2], [R.xr - 10, R.bed], [R.xl + 10, R.bed]] }, // 江戸川
  ], soilFace);
  // 土の左右と奥
  for (const [x, ry] of [[P.X0, -HP], [P.X1, HP]]) {
    const m = new THREE.Mesh(new THREE.PlaneGeometry(-P.ZB, -P.Y0), soilSide);
    m.rotation.y = ry; m.position.set(x, P.Y0 / 2, P.ZB / 2); g.add(m);
  }
  // 江戸川の川底と土手の内側（土の色）
  {
    const bed = new THREE.Mesh(new THREE.PlaneGeometry(R.xr - R.xl - 20, -P.ZB), soilIn); bed.rotation.x = -HP; bed.position.set((R.xl + R.xr) / 2, R.bed, P.ZB / 2); g.add(bed);
    for (const [xa, xb] of [[R.xl, R.xl + 10], [R.xr, R.xr - 10]]) {
      const geo = new THREE.BufferGeometry();
      geo.setAttribute('position', new THREE.Float32BufferAttribute([xa, 0, 0, xb, R.bed, 0, xb, R.bed, P.ZB, xa, 0, 0, xb, R.bed, P.ZB, xa, 0, P.ZB], 3));
      geo.computeVertexNormals(); g.add(new THREE.Mesh(geo, soilIn));
    }
  }
  const river = new THREE.Mesh(new THREE.BoxGeometry(R.xr - R.xl - 4, R.water - R.bed, -P.ZB), waterMaterial(0.55, 0x4d8fc4));
  river.position.set((R.xl + R.xr) / 2, (R.water + R.bed) / 2, P.ZB / 2); g.add(river);

  // ---- 地面 ----
  const grass = mat(C.grass, { roughness: 1 });
  for (const [x0, x1] of [[P.X0, R.xl], [R.xr, P.X1]]) {
    const m = new THREE.Mesh(new THREE.PlaneGeometry(x1 - x0, -P.ZB), grass);
    m.rotation.x = -HP; m.position.set((x0 + x1) / 2, 0.05, P.ZB / 2); m.receiveShadow = true; g.add(m);
  }
  // 江戸川の堤防（右岸）
  extrudeZ(g, [[R.xr + 2, 0], [R.xr + 14, 7.5], [R.xr + 34, 7.5], [R.xr + 46, 0]], P.ZB, 0, soilMaterial(1.0), mat(0xbfc8ae, { roughness: 1 }));
  // サッカー場（奥の半分）と立坑の上の広場
  const fieldTex = fieldTexture();
  const field = new THREE.Mesh(new THREE.PlaneGeometry(105, 34), new THREE.MeshStandardMaterial({ map: fieldTex.back, roughness: 1 }));
  field.rotation.x = -HP; field.position.set(0, 0.1, -17); field.receiveShadow = true; g.add(field);
  const plaza = new THREE.Mesh(new THREE.CircleGeometry(19, 64, 0, Math.PI), mat(0xcfccc4, { roughness: 1 }));
  plaza.rotation.x = -HP; plaza.position.set(S.x, 0.12, 0); plaza.receiveShadow = true; g.add(plaza);

  // ---- 調圧水槽 ----
  const ZC = 0.03;
  box(g, -92, SL, -25.5, T.y0, -42.5, ZC, concrete);
  const roof = box(g, -92, SL, T.y1, -0.5, -42.5, ZC, concrete, { cast: false });
  box(g, -92, 92, T.y0, T.y1, -42.5, T.zb, concrete);
  box(g, -92, T.x0, T.y0, T.y1, T.zb, ZC, concrete);
  box(g, T.x1, 92, T.y0, T.y1, T.zb, -15.8, concrete);
  box(g, 92, S.x, T.y0, T.y1, -19.3, -15.8, concrete);
  const pillarMat = mat(C.concrete);
  const pillars = [];
  for (const z of [-10, -27]) for (let k = 0; k < 15; k++) {
    const p = new THREE.Mesh(new THREE.BoxGeometry(2, 18, 7), pillarMat);
    p.position.set(-77 + 11 * k, -13, z); p.castShadow = true; p.receiveShadow = true; g.add(p); pillars.push(p);
  }
  // ---- 第1立坑 ----
  halfCylY(g, S.x, 0, S.r, S.y0, TU.y - TU.r, shellMat);
  halfCylY(g, S.x, 0, S.r, TU.y - TU.r, TU.y + TU.r, shellMat, HP + 0.36, 3 * HP);
  halfCylY(g, S.x, 0, S.r, TU.y + TU.r, T.y0, shellMat);
  halfCylY(g, S.x, 0, S.r, T.y0, T.y1, shellMat, HP, Math.PI);
  halfCylY(g, S.x, 0, S.r, T.y1, S.y1, shellMat);
  box(g, SL - S.w, SL, S.y0 - 6, TU.y - TU.r, -0.4, ZC, concrete); box(g, SL - S.w, SL, TU.y + TU.r, T.y0 - 3.5, -0.4, ZC, concrete);
  box(g, SR, SR + S.w, S.y0 - 6, TU.y - TU.r, -0.4, ZC, concrete); box(g, SR, SR + S.w, TU.y + TU.r, 0, -0.4, ZC, concrete);
  box(g, SL - S.w, SR + S.w, S.y0 - 6, S.y0, -0.4, ZC, concrete); box(g, SL - S.w, SR + S.w, S.y1, 0, -0.4, ZC, concrete);
  for (const y of [S.y0 - 3, S.y1 + 1]) halfCylY(g, S.x, 0, S.r + S.w, y - (y < -10 ? 3 : 1), y + (y < -10 ? 3 : 1), concrete, HP, 3 * HP, false);
  // ---- トンネル ----
  halfTubeX(g, SR, TU.x1, TU.y, TU.r, shellMat);
  box(g, SR, TU.x1, TU.y - TU.r - 0.7, TU.y - TU.r, -0.4, ZC, concreteDark); box(g, SR, TU.x1, TU.y + TU.r, TU.y + TU.r + 0.7, -0.4, ZC, concreteDark);

  // ---- 排水機場（地下の箱・底版5.6m） ----
  const pumpBox = new THREE.Group(); g.add(pumpBox);
  const pumpFloorMat = mat(C.concrete);
  box(pumpBox, PU.x0, PU.x1, PU.y0, PU.in0, -42.5, ZC, pumpFloorMat);       // 底版（最大5.6m）
  box(pumpBox, PU.x0, PU.x1, -1.2, 0, -42.5, ZC, concrete, { cast: false });  // 天井
  box(pumpBox, PU.x0, PU.x1, PU.in0, -1.2, -42.5, -39, concrete);           // 奥
  box(pumpBox, PU.x0, PU.x0 + 3.5, PU.in0, -1.2, -39, ZC, concrete);        // 左
  // 上の建屋（ガスタービン室）
  const hall = new THREE.Group(); g.add(hall);
  box(hall, -162, -100, 0, 0.6, -36, ZC, concreteDark);
  box(hall, -162, -100, 0.6, 11, -36, -35.4, mat(0xe2e0da));
  box(hall, -162, -161.4, 0.6, 11, -35.4, ZC, mat(0xe2e0da));
  box(hall, -100.6, -100, 0.6, 11, -35.4, ZC, mat(0xe2e0da));
  box(hall, -162, -100, 11, 11.6, -36, ZC, mat(0xd2d0ca), { cast: false });
  // ポンプ（見えている2台）・ガスタービン・吐出管
  const pumps = [];
  const turbineMat = mat(0x6f7a84, { metalness: 0.45, roughness: 0.45 }), pumpMat = mat(0x46708f, { metalness: 0.3, roughness: 0.5 });
  for (const z of [-12, -30]) {
    const vol = new THREE.Mesh(new THREE.CylinderGeometry(5.6, 5.6, 4.2, 48), pumpMat); vol.position.set(-130, -14.5, z); vol.castShadow = true; g.add(vol);
    const col = new THREE.Mesh(new THREE.CylinderGeometry(2.2, 2.6, 4, 32), pumpMat); col.position.set(-130, -10.4, z); g.add(col);
    const shaft = new THREE.Mesh(new THREE.CylinderGeometry(0.5, 0.5, 11, 16), steel); shaft.position.set(-130, -3, z); g.add(shaft);
    const gear = new THREE.Mesh(new THREE.BoxGeometry(4, 3, 4), turbineMat); gear.position.set(-130, 2.2, z); gear.castShadow = true; g.add(gear);
    const tb = new THREE.Mesh(new THREE.CylinderGeometry(1.7, 1.7, 13, 32), turbineMat); tb.rotation.z = HP; tb.position.set(-140, 2.6, z); tb.castShadow = true; g.add(tb);
    const ex = new THREE.Mesh(new THREE.CylinderGeometry(1.2, 1.2, 9, 24), turbineMat); ex.position.set(-148, 7, z); g.add(ex);
    const pipe = new THREE.Mesh(new THREE.CylinderGeometry(2.0, 2.0, 30, 24), pumpMat); pipe.rotation.z = HP; pipe.position.set(-150, -12, z); g.add(pipe);
    pumps.push({ vol, tb });
  }
  // 樋管（手前の1本を切って見せる。全6本）
  box(g, CV.x0, CV.x1, CV.y0, CV.y0 + 0.4, -2.7, ZC, concreteDark); box(g, CV.x0, CV.x1, CV.y1 - 0.4, CV.y1, -2.7, ZC, concreteDark);
  box(g, CV.x0, CV.x1, CV.y0, CV.y1, -3.1, -2.7, concreteDark);
  const culvertWater = new THREE.Mesh(new THREE.BoxGeometry(CV.x1 - CV.x0, CV.y1 - CV.y0 - 0.8, 2.6), waterMaterial(0.5)); culvertWater.position.set((CV.x0 + CV.x1) / 2, (CV.y0 + CV.y1) / 2, -1.35); g.add(culvertWater);

  // ---- 水（たまる水・地下水）----
  const tankWater = new THREE.Mesh(new THREE.BoxGeometry(T.x1 - T.x0, 1, -T.zb), waterMaterial(0.5));
  tankWater.position.set(0, T.y0, T.zb / 2); g.add(tankWater);
  const shaftWater = new THREE.Mesh(new THREE.CylinderGeometry(S.r - 0.2, S.r - 0.2, 1, 64, 1, false, HP, Math.PI), waterMaterial(0.5)); shaftWater.position.set(S.x, S.y0, 0); g.add(shaftWater);
  const tunnelWater = new THREE.Mesh(new THREE.CylinderGeometry(TU.r - 0.15, TU.r - 0.15, TU.x1 - SR, 48, 1, false, HP, Math.PI), waterMaterial(0.5));
  tunnelWater.rotation.z = HP; tunnelWater.position.set((SR + TU.x1) / 2, TU.y, 0); g.add(tunnelWater);
  const pumpWater = new THREE.Mesh(new THREE.BoxGeometry(PU.x1 - PU.x0 - 3.5, 1, 39), waterMaterial(0.45)); pumpWater.position.set((PU.x0 + 3.5 + PU.x1) / 2, PU.in0, -19.5); g.add(pumpWater);
  const waters = { tank: tankWater, shaft: shaftWater, tunnel: tunnelWater, pump: pumpWater };
  function setWater(name, level, alpha = 1) {
    const w = waters[name];
    if (name === 'tank') { const h = Math.max(0.01, level - T.y0); w.scale.y = h; w.position.y = T.y0 + h / 2; }
    if (name === 'shaft') { const h = Math.max(0.01, level - S.y0); w.scale.y = h; w.position.y = S.y0 + h / 2; }
    if (name === 'pump') { const h = Math.max(0.01, level - PU.in0); w.scale.y = h; w.position.y = PU.in0 + h / 2; }
    if (name === 'tunnel') { w.scale.y = 1; }
    w.material.opacity = 0.5 * alpha; w.visible = alpha > 0.001;
  }
  for (const n of Object.keys(waters)) setWater(n, -999, 0);

  // ---- 手前の土（最初は地面がつながって見える → 外して断面を見せる）----
  const front = new THREE.Group(); g.add(front);
  const fx0 = -200;
  const blk = new THREE.Mesh(new THREE.BoxGeometry(P.X1 - fx0, -P.Y0, 160), soilFront); blk.position.set((fx0 + P.X1) / 2, P.Y0 / 2, 80); front.add(blk);
  const fGrass = new THREE.Mesh(new THREE.PlaneGeometry(P.X1 - fx0, 160), mat(C.grass, { roughness: 1, transparent: true })); fGrass.rotation.x = -HP; fGrass.position.set((fx0 + P.X1) / 2, 0.05, 80); fGrass.receiveShadow = true; front.add(fGrass);
  const fField = new THREE.Mesh(new THREE.PlaneGeometry(105, 34), new THREE.MeshStandardMaterial({ map: fieldTex.front, roughness: 1, transparent: true })); fField.rotation.x = -HP; fField.position.set(0, 0.1, 17); fField.receiveShadow = true; front.add(fField);
  const fPlaza = new THREE.Mesh(new THREE.CircleGeometry(19, 64, Math.PI, Math.PI), mat(0xcfccc4, { roughness: 1, transparent: true })); fPlaza.rotation.x = -HP; fPlaza.position.set(S.x, 0.12, 0); fPlaza.receiveShadow = true; front.add(fPlaza);
  const frontMats = [soilFront, fGrass.material, fField.material, fPlaza.material];
  function setFront(k, alpha) {
    front.position.set(0, -25 * k, 70 * k);
    for (const m of frontMats) { if (m.uniforms) m.uniforms.uAlpha.value = alpha; else m.opacity = alpha; }
    front.visible = alpha > 0.001;
  }
  // 人（サッカー場・水槽の中の目安）
  const people = [person(g, -20, 0.1, -12), person(g, 14, 0.1, -20, 0xd6352b), person(g, -3, 0.1, -26, 0x2f7fc8), person(g, 30, 0.1, -8, 0xe0a030)];
  const pinside = person(g, -60.5, T.y0, -6, 0xd6352b);

  // ---- 矢印（浮く力・重さ）----
  const AX = [-70, -35, 0, 35, 70];
  const up = AX.map(() => arrow(g, 0x2f7fc8)), down = AX.map(() => { const a = arrow(g, C.red); a.rotation.z = Math.PI; return a; });
  function setForces(t, ua, da) {
    up.forEach((a, i) => { a.position.set(AX[i], -44 + 3 * ((t * 0.8 + i * 0.2) % 1.5) / 1.5, 4); setArrow(a, ua); });
    down.forEach((a, i) => { a.position.set(AX[i], 18 - 3 * ((t * 0.8 + i * 0.2) % 1.5) / 1.5, 4); setArrow(a, da); });
  }
  // ---- 地下連続壁（深さ52m）と井戸 ----
  const wallMat = new THREE.MeshStandardMaterial({ color: C.red, transparent: true, opacity: 0, roughness: 0.6 });
  const dwall = [box(g, -94, -93, -52, 0, -44, 0.2, wallMat, { cast: false }), box(g, 93, 94, -52, 0, -44, -16, wallMat, { cast: false })];
  const wellMat = new THREE.MeshStandardMaterial({ color: 0x2f7fc8, transparent: true, opacity: 0 });
  const wells = [-70, -35, 0, 35, 70].map(x => { const m = new THREE.Mesh(new THREE.CylinderGeometry(0.8, 0.8, 45, 12), wellMat); m.position.set(x, -20, -22); g.add(m); return m; });
  function setWalls(a, w) { wallMat.opacity = 0.85 * a; dwall.forEach(m => m.visible = a > 0.001); wellMat.opacity = w; wells.forEach(m => m.visible = w > 0.001); }
  // ---- 壁の切断（ワイヤーソー）：立坑と水槽のあいだの壁 ----
  const panelMat = new THREE.MeshStandardMaterial({ color: 0xcfc6b8, transparent: true, opacity: 0, roughness: 0.9 });
  const panel = new THREE.Mesh(new THREE.BoxGeometry(2.1, T.y1 - T.y0, 15.8), panelMat); panel.position.set(SL - 1.05, (T.y0 + T.y1) / 2, -7.9); g.add(panel);
  const saw = new THREE.Mesh(new THREE.SphereGeometry(0.9, 16, 12), new THREE.MeshBasicMaterial({ color: 0xffd23f })); g.add(saw);
  function setPanel(alpha, cut) {
    panelMat.opacity = alpha; panel.visible = alpha > 0.001; saw.visible = cut > 0 && cut < 1 && alpha > 0.5;
    // 切る線：上辺→奥の辺→下辺 を cut(0〜1) でたどる
    const L1 = 15.8, L2 = T.y1 - T.y0, L3 = 15.8, tot = L1 + L2 + L3; let s = cut * tot;
    if (s < L1) saw.position.set(SL - 1.05, T.y1, -s);
    else if (s < L1 + L2) saw.position.set(SL - 1.05, T.y1 - (s - L1), -15.8);
    else saw.position.set(SL - 1.05, T.y0, -15.8 + (s - L1 - L2));
  }
  setPanel(0, 0); setWalls(0, 0);
  // 水の流れの粒（トンネル→立坑→水槽→ポンプ→樋管→江戸川）
  const path = new THREE.CatmullRomCurve3([
    new THREE.Vector3(300, TU.y, -1), new THREE.Vector3(SR + 2, TU.y, -1), new THREE.Vector3(S.x, TU.y + 2, -6), new THREE.Vector3(S.x - 4, T.y0 + 3, -8),
    new THREE.Vector3(60, T.y0 + 2, -4), new THREE.Vector3(-40, T.y0 + 2, -4), new THREE.Vector3(-90, T.y0 + 2, -5), new THREE.Vector3(-130, -14, -6),
    new THREE.Vector3(-150, -12, -3), new THREE.Vector3(-175, CV.y0 + 2.5, -1.3), new THREE.Vector3(-262, CV.y0 + 2.5, -1.3), new THREE.Vector3(-290, R.water - 1, -6),
  ]);
  const flow = flowDots(g, path, { n: 90, size: 1.3 });

  return {
    group: g,
    env(st) { st.scene.background = new THREE.Color(C.bg); st.scene.fog = new THREE.Fog(C.bg, 1100, 3200); const sc = st.sun.shadow.camera; sc.left = -520; sc.right = 520; sc.top = 520; sc.bottom = -520; sc.updateProjectionMatrix(); st.sun.position.set(-240, 600, 420); st.sun.target.position.set(40, 0, -40); st.sun.target.updateMatrixWorld(); },
    soils, waters, setFront, setWater, setForces, setWalls, setPanel, pillars, pillarMat, pumps, flow, people, pinside, roof, pumpFloorMat,
  };
}

function fieldTexture() {
  const cv = document.createElement('canvas'); cv.width = 1050; cv.height = 680;
  const g = cv.getContext('2d');
  g.fillStyle = '#b9c7a2'; g.fillRect(0, 0, 1050, 680);
  for (let i = 0; i < 10; i++) { g.fillStyle = i % 2 ? '#b3c29c' : '#bccaa6'; g.fillRect(i * 105, 0, 105, 680); }
  g.strokeStyle = '#ffffff'; g.lineWidth = 5;
  g.strokeRect(10, 10, 1030, 660);
  g.beginPath(); g.moveTo(525, 10); g.lineTo(525, 670); g.stroke();
  g.beginPath(); g.arc(525, 340, 91.5, 0, Math.PI * 2); g.stroke();
  g.strokeRect(10, 340 - 201.5, 165, 403); g.strokeRect(1040 - 165, 340 - 201.5, 165, 403);
  g.strokeRect(10, 340 - 91.5, 55, 183); g.strokeRect(1040 - 55, 340 - 91.5, 55, 183);
  const mk = (oy) => { const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; t.repeat.set(1, 0.5); t.offset.set(0, oy); return t; };
  return { back: mk(0.5), front: mk(0) };
}
