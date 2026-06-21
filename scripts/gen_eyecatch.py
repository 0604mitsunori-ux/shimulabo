# -*- coding: utf-8 -*-
"""note用アイキャッチ2枚を生成してダウンロードフォルダに保存（1280x670）。"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1280, 670
FONT_BOLD = "C:/Windows/Fonts/YuGothB.ttc"
FONT_MED  = "C:/Windows/Fonts/YuGothM.ttc"
OUT = os.path.join(os.path.expanduser("~"), "Downloads")
os.makedirs(OUT, exist_ok=True)

def f(path, size):
    return ImageFont.truetype(path, size)

def lerp(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))

def diagonal_gradient(c1, c2):
    """左上→右下の斜めグラデーション"""
    base = Image.new("RGB", (W, H), c1)
    px = base.load()
    maxd = W + H
    for y in range(H):
        for x in range(0, W, 2):  # 2px刻みで高速化
            t = (x + y) / maxd
            col = lerp(c1, c2, t)
            px[x, y] = col
            if x + 1 < W:
                px[x + 1, y] = col
    return base

def soft_circle(img, cx, cy, r, color, alpha):
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color + (alpha,))
    layer = layer.filter(ImageFilter.GaussianBlur(2))
    img.alpha_composite(layer)

def mic_icon(img, cx, cy, scale, color=(255, 255, 255)):
    """シンプルなマイクのアイコンを描画"""
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    bw = int(70 * scale)      # body width
    bh = int(150 * scale)     # body height
    top = cy - int(120 * scale)
    # body (rounded capsule)
    d.rounded_rectangle([cx - bw // 2, top, cx + bw // 2, top + bh],
                        radius=bw // 2, fill=color + (255,))
    # arc holder
    aw = int(110 * scale)
    ah = int(110 * scale)
    ay = top + bh - int(70 * scale)
    d.arc([cx - aw // 2, ay - ah // 2, cx + aw // 2, ay + ah // 2],
          start=20, end=160, fill=color + (255,), width=int(14 * scale))
    # stand
    d.line([cx, ay + ah // 2 - int(8 * scale), cx, ay + ah // 2 + int(45 * scale)],
           fill=color + (255,), width=int(14 * scale))
    d.line([cx - int(45 * scale), ay + ah // 2 + int(45 * scale),
            cx + int(45 * scale), ay + ah // 2 + int(45 * scale)],
           fill=color + (255,), width=int(14 * scale))
    # sound waves
    for i, rr in enumerate((int(130 * scale), int(170 * scale))):
        d.arc([cx - rr, cy - rr, cx + rr, cy + rr], start=-55, end=55,
              fill=color + (160 - i * 60,), width=int(10 * scale))
    img.alpha_composite(layer)

def text_w(draw, txt, font):
    b = draw.textbbox((0, 0), txt, font=font)
    return b[2] - b[0]

def draw_shadow_text(draw, xy, txt, font, fill, shadow=(0, 0, 0, 90), off=3):
    x, y = xy
    draw.text((x + off, y + off), txt, font=font, fill=shadow)
    draw.text((x, y), txt, font=font, fill=fill)

def make(filename, c1, c2, tag, headlines, sub, accent):
    img = diagonal_gradient(c1, c2).convert("RGBA")
    # 装飾の淡い円
    soft_circle(img, 1080, 120, 220, (255, 255, 255), 26)
    soft_circle(img, 1180, 560, 180, accent, 40)
    soft_circle(img, 120, 600, 160, (255, 255, 255), 18)
    # マイクアイコン（右側）
    mic_icon(img, 1040, 330, 1.15)
    d = ImageDraw.Draw(img)

    # タグpill（左上）
    ftag = f(FONT_BOLD, 30)
    tw = text_w(d, tag, ftag)
    pad = 22
    px0, py0 = 80, 70
    d.rounded_rectangle([px0, py0, px0 + tw + pad * 2, py0 + 56],
                        radius=28, fill=(255, 255, 255, 235))
    d.text((px0 + pad, py0 + 11), tag, font=ftag, fill=c1)

    # 見出し（複数行）
    fh = f(FONT_BOLD, 76)
    y = 190
    for line in headlines:
        draw_shadow_text(d, (80, y), line, fh, (255, 255, 255, 255))
        y += 96
    # アクセント下線
    last_w = text_w(d, headlines[-1], fh)
    d.rounded_rectangle([84, y + 6, 84 + min(last_w, 560), y + 20],
                        radius=7, fill=accent + (255,))

    # サブ
    fs = f(FONT_MED, 36)
    d.text((84, y + 48), sub, font=fs, fill=(255, 255, 255, 230))

    # 下部 ワードマーク
    fw = f(FONT_BOLD, 44)
    wm = "Typeless"
    d.text((80, H - 92), wm, font=fw, fill=(255, 255, 255, 255))
    fwc = f(FONT_MED, 26)
    cap = "話すだけで、書ける。AI音声入力"
    d.text((80 + text_w(d, wm, fw) + 22, H - 80), cap, font=fwc, fill=(255, 255, 255, 200))

    out = os.path.join(OUT, filename)
    img.convert("RGB").save(out, "PNG", quality=95)
    print("saved:", out)

# 1) オールラウンダー（indigo → violet）
make("Typeless_アイキャッチ_オールラウンダー.png",
     (79, 70, 229), (147, 51, 234),
     "音声入力 / PR",
     ["話すだけで、", "文章が完成する。"],
     "いま一番の音声入力ツールを使ってみた",
     accent=(250, 204, 21))   # gold

# 2) 教員向け（indigo → teal blue）
make("Typeless_アイキャッチ_教員向け.png",
     (67, 56, 202), (14, 116, 144),
     "先生向け / PR",
     ["キーボードが", "苦手な先生へ。"],
     "“話すだけ”で校務の文章が終わる時代",
     accent=(52, 211, 153))   # green

print("done.")
