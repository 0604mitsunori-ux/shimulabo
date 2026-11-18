"""「人の粒」アニメ（assets/crowd.js）を各シミュの結果欄に差し込む。

設定は 1ページ1ファイル：scripts/crowd_pages/<slug>.json
  {"buttons": ["calcBtn"], "js": "...計算ボタンの後に動かすJS..."}
  js の中では v('id') で入力欄の値、el が描く場所。使える型は crowd.js の先頭の説明を参照。

  python scripts/add_crowd.py              … 全ページ
  python scripts/add_crowd.py gacha unmei  … 指定したページだけ（同時に何人で作ってもぶつからない）

何度実行しても同じ結果になる。gen_sims*.py でページを作り直したら再実行する。
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ROOT / "scripts" / "crowd_pages"
START, END = "<!-- crowd:start -->", "<!-- crowd:end -->"
VER = "4"
# 結果欄の「シェア数」の行の直前に入れる（どのページもほぼ同じ形）
ANCHOR = re.compile(r'\n[ \t]*<div style="text-align:center;[^"]*"><span id="shareCount"')
OLD = re.compile(r"\n[ \t]*" + re.escape(START) + r"[\s\S]*?" + re.escape(END))


def block(cfg):
    buttons = ",".join(f"'{b}'" for b in cfg.get("buttons", ["calcBtn"]))
    js = "\n".join("          " + ln.strip() for ln in cfg["js"].strip().splitlines())
    return f"""{START}
      <div id="crowdBox" style="margin-top:18px;"></div>
      <script src="../../assets/crowd.js?v={VER}"></script>
      <script>
      (function () {{
        var el = document.getElementById('crowdBox');
        function v(id) {{ var e = document.getElementById(id); return e ? e.value : ''; }}
        function run() {{
{js}
        }}
        [{buttons}].forEach(function (id) {{
          var b = document.getElementById(id);
          if (b) b.addEventListener('click', function () {{ setTimeout(run, 30); }});
        }});
      }})();
      </script>
      {END}"""


def patch(slug):
    cfg = json.loads((PAGES / f"{slug}.json").read_text(encoding="utf-8"))
    p = ROOT / "sims" / slug / "index.html"
    raw = p.read_bytes().decode("utf-8")
    crlf = "\r\n" in raw
    s = OLD.sub("", raw.replace("\r\n", "\n"))
    m = ANCHOR.search(s)
    if not m:
        print("NG 差し込み場所なし:", slug)
        return False
    s = s[:m.start()] + "\n      " + block(cfg) + s[m.start():]
    if crlf:
        s = s.replace("\n", "\r\n")
    p.write_bytes(s.encode("utf-8"))
    print("OK:", slug)
    return True


def main():
    slugs = sys.argv[1:] or sorted(f.stem for f in PAGES.glob("*.json"))
    for slug in slugs:
        patch(slug)


if __name__ == "__main__":
    main()
