/* =========================================================
   シミュラボ リクエスト投票カウンター（vote.js）
   - リクエスト案に対する 👍 投票を数える。
   - 1ブラウザにつき同じ案へは1票（localStorageでガード）。

   ▼保存先（API定数で切替）
     API = ''           … localStorage（ブラウザごと・開発/単体確認用）
     API = '/api/vote'  … サーバー(KV)で全ユーザー横断の本物の集計
   公開時は下の API を実エンドポイントに変えるだけ。
   ========================================================= */
(function () {
  const API = '';        // ★公開時にここを '/api/vote' へ変更

  const vkey = (id) => 'simulab:vote:' + id;
  const dkey = (id) => 'simulab:voted:' + id;
  const lget = (id) => (parseInt(localStorage.getItem(vkey(id)), 10) || 0);
  function lvote(id) {
    const n = lget(id) + 1;
    try { localStorage.setItem(vkey(id), n); localStorage.setItem(dkey(id), '1'); } catch (e) {}
    return n;
  }

  async function get(id) {
    if (API) { try { const r = await fetch(`${API}?req=${encodeURIComponent(id)}`); const j = await r.json(); return j.count | 0; } catch (e) {} }
    return lget(id);
  }
  async function vote(id) {
    if (API) {
      try {
        const r = await fetch(API, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ req: id }) });
        const j = await r.json(); try { localStorage.setItem(dkey(id), '1'); } catch (e) {} return j.count | 0;
      } catch (e) {}
    }
    return lvote(id);
  }
  const hasVoted = (id) => localStorage.getItem(dkey(id)) === '1';
  async function counts(ids) { const o = {}; await Promise.all(ids.map(async (id) => { o[id] = await get(id); })); return o; }

  window.Vote = { API, get, vote, hasVoted, counts };
})();
