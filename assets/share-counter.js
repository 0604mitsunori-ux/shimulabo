/* =========================================================
   シミュラボ 拡散カウンター（share-counter.js）
   - シェアボタンが押された回数を数え、一定回数を超えたら
     「🔥 ◯回シェアされました」を表示する。
   - ⚠️ この数値は「当サイトのシェアボタンが押された回数」であり、
        実際の投稿数や第三者の再拡散数ではない（話題度の目安）。

   ▼データの保存先（API定数で切替）
     API = ''            … localStorage（ブラウザごと・開発/単体確認用）
     API = '/api/share'  … サーバー(KV)で全ユーザー横断の本物の集計
   公開時は下の API を実エンドポイントに変えるだけ。
   ========================================================= */
(function () {
  const API = '';        // ★公開時にここを '/api/share' 等へ変更
  const THRESHOLD = 30;  // この回数以上で一般公開表示

  const lkey = (id) => 'simulab:share:' + id;
  const localGet = (id) => (parseInt(localStorage.getItem(lkey(id)), 10) || 0);
  const localInc = (id) => {
    const n = localGet(id) + 1;
    try { localStorage.setItem(lkey(id), n); } catch (e) {}
    return n;
  };

  async function get(id) {
    if (API) {
      try { const r = await fetch(`${API}?sim=${encodeURIComponent(id)}`); const j = await r.json(); return j.count | 0; }
      catch (e) {}
    }
    return localGet(id);
  }
  async function inc(id) {
    if (API) {
      try {
        const r = await fetch(API, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ sim: id }) });
        const j = await r.json(); return j.count | 0;
      } catch (e) {}
    }
    return localInc(id);
  }
  const label = (n) => `🔥 ${n.toLocaleString()}回シェアされました`;

  window.ShareCounter = {
    THRESHOLD, get, inc,

    /* シミュページ用：シェアボタンに増分を付け、しきい値超えでバッジ表示 */
    async initSim(opts) {
      const { simId, badgeEl, shareBtnIds = [] } = opts;
      const show = (n) => {
        if (!badgeEl) return;
        if (n >= THRESHOLD) { badgeEl.textContent = label(n); badgeEl.style.display = ''; }
        else { badgeEl.style.display = 'none'; }
      };
      /* GA4 に「share」イベントを送る（2026-11-18〜。GA4の推奨イベント：method / content_type / item_id） */
      const track = (method) => {
        try { if (typeof window.gtag === 'function') window.gtag('event', 'share', { method, content_type: 'sim', item_id: simId }); } catch (e) {}
      };
      shareBtnIds.forEach((bid) => {
        const b = document.getElementById(bid);
        if (b) b.addEventListener('click', async () => { track('x'); show(await inc(simId)); });
      });
      const cp = document.getElementById('copyBtn');
      if (cp && shareBtnIds.indexOf('copyBtn') < 0) cp.addEventListener('click', () => track('copy'));
      show(await get(simId));
    },

    /* ランキング用：複数シミュのカウントをまとめて取得 */
    async counts(ids) {
      const o = {};
      await Promise.all(ids.map(async (id) => { o[id] = await get(id); }));
      return o;
    }
  };

  /* ===== 各シミュページ：「これまでに◯回シミュレーションされました」 =====
     assets/sim-counts.json（scripts/build_ranking.py が GA4 から毎朝作る）を読み、
     タイトル下の説明文の直後に表示する。10回未満のページは出さない。 */

  /* ===== 理科の授業向けページ：学校・教材会社の方への帯（2026-11-19） ===== */
  (function () {
    const run = () => {
      const bc = document.querySelector('.breadcrumb a[href$="rika/"]');
      if (!bc || document.getElementById('kyBand')) return;
      const main = document.querySelector('main'); if (!main) return;
      const href = bc.getAttribute('href').replace(/rika\/$/, 'kyouiku/');
      const el = document.createElement('div');
      el.id = 'kyBand';
      el.style.cssText = 'margin:28px 0 8px;padding:16px 18px;border:1px solid var(--line,#e2ded4);border-left:5px solid var(--accent,#c4442b);border-radius:14px;background:var(--card,#fff);font-size:14px;line-height:1.75;';
      el.innerHTML = '<b>🏫 学校・教材会社の方へ</b><br>このシミュレーションは授業で無料で使えます。教材やアプリへの組み込み、単元に合わせた新しいシミュレーションの制作も承ります。 ' +
        '<a href="' + href + '" style="font-weight:800;white-space:nowrap;">くわしく見る →</a>';
      main.appendChild(el);
      el.querySelector('a').addEventListener('click', () => { try { gtag('event', 'kyouiku_band_click', { item_id: location.pathname }); } catch (e) {} });
    };
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run); else run();
  })();

  const me = document.currentScript && document.currentScript.src;
  const m = location.pathname.match(/\/sims\/([a-z0-9][a-z0-9-]*)\//);
  if (!me || !m) return;
  const simId = m[1];
  const isEn = /^\/en\//.test(location.pathname);
  const show = (rec) => {
    if (!rec || rec[0] < 10 || document.getElementById('playPill')) return;
    const h1 = document.querySelector('main h1, h1');
    if (!h1) return;
    const anchor = (h1.nextElementSibling && h1.nextElementSibling.matches('p.lead')) ? h1.nextElementSibling : h1;
    const n = rec[0].toLocaleString(isEn ? 'en-US' : 'ja-JP');
    const rk = rec[1] > 0 && rec[1] <= 10;
    const el = document.createElement('div');
    el.id = 'playPill';
    el.className = 'play-pill';
    el.innerHTML = isEn
      ? `👀 Played <b>${n}</b> times${rk ? ` · <span class="rk">#${rec[1]} this week</span>` : ''}`
      : `👀 これまでに <b>${n}</b> 回 シミュレーションされました${rk ? ` ・ <span class="rk">今週 ${rec[1]}位</span>` : ''}`;
    anchor.insertAdjacentElement('afterend', el);
  };
  const run = () => fetch(new URL('sim-counts.json', me).href, { cache: 'no-cache' })
    .then((r) => r.ok ? r.json() : null)
    .then((j) => { if (j && j.c) show(j.c[simId]); })
    .catch(() => {});
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', run);
  else run();
})();

/* タイトル下の YouTube 案内（assets/yt-promo.js を読み込む。中身は scripts/build_yt_promo.py が作る）2026-11-26 */
(function () {
  try {
    var me = document.currentScript || document.querySelector('script[src*="assets/share-counter.js"]');
    if (!me || !me.src) return;
    var s = document.createElement('script');
    s.src = me.src.replace(/share-counter\.js.*$/, 'yt-promo.js?v=1'); s.async = true;
    document.head.appendChild(s);
  } catch (e) {}
})();
