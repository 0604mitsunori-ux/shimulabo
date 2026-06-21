# -*- coding: utf-8 -*-
"""note記事用：音声入力 時短シミュレーターの「結果カード」画像を再現生成してDownloadsへ保存。"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1200, 880
FB = "C:/Windows/Fonts/YuGothB.ttc"
FM = "C:/Windows/Fonts/YuGothM.ttc"
OUT = os.path.join(os.path.expanduser("~"), "Downloads")
os.makedirs(OUT, exist_ok=True)

INK = (31, 41, 55)
INK2 = (107, 114, 128)
INDIGO = (79, 70, 229)
INDIGO_D = (67, 56, 202)
TEAL = (13, 148, 136)
BG = (244, 245, 248)
LINE = (229, 231, 235)

def f(p, s): return ImageFont.truetype(p, s)
def tw(d, t, ft): b = d.textbbox((0, 0), t, font=ft); return b[2] - b[0]

def mic(d, cx, cy, s, col):
    bw, bh = int(26*s), int(56*s); top = cy-int(40*s)
    d.rounded_rectangle([cx-bw//2, top, cx+bw//2, top+bh], radius=bw//2, fill=col)
    aw = int(44*s); ay = top+bh-int(24*s)
    d.arc([cx-aw//2, ay-aw//2, cx+aw//2, ay+aw//2], start=20, end=160, fill=col, width=int(6*s))
    d.line([cx, ay+aw//2-int(3*s), cx, ay+aw//2+int(16*s)], fill=col, width=int(6*s))
    d.line([cx-int(16*s), ay+aw//2+int(16*s), cx+int(16*s), ay+aw//2+int(16*s)], fill=col, width=int(6*s))

def make(filename, label, big, sub, stats):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ヘッダー（ブランド＋シミュ名）
    fbrand = f(FB, 30)
    d.text((60, 44), "シミュラボ", font=fbrand, fill=INDIGO)
    fttl = f(FM, 26)
    d.text((60 + tw(d, "シミュラボ", fbrand) + 18, 48), "｜音声入力 時短シミュレーター",
           font=fttl, fill=INK2)

    # 結果カード
    cx0, cy0, cx1, cy1 = 60, 110, W-60, 560
    sh = Image.new("RGBA", img.size, (0,0,0,0)); ds = ImageDraw.Draw(sh)
    ds.rounded_rectangle([cx0+6, cy0+10, cx1+6, cy1+10], radius=26, fill=(30,41,59,40))
    sh = sh.filter(ImageFilter.GaussianBlur(10)); img.paste(Image.alpha_composite(img.convert("RGBA"), sh).convert("RGB"))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([cx0, cy0, cx1, cy1], radius=26, fill=(255,255,255))

    # label
    flab = f(FM, 30)
    lw = tw(d, label, flab)
    d.text(((W-lw)//2, cy0+44), label, font=flab, fill=INK2)
    # big
    fbig = f(FB, 124)
    bw = tw(d, big, fbig)
    d.text(((W-bw)//2, cy0+86), big, font=fbig, fill=INDIGO_D)
    # sub
    fsub = f(FM, 28)
    sw = tw(d, sub, fsub)
    d.text(((W-sw)//2, cy0+232), sub, font=fsub, fill=INK2)

    # statline (3 stats)
    n = len(stats); gap = 24
    total = cx1 - cx0 - 56
    bwid = (total - gap*(n-1)) // n
    sx = cx0 + 28; sy = cy0 + 290
    fk = f(FM, 24); fv = f(FB, 40)
    for i, (k, v, acc) in enumerate(stats):
        x = sx + i*(bwid+gap)
        d.rounded_rectangle([x, sy, x+bwid, sy+118], radius=16, fill=(247,248,250), outline=LINE, width=1)
        kw = tw(d, k, fk); d.text((x+(bwid-kw)//2, sy+22), k, font=fk, fill=INK2)
        vcol = TEAL if acc else INK
        vw = tw(d, v, fv); d.text((x+(bwid-vw)//2, sy+56), v, font=fv, fill=vcol)

    # Typeless CTA box
    bx0, by0, bx1, by1 = 60, 600, W-60, 800
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=18, fill=(238,242,255), outline=(165,180,252), width=2)
    mic(d, bx0+50, by0+58, 1.0, INDIGO)
    fc1 = f(FB, 32)
    d.text((bx0+96, by0+26), "その時短、「音声入力」で実現できます。", font=fc1, fill=INDIGO_D)
    fc2 = f(FM, 25)
    d.text((bx0+96, by0+74), "今いちばんおすすめは Typeless。話すだけで高精度に文字化＆AIが整文。", font=fc2, fill=INK2)
    # button
    fbtn = f(FB, 28); btxt = "Typeless を無料で試す →"
    btw = tw(d, btxt, fbtn)
    d.rounded_rectangle([bx0+96, by1-66, bx0+96+btw+56, by1-12], radius=27, fill=INDIGO)
    d.text((bx0+96+28, by1-58), btxt, font=fbtn, fill=(255,255,255))

    # footer URL
    ffoot = f(FM, 24)
    d.text((60, H-46), "▶ 試してみる：shimulabo.com/sims/input-jitan/", font=ffoot, fill=INK2)

    out = os.path.join(OUT, filename)
    img.save(out, "PNG")
    print("saved:", out)

# オールラウンダー：1日5,000字・70字/分・時給2,500円
make("シミュ結果_オールラウンダー.png",
     "音声入力で 年間の削減額",
     "¥724,166",
     "1日5,000字・70字/分・時給2,500円",
     [("1日の時短", "48分", True), ("年間の時短時間", "290時間", False), ("10年の削減額", "¥7,241,660", False)])

# 教員向け：1日3,000字・45字/分・時給2,000円
make("シミュ結果_教員向け.png",
     "音声入力で 年間の削減額",
     "¥540,740",
     "1日3,000字・45字/分・時給2,000円",
     [("1日の時短", "44分", True), ("年間の時短時間", "270時間", False), ("10年の削減額", "¥5,407,407", False)])

print("done.")
