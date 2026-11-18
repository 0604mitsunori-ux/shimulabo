/* =========================================================
   シミュラボ「人の粒」アニメ（crowd.js）
   「確率○%」「100人中○位」を、人の点の群れで見せる共通部品。
   ライブラリなし・Canvas 2D。画面に入った時だけ動く。動きを減らす設定の人には最後の形だけ出す。

   Crowd.lottery(el, opts)       … n人が抽選を何回か受けて、当たった人が金色になる → 最後に当選者が前に集まる
     opts: n(1000) p(1回で当たる確率) rounds(回数) title roundLabel(k) unit('人') you(false＝「あなた」の印を出さない)
           final(wins, n, youWon) → 下に出す文 / replay(true)
   Crowd.distribution(el, opts)  … n人の点数が上から落ちて山（分布）になり、自分の点が光る
     opts: n(100) mean sd you line lineLabel title tick(v) rankText(rank,n) final(rank,n,above)
           goodAbove(true＝線より右を色づけ)
   Crowd.units(el, opts)         … 全部の回数・時間を玉で並べ、もう過ぎた分が灰色に変わって、のこりが光る
     opts: total used unit('回') title leftLabel('のこり') now(false＝「いま」の印を出さない) final(left,total)
   Crowd.pile(el, opts)          … お金・物のブロックが落ちて積み上がる（棒を2〜4本並べて比べられる）
     opts: bars:[{label,value,color}] unit('円') per(1ブロックの量・省略で自動) title final() fmtv(v)
   Crowd.race(el, opts)          … AとBの線が左から右へ伸びて、逆転した所に★
     opts: series:[{label,values[],color}] xLabel(i) unit fmtv(v) title crossLabel(i) final(crossIndex)

   el の中に canvas と説明文を作る。同じ el に再度呼ぶと、前の動きを止めて作り直す。
   ========================================================= */
(function () {
  'use strict';
  var RM = !!(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches);
  var GOLD = '#e3a21a', GRAY = '#cfc8ba', DARK = '#8b929c', GOOD = '#3f9a72';

  function cssVar(name, d) {
    var v = getComputedStyle(document.documentElement).getPropertyValue(name);
    return (v && v.trim()) || d;
  }
  function font(px, bold) {
    return (bold ? '800 ' : '600 ') + px + 'px ' + getComputedStyle(document.body).fontFamily;
  }
  function easeOut(t) { t = t < 0 ? 0 : t > 1 ? 1 : t; return 1 - Math.pow(1 - t, 3); }
  function easeInOut(t) { t = t < 0 ? 0 : t > 1 ? 1 : t; return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }
  function fmt(n) { return Math.round(n).toLocaleString('ja-JP'); }

  /* 器を作る：canvas＋説明文＋もう一度ボタン */
  function build(el, height) {
    if (el._crowdStop) el._crowdStop();
    el.innerHTML = '';
    el.classList.add('crowd');
    var c = document.createElement('canvas');
    c.setAttribute('role', 'img');
    c.style.cssText = 'display:block;width:100%;height:' + height + 'px;border-radius:10px;background:' + cssVar('--card', '#fff') + ';border:1px solid ' + cssVar('--line', '#e2ded4');
    var cap = document.createElement('p');
    cap.className = 'crowd-cap';
    cap.setAttribute('aria-live', 'polite');
    cap.style.cssText = 'margin:10px 0 0;font-size:14px;line-height:1.7;color:' + cssVar('--ink', '#14181d') + ';min-height:1.7em;text-align:center';
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'btn btn-ghost crowd-replay';
    btn.textContent = '↻ もう一度ためす';
    btn.style.cssText = 'width:auto;display:none;margin:8px auto 0;padding:8px 18px;font-size:13px';
    el.appendChild(c); el.appendChild(cap); el.appendChild(btn);
    var w = el.clientWidth || 600, dpr = Math.min(2, window.devicePixelRatio || 1);
    c.width = Math.round(w * dpr); c.height = Math.round(height * dpr);
    var g = c.getContext('2d'); g.setTransform(dpr, 0, 0, dpr, 0, 0);
    return { c: c, g: g, w: w, h: height, cap: cap, btn: btn };
  }

  /* 画面に入ったら start、時間 total(ms) まで draw(t) を回す */
  function play(el, S, total, draw) {
    var raf = 0, io = null, stopped = false, t0 = 0;
    function frame(now) {
      if (stopped) return;
      if (!t0) t0 = now;
      var t = now - t0;
      draw(Math.min(t, total));
      if (t < total) raf = requestAnimationFrame(frame);
      else S.btn.style.display = 'flex';
    }
    function start() {
      if (RM) { draw(total); S.btn.style.display = 'flex'; return; }
      t0 = 0; S.btn.style.display = 'none'; raf = requestAnimationFrame(frame);
    }
    el._crowdStop = function () { stopped = true; cancelAnimationFrame(raf); if (io) io.disconnect(); };
    draw(0);
    if ('IntersectionObserver' in window) {
      io = new IntersectionObserver(function (es) {
        if (es[0].isIntersecting) { io.disconnect(); io = null; start(); }
      }, { threshold: .35 });
      io.observe(S.c);
    } else start();
  }

  function dot(g, x, y, r, color) {
    g.fillStyle = color; g.beginPath(); g.arc(x, y, r, 0, 6.2832); g.fill();
  }
  function label(g, text, x, y, color) { // 点の上でも読めるよう白いふちどり
    g.font = font(11, true); g.textAlign = 'center'; g.textBaseline = 'middle';
    g.lineJoin = 'round'; g.lineWidth = 3.5; g.strokeStyle = 'rgba(255,255,255,.95)'; g.strokeText(text, x, y);
    g.fillStyle = color; g.fillText(text, x, y);
  }
  function ring(g, x, y, r, color) {
    g.strokeStyle = color; g.lineWidth = 2; g.beginPath(); g.arc(x, y, r, 0, 6.2832); g.stroke();
  }

  /* ===== 抽選 ===== */
  function lottery(el, o) {
    var n = Math.max(10, Math.min(2000, o.n || 1000));
    var p = Math.max(0, Math.min(1, +o.p || 0));
    var R = Math.max(1, Math.min(100, Math.round(o.rounds || 1)));
    var narrow = (el.clientWidth || 600) < 520;
    var S = build(el, o.height || (narrow ? 300 : 340)), g = S.g, W = S.w, H = S.h;
    var ink = cssVar('--ink', '#14181d'), ink3 = cssVar('--ink-3', '#8b929c'), accent = cssVar('--accent', '#c4442b');

    // 並べ方（上に見出し、残りに格子）
    var unitS = o.unit || '人', titleS = o.title || '結果';
    var lay = headLayout(g, W, narrow, titleS, '● 当選 ' + fmt(n) + ' / ' + fmt(n) + unitS);
    var top = 44 + lay.extra, bot = 14, aw = W - 24, ah = H - top - bot;
    var cols = Math.max(1, Math.ceil(Math.sqrt(n * aw / ah))), rows = Math.ceil(n / cols);
    var cell = Math.min(aw / cols, ah / rows), r = Math.max(1.1, cell * .36);
    var ox = (W - cols * cell) / 2 + cell / 2, oy = top + (ah - rows * cell) / 2 + cell / 2;
    function pos(k) { return [ox + (k % cols) * cell, oy + Math.floor(k / cols) * cell]; }
    var you = Math.min(n - 1, Math.floor(rows / 2) * cols + Math.floor(cols / 2));

    // 先に全員の抽選を決める（何回目で当たったか。-1＝最後まで外れ）
    var win = new Array(n), wins = 0;
    for (var i = 0; i < n; i++) {
      win[i] = -1;
      for (var k = 0; k < R; k++) { if (Math.random() < p) { win[i] = k; wins++; break; } }
    }
    // 最後に当選者を前へ集める並び順
    var order = [];
    for (i = 0; i < n; i++) order.push(i);
    order.sort(function (a, b) {
      var wa = win[a] >= 0, wb = win[b] >= 0;
      if (wa !== wb) return wa ? -1 : 1;
      if (wa && win[a] !== win[b]) return win[a] - win[b];
      return a - b;
    });
    var slot = new Array(n);
    for (i = 0; i < n; i++) slot[order[i]] = i;
    var jit = new Array(n);
    for (i = 0; i < n; i++) jit[i] = Math.random();

    var rd = Math.max(160, Math.min(900, 4800 / R));          // 1回の抽選にかける時間
    var tA = R * rd, tB = tA + 500, tC = tB + 1300, total = tC + 200;
    function winTime(i) { return win[i] < 0 ? Infinity : (win[i] + .1 + jit[i] * .75) * rd; }
    var youWon = win[you] >= 0;
    var roundLabel = o.roundLabel || function (k) { return (k + 1) + '回目の抽選'; };
    S.c.setAttribute('aria-label', (o.title || '') + '：' + fmt(n) + '人中 ' + fmt(wins) + '人が当選');

    play(el, S, total, function (t) {
      g.clearRect(0, 0, W, H);
      // 見出し
      var k = Math.min(R - 1, Math.floor(t / rd)), cnt = 0;
      for (i = 0; i < n; i++) if (winTime(i) <= t) cnt++;
      header(g, W, narrow, t < tA ? roundLabel(k) + (R > 1 ? '（' + (k + 1) + '/' + R + '）' : '') : titleS,
        [['● 当選 ' + fmt(cnt), GOLD], [' / ' + fmt(n) + unitS, ink3]], lay);

      // 点
      var m = t < tB ? 0 : easeInOut((t - tB) / (tC - tB));
      for (i = 0; i < n; i++) {
        var a = pos(i), b = pos(slot[i]);
        var x = a[0] + (b[0] - a[0]) * m, y = a[1] + (b[1] - a[1]) * m;
        var wt = winTime(i), on = wt <= t, rr = r;
        if (on && t - wt < 320) rr = r * (1 + .9 * Math.sin(Math.PI * (t - wt) / 320));
        dot(g, x, y, rr, on ? GOLD : GRAY);
        if (i === you && o.you !== false) {
          ring(g, x, y, r + 3.5, accent);
          if (t >= tC) {
            var ly = y - r - 12 < top - 4 ? y + r + 13 : y - r - 12;
            label(g, 'あなた', x, ly, accent);
          }
        }
      }
      if (t >= tC - 1) {
        S.cap.textContent = o.final ? o.final(wins, n, youWon)
          : fmt(n) + '人中 ' + fmt(wins) + '人が当選（' + (wins / n * 100).toFixed(1) + '%）。このシミュでは、あなたは' + (youWon ? '当選！' : '落選…');
      } else S.cap.textContent = ' ';
    });
    S.btn.onclick = function () { lottery(el, o); };
  }

  /* ===== 分布（点数の山） ===== */
  function invNorm(q) { // Acklam の近似
    var a = [-39.69683028665376, 220.9460984245205, -275.9285104469687, 138.357751867269, -30.66479806614716, 2.506628277459239],
      b = [-54.47609879822406, 161.5858368580409, -155.6989798598866, 66.80131188771972, -13.28068155288572],
      c = [-.007784894002430293, -.3223964580411365, -2.400758277161838, -2.549732539343734, 4.374664141464968, 2.938163982698783],
      d = [.007784695709041462, .3224671290700398, 2.445134137142996, 3.754408661907416], pl = .02425, x, r;
    if (q < pl) { x = Math.sqrt(-2 * Math.log(q)); return (((((c[0] * x + c[1]) * x + c[2]) * x + c[3]) * x + c[4]) * x + c[5]) / ((((d[0] * x + d[1]) * x + d[2]) * x + d[3]) * x + 1); }
    if (q > 1 - pl) { x = Math.sqrt(-2 * Math.log(1 - q)); return -(((((c[0] * x + c[1]) * x + c[2]) * x + c[3]) * x + c[4]) * x + c[5]) / ((((d[0] * x + d[1]) * x + d[2]) * x + d[3]) * x + 1); }
    x = q - .5; r = x * x;
    return (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * x / (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1);
  }

  function distribution(el, o) {
    var n = Math.max(20, Math.min(400, o.n || 100));
    var mean = +o.mean || 0, sd = Math.max(1e-6, +o.sd || 1), you = +o.you;
    var hasLine = o.line != null && isFinite(o.line);
    var narrow = (el.clientWidth || 600) < 520;
    var S = build(el, o.height || (narrow ? 270 : 300)), g = S.g, W = S.w, H = S.h;
    var ink = cssVar('--ink', '#14181d'), ink3 = cssVar('--ink-3', '#8b929c'), accent = cssVar('--accent', '#c4442b'), line = cssVar('--line', '#e2ded4');

    // ほかの人の点数（きれいな山になるよう、分位点から作る）
    var vals = [];
    for (var i = 0; i < n - 1; i++) vals.push(mean + sd * invNorm((i + .5) / (n - 1)));
    var lo = mean - 3.2 * sd, hi = mean + 3.2 * sd;
    lo = Math.min(lo, you - .4 * sd, hasLine ? o.line - .4 * sd : lo);
    hi = Math.max(hi, you + .4 * sd, hasLine ? +o.line + .4 * sd : hi);
    var bw = sd / 2.4, nb = Math.ceil((hi - lo) / bw);
    var bins = new Array(nb), dots = [];
    for (i = 0; i < nb; i++) bins[i] = 0;
    function binOf(v) { return Math.max(0, Math.min(nb - 1, Math.floor((v - lo) / bw))); }
    for (i = 0; i < vals.length; i++) { var bi = binOf(vals[i]); dots.push({ v: vals[i], b: bi, s: bins[bi]++ }); }
    var yb = binOf(you), youDot = { v: you, b: yb, s: bins[yb]++, you: true };
    var maxS = 0; for (i = 0; i < nb; i++) maxS = Math.max(maxS, bins[i]);

    var titleD = o.title || (n + '人の点数を並べると');
    var lay = headLayout(g, W, narrow, titleD, (o.rankText || function (rk, nn) { return nn + '人中 ' + rk + '位'; })(n, n));
    var left = 16, right = 16, top = 44 + lay.extra, base = H - 34;
    var pw = (W - left - right) / nb;
    var r = Math.max(1.5, Math.min(pw * .42, (base - top - 10) / maxS * .45));
    var stepY = Math.min(r * 2.15, (base - top - 10) / maxS);
    function X(v) { return left + (v - lo) / (hi - lo) * (W - left - right); }
    function bx(b) { return left + (b + .5) * pw; }
    function by(s) { return base - r - 1 - s * stepY; }

    // 落ちる順番：ほかの人はばらばらに、自分は最後
    var drop = dots.slice();
    for (i = drop.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), tmp = drop[i]; drop[i] = drop[j]; drop[j] = tmp; }
    var spread = 1800, fall = 520;
    drop.forEach(function (d, k) { d.t0 = k / drop.length * spread; });
    youDot.t0 = spread + 350;
    var total = youDot.t0 + fall + 900;

    var rank = 1; for (i = 0; i < vals.length; i++) if (vals[i] > you) rank++;
    var above = 0; if (hasLine) for (i = 0; i < vals.length; i++) if (vals[i] >= o.line) above++;
    var tick = o.tick || function (v) { return String(Math.round(v)); };
    var rankText = o.rankText || function (rk, nn) { return nn + '人中 ' + rk + '位'; };
    S.c.setAttribute('aria-label', (o.title || '') + '：' + rankText(rank, n));

    function drawDot(d, t) {
      var p = (t - d.t0) / fall;
      if (p < 0) return;
      var y1 = by(d.s), y0 = top - 10, y = p >= 1 ? y1 : y0 + (y1 - y0) * (p * p);
      var col = GRAY;
      if (hasLine && o.goodAbove !== false && d.v >= o.line) col = GOOD;
      if (d.you) col = GOLD;
      dot(g, bx(d.b), y, d.you ? r * 1.15 : r, col);
      if (d.you && p >= 1) {
        ring(g, bx(d.b), y, r + 4, accent);
        var pulse = (t - d.t0 - fall) / 900;
        if (pulse < 1) { g.globalAlpha = 1 - pulse; ring(g, bx(d.b), y, r + 4 + pulse * 18, GOLD); g.globalAlpha = 1; }
        label(g, 'あなた', bx(d.b), Math.max(top + 2, y - r - 13), accent);
      }
    }

    play(el, S, total, function (t) {
      g.clearRect(0, 0, W, H);
      // 軸
      g.strokeStyle = line; g.lineWidth = 1; g.beginPath(); g.moveTo(left, base + .5); g.lineTo(W - right, base + .5); g.stroke();
      g.fillStyle = ink3; g.font = font(11); g.textAlign = 'center'; g.textBaseline = 'middle';
      for (var s = -2; s <= 2; s++) { var tv = mean + s * sd, tx = X(tv); g.fillText(tick(tv), tx, base + 14); g.fillRect(tx, base, 1, 4); }
      // 合格ライン
      if (hasLine) {
        var lx = Math.round(X(o.line)) + .5;
        g.strokeStyle = GOOD; g.setLineDash([4, 4]); g.beginPath(); g.moveTo(lx, top + 4); g.lineTo(lx, base); g.stroke(); g.setLineDash([]);
        g.fillStyle = GOOD; g.font = font(11, true);
        var lt = o.lineLabel || '合格ライン', tw = g.measureText(lt).width;
        g.textAlign = lx + tw / 2 + 6 > W ? 'right' : lx - tw / 2 - 6 < 0 ? 'left' : 'center';
        g.fillText(lt, lx, top - 4);
      }
      // 見出し
      header(g, W, narrow, titleD, t >= youDot.t0 + fall ? [[rankText(rank, n), GOLD]] : [], lay);
      for (var k = 0; k < drop.length; k++) drawDot(drop[k], t);
      drawDot(youDot, t);
      S.cap.textContent = t >= youDot.t0 + fall ? (o.final ? o.final(rank, n, above) : rankText(rank, n)) : ' ';
    });
    S.btn.onclick = function () { distribution(el, o); };
  }

  /* 共通：格子の並べ方 */
  function gridLayout(n, W, top, ah) {
    var aw = W - 24;
    var cols = Math.max(1, Math.ceil(Math.sqrt(n * aw / ah))), rows = Math.ceil(n / cols);
    var cell = Math.min(aw / cols, ah / rows), r = Math.max(1.1, cell * .36);
    var ox = (W - cols * cell) / 2 + cell / 2, oy = top + (ah - rows * cell) / 2 + cell / 2;
    return { r: r, pos: function (k) { return [ox + (k % cols) * cell, oy + Math.floor(k / cols) * cell]; } };
  }
  /* 見出しの並べ方：長い題は文字を小さく、右の数字が入らなければ2行目へ（extra＝増える高さ） */
  function headLayout(g, W, narrow, left, sampleRight) {
    var fs = narrow ? 12 : 13; g.font = font(fs, true);
    while (g.measureText(left).width > W - 28 && fs > 10) { fs--; g.font = font(fs, true); }
    var rw = sampleRight ? g.measureText(sampleRight).width : 0;
    var two = !!sampleRight && g.measureText(left).width + rw + 16 > W - 28;
    return { fs: fs, two: two, extra: two ? 18 : 0 };
  }
  function header(g, W, narrow, left, rightParts, lay) { // rightParts: [[text,color],...]
    lay = lay || headLayout(g, W, narrow, left, rightParts.map(function (p) { return p[0]; }).join(''));
    g.textBaseline = 'middle'; g.textAlign = 'left'; g.font = font(lay.fs, true);
    g.fillStyle = cssVar('--ink', '#14181d'); g.fillText(left, 14, 22);
    var i, x;
    if (lay.two) {
      x = 14;
      for (i = 0; i < rightParts.length; i++) { g.fillStyle = rightParts[i][1]; g.fillText(rightParts[i][0], x, 40); x += g.measureText(rightParts[i][0]).width; }
    } else {
      g.textAlign = 'right'; x = W - 14;
      for (i = rightParts.length - 1; i >= 0; i--) { g.fillStyle = rightParts[i][1]; g.fillText(rightParts[i][0], x, 22); x -= g.measureText(rightParts[i][0]).width; }
    }
  }
  function niceStep(raw) {
    if (!(raw > 0)) return 1;
    var e = Math.pow(10, Math.floor(Math.log10(raw))), f = raw / e;
    return (f <= 1 ? 1 : f <= 2 ? 2 : f <= 5 ? 5 : 10) * e;
  }

  /* ===== のこりの玉（人生の残り・回数） ===== */
  function units(el, o) {
    var total = Math.max(1, Math.round(+o.total || 1)), used = Math.max(0, Math.min(total, Math.round(+o.used || 0)));
    var scale = Math.max(1, Math.ceil(total / 1500)), n = Math.ceil(total / scale), nu = Math.round(used / scale);
    var narrow = (el.clientWidth || 600) < 520;
    var S = build(el, o.height || (narrow ? 280 : 320)), g = S.g, W = S.w, H = S.h;
    var unit = o.unit || '回', accent = cssVar('--accent', '#c4442b'), ink3 = cssVar('--ink-3', '#8b929c');
    var titleU = o.title || '全部を玉で並べると';
    var lay = headLayout(g, W, narrow, titleU, (o.leftLabel || 'のこり') + ' ' + fmt(total) + unit + ' / ' + fmt(total) + unit);
    var top = (scale > 1 ? 54 : 44) + lay.extra, L = gridLayout(n, W, top, H - top - 14);
    var tIn = 900, tSweep = Math.max(900, Math.min(2600, nu * 6)), total_t = tIn + 300 + tSweep + 600;
    var left = total - used;
    S.c.setAttribute('aria-label', (o.title || '') + '：のこり ' + fmt(left) + unit + ' / ' + fmt(total) + unit);
    play(el, S, total_t, function (t) {
      g.clearRect(0, 0, W, H);
      var k = t < tIn + 300 ? 0 : Math.round(nu * easeInOut((t - tIn - 300) / tSweep));
      var shownLeft = Math.max(left, total - Math.round(k * scale));
      header(g, W, narrow, titleU, [[(o.leftLabel || 'のこり') + ' ' + fmt(shownLeft) + unit, GOLD], [' / ' + fmt(total) + unit, ink3]], lay);
      if (scale > 1) { g.textAlign = 'left'; g.font = font(11); g.fillStyle = ink3; g.fillText('● 1つ＝' + fmt(scale) + unit, 14, 40 + lay.extra); }
      for (var i = 0; i < n; i++) {
        var a = L.pos(i), appear = i / n * tIn;
        if (t < appear) continue;
        var rr = L.r * (t - appear < 200 ? (t - appear) / 200 : 1);
        var gone = i < k;
        dot(g, a[0], a[1], rr, gone ? GRAY : GOLD);
      }
      if (t >= total_t - 1 && nu > 0 && nu < n && o.now !== false) { var p = L.pos(nu); ring(g, p[0], p[1], L.r + 3.5, accent); label(g, 'いま', p[0], p[1] - L.r - 12 < top ? p[1] + L.r + 13 : p[1] - L.r - 12, accent); }
      S.cap.textContent = t >= total_t - 1 ? (o.final ? o.final(left, total) : 'のこり ' + fmt(left) + unit + '（全体の ' + (left / total * 100).toFixed(0) + '%）') : ' ';
    });
    S.btn.onclick = function () { units(el, o); };
  }

  /* ===== 積み上がる山（お金・物） ===== */
  function pile(el, o) {
    var bars = (o.bars || []).filter(function (b) { return b && isFinite(b.value); }).slice(0, 4);
    if (!bars.length) return;
    var narrow = (el.clientWidth || 600) < 520;
    var S = build(el, o.height || (narrow ? 300 : 340)), g = S.g, W = S.w, H = S.h;
    var ink = cssVar('--ink', '#14181d'), ink3 = cssVar('--ink-3', '#8b929c'), line = cssVar('--line', '#e2ded4');
    var COLORS = [GOLD, cssVar('--accent', '#c4442b'), '#2f6fb0', GOOD];
    var unit = o.unit || '円', fmtv = o.fmtv || function (v) { return fmt(v) + unit; };
    var maxV = 0; bars.forEach(function (b) { maxV = Math.max(maxV, Math.abs(b.value)); });
    var top = 58, base = H - 34, nb = bars.length;
    var colW = Math.min(150, (W - 40) / nb * .62), gap = (W - colW * nb) / (nb + 1);
    var across = 10, bw = colW / across;
    var rowsTarget = Math.max(4, Math.floor((base - top - 18) / (bw * .5)));
    var per = o.per || niceStep(maxV / (across * rowsTarget));
    var counts = bars.map(function (b) { return Math.ceil(Math.abs(b.value) / per - 1e-9); });
    var maxRows = Math.max(1, Math.ceil(Math.max.apply(null, counts) / across));
    var bh = Math.min(bw * 1.1, (base - top - 18) / maxRows);
    var dur = 2600, total = dur + 900;
    S.c.setAttribute('aria-label', (o.title || '') + '：' + bars.map(function (b) { return b.label + ' ' + fmtv(b.value); }).join('、'));
    play(el, S, total, function (t) {
      g.clearRect(0, 0, W, H);
      header(g, W, narrow, o.title || '積み上げると', []);
      g.textAlign = 'left'; g.font = font(11); g.fillStyle = ink3; g.fillText('■ 1つ＝' + fmtv(per), 14, 40);
      g.strokeStyle = line; g.lineWidth = 1; g.beginPath(); g.moveTo(12, base + .5); g.lineTo(W - 12, base + .5); g.stroke();
      var p = easeOut(t / dur);
      bars.forEach(function (b, bi) {
        var x0 = gap + bi * (colW + gap), cnt = counts[bi], show = Math.round(cnt * Math.min(1, t / dur));
        var col = b.color || COLORS[bi % COLORS.length];
        for (var i = 0; i < show; i++) {
          var cx = x0 + (i % across) * bw, ry = Math.floor(i / across), y1 = base - (ry + 1) * bh;
          var since = t - i / Math.max(1, cnt) * dur, drop = since < 160 ? (1 - since / 160) * 40 : 0;
          g.fillStyle = col; g.globalAlpha = .92;
          g.fillRect(cx + .6, y1 - drop + .6, bw - 1.2, bh - 1.2);
        }
        g.globalAlpha = 1;
        var topY = base - Math.ceil(show / across) * bh;
        g.textAlign = 'center'; g.textBaseline = 'middle';
        g.font = font(narrow ? 12 : 13, true); g.fillStyle = ink;
        g.fillText(fmtv(b.value * p), x0 + colW / 2, Math.max(top - 6, topY - 12));
        g.font = font(narrow ? 11 : 12, true); g.fillStyle = ink3;
        g.fillText(b.label, x0 + colW / 2, base + 16);
      });
      S.cap.textContent = t >= total - 1 ? (o.final ? o.final() : '') || ' ' : ' ';
    });
    S.btn.onclick = function () { pile(el, o); };
  }

  /* ===== AとBのレース（年ごとの線） ===== */
  function race(el, o) {
    var ser = (o.series || []).filter(function (s) { return s && s.values && s.values.length > 1; }).slice(0, 3);
    if (!ser.length) return;
    var N = ser[0].values.length;
    var narrow = (el.clientWidth || 600) < 520;
    var S = build(el, o.height || (narrow ? 280 : 320)), g = S.g, W = S.w, H = S.h;
    var ink = cssVar('--ink', '#14181d'), ink3 = cssVar('--ink-3', '#8b929c'), line = cssVar('--line', '#e2ded4');
    var COLORS = [cssVar('--accent', '#c4442b'), '#2f6fb0', GOLD];
    var fmtv = o.fmtv || function (v) { return fmt(v) + (o.unit || ''); };
    var xLabel = o.xLabel || function (i) { return String(i); };
    var lo = 0, hi = 0;
    ser.forEach(function (s) { s.values.forEach(function (v) { lo = Math.min(lo, v); hi = Math.max(hi, v); }); });
    if (hi === lo) hi = lo + 1;
    var top = 58, base = H - 30, left = 14, right = narrow ? 70 : 96;
    function X(i) { return left + i / (N - 1) * (W - left - right); }
    function Y(v) { return base - (v - lo) / (hi - lo) * (base - top); }
    var cross = -1;
    if (ser.length >= 2) for (var i = 1; i < N; i++) {
      var d0 = ser[0].values[i - 1] - ser[1].values[i - 1], d1 = ser[0].values[i] - ser[1].values[i];
      if (d0 !== 0 && (d0 < 0) !== (d1 < 0)) { cross = i; break; }
    }
    var dur = 3000, total = dur + 900;
    S.c.setAttribute('aria-label', (o.title || '') + '：' + ser.map(function (s) { return s.label + ' ' + fmtv(s.values[N - 1]); }).join('、'));
    play(el, S, total, function (t) {
      g.clearRect(0, 0, W, H);
      header(g, W, narrow, o.title || 'くらべると', []);
      // 凡例
      var lx = 14; g.font = font(11, true); g.textAlign = 'left';
      ser.forEach(function (s, si) { var c = s.color || COLORS[si]; g.fillStyle = c; g.fillRect(lx, 37, 14, 3); g.fillText(s.label, lx + 18, 39); lx += 26 + g.measureText(s.label).width; });
      // 軸
      g.strokeStyle = line; g.lineWidth = 1; g.beginPath(); g.moveTo(left, base + .5); g.lineTo(W - right, base + .5); g.stroke();
      g.fillStyle = ink3; g.font = font(11); g.textAlign = 'center';
      var stepI = Math.max(1, Math.ceil((N - 1) / (narrow ? 4 : 6)));
      for (var k = 0; k < N; k += stepI) g.fillText(xLabel(k), X(k), base + 14);
      var f = (N - 1) * easeInOut(t / dur), fi = Math.floor(f), fr = f - fi;
      ser.forEach(function (s, si) {
        var c = s.color || COLORS[si], v = s.values;
        g.strokeStyle = c; g.lineWidth = 2.5; g.lineJoin = 'round'; g.beginPath();
        for (var j = 0; j <= fi; j++) { if (j) g.lineTo(X(j), Y(v[j])); else g.moveTo(X(0), Y(v[0])); }
        var cur = fi < N - 1 ? v[fi] + (v[fi + 1] - v[fi]) * fr : v[N - 1];
        g.lineTo(X(f), Y(cur)); g.stroke();
        dot(g, X(f), Y(cur), 4.5, c);
        g.font = font(narrow ? 11 : 12, true); g.fillStyle = c; g.textAlign = 'left'; g.textBaseline = 'middle';
        g.fillText(fmtv(cur), X(f) + 8, Y(cur) + (si === 0 ? -8 : 8));
      });
      if (cross > 0 && f >= cross) {
        var cx = X(cross), cy = Y((ser[0].values[cross] + ser[1].values[cross]) / 2);
        g.fillStyle = GOLD; g.font = font(18, true); g.textAlign = 'center'; g.fillText('★', cx, cy);
        var ct = o.crossLabel ? o.crossLabel(cross) : xLabel(cross) + 'で逆転';
        g.font = font(11, true); var cw = g.measureText(ct).width;
        var clx = Math.max(left + cw / 2 + 2, Math.min(cx, W - right - cw / 2 - 6));
        label(g, ct, clx, cy - 18 < top + 14 ? cy + 20 : cy - 18, ink);
      }
      S.cap.textContent = t >= total - 1 ? (o.final ? o.final(cross) : '') || ' ' : ' ';
    });
    S.btn.onclick = function () { race(el, o); };
  }

  window.Crowd = { lottery: lottery, distribution: distribution, units: units, pile: pile, race: race };
})();
