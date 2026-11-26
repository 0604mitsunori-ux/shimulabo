/* =========================================================
   シミュラボ YouTube へのクリックを数える（yt-track.js）2026-11-26
   - サイト内のどこからでも、YouTube（youtube.com / youtu.be）へのリンクが押されたら
     GA4 にイベント yt_outbound_click を送る。
       link_type : watch（動画）／subscribe（チャンネル登録）／channel（チャンネル）／other
       video_id  : 動画のID（動画へのリンクのとき）
       place     : sim_embed（シミュページの動画の下）／top（トップの帯）／douga（動画ページ）／
                   request_done（リクエスト送信後のカード）／footer／other
       from_sim  : タイトル下の案内（yt_promo_click）を押して来た人なら、その元のシミュの名前
   - 読み込む場所：シミュページ（assets/share-counter.js が読み込む）・トップ・動画ページ・リクエストページ
   - ほかの YouTube 関連のイベント：
       yt_promo_click（タイトル下の案内を押した）／yt_promo_hide（×でかくした）
       yt_play（サイト内で再生ボタンを押した）／yt_subscribe_click（動画ページの登録ボタン）／yt_popular_click（トップの人気動画）
   ========================================================= */
(function () {
  if (window.__ytTrack) return; window.__ytTrack = 1;
  function kind(u) {
    if (/[?&]sub_confirmation=1/.test(u)) return 'subscribe';
    if (/\/watch\?|youtu\.be\/|\/shorts\//.test(u)) return 'watch';
    if (/\/channel\/|\/@/.test(u)) return 'channel';
    return 'other';
  }
  function vid(u) {
    var m = u.match(/[?&]v=([\w-]{6,})/) || u.match(/youtu\.be\/([\w-]{6,})/) || u.match(/\/shorts\/([\w-]{6,})/);
    return m ? m[1] : '';
  }
  function place(a) {
    if (a.closest('.yt-video')) return 'sim_embed';
    if (a.closest('.yt-top')) return 'top';
    if (a.closest('.rb')) return 'request_done';
    if (/\/douga\//.test(location.pathname)) return 'douga';
    if (a.closest('footer')) return 'footer';
    return 'other';
  }
  function onClick(e) {
    if (e.type === 'auxclick' && e.button !== 1) return;   // まん中クリック（新しいタブで開く）も数える
    var a = e.target && e.target.closest ? e.target.closest('a[href]') : null;
    if (!a) return;
    var u = a.href || '';
    if (!/^https?:\/\/(www\.|m\.)?(youtube\.com|youtu\.be)\//.test(u)) return;
    var from = '';
    try { from = sessionStorage.getItem('simulab:ytfrom') || ''; } catch (er) {}
    try { gtag('event', 'yt_outbound_click', { link_type: kind(u), video_id: vid(u), place: place(a), from_sim: from, transport_type: 'beacon' }); } catch (er) {}
  }
  document.addEventListener('click', onClick, true);
  document.addEventListener('auxclick', onClick, true);
})();
