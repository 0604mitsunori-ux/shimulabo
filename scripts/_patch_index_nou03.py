# -*- coding: utf-8 -*-
"""十人十脳と連動するテスト 第3〜7弾（1回限り・2026-11-05）
   - 新規20本：トップのカード＋ランキング＋公開本数、share.js の ALLOW、sitemap
   - 作り直し5本（tango-kioku / chrono / rhythm-test / hsp-shindan / iq-test）：トップのカードの題と説明を新しい中身に、sitemap の更新日を今日に
   - シェア画像は プロジェクト/YouTube脳科学チャンネル/クリエイティブ/診断ページOGP/ で作ったものを ogp/ に写す
   ページ本体は scripts/gen_nou_pages.py で作る
"""
import io, os, re, shutil

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPTS)
OGP_SRC = r"C:\Users\pc\Desktop\Nsawa\プロジェクト\YouTube脳科学チャンネル\クリエイティブ\診断ページOGP"
TODAY = "2026-11-05"
GRAD = "linear-gradient(135deg,#f0fdfa,#ccfbf1)"

NEW = [  # (slug, emoji, タイトル, カード説明, score)
    ("onkan-test", "🎹", "絶対音感・相対音感テスト", "鳴った音のドレミ、分かる？2つの音の高い・低いも聞き分ける。", 54),
    ("sakuchou-test", "🔊", "音の錯覚テスト（上がる？下がる？）", "同じ2つの音なのに、上がって聞こえる人と下がって聞こえる人がいる。", 53),
    ("sakushi-kaiten", "💃", "回転の錯視テスト（どっち回り？）", "回る向きの手がかりがない玉。あなたの頭は、どちら回りに決める？", 54),
    ("hybrid-gazou", "👓", "近くと遠くで変わる数字テスト", "1枚の絵に2つの数字。近くと遠くで、見える数字が入れかわる。", 55),
    ("dunning-kruger", "🤔", "ダニング＝クルーガー効果テスト", "解く前の予想と、実際の点数。自分の実力、正しく見積もれる？", 54),
    ("ao-midori", "🟦", "青と緑の境目テスト", "青から緑へ変わる12色。あなたの「青」はどこまで？信号が青と呼ばれる理由も。", 53),
    ("dress-iro", "👗", "ドレスの色テスト（白と金？青と黒？）", "同じ色の布なのに、光しだいで見え方が変わる。頭の「光の思いこみ」を試す。", 55),
    ("hidarikiki", "✋", "利き手・利き目・利き足チェック", "8つの動作で利き手の度合いを数字に。左利きは10人に1人。", 54),
    ("shikou-type", "🧠", "考え方のタイプ診断（絵・図・言葉）", "頭の中で、絵で考える？言葉で考える？3つのタイプに分けて。", 53),
    ("kao-kioku", "🙂", "顔の記憶力テスト", "8人の顔を20秒で覚えて、よく似た顔の中から当てる。", 54),
    ("houkou-kankaku", "🧭", "方向音痴テスト（図形を回せる？）", "頭の中で図形を回す10問と、方向感覚の5つの質問。", 54),
    ("jikan-kankaku", "⏱️", "時間感覚テスト（目を閉じて30秒）", "時計を見ずに10秒・30秒・60秒。あなたの頭の中の時計は速い？遅い？", 54),
    ("kazu-shunkan", "🔢", "数の瞬間テスト（一瞬で数が分かる？）", "0.2秒だけ出る点の数を当てる。パッと分かるのは何個まで？", 53),
    ("yomu-hayasa", "📖", "読む速さテスト（1分間に何文字？）", "短いお話を読んで、読む速さと内容の理解を同時に測る。", 53),
    ("mikaku-type", "🌿", "味覚タイプ診断（パクチー・苦み）", "パクチーが石けんの味？苦みに敏感？10問であなたの舌のタイプを。", 54),
    ("mcgurk-test", "👄", "マガーク効果テスト（目で聞く音）", "同じ「ば」の声が、口の動きで「だ」に聞こえる？", 53),
    ("yume-type", "💭", "夢タイプ診断", "毎晩夢を覚えている人と、ほとんど覚えていない人のちがい。", 53),
    ("torihada-test", "🎵", "音楽で鳥肌が立つ？テスト", "同じ曲で鳥肌が立つ人と立たない人。鳥肌タイプ？涙タイプ？", 53),
    ("shinpaku-kankaku", "💓", "心臓の音が分かる？テスト", "脈にさわらずに数えた心拍と、実際の脈をくらべる。", 53),
    ("akubi-test", "🥱", "あくびがうつる？テスト", "あくびをするアニメを1分間。あなたのあくびは、うつる？", 54),
]
REBUILT = [  # (slug, 今のカード, 新しいカード)
    ("tango-kioku", "<h3>単語記憶テスト</h3><p>いくつ覚えられる？記憶力チェック</p>",
     "<h3>単語記憶テスト</h3><p>12個の言葉、すぐあとと少しあとで、どれだけ残る？</p>"),
    ("chrono", "<h3>朝型・夜型診断</h3><p>あなたの最適な時間帯は？</p>",
     "<h3>朝型・夜型診断（クロノタイプ）</h3><p>8つの質問で朝型・夜型の傾向を。約70万人の遺伝子研究の話も。</p>"),
    ("rhythm-test", "<h3>リズム感テスト</h3><p>ビートに合わせてタップ</p>",
     "<h3>リズム感テスト</h3><p>音に合わせてタップ。拍よりどのくらい早い？音が消えても続けられる？</p>"),
    ("hsp-shindan", "<h3>HSP診断（繊細さん）</h3><p>あなたの繊細さレベルを12問でチェック。</p>",
     "<h3>HSP診断（繊細さん）</h3><p>12問で繊細さの4つの面を。蘭・チューリップ・タンポポ、あなたはどれ？</p>"),
    ("iq-test", "<h3>IQテスト（簡易版）</h3><p>10問で論理思考力をチェック</p>",
     "<h3>IQテスト（パターン問題と「見ない力」）</h3><p>パターン問題8問と、一瞬だけ動くしま模様。IQが高い人は何を見ていない？</p>"),
]

for slug in [r[0] for r in REBUILT] + [n[0] for n in NEW]:
    shutil.copyfile(os.path.join(OGP_SRC, slug + ".png"), os.path.join(ROOT, "ogp", slug + ".png"))
    assert os.path.isfile(os.path.join(ROOT, "sims", slug, "index.html")), slug

IDX = os.path.join(ROOT, "index.html")
html = io.open(IDX, encoding="utf-8").read()
assert "sims/akubi-test/" not in html, "既に挿入済み（中止）"

for slug, old, new in REBUILT:
    assert html.count(old) == 1, slug
    html = html.replace(old, new)

cards = "".join("""    <a class="sim-card" data-cat="brain" href="sims/%s/">
      <div class="thumb" style="background:%s"><span class="emoji">%s</span></div>
      <div class="body"><div class="cat">脳トレ・診断テスト</div><h3>%s</h3><p>%s</p><span class="go">触ってみる →</span></div>
    </a>
""" % (s, GRAD, e, t, d) for s, e, t, d, _ in NEW)
marker = '    <a class="req-card" href="request/">'
assert marker in html
html = html.replace(marker, cards + marker, 1)

idx = html.index("\n  ];")
before = html[:idx].rstrip()
if not before.endswith(","):
    before += ","
html = before + "\n" + ",\n".join("    { href: 'sims/%s/', emoji: '%s', title: '%s', cat: '脳トレ・診断テスト', score: %d }" % (s, e, t, sc) for s, e, t, _, sc in NEW) + html[idx:]

m = re.search(r"<b>(\d+)</b>本 公開中", html); cnt = int(m.group(1))
html = html.replace("<b>%d</b>本 公開中" % cnt, "<b>%d</b>本 公開中" % (cnt + len(NEW)), 1)
io.open(IDX, "w", encoding="utf-8").write(html)
print("index.html: +%d cards, count=%d" % (len(NEW), cnt + len(NEW)))

SH = os.path.join(ROOT, "api", "share.js")
js = io.open(SH, encoding="utf-8").read()
for s, *_ in NEW:
    if "'%s'" % s not in js:
        js = js.replace("'hsp-shindan'", "'hsp-shindan', '%s'" % s, 1)
io.open(SH, "w", encoding="utf-8").write(js)

SM = os.path.join(ROOT, "sitemap.xml")
sm = io.open(SM, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in sm else "\n"
for slug, *_ in REBUILT:
    sm, n = re.subn(r"(<loc>https://shimulabo.com/sims/%s/</loc><lastmod>)[\d-]+" % re.escape(slug), r"\g<1>" + TODAY, sm)
    assert n == 1, slug
sm = sm.replace("</urlset>", "".join("  <url><loc>https://shimulabo.com/sims/%s/</loc><lastmod>%s</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>%s" % (s, TODAY, nl) for s, *_ in NEW) + "</urlset>")
io.open(SM, "w", encoding="utf-8", newline="").write(sm)
print("share.js / sitemap.xml updated")
