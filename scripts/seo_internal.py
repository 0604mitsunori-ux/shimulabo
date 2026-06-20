# -*- coding: utf-8 -*-
"""シミュラボ 内部SEO一括適用（冪等）
   - canonical / og:locale / robots メタ
   - JSON-LD（WebSite+Organization / WebApplication / FAQPage / BreadcrumbList）
   - パンくず（表示） / 関連シミュ内部リンク
   - sitemap.xml / robots.txt 生成
   公開時は BASE を実ドメインへ find/replace すること。
"""
import os, re, glob, json, html as htmllib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://shimulabo.com"   # ★公開時に実ドメインへ置換

HEAD_MARK = "<!-- seo-internal -->"
BC_MARK   = 'class="breadcrumb"'
REL_MARK  = 'class="related"'

# シミュのメタ（id, タイトル, 絵文字, カテゴリ, 説明）
SIMS = [
    ("kaigi-cost",         "会議コストシミュレーター",             "🔥", "お金・時間",     "参加人数と年収から、会議中に溶けていく人件費をリアルタイム計算。"),
    ("kuchikomi-hakyu",    "口コミ波及シミュレーター",             "📈", "店舗・ビジネス", "店舗の口コミが集客にどれだけ波及するかを12か月でシミュレーション。"),
    ("jutai",              "渋滞は勝手に生まれる",                 "🚗", "ふしぎ・現象",   "事故ゼロでも渋滞の波が発生する自然渋滞をリング道路で再現。"),
    ("life",               "ライフゲーム",                         "🦠", "ふしぎ・現象",   "3つのルールだけで生命のようなパターンが生まれるライフゲーム。"),
    ("forest-fire",        "森林火災シミュレーター",               "🔥", "ふしぎ・現象",   "木の密度を超えると一気に燃え広がる浸透の臨界を体感。"),
    ("schelling",          "街の分断シミュレーター",               "🏘️", "ふしぎ・現象",   "弱い好みだけで街が分断されるシェリングの分居モデル。"),
    ("sandpile",           "砂山崩しシミュレーター",               "⛰️", "ふしぎ・現象",   "砂を積むとある時 突然 大崩壊が起きる自己組織化臨界。"),
    ("boids",              "鳥の群れシミュレーター（ボイド）",     "🐦", "ふしぎ・現象",   "3つのルールだけで群れが生まれるボイドモデル。"),
    ("double-pendulum",    "二重振り子シミュレーター",             "🌀", "ふしぎ・現象",   "わずかな初期差が大きな違いを生む二重振り子のカオス。"),
    ("wave",               "波の干渉シミュレーター",               "🌊", "ふしぎ・現象",   "2つの波が重なって生まれる干渉のしま模様を体感。"),
    ("diffusion",          "拡散シミュレーター",                   "🫧", "ふしぎ・現象",   "2色の粒子が混ざって戻らない不可逆性（エントロピー）。"),
    ("turing",             "模様が生まれるシミュレーター",         "🐆", "ふしぎ・現象",   "反応拡散でヒョウ柄やシマ模様が生まれるチューリングパターン。"),
    ("sync",               "同期現象シミュレーター",               "✨", "ふしぎ・現象",   "バラバラのホタルが勝手に点滅を揃える同期現象。"),
    ("machi-jikan",        "人生の「待ち時間」シミュレーター",     "⏳", "人生・自分ごと", "信号・レジ・電車・読み込み…生涯で待つだけに使う時間を計算。"),
    ("scroll-distance",    "スクロール距離メーター",               "📱", "人生・自分ごと", "スマホ時間から、親指が1年でスクロールする距離をエベレスト換算。"),
    ("influencer-soroban", "インフルエンサー皮算用シミュレーター", "🦝", "マーケティング", "フォロワー数から皮算用の月収と脳内ランクを判定するジョークツール。"),
    ("catchcopy",          "うさんくさいキャッチコピー製造機",     "🪧", "マーケティング", "商品名を入れるだけでうさんくさい広告コピーを量産するジョークツール。"),
    ("subsc",              "サブスク墓場シミュレーター",           "💸", "お金・時間",     "使ってないサブスクに1年・10年で捨てている金額を計算。"),
    ("caffeine",           "カフェイン残量シミュレーター",         "☕", "人生・自分ごと", "就寝時に体内へ残るカフェイン量を半減期で計算。"),
    ("sleep-debt",         "睡眠負債シミュレーター",               "😴", "人生・自分ごと", "平日の睡眠から1年で積み上がる睡眠負債を計算。"),
    ("warikan",            "割り勘の不公平シミュレーター",         "🍻", "お金・時間",     "飲み会の割り勘で損得いくらかを飲んだ量から計算。"),
    ("takarakuji",         "宝くじ買い続けたらシミュレーター",     "🎰", "お金・時間",     "買い続けた総額・期待回収・運用との差を計算。"),
    ("oyako",              "あと何回、親に会えるか",               "👨‍👩‍👧", "人生・自分ごと", "親の年齢と会う回数から残りの回数を計算。"),
    ("infure",             "物価2倍まで何年？シミュレーター",       "📉", "お金・時間",     "インフレ率から物価2倍までの年数とお金の目減りを計算。"),
    ("if-company",         "もしあなたが会社だったら",             "🏢", "マーケティング", "年収・支出・貯金から時価総額と格付けを算出するジョーク。"),
    ("nidone",             "二度寝損失シミュレーター",             "🛌", "人生・自分ごと", "二度寝に1年で溶かす時間を映画何本分かで可視化。"),
    ("chiritsumo",         "塵も積もればシミュレーター",           "🪙", "お金・時間",     "毎日の小さな出費が積もる総額と運用との差を計算。"),
    ("shutten",            "出店集客シミュレーター",               "🏪", "店舗・ビジネス", "業種・立地・商圏から出店1年目の集客を試算。MEO対策での伸びしろも算出。"),
    ("tenshoku",           "転職 年収ifシミュレーター",           "🔀", "仕事・働き方",     "転職した場合としない場合の生涯年収の差を昇給率込みで試算。"),
    ("fire",               "FIRE達成シミュレーター",               "🔥", "お金・時間",     "毎月の投資額と利回りからFIRE達成までの年数を試算。"),
    ("kyuryobi",           "あと何回給料日シミュレーター",         "📆", "お金・時間",     "定年までに受け取る給料日の残り回数を計算。"),
    ("coffee-life",        "コーヒー一生分シミュレーター",         "☕", "お金・時間",     "一生で飲むコーヒーの杯数・総額・カフェイン量を計算。"),
    ("yoi",                "酔いがさめるまでシミュレーター",       "🍺", "人生・自分ごと", "飲んだ量と体重からアルコールが抜ける時間を概算。"),
    ("taiju",              "半年後の体重シミュレーター",           "⚖️", "人生・自分ごと", "1日のカロリー収支から半年後・1年後の体重を予測。"),
    ("unmei",              "運命の人に出会う確率",                 "💘", "恋愛・婚活", "人口と条件から運命の人候補と出会う確率を試算。"),
    ("mental-age",         "精神年齢診断",                         "🧠", "人生・自分ごと", "5つの質問で精神年齢とおじさん度を診断。"),
    ("isekai",             "異世界転生チート度診断",               "🗡️", "人生・自分ごと", "現代スキルから異世界転生時のチート度を診断。"),
    ("neage",              "値上げ客数シミュレーター",             "🏷️", "店舗・ビジネス", "価格弾力性から値上げ時の客数と売上への影響を試算。"),
    ("konkatsu-match",     "婚活マッチ診断",                       "💍", "恋愛・婚活", "年齢と条件から釣り合いやすい相手像と出会い方を試算（点数化しない）。"),
    ("konkatsu-jouken",    "婚活 条件マッチ診断",                  "💕", "恋愛・婚活", "理想の条件を満たす人数と、条件を緩めると候補が何倍になるかを試算。"),
    ("konkatsu-type",      "婚活 相性タイプ診断",                  "🫶", "恋愛・婚活", "5つの質問で価値観タイプと相性の良い相手・婚活法を診断。"),
    ("kokuhaku",           "告白成功率シミュレーター",             "💌", "恋愛・婚活", "相手との関係や脈ありサインから告白の成功率を診断。"),
    ("ryomoi",             "両思い度診断",                         "💞", "恋愛・婚活", "相手の言動から両思いの可能性を5つの質問で診断。"),
    ("aisho-name",         "名前で相性占い",                       "💘", "恋愛・婚活", "二人の名前から相性を占う定番の相性占い。"),
    ("same-class",         "好きな人と同じクラスになる確率",       "🏫", "恋愛・婚活", "クラス数から好きな人と同じクラスになる確率を計算（中高生向け）。"),
    ("moteki",             "モテ期はいつ来る？診断",               "🌟", "恋愛・婚活", "年齢と調子から次のモテ期がいつ来るかを占う恋愛診断。"),
    ("ad-roas",            "広告ROAS試算シミュレーター",           "📊", "店舗・ビジネス", "広告費とCVR・客単価からROASと差引利益を試算。"),
    ("ltv",                "LTVシミュレーター",                     "🔁", "店舗・ビジネス", "客単価と来店頻度からLTVと獲得コスト上限を試算。"),
    ("coupon",             "クーポン採算シミュレーター",           "🎟️", "店舗・ビジネス", "割引と原価率・リピート率からクーポン施策の利益を試算。"),
    ("chirashi-web",       "チラシ vs Web広告シミュレーター",      "📰", "店舗・ビジネス", "同じ予算でチラシとWeb広告の集客数を比較。"),
    ("jutaku-loan",        "住宅ローン返済シミュレーター",         "🏠", "マネー・保険・不動産", "借入額と金利・年数から毎月返済額・総利息を計算。"),
    ("kuriage",            "繰上返済 効果シミュレーター",         "💴", "マネー・保険・不動産", "繰上返済で短縮できる期間と減る利息を試算。"),
    ("hosho",              "必要保障額シミュレーター",             "🛡️", "マネー・保険・不動産", "遺族の生活費と貯蓄・遺族年金から必要保障額を試算。"),
    ("rougo",              "老後資金シミュレーター",               "👴", "マネー・保険・不動産", "年金と生活費から老後に不足する資金を試算。"),
    ("zangyo",             "残業代シミュレーター",                 "🕒", "仕事・働き方", "月給と残業時間から月・年の残業代を計算。"),
    ("yukyu",              "有給消化シミュレーター",               "🏖️", "仕事・働き方", "残っている有給を金額に換算。"),
    ("freelance",          "フリーランス手取りシミュレーター",     "🧑‍💻", "仕事・働き方", "売上と経費から税・社保を引いた手取りをざっくり試算。"),
    ("tsukin",             "通勤時間の生涯コスト",                 "🚃", "仕事・働き方", "片道の通勤時間から生涯の通勤時間を日数換算。"),
    ("goukaku",            "合格可能性シミュレーター",             "✏️", "学生・勉強", "偏差値と残り期間から志望校の合格可能性を診断。"),
    ("benkyo-time",        "勉強時間シミュレーター",               "📚", "学生・勉強", "1日の勉強時間から受験までの総時間とライバル差を可視化。"),
    ("gakuhi",             "学費総額シミュレーター",               "🎓", "学生・勉強", "進路と下宿の有無から大学卒業までの教育費総額を試算。"),
    ("bukatsu",            "部活引退カウントダウン",               "🏃", "学生・勉強", "学年と引退時期から部活引退までの残り日数を計算。"),
    ("bep",                "損益分岐点シミュレーター",             "⚖️", "店舗・ビジネス", "固定費と粗利率から黒字に必要な売上と客数を計算。"),
    ("noshow",             "ノーショー損失シミュレーター",         "🚫", "店舗・ビジネス", "予約の無断キャンセルで失う金額を月・年で試算。"),
    ("jinkenhi",           "人件費率診断シミュレーター",           "👥", "店舗・ビジネス", "月商と人件費から人件費率を業種目安と比較。"),
    ("nisa",               "NISA積立シミュレーター",               "📈", "マネー・保険・不動産", "毎月の積立と利回りから将来資産を複利で計算。"),
    ("kuruma-iji",         "車の維持費シミュレーター",             "🚙", "マネー・保険・不動産", "ガソリン・保険・車検等から年間維持費と総額を計算。"),
    ("furusato",           "ふるさと納税 上限額シミュレーター",     "🎁", "マネー・保険・不動産", "年収と家族構成からふるさと納税の上限額の目安を試算。"),
    ("jikkou-jikyu",       "実質時給シミュレーター",               "⏱️", "仕事・働き方", "残業込みの総労働時間で割った実質時給を計算。"),
    ("fukugyo-zei",        "副業の税金・手取りシミュレーター",     "💸", "仕事・働き方", "副業所得から確定申告の要否と税・手取りを試算。"),
    ("shouyo-tedori",      "ボーナス手取りシミュレーター",         "💰", "仕事・働き方", "ボーナス額面から社保・税を引いた手取りを試算。"),
    ("tango",              "英単語マスター日数シミュレーター",     "📖", "学生・勉強", "単語数と1日のペースから覚え終わる日数を計算。"),
    ("shogakukin",         "奨学金返済シミュレーター",             "🎓", "学生・勉強", "借入額・利率・年数から毎月返済額と総利息を計算。"),
    ("benkyo-target",      "目標点までの勉強量シミュレーター",     "🎯", "学生・勉強", "目標点と残り日数から1日に必要な勉強時間を逆算。"),
    ("kaiten",             "回転率シミュレーター",                 "🍽️", "店舗・ビジネス", "席数・回転数・客単価から飲食店の1日・月の売上を試算。"),
    ("line-cv",            "LINE・メルマガ配信効果シミュレーター", "✉️", "店舗・ビジネス", "配信数と開封率・購入率から1回の配信の売上を試算。"),
    ("zaiko",              "在庫の持ちすぎコストシミュレーター",   "📦", "店舗・ビジネス", "在庫金額と保管・廃棄率から持ちすぎコストを年で試算。"),
    ("chochiku-mokuhyo",   "目標金額までの積立シミュレーター",     "🎯", "マネー・保険・不動産", "目標額・利回り・年数から必要な毎月の積立額を逆算。"),
    ("reborisk",           "リボ払い 利息シミュレーター",         "💳", "マネー・保険・不動産", "リボ残高と年率・返済額から完済期間と総利息を計算。"),
    ("fukuri72",           "72の法則シミュレーター",               "✨", "マネー・保険・不動産", "利回りからお金が2倍になる年数を72の法則で計算。"),
    ("taishokukin",        "退職金 手取りシミュレーター",         "🎁", "仕事・働き方", "退職金の額面と勤続年数から税引き後の手取りを試算。"),
    ("nenkin-mikomi",      "年金見込みシミュレーター",             "🧓", "仕事・働き方", "平均年収と加入年数から将来の年金額の目安を試算。"),
    ("zaitaku-setsuyaku",  "在宅勤務 節約シミュレーター",         "🏠", "仕事・働き方", "昼食代と通勤時間から在宅勤務で浮くお金と時間を試算。"),
    ("naishin",            "内申点シミュレーター",                 "📋", "学生・勉強", "9教科の評定から内申点の目安を計算（実技2倍対応）。"),
    ("juken-hiyou",        "受験費用シミュレーター",               "💰", "学生・勉強", "受験校数・受験料・入学金から受験の総費用を試算。"),
    ("natsuyasumi",        "夏休みの宿題シミュレーター",           "🌻", "学生・勉強", "残りの宿題量と日数から1日のノルマと間に合うかを計算。"),
]
SIM_BY_ID = {s[0]: s for s in SIMS}

# サブページ（パンくず用ラベル）
SUBPAGES = {
    "contact": "広告掲載・タイアップ",
    "request": "リクエスト",
    "board":   "リクエストボード",
    "terms":   "利用規約",
    "privacy": "プライバシーポリシー",
}

def page_meta(path):
    rel = os.path.relpath(path, ROOT).replace("\\", "/")
    parts = rel.split("/")
    if rel == "index.html":
        return {"kind": "home", "url": "/", "prefix": ""}
    if parts[0] == "sims" and len(parts) == 3:
        return {"kind": "sim", "id": parts[1], "url": f"/sims/{parts[1]}/", "prefix": "../../"}
    if parts[0] in SUBPAGES:
        return {"kind": "sub", "id": parts[0], "url": f"/{parts[0]}/", "prefix": "../"}
    return {"kind": "other", "url": "/" + "/".join(parts[:-1]) + "/", "prefix": "../"}

def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + '</script>'

def extract_faq(htmltext):
    m = re.search(r'<dl class="faq">(.*?)</dl>', htmltext, re.S)
    if not m: return []
    block = m.group(1)
    dts = re.findall(r'<dt>(.*?)</dt>', block, re.S)
    dds = re.findall(r'<dd>(.*?)</dd>', block, re.S)
    out = []
    for q, a in zip(dts, dds):
        q = htmllib.unescape(re.sub(r'<[^>]+>', '', q)).strip()
        a = htmllib.unescape(re.sub(r'<[^>]+>', '', a)).strip()
        if q and a:
            out.append((q, a))
    return out

def head_block(meta, htmltext):
    url = BASE + meta["url"]
    lines = [
        HEAD_MARK,
        f'<link rel="canonical" href="{url}">',
        '<meta property="og:locale" content="ja_JP">',
        '<meta name="robots" content="index,follow">',
    ]
    blocks = []
    if meta["kind"] == "home":
        blocks.append(jsonld({
            "@context": "https://schema.org", "@type": "WebSite",
            "name": "シミュラボ", "url": BASE + "/", "inLanguage": "ja",
            "description": "身近なギモンや現象を、入力するだけで数字とアニメで体感できる無料シミュレーター集。"
        }))
        blocks.append(jsonld({
            "@context": "https://schema.org", "@type": "Organization",
            "name": "シミュラボ", "url": BASE + "/", "logo": BASE + "/apple-touch-icon.png"
        }))
    elif meta["kind"] == "sim":
        sid = meta["id"]; _, title, _, cat, desc = SIM_BY_ID[sid]
        blocks.append(jsonld({
            "@context": "https://schema.org", "@type": "WebApplication",
            "name": title, "url": url, "description": desc,
            "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any",
            "inLanguage": "ja", "isAccessibleForFree": True,
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "JPY"},
            "publisher": {"@type": "Organization", "name": "シミュラボ", "url": BASE + "/"}
        }))
        blocks.append(jsonld({
            "@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "ホーム", "item": BASE + "/"},
                {"@type": "ListItem", "position": 2, "name": title, "item": url},
            ]
        }))
        faq = extract_faq(htmltext)
        if faq:
            blocks.append(jsonld({
                "@context": "https://schema.org", "@type": "FAQPage",
                "mainEntity": [
                    {"@type": "Question", "name": q,
                     "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq
                ]
            }))
    elif meta["kind"] == "sub":
        label = SUBPAGES[meta["id"]]
        blocks.append(jsonld({
            "@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "ホーム", "item": BASE + "/"},
                {"@type": "ListItem", "position": 2, "name": label, "item": url},
            ]
        }))
    return "\n".join("    " + l for l in lines) + "\n" + "\n".join("    " + b for b in blocks)

def breadcrumb_html(meta):
    home = meta["prefix"] + "index.html"
    if meta["kind"] == "sim":
        _, title, _, cat, _ = SIM_BY_ID[meta["id"]]
        mid = f'{htmllib.escape(cat)}<span>›</span>'
        cur = htmllib.escape(title)
    elif meta["kind"] == "sub":
        mid = ""; cur = htmllib.escape(SUBPAGES[meta["id"]])
    else:
        return None
    return (f'  <nav class="breadcrumb" aria-label="breadcrumb">'
            f'<a href="{home}">ホーム</a><span>›</span>{mid}'
            f'<span class="cur">{cur}</span></nav>\n')

def related_html(sid):
    cur = SIM_BY_ID[sid]
    same = [s for s in SIMS if s[0] != sid and s[3] == cur[3]]
    other = [s for s in SIMS if s[0] != sid and s[3] != cur[3]]
    picks = (same + other)[:3]
    cards = "".join(
        f'<a class="related-card" href="../{s[0]}/index.html"><span class="e">{s[2]}</span><span>{htmllib.escape(s[1])}</span></a>'
        for s in picks
    )
    return ('  <nav class="related" aria-label="related">\n'
            '    <h2>ほかのシミュレーション</h2>\n'
            f'    <div class="related-grid">{cards}</div>\n'
            '  </nav>\n\n')

# ---- 各ページ適用 ----
patched = 0
for path in glob.glob(os.path.join(ROOT, "**", "index.html"), recursive=True):
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    meta = page_meta(path)
    changed = False

    if HEAD_MARK not in html and "</head>" in html:
        html = html.replace("</head>", head_block(meta, html) + "\n</head>", 1)
        changed = True

    if BC_MARK not in html:
        bc = breadcrumb_html(meta)
        if bc and '<div class="sim-head">' in html:
            html = html.replace('  <div class="sim-head">', bc + '\n  <div class="sim-head">', 1)
            changed = True

    if meta["kind"] == "sim" and REL_MARK not in html:
        anchor = '  </article>\n\n  <section class="req-banner">'
        if anchor in html:
            html = html.replace(anchor, '  </article>\n\n' + related_html(meta["id"]) + '  <section class="req-banner">', 1)
            changed = True

    if changed:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        patched += 1
        print("seo:", os.path.relpath(path, ROOT), "->", meta["kind"])

# ---- sitemap.xml ----
urls = ["/"] + [f"/sims/{s[0]}/" for s in SIMS] + [f"/{k}/" for k in SUBPAGES]
sm = ['<?xml version="1.0" encoding="UTF-8"?>',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in urls:
    pr = "1.0" if u == "/" else ("0.8" if u.startswith("/sims/") else "0.5")
    sm.append(f"  <url><loc>{BASE}{u}</loc><changefreq>weekly</changefreq><priority>{pr}</priority></url>")
sm.append("</urlset>")
with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write("\n".join(sm) + "\n")

# ---- robots.txt ----
with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
    f.write("User-agent: *\nAllow: /\n\nSitemap: " + BASE + "/sitemap.xml\n")

print(f"done. {patched} pages patched. sitemap.xml / robots.txt written.")
