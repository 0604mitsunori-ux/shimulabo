/* =========================================================
   シミュラボ リクエスト受付API（Vercel Serverless Function 版）
   - POST /api/request  body:{ idea, genre, why, nick, email }
        → サーバー(KV)にリクエストを蓄積。 { ok:true } を返す。
   - GET  /api/request?key=<ADMIN_KEY>
        → 蓄積されたリクエスト一覧を返す（管理用・要 ADMIN_KEY）。

   ■ 使い方（公開時）
   1. Vercel + Vercel KV を用意（share.js と同じ）
   2. `npm i @vercel/kv`
   3. 環境変数 ADMIN_KEY を任意の文字列で設定（一覧取得の保護用）
   4. request/index.html のフォーム送信を mailto から
      fetch('/api/request', {method:'POST', body: JSON.stringify(...)}) に切替
   これで「リクエストがサーバーに溜まる」状態になる。
   さらに投票機能を足せば、人気リクエストボードにも発展できる。
   ========================================================= */
import { kv } from '@vercel/kv';

const LIST = 'requests';

export default async function handler(req, res) {
  // 管理用：一覧取得
  if (req.method === 'GET') {
    if ((req.query?.key || '') !== process.env.ADMIN_KEY) {
      return res.status(401).json({ error: 'unauthorized' });
    }
    const items = await kv.lrange(LIST, 0, -1);
    return res.status(200).json({ count: items.length, items: items.map(s => JSON.parse(s)) });
  }

  // 投稿：リクエスト追加
  if (req.method === 'POST') {
    const b = req.body || {};
    const idea = (b.idea || '').toString().slice(0, 1000).trim();
    if (!idea) return res.status(400).json({ error: 'idea required' });

    const rec = {
      idea,
      genre: (b.genre || '').toString().slice(0, 50),
      why:   (b.why   || '').toString().slice(0, 1000),
      nick:  (b.nick  || '').toString().slice(0, 50),
      email: (b.email || '').toString().slice(0, 120),
      ua:    (req.headers['user-agent'] || '').slice(0, 200)
      // 受信日時はサーバー側で付与する（KVの追加順でも代用可）
    };
    await kv.rpush(LIST, JSON.stringify(rec));
    return res.status(200).json({ ok: true });
  }

  return res.status(405).json({ error: 'method not allowed' });
}
