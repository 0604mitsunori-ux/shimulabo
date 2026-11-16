  /* ===== 人気ランキング＋シミュレーション回数（本物のデータ） =====
     assets/ranking.json は scripts/build_ranking.py が GA4 の閲覧数から毎朝作る。
     読めなかったときだけ、上の SIMS（運営のおすすめ順）で表示する。 */
  (async function renderRanking(){
    const list = document.getElementById('rankList');
    const more = document.getElementById('rankMore');
    const tabs = document.getElementById('rankTabs');
    const note = document.getElementById('rankNote');
    const esc = (t) => String(t).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
    const fmt = (n) => Number(n || 0).toLocaleString('ja-JP');
    const reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

    function rowHtml(s, rank, right, ratio) {
      const topClass = rank <= 3 ? ' top' + rank : '';
      const badge = rank === 1 ? '🥇' : rank === 2 ? '🥈' : rank === 3 ? '🥉' : rank;
      return `<a class="rank-row${topClass}" href="${esc(s.href)}">
        <span class="rank-badge">${badge}</span>
        <span class="rank-emoji">${s.emoji}</span>
        <span class="rank-main"><span class="t">${esc(s.title)}</span><span class="c">${esc(s.cat)}</span>
          <span class="rank-bar"><span class="fill" style="width:${Math.max(3, Math.round(ratio * 100))}%"></span></span></span>
        <span class="rank-stat">${right}</span>
        <span class="rank-arrow">›</span>
      </a>`;
    }

    let data = null;
    try {
      const r = await fetch('assets/ranking.json', { cache: 'no-cache' });
      if (r.ok) data = await r.json();
    } catch (e) {}

    // ---- 読めなかったとき：おすすめ順（従来の SIMS） ----
    if (!data || !data.rankings || !(data.rankings.week || []).length) {
      document.getElementById('rankTitle').textContent = '🏆 おすすめのシミュレーション';
      note.textContent = '運営のおすすめ順';
      const top = SIMS.slice().sort((a, b) => b.score - a.score).slice(0, 5);
      list.innerHTML = top.map((s, i) => rowHtml(s, i + 1, '', s.score / top[0].score)).join('');
      return;
    }

    // ---- シミュレーション回数カウンター ----
    const pc = document.getElementById('playCounter');
    pc.hidden = false;
    document.getElementById('pcWeek').textContent = fmt(data.week);
    document.getElementById('pcYday').textContent = fmt(data.yesterday);
    if (data.prevWeek > 0) {
      const diff = Math.round((data.week / data.prevWeek - 1) * 100);
      const tr = document.getElementById('pcTrend');
      tr.textContent = '先週より ' + (diff >= 0 ? '+' : '') + diff + '%';
      tr.classList.add(diff >= 0 ? 'up' : 'down');
    }
    document.querySelectorAll('.ms-plays').forEach(el => { el.hidden = false; });
    document.getElementById('msTotal').textContent = fmt(data.total);

    const totalEl = document.getElementById('pcTotal');
    totalEl.textContent = fmt(data.total);   // アニメが動かない環境でも正しい数字を出しておく
    const countUp = () => {
      if (reduce) { totalEl.textContent = fmt(data.total); return; }
      const t0 = performance.now(), dur = 1400, to = data.total;
      const step = (t) => {
        const k = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - k, 3);
        totalEl.textContent = fmt(Math.round(to * e));
        if (k < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    };
    if ('IntersectionObserver' in window) {
      const io = new IntersectionObserver((es) => {
        if (es.some(x => x.isIntersecting)) { io.disconnect(); countUp(); }
      }, { threshold: .4 });
      io.observe(pc);
    } else countUp();

    // ---- 出典・更新時刻 ----
    const up = new Date(data.updated);
    const src = document.getElementById('rankSrc');
    src.hidden = false;
    src.textContent = `※回数＝シミュのページが開かれた回数（Googleアナリティクスで集計）。${up.getMonth() + 1}/${up.getDate()} ${String(up.getHours()).padStart(2, '0')}:${String(up.getMinutes()).padStart(2, '0')} 更新・毎朝更新します`;

    // ---- タブ（今週／急上昇／今月／全期間） ----
    const LABEL = { week: '直近7日の回数で集計', rising: '先週より増えた回数の順', month: '直近30日の回数で集計', all: '公開からの累計で集計' };
    let cur = 'week', open = false;
    function stat(r, i) {
      let h = `<span class="rank-num"><b>${fmt(r.views)}</b>回</span>`;
      if (cur === 'rising') return h + `<span class="rank-mv up" title="先週 ${fmt(r.prevViews)}回">+${fmt(r.up)}</span>`;
      if (cur !== 'week') return h;
      if (!r.prev) return h + '<span class="rank-mv new" title="先週はランク外">NEW</span>';
      const d = r.prev - (i + 1);
      if (d > 0) return h + `<span class="rank-mv up" title="先週${r.prev}位">▲${d}</span>`;
      if (d < 0) return h + `<span class="rank-mv down" title="先週${r.prev}位">▼${-d}</span>`;
      return h + '<span class="rank-mv same" title="先週と同じ順位">―</span>';
    }
    function draw() {
      const rows = data.rankings[cur] || [];
      const max = Math.max(1, ...rows.map(r => r.views));
      const shown = open ? rows : rows.slice(0, 5);
      list.innerHTML = shown.length
        ? shown.map((r, i) => rowHtml({ href: 'sims/' + r.id + '/', emoji: r.emoji, title: r.title, cat: r.cat }, i + 1, stat(r, i), r.views / max)).join('')
        : '<p class="rank-empty">まだデータがありません</p>';
      more.hidden = rows.length <= 5;
      more.textContent = open ? '5位までに戻す' : `6〜${rows.length}位も見る`;
      more.setAttribute('aria-expanded', open ? 'true' : 'false');
      note.textContent = LABEL[cur];
    }
    tabs.hidden = false;
    tabs.addEventListener('click', (e) => {
      const b = e.target.closest('button[data-k]'); if (!b) return;
      cur = b.dataset.k; open = false;
      tabs.querySelectorAll('button').forEach(x => x.setAttribute('aria-selected', x === b ? 'true' : 'false'));
      draw();
    });
    tabs.addEventListener('keydown', (e) => {
      if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
      const bs = [...tabs.querySelectorAll('button')], i = bs.findIndex(x => x.dataset.k === cur);
      const n = bs[(i + (e.key === 'ArrowRight' ? 1 : bs.length - 1)) % bs.length];
      n.focus(); n.click();
    });
    more.addEventListener('click', () => { open = !open; draw(); });
    draw();
  })();
