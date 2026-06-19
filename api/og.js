/* =========================================================
   シミュラボ 動的OGP画像（Vercel Edge / @vercel/og 版）※任意・公開後の拡張
   - /api/og?title=...&label=...&value=...&cat=...
     → リクエストごとにOGP画像(1200x630)を生成して返す。
   - これを使うと「結果の数字入りOGP」をシェアごとに出せる。
     例: 各シミュのシェアURLに ?title=口コミ波及&value=%2B147人 を付け、
         そのページの og:image を /api/og?... にする（動的に差し替え）。

   ■ 使い方（公開後）
   1. `npm i @vercel/og`
   2. このファイルを api/og.js として配置（Edge Runtime）
   3. 動的に出したいページで og:image を /api/og?title=...&value=... に
   ※ 静的な ogp/*.png（gen_images.pyで生成）だけでも十分運用可能。
     動的が必要になったときの拡張用テンプレート。
   ========================================================= */
import { ImageResponse } from '@vercel/og';

export const config = { runtime: 'edge' };

export default function handler(req) {
  const { searchParams } = new URL(req.url);
  const title = (searchParams.get('title') || 'シミュラボ').slice(0, 40);
  const label = (searchParams.get('label') || '').slice(0, 30);
  const value = (searchParams.get('value') || '').slice(0, 24);
  const cat   = (searchParams.get('cat')   || 'シミュレーター').slice(0, 20);

  return new ImageResponse(
    {
      type: 'div',
      props: {
        style: {
          width: '100%', height: '100%', display: 'flex', flexDirection: 'column',
          justifyContent: 'space-between', padding: '64px',
          background: 'linear-gradient(135deg, #0fb5c4, #6366f1)', color: '#fff',
          fontFamily: 'sans-serif'
        },
        children: [
          { type: 'div', props: { style: { fontSize: 30, fontWeight: 700 }, children: '🧪 シミュラボ' } },
          { type: 'div', props: { style: { display: 'flex', flexDirection: 'column', gap: '10px' }, children: [
            { type: 'div', props: { style: { fontSize: 26, opacity: .9 }, children: cat } },
            { type: 'div', props: { style: { fontSize: 60, fontWeight: 800, lineHeight: 1.2 }, children: title } },
            value ? { type: 'div', props: { style: { fontSize: 48, fontWeight: 800 }, children: `${label} ${value}` } } : null
          ] } },
          { type: 'div', props: { style: { fontSize: 26, opacity: .9 }, children: '触って分かるシミュレーター集' } }
        ]
      }
    },
    { width: 1200, height: 630 }
  );
}
