/* =========================================================
   シミュラボ リクエスト投票API（Vercel Serverless Function 版）
   - GET  /api/vote?req=<id>    → { req, count }      （現在の票数）
   - POST /api/vote  body:{req} → { req, count }      （+1して返す）

   ■ 使い方（公開時）
   1. Vercel + Vercel KV（share.js / request.js と同じ）
   2. `npm i @vercel/kv`
   3. assets/vote.js の  const API = ''  を  '/api/vote'  に変更
   ※ 1人1票の厳密な担保はサーバー側だけでは難しい（同一ブラウザは
     localStorageでガード）。本気でやるならIP単位の制限やログイン導入を検討。
   ========================================================= */
import { kv } from '@vercel/kv';

// 投票を受け付ける案ID（不正キー防止のホワイトリスト。候補追加時に更新）
const ALLOW = new Set([
  'req-life-calendar', 'req-turing', 'req-tabemono', 'req-chintai',
  'req-sync', 'req-shugi', 'req-this-year', 'req-edo'
]);

export default async function handler(req, res) {
  const id = (req.method === 'POST' ? req.body?.req : req.query?.req) || '';
  if (!ALLOW.has(id)) return res.status(400).json({ error: 'unknown req' });

  const key = `vote:${id}`;
  try {
    let count;
    if (req.method === 'POST') count = await kv.incr(key);
    else count = (await kv.get(key)) || 0;
    res.setHeader('Cache-Control', 'no-store');
    return res.status(200).json({ req: id, count });
  } catch (e) {
    return res.status(500).json({ error: 'kv error' });
  }
}
