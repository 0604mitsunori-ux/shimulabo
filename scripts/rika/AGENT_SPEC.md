# 理科の授業向けシミュ 作成仕様（作成担当向け）

シミュラボ（https://shimulabo.com）に「理科の授業向け」シミュを追加する。使う場面は小学校〜高校の理科の授業。
端末は GIGAスクールのタブレット（**iPad 縦 820×1180 の Safari** が最多。Chromebook・Windows タブレット）と電子黒板・プロジェクター。

## 1. 作るもの
`scripts/rika/<担当モジュール>.py` に `SIMS = [dict(...), dict(...)]` を書く（1モジュール2本）。
HTMLはこのdictから `scripts/rika/common.py` の `render()` が作る（ページの骨格・GA・広告・構造化データ・シェアボタン・全画面ボタンは共通）。
**お手本**：`scripts/fable20/sims_a.py`（同じ形式の dict。部品の使い方・JSの書き方はここを真似る）

### dict の必須キー
| キー | 内容 |
|---|---|
| slug | 指定されたもの（URL `/sims/<slug>/`） |
| cat | 必ず `"rika"` |
| title | h1・カードの名前（例「湿度と雲のでき方シミュレーター（飽和水蒸気量・露点）」） |
| title_tag | `<title>` の前半（「｜シミュラボ」は自動で付く）。検索される単元名を前に（例「露点・飽和水蒸気量のシミュレーター｜湿度の計算と雲のでき方」） |
| meta_desc | 120字前後 |
| og_title / og_desc | SNS用 |
| lead | 2〜3文。何ができるか |
| model | バッジに出す単元名（例「中2 気象観測・天気の変化」） |
| level | 例「中学2年」「小学4年・6年、中学3年」 |
| unit | 学習指導要領の単元名（例「中学校 第2分野（4）気象とその変化」） |
| emoji / card_desc / score | トップのカード用（card_desc 40〜60字、score は 70〜85 の整数） |
| canvas / controls / buttons / stats / legend | `common.canvas() / slider() / select() / btn() / stats()` で作る（お手本参照） |
| article | 記事HTML（下の4章構成） |
| faqs | `[(質問, 答え), ...]` 4〜6問。授業や定期テストで聞かれそうなもの |
| rel | `[(slug, 絵文字, 名前), ...]` 3〜5件。下の「既存の関連シミュ」から選ぶ |
| js | 下のJS規約に従う |

## 2. JS 規約
- `js` は共通テンプレートの `try { ... }` の中にそのまま入る。使えるもの：`$(id)`, `num(n)`, `clamp(v,a,b)`, `rnd(a,b)`, `randn()`, `setShare(text)`, `cpos(cv,e)`, `setStat(id,v)`（スライダーの数値表示 `syncSliders()` は実行済み）。
- canvas は `id="cv"`。**Retina対応必須**：`const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const ctx=cv.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0);` として描画は W×H の座標で。`cpos()` の戻り値は dpr 倍なので `/dpr` する。
- 指・ペンで操作できること：`pointerdown / pointermove / pointerup`（`touch-action:none` は canvas に設定済み）。ボタン・スライダーは指で押せる大きさ。
- アニメは `requestAnimationFrame`。外部通信・外部ライブラリ・画像ファイルは使わない（端末だけで完結）。
- 関数式を代入した直後の行頭を `(` で始めない（ASIで落ちる）。`window.x=function(){...};` のように `;` を付ける。
- 結果の一文を `setShare()` に入れる（例「【湿度と露点】気温25℃・湿度60%の空気は約16.7℃で露が出始める｜シミュラボ」）。
- 統計欄（stats）は初期表示で必ず値を入れる（「—」のまま残さない）。

## 3. 教材としての正確さ
- 数値・式は教科書や公的機関の値に合わせる。単純化した点（大きさ・距離を誇張した図など）は本文に明記する。
- 用語は今の学習指導要領・教科書の言い方にする（例：遺伝は「顕性・潜性」。「優性・劣性」は使わない）。
- 小学生向けの単元は、小学生にも読める言葉で。漢字が多すぎないように。
- 主要な数値は Python などで別に計算して照合する（例：25℃の飽和水蒸気量 23.1 g/m³）。

## 4. 記事（article）の構成
`<h2>` で次の4章。誇張表現（「驚くほど」「完全ガイド」など）は使わない。です・ます調。
1. **このシミュレーションでわかること**（結論を2〜3行。学習指導要領の単元名と学年を明記）
2. **授業での使い方**（導入・展開・まとめのどこで使うか。児童・生徒への問いの例を3つ）
3. **しくみ・解説**（式・図・計算問題の解き方。必要なら早見表 `common.T()`）
4. **参考**（教科書・公的機関の名前。URLは確実なものだけ）

## 5. 確認手順（必ず全部やる）
1. ページ生成：`python scripts/rika/build_sims.py --module <担当モジュール>`（自分のページだけ生成される）
2. ヘッドレスChromeでエラー確認：
   ```bash
   "/c/Program Files/Google/Chrome/Application/chrome.exe" --headless=new --disable-gpu --allow-file-access-from-files --virtual-time-budget=5000 --enable-logging=stderr --v=0 --dump-dom "file:///C:/Users/社員/Desktop/Nsawa/プロジェクト/シミュラボ/sims/<slug>/index.html" > /tmp/<slug>.html 2> /tmp/<slug>.err
   ```
   `.err` に `Uncaught` や `CONSOLE` のエラーが無いこと、`.html` の統計欄が「—」のままでないこと。
3. iPad縦の見た目：`--screenshot="C:/Users/社員/Desktop/Nsawa/プロジェクト/シミュラボ_理科授業/shots/<slug>.png" --window-size=820,1180 --hide-scrollbars --virtual-time-budget=4000` で撮って、Read で画像を開いて自分の目で確認（文字のはみ出し・重なり・小さすぎるボタンが無いか）。
4. 主要な数値を別計算で照合。

## 6. 触ってはいけないもの
`index.html` / `sitemap.xml` / `api/share.js` / `rika/index.html` / `scripts/rika/build_sims.py` / `scripts/rika/common.py` / `scripts/rika/build.py` / `scripts/rika/units.json` / 他の担当のモジュール。**git の commit / push はしない**（まとめて公開する）。ブラウザの共有ペイン（Claude_Browser）は使わない（他の担当と取り合いになる）。

## 7. 既存の関連シミュ（rel に使える slug）
magnet 磁力線シミュレーター🧲 / kyou-no-tsuki 今日の月🌙 / hoshizora-shisu 今夜の星空指数🔭 / pendulum-wave 振り子の波 / amagumo-now いまの雨雲マップ🌧️ / solar-hatsuden 今日のソーラー発電シミュ🔋 / lotka-volterra キツネとウサギ 増減シミュレーター🐰 / jishin-live 日本はいまも揺れている🗾 / mosquito-on モスキート音テスト / ripple 波紋シミュレーター / doppler ドップラー効果シミュレーター / diffusion 拡散シミュレーター / coffee-milk コーヒーにミルクを落とすと / denkidai-keisan 電気代計算機 / newtons-cradle ニュートンのゆりかご / led-setsuyaku LED電球の節約シミュ / chikyu-yure 地球まるごと地震カウンター🌐 / tsunami-kishi 津波はなぜ岸で高くなる？🌊 / building-quake 地震でビルはどう揺れる？🏢 / kaibatsu-check うちの海抜チェッカー⛰️ / reaction-test 反応速度テスト / myakuhaku-heikin 脈拍・心拍数 平均チェック / kiatsu-jet 気圧ジェットコースター指数🎢 / sentaku-kawaku 洗濯物 乾く時間メーター👕 / kaminari-alert 今日の雷ゴロゴロ度⚡ / yohou-shinrai 週間予報、どこまで信じる？🔮 / ketsueki-iden 血液型 遺伝 判定 / shinka-sim 進化シミュレーター / dna DNA二重らせん / solar-system 太陽系シミュレーター / hiruma-nagasa 昼の長さメーター🌅 / gravity 重力シミュレーター / gears 歯車シミュレーター / wave 波の干渉シミュレーター / double-slit ダブルスリット実験 / lissajous リサージュ図形 / iss-doko ISSはいまどこ？🛰️
（絵文字が無いものは、トップのカードの絵文字を `index.html` で確認して使う。読むだけならOK）

## 8. 報告
各シミュについて：できること（3行）／照合した数値／iPad縦で確認した結果／気になる点・未対応。
