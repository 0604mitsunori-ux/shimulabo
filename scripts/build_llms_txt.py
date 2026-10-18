"""/llms.txt を作る（2026-10-18）。ChatGPT など AI がサイトの中身を把握しやすいように、
理科の授業向け（学習指導要領の単元別）・ラボ・ライブの入口と、カテゴリごとの全シミュを Markdown で並べる。
元データ: scripts/rika/units.json（理科）と index.html のカード（タイトル・説明・カテゴリ）。何度実行しても同じ結果。
使い方: python scripts/build_llms_txt.py   （シミュを足したあとに実行）
"""
import html as H
import io, json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://shimulabo.com"
rd = lambda p: io.open(os.path.join(ROOT, p), encoding="utf-8").read()
txt = lambda s: H.unescape(re.sub(r"<[^>]+>", "", s)).strip()

idx = rd("index.html")
cats = re.findall(r"\['([a-z0-9]+)','([^']+)','[^']*'\]", idx[idx.index("const CATS"):])
cards = {}
for m in re.finditer(r'<a class="sim-card" data-cat="([a-z0-9]+)" href="sims/([^/"]+)/">(.*?)</a>', idx, re.S):
    cat, slug, body = m.groups()
    t = re.search(r"<h3>(.*?)</h3>", body, re.S); d = re.search(r"<p>(.*?)</p>", body, re.S)
    cards.setdefault(slug, (cat, txt(t.group(1)) if t else slug, txt(d.group(1)) if d else ""))
# noindex のページ（scripts/noindex_thin.txt）は載せない
cards = {s: v for s, v in cards.items() if "noindex" not in rd(f"sims/{s}/index.html")[:3000]}

U = json.load(io.open(os.path.join(ROOT, "scripts", "rika", "units.json"), encoding="utf-8"))
out = [
    "# シミュラボ（shimulabo.com）",
    "",
    "> 身近な疑問や理科の現象を、数字を入れるだけで計算・アニメーションで確かめられる無料のWebシミュレーター集。"
    "ログイン不要・ブラウザだけで動き、入力した内容はサーバーに送らない。理科の授業（小学校〜高校）、日々の計算、"
    "気象庁などの公開データを使ったライブ表示（地震・潮・天気・星空など）を扱う。",
    "",
    f"- 掲載しているシミュ: {len(cards)}本（{len(cats)}カテゴリ）",
    "- 引用: 出典「シミュラボ」とページのURLを書けば、記事・授業資料・SNSへの引用は自由（事前連絡不要）",
    f"- サイトマップ: {BASE}/sitemap.xml",
    "",
    "## 入口",
    f"- [理科の授業で使えるシミュレーター（小学校・中学校・高校の単元別）]({BASE}/rika/): 学習指導要領（平成29・30年告示）の単元名で探せる。GIGAタブレット・電子黒板向け",
    f"- [シミュレーション・ラボ]({BASE}/lab/): 社会・物理・AIの数理モデル（感染・渋滞・取り付け騒ぎ・ニューラルネットなど）",
    f"- [ライブデータラボ]({BASE}/live/): 気象庁・国土地理院・Open-Meteo などの公開データでその日の値を表示する",
    f"- [トップ（カテゴリ別の一覧）]({BASE}/)",
    "",
    "## 理科の授業向け（学習指導要領の単元別）",
]
for s in U["sections"]:
    for g in s["groups"]:
        out.append(f"### {s['title']} {g['title']}")
        for it in g["items"]:
            name = cards.get(it["id"], (None, it["id"], ""))[1]
            out.append(f"- [{name}]({BASE}/sims/{it['id']}/): {it['unit']}。{it['use']}")
        out.append("")
out.append("## カテゴリ別の全シミュ")
for slug, label in cats:
    items = [(s, t, d) for s, (c, t, d) in cards.items() if c == slug]
    if not items: continue
    out.append(f"### {label}（{len(items)}本）")
    out += [f"- [{t}]({BASE}/sims/{s}/): {d}" for s, t, d in items]
    out.append("")
io.open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(out).rstrip() + "\n")
print(f"llms.txt: {len(cards)}本 / {len(out)}行")
