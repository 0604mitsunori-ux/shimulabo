# -*- coding: utf-8 -*-
"""シミュラボ：OGP画像 & favicon PNG 生成（Pillow）
   出力: ogp/*.png（1200x630）, apple-touch-icon.png, favicon-32x32.png, favicon-16x16.png
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

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

def lerp(c1, c2, t):
    return tuple(round(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def grad_color(stops, t):
    t = max(0.0, min(1.0, t))
    for i in range(len(stops) - 1):
        p0, c0 = stops[i]; p1, c1 = stops[i + 1]
        if t <= p1:
            tt = (t - p0) / (p1 - p0) if p1 > p0 else 0
            return lerp(c0, c1, max(0.0, min(1.0, tt)))
    return stops[-1][1]

def dgrad(w, h, stops, ax=0.62, ay=0.38):
    """斜めグラデを低解像度で作り拡大（高速・滑らか）。t は右・上ほど大きい。"""
    sw, sh = 140, 74
    small = Image.new("RGB", (sw, sh))
    px = small.load()
    s = ax + ay
    for y in range(sh):
        fy = (1 - y / (sh - 1)) * ay
        for x in range(sw):
            t = ((x / (sw - 1)) * ax + fy) / s
            px[x, y] = grad_color(stops, t)
    return small.resize((w, h), Image.BICUBIC)

def dotgrid(d, x0, y0, cols, rows, gap, r, color):
    for i in range(cols):
        for j in range(rows):
            cx = x0 + i * gap; cy = y0 + j * gap
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)

def sparkle(d, cx, cy, R, color=(255, 255, 255, 235)):
    """4方向にとがった輝き（菱形×2）"""
    nv = R * 0.16
    d.polygon([(cx, cy - R), (cx + nv, cy), (cx, cy + R), (cx - nv, cy)], fill=color)
    d.polygon([(cx - R, cy), (cx, cy + nv), (cx + R, cy), (cx, cy - nv)], fill=color)

BG_STOPS = [(0.0, (16, 146, 178)), (0.42, (38, 88, 212)), (0.72, (66, 80, 226)), (1.0, (122, 92, 238))]
CYAN = (74, 222, 235)
PILL_BLUE = (37, 99, 235)

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

def make_ogp(path, title, category, tagline="触って分かるシミュレーター集", underline=None):
    W, H = 1200, 630
    img = dgrad(W, H, BG_STOPS).convert("RGBA")

    # ===== 装飾レイヤー（半透明） =====
    deco = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dd = ImageDraw.Draw(deco)
    # 大きな淡い円（右上・右下）
    dd.ellipse([W - 250, -170, W + 230, 310], fill=(255, 255, 255, 16))
    dd.ellipse([W - 470, H - 250, W - 110, H + 110], fill=(255, 255, 255, 12))
    # 斜めライン（右下）
    for k in range(6):
        off = k * 78
        dd.line([(W - 560 + off, H + 20), (W - 40 + off, H - 470)], fill=(255, 255, 255, 26), width=2)
    # ドットグリッド（右上・右下）
    dotgrid(dd, W - 250, 70, 9, 4, 23, 3, (255, 255, 255, 70))
    dotgrid(dd, W - 210, H - 130, 8, 3, 23, 3, (255, 255, 255, 55))
    # 光沢の球（下・中央右）＋ハイライト
    bx, by, br = W - 360, H - 120, 52
    dd.ellipse([bx - br, by - br, bx + br, by + br], fill=(255, 255, 255, 26))
    dd.ellipse([bx - br * 0.5, by - br * 0.6, bx - br * 0.5 + br * 0.5, by - br * 0.6 + br * 0.5], fill=(255, 255, 255, 70))
    img = Image.alpha_composite(img, deco)

    # 輝き（グロー付き）
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([W - 330, 78, W - 250, 158], fill=(255, 255, 255, 120))
    glow = glow.filter(ImageFilter.GaussianBlur(14))
    img = Image.alpha_composite(img, glow)
    spk = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sparkle(ImageDraw.Draw(spk), W - 290, 118, 26)
    img = Image.alpha_composite(img, spk)

    d = ImageDraw.Draw(img)

    # ===== ロゴ＋ワードマーク（左上） =====
    tile = logo_tile(92)
    img.paste(tile, (64, 52), tile)
    d.text((176, 58), "シミュラボ", font=font(FONT_BOLD, 48), fill=WHITE)
    d.text((178, 116), "SIMU LAB", font=font(FONT_MED, 23), fill=(255, 255, 255, 225))

    # ===== カテゴリピル =====
    pill_f = font(FONT_BOLD, 28)
    tw = pill_f.getlength(category)
    px, py = 64, 206
    d.rounded_rectangle([px, py, px + tw + 56, py + 54], radius=27, fill=(255, 255, 255, 240))
    d.text((px + 28, py + 9), category, font=pill_f, fill=PILL_BLUE)

    # ===== タイトル（発光＋本体） =====
    tf = font(FONT_BOLD, 64)
    lines = wrap_jp(title, tf, W - 150)[:3]
    ty0 = 300
    lh = 84
    # 発光レイヤー
    tg = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    tgd = ImageDraw.Draw(tg)
    ty = ty0
    for ln in lines:
        tgd.text((64, ty), ln, font=tf, fill=(150, 215, 255, 180))
        ty += lh
    tg = tg.filter(ImageFilter.GaussianBlur(10))
    img = Image.alpha_composite(img, tg)
    d = ImageDraw.Draw(img)
    # 本体（白）＋キーワード下線（シアン）
    ty = ty0
    for ln in lines:
        d.text((64, ty), ln, font=tf, fill=WHITE)
        if underline and underline in ln:
            pre = ln.split(underline)[0]
            xs = 64 + tf.getlength(pre)
            xe = xs + tf.getlength(underline)
            uy = ty + lh * 0.92
            d.rounded_rectangle([xs, uy, xe, uy + 9], radius=4, fill=CYAN + (255,))
        ty += lh

    # ===== アクセントバー（短いシアン線） =====
    aby = ty + 10
    if aby < H - 96:
        d.rounded_rectangle([64, aby, 64 + 92, aby + 9], radius=4, fill=CYAN + (235,))

    # ===== タグライン（下） =====
    d.text((64, H - 64), tagline + "　｜　シミュラボ", font=font(FONT_MED, 27), fill=(255, 255, 255, 235))

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
    ("kuchikomi-hakyu",    "口コミ波及シミュレーター",                 "店舗・ビジネス"),
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
    ("shutten",            "出店集客シミュレーター",                   "店舗・ビジネス"),
    ("tenshoku",           "転職 年収ifシミュレーター",                "仕事・働き方"),
    ("fire",               "FIRE達成シミュレーター",                   "お金・時間"),
    ("kyuryobi",           "あと何回給料日",                           "お金・時間"),
    ("coffee-life",        "コーヒー一生分",                           "お金・時間"),
    ("yoi",                "酔いがさめるまで",                         "人生・自分ごと"),
    ("taiju",              "半年後の体重",                             "人生・自分ごと"),
    ("unmei",              "運命の人に出会う確率",                     "恋愛・婚活"),
    ("mental-age",         "精神年齢診断",                             "人生・自分ごと"),
    ("isekai",             "異世界転生チート度診断",                   "人生・自分ごと"),
    ("neage",              "値上げ客数シミュレーター",                 "店舗・ビジネス"),
    ("konkatsu-match",     "婚活マッチ診断",                           "恋愛・婚活"),
    ("konkatsu-jouken",    "婚活 条件マッチ診断",                      "恋愛・婚活"),
    ("konkatsu-type",      "婚活 相性タイプ診断",                      "恋愛・婚活"),
    ("kokuhaku",           "告白成功率シミュレーター",                 "恋愛・婚活"),
    ("ryomoi",             "両思い度診断",                             "恋愛・婚活"),
    ("aisho-name",         "名前で相性占い",                           "恋愛・婚活"),
    ("same-class",         "好きな人と同じクラスになる確率",           "恋愛・婚活"),
    ("moteki",             "モテ期はいつ来る？診断",                   "恋愛・婚活"),
    ("ad-roas",            "広告ROAS試算シミュレーター",               "店舗・ビジネス"),
    ("ltv",                "LTV（顧客生涯価値）シミュレーター",         "店舗・ビジネス"),
    ("coupon",             "クーポン採算シミュレーター",               "店舗・ビジネス"),
    ("chirashi-web",       "チラシ vs Web広告",                        "店舗・ビジネス"),
    ("jutaku-loan",        "住宅ローン返済シミュレーター",             "マネー・保険・不動産"),
    ("kuriage",            "繰上返済 効果シミュレーター",             "マネー・保険・不動産"),
    ("hosho",              "必要保障額シミュレーター",                 "マネー・保険・不動産"),
    ("rougo",              "老後資金シミュレーター",                   "マネー・保険・不動産"),
    ("zangyo",             "残業代シミュレーター",                     "仕事・働き方"),
    ("yukyu",              "有給消化シミュレーター",                   "仕事・働き方"),
    ("freelance",          "フリーランス手取りシミュレーター",         "仕事・働き方"),
    ("tsukin",             "通勤時間の生涯コスト",                     "仕事・働き方"),
    ("goukaku",            "合格可能性シミュレーター",                 "学生・勉強"),
    ("benkyo-time",        "勉強時間シミュレーター",                   "学生・勉強"),
    ("gakuhi",             "学費総額シミュレーター",                   "学生・勉強"),
    ("bukatsu",            "部活引退カウントダウン",                   "学生・勉強"),
    ("bep",                "損益分岐点シミュレーター",                 "店舗・ビジネス"),
    ("noshow",             "ノーショー損失シミュレーター",             "店舗・ビジネス"),
    ("jinkenhi",           "人件費率診断シミュレーター",               "店舗・ビジネス"),
    ("nisa",               "NISA積立シミュレーター",                   "マネー・保険・不動産"),
    ("kuruma-iji",         "車の維持費シミュレーター",                 "マネー・保険・不動産"),
    ("furusato",           "ふるさと納税 上限額",                      "マネー・保険・不動産"),
    ("jikkou-jikyu",       "実質時給シミュレーター",                   "仕事・働き方"),
    ("fukugyo-zei",        "副業の税金・手取り",                       "仕事・働き方"),
    ("shouyo-tedori",      "ボーナス手取りシミュレーター",             "仕事・働き方"),
    ("tango",              "英単語マスター日数",                       "学生・勉強"),
    ("shogakukin",         "奨学金返済シミュレーター",                 "学生・勉強"),
    ("benkyo-target",      "目標点までの勉強量",                       "学生・勉強"),
    ("kaiten",             "回転率シミュレーター",                     "店舗・ビジネス"),
    ("line-cv",            "LINE・メルマガ配信効果",                   "店舗・ビジネス"),
    ("zaiko",              "在庫の持ちすぎコスト",                     "店舗・ビジネス"),
    ("chochiku-mokuhyo",   "目標金額までの積立",                       "マネー・保険・不動産"),
    ("reborisk",           "リボ払い 利息シミュレーター",             "マネー・保険・不動産"),
    ("fukuri72",           "72の法則シミュレーター",                   "マネー・保険・不動産"),
    ("taishokukin",        "退職金 手取りシミュレーター",             "仕事・働き方"),
    ("nenkin-mikomi",      "年金見込みシミュレーター",                 "仕事・働き方"),
    ("zaitaku-setsuyaku",  "在宅勤務 節約シミュレーター",             "仕事・働き方"),
    ("naishin",            "内申点シミュレーター",                     "学生・勉強"),
    ("juken-hiyou",        "受験費用シミュレーター",                   "学生・勉強"),
    ("natsuyasumi",        "夏休みの宿題シミュレーター",               "学生・勉強"),
    ("kosodate-hiyou",      "子育て費用 総額シミュレーター",      "子ども・育児"),
    ("kodomo-jikan",        "子どもと過ごせる残り時間",      "子ども・育児"),
    ("ikukyu",              "育休手当シミュレーター",      "子ども・育児"),
    ("jidou-teate",         "児童手当 総額シミュレーター",      "子ども・育児"),
    ("hoiku-youchi",        "保育園 vs 幼稚園 コスト",      "子ども・育児"),
    ("omutsu",              "おむつ 総数・費用",      "子ども・育児"),
    ("shinchou",            "子どもの身長予測",      "子ども・育児"),
    ("nezukashi",           "寝かしつけ 生涯時間",      "子ども・育児"),
    ("gakushi",             "学資 積立シミュレーター",      "子ども・育児"),
    ("okozukai",            "おこづかい 生涯総額",      "子ども・育児"),
    ("pet-age",             "犬・猫の年齢 人間換算",      "ペット"),
    ("pet-hiyou",           "ペットの生涯費用",      "ペット"),
    ("pet-jikan",           "ペットと過ごせる残り時間",      "ペット"),
    ("pet-hoken",           "ペット保険 元が取れる？",      "ペット"),
    ("sanpo",               "犬の散歩 生涯距離",      "ペット"),
    ("neko-nemuri",         "猫が寝てる時間",      "ペット"),
    ("food-ryou",           "ペットの適正フード量",      "ペット"),
    ("tatou",               "多頭飼い 費用",      "ペット"),
    ("pet-taiju",           "ペットの肥満度",      "ペット"),
    ("pet-gohan-life",      "一生で食べるフード量",      "ペット"),
    ("buzz",                "バズ偏差値メーター",      "マーケティング"),
    ("kakaku-matsu",        "松竹梅の法則",      "マーケティング"),
    ("naming-buzz",         "ネーミングバズ度診断",      "マーケティング"),
    ("gacha",               "ガチャ天井シミュレーター",      "お金・時間"),
    ("kakuyasu-sim",        "格安SIM乗り換えメーター",      "お金・時間"),
    ("jihanki",             "自販機 損失メーター",      "お金・時間"),
    ("kinenbi",             "記念日カウンター",      "恋愛・婚活"),
    ("enkyori",             "遠距離恋愛シミュレーター",      "恋愛・婚活"),
    ("aishou-seiza",        "星座の相性占い",      "恋愛・婚活"),
    ("seo-ctr",             "検索順位別クリック率",      "マーケティング"),
    ("seo-kachi",           "検索流入のお金換算",      "マーケティング"),
    ("zero-click",          "ゼロクリック検索シミュ",      "マーケティング"),
    ("ai-inyou",            "AI被引用ポテンシャル診断",      "マーケティング"),
    ("repeat-rieki",        "リピート率改善シミュ",      "マーケティング"),
    ("bmi",                 "BMI・適正体重",      "健康・カラダ"),
    ("kiso-taisha",         "基礎代謝＆必要カロリー",      "健康・カラダ"),
    ("tainai-nenrei",       "体内年齢診断",      "健康・カラダ"),
    ("suibun",              "1日の水分必要量",      "健康・カラダ"),
    ("taishibo",            "体脂肪率ざっくり推定",      "健康・カラダ"),
    ("hosu-karori",         "歩数の消費カロリー",      "健康・カラダ"),
    ("sake-karori",         "お酒のカロリー",      "健康・カラダ"),
    ("suimin-cycle",        "快眠の起床時刻",      "健康・カラダ"),
    ("suwari",              "座りすぎメーター",      "健康・カラダ"),
    ("mizu-body",           "体の水分量",      "健康・カラダ"),
    ("tanjyobi-uranai",     "誕生日でわかる運命数",      "占い・診断"),
    ("zensei",              "前世診断",      "占い・診断"),
    ("kotoshi-unsei",       "今年の運勢占い",      "占い・診断"),
    ("namae-uranai",        "名前占い",      "占い・診断"),
    ("soul-color",          "ソウルカラー診断",      "占い・診断"),
    ("doubutsu-uranai",     "誕生月の動物キャラ占い",      "占い・診断"),
    ("ketsueki-aishou",     "血液型相性占い",      "占い・診断"),
    ("lucky-today",         "今日の運勢＆ラッキー",      "占い・診断"),
    ("kyusei",              "九星気学 本命星占い",      "占い・診断"),
    ("tarot-today",         "今日の一枚タロット",      "占い・診断"),
    ("nenpi-gas",           "年間ガソリン代",      "クルマ・乗り物"),
    ("ev-vs-gas",           "EV vs ガソリン燃料費",      "クルマ・乗り物"),
    ("kuruma-yosan",        "車購入予算",      "クルマ・乗り物"),
    ("kousoku-shita",       "高速 vs 下道",      "クルマ・乗り物"),
    ("shaken-tsumitate",    "車の維持費 毎月積立",      "クルマ・乗り物"),
    ("souko-kyori",         "生涯走行距離",      "クルマ・乗り物"),
    ("chuko-nedan",         "中古車 値落ち",      "クルマ・乗り物"),
    ("drive-yosan",         "ドライブ費用",      "クルマ・乗り物"),
    ("tsukin-car",          "車通勤 vs 電車通勤",      "クルマ・乗り物"),
    ("kuruma-hoyuu",        "マイカー vs カーシェア",      "クルマ・乗り物"),
    ("ryohi",               "旅行費用 総額",      "旅行・おでかけ"),
    ("mile-tamaru",         "マイル特典航空券",      "旅行・おでかけ"),
    ("jisa-boke",           "時差ボケ回復",      "旅行・おでかけ"),
    ("kaigai-iju",          "海外移住の生活費",      "旅行・おでかけ"),
    ("tabi-tsumitate",      "旅行貯金",      "旅行・おでかけ"),
    ("lcc-shinkansen",      "LCC vs 新幹線",      "旅行・おでかけ"),
    ("gasolin-doko",        "満タンでどこまで",      "旅行・おでかけ"),
    ("onsen-seiha",         "全国制覇まで何年",      "旅行・おでかけ"),
    ("sekai-isshu",         "世界一周",      "旅行・おでかけ"),
    ("theme-park",          "テーマパーク1日予算",      "旅行・おでかけ"),
    ("yachin-tekisei",      "適正家賃シミュレーター",      "住まい・暮らし"),
    ("hikkoshi-hiyou",      "引っ越し費用",      "住まい・暮らし"),
    ("chintai-mochiie",     "賃貸 vs 持ち家 生涯コスト",      "住まい・暮らし"),
    ("denki-setsuyaku",     "電気代 節約シミュ",      "住まい・暮らし"),
    ("hitorigurashi",       "ひとり暮らし初期費用",      "住まい・暮らし"),
    ("kounetsu",            "光熱費の平均",      "住まい・暮らし"),
    ("net-hikari",          "ネット代見直し",      "住まい・暮らし"),
    ("kaji-jikan",          "家事の生涯時間",      "住まい・暮らし"),
    ("kagu-tsumitate",      "家具・家電 買い替え積立",      "住まい・暮らし"),
    ("tatami-henkan",       "部屋の広さ換算",      "住まい・暮らし"),
    ("ramen-roudou",        "ラーメン1杯の労働時間",      "グルメ・食"),
    ("gaishoku-jisui",      "外食 vs 自炊",      "グルメ・食"),
    ("issho-tabemono",      "一生で食べる量",      "グルメ・食"),
    ("conveni-super",       "コンビニ vs スーパー",      "グルメ・食"),
    ("karori-undou",        "食べ物のカロリー消費",      "グルメ・食"),
    ("cafe-nenkan",         "カフェ代 年間",      "グルメ・食"),
    ("obento-lunch",        "お弁当 vs 外食ランチ",      "グルメ・食"),
    ("tabehoudai",          "食べ放題の元取り",      "グルメ・食"),
    ("uber-jisui",          "デリバリー vs 自炊",      "グルメ・食"),
    ("nomikai-nenkan",      "飲み会の年間予算",      "グルメ・食"),
    ("lorenz",              "ローレンツ・アトラクタ",      "あそぶ・実験"),
    ("pendulum-wave",       "振り子の波",      "あそぶ・実験"),
    ("solar-system",        "太陽系シミュレーター",      "あそぶ・実験"),
    ("gravity",             "重力シミュレーター",      "あそぶ・実験"),
    ("fireworks",           "花火シミュレーター",      "あそぶ・実験"),
    ("fractal-tree",        "フラクタルの木",      "あそぶ・実験"),
    ("mandelbrot",          "マンデルブロ集合",      "あそぶ・実験"),
    ("starfield",           "ワープ星空",      "あそぶ・実験"),
    ("gears",               "歯車シミュレーター",      "あそぶ・実験"),
    ("dna",                 "DNA二重らせん",      "あそぶ・実験"),
    ("reaction-test",       "反応速度テスト",      "あそぶ・実験"),
    ("typing-test",         "タイピング速度測定",      "あそぶ・実験"),
    ("memory-test",         "記憶力テスト",      "あそぶ・実験"),
    ("spirograph",          "スピログラフ",      "あそぶ・実験"),
    ("ripple",              "波紋シミュレーター",      "あそぶ・実験"),
    ("datsumo-sougaku",     "脱毛の総額",      "美容・ファッション"),
    ("cosme-nenkan",        "コスメ代 年間",      "美容・ファッション"),
    ("fuku-shogai",         "服の生涯コスト",      "美容・ファッション"),
    ("biyoin-nenkan",       "美容院 年間費用",      "美容・ファッション"),
    ("diet-mokuhyou",       "ダイエット目標カロリー",      "美容・ファッション"),
    ("nail-matsu",          "ネイル・まつエク 年間",      "美容・ファッション"),
    ("hada-nenrei",         "肌年齢診断",      "美容・ファッション"),
    ("wardrobe",            "クローゼット稼働率",      "美容・ファッション"),
    ("kami-nobiru",         "髪が伸びるまで",      "美容・ファッション"),
    ("depacos",             "デパコス vs プチプラ",      "美容・ファッション"),
    ("marathon-yosoku",     "フルマラソン完走予測",      "スポーツ・運動"),
    ("run-pace",            "ランニング目標ペース",      "スポーツ・運動"),
    ("kintore-1rm",         "1RM計算機",      "スポーツ・運動"),
    ("tairyoku-nenrei",     "体力年齢診断",      "スポーツ・運動"),
    ("shomou-undou",        "運動の消費カロリー",      "スポーツ・運動"),
    ("golf-handi",          "ゴルフ ハンデ目安",      "スポーツ・運動"),
    ("swim-pace",           "水泳ペース換算",      "スポーツ・運動"),
    ("jitensha",            "サイクリング所要＆消費",      "スポーツ・運動"),
    ("taishibo-otoshi",     "体脂肪を落とす運動量",      "スポーツ・運動"),
    ("shinpaku-zone",       "心拍ゾーン計算",      "スポーツ・運動"),
    ("oshi-nenkan",         "推し活 年間費用",      "推し活・エンタメ"),
    ("live-ensei",          "ライブ遠征費",      "推し活・エンタメ"),
    ("subsc-motodori",      "動画サブスク 元取り",      "推し活・エンタメ"),
    ("tsumige",             "積みゲー消化",      "推し活・エンタメ"),
    ("eiga-shougai",        "一生で観る映画",      "推し活・エンタメ"),
    ("manga-otomegai",      "漫画 大人買い",      "推し活・エンタメ"),
    ("oshi-jikan",          "推しに使う時間",      "推し活・エンタメ"),
    ("ticket-tousen",       "チケット当選確率",      "推し活・エンタメ"),
    ("live-sankai",         "一生で行けるライブ回数",      "推し活・エンタメ"),
    ("goods-shuunou",       "推しグッズ収納",      "推し活・エンタメ"),
    ("stress-do",           "ストレス度診断",      "メンタル・自己分析"),
    ("seikaku-type",        "性格タイプ診断",      "メンタル・自己分析"),
    ("moeotsuki-do",        "燃え尽き度チェック",      "メンタル・自己分析"),
    ("jiko-koutei",         "自己肯定感チェック",      "メンタル・自己分析"),
    ("komyu-type",          "コミュ力タイプ診断",      "メンタル・自己分析"),
    ("kachikan",            "価値観診断",      "メンタル・自己分析"),
    ("chrono",              "朝型・夜型診断",      "メンタル・自己分析"),
    ("ketsudan",            "決断スタイル診断",      "メンタル・自己分析"),
    ("resilience",          "レジリエンス診断",      "メンタル・自己分析"),
    ("kokoro-yoyuu",        "心の余裕度チェック",      "メンタル・自己分析"),
    ("contact",            "広告掲載・タイアップのご相談",             "FOR BUSINESS"),
    ("request",            "こんなシミュ、作ってほしい！",             "REQUEST"),
    ("board",              "みんなが見たいシミュ、投票で決定",         "REQUEST BOARD"),
]

# --- 全カテゴリ3本ずつ補充分(gen_sims22〜26)を自動取り込み ---
for _m in ('gen_sims22','gen_sims23','gen_sims24','gen_sims25','gen_sims26','gen_sims_teacher','gen_sims27','gen_sims28','gen_sims29','gen_sims30','gen_sims_voice','gen_sims_seo3','gen_sims_visual','gen_sims_typeless','gen_sims_type16','gen_sims_tool','gen_sims_brain','gen_sims_tool2','gen_sims_brain2','gen_sims_petmed','gen_sims_webmkt','gen_sims_wedding','gen_sims_uranai2','gen_sims_match','gen_sims_tantei','gen_sims_kidedu','gen_sims_hikari','gen_sims_manner','gen_sims_tool3','gen_sims_brain3','gen_sims_test3','gen_sims_karada','gen_sims_ninkatsu','gen_sims_petkids','gen_sims_keisan2','gen_sims_wedding2','gen_sims_seo4','gen_sims_seo5','gen_sims_seo6','gen_sims_voice2','gen_sims_seo7','gen_sims_seo8','gen_sims_cook'):
    try:
        _mod = __import__(_m)
        for _s in _mod.SIMS:
            SIMS.append((_s['id'], _s['h1'], _s['cat']))
    except Exception as _e:
        print('skip', _m, _e)

for sid, title, cat in SIMS:
    ul = "なんとなく" if sid == "default" else None
    make_ogp(os.path.join(OGP_DIR, f"{sid}.png"), title, cat, underline=ul)

# favicon / touch icon
logo_tile(180).convert("RGB").save(os.path.join(ROOT, "apple-touch-icon.png"), "PNG")
logo_tile(32).save(os.path.join(ROOT, "favicon-32x32.png"), "PNG")
logo_tile(16).save(os.path.join(ROOT, "favicon-16x16.png"), "PNG")
print("icons: apple-touch-icon.png, favicon-32x32.png, favicon-16x16.png")
print("done.")
