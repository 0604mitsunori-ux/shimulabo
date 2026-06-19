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
      show(await get(simId));
      shareBtnIds.forEach((bid) => {
        const b = document.getElementById(bid);
        if (b) b.addEventListener('click', async () => show(await inc(simId)));
      });
    },

    /* ランキング用：複数シミュのカウントをまとめて取得 */
    async counts(ids) {
      const o = {};
      await Promise.all(ids.map(async (id) => { o[id] = await get(id); }));
      return o;
    }
  };
})();
