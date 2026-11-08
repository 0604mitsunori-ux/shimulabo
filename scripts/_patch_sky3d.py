# -*- coding: utf-8 -*-
"""既存の天体ページに「3Dで見る」を足す（2026-11-08）。2Dの図と操作はそのまま、同じスライダーで動く3Dを下に置く
   使い方: python scripts/_patch_sky3d.py [slug ...]   … 何度実行しても同じ結果（前に入れた3Dの部分は入れ直す）
   3Dの中身は sims/<slug>/view3d.js。three.js は見える位置までスクロールしてから読み込む
"""
import io, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = {
    "tsuki-michikake": ([("top", "宇宙（北極の上）から"), ("side", "ななめから"), ("earth", "地球から月を見る")],
                        "太陽・地球・月を3Dで回して見られます（大きさと距離は誇張）。「地球から月を見る」にすると、地球のそばから見た月の形になります。月齢と時刻は上のスライダーで動かしてください。", None),
    "gesshoku-nisshoku": ([("moon", "月のそば（地球から見る向き）"), ("side", "横から全体"), ("earth", "地球のそば")],
                          "太陽・地球・月の大きさと距離を実際の比率で並べ、地球の影（本影・半影）と月の影を3Dで表示しています。上の「見るとき」「月齢」「通り道のずれ」と連動します。", None),
    "taiyou-ugoki": ([("persp", "ななめ上（南南東）から"), ("top", "真上から"), ("east", "東から")],
                     "透明半球を3Dで回して見られます。オレンジが選んだ日の太陽の通り道、点線が夏至・春分秋分・冬至です。中心の棒の影も、太陽の位置に合わせて動きます。",
                     None),
    "hoshi-ugoki": ([("south", "南を見る"), ("north", "北を見る"), ("east", "東を見る"), ("west", "西を見る"), ("out", "天球を外から")],
                    "東京で見上げた星空を3Dにしています。「天球を外から」にすると、星が北極星の近くを軸にして回っている様子（天球の回転）が分かります。上の日付・時刻・注目する星と連動します。",
                    ("  const AS=", "  window.__hoshi={ST:ST,CO:CO,LAT:LAT,LON:LON};\n  const AS=")),
    "kinsei-michikake": ([("top", "北極の上から"), ("side", "ななめから"), ("earth", "地球から金星を見る")],
                         "太陽・金星・地球の位置を3Dで表示しています（大きさは誇張）。「地球から金星を見る」で、望遠鏡で見たときの金星の形と向きになります。上の日付と連動します。",
                         ("  function visOf(st){", "  { const __st0=state; state=function(){ const s=__st0(); window.__sim2d={lv:s.lv, le:s.le}; return s; }; }\n  function visOf(st){")),
}
CSS = '<link rel="stylesheet" href="../../assets/three/sim3d.css?v=1">'
LOADER = """<script>(()=>{const el=document.getElementById('view3d');if(!el)return;const go=()=>import('./view3d.js?v=1').catch(()=>{const l=el.querySelector('.load');if(l)l.textContent='3D表示を読み込めませんでした';});if('IntersectionObserver' in window){const io=new IntersectionObserver(es=>{if(es[0].isIntersecting){io.disconnect();go();}},{rootMargin:'300px'});io.observe(el);}else go();})();</script>"""

for slug in (sys.argv[1:] or PAGES):
    cams, legend, hook = PAGES[slug]
    p = os.path.join(ROOT, "sims", slug, "index.html")
    h = io.open(p, encoding="utf-8").read()
    assert os.path.isfile(os.path.join(ROOT, "sims", slug, "view3d.js")), slug
    h = re.sub(r"\n?<!-- sky3d:start -->.*?<!-- sky3d:end -->", "", h, flags=re.S)
    h = re.sub(r"\n?<!-- sky3d-loader:start -->.*?<!-- sky3d-loader:end -->", "", h, flags=re.S)
    if CSS not in h:
        h = h.replace('<link rel="stylesheet" href="../../assets/style.css?v=4">', '<link rel="stylesheet" href="../../assets/style.css?v=4">\n' + CSS, 1)
    btns = "".join('<button data-v="%s"%s>%s</button>' % (k, ' class="on"' if i == 0 else "", t) for i, (k, t) in enumerate(cams))
    block = """
<!-- sky3d:start -->
    <div class="v3d-block" style="width:100%%;margin-top:18px;">
      <h3 style="margin:0 0 8px;font-size:15px;">🧊 3Dで見る（ドラッグで回転・上の操作と連動）</h3>
      <div class="view3d dark" id="view3d"><div class="load">3D模型を読み込み中…</div><div class="hud" id="hud3d" style="display:none"></div></div>
      <div class="cam-row" id="camRow3d">%s</div>
      <p class="lab-legend" style="margin-top:6px;">%s</p>
    </div>
<!-- sky3d:end -->""" % (btns, legend)
    m = re.search(r'<p class="lab-legend">.*?</p>', h, flags=re.S)
    assert m, slug
    h = h[:m.end()] + block + h[m.end():]
    h = h.replace('<script src="../../assets/share-counter.js', "<!-- sky3d-loader:start -->\n" + LOADER + "\n<!-- sky3d-loader:end -->\n" + '<script src="../../assets/share-counter.js', 1)
    if hook and hook[1] not in h:
        assert hook[0] in h, (slug, "hook")
        h = h.replace(hook[0], hook[1], 1)
    io.open(p, "w", encoding="utf-8").write(h)
    print("patched", slug)
