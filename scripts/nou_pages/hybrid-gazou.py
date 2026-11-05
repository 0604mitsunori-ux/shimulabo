# -*- coding: utf-8 -*-
# 十人十脳 第10話「見える人・見えない人（近くと遠くで別の絵）」と連動（2026-11-05 新規）
PAGE = {
    "slug": "hybrid-gazou",
    "title": "近くと遠くで変わる数字テスト｜あなたにはどっちの数字が見える？ハイブリッド画像の錯視｜シミュラボ",
    "desc": "1枚の画像に、2つの数字がかくれています。近くで見ると見える数字と、離れて見ると見える数字。あなたには、いまどちらが見えますか？細かい線と大まかな形のどちらを先に拾うかを、6問で試すセルフテスト。診断ではありません。",
    "og_title": "あなたにはどっちの数字が見える？｜近くと遠くで変わる数字テスト",
    "og_desc": "1枚に2つの数字。近くと遠くで、見える数字が入れかわる。",
    "ld_name": "近くと遠くで変わる数字テスト",
    "h1": "近くと遠くで変わる数字テスト（あなたにはどっちが見える？）",
    "lead": "このページの画像には、<b>2つの数字が重ねてかくしてあります</b>。細い線でかいた数字と、ぼかした太い数字です。近くで見るか、離れて見るかで、見える数字が入れかわります。まずは、いつもの距離で見えた数字を答えてください。6問、約1分です。",
    "start_h2": "👓 いつもの距離で、見えた数字を答えてね",
    "start_text": "1問ごとに画像が1枚出ます。いちばん先に見えた数字を選んでください。答えたあとで、画面から離れて見ると…？",
    "tag": "錯視",
    "card_label": "近くと遠くで変わる数字テストの結果",
    "card_footer": "あなたにはどっちの数字が見える？ → shimulabo.com",
    "stage_html": """
      <div class="syn-top"><span>いちばん先に見えた数字は？</span><span id="count">1 / 6</span></div>
      <div class="syn-bar"><i id="bar"></i></div>
      <canvas id="hy" width="400" height="400" style="width:100%;max-width:300px;display:block;margin:6px auto 10px;border-radius:12px;"></canvas>
      <div class="syn-btns" id="opts" style="grid-template-columns:repeat(3,1fr);"></div>
    """,
    "js": r"""
  const $ = NOU.$;
  // ぼかした太い数字（離れると見える）＋細い線だけの数字（近くで見える）を1枚に重ねる
  function hybrid(low, high) {
    const W = 400, mk = (d, w, blur) => { const c = document.createElement('canvas'); c.width = c.height = W; const x = c.getContext('2d');
      x.fillStyle = '#fff'; x.fillRect(0, 0, W, W); x.filter = blur ? `blur(${blur}px)` : 'none'; x.fillStyle = '#000'; x.font = `${w} 330px "Noto Sans JP","Yu Gothic",sans-serif`; x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText(d, W / 2, W / 2 + 10); return x.getImageData(0, 0, W, W).data; };
    const L = mk(low, '900', 20), H = mk(high, '300', 0), Hb = mk(high, '300', 4);   // 太い数字は大きくぼかす／細い数字は線の部分だけ残す（11/5 目で見て調整）
    const c = $('hy'), x = c.getContext('2d'), img = x.createImageData(W, W);
    for (let i = 0; i < L.length; i += 4) { const v = Math.max(0, Math.min(255, 0.75 * (L[i] - 255) + 235 + (H[i] - Hb[i]))); img.data[i] = img.data[i + 1] = img.data[i + 2] = v; img.data[i + 3] = 255; }
    x.putImageData(img, 0, 0);
  }
  const Q = [[0, 7], [1, 6], [2, 9], [7, 0], [6, 1], [9, 2]].sort(() => Math.random() - .5);   // [離れると見える数字, 近くで見える数字]（形のちがう組だけ）
  let k = 0, ans = [];
  function next() {
    const [lo, hi] = Q[k]; hybrid(lo, hi); $('count').textContent = (k + 1) + ' / 6'; $('bar').style.width = (k / 6 * 100) + '%';
    const other = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9].find(d => d !== lo && d !== hi && (d + k) % 3 === 0);
    $('opts').innerHTML = [lo, hi, other].sort(() => Math.random() - .5).map(d => `<button type="button" data-v="${d}" style="font-size:24px;font-weight:900;">${d}</button>`).join('') + '<button type="button" data-v="-1" style="grid-column:span 3;">どれでもない・分からない</button>';
  }
  $('opts').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; const v = +b.dataset.v, [lo, hi] = Q[k]; ans.push(v === hi ? 'near' : v === lo ? 'far' : 'none'); k++; if (k < 6) next(); else done(); });
  function done() {
    const near = ans.filter(a => a === 'near').length, far = ans.filter(a => a === 'far').length;
    const T = near >= 5 ? ['🔍', '細かい線が先に見えるタイプ', 'いつもの距離では、細い線でかいた数字が先に見えました。画面から2〜3メートル離れるか、目を細めて見ると、もう一つの数字が出てきます。']
            : far >= 5 ? ['🌫️', '大まかな形が先に見えるタイプ', 'いつもの距離でも、ぼかした太い数字が先に見えました。画面が小さい・遠い・ぼやけて見えるときにも、こうなりやすくなります。']
            : ['🔀', '両方が見えるタイプ', '問題によって、細い線の数字とぼかした数字の両方が見えました。見る距離や画面の大きさで、どちらが勝つかが入れかわります。'];
    NOU.finish({
      label: '6問中、細い線の数字が見えた数', big: near, unit: ' / 6 問', emoji: T[0], typeName: T[1], advice: T[2],
      extraHTML: `<div class="syn-rows"><div><span class="k">🔍 細い線の数字（近くで見える）</span><span class="v">${near} 問</span></div><div><span class="k">🌫️ ぼかした数字（離れると見える）</span><span class="v">${far} 問</span></div></div><p style="font-size:12px;color:var(--ink-3);">「もう一度」で、今度は画面から離れて答えてみてください。答えが入れかわるはずです。</p>`,
      share: `近くと遠くで変わる数字テストやってみた👓 6問中${near}問で細い線の数字が見えて「${T[1]}」でした。あなたにはどっちの数字が見える？`,
      cardTitle: 'わたしの目が先に拾うもの', cardLine: `細い線 ${near}問・ぼかした形 ${far}問`,
      draw: (x, R) => {
        const cw = (R.w - 5 * 18) / 6;
        ans.forEach((a, i) => { const xx = R.x + i * (cw + 18), y = R.y + 150;
          x.fillStyle = a === 'near' ? '#4FC6B4' : a === 'far' ? '#F5BB5C' : '#2A3C43'; x.beginPath(); x.roundRect(xx, y, cw, 220, 20); x.fill();
          x.fillStyle = '#0D1417'; x.textAlign = 'center'; x.font = '900 64px ' + R.F; x.fillText(a === 'near' ? '🔍' : a === 'far' ? '🌫️' : '？', xx + cw / 2, y + 140); });
        x.textAlign = 'center'; x.font = '800 36px ' + R.F; x.fillStyle = '#4FC6B4'; x.fillText('🔍 細い線の数字', R.x + R.w * .27, R.y + 90); x.fillStyle = '#F5BB5C'; x.fillText('🌫️ ぼかした数字', R.x + R.w * .73, R.y + 90);
      },
    });
  }
  function start() { k = 0; ans = []; NOU.startPanels(); next(); }
  $('startBtn').addEventListener('click', start); $('againBtn').addEventListener('click', start);
""",
    "note": "細い線でかいた数字と、ぼかした太い数字を1枚に重ねた画像を見て、どちらが先に見えたかを答えるセルフテストです。研究で「ハイブリッド画像」と呼ばれる作り方をもとに、このページで画像を作っています。",
    "article": """
    <h2>1枚の画像に、2つの絵をかくす</h2>
    <p>このページの画像は、<b>ぼかした太い数字</b>と、<b>細い線だけの数字</b>を重ねて作っています。近くで見ると、目は細い線をはっきりとらえるので、細い線の数字が見えます。離れて見ると、細い線は細かすぎて見えなくなり、ぼかした大きな形だけが残ります。</p>
    <p>このような画像は「ハイブリッド画像」と呼ばれ、見る距離によって別の絵に見えることが紹介されています（Oliva・Torralba・Schyns 2006）。</p>

    <h2>頭は「大まかな形」から先に見る？</h2>
    <p>ぼかした絵と細い線の絵を重ねた画像を使って、人が景色をどう見分けるかを調べた研究があります。結果からは、<b>まず大まかな形（ぼんやりした明るさのかたまり）で見当をつけ、そのあと細かい線で確かめる</b>という見方をしている可能性が示されました（Schyns・Oliva 1994）。</p>
    <p>ただし、どちらが勝つかは、画面の大きさ、見る距離、目の見え方でも変わります。同じ人でも、近くで見るか離れて見るかで答えが入れかわります。</p>

    <h2>見え方が変わる理由</h2>
    <ul>
      <li><b>画面が小さい・遠い</b>：細い線が見えにくくなり、ぼかした数字が勝ちやすい</li>
      <li><b>目を細める</b>：見え方がぼやけて、ぼかした数字が出てくる</li>
      <li><b>画面が大きい・近い</b>：細い線の数字が勝ちやすい</li>
    </ul>
    <p>「もう一度」で、今度は2〜3メートル離れて答えてみてください。答えが入れかわったら、あなたの目と頭が、距離で見るものを切りかえている証拠です。</p>

    <h2>結果の3つのタイプ</h2>
    <div class="tbl-scroll">
    <table class="seo-table">
    <tr><th>タイプ</th><th>どんな結果？</th></tr>
    <tr><td>🔍 細かい線が先に見えるタイプ</td><td>6問中5問以上で、細い線の数字が見えた</td></tr>
    <tr><td>🔀 両方が見えるタイプ</td><td>問題によって、どちらも見えた</td></tr>
    <tr><td>🌫️ 大まかな形が先に見えるタイプ</td><td>6問中5問以上で、ぼかした数字が見えた</td></tr>
    </table>
    </div>
""",
    "faq": [
        ("このテストで視力が分かりますか？", "いいえ。遊びのためのセルフテストで、視力の検査ではありません。見え方が気になる人は、眼科で検査を受けられます。"),
        ("どちらが正解ですか？", "どちらも正解です。1枚の画像に2つの数字が入っていて、見る距離で見える数字が変わります。"),
        ("離れても数字が変わりません。", "画面の大きさや明るさで変わりにくいことがあります。2〜3メートル離れるか、目を細めて見てください。"),
        ("答えは送信されますか？", "いいえ。答えはこの画面の中だけで使い、送信も保存もしません（サイト全体のアクセス解析については<a href=\"../../privacy/\">プライバシーポリシー</a>をご覧ください）。"),
    ],
    "refs": [
        "Schyns PG, Oliva A (1994). From Blobs to Boundary Edges: Evidence for Time- and Spatial-Scale-Dependent Scene Recognition. <i>Psychological Science</i>, 5(4), 195–200.",
        "Oliva A, Torralba A, Schyns PG (2006). Hybrid images. <i>ACM Transactions on Graphics</i>（SIGGRAPH 2006）, 25(3), 527–532.",
    ],
    "related": [("sakushi-kaiten", "🌀", "回転の錯視テスト（どちら回り？）"), ("shikikaku-test", "🎨", "色覚テスト（あなたの目は何色型？）"), ("shiryoku-test", "👁️", "視力テスト"), ("aphantasia-test", "🍎", "アファンタジア テスト（頭の中の映像）")],
}
