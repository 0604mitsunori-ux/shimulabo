# シミュラボ（shimulabo.com）公開・運用マニュアル

触って分かるシミュレーター集。静的サイト（HTML/CSS/JS）＋ Vercel サーバーレス関数。

---

## 0. 構成ざっくり

```
シミュラボ/
├── index.html              トップ（ランキング・カテゴリ・ギャラリー）
├── sims/<id>/index.html    各シミュレーター（7本）
├── contact/ request/ board/ terms/ privacy/   サブページ
├── assets/                 共通CSS・JS（share-counter.js / vote.js）
├── ogp/                    OGP画像（PNG・gen_images.pyで生成）
├── api/                    サーバーレス関数（share/vote/request/og）※KV利用
├── sitemap.xml / robots.txt / favicon類
├── scripts/                ビルド用Python（※公開には含めない）
└── package.json            api/ の依存（@vercel/kv, @vercel/og）
```

ローカル確認: `python -m http.server 8791` をこのフォルダで実行 → http://localhost:8791/

---

## 1. デプロイ（Vercel・無料）

### 方法A：GitHub経由（おすすめ・自動再デプロイ）
1. GitHubで空リポジトリを作成（例: `shimulabo`）
2. このフォルダをpush
   ```bash
   git init
   git add .
   git commit -m "シミュラボ 初回公開"
   git branch -M main
   git remote add origin https://github.com/<あなた>/shimulabo.git
   git push -u origin main
   ```
3. [vercel.com](https://vercel.com) にGitHubでログイン → 「Add New Project」→ このリポジトリを選択
4. Framework Preset = **Other**（静的サイト）。そのまま **Deploy**
5. 数十秒で `https://shimulabo.vercel.app` が公開される

> 以降は `git push` するたびに自動で再デプロイされる。

### 方法B：Vercel CLI（GitHub不要）
```bash
npm i -g vercel
cd シミュラボ
vercel          # 初回。質問はだいたいEnterでOK
vercel --prod   # 本番反映
```

---

## 2. 独自ドメイン接続（shimulabo.com）

1. Vercel のプロジェクト → **Settings → Domains** → `shimulabo.com` を追加
2. Vercelが表示するDNS設定を、**お名前.com の DNSレコード設定**に登録：
   - `A` レコード： `@` → **Vercelが表示するIP**（例: `76.76.21.21`）
   - `CNAME`： `www` → **`cname.vercel-dns.com`**
   - ※ 実際の値は必ず **Vercel画面の表示に従う**（変わることがある）
3. 反映に数分〜最大48時間。**SSL（https）はVercelが自動発行**（無料・設定不要）
4. `www`付き → なし（またはその逆）の統一リダイレクトもVercelのDomains画面で設定

---

## 3. 機能を「全ユーザー横断の本物の集計」にする（任意）

拡散カウント・投票・リクエスト保存を全ユーザー共通にする場合のみ。
**やらなくてもサイトは公開・閲覧できる**（カウントがブラウザ単位になるだけ）。

1. Vercel → **Storage → Create → KV**（Upstash Redis）をプロジェクトに接続
   → 環境変数 `KV_REST_API_URL` / `KV_REST_API_TOKEN` が自動で入る
2. フロントのフラグを切り替え：
   - `assets/share-counter.js` … `const API = ''` → `'/api/share'`
   - `assets/vote.js` … `const API = ''` → `'/api/vote'`
3. リクエストをサーバー保存にする場合（任意）：
   - `request/index.html` のフォーム送信を mailto → `fetch('/api/request', …)` に変更
   - 一覧取得保護用に環境変数 `ADMIN_KEY` を設定
4. `git push`（or `vercel --prod`）で反映

> `package.json` に依存が書いてあるので、Vercelが自動で `@vercel/kv` 等をインストールする。

---

## 4. メール宛先を実アドレスに

- `contact/index.html` … `const TO = 'ad@example.com'` を実アドレスへ
- `request/index.html` … `const TO = 'request@example.com'` を実アドレスへ

（mailto方式。受信用アドレスを用意して差し替えるだけ）

---

## 5. 公開後のSEO初期設定

1. [Google Search Console](https://search.google.com/search-console) に `shimulabo.com` を登録（DNS認証 or HTMLメタ）
2. 「サイトマップ」で `https://shimulabo.com/sitemap.xml` を送信
3. [リッチリザルト テスト](https://search.google.com/test/rich-results) で各シミュURLを検証（FAQ・パンくずの構造化データ確認）
4. （任意）Google アナリティクス / Search Console 連携でアクセス計測

---

## 6. 新しいシミュレーターを追加する手順

1. `sims/<新id>/index.html` を作成（既存シミュをコピーして中身を差し替えるのが速い）
   - 末尾に `share-counter.js` の `initSim({ simId:'<新id>', … })` を入れる
2. `index.html` に：ギャラリーカード追加＋ランキング `SIMS` 配列に1行追加
3. `scripts/seo_internal.py` の `SIMS` に1行追加 → 下記を実行：
   ```bash
   python scripts/gen_images.py      # OGP画像を生成（新idぶん）
   python scripts/patch_heads.py     # favicon/OGPメタを新ページに付与
   python scripts/seo_internal.py    # 構造化データ・パンくず・関連リンク・sitemap更新
   ```
4. `api/share.js` `api/vote.js` の `ALLOW` セット（許可ID）に新idを追加（KV利用時）
5. `git push`

> スクリプトはすべて**冪等**（何度実行しても二重挿入されない）。

---

## 7. ビルド用スクリプト一覧（scripts/・公開には含めない）

| スクリプト | 役割 |
|-----------|------|
| `gen_images.py` | OGP画像(1200x630)・favicon PNG を生成 |
| `patch_heads.py` | 全ページの`<head>`に favicon・OGP/Twitterメタを挿入 |
| `seo_internal.py` | canonical・JSON-LD・パンくず・関連リンク・sitemap/robots |
| `set_domain.py` | ドメイン文字列を一括置換（例: `python scripts/set_domain.py 新ドメイン`） |

実行には Python と Pillow（`pip install pillow`）が必要。

---

## 8. 公開前 最終チェックリスト

- [ ] `scripts/`・`アイデア帳.md` が公開URLから見えない（`.vercelignore` で除外済み）
- [ ] `contact` / `request` のメール宛先を実アドレスに変更した
- [ ] （KV使う場合）`share-counter.js` `vote.js` の `API` を切り替えた
- [ ] Search Console 登録＋ sitemap 送信
- [ ] 主要シミュをスマホ実機で表示確認
- [ ] 利用規約・プライバシーポリシーの内容を確認（運営者名・管轄など）
```
