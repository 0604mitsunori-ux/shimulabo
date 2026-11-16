"""トップの人気ランキングを GA4 実データ版に差し替え（2026-11-16）。冪等ではないので1回だけ実行。"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
p = ROOT / "index.html"
s = p.read_text(encoding="utf-8")

old_sec = '''  <section class="rank-wrap">
    <div class="rank-head">
      <h2>🏆 人気のシミュレーション</h2>
      <span class="note">注目度の高い順</span>
    </div>
    <div class="rank-list" id="rankList"></div>
  </section>'''
new_sec = '''  <section class="rank-wrap" id="rankWrap" aria-labelledby="rankTitle">
    <div class="rank-head">
      <h2 id="rankTitle">🏆 人気ランキング</h2>
      <span class="note" id="rankNote">みんなが本当に遊んだ回数で集計</span>
    </div>
    <div class="play-counter" id="playCounter" hidden>
      <div class="pc-main">
        <span class="pc-label">これまでに</span>
        <b class="pc-num" id="pcTotal">0</b>
        <span class="pc-unit">回 シミュレーションされました</span>
      </div>
      <div class="pc-sub">
        <span>今週 <b id="pcWeek">-</b>回</span>
        <span>きのう <b id="pcYday">-</b>回</span>
        <span class="pc-trend" id="pcTrend"></span>
      </div>
    </div>
    <div class="rank-tabs" role="tablist" aria-label="ランキングの期間" id="rankTabs" hidden>
      <button type="button" role="tab" data-k="week" aria-selected="true">今週</button>
      <button type="button" role="tab" data-k="rising" aria-selected="false">急上昇</button>
      <button type="button" role="tab" data-k="month" aria-selected="false">今月</button>
      <button type="button" role="tab" data-k="all" aria-selected="false">全期間</button>
    </div>
    <div class="rank-list" id="rankList" role="tabpanel" aria-labelledby="rankTitle"></div>
    <button type="button" class="rank-more" id="rankMore" hidden>6〜10位も見る</button>
    <p class="rank-src" id="rankSrc" hidden></p>
  </section>'''
assert old_sec in s
s = s.replace(old_sec, new_sec)

old_ms = '''    <span><b>953</b>本 公開中</span>'''
new_ms = '''    <span><b>953</b>本 公開中</span>
    <span class="sep ms-plays" hidden></span>
    <span class="ms-plays" hidden><b id="msTotal">-</b>回 遊ばれた</span>'''
assert old_ms in s
s = s.replace(old_ms, new_ms, 1)

a = s.index("  (async function renderRanking(){")
b = s.index("  /* ===== ギャラリーカードに拡散数を表示")
new_js = (ROOT / "scripts" / "_ranking_snippet.js").read_text(encoding="utf-8")
s = s[:a] + new_js + "\n" + s[b:]
p.write_text(s, encoding="utf-8")
print("ok")
