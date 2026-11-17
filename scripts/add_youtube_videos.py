"""シミュページに YouTube（@shimulabo）の解説動画を差し込む。

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


def main():
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
