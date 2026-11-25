"""/douga/（YouTubeチャンネルの紹介＋「もしも」リクエスト）を作る（2026-11-20）。何度実行しても同じ結果。
- 動画の一覧・チャンネル・投稿時間は scripts/add_youtube_videos.py の EPISODES / CHANNEL / POST_TIME を使う
- 頭・ヘッダー・フッターは contact/index.html を流用（build_kyouiku.py と同じ作り）
- リクエストは今の受付（assets/req-api.js → GAS → スプレッドシート）に genre='YouTubeのもしも' で入る。
  集計＝シートのD列（ジャンル）で絞り込む。サイトの「みんなのもしも」に出るのは J列（掲載）に○を付けたものだけ
使い方: python scripts/add_youtube_videos.py && python scripts/build_youtube_page.py
"""
import html as H
import io, json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from add_youtube_videos import EPISODES, CHANNEL, POST_TIME, CH_NAME, CH_HANDLE  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://shimulabo.com"
rd = lambda p: io.open(os.path.join(ROOT, p), encoding="utf-8").read()
def wr(p, s): io.open(os.path.join(ROOT, p), "w", encoding="utf-8", newline="").write(s)

SUB = CHANNEL + "?sub_confirmation=1"
TITLE = f"YouTube｜Webではできない大きなシミュレーションを3Dの動画で（{POST_TIME}公開）｜シミュラボ"
DESC = (f"シミュラボのYouTubeチャンネル。何十人が何百年暮らす町や、日本じゅうに広がるゾンビなど、ブラウザでは重すぎて動かせない"
        f"大きなシミュレーションを3Dで100回ずつ試して動画にしています。{POST_TIME}に新しい動画を公開。見てみたい「もしも」のリクエストも受付中です。")

FAQS = [
    ("動画はいつ公開されますか？", f"{POST_TIME}に新しい動画を公開しています。チャンネル登録をして、ベルのマークを押しておくと、公開したときにお知らせが届きます。"),
    ("リクエストした「もしも」は必ず動画になりますか？", "すべては作れません。届いた数や、シミュレーションにできるかどうかを見て、動画にするものを選びます。動画になったら、このページでお知らせします。"),
    ("動画の数字は本当ですか？", "とても単純にしたモデルで試した結果です。決まりを変えると数字も変わります。使った決まりは、各動画の概要欄にすべて書いています。"),
    ("サイトで同じシミュレーションを動かせますか？", "一部の動画には、サイトで似たことを試せるシミュレーションがあります（動画の下のリンクから）。3Dで大人数・長い期間を動かすものは、動画だけで公開しています。"),
]
EXAMPLES = ["もしも全員が週3日しか働かなかったら？", "もしも日本の人口が100人だったら？", "もしも雨が1年間降らなかったら？",
            "もしもお金がない国があったら？", "もしも寿命が200年になったら？"]


def jp_date(d):
    y, m, dd = d.split("-")
    return f"{int(y)}年{int(m)}月{int(dd)}日"


c = rd("contact/index.html")
head = c[:c.index("</head>")]
head = re.sub(r"<title>.*?</title>", f"<title>{TITLE}</title>", head, flags=re.S)
head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{DESC}">', head)
head = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="Webではできないシミュレーションは、YouTubeで｜シミュラボ">', head)
head = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="3Dで100回ずつ試す「もしも」の動画。{POST_TIME}に公開。見てみたい「もしも」も募集中。">', head)
head = head.replace(f"{BASE}/contact/", f"{BASE}/douga/").replace("/ogp/contact.png", "/ogp/douga.png")
head = head.replace('"name": "広告掲載・タイアップ"', '"name": "YouTube"')
assert f"{BASE}/douga/" in head and "/ogp/douga.png" in head and '"name": "YouTube"' in head

ld_videos = [{
    "@context": "https://schema.org", "@type": "VideoObject",
    "name": f'{e["title"]}{e["sub"]}【3Dシミュレーション】', "description": e["desc"],
    "thumbnailUrl": [f'{BASE}/assets/yt/{e["vid"]}.jpg'], "uploadDate": e["date"] + "T19:00:00+09:00",
    "duration": e["dur"], "embedUrl": f'https://www.youtube.com/embed/{e["vid"]}',
    "contentUrl": f'https://www.youtube.com/watch?v={e["vid"]}',
    "publisher": {"@type": "Organization", "name": "シミュラボ", "url": BASE + "/"},
} for e in EPISODES]
ld_faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS]}

head += ('    <style>\n'
 '.yt-hero{display:grid;grid-template-columns:1.25fr .75fr;gap:22px;align-items:center;margin:6px 0 10px}\n'
 '.yt-hero .cat{color:#d9002b}\n'
 '.yt-hero h1 .nb{display:inline-block}\n'
 '.yt-btns{display:flex;gap:10px;flex-wrap:wrap;margin-top:14px}\n'
 '.yt-btns a{display:inline-flex;align-items:center;gap:6px;padding:12px 22px;border-radius:999px;font-weight:800;font-size:15px;text-decoration:none}\n'
 '.yt-sub{background:#ff0033;color:#fff}.yt-sub:hover{background:#d9002b;color:#fff}\n'
 '.yt-ghost{border:1px solid var(--line);color:var(--ink);background:var(--card)}.yt-ghost:hover{border-color:var(--teal);color:var(--teal-d)}\n'
 '.yt-card{background:var(--card);border:1px solid var(--line);border-radius:18px;padding:22px 20px;text-align:center}\n'
 '.yt-card img{width:96px;height:96px;border-radius:50%;display:block;margin:0 auto 10px}\n'
 '.yt-card b{display:block;font-size:20px}.yt-card .h{display:block;font-size:13px;color:var(--ink-3);margin-top:2px}\n'
 '.yt-time{display:inline-flex;align-items:center;gap:6px;font-size:14px;font-weight:800;background:#fff1f3;color:#d9002b;border-radius:999px;padding:6px 14px;margin-top:12px}\n'
 '.yt-points{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:8px 0 6px}\n'
 '.yt-point{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:16px 16px 14px}\n'
 '.yt-point .ic{font-size:26px;line-height:1}.yt-point h3{margin:8px 0 4px;font-size:16px}.yt-point p{margin:0;font-size:13px;color:var(--ink-2);line-height:1.7}\n'
 '.yt-latest{display:grid;grid-template-columns:minmax(0,1.45fr) minmax(0,1fr);gap:20px;align-items:start}\n'
 '.yt-play{position:relative;display:block;width:100%;aspect-ratio:16/9;border:0;padding:0;border-radius:var(--radius);overflow:hidden;background:#0D1417;cursor:pointer}\n'
 '.yt-play img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .4s}.yt-play:hover img{transform:scale(1.03)}\n'
 '.yt-play .yt-btn{position:absolute;left:50%;top:50%;width:72px;height:50px;margin:-25px 0 0 -36px;border-radius:14px;background:#ff0033;box-shadow:0 6px 20px rgba(0,0,0,.35)}\n'
 '.yt-play .yt-btn::after{content:"";position:absolute;left:29px;top:15px;border-style:solid;border-width:10px 0 10px 17px;border-color:transparent transparent transparent #fff}\n'
 '.yt-play iframe{position:absolute;inset:0;width:100%;height:100%;border:0}\n'
 '.yt-meta{font-size:12.5px;color:var(--ink-3);font-weight:700}.yt-meta small{display:inline-block;background:#ff0033;color:#fff;border-radius:4px;padding:1px 6px;margin-right:6px;font-size:11px}\n'
 '.yt-latest h3{margin:6px 0 2px;font-size:19px;line-height:1.45}.yt-latest .s{margin:0 0 8px;font-size:13.5px;color:var(--ink-2);font-weight:700}\n'
 '.yt-latest p.d{margin:0 0 12px;font-size:14px;color:var(--ink-2);line-height:1.8}\n'
 '.yt-latest .lk{display:flex;flex-direction:column;gap:6px;font-size:14px;font-weight:800}\n'
 '.yt-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,260px),1fr));gap:14px}\n'
 '.yt-grid a{display:block;background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden;text-decoration:none;color:inherit}\n'
 '.yt-grid img{width:100%;aspect-ratio:16/9;object-fit:cover;display:block}.yt-grid .t{padding:10px 12px 12px;font-size:14px;font-weight:800;line-height:1.5}\n'
 '.yt-two{display:grid;grid-template-columns:1fr 1fr;gap:12px}\n'
 '.yt-two>div{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:16px 16px 14px}\n'
 '.yt-two .k{font-size:12px;font-weight:800;letter-spacing:.06em;color:var(--teal-d)}.yt-two .k.r{color:#d9002b}\n'
 '.yt-two h3{margin:4px 0 6px;font-size:17px}.yt-two p{margin:0;font-size:13.5px;color:var(--ink-2);line-height:1.7}\n'
 '#req .ex{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 6px}\n'
 '#req .ex button{border:1px dashed var(--line);background:var(--card);border-radius:999px;padding:7px 13px;font-size:13px;cursor:pointer;color:var(--ink-2)}\n'
 '#req .ex button:hover{border-color:var(--teal);color:var(--teal-d)}\n'
 '.yt-list{list-style:none;margin:8px 0 0;padding:0}\n'
 '.yt-list li{display:flex;justify-content:space-between;gap:12px;align-items:flex-start;padding:11px 2px;border-top:1px solid var(--line-2);font-size:14px;line-height:1.6}\n'
 '.yt-list li:first-child{border-top:0}.yt-list .who{display:block;font-size:12px;color:var(--ink-3)}\n'
 '.yt-st{flex:none;font-size:12px;font-weight:800;border-radius:999px;padding:3px 10px;background:var(--teal-l);color:var(--teal-d);white-space:nowrap}\n'
 '.yt-st.mk{background:#fff4dc;color:#9a6200}.yt-st.ok{background:#ff0033;color:#fff;text-decoration:none}\n'
 '.yt-empty{font-size:13.5px;color:var(--ink-3);margin:8px 0 0}\n'
 '@media(max-width:760px){.yt-hero,.yt-latest,.yt-two{grid-template-columns:1fr}.yt-points{grid-template-columns:1fr}.yt-card{display:flex;align-items:center;gap:14px;text-align:left;padding:14px}.yt-card img{width:64px;height:64px;margin:0}.yt-time{margin-top:6px}}\n'
 '    </style>\n'
 + "".join('    <script type="application/ld+json">' + json.dumps(v, ensure_ascii=False) + "</script>\n" for v in ld_videos)
 + '    <script type="application/ld+json">' + json.dumps(ld_faq, ensure_ascii=False) + "</script>\n")
header = c[c.index("</head>"):c.index('<main class="wrap">')]

L = EPISODES[0]
lt = H.escape(L["title"])
sim_link = (f'<a href="../sims/{L["sim"][0]}/">🧪 サイトで似たことを試す：{H.escape(L["sim"][1])} →</a>' if L.get("sim") else "")
others = ""
if len(EPISODES) > 1:
    cards = "".join(f'<a href="https://www.youtube.com/watch?v={e["vid"]}" target="_blank" rel="noopener"><img src="../assets/yt/{e["vid"]}.jpg" alt="{H.escape(e["title"])}" loading="lazy" width="960" height="540"><div class="t">{H.escape(e["title"])}</div></a>' for e in EPISODES[1:])
    others = f'''
  <section class="panel">
    <h2>🎬 これまでの動画</h2>
    <div class="yt-grid">{cards}</div>
    <p style="margin:12px 0 0;font-size:14px;font-weight:800"><a href="{CHANNEL}/videos" target="_blank" rel="noopener">YouTubeで全部の動画を見る →</a></p>
  </section>
'''
chips = "".join(f'<button type="button">{H.escape(x)}</button>' for x in EXAMPLES)
faq_dl = "".join(f"<dt>{q}</dt><dd>{a}</dd>" for q, a in FAQS)

main = f'''<main class="wrap">
  <nav class="breadcrumb" aria-label="breadcrumb"><a href="../">ホーム</a><span>›</span><span class="cur">YouTube</span></nav>

  <div class="yt-hero">
    <div class="sim-head" style="margin:0">
      <div class="cat">YOUTUBE</div>
      <h1><span class="nb">Webではできない</span><span class="nb">シミュレーションは、</span><br><span class="nb">YouTubeで</span><span class="nb">やっています。</span></h1>
      <p class="lead">何十人が何百年暮らす町や、日本じゅうに広がるゾンビ。ブラウザでは重すぎて動かせない大きなシミュレーションは、3Dで100回ずつ試して動画にしています。見る前に、結果を予想してみてください。</p>
      <div class="yt-btns">
        <a class="yt-sub" href="{SUB}" target="_blank" rel="noopener" data-ev="hero">🔔 チャンネル登録</a>
        <a class="yt-ghost" href="#req">💡 「もしも」をリクエスト</a>
      </div>
    </div>
    <div class="yt-card">
      <img src="../assets/yt/channel3d.jpg" width="96" height="96" alt="シミュラボのアイコン">
      <div><b>{CH_NAME}</b><span class="h">{CH_HANDLE}</span>
      <span class="yt-time">🕖 {POST_TIME}に新しい動画</span></div>
    </div>
  </div>

  <div class="yt-points">
    <div class="yt-point"><div class="ic">🕖</div><h3>{POST_TIME}に公開</h3><p>毎日、夜7時に新しい動画を1本ずつ公開します。</p></div>
    <div class="yt-point"><div class="ic">🧪</div><h3>同じ決まりで100回ずつ</h3><p>同じ決まりで100回動かして、平均で比べます。映像に映るのは、そのうちの1回です。</p></div>
    <div class="yt-point"><div class="ic">🤔</div><h3>答えは最後まで</h3><p>途中で何度か予想してもらいます。見る前に予想して、コメントで答え合わせしてください。</p></div>
  </div>

  <section class="panel">
    <h2>▶ 最新の動画</h2>
    <div class="yt-latest">
      <div class="yt-play" role="button" tabindex="0" aria-label="動画を再生：{lt}" data-vid="{L["vid"]}">
        <img src="../assets/yt/{L["vid"]}.jpg" width="960" height="540" alt="{lt}">
        <span class="yt-btn" aria-hidden="true"></span>
      </div>
      <div>
        <div class="yt-meta"><small>最新</small>{jp_date(L["date"])}公開・{L["len"]}</div>
        <h3>{lt}</h3>
        <p class="s">{H.escape(L["sub"])}</p>
        <p class="d">{H.escape(L["desc"])}</p>
        <div class="lk">
          <a href="https://www.youtube.com/watch?v={L["vid"]}" target="_blank" rel="noopener">YouTubeで見る（コメントで予想を書く）→</a>
          {sim_link}
        </div>
      </div>
    </div>
  </section>
{others}
  <section class="panel">
    <h2>🔁 サイトとYouTubeのちがい</h2>
    <div class="yt-two">
      <div><div class="k">このサイト</div><h3>自分で数字を変えて、その場で試せる</h3><p>人数や金額、確率を変えると、すぐに結果が変わります。スマホ・タブレットでも、登録なしで使えます。<a href="../">シミュレーションを探す →</a></p></div>
      <div><div class="k r">YouTube</div><h3>何十人×何百年を、3Dで100回ずつ</h3><p>大人数・長い期間を動かすので、ブラウザでは重すぎるものを動画にしています。どうなるかを、映像とグラフで追えます。</p></div>
    </div>
  </section>

  <section class="panel" id="req">
    <h2>💡 YouTubeで取り上げてほしい「もしも」</h2>
    <p style="font-size:14px;color:var(--ink-2);margin:0 0 12px;line-height:1.8">「もしも○○だったら、どうなる？」を送ってください。届いた数や、シミュレーションにできるかを見て、動画にするものを選びます。動画になったら、このページでお知らせします。</p>
    <div id="reqForm">
      <div class="field">
        <label>見てみたい「もしも」 <span class="hint">（必須）</span></label>
        <div class="ex" aria-label="例">{chips}</div>
        <textarea id="idea" maxlength="300" placeholder="例：もしも全員が週3日しか働かなかったら、町はどうなる？"></textarea>
      </div>
      <div class="field">
        <label>なぜ見てみたい？ <span class="hint">（任意）</span></label>
        <textarea id="why" maxlength="500" style="min-height:70px;" placeholder="気になる理由や、こうなりそう、という予想など"></textarea>
      </div>
      <div class="field">
        <label>ニックネーム <span class="hint">（任意・動画で紹介するときの名前）</span></label>
        <input type="text" id="nick" maxlength="30" placeholder="例：しみゅ太郎">
      </div>
      <div style="position:absolute;left:-9999px;" aria-hidden="true"><label>ウェブサイト<input type="text" id="website" tabindex="-1" autocomplete="off"></label></div>
      <button class="btn btn-primary" id="sendBtn" type="button">この「もしも」を送る</button>
      <p id="note" style="font-size:13px;color:var(--ink-2);margin:12px 0 0;text-align:center;">メールアドレスや登録はいりません。</p>
    </div>
    <div id="reqDone" style="display:none;text-align:center;padding:10px 0 4px">
      <p style="font-size:18px;font-weight:800;margin:0 0 6px">🎉 受け付けました！</p>
      <p style="font-size:14px;color:var(--ink-2);margin:0 0 10px">受付番号：<b id="doneId"></b>　動画になったら、このページでお知らせします。</p>
      <div id="doneBoost"></div>
      <button class="btn" id="againBtn" type="button" style="width:auto;display:inline-flex;padding:10px 20px">もう1つ送る</button>
    </div>

    <div id="mineBox" style="display:none;margin-top:18px">
      <h3 style="font-size:16px;margin:0">あなたが送った「もしも」</h3>
      <ul class="yt-list" id="mineList"></ul>
    </div>
    <div style="margin-top:18px">
      <h3 style="font-size:16px;margin:0">みんなの「もしも」</h3>
      <ul class="yt-list" id="allList"></ul>
      <p class="yt-empty" id="allEmpty">読み込み中…</p>
    </div>
  </section>

  <section class="panel" style="text-align:center">
    <h2 style="justify-content:center">🔔 新しい動画を見逃さない</h2>
    <p style="font-size:14px;color:var(--ink-2);margin:0 0 14px">{POST_TIME}に公開します。チャンネル登録とベルのマークで、公開したときにお知らせが届きます。</p>
    <div class="yt-btns" style="justify-content:center;margin-top:0"><a class="yt-sub" href="{SUB}" target="_blank" rel="noopener" data-ev="bottom">🔔 チャンネル登録</a></div>
  </section>

  <article class="article">
    <h2>よくあるご質問</h2>
    <dl class="faq">{faq_dl}</dl>
  </article>
</main>
'''

footer = c[c.index('<footer class="site-footer">'):c.index("</footer>") + len("</footer>")]

js = r'''
<script src="../assets/req-api.js?v=2"></script>
<script src="../assets/req-boost.js?v=1"></script>
<script>
(() => {
  const $ = (id) => document.getElementById(id);
  const esc = (s) => String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const ev = (name, p) => { try { gtag('event', name, p || {}); } catch (e) {} };

  // 動画：押したときだけ読み込む
  document.querySelectorAll('.yt-play').forEach((el) => {
    const play = () => {
      const f = document.createElement('iframe');
      f.src = 'https://www.youtube-nocookie.com/embed/' + el.dataset.vid + '?autoplay=1';
      f.title = el.getAttribute('aria-label');
      f.allow = 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture';
      f.allowFullscreen = true;
      el.innerHTML = ''; el.appendChild(f); el.removeAttribute('role'); el.onclick = null;
      ev('yt_play', { video_id: el.dataset.vid, place: 'youtube_page' });
    };
    el.onclick = play;
    el.onkeydown = (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); play(); } };
  });
  document.querySelectorAll('a.yt-sub').forEach((a) => a.addEventListener('click', () => ev('yt_subscribe_click', { place: a.dataset.ev || '' })));

  // 例のチップ → 入力欄へ
  document.querySelectorAll('#req .ex button').forEach((b) => b.addEventListener('click', () => { $('idea').value = b.textContent; $('idea').focus(); }));

  const stLabel = (s, url) => {
    if (s === '公開済み' && url) return '<a class="yt-st ok" href="' + esc(url) + '" target="_blank" rel="noopener">▶ 動画になりました</a>';
    if (s === '制作中') return '<span class="yt-st mk">制作中</span>';
    if (s === '見送り') return '<span class="yt-st">今回は見送り</span>';
    return '<span class="yt-st">受付中</span>';
  };
  const okUrl = (u) => /^https:\/\/(www\.youtube\.com|youtu\.be|shimulabo\.com)\//.test(u || '') ? u : '';
  const li = (x, who) => '<li><div>' + esc(x.idea) + (who ? '<span class="who">' + esc(who) + '</span>' : '') + '</div>' + stLabel(x.status, okUrl(x.url)) + '</li>';

  function renderMine() {
    const m = ReqAPI.mine({ yt: true }).slice(0, 10);
    if (!m.length) { $('mineBox').style.display = 'none'; return; }
    $('mineBox').style.display = '';
    $('mineList').innerHTML = m.map((x) => li({ idea: x.idea, status: '受付' })).join('');
    ReqAPI.status(m.map((x) => x.id)).then((arr) => {
      const by = {}; arr.forEach((x) => { by[x.id] = x; });
      $('mineList').innerHTML = m.map((x) => { const s = by[x.id] || {}; return li({ idea: x.idea, status: s.status || '受付', url: s.url }); }).join('');
    }).catch(() => {});
  }
  function renderAll() {
    ReqAPI.list({ yt: true }).then((items) => {
      if (!items.length) { $('allEmpty').textContent = 'まだありません。最初の「もしも」を送ってみてください。'; return; }
      $('allEmpty').style.display = 'none';
      $('allList').innerHTML = items.slice(0, 30).map((x) => li(x, x.nick ? x.nick + ' さん' : '')).join('');
    }).catch(() => { $('allEmpty').textContent = 'いまは読み込めませんでした。'; });
  }
  renderMine(); renderAll();

  let busy = false;
  $('sendBtn').addEventListener('click', async () => {
    if (busy) return;
    const idea = $('idea').value.trim();
    const note = $('note');
    if (!idea) { note.textContent = '⚠️ 見てみたい「もしも」を書いてください。'; note.style.color = 'var(--accent-d)'; return; }
    busy = true; $('sendBtn').disabled = true; $('sendBtn').textContent = '送信中…';
    try {
      const j = await ReqAPI.submit({ idea, genre: ReqAPI.YT, why: $('why').value.trim(), nick: $('nick').value.trim(), email: '', website: $('website').value });
      if (!j || !j.ok) throw new Error((j && j.error) || 'failed');
      ReqAPI.remember(j.id, idea, ReqAPI.YT);
      $('doneId').textContent = j.id;
      $('reqForm').style.display = 'none'; $('reqDone').style.display = '';
      try { ReqBoost.mount($('doneBoost'), { id: j.id, idea: idea, yt: true }); } catch (e) {}
      renderMine();
      ev('yt_request_submit', {});
    } catch (e) {
      note.textContent = '⚠️ うまく送れませんでした。少し時間をおいてもう一度お試しください。' + (String(e.message) === 'busy' ? '（ただいま混み合っています）' : '');
      note.style.color = 'var(--accent-d)';
    }
    busy = false; $('sendBtn').disabled = false; $('sendBtn').textContent = 'この「もしも」を送る';
  });
  $('againBtn').addEventListener('click', () => {
    $('idea').value = ''; $('why').value = '';
    $('reqDone').style.display = 'none'; $('reqForm').style.display = ''; $('idea').focus();
  });
})();
</script>
<script src="../assets/lang-toggle.js?v=4"></script>
</body>
</html>
'''

os.makedirs(os.path.join(ROOT, "douga"), exist_ok=True)
wr("douga/index.html", head + header + main + "\n" + footer + "\n" + js)
print(f"douga/index.html（動画{len(EPISODES)}本）")

p = os.path.join(ROOT, "ogp", "douga.png")
if not os.path.exists(p):
    gen = os.path.join(ROOT, "scripts", "gen_images.py"); ns = {"__file__": gen}
    exec(compile(rd("scripts/gen_images.py").split("\nSIMS = [")[0], gen, "exec"), ns)
    ns["make_ogp"](p, "Webではできない\nシミュレーションを3Dで", "YOUTUBE", underline="3D")
    print("OGP:", p)
