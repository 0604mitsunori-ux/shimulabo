"""シミュページに YouTube（1000人ギャンブル実験 @1000ninjikken）の解説動画を差し込む。

VIDEOS に slug と動画を足して実行するだけ。何度実行しても同じ結果になる。
gen_sims*.py でページを作り直したら、このスクリプトも再実行する。

  python scripts/add_youtube_videos.py
"""
import html
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
START, END = "<!-- yt-video:start -->", "<!-- yt-video:end -->"

# slug: (動画ID, 見出し, ひとこと)
VIDEOS = {
    "takarakuji": (
        "DEVQhtWyK3g",
        "動画：1000人がロト6を30年買い続けたら",
        "コンピューターの中の1000人に、ロト6を30年間買い続けてもらいました。30年後にプラスだったのは何人か、アニメで見られます。",
    ),
}

# 差し込む場所：記事（計算方法など）の直前＝結果パネルのすぐ下
ANCHOR = '\n  <article class="article">'
OLD = re.compile(r"\n[ \t]*" + re.escape(START) + r"[\s\S]*?" + re.escape(END))


def block(vid, title, lead):
    t, l = html.escape(title), html.escape(lead)
    return f"""{START}
  <section class="panel yt-video">
    <h2>▶ {t}</h2>
    <p style="font-size:14px;color:var(--ink-2);margin:0 0 10px;">{l}</p>
    <div style="position:relative;padding-top:56.25%;border-radius:var(--radius);overflow:hidden;background:#0D1417;">
      <iframe src="https://www.youtube-nocookie.com/embed/{vid}" title="{t}" loading="lazy" style="position:absolute;inset:0;width:100%;height:100%;border:0;" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    </div>
  </section>
  {END}"""


# ★11/20 長澤「いったんYouTube紹介はなくす・別のチャンネルを付ける」→ ENABLED=False で全部外す。
# 新しいチャンネルが決まったら CHANNEL・帯の名前/ハンドル/説明文・assets/yt/channel.jpg・TOP_LATEST・VIDEOS を差し替えて True にして実行。
ENABLED = False
CHANNEL = "https://www.youtube.com/@1000ninjikken"
# 11/20 チャンネル改名（シミュラボ @shimulabo → 1000人ギャンブル実験 @1000ninjikken）。旧リンクは置き換える
OLD_CHANNELS = ["https://www.youtube.com/@shimulabo"]

# トップページの「YouTube」帯に出す最新動画。新しい動画を出したらここを差し替えて実行。
# サムネは assets/yt/<動画ID>.jpg（960×540）を置く。
TOP_LATEST = ("IaBm8sb7pvg", "パチンコで10万円負けた1000人が「取り返すまでやめない」と決めたら、どうなるのか")

TOP_START, TOP_END = "<!-- yt-top:start -->", "<!-- yt-top:end -->"
TOP_ANCHOR = '\n  <section class="rank-wrap" id="liveShelf">'
TOP_OLD = re.compile(r"\n[ \t]*" + re.escape(TOP_START) + r"[\s\S]*?" + re.escape(TOP_END))
FOOT_ANCHOR = '      <a href="about/">運営者情報</a>'
FOOT_LINK = f'      <a href="{CHANNEL}" target="_blank" rel="noopener">YouTube</a>'


def top_block(vid, title):
    t = html.escape(title)
    return f"""{TOP_START}
  <section class="rank-wrap yt-top" id="ytShelf" aria-labelledby="ytTitle">
    <style>
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
      .yt-top .yt-desc{{font-size:14px;color:var(--ink-2);line-height:1.8;margin:0 0 12px}}
      .yt-top .yt-new{{font-size:13px;font-weight:800;margin:0 0 14px}}
      .yt-top .yt-new small{{display:inline-block;background:#ff0033;color:#fff;border-radius:4px;padding:1px 6px;margin-right:6px;font-size:11px}}
      .yt-top .yt-links{{display:flex;flex-wrap:wrap;gap:8px}}
      .yt-top .yt-links a{{display:inline-flex;align-items:center;gap:6px;padding:10px 16px;border-radius:999px;font-weight:800;font-size:14px;text-decoration:none}}
      .yt-top .yt-sub{{background:#ff0033;color:#fff}}
      .yt-top .yt-sub:hover{{background:#d9002b;color:#fff}}
      .yt-top .yt-all{{border:1px solid var(--line);color:var(--ink)}}
      @media (max-width:720px){{.yt-top .yt-grid{{grid-template-columns:1fr;gap:14px}}}}
    </style>
    <div class="rank-head">
      <h2 id="ytTitle">▶ YouTubeでも見られます</h2>
      <span class="note">シミュレーションをアニメで解説</span>
    </div>
    <div class="yt-grid">
      <div class="yt-play" role="button" tabindex="0" aria-label="動画を再生：{t}" data-vid="{vid}">
        <img src="assets/yt/{vid}.jpg" width="960" height="540" loading="lazy" decoding="async" alt="{t}">
        <span class="yt-btn" aria-hidden="true"></span>
      </div>
      <div>
        <div class="yt-ch"><img src="assets/yt/channel.jpg" width="44" height="44" alt=""><div><b>1000人ギャンブル実験</b><span>@1000ninjikken</span></div></div>
        <p class="yt-desc">ギャンブルの「本当はどうなの？」を、コンピューターの中の1000人で確かめるチャンネルです。動画で使ったシミュレーターは、このサイトで数字を変えて試せます。</p>
        <p class="yt-new"><small>最新</small>{t}</p>
        <div class="yt-links">
          <a class="yt-sub" href="{CHANNEL}?sub_confirmation=1" target="_blank" rel="noopener">🔔 チャンネル登録</a>
          <a class="yt-all" href="{CHANNEL}/videos" target="_blank" rel="noopener">動画一覧 →</a>
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
        }}
        el.onclick = play;
        el.onkeydown = function (e) {{ if (e.key === 'Enter' || e.key === ' ') {{ e.preventDefault(); play(); }} }};
      }});
    </script>
  </section>
  {TOP_END}"""


def patch_top():
    p = ROOT / "index.html"
    raw = p.read_bytes().decode("utf-8")
    crlf = "\r\n" in raw
    s = TOP_OLD.sub("", raw.replace("\r\n", "\n"))
    for old in OLD_CHANNELS:
        s = s.replace(f'      <a href="{old}" target="_blank" rel="noopener">YouTube</a>', FOOT_LINK)
    if TOP_ANCHOR not in s:
        print("トップ：差し込み場所なし")
        return
    s = s.replace(TOP_ANCHOR, "\n  " + top_block(*TOP_LATEST) + TOP_ANCHOR, 1)
    if FOOT_LINK not in s and FOOT_ANCHOR in s:
        s = s.replace(FOOT_ANCHOR, FOOT_LINK + "\n" + FOOT_ANCHOR, 1)
    if crlf:
        s = s.replace("\n", "\r\n")
    p.write_bytes(s.encode("utf-8"))
    print("OK: トップ", TOP_LATEST[0])


def remove_all():
    """YouTube紹介をサイトから全部外す（トップの帯・フッターのリンク・各シミュの埋め込み）。"""
    foot = re.compile(r'\n[ \t]*<a href="https://www\.youtube\.com/@[^"]*" target="_blank" rel="noopener">YouTube</a>')
    paths = [ROOT / "index.html"] + [ROOT / "sims" / slug / "index.html" for slug in VIDEOS]
    for p in paths:
        raw = p.read_bytes().decode("utf-8")
        crlf = "\r\n" in raw
        s = raw.replace("\r\n", "\n")
        s = OLD.sub("", TOP_OLD.sub("", s))
        s = foot.sub("", s)
        if crlf:
            s = s.replace("\n", "\r\n")
        if s != raw:
            p.write_bytes(s.encode("utf-8"))
            print("外した:", p.relative_to(ROOT))


def main():
    if not ENABLED:
        remove_all()
        return
    patch_top()
    for slug, (vid, title, lead) in VIDEOS.items():
        p = ROOT / "sims" / slug / "index.html"
        raw = p.read_bytes().decode("utf-8")
        crlf = "\r\n" in raw
        s = OLD.sub("", raw.replace("\r\n", "\n"))
        if ANCHOR not in s:
            print("差し込み場所なし:", slug)
            continue
        s = s.replace(ANCHOR, "\n  " + block(vid, title, lead) + ANCHOR, 1)
        if crlf:
            s = s.replace("\n", "\r\n")
        p.write_bytes(s.encode("utf-8"))
        print("OK:", slug, vid)


if __name__ == "__main__":
    main()
