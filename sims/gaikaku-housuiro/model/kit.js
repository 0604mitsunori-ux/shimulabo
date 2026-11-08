// 模型づくりの部品集（どの話でも使う）
import { THREE, C, mat } from './stage-lite.js';

// 土の断面：色は高さ（world y）で決まる帯。uWater で地下水の青を重ねる
export function soilMaterial(shade = 1, { bands } = {}) {
  const B = bands || [[-1.5, [0.80, 0.72, 0.60]], [-10, [0.86, 0.80, 0.67]], [-24, [0.75, 0.67, 0.54]], [-42, [0.80, 0.72, 0.58]], [-62, [0.68, 0.59, 0.47]], [-95, [0.74, 0.65, 0.52]], [-125, [0.64, 0.56, 0.45]]];
  let fn = 'vec3 c = vec3(0.60,0.52,0.41);\n', lines = '';
  for (const [y, col] of B) {
    fn += `if (y < ${y.toFixed(2)}) c = vec3(${col.map(v => v.toFixed(3)).join(',')});\n`;
    lines += `b = max(b, 1.0 - smoothstep(0.0, 0.3, abs(y - (${y.toFixed(2)}))));\n`;
  }
  return new THREE.ShaderMaterial({
    uniforms: { uWater: { value: 0 }, uShade: { value: shade }, uAlpha: { value: 1 }, uTable: { value: -3.0 }, uFrost: { value: 0 }, uFrostC: { value: new THREE.Vector3() }, uFrostR: { value: 0 } },
    transparent: true, side: THREE.DoubleSide,
    vertexShader: `varying vec3 vW; void main(){ vec4 w = modelMatrix*vec4(position,1.0); vW=w.xyz; gl_Position = projectionMatrix*viewMatrix*w; }`,
    fragmentShader: `
      uniform float uWater, uShade, uAlpha, uTable, uFrost, uFrostR; uniform vec3 uFrostC; varying vec3 vW;
      void main(){
        float y = vW.y; ${fn}
        float b = 0.0; ${lines}
        c *= 1.0 - 0.12 * b;
        float wt = uWater * smoothstep(uTable + 0.5, uTable - 1.0, y);
        c = mix(c, vec3(0.42,0.64,0.88), 0.6 * wt);
        float fr = uFrost * (1.0 - smoothstep(uFrostR * 0.85, uFrostR, length(vW - uFrostC)));
        c = mix(c, vec3(0.86,0.93,0.98), 0.85 * fr);
        gl_FragColor = vec4(pow(c * uShade, vec3(2.2)), uAlpha);
        #include <colorspace_fragment>
      }`,
  });
}

export function waterMaterial(opacity = 0.55, color = C.water) {
  return new THREE.MeshStandardMaterial({ color, transparent: true, opacity, roughness: 0.25, metalness: 0.0, depthWrite: false, side: THREE.DoubleSide });
}

export function box(group, x0, x1, y0, y1, z0, z1, material, { cast = true, receive = true } = {}) {
  const m = new THREE.Mesh(new THREE.BoxGeometry(x1 - x0, y1 - y0, z1 - z0), material);
  m.position.set((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2);
  m.castShadow = cast; m.receiveShadow = receive;
  group.add(m); return m;
}

// z<0 側の半分の円筒（縦）。thetaは three の CylinderGeometry と同じ（x=sinθ, z=cosθ）
export const HP = Math.PI / 2;
export function halfCylY(group, cx, cz, r, y0, y1, material, th0 = HP, th1 = 3 * HP, open = true) {
  const m = new THREE.Mesh(new THREE.CylinderGeometry(r, r, y1 - y0, 72, 1, open, th0, th1 - th0), material);
  m.position.set(cx, (y0 + y1) / 2, cz); m.receiveShadow = true; m.castShadow = !open;
  group.add(m); return m;
}
// x 方向の半分の管（z<0 側）
export function halfTubeX(group, x0, x1, cy, r, material, open = true) {
  const g = new THREE.CylinderGeometry(r, r, x1 - x0, 64, 1, open, HP, Math.PI);
  const m = new THREE.Mesh(g, material);
  m.rotation.z = Math.PI / 2; m.position.set((x0 + x1) / 2, cy, 0); m.receiveShadow = true;
  group.add(m); return m;
}
// 厚みのある半円の輪（断面の切り口）：z=0 の面に置く
export function ringFace(group, cx, cy, r0, r1, material, axis = 'z') {
  const s = new THREE.Shape(); s.absarc(0, 0, r1, 0, Math.PI * 2, false);
  const h = new THREE.Path(); h.absarc(0, 0, r0, 0, Math.PI * 2, true); s.holes.push(h);
  const m = new THREE.Mesh(new THREE.ShapeGeometry(s, 64), material);
  m.position.set(cx, cy, 0.04); group.add(m); return m;
}

// 矢印（+y 向き）。group.userData.mat で透明度を変える
export function arrow(group, color, { len = 12, r = 1.1, head = 2.8, headLen = 5 } = {}) {
  const g = new THREE.Group();
  const m = new THREE.MeshStandardMaterial({ color, roughness: 0.6, transparent: true, opacity: 0 });
  const s = new THREE.Mesh(new THREE.CylinderGeometry(r, r, len - headLen, 20), m); s.position.y = (len - headLen) / 2; g.add(s);
  const h = new THREE.Mesh(new THREE.ConeGeometry(head, headLen, 28), m); h.position.y = len - headLen / 2; g.add(h);
  g.userData.mat = m; group.add(g); return g;
}
export function setArrow(g, alpha) { g.userData.mat.opacity = alpha; g.visible = alpha > 0.001; }

// 人の大きさの目安（1.7m）
export function person(group, x, y, z, color = 0x2f7fc8, s = 1) {
  const g = new THREE.Group();
  const m = new THREE.MeshStandardMaterial({ color, roughness: 0.7 });
  const body = new THREE.Mesh(new THREE.CapsuleGeometry(0.22 * s, 0.9 * s, 4, 12), m); body.position.y = 0.75 * s; g.add(body);
  const head = new THREE.Mesh(new THREE.SphereGeometry(0.16 * s, 16, 12), m); head.position.y = 1.55 * s; g.add(head);
  g.position.set(x, y, z); g.traverse(o => { if (o.isMesh) o.castShadow = true; });
  group.add(g); return g;
}

// 雨（線の粒）。update(t) で落とす
export function rain(group, { x0, x1, z0, z1, top = 60, bottom = 0, n = 1500, color = 0x6f9fd0 }) {
  const pos = new Float32Array(n * 6), seed = [];
  for (let i = 0; i < n; i++) seed.push([x0 + Math.random() * (x1 - x0), z0 + Math.random() * (z1 - z0), Math.random()]);
  const g = new THREE.BufferGeometry(); g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  const m = new THREE.LineBasicMaterial({ color, transparent: true, opacity: 0 });
  const L = new THREE.LineSegments(g, m); L.frustumCulled = false; group.add(L);
  return {
    obj: L,
    update(t, alpha, speed = 40) {
      m.opacity = alpha; L.visible = alpha > 0.001; if (!L.visible) return;
      const H = top - bottom;
      for (let i = 0; i < n; i++) {
        const [x, z, p] = seed[i];
        const y = top - (((p * H) + t * speed) % H);
        pos.set([x, y, z, x - 0.3, y + 3.5, z], i * 6);
      }
      g.attributes.position.needsUpdate = true;
    },
  };
}

// 流れの粒（道すじに沿って動く点）。path は THREE.Curve
export function flowDots(group, curve, { n = 60, size = 1.6, color = 0x2f7fc8 } = {}) {
  const geo = new THREE.SphereGeometry(size, 10, 8);
  const m = new THREE.MeshStandardMaterial({ color, roughness: 0.4, transparent: true, opacity: 0, emissive: color, emissiveIntensity: 0.25 });
  const inst = new THREE.InstancedMesh(geo, m, n); inst.frustumCulled = false; group.add(inst);
  const d = new THREE.Object3D();
  return {
    obj: inst,
    update(t, alpha, speed = 0.08) {
      m.opacity = alpha; inst.visible = alpha > 0.001; if (!inst.visible) return;
      for (let i = 0; i < n; i++) {
        const u = ((((i / n) + t * speed) % 1) + 1) % 1;   // 逆向き（t がマイナス）でも 0〜1 に収める
        d.position.copy(curve.getPointAt(u)); d.updateMatrix(); inst.setMatrixAt(i, d.matrix);
      }
      inst.instanceMatrix.needsUpdate = true;
    },
  };
}

// 板に文字（3Dの中の看板）
export function textPlane(group, text, { w = 40, h = 10, color = '#22262b', bg = 'rgba(255,255,255,0.0)', font = 'bold 96px "BIZ UDPGothic","Yu Gothic",sans-serif' } = {}) {
  const cv = document.createElement('canvas'); cv.width = 1024; cv.height = Math.round(1024 * h / w);
  const g = cv.getContext('2d'); g.fillStyle = bg; g.fillRect(0, 0, cv.width, cv.height);
  g.font = font; g.fillStyle = color; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText(text, cv.width / 2, cv.height / 2);
  const t = new THREE.CanvasTexture(cv); t.colorSpace = THREE.SRGBColorSpace;
  const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), new THREE.MeshBasicMaterial({ map: t, transparent: true }));
  group.add(m); return m;
}

export const concreteMat = (c = C.concrete, extra = {}) => mat(c, extra);

// 断面の切り口：土の長方形から holes（くり抜く形）を抜いて描く。ステンシルで抜くので形を組み合わせるだけでよい
//   holes: [{rect:[x0,x1,y0,y1]}, {circle:[cx,cy,r]}, {poly:[[x,y],...]}]
export function sectionFace(group, { x0, x1, y0, y1, z = 0 }, holes, material) {
  const maskMat = new THREE.MeshBasicMaterial({ colorWrite: false, depthWrite: false, side: THREE.DoubleSide,
    stencilWrite: true, stencilRef: 1, stencilFunc: THREE.AlwaysStencilFunc, stencilZPass: THREE.ReplaceStencilOp });
  const masks = [];
  for (const h of holes) {
    const s = new THREE.Shape();
    if (h.rect) { const [a, b, c, d] = h.rect; s.moveTo(a, c); s.lineTo(b, c); s.lineTo(b, d); s.lineTo(a, d); s.closePath(); }
    else if (h.circle) { const [cx, cy, r] = h.circle; s.absarc(cx, cy, r, 0, Math.PI * 2, false); }
    else if (h.poly) h.poly.forEach(([x, y], i) => i ? s.lineTo(x, y) : s.moveTo(x, y));
    const m = new THREE.Mesh(new THREE.ShapeGeometry(s, 48), maskMat);
    m.position.z = z + 0.005; m.renderOrder = -10; group.add(m); masks.push(m);
  }
  material.stencilWrite = true; material.stencilRef = 1; material.stencilFunc = THREE.NotEqualStencilFunc;
  material.stencilZPass = THREE.KeepStencilOp;
  const face = new THREE.Mesh(new THREE.PlaneGeometry(x1 - x0, y1 - y0), material);
  face.position.set((x0 + x1) / 2, (y0 + y1) / 2, z); face.renderOrder = -5; group.add(face);
  return { face, masks };
}

// 押し出しの台形（堤防など）：断面 pts を z0→z1 に押し出す
export function extrudeZ(group, pts, z0, z1, capMat, sideMat) {
  const s = new THREE.Shape(); pts.forEach(([x, y], i) => i ? s.lineTo(x, y) : s.moveTo(x, y));
  const g = new THREE.ExtrudeGeometry(s, { depth: z1 - z0, bevelEnabled: false });
  const m = new THREE.Mesh(g, [capMat, sideMat]); m.position.z = z0; m.receiveShadow = true; m.castShadow = true;
  group.add(m); return m;
}
