"""サイトに YouTube（シミュラボ＝3Dシミュレーション @shimulabo-3d）の紹介を入れる。何度実行しても同じ結果。

- トップ：「Webではできない大きなシミュレーションは、YouTubeで」の帯（最新動画・毎日19時・チャンネル登録・もしもリクエスト）
- トップのフッター：YouTube（→ /douga/）
- 関係するシミュページ：動画の埋め込み（VIDEOS）
- /douga/ のページ（動画一覧）は scripts/build_youtube_page.py（EPISODES をここから読む）

新しい動画を出したら：
  1. assets/yt/<動画ID>.jpg（960×540・サムネを縮めたもの）を置く
  2. EPISODES の先頭に1件足す（新しい順）
  3. python scripts/add_youtube_videos.py && python scripts/build_youtube_page.py && python scripts/build_yt_promo.py
     （build_yt_promo.py＝全シミュページのタイトル下に出す案内 assets/yt-promo.js を作る）

gen_sims*.py でページを作り直したら、このスクリプトも再実行する。
"""
import html
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
START, END = "<!-- yt-video:start -->", "<!-- yt-video:end -->"

ENABLED = True
# ※ページのフォルダ名を youtube/ にしないこと（Windowsでは制作用の YouTube/ フォルダと同じ場所になる）
# ハンドルは 12/4ごろ @shimulabo-3d → @shimulabo に変える予定なので、変わらないチャンネルIDのURLを使う
CHANNEL = "https://www.youtube.com/channel/UCzu0T5y3udo8jnZwVnTtOxw"
CH_NAME, CH_HANDLE = "シミュラボ", "@shimulabo-3d"
CH_ICON = "assets/yt/channel3d.jpg"
POST_TIME = "毎日19時"

# 公開済みの動画（新しい順）。sim＝サイトで似たことを試せるページ（なければ None）
EPISODES = [
    {
        "vid": "RIUNkEa7ZBw",
        "title": "全員が150歳まで生きられる村、300年後どうなる？",
        "sub": "80歳の村と並べて300年早送り",
        "date": "2026-11-25",
        "dur": "PT9M8S",
        "len": "9:08",
        "desc": "もしも、村の全員が150歳まで元気に生きられるようになったら。川をはさんで、同じ100人・同じ広さの田畑を持つ「80歳の村」と「150歳の村」を並べ、300年を100回ずつ動かして比べました。",
        "sim": None,
    },
    {
        "vid": "93-rkmJ1Iis",
        "title": "奪う町と交換する町、200年後に栄えるのは？",
        "sub": "砂漠の6つのオアシスを200年早送り",
        "date": "2026-11-24",
        "dur": "PT8M23S",
        "len": "8:23",
        "desc": "砂漠に、40人ずつの6つのオアシスの町。足りない品を、よその町を襲って手に入れる「奪う町」と、市場で交換して手に入れる「交換する町」で、200年を100回ずつ動かして比べました。",
        "sim": None,
    },
    {
        "vid": "OEXjk8rvKTY",
        "title": "守る村と試す村、200年後に栄えるのは？",
        "sub": "天気が変わる谷の棚田を200年早送り",
        "date": "2026-11-23",
        "dur": "PT8M46S",
        "len": "8:46",
        "desc": "谷をはさんで向かい合う、棚田の村が2つ。先祖から伝わる作物をそのまま育てる「守る村」と、毎年畑の一部で新しい作物を試す「試す村」。天気が少しずつ変わる200年を100回ずつ動かして比べました。",
        "sim": None,
    },
    {
        "vid": "Q6xXKIcol34",
        "title": "すぐ動く人と考えてから動く人、1年後に多く集めるのは？",
        "sub": "霧の森で木の実集めを100回",
        "date": "2026-11-22",
        "dur": "PT9M4S",
        "len": "9:04",
        "desc": "霧の深い森で、よく実る木が季節ごとに入れ替わる。はずれたらすぐ次へ行く「すぐ動く人」と、前に行った木を思い出してから選ぶ「考えてから動く人」、20人ずつで1年の木の実集めを100回ずつ比べました。",
        "sim": None,
    },
    {
        "vid": "y62ExHjqXfs",
        "title": "すべての罪を死刑にしたら、町はどうなる？",
        "sub": "1000人の町を30年動かした結果",
        "date": "2026-11-22",
        "dur": "PT8M29S",
        "len": "8:29",
        "desc": "1000人の小さな町で、罪の罰を「今の罰」「すべて死刑」「通報しづらい」などに変えて、30年を100回ずつ動かしました。とても単純にしたモデルの結果で、現実の予測ではありません。",
        "sim": None,
    },
    {
        "vid": "khhWAN6QtGU",
        "title": "日本にゾンビが1体現れたら、全滅まで何日？",
        "sub": "100回シミュレーションした結果",
        "date": "2026-11-21",
        "dur": "PT10M6S",
        "len": "10:06",
        "desc": "ある朝、新宿にゾンビが1体だけ現れたら。日本を10km四方のマスに分けて国勢調査の人口を配り、交通を止める・みんなで戦うなどの場合を100回ずつ試しました。",
        "sim": ("kansen-agent", "感染はこう広がる SIRシミュレーター"),
    },
    {
        "vid": "qCl_Q5FrR5Y",
        "title": "優しい村に乱暴な人が1人来たら？",
        "sub": "150日後の意外な結末",
        "date": "2026-11-21",
        "dur": "PT9M26S",
        "len": "9:26",
        "desc": "優しい人だけが暮らす村に、食べ物を奪う乱暴な人を1人だけ入れて150日。後半は、相手を覚えていて何度もつき合う村で、6つの性格を100世代競わせました。",
        "sim": ("shinrai-shinka", "信頼の進化シミュレーター（囚人のジレンマ）"),
    },
    {
        "vid": "Tz7QjIJqpgo",
        "title": "協力の港と競争の港、200年後に残るのは？",
        "sub": "同じ島の2つの港を200年早送り",
        "date": "2026-11-20",
        "dur": "PT8M48S",
        "len": "8:48",
        "desc": "同じ島に、同じ40人・同じだけの魚がいる2つの港。とった魚をみんなで分ける「協力の港」と、とった人のものになる「競争の港」を、200年ぶん100回ずつ動かしました。",
        "sim": ("shinrai-shinka", "信頼の進化シミュレーター（囚人のジレンマ）"),
    },
]

# 人気の動画（トップで3秒ごとに入れ替わる）。実行するたびにチャンネルの公開フィードの再生回数で並べ直す。
# 取れなかったときは POPULAR_FALLBACK の順。再生回数そのものはページに出さない（すぐ古くなるため）
CHANNEL_ID = "UCzu0T5y3udo8jnZwVnTtOxw"
POPULAR_FALLBACK = ["qCl_Q5FrR5Y", "khhWAN6QtGU", "Tz7QjIJqpgo"]


def popular(n=3):
    import urllib.request
    have = {e["vid"]: e for e in EPISODES}
    try:
        x = urllib.request.urlopen(f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}", timeout=15).read().decode("utf-8")
        views = {}
        for e in re.findall(r"<entry>(.*?)</entry>", x, re.S):
            v, c = re.search(r"<yt:videoId>(.*?)<", e), re.search(r'views="(\d+)"', e)
            if v and c and v.group(1) in have:
                views[v.group(1)] = int(c.group(1))
        order = sorted(views, key=lambda k: -views[k])
        print("人気（再生回数順）:", ", ".join(f"{k}={views[k]}" for k in order))
    except Exception as ex:  # noqa: BLE001
        print("人気：フィードが取れないので固定の順にします", ex)
        order = []
    order += [v for v in POPULAR_FALLBACK if v not in order and v in have]
    order += [e["vid"] for e in EPISODES if e["vid"] not in order]
    return [have[v] for v in order[:n]]


# シミュページに埋め込む動画　slug: (動画ID, 見出し, ひとこと)
VIDEOS = {
    "kansen-agent": (
        "khhWAN6QtGU",
        "動画：日本にゾンビが1体現れたら、全滅まで何日？",
        "同じ「うつる・治る」の考え方で、日本じゅうの人口を使って90日を動かした動画です。交通を止めると、どれだけ遅らせられるのか。見る前に予想してみてください。",
    ),
    "shinrai-shinka": (
        "Tz7QjIJqpgo",
        "動画：協力の港と競争の港、200年後に残るのは？",
        "「ずるをする人」がいる世界を、3Dで200年動かした動画です。漁港の40人が、協力と競争のどちらで生き残るのか。見る前に予想してみてください。",
    ),
}
# 以前に動画を埋め込んでいたページ（今は外す）
OLD_VIDEO_SLUGS = ["takarakuji"]

# 差し込む場所：記事（計算方法など）の直前＝結果パネルのすぐ下
ANCHOR = '\n  <article class="article">'
OLD = re.compile(r"\n[ \t]*" + re.escape(START) + r"[\s\S]*?" + re.escape(END))

TOP_START, TOP_END = "<!-- yt-top:start -->", "<!-- yt-top:end -->"
TOP_ANCHOR = '\n  <section class="rank-wrap" id="liveShelf">'
TOP_OLD = re.compile(r"\n[ \t]*" + re.escape(TOP_START) + r"[\s\S]*?" + re.escape(TOP_END))
FOOT_ANCHOR = '      <a href="about/">運営者情報</a>'
FOOT_LINK = '      <a href="douga/">YouTube</a>'
FOOT_ANY = re.compile(r'\n[ \t]*<a href="(?:https://www\.youtube\.com/[^"]*|youtube/|douga/)"(?: target="_blank" rel="noopener")?>YouTube</a>')


def block(vid, title, lead):
    t, l = html.escape(title), html.escape(lead)
    return f"""{START}
  <section class="panel yt-video">
    <h2>▶ {t}</h2>
    <p style="font-size:14px;color:var(--ink-2);margin:0 0 10px;">{l}</p>
    <div style="position:relative;padding-top:56.25%;border-radius:var(--radius);overflow:hidden;background:#0D1417;">
      <iframe src="https://www.youtube-nocookie.com/embed/{vid}" title="{t}" loading="lazy" style="position:absolute;inset:0;width:100%;height:100%;border:0;" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    </div>
    <p style="font-size:13px;margin:10px 0 0;display:flex;gap:14px;flex-wrap:wrap;"><a href="{CHANNEL}?sub_confirmation=1" target="_blank" rel="noopener" style="font-weight:800;color:#d9002b;">🔔 チャンネル登録（{POST_TIME}に新しい動画）</a><a href="../../douga/" style="font-weight:800;">ほかの動画・「もしも」のリクエスト →</a></p>
  </section>
  {END}"""


def pop_slides(pop):
    out = []
    for i, e in enumerate(pop):
        t = html.escape(e["title"]); sub = html.escape(e.get("sub", ""))
        out.append(f'''        <a class="yt-slide{' on' if i == 0 else ''}" href="https://www.youtube.com/watch?v={e["vid"]}" target="_blank" rel="noopener" data-vid="{e["vid"]}" aria-hidden="{'false' if i == 0 else 'true'}"{'' if i == 0 else ' tabindex="-1"'}>
          <span class="th"><img src="assets/yt/{e["vid"]}.jpg" width="960" height="540" loading="lazy" decoding="async" alt=""><i>{e["len"]}</i></span>
          <span class="tx"><b class="rk">🔥 人気 {i + 1}位</b><strong>{t}</strong><span class="sb">{sub}</span><span class="go">▶ YouTubeで見る</span></span>
        </a>''')
    return "\n".join(out)


def top_block(ep, pop):
    vid = ep["vid"]
    t = html.escape(ep["title"])
    dots = "".join(f'<button type="button" class="{"on" if i == 0 else ""}" aria-label="人気{i + 1}位を表示"></button>' for i in range(len(pop)))
    slides = pop_slides(pop)
    return f"""{TOP_START}
  <section class="rank-wrap yt-top" id="ytShelf" aria-labelledby="ytTitle">
    <style>
      .yt-top h2 .nb{{display:inline-block}}
      .yt-top .yt-grid{{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(0,1fr);gap:22px;align-items:center}}
      .yt-top .yt-play{{position:relative;display:block;width:100%;aspect-ratio:16/9;border:0;padding:0;border-radius:var(--radius);overflow:hidden;background:#0D1417;cursor:pointer}}
      .yt-top .yt-play img{{width:100%;height:100%;object-fit:cover;display:block;transition:transform .4s}}
      .yt-top .yt-play:hover img{{transform:scale(1.03)}}
      .yt-top .yt-btn{{position:absolute;left:50%;top:50%;width:72px;height:50px;margin:-25px 0 0 -36px;border-radius:14px;background:#ff0033;box-shadow:0 6px 20px rgba(0,0,0,.35)}}
      .yt-top .yt-btn::after{{content:"";position:absolute;left:29px;top:15px;border-style:solid;border-width:10px 0 10px 17px;border-color:transparent transparent transparent #fff}}
      .yt-top iframe{{position:absolute;inset:0;width:100%;height:100%;border:0}}
      .yt-top .yt-ch{{display:flex;align-items:center;gap:10px;margin-bottom:10px}}
      .yt-top .yt-ch img{{width:44px;height:44px;border-radius:50%}}
      .yt-top .yt-ch b{{font-size:17px}}
      .yt-top .yt-ch span{{display:block;font-size:12px;color:var(--ink-3)}}
      .yt-top .yt-desc{{font-size:14px;color:var(--ink-2);line-height:1.8;margin:0 0 10px}}
      .yt-top .yt-time{{display:inline-flex;align-items:center;gap:6px;font-size:13px;font-weight:800;background:#fff1f3;color:#d9002b;border-radius:999px;padding:4px 12px;margin:0 0 10px}}
      .yt-top .yt-new{{font-size:13px;font-weight:800;margin:0 0 14px;line-height:1.6}}
      .yt-top .yt-new small{{display:inline-block;background:#ff0033;color:#fff;border-radius:4px;padding:1px 6px;margin-right:6px;font-size:11px}}
      .yt-top .yt-links{{display:flex;flex-wrap:wrap;gap:8px}}
      .yt-top .yt-links a{{display:inline-flex;align-items:center;gap:6px;padding:10px 16px;border-radius:999px;font-weight:800;font-size:14px;text-decoration:none}}
      .yt-top .yt-sub{{background:#ff0033;color:#fff}}
      .yt-top .yt-sub:hover{{background:#d9002b;color:#fff}}
      .yt-top .yt-all{{border:1px solid var(--line);color:var(--ink)}}
      .yt-top .yt-req{{display:block!important;margin-top:12px;padding:0!important;font-size:13.5px!important;color:var(--teal-d)}}
      .yt-top .yt-pop{{margin-top:22px;border-top:1px dashed var(--line);padding-top:18px}}
      .yt-top .yt-pop-h{{display:flex;align-items:center;justify-content:space-between;gap:10px;margin:0 0 10px}}
      .yt-top .yt-pop-h b{{font-size:16px}}
      .yt-top .yt-dots{{display:flex;gap:6px}}
      .yt-top .yt-dots button{{width:26px;height:6px;border:0;border-radius:3px;background:var(--line);padding:0;cursor:pointer;overflow:hidden;position:relative}}
      .yt-top .yt-dots button.on::after{{content:"";position:absolute;inset:0;background:#ff0033;transform-origin:left;animation:ytFill 3s linear forwards}}
      .yt-top .yt-pop.paused .yt-dots button.on::after{{animation-play-state:paused}}
      @keyframes ytFill{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
      .yt-top .yt-stage{{position:relative;height:190px;overflow:hidden;border-radius:var(--radius)}}
      .yt-top .yt-slide{{position:absolute;inset:0;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr);gap:18px;align-items:center;background:var(--card);border:1px solid var(--line);border-radius:var(--radius);padding:12px;text-decoration:none;color:inherit;opacity:0;transform:translateY(100%);transition:transform .55s cubic-bezier(.2,.8,.2,1),opacity .4s}}
      .yt-top .yt-slide.on{{opacity:1;transform:none}}
      .yt-top .yt-slide.out{{opacity:0;transform:translateY(-100%)}}
      .yt-top .yt-slide .th{{position:relative;display:block;height:100%;border-radius:10px;overflow:hidden;background:#0D1417}}
      .yt-top .yt-slide .th img{{width:100%;height:100%;object-fit:cover;display:block}}
      .yt-top .yt-slide .th i{{position:absolute;right:6px;bottom:6px;font-style:normal;font-size:11.5px;font-weight:800;color:#fff;background:rgba(0,0,0,.75);border-radius:4px;padding:1px 6px}}
      .yt-top .yt-slide .tx{{display:flex;flex-direction:column;gap:5px;min-width:0}}
      .yt-top .yt-slide .rk{{align-self:flex-start;font-size:12px;background:#fff1f3;color:#d9002b;border-radius:999px;padding:3px 10px}}
      .yt-top .yt-slide strong{{font-size:17px;line-height:1.45}}
      .yt-top .yt-slide .sb{{font-size:13px;color:var(--ink-2)}}
      .yt-top .yt-slide .go{{font-size:13px;font-weight:800;color:#d9002b}}
      .yt-top .yt-slide:hover strong{{text-decoration:underline}}
      @media (max-width:720px){{.yt-top .rank-head h2{{display:block;line-height:1.5}}.yt-top h2 .nb{{display:inline}}.yt-top .yt-grid{{grid-template-columns:1fr;gap:14px}}.yt-top .yt-stage{{height:118px}}.yt-top .yt-slide{{gap:10px;padding:8px;grid-template-columns:44% 1fr}}.yt-top .yt-slide strong{{font-size:14px}}.yt-top .yt-slide .sb,.yt-top .yt-slide .go{{display:none}}.yt-top .yt-slide .rk{{font-size:11px;padding:2px 8px}}}}
      @media (prefers-reduced-motion:reduce){{.yt-top .yt-slide{{transition:none}}.yt-top .yt-dots button.on::after{{animation:none;transform:none}}}}
    </style>
    <div class="rank-head">
      <h2 id="ytTitle">▶ <span class="nb">Webではできない</span><span class="nb">大きなシミュレーションは、</span><span class="nb">YouTubeで</span></h2>
      <span class="note">3Dで100回ずつ試す動画</span>
    </div>
    <div class="yt-grid">
      <div class="yt-play" role="button" tabindex="0" aria-label="動画を再生：{t}" data-vid="{vid}">
        <img src="assets/yt/{vid}.jpg" width="960" height="540" loading="lazy" decoding="async" alt="{t}">
        <span class="yt-btn" aria-hidden="true"></span>
      </div>
      <div>
        <div class="yt-ch"><img src="{CH_ICON}" width="44" height="44" alt=""><div><b>{CH_NAME}</b><span>{CH_HANDLE}</span></div></div>
        <p class="yt-desc">何十人が何百年暮らす町や、日本じゅうに広がるゾンビ。ブラウザでは重すぎて動かせない大きなシミュレーションは、3Dの動画にしてYouTubeで公開しています。</p>
        <p class="yt-time">🕖 {POST_TIME}に新しい動画</p>
        <p class="yt-new"><small>最新</small>{t}（{ep["len"]}）</p>
        <div class="yt-links">
          <a class="yt-sub" href="{CHANNEL}?sub_confirmation=1" target="_blank" rel="noopener">🔔 チャンネル登録</a>
          <a class="yt-all" href="douga/">動画一覧 →</a>
          <a class="yt-req" href="douga/#req">💡 YouTubeで見たい「もしも」を送る →</a>
        </div>
      </div>
    </div>
    <div class="yt-pop" id="ytPop" aria-roledescription="carousel" aria-label="いま人気の動画">
      <div class="yt-pop-h"><b>🔥 いま人気の動画</b><div class="yt-dots">{dots}</div></div>
      <div class="yt-stage">
{slides}
      </div>
    </div>
    <script>
      (function () {{
        var box = document.getElementById('ytPop'); if (!box) return;
        var sl = box.querySelectorAll('.yt-slide'), dt = box.querySelectorAll('.yt-dots button'), i = 0, tm = null;
        var still = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
        function show(n) {{
          if (n === i) return;
          sl[i].classList.remove('on'); sl[i].classList.add('out'); sl[i].setAttribute('aria-hidden', 'true'); sl[i].tabIndex = -1;
          var old = sl[i]; setTimeout(function () {{ old.classList.remove('out'); }}, 600);
          dt[i].classList.remove('on'); i = n;
          sl[i].classList.add('on'); sl[i].setAttribute('aria-hidden', 'false'); sl[i].removeAttribute('tabindex');
          void dt[i].offsetWidth; dt[i].classList.add('on');
        }}
        function go() {{ stop(); if (!still) tm = setInterval(function () {{ show((i + 1) % sl.length); }}, 3000); }}
        function stop() {{ if (tm) clearInterval(tm); tm = null; }}
        dt.forEach(function (b, n) {{ b.onclick = function () {{ show(n); go(); }}; }});
        box.addEventListener('mouseenter', function () {{ stop(); box.classList.add('paused'); }});
        box.addEventListener('mouseleave', function () {{ box.classList.remove('paused'); go(); }});
        box.addEventListener('focusin', function () {{ stop(); box.classList.add('paused'); }});
        box.addEventListener('focusout', function () {{ box.classList.remove('paused'); go(); }});
        sl.forEach(function (a) {{ a.addEventListener('click', function () {{ try {{ gtag('event', 'yt_popular_click', {{ video_id: a.dataset.vid }}); }} catch (e) {{}} }}); }});
        if ('IntersectionObserver' in window) {{
          new IntersectionObserver(function (es) {{ es[0].isIntersecting ? go() : stop(); }}).observe(box);
        }} else go();
      }})();
      document.querySelectorAll('.yt-top .yt-play').forEach(function (el) {{
        function play() {{
          var f = document.createElement('iframe');
          f.src = 'https://www.youtube-nocookie.com/embed/' + el.dataset.vid + '?autoplay=1';
          f.title = el.getAttribute('aria-label');
          f.allow = 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture';
          f.allowFullscreen = true;
          el.innerHTML = ''; el.appendChild(f); el.removeAttribute('role'); el.onclick = null;
          try {{ gtag('event', 'yt_play', {{ video_id: el.dataset.vid, place: 'top' }}); }} catch (e) {{}}
        }}
        el.onclick = play;
        el.onkeydown = function (e) {{ if (e.key === 'Enter' || e.key === ' ') {{ e.preventDefault(); play(); }} }};
      }});
    </script>
  </section>
  {TOP_END}"""


def rw(p, fn):
    raw = p.read_bytes().decode("utf-8")
    crlf = "\r\n" in raw
    s = fn(raw.replace("\r\n", "\n"))
    if crlf:
        s = s.replace("\n", "\r\n")
    if s != raw:
        p.write_bytes(s.encode("utf-8"))
        return True
    return False


def patch_top():
    def fn(s):
        s = FOOT_ANY.sub("", TOP_OLD.sub("", s))
        if not ENABLED:
            return s
        if TOP_ANCHOR not in s:
            raise SystemExit("トップ：差し込み場所なし")
        s = s.replace(TOP_ANCHOR, "\n  " + top_block(EPISODES[0], popular()) + TOP_ANCHOR, 1)
        if FOOT_ANCHOR in s:
            s = s.replace(FOOT_ANCHOR, FOOT_LINK + "\n" + FOOT_ANCHOR, 1)
        return s
    rw(ROOT / "index.html", fn)
    print("トップ:", EPISODES[0]["vid"] if ENABLED else "外した")


def patch_sims():
    for slug in set(VIDEOS) | set(OLD_VIDEO_SLUGS):
        p = ROOT / "sims" / slug / "index.html"
        if not p.exists():
            print("ページなし:", slug)
            continue
        v = VIDEOS.get(slug) if ENABLED else None

        def fn(s, v=v):
            s = OLD.sub("", s)
            if v:
                if ANCHOR not in s:
                    raise SystemExit("差し込み場所なし: " + slug)
                s = s.replace(ANCHOR, "\n  " + block(*v) + ANCHOR, 1)
            return s
        rw(p, fn)
        print("シミュ:", slug, v[0] if v else "（なし）")


if __name__ == "__main__":
    patch_top()
    patch_sims()
