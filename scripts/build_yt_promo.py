"""全シミュページのタイトル下に出す「YouTubeで壮大なシミュレーション」の案内（assets/yt-promo.js）を作る（2026-11-26）。
何度実行しても同じ結果。

- 動画の一覧は scripts/add_youtube_videos.py の EPISODES を読む（新しい動画を足したら、これも実行する）
- 小さいサムネ（240×135）を assets/yt/s/<動画ID>.jpg に作る（各ページで読む画像を軽くするため）
- 出す場所は各ページの .sim-head の最後（タイトルと説明文のすぐ下）。差し込みは assets/share-counter.js が
  assets/yt-promo.js を読み込んで行う（全845ページが share-counter.js を読んでいるので、ページの作り直しは不要）
- リンク先はサイト内の /douga/（学校のフィルタで youtube.com が開けない端末でも開けるように）

使い方： python scripts/add_youtube_videos.py && python scripts/build_youtube_page.py && python scripts/build_yt_promo.py
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from add_youtube_videos import EPISODES, ENABLED  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 理科の授業向けページ（パンくずに rika/ があるページ）では出さない動画（題に「死刑」など、授業で映すのに向かない言葉があるもの）
SCHOOL_SKIP = {"y62ExHjqXfs"}

# ---------- 小さいサムネ ----------
from PIL import Image  # noqa: E402

os.makedirs(os.path.join(ROOT, "assets", "yt", "s"), exist_ok=True)
eps = []
for e in EPISODES:
    src = os.path.join(ROOT, "assets", "yt", e["vid"] + ".jpg")
    if not os.path.exists(src):
        print("サムネなし（とばす）:", e["vid"])
        continue
    dst = os.path.join(ROOT, "assets", "yt", "s", e["vid"] + ".jpg")
    if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(src):
        Image.open(src).convert("RGB").resize((240, 135), Image.LANCZOS).save(dst, "JPEG", quality=80, optimize=True)
    d = {"v": e["vid"], "t": e["title"], "s": e["sub"], "l": e["len"]}
    if e["vid"] in SCHOOL_SKIP:
        d["x"] = 1   # 理科のページでは出さない
    eps.append(d)

JS = r"""/* =========================================================
   シミュラボ タイトル下の YouTube 案内（yt-promo.js）
   ※このファイルは scripts/build_yt_promo.py が作る。直接書きかえない。
   - 各シミュページの .sim-head の最後（タイトルと説明文のすぐ下）に1行の案内を出す
   - 動画はページと日付で入れかわる（同じページでも日がたつと別の動画）
   - リンク先はサイト内の /douga/（学校の端末でも開ける）
   - × で30日間かくせる（授業で映すときのため）
   ========================================================= */
(function () {
  var EP = __EP__;
  var ON = __ON__;
  var HIDE = 'simulab:ytpromo:hide', DAYS = 30;
  if (!ON || !EP.length) return;
  function run() {
    try {
      var head = document.querySelector('.sim-head');
      if (!head || document.querySelector('.ytp') || document.querySelector('.yt-video')) return;   // 動画をうめこんであるページには出さない
      var hid = 0; try { hid = parseInt(localStorage.getItem(HIDE), 10) || 0; } catch (e) {}
      if (hid && Date.now() - hid < DAYS * 864e5) return;
      var me = document.querySelector('script[src*="assets/share-counter.js"]');
      var base = me ? me.getAttribute('src').replace(/assets\/share-counter\.js.*$/, '') : '../../';
      var slug = (location.pathname.match(/\/sims\/([^\/]+)/) || [0, ''])[1], h = 0;
      for (var i = 0; i < slug.length; i++) h = (h * 31 + slug.charCodeAt(i)) >>> 0;
      var list = EP;
      if (document.querySelector('.breadcrumb a[href$="rika/"]')) list = EP.filter(function (e) { return !e.x; });   // 理科の授業向けページ
      if (!list.length) return;
      var ep = list[(h + Math.floor(Date.now() / 864e5)) % list.length];

      if (!document.getElementById('ytpCss')) {
        var st = document.createElement('style'); st.id = 'ytpCss';
        st.textContent =
          '.ytp{position:relative;display:flex;align-items:center;gap:12px;margin:14px 0 0;padding:8px 40px 8px 8px;border:1px solid var(--line,#e2ded4);border-radius:14px;background:#fff;text-decoration:none;color:var(--ink,#14181d);text-align:left;max-width:640px}' +
          '.ytp:hover{border-color:#e5484d;box-shadow:0 4px 14px rgba(0,0,0,.06)}' +
          '.ytp-th{position:relative;flex:0 0 auto;width:112px;aspect-ratio:16/9;border-radius:9px;overflow:hidden;background:#111}' +
          '.ytp-th img{width:100%;height:100%;object-fit:cover;display:block}' +
          '.ytp-th i{position:absolute;inset:0;margin:auto;width:30px;height:21px;border-radius:6px;background:#e5484d;display:flex;align-items:center;justify-content:center}' +
          '.ytp-th i::after{content:"";border-style:solid;border-width:5px 0 5px 9px;border-color:transparent transparent transparent #fff;margin-left:2px}' +
          '.ytp-th b{position:absolute;right:4px;bottom:4px;background:rgba(0,0,0,.78);color:#fff;font-size:10px;font-weight:700;line-height:1;padding:2px 4px;border-radius:4px}' +
          '.ytp-tx{min-width:0;flex:1 1 auto;line-height:1.45}' +
          '.ytp-k{display:block;font-size:11.5px;font-weight:800;color:#c4302b;letter-spacing:.02em}' +
          '.ytp-t{display:block;font-size:14px;font-weight:800;overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical}' +
          '.ytp-s{display:block;font-size:12px;color:var(--ink-2,#59616c);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}' +
          '.ytp-x{position:absolute;top:2px;right:4px;width:30px;height:30px;border:0;background:none;color:var(--ink-3,#8b929c);font-size:18px;line-height:1;cursor:pointer;border-radius:50%}' +
          '.ytp-x:hover{background:rgba(0,0,0,.06);color:var(--ink,#14181d)}' +
          '@media(max-width:480px){.ytp{gap:10px}.ytp-th{width:92px}.ytp-t{font-size:13px}.ytp-s{display:none}}';
        document.head.appendChild(st);
      }

      var a = document.createElement('a');
      a.className = 'ytp'; a.href = base + 'douga/';
      a.setAttribute('aria-label', 'YouTubeの動画：' + ep.t);
      var th = document.createElement('span'); th.className = 'ytp-th';
      var im = document.createElement('img'); im.src = base + 'assets/yt/s/' + ep.v + '.jpg'; im.alt = ''; im.width = 240; im.height = 135; im.loading = 'lazy'; im.decoding = 'async';
      th.appendChild(im); th.appendChild(document.createElement('i'));
      var ln = document.createElement('b'); ln.textContent = ep.l; th.appendChild(ln);
      var tx = document.createElement('span'); tx.className = 'ytp-tx';
      var k = document.createElement('span'); k.className = 'ytp-k'; k.textContent = '▶ もっと壮大なシミュレーションは、YouTubeで';
      var t = document.createElement('span'); t.className = 'ytp-t'; t.textContent = ep.t;
      var s = document.createElement('span'); s.className = 'ytp-s'; s.textContent = ep.s + '（3Dの動画・毎日19時に新作）';
      tx.appendChild(k); tx.appendChild(t); tx.appendChild(s);
      var x = document.createElement('button'); x.type = 'button'; x.className = 'ytp-x'; x.textContent = '×'; x.setAttribute('aria-label', 'この案内をかくす');
      x.addEventListener('click', function (e) { e.preventDefault(); e.stopPropagation(); try { localStorage.setItem(HIDE, String(Date.now())); } catch (er) {} a.remove(); try { gtag('event', 'yt_promo_hide', { item_id: slug }); } catch (er) {} });
      a.addEventListener('click', function () { try { gtag('event', 'yt_promo_click', { item_id: slug, video: ep.v }); } catch (er) {} });
      a.appendChild(th); a.appendChild(tx); a.appendChild(x);
      head.appendChild(a);
    } catch (e) {}
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run); else run();
})();
"""

out = JS.replace("__EP__", json.dumps(eps, ensure_ascii=False)).replace("__ON__", "true" if ENABLED else "false")
io.open(os.path.join(ROOT, "assets", "yt-promo.js"), "w", encoding="utf-8", newline="\n").write(out)
print(f"assets/yt-promo.js（動画{len(eps)}本）")
