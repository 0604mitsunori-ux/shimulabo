/* =========================================================
   シミュラボ リクエスト受付の窓口（req-api.js）
   - 送り先は Google Apps Script のウェブアプリ（スプレッドシートに溜まり、長澤さんのGmailに通知）
   - 送ったリクエストの受付番号はこのブラウザに覚えておき、
     「公開済み」になったら どのページでも右下にお知らせを出す（showDoneToast）
   ========================================================= */
(function () {
  var ENDPOINT = 'https://script.google.com/macros/s/AKfycbwajmyydg2DVMZcxjUI6LVambyxVjiU4LCU90UnUCKYHA6MbvpcfvmeSwIKWMCbbOrz9A/exec';
  var KEY = 'simulab:myreq';      // [{id, idea, at}]
  var SEEN = 'simulab:myreq:seen'; // お知らせを閉じた受付番号

  function lget(k, d) { try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } }
  function lset(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }

  function mine() { return lget(KEY, []); }
  function remember(id, idea) {
    var a = mine().filter(function (x) { return x.id !== id; });
    a.unshift({ id: id, idea: String(idea || '').slice(0, 80), at: Date.now() });
    lset(KEY, a.slice(0, 30));
  }

  function submit(data) {
    data.action = 'submit';
    return fetch(ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'text/plain;charset=utf-8' },   // プリフライトを起こさない
      body: JSON.stringify(data)
    }).then(function (r) { return r.json(); });
  }
  function list() {
    return fetch(ENDPOINT + '?list=1').then(function (r) { return r.json(); })
      .then(function (j) { return (j && j.items) || []; });
  }
  function status(ids) {
    if (!ids.length) return Promise.resolve([]);
    return fetch(ENDPOINT + '?ids=' + encodeURIComponent(ids.join(','))).then(function (r) { return r.json(); })
      .then(function (j) { return (j && j.items) || []; });
  }

  /* どのページでも：自分のリクエストが公開済みになっていたら右下にお知らせ */
  function showDoneToast() {
    var m = mine(); if (!m.length) return;
    if (/\/board\//.test(location.pathname)) return;   // ボードでは一覧の中で見せる
    var seen = lget(SEEN, []);
    var ids = m.map(function (x) { return x.id; }).filter(function (id) { return seen.indexOf(id) < 0; });
    if (!ids.length) return;
    // 1日に何度も問い合わせない（6時間ごと）
    var last = lget('simulab:myreq:checked', 0);
    if (Date.now() - last < 6 * 3600 * 1000) return;
    lset('simulab:myreq:checked', Date.now());
    status(ids).then(function (items) {
      var done = items.filter(function (x) { return x.status === '公開済み' && x.url; });
      if (!done.length) return;
      var d = done[0];
      var box = document.createElement('div');
      box.setAttribute('role', 'status');
      box.style.cssText = 'position:fixed;right:14px;bottom:14px;left:14px;max-width:380px;margin-left:auto;z-index:9999;background:#fff;border:2px solid #c2452d;border-radius:16px;padding:14px 16px 14px;box-shadow:0 10px 30px rgba(0,0,0,.18);font-size:14px;line-height:1.6;color:#1d1d1f;';
      var t = document.createElement('div'); t.style.cssText = 'font-weight:800;font-size:15px;margin-bottom:4px;';
      t.textContent = '🎉 あなたのリクエストが形になりました！';
      var p = document.createElement('div'); p.style.cssText = 'color:#555;font-size:13px;margin-bottom:10px;';
      p.textContent = '「' + String(d.idea).slice(0, 40) + (String(d.idea).length > 40 ? '…' : '') + '」';
      var a = document.createElement('a'); a.href = d.url; a.textContent = 'できたシミュを見る →';
      a.style.cssText = 'display:inline-block;background:#c2452d;color:#fff;font-weight:800;padding:10px 18px;border-radius:10px;text-decoration:none;';
      var x = document.createElement('button'); x.type = 'button'; x.textContent = '×'; x.setAttribute('aria-label', '閉じる');
      x.style.cssText = 'position:absolute;top:6px;right:10px;border:none;background:none;font-size:20px;cursor:pointer;color:#888;';
      function close() { var s = lget(SEEN, []); s.push(d.id); lset(SEEN, s); box.remove(); }
      x.onclick = close; a.addEventListener('click', function () { var s = lget(SEEN, []); s.push(d.id); lset(SEEN, s); });
      box.appendChild(x); box.appendChild(t); box.appendChild(p); box.appendChild(a);
      document.body.appendChild(box);
    }).catch(function () {});
  }

  window.ReqAPI = { ENDPOINT: ENDPOINT, submit: submit, list: list, status: status, mine: mine, remember: remember, showDoneToast: showDoneToast };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', showDoneToast); else showDoneToast();
})();
