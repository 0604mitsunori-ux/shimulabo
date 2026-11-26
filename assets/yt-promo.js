/* =========================================================
   シミュラボ タイトル下の YouTube 案内（yt-promo.js）
   ※このファイルは scripts/build_yt_promo.py が作る。直接書きかえない。
   - 各シミュページの .sim-head の最後（タイトルと説明文のすぐ下）に1行の案内を出す
   - 動画はページと日付で入れかわる（同じページでも日がたつと別の動画）
   - リンク先はサイト内の /douga/（学校の端末でも開ける）
   - × で30日間かくせる（授業で映すときのため）
   ========================================================= */
(function () {
  var EP = [{"v": "RIUNkEa7ZBw", "t": "全員が150歳まで生きられる村、300年後どうなる？", "s": "80歳の村と並べて300年早送り", "l": "9:08"}, {"v": "93-rkmJ1Iis", "t": "奪う町と交換する町、200年後に栄えるのは？", "s": "砂漠の6つのオアシスを200年早送り", "l": "8:23"}, {"v": "OEXjk8rvKTY", "t": "守る村と試す村、200年後に栄えるのは？", "s": "天気が変わる谷の棚田を200年早送り", "l": "8:46"}, {"v": "Q6xXKIcol34", "t": "すぐ動く人と考えてから動く人、1年後に多く集めるのは？", "s": "霧の森で木の実集めを100回", "l": "9:04"}, {"v": "y62ExHjqXfs", "t": "すべての罪を死刑にしたら、町はどうなる？", "s": "1000人の町を30年動かした結果", "l": "8:29", "x": 1}, {"v": "khhWAN6QtGU", "t": "日本にゾンビが1体現れたら、全滅まで何日？", "s": "100回シミュレーションした結果", "l": "10:06"}, {"v": "qCl_Q5FrR5Y", "t": "優しい村に乱暴な人が1人来たら？", "s": "150日後の意外な結末", "l": "9:26"}, {"v": "Tz7QjIJqpgo", "t": "協力の港と競争の港、200年後に残るのは？", "s": "同じ島の2つの港を200年早送り", "l": "8:48"}];
  var ON = true;
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
