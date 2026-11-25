/* =========================================================
   シミュラボ リクエスト送信後の「シェアで優先」カード（req-boost.js）2026-11-25
   - リクエストを送った直後の画面に出す。必須ではなく「優先」。
   - シェア → その投稿のURLを貼って送る → 受付表に「シェア報告」として入る（つくり手が実際に見て確かめる）
   - URLの送り先は今の受付（ReqAPI.submit）。genre='シェア報告'・idea に受付番号・why にURL。
     掲載（○）にしないので、サイトの一覧には出ない。
   - YouTube は「登録したら優先」にはしない（見返りつきの登録は YouTube のルールで問題になるため）。案内だけ。
   使い方： ReqBoost.mount(入れ物の要素, { id: 受付番号, idea: 送った文, yt: YouTubeの「もしも」なら true, base: サイトのルートへの相対パス })
   ========================================================= */
(function () {
  var YT_URL = 'https://www.youtube.com/channel/UCzu0T5y3udo8jnZwVnTtOxw?sub_confirmation=1';
  var SITE = 'https://shimulabo.com';
  var TAG = '#シミュラボ リクエスト企画';
  var SENT = 'simulab:boost:sent';   // シェアURLを送った受付番号

  function lget(k, d) { try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } }
  function lset(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  function ev(action) { try { gtag('event', 'request_boost', { action: action }); } catch (e) {} }
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }

  function css() {
    if (document.getElementById('rbCss')) return;
    var s = document.createElement('style'); s.id = 'rbCss';
    s.textContent =
      '.rb{margin:16px auto 18px;max-width:560px;text-align:left;background:#fff8ef;border:1.5px solid #f0d9b8;border-radius:16px;padding:16px 16px 14px;color:var(--ink,#14181d);font-size:14px;line-height:1.7}' +
      '.rb h3{margin:0 0 4px;font-size:16px;line-height:1.5}' +
      '.rb p{margin:0 0 10px;color:var(--ink-2,#59616c);font-size:13.5px}' +
      '.rb-steps{margin:0 0 10px;padding:0;list-style:none;counter-reset:rb}' +
      '.rb-steps>li{counter-increment:rb;position:relative;padding:0 0 12px 30px}' +
      '.rb-steps>li::before{content:counter(rb);position:absolute;left:0;top:1px;width:21px;height:21px;border-radius:50%;background:var(--accent,#c4442b);color:#fff;font-size:12px;font-weight:800;display:flex;align-items:center;justify-content:center}' +
      '.rb-steps b{display:block;font-size:14px;margin-bottom:5px}' +
      '.rb textarea{width:100%;box-sizing:border-box;min-height:128px;border:1.5px solid var(--line,#e2ded4);border-radius:10px;padding:9px 10px;font:inherit;font-size:13.5px;line-height:1.6;background:#fff;resize:vertical}' +
      '.rb-row{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px}' +
      '.rb-btn{display:inline-flex;align-items:center;justify-content:center;gap:6px;border:1.5px solid var(--line,#e2ded4);background:#fff;color:var(--ink,#14181d);border-radius:999px;padding:9px 16px;font:inherit;font-size:13.5px;font-weight:800;cursor:pointer;text-decoration:none}' +
      '.rb-btn.x{background:#14181d;border-color:#14181d;color:#fff}' +
      '.rb-btn.go{background:var(--accent,#c4442b);border-color:var(--accent,#c4442b);color:#fff}' +
      '.rb-btn:disabled{opacity:.6;cursor:default}' +
      '.rb-url{display:flex;gap:8px;flex-wrap:wrap}' +
      '.rb-url input{flex:1 1 220px;min-width:0;border:1.5px solid var(--line,#e2ded4);border-radius:10px;padding:9px 10px;font:inherit;font-size:14px;background:#fff}' +
      '.rb-msg{font-size:13px;font-weight:700;margin:8px 0 0;min-height:1.2em}' +
      '.rb-msg.ok{color:#1c7c54}.rb-msg.ng{color:var(--accent-d,#9d3320)}' +
      '.rb-yt{border-top:1px dashed #e8cfa8;margin-top:4px;padding-top:12px;display:flex;flex-wrap:wrap;align-items:center;gap:8px 12px}' +
      '.rb-yt span{flex:1 1 200px;font-size:13.5px;color:var(--ink-2,#59616c)}' +
      '.rb-foot{margin:12px 0 0;font-size:12px;color:var(--ink-3,#8b929c);line-height:1.7}' +
      '@media(max-width:600px){.rb textarea,.rb-url input{font-size:16px}}';   // iPhoneで入力時に画面が拡大しないように
    document.head.appendChild(s);
  }

  function shareText(o) {
    var idea = String(o.idea || '').replace(/\s+/g, ' ').trim();
    if (idea.length > 40) idea = idea.slice(0, 40) + '…';
    var page = SITE + (o.yt ? '/douga/' : '/request/');
    var head = o.yt
      ? 'シミュラボのYouTubeに「' + idea + '」をリクエストしました！'
      : 'シミュラボに「' + idea + '」をリクエストしました！';
    var tail = o.yt
      ? 'みんなの「もしも」が3Dのシミュレーション動画になります。'
      : 'みんなのリクエストからシミュレーターが生まれるサイトです。';
    return head + '\n' + tail + '\n' + TAG + '\n' + page;
  }

  function mount(root, o) {
    if (!root || !o || !o.id) return;
    css();
    root.innerHTML = '';
    var box = el('div', 'rb');
    box.appendChild(el('h3', null, '🚀 シェアしてくれた方のリクエストを、優先して作ります'));
    box.appendChild(el('p', null, 'シェアして、その投稿のURLを下にはって送ってください。URLのあるリクエストから先に作ります。'));

    var ol = el('ol', 'rb-steps');

    // 1) シェアする
    var li1 = el('li'); li1.appendChild(el('b', null, 'シェアする'));
    var ta = el('textarea'); ta.value = shareText(o); ta.setAttribute('aria-label', 'シェアする文（自由に変えられます）');
    li1.appendChild(ta);
    var row = el('div', 'rb-row');
    var bx = el('a', 'rb-btn x', '𝕏 でシェア'); bx.href = '#'; bx.target = '_blank'; bx.rel = 'noopener';
    bx.addEventListener('click', function () { bx.href = 'https://twitter.com/intent/tweet?text=' + encodeURIComponent(ta.value); ev('share_x'); });
    var bc = el('button', 'rb-btn', '文をコピー'); bc.type = 'button';
    bc.addEventListener('click', function () {
      var done = function () { bc.textContent = 'コピーしました'; setTimeout(function () { bc.textContent = '文をコピー'; }, 1800); ev('copy'); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(ta.value).then(done, function () { ta.select(); document.execCommand('copy'); done(); });
      else { ta.select(); try { document.execCommand('copy'); } catch (e) {} done(); }
    });
    row.appendChild(bx); row.appendChild(bc);
    li1.appendChild(row);
    ol.appendChild(li1);

    // 2) 投稿のURLを送る
    var li2 = el('li'); li2.appendChild(el('b', null, 'シェアした投稿のURLを送る（任意）'));
    var ur = el('div', 'rb-url');
    var inp = el('input'); inp.type = 'url'; inp.placeholder = '例：https://x.com/…/status/…'; inp.maxLength = 300; inp.setAttribute('aria-label', 'シェアした投稿のURL');
    var bs = el('button', 'rb-btn go', 'URLを送る'); bs.type = 'button';
    ur.appendChild(inp); ur.appendChild(bs);
    var msg = el('div', 'rb-msg'); msg.setAttribute('role', 'status');
    li2.appendChild(ur); li2.appendChild(msg);
    ol.appendChild(li2);
    box.appendChild(ol);

    function sentUI() { inp.disabled = true; bs.disabled = true; bs.textContent = '送信済み'; msg.className = 'rb-msg ok'; msg.textContent = '✅ ありがとうございます。このリクエストを優先の列に入れました。'; }
    if (lget(SENT, []).indexOf(o.id) >= 0) sentUI();
    var busy = false;
    bs.addEventListener('click', function () {
      if (busy) return;
      var u = inp.value.trim();
      if (!/^https:\/\/[^\s]{8,300}$/.test(u)) { msg.className = 'rb-msg ng'; msg.textContent = '⚠️ https:// から始まる投稿のURLを入れてください。'; inp.focus(); return; }
      if (!window.ReqAPI) { msg.className = 'rb-msg ng'; msg.textContent = '⚠️ うまく送れませんでした。少し時間をおいてお試しください。'; return; }
      busy = true; bs.disabled = true; bs.textContent = '送信中…'; msg.textContent = '';
      var idea = String(o.idea || '').replace(/\s+/g, ' ').slice(0, 60);
      ReqAPI.submit({ idea: '【シェア報告】受付番号 ' + o.id + '／' + idea, genre: 'シェア報告', why: u, nick: '', email: '', website: '' })
        .then(function (j) {
          if (!j || !j.ok) throw new Error((j && j.error) || 'failed');
          var a = lget(SENT, []); a.push(o.id); lset(SENT, a.slice(-30));
          sentUI(); ev('url_sent');
        })
        .catch(function (er) {
          msg.className = 'rb-msg ng';
          msg.textContent = '⚠️ うまく送れませんでした。少し時間をおいてもう一度お試しください。' + (String(er.message) === 'busy' ? '（ただいま混み合っています）' : '');
          bs.disabled = false; bs.textContent = 'URLを送る';
        })
        .then(function () { busy = false; });
    });

    // YouTube は案内だけ（優先の条件にはしない）
    var yt = el('div', 'rb-yt');
    yt.appendChild(el('span', null, '▶ Webではできない大きな実験は、YouTubeで動画にしています。'));
    var by = el('a', 'rb-btn', '🔔 チャンネルを見る'); by.href = YT_URL; by.target = '_blank'; by.rel = 'noopener';
    by.addEventListener('click', function () { ev('youtube'); });
    yt.appendChild(by);
    box.appendChild(yt);

    box.appendChild(el('p', 'rb-foot',
      'シェアをしなくても、リクエストは今までどおり受け付けています（学校のパソコンなどでシェアできないときは、そのままで大丈夫です）。' +
      'シェアは1つのリクエストにつき1回で十分です。文は自由に変えてかまいません。' +
      'リクエスト企画への参加だと分かるように、文に「' + TAG + '」を入れています。'));
    root.appendChild(box);
  }

  window.ReqBoost = { mount: mount, text: shareText };
})();
