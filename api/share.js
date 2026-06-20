/* =========================================================
   シミュラボ 拡散カウンターAPI（Vercel Serverless Function 版）
   - GET  /api/share?sim=<id>   → { sim, count }      （現在値を返す）
   - POST /api/share  body:{sim} → { sim, count }      （+1して返す）

   ■ 使い方（公開時）
   1. Vercel にこのフォルダごとデプロイ
   2. Vercel KV（または Upstash Redis）をプロジェクトに追加
      → 環境変数 KV_REST_API_URL / KV_REST_API_TOKEN が自動で入る
   3. `npm i @vercel/kv` を依存に追加
   4. assets/share-counter.js の  const API = ''  を  '/api/share'  に変更
   これだけで「全ユーザー横断の本物のシェア数」になる。

   ■ 他社サービスの場合
   - Netlify Functions / Cloudflare Workers でも、KVに INCR するだけで同等。
   - 保存先キーは share:<sim> 。集計の中身は単純なカウンタ。
   ========================================================= */
import { kv } from '@vercel/kv';

// 受け付けるシミュID（不正キーでKVを汚さないためのホワイトリスト）
const ALLOW = new Set([
  'kaigi-cost', 'jutai', 'scroll-distance', 'machi-jikan',
  'catchcopy', 'influencer-soroban', 'kuchikomi-hakyu',
  'subsc', 'caffeine', 'sleep-debt', 'warikan', 'takarakuji',
  'oyako', 'infure', 'if-company', 'nidone', 'chiritsumo', 'shutten',
  'tenshoku', 'fire', 'kyuryobi', 'coffee-life', 'yoi', 'taiju',
  'unmei', 'mental-age', 'isekai', 'neage',
  'konkatsu-match', 'konkatsu-jouken', 'konkatsu-type',
  'kokuhaku', 'ryomoi', 'aisho-name', 'same-class', 'moteki',
  'life', 'forest-fire', 'schelling', 'sandpile', 'boids',
  'double-pendulum', 'wave', 'diffusion', 'turing', 'sync',
  'ad-roas', 'ltv', 'coupon', 'chirashi-web',
  'jutaku-loan', 'kuriage', 'hosho', 'rougo',
  'zangyo', 'yukyu', 'freelance', 'tsukin',
  'goukaku', 'benkyo-time', 'gakuhi', 'bukatsu',
  'bep', 'noshow', 'jinkenhi', 'nisa', 'kuruma-iji', 'furusato',
  'jikkou-jikyu', 'fukugyo-zei', 'shouyo-tedori', 'tango', 'shogakukin', 'benkyo-target'
]);

export default async function handler(req, res) {
  const sim = (req.method === 'POST' ? req.body?.sim : req.query?.sim) || '';
  if (!ALLOW.has(sim)) {
    return res.status(400).json({ error: 'unknown sim' });
  }
  const key = `share:${sim}`;
  try {
    let count;
    if (req.method === 'POST') {
      count = await kv.incr(key);          // +1（アトミック）
    } else {
      count = (await kv.get(key)) || 0;    // 現在値
    }
    res.setHeader('Cache-Control', 'no-store');
    return res.status(200).json({ sim, count });
  } catch (e) {
    return res.status(500).json({ error: 'kv error' });
  }
}
