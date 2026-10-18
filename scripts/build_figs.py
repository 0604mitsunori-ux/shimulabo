"""シミュのページに「図」を入れる（2026-10-18・理科の授業向け＋読まれている一般ページ）。何度実行しても同じ結果。
  - 図の定義は scripts/figs/<slug の - を _ にした名前>.py の FIGS（書き方は scripts/figs/FIG_SPEC.md）。
  - sims/<slug>/<slug>-<n>.svg（ページに表示）と <slug>-<n>.png（2400×1350・保存用）を書き出し、本文に差し込む。
    差し込む位置：モジュールの ANCHOR（正規表現）があればその直後。なければ「しくみ」の見出しの直後、
    それもなければ本文の最初の見出し（と直後の段落）の後。構造化データ（WebApplication）に image も足す。
使い方:
  python scripts/build_figs.py                 … 全部
  python scripts/build_figs.py --only a,b      … 指定したページだけ（作成担当の確認用）
  python scripts/build_figs.py --no-png        … PNG を作らない（差し込みだけ）
理科の build_sims.py はページを作り直したあとに inject_for() を呼ぶ。gen_sims*.py で一般ページを作り直したときは、このスクリプトをもう一度実行する。
"""
import importlib, io, json, os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
FIGDIR = os.path.join(HERE, "figs")
sys.path.insert(0, FIGDIR)
BASE = "https://shimulabo.com"
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
START, END = "<!-- rika-figs:start -->", "<!-- rika-figs:end -->"
STYLE = ('<style id="rika-fig-style">.rika-figs{margin:8px 0 22px}.rika-fig{margin:0 0 18px}'
         '.rika-fig a.zoom{display:block}.rika-fig img{display:block;width:100%;height:auto;border:1px solid var(--line,#e2ded4);border-radius:8px;background:#faf8f3}'
         '.rika-fig figcaption{font-size:13.5px;line-height:1.7;margin-top:6px;color:var(--ink-2,#3d434b)}'
         '.rika-fig .dl{white-space:nowrap;margin-left:6px;font-size:12.5px}.rika-figs .fig-note{font-size:12.5px;color:var(--ink-2,#3d434b);margin:0}</style>')
NOTE_RIKA = "図はタップすると大きく表示されます。授業のプリント・スライド・板書計画に自由に使えます（出典「シミュラボ」とページのURLを添えてください）。"
NOTE_GEN = "図はタップすると大きく表示されます。資料やSNSに使うときは、出典「シミュラボ」とページのURLを添えてください。"


def rd(p): return io.open(p, encoding="utf-8").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)


def modules(only=None):
    names = sorted(f[:-3] for f in os.listdir(FIGDIR) if f.endswith(".py") and f not in ("figlib.py", "__init__.py"))
    if only: names = [n for n in names if n.replace("_", "-") in only or n in only]
    return names


def load(mod):
    m = importlib.import_module(mod)
    slug = getattr(m, "SLUG", mod.replace("_", "-"))
    for i, f in enumerate(m.FIGS, 1):
        for k in ("svg", "alt", "caption"): assert k in f, f"{mod} 図{i}: {k} がありません"
    return slug, m.FIGS, getattr(m, "ANCHOR", None)


def shrink(pp):
    """保存用 PNG を256色にして軽くする（図は色数が少ないので見た目はほぼ同じ・約3分の1）"""
    from PIL import Image
    im = Image.open(pp)
    if im.mode == "P": return
    im.convert("RGB").quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(pp, "PNG", optimize=True)


def write_files(slug, figs, png=True):
    d = os.path.join(ROOT, "sims", slug)
    assert os.path.isdir(d), f"sims/{slug}/ がありません"
    for i, f in enumerate(figs, 1):
        s = f["svg"]() if callable(f["svg"]) else f["svg"]
        assert s.startswith("<svg") and 'viewBox="0 0 1200 675"' in s, f"{slug} 図{i}: 1200×675 の svg ではありません"
        sp = os.path.join(d, f"{slug}-{i}.svg"); pp = os.path.join(d, f"{slug}-{i}.png")
        old = rd(sp) if os.path.exists(sp) else None
        if old != s: wr(sp, s)
        if png and (old != s or not os.path.exists(pp)):
            if os.path.exists(pp): os.remove(pp)
            prof = tempfile.mkdtemp(prefix="figs_chrome_")      # 何人かが同時に書き出してもぶつからないように
            subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--window-size=1200,675",
                            f"--user-data-dir={prof}", "--force-device-scale-factor=2", f"--screenshot={pp}",
                            "file:///" + sp.replace("\\", "/")], capture_output=True, timeout=120)
            shutil.rmtree(prof, ignore_errors=True)
            assert os.path.exists(pp), f"{slug} 図{i}: PNG を作れませんでした"
            shrink(pp)
    for fn in os.listdir(d):      # 図が減ったときの古いファイルを消す
        m = re.fullmatch(re.escape(slug) + r"-(\d+)\.(svg|png)", fn)
        if m and int(m.group(1)) > len(figs): os.remove(os.path.join(d, fn))


def block(slug, figs, rika):
    items = []
    for i, f in enumerate(figs, 1):
        alt = f["alt"].replace('"', "&quot;")
        items.append(f'''  <figure class="rika-fig" id="zu{i}">
    <a class="zoom" href="{slug}-{i}.png" target="_blank" rel="noopener"><img src="{slug}-{i}.svg" width="1200" height="675" loading="lazy" decoding="async" alt="{alt}"></a>
    <figcaption><b>図{i}</b>　{f["caption"]}<span class="dl"><a href="{slug}-{i}.png" download>PNGで保存</a>・<a href="{slug}-{i}.svg" download>SVG</a></span></figcaption>
  </figure>
''')
    return (f'{START}\n<div class="rika-figs">\n' + "".join(items) +
            f'  <p class="fig-note">{NOTE_RIKA if rika else NOTE_GEN}</p>\n</div>\n{END}\n')


def inject(slug, figs, anchor=None):
    p = os.path.join(ROOT, "sims", slug, "index.html")
    h = rd(p); h0 = h
    rika = 'href="../../rika/"' in h
    h = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n", "", h, flags=re.S)
    if 'id="rika-fig-style"' not in h:
        h = h.replace("</head>", STYLE + "\n</head>", 1)
    art = h.find('<article class="article">')
    assert art >= 0, f"{slug}: 本文（article）が見つかりません"
    m = None
    if anchor:
        m = re.compile(anchor, re.S).search(h, art)
        assert m, f"{slug}: ANCHOR {anchor!r} が見つかりません"
    if not m: m = re.compile(r"<h2[^>]*>[^<]*しくみ[^<]*</h2>\n?").search(h, art)
    if not m: m = re.compile(r"<h2[^>]*>.*?</h2>\s*(<p[ >].*?</p>\s*)?", re.S).search(h, art)
    assert m, f"{slug}: 図を入れる位置が見つかりません"
    h = h[:m.end()] + block(slug, figs, rika) + h[m.end():]

    def add_img(mm):       # 構造化データ（WebApplication）に image を入れる
        try: j = json.loads(mm.group(1))
        except Exception: return mm.group(0)
        t = j.get("@type"); t = t if isinstance(t, list) else [t]
        if "WebApplication" not in t: return mm.group(0)
        j["image"] = [f"{BASE}/sims/{slug}/{slug}-{i}.png" for i in range(1, len(figs) + 1)]
        return '<script type="application/ld+json">' + json.dumps(j, ensure_ascii=False) + "</script>"
    h = re.sub(r'<script type="application/ld\+json">(.*?)</script>', add_img, h, flags=re.S)
    if h != h0: wr(p, h)


def inject_for(slugs):
    """理科の build_sims.py から呼ぶ：作り直したページのうち、図の定義と SVG があるものに差し込み直す（PNG は作らない）"""
    have = {}
    for mod in modules():
        slug, figs, anchor = load(mod); have[slug] = (figs, anchor)
    for s in slugs:
        if s in have and os.path.exists(os.path.join(ROOT, "sims", s, f"{s}-1.svg")):
            inject(s, *have[s])


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    only = set(a[a.index("--only") + 1].split(",")) if "--only" in a else None
    n = 0
    for mod in modules(only):
        slug, figs, anchor = load(mod)
        write_files(slug, figs, png="--no-png" not in a)
        inject(slug, figs, anchor); n += len(figs)
        print(f"{slug}: 図{len(figs)}枚")
    print(f"計 {n}枚")
