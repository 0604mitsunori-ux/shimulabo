/* =========================================================
   シミュラボ 結果演出（result-fx）
   - 各シミュの結果欄を監視し、「富士山○個分」などの比較スタッツを
     検出して対応する絵文字をポップ表示。大きな数字をバウンスさせ、
     楽しい比較が出たときは軽い紙吹雪＋絵文字が舞う。
   - 既存の各 index.html に <script src=".../result-fx.js"> を読み込むだけ。
     各シミュの calc を書き換える必要はなし（#calcBtn のクリックを監視）。
   ========================================================= */
(function () {
  // ラベル/値に含まれるキーワード → 絵文字（上から順に最初の一致を採用）
  var MAP = [
    [/富士山/, '🗻'], [/エベレスト/, '⛰️'], [/東京ドーム|ドーム/, '🏟️'],
    [/地球|周/, '🌍'], [/月まで|月面|\b月\b/, '🌙'],
    [/映画/, '🎬'], [/絵本/, '📖'], [/本棚|蔵書/, '📚'],
    [/ペットボトル/, '🍶'], [/コップ/, '🥤'], [/ジョッキ|ビール/, '🍺'], [/缶/, '🥫'],
    [/袋/, '🛍️'], [/箱|ケース/, '📦'],
    [/ゾウ|象/, '🐘'], [/相撲|力士/, '🏋️'], [/プール/, '🏊'], [/お?風呂/, '🛁'],
    [/教室/, '🏫'], [/コーヒー/, '☕'], [/茶碗|ごはん|お米|白米/, '🍚'],
    [/タバコ|本数/, '🚬'], [/東京.?大阪|往復/, '🚗'], [/サッカー/, '⚽'],
    [/世界一周/, '✈️'], [/温泉/, '♨️']
  ];
  // 絵文字を出さない（深刻・ネガティブで賑やかし不要な）カテゴリ
  var QUIET_CATS = ['メンタル・自己分析'];

  function emojiFor(text) {
    for (var i = 0; i < MAP.length; i++) if (MAP[i][0].test(text)) return MAP[i][1];
    return null;
  }
  function firstNum(text) {
    var m = String(text).replace(/,/g, '').match(/-?\d+(\.\d+)?/);
    return m ? parseFloat(m[0]) : NaN;
  }
  function catLabel() {
    var c = document.querySelector('.sim-head .cat');
    return c ? c.textContent.trim() : '';
  }

  var lastSig = '';
  function enhance() {
    var panel = document.getElementById('resultPanel');
    if (!panel || panel.style.display === 'none') return;
    var result = panel.querySelector('.result') || panel;

    // スタッツ収集（ラベル.k と 値.v）
    var stats = [].slice.call(panel.querySelectorAll('.stat'));
    var matches = [];
    stats.forEach(function (st) {
      var k = (st.querySelector('.k') || {}).textContent || '';
      var v = (st.querySelector('.v') || {}).textContent || '';
      var emo = emojiFor(k) || emojiFor(v);
      if (!emo) return;
      var n = firstNum(v);
      if (!isFinite(n) || n < 1) return;
      var um = String(v).replace(/,/g, '').match(/-?\d+(?:\.\d+)?\s*(.*)$/);
      var unit = (um && um[1]) ? um[1].trim() : '個';
      var noun = k.replace(/[（(].*?[)）]/g, '').replace(/(を|に|は|で|の|あたり|にすると|なら)$/g, '').trim();
      matches.push({ label: noun, emoji: emo, count: Math.round(n), unit: unit });
    });

    var sig = matches.map(function (m) { return m.label + m.count + m.emoji; }).join('|');
    // 数字のバウンス（毎回）
    var big = panel.querySelector('.big');
    if (big) { big.classList.remove('fx-pop'); void big.offsetWidth; big.classList.add('fx-pop'); }

    if (sig === lastSig) return; // 同じ結果なら絵文字は作り直さない
    lastSig = sig;

    // 既存のFX要素を除去
    var old = panel.querySelector('.fx-wrap');
    if (old) old.parentNode.removeChild(old);
    if (!matches.length) return;

    // いちばん見栄えする1〜2件を採用（count上限でソート、極端に多いものは後ろ）
    matches.sort(function (a, b) {
      var sa = a.count > 40 ? a.count / 100 : a.count;
      var sb = b.count > 40 ? b.count / 100 : b.count;
      return sb - sa;
    });
    var pick = matches.slice(0, 2);

    var wrap = document.createElement('div');
    wrap.className = 'fx-wrap';
    var CAP = 24;
    pick.forEach(function (m) {
      var row = document.createElement('div');
      row.className = 'fx-icons';
      var lab = document.createElement('div');
      lab.className = 'fx-lab';
      lab.textContent = m.label + ' ' + m.count.toLocaleString('ja-JP') + (m.unit || '個');
      row.appendChild(lab);
      var show = Math.min(m.count, CAP);
      for (var i = 0; i < show; i++) {
        var s = document.createElement('span');
        s.className = 'fx-icon';
        s.textContent = m.emoji;
        s.style.animationDelay = (i * 45) + 'ms';
        row.appendChild(s);
      }
      if (m.count > CAP) {
        var more = document.createElement('span');
        more.className = 'fx-more';
        more.textContent = '…×' + m.count.toLocaleString('ja-JP');
        row.appendChild(more);
      }
      wrap.appendChild(row);
    });

    // statline の直後（無ければ result の末尾近く）に差し込む
    var sl = panel.querySelector('.statline');
    if (sl && sl.parentNode) sl.parentNode.insertBefore(wrap, sl.nextSibling);
    else result.insertBefore(wrap, result.firstChild ? result.firstChild.nextSibling : null);

    // お祝い演出（楽しい比較が出た & 深刻カテゴリでない時だけ）
    if (QUIET_CATS.indexOf(catLabel()) === -1) {
      celebrate(pick[0].emoji);
    }
  }

  // ===== 紙吹雪＋絵文字が舞う =====
  function celebrate(emoji) {
    var cv = document.createElement('canvas');
    cv.style.cssText = 'position:fixed;inset:0;width:100%;height:100%;pointer-events:none;z-index:9999';
    cv.width = innerWidth; cv.height = innerHeight;
    document.body.appendChild(cv);
    var x = cv.getContext('2d');
    var cols = ['#f43f5e', '#0fb5c4', '#6366f1', '#f59e0b', '#8b5cf6', '#22c55e'];
    var P = [], cx = innerWidth / 2, cy = innerHeight * 0.32, t0 = performance.now();
    for (var i = 0; i < 90; i++) {
      var a = Math.random() * Math.PI * 2, sp = 4 + Math.random() * 9;
      P.push({ x: cx, y: cy, vx: Math.cos(a) * sp, vy: Math.sin(a) * sp - 3, c: cols[i % cols.length], r: 4 + Math.random() * 4, rot: Math.random() * 6, em: (i % 6 === 0) });
    }
    function frame(now) {
      var el = now - t0; x.clearRect(0, 0, cv.width, cv.height);
      P.forEach(function (p) {
        p.vy += 0.22; p.vx *= 0.99; p.x += p.vx; p.y += p.vy; p.rot += 0.2;
        var al = Math.max(0, 1 - el / 1300);
        x.globalAlpha = al;
        if (p.em) { x.font = '22px serif'; x.fillText(emoji, p.x, p.y); }
        else { x.save(); x.translate(p.x, p.y); x.rotate(p.rot); x.fillStyle = p.c; x.fillRect(-p.r, -p.r / 2, p.r * 2, p.r); x.restore(); }
      });
      x.globalAlpha = 1;
      if (el < 1300) requestAnimationFrame(frame); else cv.remove();
    }
    requestAnimationFrame(frame);
  }

  function hook() {
    var btn = document.getElementById('calcBtn');
    if (btn) btn.addEventListener('click', function () { setTimeout(enhance, 40); });
    // 念のため：結果パネルの表示切替も監視（calcBtn以外で出すシミュ対策）
    var panel = document.getElementById('resultPanel');
    if (panel && window.MutationObserver) {
      new MutationObserver(function () { setTimeout(enhance, 40); })
        .observe(panel, { attributes: true, attributeFilter: ['style'] });
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', hook);
  else hook();
})();
