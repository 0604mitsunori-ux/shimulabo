/* シミュラボ 言語トグル＋自動検出バナー（自動リダイレクトはしない＝SEO/UX配慮）
   英語版が存在するページ(EN_SIMS)とトップだけ JA⇄EN を出す。
   英語版を増やしたら EN_SIMS に id を足すだけ。 */
(function () {
  // 英語版(/en/sims/<id>/)が存在するシミュID
  var EN_SIMS = [
    'input-jitan', 'gijiroku-jitan', 'mail-jitan', 'blog-shippitsu', 'moji-okoshi',
    'shorui-jitan', 'chat-jitan', 'memo-jitan', 'shogai-typing', 'kenshouen'
  ];

  var path = location.pathname;
  var isEN = path.indexOf('/en/') !== -1;
  function simIdOf(p) { var m = p.match(/\/sims\/([^\/]+)\//); return m ? m[1] : null; }
  var id = simIdOf(path);

  // 切替先URL（絶対パス）。無い場合は null。
  var href = null, label = '';
  if (isEN) {
    label = '日本語';
    href = id ? ('/sims/' + id + '/') : '/';
  } else {
    label = 'English';
    if (id) { if (EN_SIMS.indexOf(id) !== -1) href = '/en/sims/' + id + '/'; }
    else { href = '/en/'; } // 日本語トップ → 英語トップ
  }

  function insertToggle() {
    if (!href) return;
    var inner = document.querySelector('.site-header .inner');
    if (!inner || inner.querySelector('.lang-switch')) return;
    var a = document.createElement('a');
    a.className = 'lang-switch';
    a.href = href;
    a.textContent = '🌐 ' + label;
    a.setAttribute('rel', 'alternate');
    var back = inner.querySelector('.back');
    if (back) inner.insertBefore(a, back); else inner.appendChild(a);
  }

  // 英語ブラウザで日本語ページを見ている場合だけ、控えめな誘導バナー（自動遷移はしない）
  function maybeBanner() {
    if (isEN || !href) return;
    var lang = (navigator.language || navigator.userLanguage || '').toLowerCase();
    if (lang.indexOf('en') !== 0) return;
    try { if (localStorage.getItem('sl_lang_dismiss') === '1') return; } catch (e) {}
    var b = document.createElement('div');
    b.className = 'lang-banner';
    b.innerHTML = '<span>This page is also available in English.</span>' +
      '<a href="' + href + '">View in English →</a>' +
      '<button type="button" aria-label="close">✕</button>';
    document.body.appendChild(b);
    b.querySelector('button').addEventListener('click', function () {
      b.remove();
      try { localStorage.setItem('sl_lang_dismiss', '1'); } catch (e) {}
    });
  }

  function init() { insertToggle(); maybeBanner(); }
  if (document.readyState !== 'loading') init();
  else document.addEventListener('DOMContentLoaded', init);
})();
