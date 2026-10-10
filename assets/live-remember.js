/* ライブ系：選んだ都道府県・地点をこのブラウザに記憶し、次に開いたときはその地域ですぐ表示する（2026-10）
   都道府県は全ページ共通（夕焼けで東京を選べば、星空・傘・洗濯も東京で開く）。地点（#spot）はページごと。
   保存先は localStorage のみ（サーバーには送らない）。 */
(function () {
  var NO_AUTO = ['umareta-hi-tenki'];          // 地域以外の入力（誕生日など）が主役のページは、自動では計算しない
  var path = location.pathname.replace(/index\.html$/, '');
  var slug = (path.match(/\/sims\/([^/]+)\//) || [])[1] || '';
  var base = function (t) { return (t || '').replace(/[（(].*$/, '').trim(); };
  function store(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function load(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  var sel = document.getElementById('pref'), key, val, idx = -1;
  if (sel) {
    key = 'shimulabo:pref';
    val = load(key);
    sel.addEventListener('change', function () { store(key, base(sel.options[sel.selectedIndex].text)); });
    if (val) idx = Array.prototype.findIndex.call(sel.options, function (o) { return base(o.text) === val; });
  } else {
    sel = document.getElementById('spot'); if (!sel) return;
    key = 'shimulabo:spot:' + slug;
    val = load(key);
    sel.addEventListener('change', function () { store(key, sel.value); });
    if (val) idx = Array.prototype.findIndex.call(sel.options, function (o) { return o.value === val; });
  }
  var btn = document.getElementById('calcBtn');
  if (btn) btn.addEventListener('click', function () { sel.dispatchEvent(new Event('change')); });
  if (idx < 0) return;
  sel.selectedIndex = idx;
  var note = document.createElement('p');
  note.className = 'hint';
  note.style.marginTop = '6px';
  note.textContent = '前回選んだ「' + base(sel.options[idx].text) + '」で表示しています（このブラウザに保存）';
  sel.parentNode.appendChild(note);
  if (NO_AUTO.indexOf(slug) >= 0) return;
  if (btn) {
    // 開いた直下で結果までスクロールしないよう、自動表示のあいだだけスクロールを止める（操作したら即解除）
    var orig = Element.prototype.scrollIntoView, restored = false;
    var restore = function () { if (!restored) { restored = true; Element.prototype.scrollIntoView = orig; } };
    Element.prototype.scrollIntoView = function () {};
    ['pointerdown', 'keydown', 'touchstart'].forEach(function (ev) { window.addEventListener(ev, restore, { once: true, capture: true }); });
    setTimeout(restore, 6000);
    btn.click();
  } else {
    sel.dispatchEvent(new Event('change'));
  }
})();
