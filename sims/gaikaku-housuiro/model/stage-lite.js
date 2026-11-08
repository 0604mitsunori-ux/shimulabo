// シミュラボ用の小さな舞台（YouTube「インフラ解剖室」の模型エンジンから、Webで必要な分だけ）
import * as THREE from '../../../assets/three/three.module.js';
export { THREE };
export const C = {
  bg: 0xe8e9eb, concrete: 0xd9d5cc, concreteDark: 0xb9b4a9,
  soil1: 0xcbb79a, soil2: 0xb8a083, soil3: 0xa48b6f, soil4: 0x8f785e,
  grass: 0xc5ccb6, water: 0x3f8fd8, red: 0xd6352b,
  ink: '#22262b', inkSoft: '#5b636c', redCss: '#d6352b', blueCss: '#2f7fc8',
};
export function mat(color, opts = {}) {
  return new THREE.MeshStandardMaterial({ color, roughness: 0.92, metalness: 0.0, flatShading: false, ...opts });
}
