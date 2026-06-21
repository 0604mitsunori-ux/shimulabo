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
  'jikkou-jikyu', 'fukugyo-zei', 'shouyo-tedori', 'tango', 'shogakukin', 'benkyo-target',
  'kaiten', 'line-cv', 'zaiko', 'chochiku-mokuhyo', 'reborisk', 'fukuri72',
  'taishokukin', 'nenkin-mikomi', 'zaitaku-setsuyaku', 'naishin', 'juken-hiyou', 'natsuyasumi',
  'kosodate-hiyou', 'kodomo-jikan', 'ikukyu', 'jidou-teate', 'hoiku-youchi', 'omutsu', 'shinchou', 'nezukashi', 'gakushi', 'okozukai', 'pet-age', 'pet-hiyou', 'pet-jikan', 'pet-hoken', 'sanpo', 'neko-nemuri', 'food-ryou', 'tatou', 'pet-taiju', 'pet-gohan-life',
  'buzz', 'kakaku-matsu', 'naming-buzz', 'gacha', 'kakuyasu-sim', 'jihanki', 'kinenbi', 'enkyori', 'aishou-seiza',
  'seo-ctr', 'seo-kachi', 'zero-click', 'ai-inyou', 'repeat-rieki',
  'bmi', 'kiso-taisha', 'tainai-nenrei', 'suibun', 'taishibo', 'hosu-karori', 'sake-karori', 'suimin-cycle', 'suwari', 'mizu-body',
  'tanjyobi-uranai', 'zensei', 'kotoshi-unsei', 'namae-uranai', 'soul-color', 'doubutsu-uranai', 'ketsueki-aishou', 'lucky-today', 'kyusei', 'tarot-today',
  'nenpi-gas', 'ev-vs-gas', 'kuruma-yosan', 'kousoku-shita', 'shaken-tsumitate', 'souko-kyori', 'chuko-nedan', 'drive-yosan', 'tsukin-car', 'kuruma-hoyuu',
  'ryohi', 'mile-tamaru', 'jisa-boke', 'kaigai-iju', 'tabi-tsumitate', 'lcc-shinkansen', 'gasolin-doko', 'onsen-seiha', 'sekai-isshu', 'theme-park',
  'yachin-tekisei', 'hikkoshi-hiyou', 'chintai-mochiie', 'denki-setsuyaku', 'hitorigurashi', 'kounetsu', 'net-hikari', 'kaji-jikan', 'kagu-tsumitate', 'tatami-henkan',
  'ramen-roudou', 'gaishoku-jisui', 'issho-tabemono', 'conveni-super', 'karori-undou', 'cafe-nenkan', 'obento-lunch', 'tabehoudai', 'uber-jisui', 'nomikai-nenkan',
  'lorenz', 'pendulum-wave', 'solar-system', 'gravity', 'fireworks', 'fractal-tree', 'mandelbrot', 'starfield', 'gears', 'dna', 'reaction-test', 'typing-test', 'memory-test', 'spirograph', 'ripple',
  'datsumo-sougaku', 'cosme-nenkan', 'fuku-shogai', 'biyoin-nenkan', 'diet-mokuhyou', 'nail-matsu', 'hada-nenrei', 'wardrobe', 'kami-nobiru', 'depacos',
  'marathon-yosoku', 'run-pace', 'kintore-1rm', 'tairyoku-nenrei', 'shomou-undou', 'golf-handi', 'swim-pace', 'jitensha', 'taishibo-otoshi', 'shinpaku-zone',
  'oshi-nenkan', 'live-ensei', 'subsc-motodori', 'tsumige', 'eiga-shougai', 'manga-otomegai', 'oshi-jikan', 'ticket-tousen', 'live-sankai', 'goods-shuunou',
  'stress-do', 'seikaku-type', 'moeotsuki-do', 'jiko-koutei', 'komyu-type', 'kachikan', 'chrono', 'ketsudan', 'resilience', 'kokoro-yoyuu',
  'point-katsu', 'atm-tesuuryo', 'tsumitate-fukuri', 'jinsei-calendar', 'seimei-suimin', 'sumaho-shogai', 'cvr-uriage', 'follower-kachi', 'email-cv', 'deto-yosan', 'kekkonshiki-hiyou', 'birthday-aishou', 'genka-rieki', 'kyakutanka-up', 'kaiin-monthly', 'ideco-setsuzei', 'haitou-shisan', 'souzoku-zei', 'nenshu-tedori', 'shoushin-sa', 'fukugyo-mokuhyou', 'juku-sougaku', 'gakureki-chingin', 'pomodoro', 'nyuuji-hiyou', 'kodomo-shokuhi', 'narai-goto', 'pet-iryou', 'pet-toilet', 'pet-trim', 'tabako-cost', 'kakuzato', 'kaidan', 'birthstone', 'yesno-uranai', 'biorhythm', 'kuruma-shogai', 'jidousha-zei', 'taiya-cost', 'shogai-ryokou', 'gaika-ryougae', 'camp-hiyou', 'koushinryo', 'kaden-denkidai', 'mizu-setsuyaku', 'shokuhi-tekisei', 'osake-shogai', 'okashi-nenkan', 'kutsu-shogai', 'gym-motodori', 'supple-nenkan', 'yakyu-kyusoku', 'vertical-jump', 'undou-shukan', 'oshi-anniv', 'cosplay-hiyou', 'hakooshi', 'motivation-type', 'kansha-do', 'shuuchu-type', 'galton', 'lissajous', 'magnet', 'kaleido', 'aim-trainer', 'color-test',
  'seiseki-hyotei', 'test-toukei', 'naishin-keisan', 'shoken-jitan', 'saiten-jikan', 'sekigae-pattern', 'class-kumiawase', 'han-wake', 'shusseki-ritsu', 'print-cost', 'wasure-kyokusen', 'hensachi', 'zangyo-kyoin', 'tairyoku-hyouka', 'kyushoku-shukin',
  'hyoutei-heikin', 'gpa', 'jugyou-jisuu', 'kekka-tani', 'kyoin-kyuryo', 'kyosai-bairitsu', 'gakkyu-hensei',
  'shukatsu-sougaku', 'ohaka-hiyou', 'sougi-hiyou', 'kaigo-hiyou', 'nenkin-kurisage', 'seizen-zoyo', 'kougaku-ryoyo', 'ending-do', 'kenkou-jumyo', 'isan-bunkatsu',
  'juuminzei', 'shotokuzei', 'iryouhi-koujo', 'nenmatsu-chousei', 'fuyou-koujo', 'kabu-zei', 'shouhizei', 'kojin-jigyo', 'zoyozei', 'taishokukin-zei',
  'heigan-goukaku', 'hitsuyo-hensachi', 'juken-sougaku', 'juken-jikan', 'chugaku-juken', 'moshi-hantei', 'goukaku-saiteiten', 'nyushi-shindan', 'yobikou-hiyou', 'shigan-bairitsu',
  'kotoshi-pct', 'otoshidama', 'bonus-haibun', 'christmas-yosan', 'nengajo-cost', 'kisei-hiyou', 'goshugi-souba', 'hanami-yosan', 'valentine-yosan', 'gyouji-countdown'
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
