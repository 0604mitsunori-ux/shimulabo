# -*- coding: utf-8 -*-
# 十人十脳 第14話「100年前のIQ（フリン効果）」と連動（2026-11-06 新規）。動画の「まとめ方テスト」をWebで、ほかの問題でも。IQの数字は出さない
# 研究の事実は 制作キット/動画/第14話_100年前のIQ/00_研究メモ.md の ◯ の行だけ。問題はこのページで作ったもの（研究の問題の写しではない）
PAGE = {
    "slug": "matomekata-test",
    "title": "まとめ方テスト｜時計と定規の共通点は？あなたは「仲間」で答える？「使い方」で答える？100年で上がったIQの話も｜シミュラボ",
    "desc": "共通点・仲間はずれ・言われたことだけで答える問題、15問のセルフテスト。「仲間でまとめる答え方」と「使い方や場面でまとめる答え方」、あなたはどちらが多い？IQの平均点が100年で上がったフリン効果、「科学のめがね」という説明と反対意見、上がり続けたIQが下がり始めたノルウェーの研究も解説。IQの数字は出しません。診断ではありません。",
    "og_title": "時計と定規の共通点は？｜まとめ方テスト",
    "og_desc": "「仲間」でまとめる？「使い方」でまとめる？15問で、あなたの答え方のくせが分かる。",
    "ld_name": "まとめ方テスト（共通点・仲間はずれ・言われたことだけで答える）",
    "h1": "まとめ方テスト（あなたは「仲間」派？「使い方」派？）",
    "lead": "時計と定規の共通点を聞かれて、「どちらも測る道具」と答える人と、「どちらも机の上で使う物」と答える人がいます。どちらもまちがいではありません。共通点・仲間はずれ・言われたことだけで答える問題、15問に答えて、あなたの答え方のくせを見てみましょう。約4分です。",
    "start_h2": "🧠 15問に答えてね",
    "start_text": "問題が出たら、まず頭の中で答えを考えてください。「答えの例を見る」を押すと、2つの答え方が出ます。あなたの答えがどちらに近かったかを選んでください。正解・不正解はありません。",
    "tag": "まとめ方テスト",
    "card_label": "まとめ方テストの結果",
    "card_footer": "時計と定規の共通点は？ → shimulabo.com",
    "css": """
.mt-q{font-size:22px;font-weight:900;text-align:center;line-height:1.6;margin:10px 0 14px;color:#EEEAE3;}
.mt-q small{display:block;font-size:13px;font-weight:700;color:#8D9BA1;margin-bottom:6px;}
.mt-story{font-size:16px;font-weight:700;line-height:1.8;text-align:left;background:#111c20;border:1px solid #2A3C43;border-radius:12px;padding:12px 14px;margin:6px 0 12px;color:#EEEAE3;}
.mt-items{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;margin:6px 0 12px;}
.mt-items span{min-width:70px;padding:8px 10px;border-radius:12px;background:#111c20;border:1px solid #2A3C43;text-align:center;font-size:17px;font-weight:800;color:#EEEAE3;}
.mt-ans{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:4px 0 12px;}
.mt-ans div{border-radius:12px;padding:10px 8px;background:#111c20;text-align:center;font-size:15px;font-weight:800;line-height:1.5;color:#EEEAE3;}
.mt-ans div small{display:block;font-size:11px;font-weight:700;margin-bottom:3px;}
.mt-ans .a{border:2px solid #4FC6B4;} .mt-ans .a small{color:#4FC6B4;}
.mt-ans .b{border:2px solid #F5BB5C;} .mt-ans .b small{color:#F5BB5C;}
.syn-btns.c3{grid-template-columns:repeat(3,1fr);}
.syn-btns.c3 button{font-size:13px;padding:10px 2px;}
""",
    "stage_html": """
      <div class="syn-top"><span id="part">共通点</span><span id="count">1 / 15</span></div>
      <div class="syn-bar"><i id="bar"></i></div>
      <div id="show"></div>
      <div class="syn-btns" id="opts"></div>
    """,
    "js": r"""
  const $ = NOU.$;
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  // 問題はこのページで作ったもの（研究の問題の写しではない）。最初の1問だけ動画（十人十脳 第14話）と同じ
  const Q = [
    { k: '共通点', q: '時計 と 定規', a: 'どちらも「測る」道具', b: 'どちらも机の上で使う' },
    { k: '共通点', q: '船 と 飛行機', a: 'どちらも乗り物', b: 'どちらも旅行で使う' },
    { k: '共通点', q: '太鼓 と ピアノ', a: 'どちらも楽器', b: 'どちらも音楽の授業で見る' },
    { k: '共通点', q: '牛乳 と チーズ', a: 'どちらも牛の乳からできる', b: 'どちらも冷蔵庫に入れる' },
    { k: '共通点', q: '帽子 と 手袋', a: 'どちらも身に着ける物', b: 'どちらも寒い日に使う' },
    { k: '仲間はずれ', items: ['鍋', 'お玉', 'コンロ', 'にんじん'], a: 'にんじん（ほかは道具）', b: '外せない（どれもカレー作りに要る）' },
    { k: '仲間はずれ', items: ['歯ブラシ', 'タオル', '石けん', 'お風呂'], a: 'お風呂（ほかは持ち運べる道具）', b: '外せない（どれも体を洗うのに使う）' },
    { k: '仲間はずれ', items: ['ボール', 'バット', 'グローブ', '公園'], a: '公園（ほかは道具）', b: '外せない（どれも野球で使う）' },
    { k: '仲間はずれ', items: ['机', 'いす', '本だな', '宿題'], a: '宿題（ほかは家具）', b: '外せない（どれも勉強に使う）' },
    { k: '仲間はずれ', items: ['封筒', '切手', 'はがき', '郵便局'], a: '郵便局（ほかは紙の物）', b: '外せない（どれも手紙を出すのに使う）' },
    { k: '言われたことだけで', s: 'ラモ村では、赤い帽子の人は、みんな歌が上手だ。ケンは、ラモ村の赤い帽子の人だ。', q: 'ケンは、歌が上手？', a: '上手', b: '会ったことがないから分からない' },
    { k: '言われたことだけで', s: 'この町の犬は、みんな青い。ポチは、この町の犬だ。', q: 'ポチは、何色？', a: '青', b: '犬は青くないはず' },
    { k: '言われたことだけで', s: 'ミルの森の木は、みんな冬に花が咲く。この木は、ミルの森の木だ。', q: 'この木は、いつ花が咲く？', a: '冬', b: '冬に花は咲かないはず' },
    { k: '言われたことだけで', s: 'ある国では、月曜日は、みんな学校が昼で終わる。今日は、その国の月曜日だ。', q: '今日の学校は、昼で終わる？', a: '終わる', b: 'ふだんの月曜日は夕方まで' },
    { k: '言われたことだけで', s: 'この星では、水は上に流れる。ララ川は、この星の川だ。', q: 'ララ川の水は、どちらへ流れる？', a: '上', b: '水は下に流れるはず' },
  ];
  const LAB = { '共通点': ['仲間でまとめた答え', '使い方・場面でまとめた答え'], '仲間はずれ': ['仲間で分けた答え', '使い方・場面で考えた答え'], '言われたことだけで': ['言われたことから', '経験から'] };
  let K = 0, A = 0, B = 0, N = 0, stage = 0;
  function head() { $('part').textContent = Q[K].k; $('count').textContent = (K + 1) + ' / ' + Q.length; $('bar').style.width = (K / Q.length * 100) + '%'; }
  function body(q) {
    if (q.items) return `<div class="mt-q"><small>4つのうち、1つを外すなら？</small></div><div class="mt-items">${q.items.map(t => `<span>${esc(t)}</span>`).join('')}</div>`;
    if (q.s) return `<div class="mt-story">${esc(q.s)}</div><div class="mt-q"><small>言われたことだけを使って答えてね</small>${esc(q.q)}</div>`;
    return `<div class="mt-q"><small>2つの共通点は？</small>${esc(q.q)}</div>`;
  }
  function ask() {
    head(); stage = 0; const q = Q[K];
    $('show').innerHTML = body(q);
    $('opts').className = 'syn-btns c1'; $('opts').innerHTML = '<button type="button" data-v="go">頭の中で考えた → 答えの例を見る</button>';
  }
  function reveal() {
    stage = 1; const q = Q[K], L = LAB[q.k];
    $('show').innerHTML = body(q) + `<div class="mt-ans"><div class="a"><small>左：${L[0]}</small>${esc(q.a)}</div><div class="b"><small>右：${L[1]}</small>${esc(q.b)}</div></div>`
      + '<div class="syn-ask" style="margin:4px 0 8px">あなたの答えは、どちらに近かった？</div>';
    $('opts').className = 'syn-btns c3'; $('opts').innerHTML = ['左に近い', '右に近い', 'どちらでもない'].map((t, i) => `<button type="button" data-v="${i}">${t}</button>`).join('');
  }
  $('opts').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return;
    if (b.dataset.v === 'go') return reveal();
    const v = +b.dataset.v; if (v === 0) A++; else if (v === 1) B++; else N++;
    K++; if (K < Q.length) ask(); else done(); });
  function done() {
    $('bar').style.width = '100%';
    const tot = A + B;
    let type, emoji, advice;
    if (tot === 0 || A / Math.max(tot, 1) >= 0.666) { type = 'めがね型'; emoji = '👓'; advice = '目の前にない「ひとつ上のグループ」でまとめたり、言われた決まりだけで考えたりするのが得意なタイプ。知らない島の話でも、言われたことから答えを出せます。'; }
    else if (A / tot <= 0.334) { type = 'くらし型'; emoji = '🏠'; advice = '目の前の物を、本当に使う場面で考えるタイプ。説明が具体的だと、すっと入ってきやすいかもしれません。毎日の暮らしで役に立つ見方です。'; }
    else { type = 'まんなか型'; emoji = '⚖️'; advice = '仲間でまとめる見方と、使い方で考える見方を、問題によって使い分けるタイプ。どちらの説明にも合わせやすいかもしれません。'; }
    if (tot === 0) advice = '「どちらでもない」が多かったので、型はおおまかな目安です。' + advice;
    const P3 = [['左（仲間・言われたこと）', A], ['右（使い方・経験）', B], ['どちらでもない', N]];
    const rows = P3.map(([k, v]) => `<div><span class="k">${k}</span><span class="syn-meter"><i style="width:${v / Q.length * 100}%"></i></span><span class="v">${v}問</span></div>`).join('');
    NOU.finish({
      label: 'あなたの答え方は', big: type, unit: '', emoji, typeName: type, advice,
      extraHTML: `<div class="syn-rows">${rows}</div><p style="font-size:12px;color:var(--ink-3);">どちらの答え方が正しい・頭がいい、というものではありません。このテストからIQの数字は出しません。</p>`,
      share: `まとめ方テストやってみた🧠 わたしは「${type}」でした（仲間で${A}問・使い方で${B}問）。時計と定規の共通点、あなたはどう答える？`,
      cardTitle: 'わたしの答え方のくせ', cardLine: `仲間 ${A}問・使い方 ${B}問・どちらでもない ${N}問`,
      draw: (x, Q2) => {
        P3.forEach(([k, v], i) => { const y = Q2.y + 30 + i * 150;
          x.fillStyle = '#EEEAE3'; x.textAlign = 'left'; x.font = '800 40px ' + Q2.F; x.fillText(k, Q2.x, y + 10);
          x.textAlign = 'right'; x.fillText(v + '問', Q2.x + Q2.w, y + 10);
          x.fillStyle = '#2A3C43'; x.beginPath(); x.roundRect(Q2.x, y + 34, Q2.w, 50, 25); x.fill();
          x.fillStyle = i === 0 ? '#4FC6B4' : i === 1 ? '#F5BB5C' : '#8D9BA1'; x.beginPath(); x.roundRect(Q2.x, y + 34, Math.max(50, Q2.w * v / 15), 50, 25); x.fill(); });
      },
    });
  }
  function start() { K = 0; A = 0; B = 0; N = 0; NOU.startPanels(); ask(); }
  $('startBtn').addEventListener('click', start); $('againBtn').addEventListener('click', start);
""",
    "note": "共通点（5問）・仲間はずれ（5問）・言われたことだけで答える問題（5問）です。問題はこのページで作っています。左＝仲間でまとめた答え（言われたことから答えた答え）、右＝使い方や場面でまとめた答え（経験から答えた答え）として数えます。IQの数字は出しません。",
    "article": """
    <h2>「仲間」でまとめる？「使い方」でまとめる？</h2>
    <p>時計と定規の共通点を聞かれて、「どちらも測る道具」と答えるのは、目の前にない<b>ひとつ上のグループ（仲間）</b>でまとめる答え方です。「どちらも机の上で使う物」と答えるのは、<b>使う場面</b>を思い浮かべてまとめる答え方です。どちらもまちがいではありません。</p>
    <p>子ども向けの知能検査（WISC）には10の小テストがあり、そのうちの「類似」は、2つの物の共通点に気づく力を測るものです（Flynn 2007）。このページの問題は、その考え方をイメージして作った遊びのテストで、知能検査の問題とは別物です。</p>

    <h2>IQの平均点は、100年で上がり続けた（フリン効果）</h2>
    <p>1987年、研究者のジェームズ・フリンが14の国のデータを集めると、IQの点は<b>1つの世代のあいだに5〜25点</b>も上がっていました。とくに大きく上がっていたのは、知識や文化にあまり頼らないテストと、その場で考える力のテストでした（Flynn 1987）。</p>
    <p>1909年から2013年までの31か国・271の集団・およそ400万人のデータをまとめた研究でも、IQは世界中で100年以上上がり続けていました。1年あたりでは、全体で0.28点（10年でおよそ3点）。その場で考える力は0.41点、知識の力は0.21点で、子どもより大人で上がり方が大きく、最近の数十年は上がり方が小さくなっていました（Pietschnig と Voracek 2015）。</p>
    <p>アメリカでは1932年から2002年の70年で、およそ22点上がりました（Flynn と Weiss 2007）。計算の上では、1932年に平均だった人は、2002年の物差しで測るとおよそ78になります（実際に測った値ではありません）。</p>

    <h2>上がったのは「共通点」の力？　科学のめがね</h2>
    <p>フリンは、とくに「類似（共通点）」の問題や図形の推理のテストの大きな上がり方に注目し、<b>科学の技術が社会に広まって、今の人は具体的なやり方より抽象的なやり方で問題を考えるようになった</b>と考えました。この、具体的・実用的な考え方から抽象的な推理への移り変わりを、フリンは「科学のめがね」と名づけています（Kaufman 2010 による整理）。</p>
    <p>ただし反対の意見もあります。心理学者のカウフマンは、1974年に検査が作り直されたとき、問題の中身・出し方・採点のしかたが大きく変わったので、1947年と2002年の「類似」の点をそのまま比べるのは意味が薄い、と批判しました。フリンはこの批判に強く反対していて、決着はついていません（Kaufman 2010）。</p>

    <h2>上がり続けたIQが、下がり始めた国</h2>
    <p>ノルウェーでは、18〜19歳の男性が兵役の検査で、計算・ことばの共通点・図形のテストを受けます。1962〜1991年に生まれたおよそ74万人の点は、1962年生まれの99.5から1975年生まれの102.3まで上がり、そのあと1989年生まれの99.4まで下がっていました（Bratsberg と Rogeberg 2018）。</p>
    <p>同じ父と母から生まれた兄弟どうしで比べても、上がって、曲がって、下がる同じ流れが見られたことから、研究者は、点の上がり下がりは親の顔ぶれの変化や遺伝ではなく、<b>環境の要因</b>によるものだと結論しました。ただし、どんな環境なのかは分かっていません。学校で学ぶことの量や中身の変化、メディアとの付き合い方の変化、栄養や健康の変化などの説と矛盾しない、と書かれています。</p>

    <h2>結果の見方</h2>
    <div class="tbl-scroll">
    <table class="seo-table">
    <tr><th>タイプ</th><th>答え方</th></tr>
    <tr><td>👓 めがね型</td><td>左（仲間でまとめる・言われたことから答える）が多い</td></tr>
    <tr><td>⚖️ まんなか型</td><td>左と右が同じくらい（問題によって使い分ける）</td></tr>
    <tr><td>🏠 くらし型</td><td>右（使い方や場面でまとめる・経験から答える）が多い</td></tr>
    </table>
    </div>
    <p>「どちらでもない」を除いた答えのうち、左が3分の2以上ならめがね型、3分の1以下ならくらし型、そのあいだをまんなか型にしています。このページで決めた遊びの分け方で、どちらが上というものではありません。</p>
""",
    "faq": [
        ("このテストでIQは分かりますか？", "いいえ。このテストからIQの数字は出しません。本当のIQは、専門家が決まった手順で行う検査で測ります。"),
        ("「仲間」で答えるほうが頭がいいのですか？", "いいえ。どちらの答え方もまちがいではありません。使い方や場面で考える見方は、毎日の暮らしで役に立つ見方です。"),
        ("昔の人は頭が悪かったのですか？", "そうではありません。IQの点が上がったことは確かですが、それが人がそのまま賢くなったことなのかは分かっていません。考えるための「道具」や、求められる考え方が変わったのかもしれない、という説明があります。"),
        ("日本のIQも上がったり下がったりしているのですか？", "このページでは、日本についての研究は確かめていません。分からないことは分からない、としておきます。"),
        ("答えは送信されますか？", "いいえ。答えはこの画面の中だけで使い、送信も保存もしません（サイト全体のアクセス解析については<a href=\"../../privacy/\">プライバシーポリシー</a>をご覧ください）。"),
    ],
    "refs": [
        "Flynn JR (1987). Massive IQ gains in 14 nations: What IQ tests really measure. <i>Psychological Bulletin</i>, 101(2), 171–191.",
        "Pietschnig J, Voracek M (2015). One century of global IQ gains: A formal meta-analysis of the Flynn effect (1909–2013). <i>Perspectives on Psychological Science</i>, 10(3), 282–306.",
        "Flynn JR, Weiss LG (2007). American IQ gains from 1932 to 2002: The WISC subtests and educational progress. <i>International Journal of Testing</i>, 7(2), 209–224.",
        "Flynn JR (2007). <i>What Is Intelligence? Beyond the Flynn Effect</i>. Cambridge University Press.",
        "Kaufman AS (2010). \"In what way are apples and oranges alike?\" A critique of Flynn's interpretation of the Flynn effect. <i>Journal of Psychoeducational Assessment</i>, 28(5), 382–398.",
        "Kaufman AS (2010). Looking through Flynn's rose-colored scientific spectacles. <i>Journal of Psychoeducational Assessment</i>, 28(5), 494–505.",
        "Bratsberg B, Rogeberg O (2018). Flynn effect and its reversal are both environmentally caused. <i>Proceedings of the National Academy of Sciences</i>, 115(26), 6674–6678.",
    ],
    "related": [("iq-yottsu-chikara", "🧩", "IQ 4つの力テスト（言葉・形・覚える・速さ）"), ("iq-test", "🧩", "IQテスト（パターン問題と「見ない力」）"), ("dunning-kruger", "🤔", "ダニング＝クルーガー効果テスト"), ("tango-kioku", "📝", "単語記憶テスト")],
}
