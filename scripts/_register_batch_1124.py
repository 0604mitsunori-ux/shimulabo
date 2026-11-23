# -*- coding: utf-8 -*-
"""2026-11-24 追加の10本を、トップ・llms.txt・サイトマップ・share.js・OGP に登録する（冪等）。
   使い方: python -X utf8 scripts/_register_batch_1124.py  （ITEMS のうち sims/<slug>/index.html があるものだけ登録）"""
import io, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rd = lambda p: io.open(os.path.join(ROOT, p), encoding="utf-8").read()
def wr(p, s): io.open(os.path.join(ROOT, p), "w", encoding="utf-8").write(s)
CATS = {"wonder": ("ふしぎ・現象", "linear-gradient(135deg,#eef2ff,#e0e7ff)", "sims/jutai/"),
        "play": ("あそぶ・実験", "linear-gradient(135deg,#fdf4ff,#fae8ff)", "sims/lorenz/"),
        "car": ("クルマ・乗り物", "linear-gradient(135deg,#f0f9ff,#e0f2fe)", None)}
# slug, cat, emoji, カードの題, カード説明, llms の説明, score, OGP の題（\n で改行）
ITEMS = [
    ("fourier-ekaki", "play", "🌀", "回る円で絵を描く", "描いた線をたくさんの回る円に分けて、もう一度描きなおす。円の数を減らすと絵が丸くなります。", "一筆書きの線を離散フーリエ変換で回る円（エピサイクル）に分解し、円の数を変えながら同じ絵を描きなおす様子を見られるシミュレーター。", 75, "回る円で絵を描く\nフーリエ級数のお絵かき"),
    ("oto-gassei", "play", "🎹", "音をつくる（倍音と音色）", "サイン波に2倍〜8倍の倍音を足すと、波の形と音色が変わる。のこぎり波や四角い波も作れて、音も鳴らせる。", "基本の音（サイン波）に2倍〜8倍の倍音を好きな強さで足し、波形・スペクトル・音色の変化を目と耳で確かめるシミュレーター（のこぎり波・四角い波・三角波・フルート風・クラリネット風のプリセットつき）。", 74, "音をつくる\n倍音を足すと音色が変わる"),
    ("jishaku-furiko", "play", "🧲", "磁石の振り子（カオス実験）", "はなす場所がほんの少しちがうだけで、止まる磁石が変わる振り子。軌跡と色の地図でカオスを確かめよう。", "3つ（2〜4）の磁石の上でゆれる振り子を好きな場所からはなし、どの磁石で止まるかを軌跡と色分けの地図（フラクタル状の模様）で確かめるカオスの実験シミュレーター。", 74, "磁石の振り子\nどの磁石で止まる？カオスの実験"),
    ("kousaten-roundabout", "wonder", "🔄", "信号 vs ラウンドアバウト", "同じ台数の車を信号の交差点とラウンドアバウトに流して、待ち時間と通りぬけた台数をくらべる。車が多いとどうなる？", "同じ交通量の車を「信号のある交差点」と「ラウンドアバウト（環状交差点）」に同時に流し、平均待ち時間・1分あたりの通過台数・止まっている車の数を左右でくらべるシミュレーター（左側通行・時計回り、交通量・青の長さ・右折の割合を変えられる）。", 75, "信号 vs ラウンドアバウト\nどちらが速く通れる？"),
    ("coaster-energy", "play", "🎢", "ジェットコースターとエネルギー", "線路の形を変えてコースターを走らせよう。位置エネルギーと運動エネルギーが入れかわり、まさつで熱に変わるようすがグラフでわかる。", "線路の点を動かす・なぞって描くことでコースを作り、位置エネルギー・運動エネルギー・まさつで熱になったエネルギーを棒グラフと時間のグラフで見ながら、力学的エネルギーの保存（中学3年）を体験できるシミュレーター。", 76, "ジェットコースターとエネルギー\n力学的エネルギーの保存"),
    ("engine-4stroke", "car", "🚗", "4ストロークエンジンのしくみ", "吸気・圧縮・燃焼・排気の4行程を断面アニメで。ピストンやバルブ、混合気の粒の動きが見られ、1気筒と直列4気筒を切り替えられます。", "4ストロークエンジン（ガソリンエンジン）の吸気・圧縮・燃焼・排気を断面アニメーションで示し、クランク軸2回転で1サイクルになる関係と、直列4気筒の点火順序1-3-4-2を、回転数の変更やコマ送りで確かめられるシミュレーター。", 72, "4ストロークエンジンのしくみ\n吸気・圧縮・燃焼・排気"),
    ("kaminari-houden", "play", "⚡", "雷の通り道シミュレーター", "雲から放電が枝分かれしながら伸び、地面に届くと一気に光る。建物や避雷針を置いて、落ちる場所の変化を数えよう。", "雲から伸びる先駆けの放電（ステップトリーダー）と主雷撃を、誘電破壊モデルを簡単にした確率の計算で再現し、建物や避雷針を置いたときに落ちる場所がどう変わるかを数えられるシミュレーター。", 75, "雷の通り道シミュレーター\n放電が枝分かれして落ちるまで"),
    ("ari-pheromone", "wonder", "🐜", "アリの行列シミュレーター", "エサを見つけたアリが残すフェロモンをたどって行列ができる。エサや壁を置いて、蒸発の速さも変えられる。", "アリが帰り道に残すフェロモンと蒸発だけで行列ができるしくみを、エサ・壁の配置やアリの数・蒸発の速さ・従う強さを変えて確かめられるシミュレーター。", 76, "アリの行列シミュレーター\nフェロモンで近道ができる"),
    ("nenkin-network", "wonder", "🟡", "粘菌のネットワーク", "粒子が「通った跡」の濃い方へ曲がるだけで、黄色い網目ができる。タップでエサを置くと、エサを結ぶ形に変わります。", "数千の粒子が「通った跡」の濃い方へ曲がり自分も跡を残すという単純なルール（Jones 2010 の粘菌モデルの考え方）で、モジホコリのような網目のネットワークができ、タップで置いたエサどうしが管で結ばれていくようすを見られるシミュレーション。", 75, "粘菌のネットワーク\n網目ができるシミュレーター"),
    ("ai-gakushu-nn", "wonder", "🧠", "AIが学習するようすを見る", "小さなニューラルネットが2色の点を分ける境界線を学習。ニューロンの数や層を変えて、分けられる・分けられないをためせます。", "入力2→中間層→出力1の小さなニューラルネットが、2色の点を分ける境界を逆伝播で学習していく様子をリアルタイム表示。データの形・ニューロン数（1〜8）・層数（1〜2）・学習率を変えて、ニューロン1個では円やXORを分けられないことを体験できる。", 76, "AIが学習するようすを見る\nニューラルネットワークの学習"),
    ("nuno-cloth", "play", "🧵", "布のシミュレーション", "布をつまんで引っぱる、風でゆらす、なぞって切る。強く引くと糸が赤くなって破れる布の実験。", "カーテン・旗・ハンモック・ネットの布を、質点とバネのモデルとベルレ法で動かし、つまむ・風・重力・ピンの付け外し・切る・破れるを試せるシミュレーター。", 75, "布のシミュレーション\n引っぱる・風でゆらす・切る"),
    ("chladni-zukei", "play", "🎻", "クラドニ図形シミュレーター", "ふるえる板にまいた砂が、ふるえない場所に集まって模様になる。mとnを変えると砂が流れて別の模様に。", "ふるえる正方形の板の上で数千つぶの砂が節（ふるえない場所）に集まってクラドニ図形をつくる様子を、m・n、＋／−の型、ふるえの強さを変えながら音つきで確かめられるシミュレーター。", 74, "クラドニ図形シミュレーター\n音で砂が模様になる"),
    ("kakusa-umareru", "wonder", "💰", "公平な取引で格差が生まれる", "全員同じ金額から、公平なコイン投げで取引するだけ。それでもお金は少数の人に集まっていく。再分配の効果も試せる。", "全員が同じ金額から始め、公平なコイン投げで「貧しい方の所持金の一定割合」をやりとりするヤードセール・モデルで、格差（ジニ係数）が広がるようすと再分配の効果を見られるシミュレーション。", 72, "公平な取引で格差が生まれる\nお金のやりとりシミュレーター"),
]

def main():
    items = [it for it in ITEMS if os.path.isfile(os.path.join(ROOT, "sims", it[0], "index.html"))]
    print("対象:", [it[0] for it in items])
    html = rd("index.html"); llms = rd("llms.txt"); sm = rd("sitemap.xml"); sh = rd("api/share.js")
    src = rd("scripts/gen_images.py").split("\nSIMS = [")[0]; ns = {"__file__": os.path.join(ROOT, "scripts", "gen_images.py")}; exec(src, ns)
    added = 0
    for slug, cat, emoji, title, desc, ldesc, score, ogt in items:
        catjp, grad, anchor = CATS[cat]; anchor = anchor or "sims/nenpi-gas/"
        if f'href="sims/{slug}/"' not in html:
            i = html.index(f'<a class="sim-card" data-cat="{cat}" href="{anchor}">'); j = html.index("</a>", i) + 4
            card = (f'\n    <a class="sim-card" data-cat="{cat}" href="sims/{slug}/">\n'
                    f'      <div class="thumb" style="background:{grad}"><span class="emoji">{emoji}</span></div>\n'
                    f'      <div class="body"><div class="cat">{catjp}</div><h3>{title}</h3><p>{desc}</p><span class="go">触ってみる →</span></div>\n    </a>')
            html = html[:j] + card + html[j:]
            m = re.search(r"\n(\s*\{ href: '" + re.escape(anchor) + r"index\.html'[^\n]*)\n", html); assert m, anchor
            html = html.replace(m.group(1), m.group(1) + f"\n    {{ href: 'sims/{slug}/', emoji: '{emoji}', title: '{title}', cat: '{catjp}', score: {score} }},", 1)
            m = re.search(r"<b>(\d+)</b>本 公開中", html); html = html.replace(m.group(0), f"<b>{int(m.group(1)) + 1}</b>本 公開中", 1); added += 1
        if f"/sims/{slug}/)" not in llms:
            m = re.search(r"### " + re.escape(catjp) + r"（(\d+)本）\n", llms); assert m, catjp
            llms = llms.replace(m.group(0), f"### {catjp}（{int(m.group(1)) + 1}本）\n- [{title}](https://shimulabo.com/sims/{slug}/): {ldesc}\n", 1)
        if f"/sims/{slug}/</loc>" not in sm:
            sm = sm.replace("</urlset>", f"  <url><loc>https://shimulabo.com/sims/{slug}/</loc><lastmod>2026-11-24</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>\n</urlset>")
        if f"'{slug}'" not in sh:
            a = "  'tensha-honyaku-genkaku',\n"; assert a in sh
            sh = sh.replace(a, a + f"  '{slug}',\n", 1)
        if not os.path.isfile(os.path.join(ROOT, "ogp", slug + ".png")):
            ns["make_ogp"](os.path.join(ROOT, "ogp", slug + ".png"), ogt, catjp)
    wr("index.html", html); wr("llms.txt", llms); wr("sitemap.xml", sm); wr("api/share.js", sh)
    print("トップに追加:", added, "本 →", re.search(r"<b>(\d+)</b>本 公開中", html).group(1), "本")

if __name__ == "__main__":
    main()
