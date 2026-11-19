/* =========================================================
   トップ「みんなで作るシミュラボ」（2026-11-19）
   - assets/requests.json（手で整えた一覧）＋ ReqAPI.list()（ボードに掲載OKの新着）を合わせて表示
   - このブラウザから送ったリクエストは「あなたのリクエスト」として先頭に出す
   - 1行入力からその場でリクエストを送れる（送り先は req-api.js と同じ GAS）
   ========================================================= */
(function () {
  var root = document.getElementById('reqLive');
  if (!root) return;
  var base = (document.currentScript && document.currentScript.src) || location.href;
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };
  var day = function (s) { var d = new Date(s); return isNaN(d) ? '' : (d.getMonth() + 1) + '/' + d.getDate(); };
  var EXAMPLES = ['一生でまばたきは何回する？', '信号がなかったら交差点はどうなる？', '毎日1万歩、1年で地球を何％歩く？', '雪の結晶はどうやってできる？',
    'コンビニコーヒーをやめたら10年でいくら？', 'もし地球の自転が2倍の速さになったら？', '教室の二酸化炭素、換気しないとどうなる？'];

  root.innerHTML =
    '<div class="rl-head"><div>' +
      '<div class="rl-kicker">みんなで作るシミュラボ</div>' +
      '<h2>💡 次のシミュは、あなたのアイデアで。</h2>' +
      '<p class="rl-lead" id="rlLead">「これ、数字やアニメで見てみたい」を送ってください。面白いアイデアから実際に作って公開します。</p>' +
    '</div><div class="rl-stats" aria-label="リクエストの状況">' +
      '<div class="rl-stat wait"><b id="rlWait">0</b><span>📮 受付中</span></div>' +
      '<div class="rl-stat make"><b id="rlMake">0</b><span>🛠️ 制作中</span></div>' +
      '<div class="rl-stat done"><b id="rlDone">0</b><span>🎉 公開済み</span></div>' +
    '</div></div>' +
    '<form class="rl-form" id="rlForm" autocomplete="off">' +
      '<label for="rlIdea" class="rl-hp">見たいシミュ</label>' +
      '<input id="rlIdea" type="text" maxlength="200" placeholder="例）' + esc(EXAMPLES[0]) + '" aria-label="見たいシミュレーション">' +
      '<input class="rl-hp" id="rlWeb" type="text" tabindex="-1" aria-hidden="true">' +
      '<button type="submit" id="rlBtn">リクエストする →</button>' +
    '</form>' +
    '<p class="rl-sub">登録不要・1行でOK。ニックネームやメール（できたらお知らせ）も付けたい人は <a href="request/">くわしく送る</a></p>' +
    '<div id="rlMsg"></div>' +
    '<div class="rl-flow" aria-hidden="true"><span>① 送る</span><i>→</i><span>② つくり手が読む</span><i>→</i><span>③ 制作中に表示</span><i>→</i><span>④ 公開してお知らせ</span></div>' +
    '<div class="rl-cards" id="rlCards"></div>' +
    '<div class="rl-foot"><a href="board/">📋 リクエストと進み具合をぜんぶ見る →</a><span class="hint">横にスクロールできます</span></div>';

  // 入力例をゆっくり入れ替える
  var ex = 0, inp = document.getElementById('rlIdea');
  setInterval(function () { if (document.activeElement === inp || inp.value) return; ex = (ex + 1) % EXAMPLES.length; inp.placeholder = '例）' + EXAMPLES[ex]; }, 3500);

  var items = [], mine = [];
  function card(r) {
    var st = r.mine ? (r.status || '受付') : (r.status || '受付');
    var url = r.url ? (r.url.charAt(0) === '/' ? r.url.slice(1) : r.url) : '';
    if (url && !/^(sims\/|https:\/\/shimulabo\.com\/)/.test(url)) url = '';
    var who = r.from === 'board' ? 'はじめのボード案' : (r.nick ? r.nick + ' さん' : '') + (r.from === 'teacher' ? '（先生）' : '');
    var meta = [who, r.at ? day(r.at) + ' 受付' : '', r.done ? day(r.done) + ' 公開' : ''].filter(Boolean).join('・');
    var badge = (r.mine ? '<span class="rl-badge s-mine">あなた</span>' : '') + '<span class="rl-badge s-' + esc(st) + '">' + esc(st) + '</span>';
    var inner = '<div class="top"><span class="em">' + esc(r.e || (st === '制作中' ? '🛠️' : st === '公開済み' ? '🎉' : '📮')) + '</span>' + badge + '</div>' +
      '<div class="idea">' + esc(r.idea) + '</div>' +
      (st === '制作中' ? '<div class="bar"><i></i></div>' : '') +
      (meta ? '<div class="meta">' + esc(meta) + '</div>' : '') +
      (st === '公開済み' && url ? '<div class="go">→ ' + esc(r.name || 'できたシミュを見る') + '</div>' : '');
    var cls = 'rl-card' + (st === '制作中' ? ' make' : '');
    return (st === '公開済み' && url) ? '<a class="' + cls + '" href="' + esc(url) + '">' + inner + '</a>' : '<div class="' + cls + '">' + inner + '</div>';
  }
  function render() {
    var seen = {}, list = [];
    mine.concat(items).forEach(function (r) { if (r && r.idea && !seen[r.id]) { seen[r.id] = 1; list.push(r); } });
    var n = { 受付: 0, 制作中: 0, 公開済み: 0 };
    list.forEach(function (r) { n[r.status || '受付'] = (n[r.status || '受付'] || 0) + 1; });
    document.getElementById('rlWait').textContent = n['受付'];
    document.getElementById('rlMake').textContent = n['制作中'];
    document.getElementById('rlDone').textContent = n['公開済み'];
    document.getElementById('rlLead').innerHTML = '送られたアイデアから、これまでに <b>' + n['公開済み'] + '</b> 本のシミュが生まれました。早いものは<b>翌日</b>に公開しています。';
    var open = (n['受付'] + n['制作中'] === 0)
      ? '<div class="rl-card open" id="rlOpen"><div class="top" style="justify-content:center"><span class="em">📮</span></div>' +
        '<div class="idea">いま受付中のリクエストは 0件</div><div class="meta">次に作る1本は、あなたのアイデアかも。<br>上の欄に1行で送れます。</div></div>' : '';
    var act = list.filter(function (r) { return r.status !== '公開済み'; });
    var done = list.filter(function (r) { return r.status === '公開済み'; });
    document.getElementById('rlCards').innerHTML = act.map(card).join('') + open + done.slice(0, 8).map(card).join('');
    var o = document.getElementById('rlOpen');
    if (o) o.onclick = function () { inp.focus(); };
  }

  fetch(new URL('requests.json', base).href, { cache: 'no-cache' }).then(function (r) { return r.ok ? r.json() : { items: [] }; })
    .then(function (j) { items = (j.items || []).concat(items.filter(function (x) { return x.live; })); render(); }).catch(render);

  function loadLive() {
    if (!window.ReqAPI) return;
    ReqAPI.list().then(function (arr) {
      arr.forEach(function (r) {
        if (items.some(function (x) { return x.id === r.id; })) return;
        var u = /^https:\/\/shimulabo\.com\//.test(r.url || '') ? r.url : '';
        items.unshift({ id: r.id, idea: r.idea, nick: r.nick, at: r.at, status: r.status || '受付', url: u, live: true });
      });
      render();
    }).catch(function () {});
    var m = ReqAPI.mine();
    if (m.length) {
      mine = m.slice(0, 5).map(function (x) { return { id: x.id, idea: x.idea, at: x.at, status: '受付', mine: true }; });
      render();
      ReqAPI.status(m.slice(0, 5).map(function (x) { return x.id; })).then(function (arr) {
        var by = {}; arr.forEach(function (x) { by[x.id] = x; });
        mine = mine.map(function (x) { var s = by[x.id]; return s ? { id: x.id, idea: s.idea || x.idea, at: x.at, status: s.status || '受付', url: /^https:\/\/shimulabo\.com\//.test(s.url || '') ? s.url : '', mine: true } : x; });
        render();
      }).catch(function () {});
    }
  }
  if (window.ReqAPI) loadLive(); else window.addEventListener('load', loadLive);

  // 1行リクエスト
  var busy = false;
  document.getElementById('rlForm').addEventListener('submit', function (e) {
    e.preventDefault();
    var msg = document.getElementById('rlMsg'), btn = document.getElementById('rlBtn');
    var idea = inp.value.trim();
    if (!idea) { msg.className = 'rl-msg ng'; msg.textContent = '⚠️ 見てみたいシミュを1行で書いてください。'; inp.focus(); return; }
    if (busy || !window.ReqAPI) return;
    busy = true; btn.disabled = true; btn.textContent = '送信中…'; msg.textContent = '';
    ReqAPI.submit({ idea: idea, genre: 'その他・おまかせ', why: '', nick: '', email: '', website: document.getElementById('rlWeb').value })
      .then(function (j) {
        if (!j || !j.ok) throw new Error((j && j.error) || 'failed');
        ReqAPI.remember(j.id, idea);
        mine.unshift({ id: j.id, idea: idea, at: new Date().toISOString(), status: '受付', mine: true });
        render();
        msg.className = 'rl-msg ok';
        msg.innerHTML = '📮 <b>受け付けました！</b>（受付番号 ' + esc(j.id) + '）できたら、このブラウザでシミュラボを開いたときにお知らせが出ます。' +
          ' <a href="board/?id=' + encodeURIComponent(j.id) + '">進み具合を見る →</a>';
        inp.value = '';
        try { gtag('event', 'request_submit', { genre: 'top_quick' }); } catch (er) {}
      })
      .catch(function (er) {
        msg.className = 'rl-msg ng';
        msg.textContent = '⚠️ うまく送れませんでした。少し時間をおいてもう一度お試しください。' + (String(er.message) === 'busy' ? '（ただいま混み合っています）' : '');
      })
      .then(function () { busy = false; btn.disabled = false; btn.textContent = 'リクエストする →'; });
  });
})();
