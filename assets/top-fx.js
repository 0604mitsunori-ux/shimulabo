/* シミュラボ トップページの動き（2026-11-17）
   - ヒーロー右の「回せる点描の舞台」（Canvas 2D・外部ライブラリなし）
   - 今週よく遊ばれているシミュの流れる帯（assets/ranking.json）
   - スクロールで現れる・読み進みの線・数字のカウントアップ
   どれも「あれば足す」作りで、失敗してもページ本体は今まで通り表示される。 */
(function () {
  'use strict';
  var RM = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };

  /* ================= 1. 回せる点描の舞台 ================= */
  // 題材を足すときは SHAPES に1つ足す（fn は i番目の点の位置を o に書く。座標はおよそ -1〜1）
  var hero = $('.hero');
  var stageApi = null;
  if (hero && hero.querySelector('.lead')) {
    try { stageApi = buildStage(hero); } catch (e) { window.__fxErr = String(e && e.stack || e); }
  }

  function buildStage(hero) {
    var small = window.innerWidth < 700;
    var N = small ? 1100 : 1700;
    var R1 = new Float32Array(N), R2 = new Float32Array(N), R3 = new Float32Array(N);
    // 毎回同じ並びになる乱数（見た目を安定させる）
    var seed = 20261117;
    function rnd() { seed = (seed * 1664525 + 1013904223) >>> 0; return seed / 4294967296; }
    for (var i = 0; i < N; i++) { R1[i] = rnd(); R2[i] = rnd(); R3[i] = rnd(); }
    var sin = Math.sin, cos = Math.cos, PI = Math.PI;

    function fib(k, m, o) { // 球の表面に均等に並べる
      var y = 1 - 2 * (k + 0.5) / m, r = Math.sqrt(Math.max(0, 1 - y * y)), a = k * 2.399963;
      o.x = r * cos(a); o.y = y; o.z = r * sin(a);
    }

    // 色：0 墨 / 1 藍 / 2 朱 / 3 うすい墨 / 4 金
    var COLORS = ['rgba(20,24,29,.88)', 'rgba(44,107,134,.92)', 'rgba(196,68,43,.95)', 'rgba(20,24,29,.26)', 'rgba(169,122,36,.95)'];

    /* --- DNAの二重らせん --- */
    function dna(i, t, o) {
      var nS = Math.floor(N * 0.36);
      if (i < nS * 2) {
        var B = i >= nS, k = B ? i - nS : i, u = k / nS;
        var a = u * PI * 5 + t * 0.5 + (B ? PI : 0);
        o.x = 0.42 * cos(a) + (R1[i] - 0.5) * 0.035; o.z = 0.42 * sin(a) + (R2[i] - 0.5) * 0.035;
        o.y = (u - 0.5) * 1.95; o.c = B ? 1 : 0; o.s = 1.5;
      } else {
        var k2 = i - nS * 2, m = N - nS * 2, RUNG = 20, j = k2 % RUNG;
        var s = Math.floor(k2 / RUNG) / Math.ceil(m / RUNG);
        var u2 = (j + 0.5) / RUNG, a2 = u2 * PI * 5 + t * 0.5, q = (s * 2 - 1) * 0.38;
        o.x = q * cos(a2); o.z = q * sin(a2); o.y = (u2 - 0.5) * 1.95;
        o.c = ((s < 0.5) !== (j % 2 === 0)) ? 2 : 4; o.s = 1.15;
      }
    }

    /* --- 太陽系 --- */
    var ORB = [0.24, 0.36, 0.5, 0.66, 0.82, 1.0], PSZ = [0.024, 0.034, 0.04, 0.03, 0.075, 0.06];
    function solar(i, t, o) {
      var nSun = Math.floor(N * 0.1), nP = Math.floor(N * 0.07);
      if (i < nSun) { fib(i, nSun, o); o.x *= 0.11; o.y *= 0.11; o.z *= 0.11; o.c = 2; o.s = 1.5; return; }
      var k = i - nSun;
      if (k < nP * 6) {
        var j = Math.floor(k / nP), q = k % nP, r = PSZ[j];
        var a = j * 2.1 + t * 0.16 / Math.pow(ORB[j], 1.5);
        var px = ORB[j] * cos(a), pz = ORB[j] * sin(a);
        if (j === 4 && q % 3 === 0) { // 土星の輪
          var ra = q * 0.7, rr = r * (1.5 + R1[i] * 0.7);
          o.x = px + rr * cos(ra); o.y = 0; o.z = pz + rr * sin(ra); o.c = 4; o.s = 0.9; return;
        }
        fib(q, nP, o); o.x = o.x * r + px; o.y *= r; o.z = o.z * r + pz; o.c = j % 2 ? 1 : 0; o.s = 1.4; return;
      }
      k -= nP * 6;
      var m = N - nSun - nP * 6, jj = k % 6, aa = (Math.floor(k / 6) / (m / 6)) * PI * 2;
      o.x = ORB[jj] * cos(aa); o.y = 0; o.z = ORB[jj] * sin(aa); o.c = 3; o.s = 0.9;
    }

    /* --- 波紋（2つの波の干渉） --- */
    var G = Math.floor(Math.sqrt(N));
    function ripple(i, t, o) {
      var gi = i % G, gj = Math.floor(i / G) % G;
      var x = (gi / (G - 1)) * 2 - 1, z = (gj / (G - 1)) * 2 - 1;
      var d1 = Math.sqrt((x + 0.4) * (x + 0.4) + z * z), d2 = Math.sqrt((x - 0.4) * (x - 0.4) + z * z);
      var y = 0.09 * (sin(11 * d1 - 3.2 * t) / (1 + 1.5 * d1) + sin(11 * d2 - 3.2 * t) / (1 + 1.5 * d2));
      o.x = x * 1.05; o.z = z * 1.05; o.y = y - 0.08;
      o.c = y > 0.045 ? 1 : (y < -0.045 ? 0 : 3); o.s = 1.05 + Math.abs(y) * 7;
    }

    /* --- 振り子の波（長さのちがう15本） --- */
    var PN = 15;
    function pend(i, t, o) {
      var j = i % PN, k = Math.floor(i / PN), m = Math.ceil(N / PN), nStr = Math.floor(m * 0.45);
      var z = (j / (PN - 1)) * 1.7 - 0.85;
      var L = 1.55 * Math.pow(12 / (12 + j), 2);         // 周期が (12+j) に反比例する長さ
      var th = 0.5 * cos(2 * PI * (12 + j) * t / 36);
      var bx = L * sin(th), by = 0.95 - L * cos(th);
      if (k < nStr) { var s = k / nStr; o.x = bx * s; o.y = 0.95 - (0.95 - by) * s; o.z = z; o.c = 3; o.s = 1.05; }
      else { fib(k - nStr, m - nStr, o); o.x = o.x * 0.055 + bx; o.y = o.y * 0.055 + by; o.z = o.z * 0.055 + z; o.c = (j % 5 === 0) ? 2 : 0; o.s = 1.3; }
    }

    /* --- ローレンツ・アトラクタ（カオスの蝶） --- */
    var LEN = 5200, LZ = new Float32Array(LEN * 3);
    (function () {
      var x = 0.1, y = 0, z = 0, dt = 0.006;
      for (var w = 0; w < 600; w++) { var dx = 10 * (y - x), dy = x * (28 - z) - y, dz = x * y - (8 / 3) * z; x += dx * dt; y += dy * dt; z += dz * dt; }
      for (var q = 0; q < LEN; q++) {
        var dx2 = 10 * (y - x), dy2 = x * (28 - z) - y, dz2 = x * y - (8 / 3) * z; x += dx2 * dt; y += dy2 * dt; z += dz2 * dt;
        LZ[q * 3] = x / 21; LZ[q * 3 + 1] = (z - 25) / 25; LZ[q * 3 + 2] = y / 27;
      }
    })();
    function lorenz(i, t, o) {
      var q = ((i * 3 + Math.floor(t * 40)) % LEN) * 3;
      o.x = LZ[q]; o.y = LZ[q + 1]; o.z = LZ[q + 2];
      if (i % 40 === 0) { o.c = 2; o.s = 2.2; } else { o.c = LZ[q] > 0 ? 1 : 0; o.s = 1.1; }
    }

    /* --- 月の満ち欠け（朱の粒＝太陽の光） --- */
    function moon(i, t, o) {
      var nM = Math.floor(N * 0.8), a = t * 0.4, lx = cos(a), lz = sin(a);
      if (i < nM) {
        fib(i, nM, o); var lit = o.x * lx + o.z * lz > 0;
        o.x *= 0.7; o.y *= 0.7; o.z *= 0.7; o.c = lit ? 4 : 3; o.s = lit ? 1.5 : 0.8;
      } else {
        var u = (R1[i] + t * 0.12) % 1, d = 1.55 - u * 0.6, f1 = (R2[i] - 0.5) * 1.1, f2 = (R3[i] - 0.5) * 1.1;
        o.x = lx * d - lz * f1; o.z = lz * d + lx * f1; o.y = f2; o.c = 2; o.s = 0.8;
      }
    }

    var SHAPES = [
      { name: 'DNAの二重らせん', href: 'sims/dna/', fn: dna, pitch: 0.12, roll: 0.3, spin: 0.1 },
      { name: '太陽系', href: 'sims/solar-system/', fn: solar, pitch: 0.55, roll: 0, spin: 0.05 },
      { name: '波紋と波の干渉', href: 'sims/ripple/', fn: ripple, pitch: 0.75, roll: 0, spin: 0.07 },
      { name: '振り子の波', href: 'sims/pendulum-wave/', fn: pend, pitch: 0.16, roll: 0, spin: 0.09 },
      { name: 'ローレンツ・アトラクタ', href: 'sims/lorenz/', fn: lorenz, pitch: 0.2, roll: 0, spin: 0.16 },
      { name: '月の満ち欠け', href: 'sims/tsuki-michikake/', fn: moon, pitch: 0.2, roll: 0, spin: 0.05 }
    ];

    /* --- 舞台のDOM --- */
    var stage = document.createElement('div');
    stage.className = 'hero-stage'; stage.id = 'heroStage';
    stage.innerHTML =
      '<canvas aria-hidden="true"></canvas>' +
      '<div class="hs-cap"><span class="hs-fig"></span><span class="hs-name"></span></div>' +
      '<span class="hs-hint">ドラッグで回す・クリックではじける</span>' +
      '<div class="hs-foot"><div class="hs-dots" role="group" aria-label="見本を切り替える"></div>' +
      '<a class="hs-go" href="#">このシミュを触る →</a></div>';
    hero.querySelector('.lead').after(stage);
    hero.classList.add('has-stage');
    var cv = stage.querySelector('canvas'), ctx = cv.getContext('2d');
    var cap = stage.querySelector('.hs-cap'), figEl = stage.querySelector('.hs-fig'), nameEl = stage.querySelector('.hs-name');
    var go = stage.querySelector('.hs-go'), dots = stage.querySelector('.hs-dots');
    SHAPES.forEach(function (s, i) {
      var b = document.createElement('button'); b.type = 'button';
      b.setAttribute('aria-label', s.name + ' を見る'); b.title = s.name;
      b.addEventListener('click', function () { goTo(i, true); });
      dots.appendChild(b);
    });

    var cur = 0, nxt = -1, mStart = 0, lastSwitch = 0, holdUntil = 0;
    var MORPH = 1.7, STAY = 7.5;
    function setCaption(i) {
      figEl.textContent = 'FIG. ' + String(i + 1).padStart(2, '0');
      nameEl.textContent = SHAPES[i].name; go.href = SHAPES[i].href;
      go.setAttribute('aria-label', SHAPES[i].name + ' のシミュを触る');
      [].forEach.call(dots.children, function (b, k) { b.setAttribute('aria-current', k === i ? 'true' : 'false'); });
      cap.classList.remove('swap'); void cap.offsetWidth; cap.classList.add('swap');
    }
    function goTo(i, byUser) {
      var now = performance.now() / 1000;
      if (byUser) holdUntil = now + 14;
      if (i === cur && nxt < 0) return;
      if (nxt >= 0) cur = nxt;             // 変形の途中なら行き先を現在地にして続ける
      if (i === cur) { nxt = -1; return; }
      if (RM) { cur = i; nxt = -1; setCaption(i); draw(now); return; }
      nxt = i; mStart = now; setCaption(i);
    }

    /* --- 向き（ドラッグ・マウス追従） --- */
    var burstT = 0, mOn = false, mx = 0, my = 0;
    var yaw = 0.6, pitchOff = 0, tx = 0, ty = 0, px = 0, py = 0, drag = null, pitchBase = SHAPES[0].pitch, rollBase = SHAPES[0].roll;
    stage.addEventListener('pointerdown', function (e) {
      if (e.target.closest('a,button')) return;
      drag = { x: e.clientX, y: e.clientY, id: e.pointerId, sx: e.clientX, sy: e.clientY }; stage.classList.add('is-drag', 'touched');
      try { stage.setPointerCapture(e.pointerId); } catch (_) {}
    });
    stage.addEventListener('pointermove', function (e) {
      if (!drag) return;
      yaw += (e.clientX - drag.x) * 0.009; pitchOff += (e.clientY - drag.y) * 0.006;
      pitchOff = Math.max(-1.1, Math.min(1.1, pitchOff));
      drag.x = e.clientX; drag.y = e.clientY;
      if (!running) draw(performance.now() / 1000);
    });
    function endDrag(e) {
      if (drag && e && e.type === 'pointerup' && Math.abs(e.clientX - drag.sx) + Math.abs(e.clientY - drag.sy) < 6) burstT = performance.now() / 1000; // 動かさずに離した＝クリック→はじける
      drag = null; stage.classList.remove('is-drag');
    }
    stage.addEventListener('pointermove', function (e) { if (e.pointerType === 'touch') return; var r = stage.getBoundingClientRect(); mx = e.clientX - r.left; my = e.clientY - r.top; mOn = true; });
    stage.addEventListener('pointerleave', function () { mOn = false; });
    stage.addEventListener('pointerup', endDrag); stage.addEventListener('pointercancel', endDrag);
    hero.addEventListener('pointermove', function (e) {
      if (e.pointerType === 'touch') return;
      var r = hero.getBoundingClientRect();
      tx = ((e.clientX - r.left) / r.width - 0.5) * 0.5; ty = ((e.clientY - r.top) / r.height - 0.5) * 0.3;
    });
    hero.addEventListener('pointerleave', function () { tx = 0; ty = 0; });

    /* --- 描く --- */
    var W = 0, H = 0, DPR = 1;
    function resize() {
      var r = stage.getBoundingClientRect();
      DPR = Math.min(window.devicePixelRatio || 1, 2);
      W = Math.max(10, r.width); H = Math.max(10, r.height);
      cv.width = Math.round(W * DPR); cv.height = Math.round(H * DPR);
      if (!running) draw(performance.now() / 1000);
    }
    var BK = [0, 1, 2, 3, 4].map(function () { return new Float32Array(N * 3); }), BN = [0, 0, 0, 0, 0];
    var A = { x: 0, y: 0, z: 0, c: 0, s: 1 }, B = { x: 0, y: 0, z: 0, c: 0, s: 1 };
    var lastT = 0;
    function ease(k) { return k < 0 ? 0 : k > 1 ? 1 : k * k * k * (k * (k * 6 - 15) + 10); }

    function draw(t) {
      var dt = Math.min(0.05, Math.max(0, t - lastT)); lastT = t;
      var m = -1;
      if (nxt >= 0) { m = (t - mStart) / MORPH; if (m >= 1) { cur = nxt; nxt = -1; m = -1; lastSwitch = t; } }
      else if (!RM && !drag && t > holdUntil && t - lastSwitch > STAY) { goTo((cur + 1) % SHAPES.length, false); m = 0; }
      var SA = SHAPES[cur], SB = nxt >= 0 ? SHAPES[nxt] : null;
      var tgtP = SB ? SB.pitch : SA.pitch, tgtR = SB ? SB.roll : SA.roll;
      pitchBase += (tgtP - pitchBase) * Math.min(1, dt * 2.2); rollBase += (tgtR - rollBase) * Math.min(1, dt * 2.2);
      if (!drag && !RM) yaw += dt * (SB ? SB.spin : SA.spin);
      px += (tx - px) * Math.min(1, dt * 4); py += (ty - py) * Math.min(1, dt * 4);
      var ya = yaw + px, pa = pitchBase + pitchOff + py;
      var cy_ = cos(ya), sy_ = sin(ya), cp = cos(pa), sp = sin(pa), cr = cos(rollBase), sr = sin(rollBase);
      var S = Math.min(W, H) * 0.36, cx = W / 2, cyc = H / 2 + (H < 300 ? -4 : 6), k0 = S / 150;
      var bz = burstT ? Math.exp(-(t - burstT) * 2.4) * Math.sin(Math.min(1, (t - burstT) * 7) * 1.5708) : 0; if (bz < 0.004) bz = 0;
      BN[0] = BN[1] = BN[2] = BN[3] = BN[4] = 0;
      for (var i = 0; i < N; i++) {
        SA.fn(i, t, A);
        var x = A.x, y = A.y, z = A.z, c = A.c, s = A.s;
        if (SB) {
          SB.fn(i, t, B);
          var k = ease(m * 1.45 - R1[i] * 0.45), sw = sin(PI * k) * 0.5;
          x += (B.x - x) * k + (R2[i] - 0.5) * sw; y += (B.y - y) * k + (R3[i] - 0.5) * sw; z += (B.z - z) * k + (R1[i] - 0.5) * sw;
          s += (B.s - s) * k; if (k > 0.5) c = B.c;
        }
        if (bz) { var eb = 1 + bz * (0.5 + R2[i] * 2.4); x *= eb; y *= eb; z *= eb; }
        // 傾き（roll）→ 横回転（yaw）→ 縦回転（pitch）
        var x1 = x * cr - y * sr, y1 = x * sr + y * cr;
        var x2 = x1 * cy_ + z * sy_, z2 = -x1 * sy_ + z * cy_;
        var y3 = y1 * cp - z2 * sp, z3 = y1 * sp + z2 * cp;
        var p = 3 / (3 + z3);
        var b = BK[c], n = BN[c] * 3;
        var X = cx + x2 * S * p, Y = cyc - y3 * S * p;
        if (mOn) { var ddx = X - mx, ddy = Y - my, d2 = ddx * ddx + ddy * ddy; if (d2 < 4900) { var ff = (1 - d2 / 4900) * 20 / Math.sqrt(d2 + 1); X += ddx * ff; Y += ddy * ff; } }
        b[n] = X; b[n + 1] = Y; b[n + 2] = Math.max(0.45, s * p * k0);
        BN[c]++;
      }
      ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
      if (running) { ctx.globalCompositeOperation = 'destination-out'; ctx.fillStyle = 'rgba(0,0,0,0.42)'; ctx.fillRect(0, 0, W, H); ctx.globalCompositeOperation = 'source-over'; } // 動いている間は残像を少し残す
      else ctx.clearRect(0, 0, W, H);
      var order = [3, 0, 1, 4, 2];
      for (var oi = 0; oi < 5; oi++) {
        var ci = order[oi], bb = BK[ci], nn = BN[ci];
        if (!nn) continue;
        ctx.fillStyle = COLORS[ci]; ctx.beginPath();
        for (var q = 0; q < nn; q++) {
          var X = bb[q * 3], Y = bb[q * 3 + 1], Rr = bb[q * 3 + 2];
          ctx.moveTo(X + Rr, Y); ctx.arc(X, Y, Rr, 0, 6.2832);
        }
        ctx.fill();
      }
    }

    /* --- 回す・止める（見えていない間は描かない） --- */
    var running = false, visible = true, raf = 0;
    function loop(now) { raf = 0; if (!running) return; draw(now / 1000); raf = requestAnimationFrame(loop); }
    function sync() {
      var want = visible && !document.hidden && !RM;
      if (want && !running) { running = true; lastT = performance.now() / 1000; if (!raf) raf = requestAnimationFrame(loop); }
      else if (!want) running = false;
    }
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) { visible = es[0].isIntersecting; sync(); }).observe(stage);
    }
    document.addEventListener('visibilitychange', sync);
    if ('ResizeObserver' in window) new ResizeObserver(resize).observe(stage); else window.addEventListener('resize', resize);

    setCaption(0); resize(); lastSwitch = performance.now() / 1000; draw(lastSwitch); sync();
    return { goTo: goTo, draw: draw, shapes: SHAPES, state: function () { return { cur: cur, nxt: nxt, running: running, W: W, H: H, N: N }; } };
  }
  window.__fxStage = stageApi; // 動作確認用

  /* ================= 2. 流れる帯（今週よく遊ばれている） ================= */
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function buildTicker(data) {
    var rows = (data && data.rankings && data.rankings.week) || [];
    if (!hero || rows.length < 5) return;
    var items = rows.slice(0, 10).map(function (r, i) {
      return '<a href="sims/' + encodeURIComponent(r.id) + '/"><i>' + (i + 1) + '位</i><span>' + esc(r.emoji || '') + ' ' + esc(r.title) + '</span><b>' + Number(r.views).toLocaleString('ja-JP') + '回</b></a>';
    }).join('');
    var nav = document.createElement('nav');
    nav.className = 'fx-ticker'; nav.setAttribute('aria-label', '今週よく遊ばれているシミュ');
    nav.innerHTML = '<span class="lbl">今週の人気</span><div class="view"><div class="track"><span class="set">' + items + '</span><span class="set" aria-hidden="true">' + items + '</span></div></div>';
    [].forEach.call(nav.querySelectorAll('.set[aria-hidden] a'), function (a) { a.tabIndex = -1; });
    nav.querySelector('.track').style.setProperty('--dur', Math.max(40, rows.slice(0, 10).length * 7) + 's');
    hero.after(nav);
  }
  if (hero && window.fetch) {
    fetch('assets/ranking.json', { cache: 'no-cache' }).then(function (r) { return r.ok ? r.json() : null; }).then(buildTicker).catch(function () {});
  }

  /* ================= 3. 数字のカウントアップ（公開本数） ================= */
  var cnt = $('.hero .meta-strip b');
  if (cnt && !RM && /^\d+$/.test(cnt.textContent.trim())) {
    var goal = parseInt(cnt.textContent, 10), t0 = 0;
    cnt.textContent = '0';
    var stepNum = function (now) {
      if (!t0) t0 = now;
      var k = Math.min(1, (now - t0) / 1300), e = 1 - Math.pow(1 - k, 3);
      cnt.textContent = String(Math.round(goal * e));
      if (k < 1) requestAnimationFrame(stepNum);
    };
    setTimeout(function () { requestAnimationFrame(stepNum); }, 450);
    setTimeout(function () { cnt.textContent = String(goal); }, 4000); // 画面が裏にあっても必ず正しい数にする
  }

  /* ================= 4. スクロールで現れる ================= */
  if ('IntersectionObserver' in window && !RM) {
    var targets = [].slice.call(document.querySelectorAll('main.wrap > section, .cat-block, .group-chips'));
    var vh = window.innerHeight || 800;
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('fx-in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -6% 0px' });
    targets.forEach(function (el) {
      if (el.getBoundingClientRect().top < vh * 0.92) { el.classList.add('fx-in'); return; } // 最初から見えている所は隠さない
      el.classList.add('fx-rv'); io.observe(el);
    });
    // 検索や絞り込みで並びが変わったら、取りこぼしを防ぐために全部出す
    var showAllNow = function () { targets.forEach(function (el) { el.classList.add('fx-in'); }); };
    var si = document.getElementById('searchInput'); if (si) si.addEventListener('input', showAllNow, { once: true });
    setTimeout(function () { if (document.hidden) showAllNow(); }, 3000);
  } else {
    [].forEach.call(document.querySelectorAll('.cat-block'), function (el) { el.classList.add('fx-in'); });
  }

  /* ================= 5. 読み進みの線・ヘッダーの影 ================= */
  var bar = document.createElement('div'); bar.className = 'fx-progress'; bar.setAttribute('aria-hidden', 'true');
  document.body.appendChild(bar);
  var header = $('.site-header'), ticking = false;
  function onScroll() {
    ticking = false;
    var d = document.documentElement, max = d.scrollHeight - d.clientHeight, y = window.scrollY || d.scrollTop;
    bar.style.transform = 'scaleX(' + (max > 0 ? Math.min(1, y / max) : 0) + ')';
    if (header) header.classList.toggle('fx-scrolled', y > 8);
  }
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();
})();
