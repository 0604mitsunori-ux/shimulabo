/* シミュラボ トップページの動き・その2（2026-11-17）…派手めの演出
   top-fx.js（ヒーローの舞台・流れる帯・スクロール演出）の上に重ねる。1つ失敗しても他は動く。
   「動きを減らす」設定の端末では、このファイルの演出は全部やらない。
   見出しの文字は書き換えない（1文字ずつ span に分けるだけ。数字は ::after で重ねる）＝検索エンジンが読む文は変わらない。 */
(function () {
  'use strict';
  var RM = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (RM) return;
  var FINE = window.matchMedia && matchMedia('(hover: hover) and (pointer: fine)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)); };
  var COL = ['#c4442b', '#2c6b86', '#a97a24', '#14181d', '#6a5c82'];
  var errs = [];
  function run(name, fn) { try { fn(); } catch (e) { errs.push(name + ': ' + (e && e.message)); } }
  window.__fxMoreErr = errs;

  /* ===== A. 手前のキャンバス：クリックの火花・紙ふぶき ===== */
  var burst = function () {}, confettiAt = function () {};
  run('front', function () {
    var fc = document.createElement('canvas'); fc.className = 'fx-front'; fc.setAttribute('aria-hidden', 'true');
    document.body.appendChild(fc);
    var ctx = fc.getContext('2d'), W = 0, H = 0, D = 1, parts = [], raf = 0, last = 0;
    function size() { D = Math.min(window.devicePixelRatio || 1, 2); W = window.innerWidth; H = window.innerHeight; fc.width = Math.round(W * D); fc.height = Math.round(H * D); }
    size(); window.addEventListener('resize', size);
    burst = function (x, y, n, o) {
      o = o || {};
      for (var i = 0; i < n; i++) {
        var a = Math.random() * 6.283, sp = (o.speed || 220) * (0.35 + Math.random());
        parts.push({ x: x, y: y, vx: Math.cos(a) * sp, vy: Math.sin(a) * sp - (o.up || 0), g: o.g == null ? 520 : o.g, life: 0,
          max: (o.life || 0.8) * (0.6 + Math.random() * 0.6), c: COL[(Math.random() * COL.length) | 0],
          s: (o.size || 3) * (0.6 + Math.random()), r: Math.random() * 6.283, vr: (Math.random() - 0.5) * 14, sq: !!o.confetti });
      }
      if (parts.length > 900) parts.splice(0, parts.length - 900);
      if (!raf) { last = performance.now(); raf = requestAnimationFrame(tick); }
    };
    function tick(now) {
      var dt = Math.min(0.05, (now - last) / 1000); last = now;
      ctx.setTransform(D, 0, 0, D, 0, 0); ctx.clearRect(0, 0, W, H);
      for (var i = parts.length - 1; i >= 0; i--) {
        var p = parts[i]; p.life += dt;
        if (p.life >= p.max) { parts.splice(i, 1); continue; }
        p.vy += p.g * dt; p.vx *= (1 - 1.2 * dt); p.x += p.vx * dt; p.y += p.vy * dt; p.r += p.vr * dt;
        var k = 1 - p.life / p.max; ctx.globalAlpha = Math.min(1, k * 1.6); ctx.fillStyle = p.c;
        if (p.sq) { ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.r); ctx.fillRect(-p.s, -p.s * 0.5, p.s * 2, p.s * (0.4 + 0.6 * Math.abs(Math.cos(p.r * 1.3)))); ctx.restore(); }
        else { ctx.beginPath(); ctx.arc(p.x, p.y, p.s * k + 0.4, 0, 6.283); ctx.fill(); }
      }
      ctx.globalAlpha = 1;
      raf = parts.length ? requestAnimationFrame(tick) : 0;
    }
    confettiAt = function (el, n) {
      var r = el.getBoundingClientRect();
      burst(r.left + r.width / 2, r.top + r.height / 2, n || 70, { speed: 420, life: 1.5, size: 4, g: 620, up: 260, confetti: true });
    };
    document.addEventListener('pointerdown', function (e) {
      if (e.button) return;
      burst(e.clientX, e.clientY, 14, { speed: 190, life: 0.55, size: 2.6, g: 300 });
    }, { passive: true });
  });

  /* ===== B. 奥のキャンバス：ただよう数字と記号（スクロールでずれる） ===== */
  run('back', function () {
    var bc = document.createElement('canvas'); bc.className = 'fx-back'; bc.setAttribute('aria-hidden', 'true');
    document.body.insertBefore(bc, document.body.firstChild);
    var ctx = bc.getContext('2d'), d = 1, W = 0, H = 0, raf = 0, fr = 0;
    var SY = '0123456789+−×÷=√π∑∞%△○'.split(''), n = window.innerWidth < 700 ? 14 : 30, syms = [];
    function size() { d = 1; W = window.innerWidth; H = window.innerHeight; bc.width = Math.round(W * d); bc.height = Math.round(H * d); } // 飾りなので等倍で描く（軽くする）
    size(); window.addEventListener('resize', size);
    for (var i = 0; i < n; i++) {
      syms.push({ x: Math.random(), y: Math.random(), z: 0.3 + Math.random() * 0.7, ch: SY[(Math.random() * SY.length) | 0],
        r: (Math.random() - 0.5) * 0.8, vr: (Math.random() - 0.5) * 0.25, c: i % 7 === 0 ? 0 : (i % 3 === 0 ? 1 : 3), ph: Math.random() * 6.283 });
    }
    // 文字は最初に1回だけ小さな絵にしておき、毎コマはその絵を置くだけにする（文字を毎回描くより軽い）
    syms.forEach(function (s) {
      var fs = Math.round(20 + 44 * s.z), half = Math.ceil(fs * 0.75), sp = document.createElement('canvas');
      sp.width = sp.height = half * 2;
      var g = sp.getContext('2d'); g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillStyle = COL[s.c];
      g.font = '600 ' + fs + 'px "Hiragino Mincho ProN","Yu Mincho",serif'; g.fillText(s.ch, half, half);
      s.sp = sp; s.half = half;
    });
    function tick(now) {
      raf = 0; if (document.hidden) return;
      if ((fr++ & 1) === 1) { raf = requestAnimationFrame(tick); return; } // 1コマおきに描く（毎秒30コマで十分）
      var t = now / 1000, sy = window.scrollY || 0, span = H * 1.3, dim = W < 700 ? 0.6 : 1; // スマホは本文と重なりやすいのでうすく
      ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.clearRect(0, 0, W, H);
      for (var i = 0; i < syms.length; i++) {
        var s = syms[i];
        var y = (s.y * span - t * 8 * s.z - sy * 0.22 * s.z) % span; if (y < 0) y += span; y -= H * 0.15;
        var x = s.x * W + Math.sin(t * 0.3 + s.ph) * 18 * s.z;
        var a = s.r + t * s.vr, ca = Math.cos(a), sa = Math.sin(a);
        ctx.globalAlpha = (0.05 + 0.09 * s.z) * dim;
        ctx.setTransform(ca, sa, -sa, ca, x, y); ctx.drawImage(s.sp, -s.half, -s.half);
      }
      ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1;
      raf = requestAnimationFrame(tick);
    }
    raf = requestAnimationFrame(tick);
    document.addEventListener('visibilitychange', function () { if (!document.hidden && !raf) raf = requestAnimationFrame(tick); });
  });

  /* ===== C. 見出し：数字がぱらぱら変わってから文字になる ===== */
  run('scramble', function () {
    var h1 = $('.hero h1'); if (!h1) return;
    var tw = document.createTreeWalker(h1, NodeFilter.SHOW_TEXT, null), tn, tns = [], chs = [];
    while ((tn = tw.nextNode())) tns.push(tn);
    tns.forEach(function (node) {
      var s = node.nodeValue; if (!s.trim()) return;
      var f = document.createDocumentFragment();
      for (var i = 0; i < s.length; i++) {
        var c = s.charAt(i);
        if (/\s/.test(c)) { f.appendChild(document.createTextNode(c)); continue; }
        var sp = document.createElement('span'); sp.className = 'fx-ch'; sp.textContent = c;
        if (!/[「」、。]/.test(c)) { sp.classList.add('sc'); sp.setAttribute('data-d', '０'); chs.push(sp); }
        f.appendChild(sp);
      }
      node.parentNode.replaceChild(f, node);
    });
    var DG = '０１２３４５６７８９', st0 = performance.now() + 350, SD = 1300;
    var iv = setInterval(function () {
      var k = (performance.now() - st0) / SD, done = Math.floor(k * chs.length);
      for (var i = 0; i < chs.length; i++) {
        if (i < done) chs[i].classList.remove('sc'); else chs[i].setAttribute('data-d', DG.charAt((Math.random() * 10) | 0));
      }
      if (k >= 1) { clearInterval(iv); chs.forEach(function (c) { c.classList.remove('sc'); }); }
    }, 55);
  });

  /* ===== D. 大きな流れる文字の帯（カテゴリ一覧の前）＋スクロールの速さで帯が加速 ===== */
  run('band', function () {
    var chips = document.getElementById('groupChips'); if (!chips) return;
    var band = document.createElement('div'); band.className = 'fx-band'; band.setAttribute('aria-hidden', 'true');
    var tx = '数字にすると、面白い。<i>◆</i>なるほどを、触って確かめる。<i>◆</i>SIMULATE EVERYTHING<i>◆</i>';
    band.innerHTML = '<div class="fx-band-track"><span>' + tx + '</span><span>' + tx + '</span></div>';
    chips.parentNode.insertBefore(band, chips);
  });
  run('velocity', function () {
    var anims = [], lastY = window.scrollY || 0, vel = 0, raf = 0;
    function collect() {
      anims = $$('.fx-ticker .track, .fx-band-track').map(function (el) { return el.getAnimations ? el.getAnimations()[0] : null; }).filter(Boolean);
    }
    function setRate(r) { for (var i = 0; i < anims.length; i++) { try { anims[i].playbackRate = r; } catch (e) {} } }
    function tick() {
      raf = 0;
      var y = window.scrollY || 0, dv = Math.abs(y - lastY); lastY = y; vel += (dv - vel) * 0.25;
      if (vel > 0.3) { setRate(1 + Math.min(8, vel / 8)); raf = requestAnimationFrame(tick); } else { vel = 0; setRate(1); }
    }
    window.addEventListener('scroll', function () { if (!raf) { collect(); raf = requestAnimationFrame(tick); } }, { passive: true });
  });

  /* ===== E. カード：マウスに合わせて傾く＋光が動く ===== */
  run('tilt', function () {
    if (!FINE) return;
    var cur = null;
    document.addEventListener('pointermove', function (e) {
      var c = e.target && e.target.closest ? e.target.closest('.sim-card') : null;
      if (cur && cur !== c) { cur.style.transform = ''; cur.classList.remove('fx-tilt'); cur = null; }
      if (!c) return;
      cur = c;
      var r = c.getBoundingClientRect(), px = (e.clientX - r.left) / r.width, py = (e.clientY - r.top) / r.height;
      c.classList.add('fx-tilt');
      c.style.setProperty('--mx', (px * 100).toFixed(1) + '%'); c.style.setProperty('--my', (py * 100).toFixed(1) + '%');
      c.style.transform = 'perspective(700px) rotateX(' + ((0.5 - py) * 7).toFixed(2) + 'deg) rotateY(' + ((px - 0.5) * 9).toFixed(2) + 'deg) translateY(-3px)';
    }, { passive: true });
    document.addEventListener('pointerleave', function () { if (cur) { cur.style.transform = ''; cur.classList.remove('fx-tilt'); cur = null; } });
  });

  /* ===== F. ランキング：回数が0から数え上がる・カウンターで紙ふぶき ===== */
  run('rank', function () {
    var rl = document.getElementById('rankList'); if (!rl) return;
    function countRows() {
      $$('.rank-num b', rl).forEach(function (b, i) {
        if (b._fx) return;
        var goal = parseInt(b.textContent.replace(/[^\d]/g, ''), 10); if (!goal) return;
        b._fx = 1;
        var t0 = 0, dur = 650 + i * 90, fin = goal.toLocaleString('ja-JP');
        var step = function (now) {
          if (!t0) t0 = now;
          var k = Math.min(1, (now - t0) / dur), e = 1 - Math.pow(1 - k, 3);
          b.textContent = k < 1 ? Math.round(goal * e).toLocaleString('ja-JP') : fin;
          if (k < 1) requestAnimationFrame(step);
        };
        b.textContent = '0'; requestAnimationFrame(step);
        setTimeout(function () { b.textContent = fin; }, dur + 2500); // 画面が裏にあっても必ず正しい数にする
      });
    }
    new MutationObserver(countRows).observe(rl, { childList: true });
    countRows();
    var pc = document.getElementById('playCounter'), num = document.getElementById('pcTotal'), fired = false;
    if (pc && num && 'IntersectionObserver' in window) {
      new IntersectionObserver(function (es, io) {
        if (!es[0].isIntersecting || fired || pc.hidden) return;
        fired = true; io.disconnect();
        setTimeout(function () { confettiAt(num, 90); }, 1500);
      }, { threshold: 0.6 }).observe(pc);
    }
  });

  /* ===== G. 検索窓：例の言葉を1文字ずつ打つ ===== */
  run('search', function () {
    var si = document.getElementById('searchInput'); if (!si) return;
    var base = si.getAttribute('placeholder') || '', words = ['月の満ち欠け', '会議', '色覚', '歯車', 'カロリー', '税金', '占い'], wi = 0, ci = 0, del = false;
    var type = function () {
      if (document.activeElement === si || si.value) { si.setAttribute('placeholder', base); setTimeout(type, 1500); return; }
      var w = words[wi]; ci += del ? -1 : 1;
      si.setAttribute('placeholder', '「' + w.slice(0, ci) + '」で検索 ▍');
      var wait = del ? 45 : 120;
      if (!del && ci >= w.length) { del = true; wait = 1700; }
      else if (del && ci <= 0) { del = false; wi = (wi + 1) % words.length; wait = 350; }
      setTimeout(type, wait);
    };
    setTimeout(type, 2600);
  });

  /* ===== H. リクエストの帯：花火 ===== */
  run('fireworks', function () {
    var rb = $('.req-banner'); if (!rb || !('IntersectionObserver' in window)) return;
    var rc = document.createElement('canvas'); rc.className = 'fx-fw'; rc.setAttribute('aria-hidden', 'true');
    rb.insertBefore(rc, rb.firstChild); rb.classList.add('has-fw');
    var ctx = rc.getContext('2d'), fw = [], W = 0, H = 0, raf = 0, vis = false, last = 0, next = 0;
    function size() { var r = rb.getBoundingClientRect(), d = Math.min(window.devicePixelRatio || 1, 2); W = r.width; H = r.height; rc.width = Math.round(W * d); rc.height = Math.round(H * d); ctx.setTransform(d, 0, 0, d, 0, 0); }
    function tick(now) {
      raf = 0; if (!vis || document.hidden) return;
      var dt = Math.min(0.05, (now - last) / 1000); last = now;
      if (now > next) {
        next = now + 450 + Math.random() * 900;
        var x = W * (0.08 + Math.random() * 0.84), y = H * (0.15 + Math.random() * 0.5), c = COL[(Math.random() * 3) | 0], n = 46;
        for (var i = 0; i < n; i++) { var a = i / n * 6.283 + Math.random() * 0.1, sp = 60 + Math.random() * 130; fw.push({ x: x, y: y, vx: Math.cos(a) * sp, vy: Math.sin(a) * sp, l: 0, m: 1 + Math.random() * 0.6, c: c }); }
      }
      ctx.clearRect(0, 0, W, H);
      for (var j = fw.length - 1; j >= 0; j--) {
        var p = fw[j]; p.l += dt; if (p.l > p.m) { fw.splice(j, 1); continue; }
        p.vx *= (1 - 1.6 * dt); p.vy = p.vy * (1 - 1.6 * dt) + 70 * dt; p.x += p.vx * dt; p.y += p.vy * dt;
        var k = 1 - p.l / p.m; ctx.globalAlpha = k * 0.7; ctx.fillStyle = p.c; ctx.beginPath(); ctx.arc(p.x, p.y, 1.2 + 1.6 * k, 0, 6.283); ctx.fill();
      }
      ctx.globalAlpha = 1; raf = requestAnimationFrame(tick);
    }
    new IntersectionObserver(function (es) {
      vis = es[0].isIntersecting;
      if (vis && !raf) { size(); last = performance.now(); raf = requestAnimationFrame(tick); }
    }).observe(rb);
    document.addEventListener('visibilitychange', function () { if (vis && !document.hidden && !raf) { last = performance.now(); raf = requestAnimationFrame(tick); } });
    var btn = rb.querySelector('.btn'); if (btn) btn.addEventListener('pointerenter', function () { confettiAt(btn, 60); });
  });

  /* ===== I. ライブデータの棚に「LIVE」の点滅 ===== */
  run('live', function () {
    var h = $('#liveShelf .rank-head h2'); if (!h) return;
    var b = document.createElement('span'); b.className = 'fx-live'; b.setAttribute('aria-hidden', 'true'); b.textContent = 'LIVE';
    h.appendChild(b);
  });

  /* ===== K. ページの途中の見本：ガルトンボード（玉が落ちて山ができる） ===== */
  run('galton', function () {
    var anchor = document.getElementById('liveShelf'); if (!anchor || !('IntersectionObserver' in window)) return;
    var sec = document.createElement('section'); sec.className = 'fx-galton';
    sec.setAttribute('aria-label', 'ランダムから山ができる見本（ガルトンボード）');
    sec.innerHTML = '<div class="fg-head"><span class="fg-k">EXPERIMENT</span><b>でたらめに落としても、山の形はだいたい同じになる。</b><span class="fg-n"><i>0</i>個</span></div>' +
      '<canvas aria-hidden="true"></canvas>' +
      '<div class="fg-foot"><span>クリックで50個まとめて落とす</span><a href="sims/galton/">ガルトンボードを触る →</a></div>';
    anchor.parentNode.insertBefore(sec, anchor);
    var cv = sec.querySelector('canvas'), ctx = cv.getContext('2d'), nEl = sec.querySelector('.fg-n i');
    var R = 12, CAP = 46, W = 0, H = 0, d = 1, balls = [], bins = [], total = 0, shown = -1, raf = 0, vis = false, last = 0, acc = 0, fade = 0;
    var binom = []; (function () { var c = 1; for (var j = 0; j <= R; j++) { binom.push(c / Math.pow(2, R)); c = c * (R - j) / (j + 1); } })();
    function reset() { bins = []; for (var i = 0; i <= R; i++) bins.push(0); total = 0; }
    reset();
    function size() { var r = cv.getBoundingClientRect(); d = Math.min(window.devicePixelRatio || 1, 2); W = r.width; H = r.height; cv.width = Math.round(W * d); cv.height = Math.round(H * d); }
    function spawn(delay) {
      var K = [0]; for (var r = 1; r <= R; r++) K.push(K[r - 1] + (Math.random() < 0.5 ? 1 : 0));
      balls.push({ K: K, t: -(delay || 0), sp: 5.5 + Math.random() * 2 });
    }
    function tick(now) {
      raf = 0; if (!vis || document.hidden) return;
      var dt = Math.min(0.05, (now - last) / 1000); last = now;
      var bw = Math.min(44, (W - 24) / (R + 3)), top = 16, rowH = Math.min(11, (H * 0.5) / R), pegB = top + rowH * R, floor = H - 10, cx = W / 2, unit = (floor - pegB - 14) / CAP;
      if (!fade) { acc += dt * 7; while (acc > 1) { acc -= 1; spawn(0); } }
      ctx.setTransform(d, 0, 0, d, 0, 0); ctx.clearRect(0, 0, W, H);
      ctx.fillStyle = 'rgba(20,24,29,.34)';
      for (var r = 0; r < R; r++) for (var k = 0; k <= r; k++) { ctx.beginPath(); ctx.arc(cx + (k - r / 2) * bw, top + r * rowH, 1.6, 0, 6.283); ctx.fill(); }
      ctx.globalAlpha = fade ? Math.max(0, 1 - fade) : 1;
      for (var i = 0; i <= R; i++) {
        var h = bins[i] * unit; ctx.fillStyle = (i === R / 2) ? '#c4442b' : '#2c6b86';
        ctx.fillRect(cx + (i - R / 2) * bw - bw * 0.36, floor - h, bw * 0.72, h);
      }
      if (total > 20) { // 計算上の山（二項分布）を点線で重ねる
        ctx.strokeStyle = 'rgba(20,24,29,.8)'; ctx.lineWidth = 1.4; ctx.setLineDash([4, 4]); ctx.beginPath();
        for (var j = 0; j <= R; j++) { var yy = floor - binom[j] * total * unit, xx = cx + (j - R / 2) * bw; if (j) ctx.lineTo(xx, yy); else ctx.moveTo(xx, yy); }
        ctx.stroke(); ctx.setLineDash([]);
      }
      ctx.globalAlpha = 1;
      ctx.fillStyle = '#14181d'; ctx.fillRect(cx - (R / 2 + 0.7) * bw, floor, (R + 1.4) * bw, 1.2);
      for (var b = balls.length - 1; b >= 0; b--) {
        var o = balls[b]; o.t += dt * o.sp; if (o.t < 0) continue;
        var r0 = Math.floor(o.t), f = o.t - r0, x0, y0;
        if (r0 < R) {
          var xa = cx + (o.K[r0] - r0 / 2) * bw, xb = cx + (o.K[r0 + 1] - (r0 + 1) / 2) * bw;
          x0 = xa + (xb - xa) * f; y0 = top + (r0 + f) * rowH - 5 - Math.sin(f * Math.PI) * 3;
        } else {
          var bin = o.K[R], ff = (o.t - R) * 0.9, yTop = pegB - 5, yEnd = floor - bins[bin] * unit - 3;
          x0 = cx + (bin - R / 2) * bw; y0 = yTop + (yEnd - yTop) * Math.min(1, ff * ff);
          if (ff >= 1) { bins[bin]++; total++; balls.splice(b, 1); if (bins[bin] >= CAP && !fade) fade = 0.001; continue; }
        }
        ctx.beginPath(); ctx.arc(x0, y0, 2.6, 0, 6.283); ctx.fill();
      }
      if (fade) { fade += dt * 0.9; if (fade >= 1) { fade = 0; reset(); balls.length = 0; } }
      if (shown !== total) { shown = total; nEl.textContent = total; }
      raf = requestAnimationFrame(tick);
    }
    function start() { if (vis && !document.hidden && !raf) { size(); last = performance.now(); raf = requestAnimationFrame(tick); } }
    new IntersectionObserver(function (es) { vis = es[0].isIntersecting; start(); }).observe(sec);
    document.addEventListener('visibilitychange', start);
    window.addEventListener('resize', function () { if (vis) size(); });
    sec.addEventListener('click', function (e) {
      if (e.target.closest('a')) return;
      for (var i = 0; i < 50; i++) spawn(Math.random() * 6);
    });
    window.__fxGalton = { state: function () { return { total: total, balls: balls.length, W: W, H: H, vis: vis }; } };
  });

  /* ===== J. 棚の大きな番号（01〜04）・ボタンを押したら紙ふぶき ===== */
  run('numbers', function () {
    ['rankWrap', 'liveShelf', 'labShelf', 'rikaShelf'].forEach(function (id, i) {
      var el = document.getElementById(id); if (el) { el.setAttribute('data-fxno', '0' + (i + 1)); el.classList.add('fx-no'); }
    });
  });
  run('clicks', function () {
    document.addEventListener('click', function (e) {
      var b = e.target && e.target.closest ? e.target.closest('.chip, .cat-more, .rank-tabs button, .rank-more, .cat-title .all, .hs-dots button') : null;
      if (!b) return;
      var r = b.getBoundingClientRect();
      burst(r.left + r.width / 2, r.top + r.height / 2, 26, { speed: 260, life: 1, size: 3.2, g: 560, up: 160, confetti: true });
    });
  });

  window.__fxMore = { burst: function (x, y, n, o) { burst(x, y, n, o); } };
})();
