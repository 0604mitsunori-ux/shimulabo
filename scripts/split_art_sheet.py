"""ChatGPT で1枚にまとめて描いてもらった絵（横3×縦2 など）を、1つずつの WebP に切り分ける（2026-10-19）。
  - 半透明の光のにじみを消す（不透明度170未満を切り、170〜230をなめらかに）
  - 絵のかたまり（つながった部分）ごとに切り出す。並びは「上の段 左→右、下の段 左→右」
  - 最大480pxの WebP にして、確認用の一覧画像（白背景）も書き出す
使い方: python scripts/split_art_sheet.py <まとめ画像.png> <出力フォルダ> <名前1,名前2,...> [行数=2] [ふくらまし=5（くっつくときは1や3）]
"""
import os, sys
from collections import deque
import numpy as np
from PIL import Image, ImageFilter

src, out, names = sys.argv[1], sys.argv[2], sys.argv[3].split(",")
rows = int(sys.argv[4]) if len(sys.argv) > 4 else 2
dil = int(sys.argv[5]) if len(sys.argv) > 5 else 5
os.makedirs(out, exist_ok=True)
im = Image.open(src).convert("RGBA")
arr = np.array(im).astype(np.float32)
hard = np.clip((arr[:, :, 3] - 170) / 60, 0, 1) * 255
arr[:, :, 3] = hard
full = arr.astype(np.uint8)

S = 4
small = Image.fromarray(((hard > 10) * 255).astype(np.uint8)).resize((im.size[0] // S, im.size[1] // S), Image.BILINEAR).filter(ImageFilter.MaxFilter(dil)) if dil > 1 else Image.fromarray(((hard > 10) * 255).astype(np.uint8)).resize((im.size[0] // S, im.size[1] // S), Image.BILINEAR)
m = np.array(small) > 0
h, w = m.shape
lab = np.zeros((h, w), int); comps = []; n = 0
for y in range(h):
    for x in range(w):
        if m[y, x] and not lab[y, x]:
            n += 1; q = deque([(y, x)]); lab[y, x] = n; cnt = 0; ys = []; xs = []
            while q:
                cy, cx = q.popleft(); cnt += 1; ys.append(cy); xs.append(cx)
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < h and 0 <= nx < w and m[ny, nx] and not lab[ny, nx]:
                        lab[ny, nx] = n; q.append((ny, nx))
            comps.append((n, cnt, min(ys), max(ys), min(xs), max(xs)))
comps.sort(key=lambda c: -c[1])
big = comps[:len(names)]
small_ones = [c for c in comps[len(names):] if c[1] > 40]
assert len(big) == len(names), f"かたまりが {len(big)} 個（{len(names)} 個ほしい）"
# 小さなかけら（はなれた葉・ひななど）は、いちばん近い大きなかたまりにまとめる
owner = {c[0]: c[0] for c in big}
for c in small_ones:
    cy, cx = (c[2] + c[3]) / 2, (c[4] + c[5]) / 2
    best = min(big, key=lambda b: (max(b[2], min(cy, b[3])) - cy) ** 2 + (max(b[4], min(cx, b[5])) - cx) ** 2)
    owner[c[0]] = best[0]
H = im.size[1]
band = lambda c: min(rows - 1, int(((c[2] + c[3]) * S / 2) / (H / rows)))
big.sort(key=lambda c: (band(c), c[4] + c[5]))
labU = np.array(Image.fromarray(lab.astype(np.int32)).resize(im.size, Image.NEAREST))
sheet = Image.new("RGBA", (300 * 3, 300 * ((len(names) + 2) // 3)), (255, 255, 255, 255))
for i, (c, nm) in enumerate(zip(big, names)):
    keep = [k for k, o in owner.items() if o == c[0]]
    a = full.copy(); a[:, :, 3] = np.where(np.isin(labU, keep), a[:, :, 3], 0)
    t = Image.fromarray(a, "RGBA")
    t = t.crop(Image.fromarray(((a[:, :, 3] > 10) * 255).astype(np.uint8)).getbbox())
    t.thumbnail((480, 480), Image.LANCZOS)
    p = os.path.join(out, nm + ".webp"); t.save(p, "WEBP", quality=80, method=6)
    print(nm, t.size, os.path.getsize(p) // 1024, "KB")
    th = t.copy(); th.thumbnail((280, 280)); sheet.alpha_composite(th, ((i % 3) * 300 + 10, (i // 3) * 300 + 10))
chk = os.path.join(os.environ.get("TEMP", "."), "art_sheet_check.png")
sheet.convert("RGB").save(chk); print("確認用:", chk)
