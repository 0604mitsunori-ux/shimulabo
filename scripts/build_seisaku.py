"""/seisaku/（シミュレーター・診断ツールの制作のご相談）を作る（2026-10-18）。何度実行しても同じ結果。
本数（公開中・理科の授業向け）は index.html と units.json から数える。頭の部分（favicon・GA・広告タグ）は contact/index.html をそのまま使う。
あわせて、トップ・お問い合わせ・/rika/ のフッターや本文に /seisaku/ へのリンクを入れる（入っていれば何もしない）。
使い方: python scripts/build_seisaku.py
"""
import html as H
import io, json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://shimulabo.com"
rd = lambda p: io.open(os.path.join(ROOT, p), encoding="utf-8").read()
def wr(p, s): io.open(os.path.join(ROOT, p), "w", encoding="utf-8", newline="").write(s)

idx = rd("index.html")
total = int(re.search(r"<b>(\d+)</b>本 公開中", idx).group(1))
U = json.load(io.open(os.path.join(ROOT, "scripts", "rika", "units.json"), encoding="utf-8"))
rika = len({it["id"] for s in U["sections"] for g in s["groups"] for it in g["items"]})

def h1(slug):
    m = re.search(r"<h1>(.*?)</h1>", rd(f"sims/{slug}/index.html"), re.S)
    return re.sub(r"<[^>]+>", "", m.group(1)).strip()

def ex(*slugs):
    return "".join(f'<a class="related-card" href="../sims/{s}/"><span class="e">↗</span><span>{H.escape(h1(s))}</span></a>' for s in slugs)

TITLE = "シミュレーター・診断ツールの制作｜計算ツール・教材・診断コンテンツを作ります｜シミュラボ"
DESC = (f"計算・見積もりシミュレーター、診断コンテンツ、授業で使える理科シミュレーション、公開データを使ったライブ表示などを、企画から制作・設置まで承ります。"
        f"シミュラボで公開中の{total}本と同じ作り方で、貴社サイトに置ける形で納品します。")

KINDS = [
    ("🧮", "計算・見積もりツール", "住宅ローン・引っ越し費用・電気代など、数字を入れると答えと内訳が出るツール。商品やサービスの「自分の場合はいくら？」に答えて、問い合わせにつなげます。",
     ex("kariire-kanou", "hikkoshi-hiyou", "denkidai-keisan")),
    ("🔮", "診断・クイズ", "質問に答えるとタイプや点数が出る診断コンテンツ。シェアされやすく、結果ごとにおすすめの商品・サービスへ案内できます。",
     ex("aisho-16type", "stress-check", "ticket-tousen")),
    ("🔬", "学習・教材シミュレーション", f"授業や研修で、見えないものを動かして見せる教材。理科の授業向けは小学校〜高校の単元別に{rika}本を公開し、学校のタブレットで実際に使われています。",
     ex("tsuki-michikake", "kiroku-timer", "chuwa-ion")),
    ("🗾", "ライブデータ・防災", "気象庁・国土地理院などの公開データを読み込み、その日・その場所の値を表示するツール。自治体や防災・不動産の情報発信に。",
     ex("kaibatsu-check", "jishin-live", "shio-live")),
]

FAQS = [
    ("自社のサイトに置けますか？", "はい。1つのHTMLファイル（外部のライブラリなし）で納品するので、WordPress・Wix・自社CMSなどに設置できます。iframeで埋め込む形や、単独のページとしての納品もできます。"),
    ("スマホやタブレットで動きますか？", "はい。シミュラボの全ページと同じく、スマホ・タブレット（iPad・Chromebook）・パソコンのブラウザで動き、指でも操作できるように作ります。"),
    ("入力した個人情報はどうなりますか？", "計算は利用者の端末の中だけで行い、サーバーには送りません。入力内容を問い合わせフォームに引き継ぐなどの連携が必要な場合は、ご相談のうえで設計します。"),
    ("料金や期間はどれくらいですか？", "作るものの種類と規模によって変わるため、内容をうかがってからお見積りします。触れる試作を先にお見せして、方向性を確かめてから本制作に進みます。"),
    ("できあがった後の修正はできますか？", "はい。数値や文言の更新、項目の追加などのご相談を承ります。"),
]

# ---- 頭（contact と同じ部品を使い、ページ固有のところだけ差し替える）----
c = rd("contact/index.html")
head = c[:c.index("</head>")]
head = re.sub(r"<title>.*?</title>", f"<title>{TITLE}</title>", head, flags=re.S)
head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{DESC}">', head)
head = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="シミュレーター・診断ツールの制作｜シミュラボ">', head)
head = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="計算ツール・診断コンテンツ・学習用シミュレーションを、企画から制作・設置まで承ります。">', head)
head = head.replace(f"{BASE}/contact/", f"{BASE}/seisaku/").replace("/ogp/contact.png", "/ogp/seisaku.png")
head = head.replace('"name": "広告掲載・タイアップ"', '"name": "シミュレーター・診断ツールの制作"')
ld_service = {"@context": "https://schema.org", "@type": "Service", "name": "シミュレーター・診断ツールの制作",
              "serviceType": "Webシミュレーター・計算ツール・診断コンテンツ・教材シミュレーションの企画制作",
              "provider": {"@type": "Organization", "name": "シミュラボ", "url": BASE + "/"},
              "areaServed": "JP", "url": BASE + "/seisaku/", "description": DESC}
ld_faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS]}
head += ('    <script type="application/ld+json">' + json.dumps(ld_service, ensure_ascii=False) + "</script>\n"
         '    <script type="application/ld+json">' + json.dumps(ld_faq, ensure_ascii=False) + "</script>\n")
header = c[c.index("</head>"):c.index('<main class="wrap">')]

cards = "".join(f'''      <div class="menu-card">
        <div class="ic">{ic}</div>
        <h3>{t}</h3>
        <p>{d}</p>
        <div class="related-grid" style="margin-top:12px;grid-template-columns:1fr;">{links}</div>
      </div>
''' for ic, t, d, links in KINDS)
faq_dl = "".join(f"<dt>{q}</dt><dd>{a}</dd>" for q, a in FAQS)
opts = "".join(f'<option value="{t}">{t}</option>' for _, t, _, _ in KINDS) + '<option value="まだ決まっていない・相談したい">まだ決まっていない・相談したい</option>'

main = f'''<main class="wrap">

  <nav class="breadcrumb" aria-label="breadcrumb"><a href="../">ホーム</a><span>›</span><span class="cur">シミュレーター・診断ツールの制作</span></nav>

  <div class="sim-head">
    <div class="cat">FOR BUSINESS</div>
    <h1>シミュレーター・診断ツールの制作</h1>
    <p class="lead">計算・見積もりツール、診断コンテンツ、授業や研修で使う学習シミュレーション、公開データを使ったライブ表示などを、企画から制作・設置まで承ります。シミュラボで公開している{total}本と同じ作り方で、貴社のサイトに置ける形で納品します。</p>
  </div>

  <section class="panel">
    <div class="statline" style="margin-top:0;">
      <div class="stat"><div class="k">公開中のシミュレーター</div><div class="v">{total}本</div></div>
      <div class="stat"><div class="k">理科の授業向け（小〜高）</div><div class="v">{rika}本</div></div>
      <div class="stat"><div class="k">動く端末</div><div class="v" style="font-size:16px;">スマホ・タブレット・PC</div></div>
    </div>
    <p style="font-size:13.5px;color:var(--ink-2);margin:14px 0 0;line-height:1.8;">すべてブラウザだけで動き、ログインやアプリのインストールは不要です。入力した内容は端末の中で計算し、サーバーには送りません。</p>
  </section>

  <section class="panel">
    <h2>🛠️ 作れるもの（下は公開中の作例です）</h2>
    <div class="menu-grid" style="grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));">
{cards}    </div>
  </section>

  <article class="article">
    <h2>こんな目的で使われています</h2>
    <ul>
      <li><b>検索やAIからの集客</b>：「〇〇 計算」「〇〇 シミュレーション」で調べる人に、答えそのものを出すページは見られやすく、AIの回答に引用されることもあります。</li>
      <li><b>問い合わせ・資料請求につなげる</b>：結果のすぐ下に「くわしく相談する」を置き、自分ごとになったタイミングで案内できます。</li>
      <li><b>授業・研修・説明会</b>：電子黒板やタブレットで、条件を変えると結果が変わる様子をその場で見せられます。</li>
      <li><b>展示・イベント</b>：タブレット1台で、来場者が触って遊べるコンテンツとして使えます。</li>
    </ul>
    <h2>納品の形</h2>
    <table>
      <tr><th>形</th><th>内容</th></tr>
      <tr><td>貴社サイトに設置</td><td>1つのHTMLファイル（外部ライブラリなし）で納品。WordPressなどに設置、またはiframeで埋め込み。</td></tr>
      <tr><td>単独のページ</td><td>独自ドメインやキャンペーンページとして公開。</td></tr>
      <tr><td>シミュラボで共同公開</td><td>シミュラボ上に貴社提供のシミュレーターとして掲載（タイアップ）。</td></tr>
    </table>
    <h2>進め方</h2>
    <ol>
      <li><b>ご相談</b>：作りたいもの・使う場面・置き場所をうかがいます（無料）。</li>
      <li><b>企画と試作</b>：計算式や問いの内容を整理し、触れる試作を先にお見せします。</li>
      <li><b>制作・確認</b>：数値の照合、スマホ・タブレットでの表示確認をして仕上げます。</li>
      <li><b>公開・計測</b>：設置のお手伝いと、使われ方の計測（任意）まで。</li>
    </ol>
  </article>

  <section class="panel" id="form">
    <h2>✉️ 制作のご相談</h2>
    <div class="field">
      <label>会社名・団体名 <span class="hint">（任意）</span></label>
      <input type="text" id="company" placeholder="例：株式会社○○／○○市">
    </div>
    <div class="row">
      <div class="field">
        <label>ご担当者名 <span class="hint">（必須）</span></label>
        <input type="text" id="person" placeholder="例：山田 太郎">
      </div>
      <div class="field">
        <label>メールアドレス <span class="hint">（必須）</span></label>
        <input type="email" id="email" placeholder="例：you@example.com">
      </div>
    </div>
    <div class="field">
      <label>作りたいもの <span class="hint">（必須）</span></label>
      <select id="type">{opts}</select>
    </div>
    <div class="field">
      <label>ご相談内容 <span class="hint">（必須）</span></label>
      <textarea id="message" placeholder="作りたいもの・使う場面・置きたいサイト・ご希望の時期などをご記入いただけるとスムーズです。"></textarea>
    </div>
    <button class="btn btn-primary" id="sendBtn">この内容で相談する</button>
    <p id="formNote" style="font-size:13px;color:var(--ink-2);margin:14px 0 0;text-align:center;">送信ボタンを押すと、メールソフトが起動します。</p>
    <p style="font-size:13px;color:var(--ink-2);margin:10px 0 0;text-align:center;">広告掲載・記事タイアップのご相談は<a href="../contact/">こちら</a></p>
  </section>

  <article class="article">
    <h2>よくあるご質問</h2>
    <dl class="faq">{faq_dl}</dl>
  </article>

</main>
'''

footer = c[c.index('<footer class="site-footer">'):c.index("<script>\n(() => {")]
js = c[c.index("<script>\n(() => {"):]
js = js.replace("const subject = `【シミュラボ】広告掲載・タイアップのお問い合わせ（${$('type').value}）`;",
                "const subject = `【シミュラボ】制作のご相談（${$('type').value}）`;")
js = js.replace("■ご相談の種類：", "■作りたいもの：").replace("■会社名・媒体名：", "■会社名・団体名：")
assert "制作のご相談" in js
os.makedirs(os.path.join(ROOT, "seisaku"), exist_ok=True)
wr("seisaku/index.html", head + header + main + "\n" + footer + js)
print(f"seisaku/index.html（公開中{total}本・理科{rika}本）")

# ---- OGP ----
p = os.path.join(ROOT, "ogp", "seisaku.png")
if not os.path.exists(p):
    gen = os.path.join(ROOT, "scripts", "gen_images.py"); ns = {"__file__": gen}
    exec(compile(rd("scripts/gen_images.py").split("\nSIMS = [")[0], gen, "exec"), ns)
    ns["make_ogp"](p, "シミュレーター・診断ツールの制作", "FOR BUSINESS", underline="制作")
    print("OGP:", p)

# ---- 導線（入っていなければ足す）----
LINK = '<a href="seisaku/">シミュレーター制作のご相談</a>'
t = rd("index.html")
if "seisaku/" not in t:
    t = t.replace('      <a href="contact/">広告掲載・タイアップ</a>\n', '      ' + LINK + '\n      <a href="contact/">広告掲載・タイアップ</a>\n', 1)
    assert "seisaku/" in t; wr("index.html", t); print("トップのフッターにリンク")
t = rd("contact/index.html")
if "../seisaku/" not in t:
    t = t.replace('<h3>オリジナル診断ツール制作</h3>\n        <p>貴社専用のシミュレーター／診断ツールを共同で企画・開発。リード獲得や販促に。</p>',
                  '<h3>オリジナル診断ツール制作</h3>\n        <p>貴社専用のシミュレーター／診断ツールを共同で企画・開発。リード獲得や販促に。<a href="../seisaku/">くわしくはこちら →</a></p>', 1)
    assert "../seisaku/" in t; wr("contact/index.html", t); print("お問い合わせからリンク")
