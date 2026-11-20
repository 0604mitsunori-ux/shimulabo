"""サイトに YouTube（シミュラボ＝3Dシミュレーション @shimulabo-3d）の紹介を入れる。何度実行しても同じ結果。

- トップ：「Webではできない大きなシミュレーションは、YouTubeで」の帯（最新動画・毎日19時・チャンネル登録・もしもリクエスト）
- トップのフッター：YouTube（→ /douga/）
- 関係するシミュページ：動画の埋め込み（VIDEOS）
- /douga/ のページ（動画一覧）は scripts/build_youtube_page.py（EPISODES をここから読む）

新しい動画を出したら：
  1. assets/yt/<動画ID>.jpg（960×540・サムネを縮めたもの）を置く
  2. EPISODES の先頭に1件足す（新しい順）
  3. python scripts/add_youtube_videos.py && python scripts/build_youtube_page.py

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

# シミュページに埋め込む動画　slug: (動画ID, 見出し, ひとこと)
VIDEOS = {
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


def top_block(ep):
    vid = ep["vid"]
    t = html.escape(ep["title"])
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
      @media (max-width:720px){{.yt-top .yt-grid{{grid-template-columns:1fr;gap:14px}}}}
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
        <p class="yt-new"><small>最新</small>{t}</p>
        <div class="yt-links">
          <a class="yt-sub" href="{CHANNEL}?sub_confirmation=1" target="_blank" rel="noopener">🔔 チャンネル登録</a>
          <a class="yt-all" href="douga/">動画一覧 →</a>
          <a class="yt-req" href="douga/#req">💡 YouTubeで見たい「もしも」を送る →</a>
        </div>
      </div>
    </div>
    <script>
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
        s = s.replace(TOP_ANCHOR, "\n  " + top_block(EPISODES[0]) + TOP_ANCHOR, 1)
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
