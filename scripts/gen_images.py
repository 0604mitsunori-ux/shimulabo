# -*- coding: utf-8 -*-
"""シミュラボ：OGP画像 & favicon PNG 生成（Pillow）
   出力: ogp/*.png（1200x630）, apple-touch-icon.png, favicon-32x32.png, favicon-16x16.png
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OGP_DIR = os.path.join(ROOT, "ogp")
os.makedirs(OGP_DIR, exist_ok=True)

TEAL = (15, 181, 196)
INDIGO = (99, 102, 241)
WHITE = (255, 255, 255)

FONT_BOLD = "C:/Windows/Fonts/YuGothB.ttc"
FONT_MED  = "C:/Windows/Fonts/YuGothM.ttc"

def font(path, size):
    return ImageFont.truetype(path, size)

def hgrad(w, h, c1, c2):
    img = Image.new("RGB", (w, h), c1)
    d = ImageDraw.Draw(img)
    for x in range(w):
        t = x / (w - 1)
        col = tuple(round(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
        d.line([(x, 0), (x, h)], fill=col)
    return img

def draw_flask(d, box, color, lw):
    """box=(x0,y0,x1,y1) の中にフラスコ(三角フラスコ風)を白線で描く"""
    x0, y0, x1, y1 = box
    w = x1 - x0; h = y1 - y0
    cx = (x0 + x1) / 2
    neck = w * 0.16
    top = y0 + h * 0.06
    bot = y0 + h * 0.94
    pts = [
        (cx - neck, top), (cx - neck, top + h * 0.34),
        (x0 + w * 0.10, bot), (x1 - w * 0.10, bot),
        (cx + neck, top + h * 0.34), (cx + neck, top),
    ]
    d.line(pts + [pts[0]], fill=color, width=lw, joint="curve")
    # 口
    d.line([(cx - neck * 1.7, top), (cx + neck * 1.7, top)], fill=color, width=lw)
    # 液面
    ly = top + h * 0.62
    d.line([(x0 + w * 0.20, ly), (x1 - w * 0.20, ly)], fill=color, width=max(2, lw - 1))

def logo_tile(size):
    """角丸グラデ＋白フラスコのアイコン画像を返す"""
    img = hgrad(size, size, TEAL, INDIGO).convert("RGBA")
    # 角丸マスク
    mask = Image.new("L", (size, size), 0)
    md = ImageDraw.Draw(mask)
    r = round(size * 0.22)
    md.rounded_rectangle([0, 0, size - 1, size - 1], radius=r, fill=255)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)
    d = ImageDraw.Draw(out)
    pad = size * 0.22
    draw_flask(d, (pad, pad * 0.8, size - pad, size - pad * 0.7), WHITE, max(2, round(size * 0.055)))
    return out

def wrap_jp(text, fnt, max_w):
    lines, cur = [], ""
    for ch in text:
        if ch == "\n":
            lines.append(cur); cur = ""; continue
        if fnt.getlength(cur + ch) <= max_w:
            cur += ch
        else:
            lines.append(cur); cur = ch
    if cur:
        lines.append(cur)
    return lines

def make_ogp(path, title, category, tagline="触って分かるシミュレーター集"):
    W, H = 1200, 630
    img = hgrad(W, H, TEAL, INDIGO).convert("RGBA")
    d = ImageDraw.Draw(img)

    # ロゴ＋ワードマーク（左上）
    tile = logo_tile(86)
    img.paste(tile, (64, 56), tile)
    d.text((166, 62), "シミュラボ", font=font(FONT_BOLD, 46), fill=WHITE)
    d.text((168, 116), "SIMU LAB", font=font(FONT_MED, 22), fill=(255, 255, 255, 220))

    # カテゴリピル
    pill_f = font(FONT_BOLD, 28)
    tw = pill_f.getlength(category)
    px, py = 64, 210
    d.rounded_rectangle([px, py, px + tw + 56, py + 52], radius=26, fill=(255, 255, 255, 235))
    d.text((px + 28, py + 8), category, font=pill_f, fill=INDIGO)

    # タイトル
    tf = font(FONT_BOLD, 66)
    lines = wrap_jp(title, tf, W - 128)[:3]
    ty = 300
    for ln in lines:
        # 影で可読性UP
        d.text((66, ty + 3), ln, font=tf, fill=(0, 0, 0, 70))
        d.text((64, ty), ln, font=tf, fill=WHITE)
        ty += 84

    # タグライン（下）
    d.text((64, H - 70), tagline + "　|　シミュラボ", font=font(FONT_MED, 28), fill=(255, 255, 255, 235))

    img.convert("RGB").save(path, "PNG")
    print("OGP:", os.path.relpath(path, ROOT))

SIMS = [
    ("default",            "その「なんとなく」、数字にすると面白い。", "シミュレーター集"),
    ("kaigi-cost",         "会議コストシミュレーター",               "お金・時間"),
    ("jutai",              "渋滞は、勝手に生まれる。",                 "ふしぎ・現象"),
    ("life",               "ライフゲーム",                             "ふしぎ・現象"),
    ("forest-fire",        "森林火災シミュレーター",                   "ふしぎ・現象"),
    ("schelling",          "街の分断シミュレーター",                   "ふしぎ・現象"),
    ("sandpile",           "砂山崩しシミュレーター",                   "ふしぎ・現象"),
    ("boids",              "鳥の群れ（ボイド）",                       "ふしぎ・現象"),
    ("double-pendulum",    "二重振り子（カオス）",                     "ふしぎ・現象"),
    ("wave",               "波の干渉シミュレーター",                   "ふしぎ・現象"),
    ("diffusion",          "拡散シミュレーター",                       "ふしぎ・現象"),
    ("turing",             "模様が生まれる（反応拡散）",               "ふしぎ・現象"),
    ("sync",               "同期現象シミュレーター",                   "ふしぎ・現象"),
    ("scroll-distance",    "スクロール距離メーター",                   "人生・自分ごと"),
    ("machi-jikan",        "人生の「待ち時間」",                       "人生・自分ごと"),
    ("catchcopy",          "うさんくさいキャッチコピー製造機",         "マーケティング"),
    ("influencer-soroban", "インフルエンサー皮算用",                   "マーケティング"),
    ("kuchikomi-hakyu",    "口コミ波及シミュレーター",                 "マーケティング"),
    ("subsc",              "サブスク墓場",                             "お金・時間"),
    ("caffeine",           "カフェイン残量",                           "人生・自分ごと"),
    ("sleep-debt",         "睡眠負債",                                 "人生・自分ごと"),
    ("warikan",            "割り勘の不公平",                           "お金・時間"),
    ("takarakuji",         "宝くじ買い続けたら",                       "お金・時間"),
    ("oyako",              "あと何回、親に会えるか",                   "人生・自分ごと"),
    ("infure",             "物価2倍まで何年？",                        "お金・時間"),
    ("if-company",         "もしあなたが会社だったら",                 "マーケティング"),
    ("nidone",             "二度寝損失",                               "人生・自分ごと"),
    ("chiritsumo",         "塵も積もれば",                             "お金・時間"),
    ("shutten",            "出店集客シミュレーター",                   "マーケティング"),
    ("tenshoku",           "転職 年収ifシミュレーター",                "お金・時間"),
    ("fire",               "FIRE達成シミュレーター",                   "お金・時間"),
    ("kyuryobi",           "あと何回給料日",                           "お金・時間"),
    ("coffee-life",        "コーヒー一生分",                           "お金・時間"),
    ("yoi",                "酔いがさめるまで",                         "人生・自分ごと"),
    ("taiju",              "半年後の体重",                             "人生・自分ごと"),
    ("unmei",              "運命の人に出会う確率",                     "恋愛・婚活"),
    ("mental-age",         "精神年齢診断",                             "人生・自分ごと"),
    ("isekai",             "異世界転生チート度診断",                   "人生・自分ごと"),
    ("neage",              "値上げ客数シミュレーター",                 "マーケティング"),
    ("konkatsu-match",     "婚活マッチ診断",                           "恋愛・婚活"),
    ("konkatsu-jouken",    "婚活 条件マッチ診断",                      "恋愛・婚活"),
    ("konkatsu-type",      "婚活 相性タイプ診断",                      "恋愛・婚活"),
    ("kokuhaku",           "告白成功率シミュレーター",                 "恋愛・婚活"),
    ("ryomoi",             "両思い度診断",                             "恋愛・婚活"),
    ("aisho-name",         "名前で相性占い",                           "恋愛・婚活"),
    ("same-class",         "好きな人と同じクラスになる確率",           "恋愛・婚活"),
    ("moteki",             "モテ期はいつ来る？診断",                   "恋愛・婚活"),
    ("contact",            "広告掲載・タイアップのご相談",             "FOR BUSINESS"),
    ("request",            "こんなシミュ、作ってほしい！",             "REQUEST"),
    ("board",              "みんなが見たいシミュ、投票で決定",         "REQUEST BOARD"),
]

for sid, title, cat in SIMS:
    make_ogp(os.path.join(OGP_DIR, f"{sid}.png"), title, cat)

# favicon / touch icon
logo_tile(180).convert("RGB").save(os.path.join(ROOT, "apple-touch-icon.png"), "PNG")
logo_tile(32).save(os.path.join(ROOT, "favicon-32x32.png"), "PNG")
logo_tile(16).save(os.path.join(ROOT, "favicon-16x16.png"), "PNG")
print("icons: apple-touch-icon.png, favicon-32x32.png, favicon-16x16.png")
print("done.")
