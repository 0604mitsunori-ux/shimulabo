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
    [/富士山/, '🗻'], [/エベレスト/, '⛰️'], [/東京タワー/, '🗼'], [/スカイツリー/, '🗼'],
    [/東京ドーム|ドーム/, '🏟️'], [/地球|周/, '🌍'], [/月まで|月面|\b月\b/, '🌙'],
    [/新幹線/, '🚄'], [/ジャンボ|飛行機|ジェット/, '✈️'], [/バス/, '🚌'], [/自転車/, '🚲'],
    [/札束|お札|万円札/, '💴'], [/小判|金貨/, '🪙'], [/ドラム缶/, '🛢️'],
    [/映画/, '🎬'], [/絵本/, '📖'], [/本棚|蔵書|書籍/, '📚'], [/新聞/, '📰'],
    [/ペットボトル/, '🍶'], [/コップ/, '🥤'], [/ジョッキ|ビール/, '🍺'], [/ワイン/, '🍷'], [/缶/, '🥫'],
    [/袋/, '🛍️'], [/箱|ケース|段ボール/, '📦'], [/風船/, '🎈'], [/バケツ/, '🪣'], [/ドラム/, '🥁'],
    [/ゾウ|象/, '🐘'], [/相撲|力士/, '🏋️'], [/犬|わんこ/, '🐕'], [/猫|にゃんこ/, '🐈'],
    [/プール/, '🏊'], [/お?風呂|湯船/, '🛁'], [/教室/, '🏫'], [/家|マンション|一軒家/, '🏠'],
    [/コーヒー/, '☕'], [/茶碗|ごはん|お米|白米/, '🍚'], [/ハンバーガー/, '🍔'], [/ケーキ/, '🍰'],
    [/寿司|すし/, '🍣'], [/ピザ/, '🍕'], [/ドーナツ/, '🍩'], [/たまご|卵/, '🥚'],
    [/りんご|リンゴ/, '🍎'], [/バナナ/, '🍌'], [/牛乳|ミルク/, '🥛'], [/角砂糖|砂糖/, '🧊'],
    [/タバコ|本数/, '🚬'], [/東京.?大阪|往復/, '🚗'], [/サッカー|コート/, '⚽'],
    [/世界一周/, '✈️'], [/温泉/, '♨️'], [/プレゼント/, '🎁'], [/トロフィー|優勝/, '🏆']
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
  function simId() {
    var m = location.pathname.match(/\/sims\/([^\/]+)/);
    return m ? m[1] : '';
  }
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  // 結果から演出の強さ(0〜1)を推定：％→そのまま／比較個数→log／大きな数→log
  function computeIntensity(panel, matches) {
    var big = panel.querySelector('.big');
    var bigWrap = big && big.parentNode ? big.parentNode.textContent : (big ? big.textContent : '');
    var pm = bigWrap.replace(/,/g, '').match(/(\d+(?:\.\d+)?)\s*[%％点]/);
    if (pm) return clamp(parseFloat(pm[1]) / 100, 0.1, 1);
    if (matches.length) {
      var mx = matches.reduce(function (a, m) { return Math.max(a, m.count); }, 0);
      return clamp(Math.log10(mx + 1) / 2, 0.3, 1); // 10個→0.5, 100個→1.0
    }
    var nb = firstNum(big ? big.textContent : '');
    if (isFinite(nb) && nb > 0) return clamp(Math.log10(nb + 1) / 8, 0.3, 1); // 1万→0.5, 1億→1.0
    return 0.55;
  }

  // ===== 名物シミュの専用アニメ =====
  // 貯金・複利・積立など「育つ」系 → ブタ貯金箱がふくらむ
  var PIGGY = ['tsumitate-fukuri', 'fire', 'chiritsumo', 'haitou-shisan', 'nisa', 'tabi-tsumitate',
    'kagu-tsumitate', 'shaken-tsumitate', 'gakushi', 'kuriage', 'point-katsu'];
  // 宝くじ・大金系 → コインが降る
  var COIN = ['takarakuji', 'oshi-nenkan', 'gacha', 'hakooshi'];
  // 恋愛・相性系 → ハートが鼓動
  var HEART = ['kokuhaku', 'ryomoi', 'aishou-seiza', 'birthday-aishou', 'konkatsu-type', 'konkatsu-match',
    'moteki', 'unmei', 'ketsueki-aishou', 'aisho-name', 'same-class', 'kinenbi', 'enkyori'];
  // 時間系 → 砂時計がくるくる
  var CLOCK = ['machi-jikan', 'jinsei-calendar', 'seimei-suimin', 'sumaho-shogai', 'kaji-jikan',
    'oshi-jikan', 'kodomo-jikan', 'pet-jikan', 'nidone', 'kyuryobi'];
  // ダイエット・燃焼系 → 炎がメラメラ
  var FLAME = ['taiju', 'diet-mokuhyou', 'taishibo', 'taishibo-otoshi', 'shomou-undou',
    'karori-undou', 'hosu-karori', 'kaidan', 'sake-karori', 'kiso-taisha'];

  function insertSpecial(panel, node) {
    var result = panel.querySelector('.result') || panel;
    var sl = panel.querySelector('.statline') || panel.querySelector('.big');
    if (sl && sl.parentNode) sl.parentNode.insertBefore(node, sl.nextSibling);
    else result.insertBefore(node, result.firstChild);
  }
  function piggyNode(power) {
    power = power || 0.5;
    var d = document.createElement('div');
    d.className = 'fx-special';
    var sz = Math.round(48 + power * 46); // 48〜94px
    d.innerHTML = '<div class="fx-piggy" style="font-size:' + sz + 'px">🐷</div>' +
      '<div class="fx-cap">' + (power > 0.8 ? 'どんどん育つ大貯金！' : 'コツコツ育つ貯金箱') + '</div>';
    var coins = Math.round(3 + power * 5); // 3〜8枚
    for (var i = 0; i < coins; i++) {
      var c = document.createElement('span');
      c.className = 'fx-coin'; c.textContent = i % 3 === 2 ? '💴' : '🪙';
      c.style.left = (30 + (i / coins) * 44) + '%'; c.style.animationDelay = (i * 130) + 'ms';
      d.appendChild(c);
    }
    return d;
  }
  function fujiNode(power) {
    power = power || 0.5;
    var d = document.createElement('div');
    d.className = 'fx-special';
    var scale = (0.7 + power * 0.7).toFixed(2); // 0.7〜1.4倍
    d.innerHTML =
      '<div style="transform:scale(' + scale + ');transform-origin:bottom center;display:inline-block">' +
      '<svg class="fx-rise" width="220" height="140" viewBox="0 0 220 140" xmlns="http://www.w3.org/2000/svg">' +
      '<defs><linearGradient id="fg" x1="0" y1="0" x2="0" y2="1">' +
      '<stop offset="0" stop-color="#6f93c7"/><stop offset="1" stop-color="#3f5d8f"/></linearGradient></defs>' +
      '<polygon points="110,12 205,128 15,128" fill="url(#fg)"/>' +
      '<polygon points="110,12 138,46 126,40 116,50 110,38 104,50 94,42 82,46" fill="#fff"/>' +
      '<ellipse cx="110" cy="130" rx="100" ry="9" fill="rgba(255,255,255,.12)"/></svg></div>' +
      '<div class="fx-cap">' + (power > 0.8 ? '天までそびえる高さ！' : 'そびえ立つ高さ！') + '</div>';
    return d;
  }
  function coinNode() {
    var d = document.createElement('div');
    d.className = 'fx-special';
    d.innerHTML = '<div class="fx-piggy" style="animation-delay:.05s">💰</div><div class="fx-cap">ざっくざく！</div>';
    for (var i = 0; i < 4; i++) {
      var c = document.createElement('span');
      c.className = 'fx-coin'; c.textContent = i % 2 ? '💴' : '🪙';
      c.style.left = (36 + i * 12) + '%'; c.style.animationDelay = (i * 150) + 'ms';
      d.appendChild(c);
    }
    return d;
  }
  function heartNode(power) {
    power = power || 0.5;
    var d = document.createElement('div');
    d.className = 'fx-special';
    var sz = Math.round(50 + power * 40), spd = (1.15 - power * 0.55).toFixed(2); // 高%ほど大きく速い鼓動
    d.innerHTML = '<div class="fx-heart" style="font-size:' + sz + 'px;animation-duration:' + spd + 's">💗</div>' +
      '<div class="fx-cap">' + (power > 0.8 ? '相性バツグン…！💖' : 'ドキドキ…！') + '</div>';
    for (var i = 0; i < 5; i++) {
      var h = document.createElement('span');
      h.className = 'fx-coin'; h.textContent = ['💕', '💖', '💞', '💘', '❤️'][i];
      h.style.left = (28 + i * 11) + '%'; h.style.top = 'auto'; h.style.bottom = '-6px';
      h.style.animation = 'fxheartup 1.3s ease-out forwards'; h.style.animationDelay = (i * 130) + 'ms';
      d.appendChild(h);
    }
    return d;
  }
  function clockNode() {
    var d = document.createElement('div');
    d.className = 'fx-special';
    d.innerHTML = '<div class="fx-clock">⏳</div><div class="fx-cap">時は金なり</div>';
    return d;
  }
  function flameNode() {
    var d = document.createElement('div');
    d.className = 'fx-special';
    d.innerHTML = '<div class="fx-flame"><span>🔥</span><span>🔥</span><span>🔥</span></div><div class="fx-cap">メラメラ燃焼！</div>';
    return d;
  }
  // 専用アニメを実行（あれば {emoji} を返す）
  function runSpecial(panel, power) {
    var id = simId();
    var node = null, emoji = null;
    if (PIGGY.indexOf(id) >= 0) { node = piggyNode(power); emoji = '🪙'; }
    else if (HEART.indexOf(id) >= 0) { node = heartNode(power); emoji = '💗'; }
    else if (FLAME.indexOf(id) >= 0) { node = flameNode(); emoji = '🔥'; }
    else if (CLOCK.indexOf(id) >= 0) { node = clockNode(); emoji = '⏳'; }
    else if (COIN.indexOf(id) >= 0) { node = coinNode(); emoji = '💰'; }
    else if (id === 'scroll-distance' || hasKeyword(panel, /富士山|エベレスト/)) { node = fujiNode(power); emoji = '🗻'; }
    if (!node) return null;
    insertSpecial(panel, node);
    return { emoji: emoji };
  }
  function hasKeyword(panel, re) {
    var t = '';
    panel.querySelectorAll('.k,.v,.label,.sub').forEach(function (e) { t += e.textContent + ' '; });
    return re.test(t);
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

    // 数字のバウンス（毎回）
    var big = panel.querySelector('.big');
    var bigText = big ? big.textContent : '';
    if (big) { big.classList.remove('fx-pop'); void big.offsetWidth; big.classList.add('fx-pop'); }

    var sig = simId() + '|' + bigText + '|' + matches.map(function (m) { return m.label + m.count + m.emoji; }).join('|');
    if (sig === lastSig) return; // 同じ結果なら作り直さない
    lastSig = sig;

    // 既存のFX要素を除去
    var oldw = panel.querySelector('.fx-wrap'); if (oldw) oldw.remove();
    var olds = panel.querySelector('.fx-special'); if (olds) olds.remove();

    // 結果の大きさ＝演出の強さ
    var power = computeIntensity(panel, matches);
    // 名物シミュの専用アニメ
    var special = runSpecial(panel, power);

    if (!matches.length) {
      partyFor(panel, special ? special.emoji : null, power);
      return;
    }

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

    // テーマ演出（カテゴリ別・結果が大きいほど派手／メンタル等は静か）
    partyFor(panel, pick[0].emoji, power);
  }

  // ===== 汎用パーティクルエンジン（紙吹雪/絵文字 rain・up・burst） =====
  function fxParticles(opts) {
    opts = opts || {};
    var emojis = opts.emojis || [], n = opts.count || 60, mode = opts.mode || 'burst', dur = opts.duration || 1500;
    var cols = opts.colors || ['#f43f5e', '#0fb5c4', '#6366f1', '#f59e0b', '#8b5cf6', '#22c55e'];
    var cv = document.createElement('canvas');
    cv.style.cssText = 'position:fixed;inset:0;width:100%;height:100%;pointer-events:none;z-index:9999';
    cv.width = innerWidth; cv.height = innerHeight;
    document.body.appendChild(cv);
    var x = cv.getContext('2d');
    var P = [], cx = innerWidth / 2, cy = innerHeight * 0.32, t0 = performance.now();
    for (var i = 0; i < n; i++) {
      var p = { rot: Math.random() * 6, vr: (Math.random() - 0.5) * 0.34, c: cols[i % cols.length], r: 4 + Math.random() * 4, sz: 18 + Math.random() * 14 };
      var pw = opts.power != null ? opts.power : 0.55, boost = 0.7 + pw * 0.7;
      if (mode === 'rain') { p.x = Math.random() * innerWidth; p.y = -20 - Math.random() * innerHeight * 0.4; p.vx = (Math.random() - 0.5) * 1.6; p.vy = (3 + Math.random() * 4.5) * (0.85 + pw * 0.5); p.g = 0.10; }
      else if (mode === 'up') { p.x = cx + (Math.random() - 0.5) * innerWidth * 0.6; p.y = innerHeight * 0.62 + Math.random() * 90; p.vx = (Math.random() - 0.5) * 1.4; p.vy = -(2.2 + Math.random() * 3.4) * boost; p.g = -0.015; }
      else { var a = Math.random() * 6.283, sp = (4 + Math.random() * 9.5) * boost; p.x = cx; p.y = cy; p.vx = Math.cos(a) * sp; p.vy = Math.sin(a) * sp - 3.5; p.g = 0.22; }
      p.em = emojis.length ? ((mode === 'burst') ? (i % 2 === 0 ? emojis[(i / 2 | 0) % emojis.length] : null) : emojis[i % emojis.length]) : null;
      P.push(p);
    }
    function frame(now) {
      var el = now - t0; x.clearRect(0, 0, cv.width, cv.height);
      var al = Math.max(0, 1 - el / dur);
      P.forEach(function (p) {
        p.vy += p.g; p.vx *= 0.995; p.x += p.vx; p.y += p.vy; p.rot += p.vr;
        x.globalAlpha = al;
        if (p.em) { x.font = p.sz + 'px serif'; x.textAlign = 'center'; x.fillText(p.em, p.x, p.y); }
        else { x.save(); x.translate(p.x, p.y); x.rotate(p.rot); x.fillStyle = p.c; x.fillRect(-p.r, -p.r / 2, p.r * 2, p.r); x.restore(); }
      });
      x.globalAlpha = 1;
      if (el < dur) requestAnimationFrame(frame); else cv.remove();
    }
    requestAnimationFrame(frame);
  }

  // カテゴリ別のテーマ演出
  var CATFX = {
    '恋愛・婚活': { emojis: ['💕', '💗', '💖', '💞'], mode: 'up', count: 42 },
    'ペット': { emojis: ['🐾', '🐶', '🐱', '🦴'], mode: 'up', count: 36 },
    'お金・時間': { emojis: ['🪙', '💴', '💰'], mode: 'rain', count: 48 },
    'マネー・保険・不動産': { emojis: ['🪙', '💴', '💰'], mode: 'rain', count: 48 },
    '店舗・ビジネス': { emojis: ['💰', '📈', '🪙'], mode: 'rain', count: 42 },
    '仕事・働き方': { emojis: ['💼', '🪙', '✨'], mode: 'rain', count: 38 },
    '健康・カラダ': { emojis: ['🔥', '💪', '✨'], mode: 'burst', count: 48 },
    'スポーツ・運動': { emojis: ['🔥', '💪', '⚡', '🏅'], mode: 'burst', count: 50 },
    '占い・診断': { emojis: ['✨', '⭐', '🔮', '🌟'], mode: 'burst', count: 52 },
    '子ども・育児': { emojis: ['🎈', '🧸', '⭐', '🍼'], mode: 'up', count: 40 },
    'グルメ・食': { emojis: ['😋', '🍴', '✨', '🍚'], mode: 'burst', count: 42 },
    '旅行・おでかけ': { emojis: ['✈️', '🌍', '🧳', '⭐'], mode: 'burst', count: 44 },
    'クルマ・乗り物': { emojis: ['🚗', '💨', '✨'], mode: 'burst', count: 38 },
    '住まい・暮らし': { emojis: ['🏠', '✨', '🔑'], mode: 'burst', count: 38 },
    '美容・ファッション': { emojis: ['💄', '✨', '💖', '👜'], mode: 'up', count: 42 },
    '推し活・エンタメ': { emojis: ['🎉', '🌟', '💜', '🎤'], mode: 'burst', count: 56 },
    'マーケティング': { emojis: ['📈', '✨', '🚀'], mode: 'burst', count: 42 },
    '学生・勉強': { emojis: ['✏️', '📚', '✨', '💯'], mode: 'burst', count: 42 },
    '人生・自分ごと': { emojis: ['✨', '⏳', '🌈'], mode: 'burst', count: 42 },
    '教員・先生': { emojis: ['✏️', '📋', '💯', '✨', '🌸'], mode: 'burst', count: 44 }
  };
  function partyFor(panel, fallbackEmoji, power) {
    var cat = catLabel();
    if (QUIET_CATS.indexOf(cat) !== -1) return; // メンタル等は静かに
    power = (power == null ? 0.55 : power);
    var base = CATFX[cat] || { emojis: [fallbackEmoji || '🎉', '✨'], mode: 'burst', count: 44 };
    fxParticles({
      emojis: base.emojis, mode: base.mode, colors: base.colors,
      count: Math.min(150, Math.round(base.count * (0.45 + power))), // 結果が大きいほど増量
      power: power, duration: 1250 + Math.round(power * 950)
    });
  }

  function hook() {
    var btn = document.getElementById('calcBtn');
    if (btn) btn.addEventListener('click', function () { setTimeout(enhance, 800); });
    // 念のため：結果パネルの表示切替も監視（calcBtn以外で出すシミュ対策）
    var panel = document.getElementById('resultPanel');
    if (panel && window.MutationObserver) {
      new MutationObserver(function () { setTimeout(enhance, 800); })
        .observe(panel, { attributes: true, attributeFilter: ['style'] });
    }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', hook);
  else hook();
})();
