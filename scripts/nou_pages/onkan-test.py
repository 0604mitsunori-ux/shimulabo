# -*- coding: utf-8 -*-
# 十人十脳 第6話「音の聞こえ方（絶対音感・相対音感）」と連動（2026-11-05 新規）
PAGE = {
    "slug": "onkan-test",
    "title": "絶対音感テスト・相対音感テスト｜あなたの耳は何タイプ？音の高さの聞き分けを試す｜シミュラボ",
    "desc": "鳴った音の名前（ドレミ）が分かりますか？2つの音、どちらが高いか分かりますか？絶対音感と相対音感を、16問で試すセルフテスト。音の高さが「名前」で聞こえる人の研究も解説。診断ではありません。",
    "og_title": "あなたの耳は何タイプ？｜絶対音感・相対音感テスト",
    "og_desc": "鳴った音のドレミ、分かる？2つの音の高い・低い、分かる？",
    "ld_name": "絶対音感・相対音感テスト（あなたの耳は何タイプ？）",
    "h1": "絶対音感・相対音感テスト（あなたの耳は何タイプ？）",
    "lead": "ピアノの音を聞いただけで「いまのはソ」と分かる人がいます。一方で、2つの音の差なら分かるけれど、名前までは分からない人もいます。前半8問で「2つの音のどちらが高いか」、後半8問で「鳴った音の名前」を試します。約3分です。",
    "start_h2": "🎹 音量を小さめにして、はじめてね",
    "start_text": "前半は、2つの音が続けて鳴ります。2つ目が高いか低いかを答えてください（差はだんだん小さくなります）。後半は、音が1つ鳴ります。ドレミのどれかを選んでください。分からないときは「分からない」でOK。",
    "tag": "絶対音感テスト",
    "card_label": "絶対音感・相対音感テストの結果",
    "card_footer": "あなたの耳は何タイプ？ → shimulabo.com",
    "stage_html": """
      <div class="syn-top"><span id="part">前半：2つの音のどちらが高い？</span><span id="count">1 / 16</span></div>
      <div class="syn-bar"><i id="bar"></i></div>
      <div class="syn-big" style="font-size:64px;">🎹</div>
      <div class="syn-ask" id="ask">2つ目の音は、1つ目より…</div>
      <button type="button" class="syn-go" id="play" style="background:#2A3C43;color:#EEEAE3;">▶ もう一度鳴らす</button>
      <div class="syn-btns" id="opts" style="margin-top:10px;"></div>
    """,
    "js": r"""
  const $ = NOU.$;
  let ctx = null;
  function tone(midi, t0, dur) {                 // ピアノに近い音（倍音を少し足す）
    if (!ctx) ctx = new (window.AudioContext || window.webkitAudioContext)();
    if (ctx.state === 'suspended') ctx.resume();
    const f = 440 * Math.pow(2, (midi - 69) / 12), t = ctx.currentTime + t0, g = ctx.createGain();
    g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(0.16, t + 0.02); g.gain.exponentialRampToValueAtTime(0.001, t + dur);
    [1, 2, 3, 4].forEach((h, i) => { const o = ctx.createOscillator(), gg = ctx.createGain(); o.frequency.value = f * h; gg.gain.value = [1, .45, .22, .1][i]; o.connect(gg).connect(g); o.start(t); o.stop(t + dur + .05); });
    g.connect(ctx.destination);
  }
  const NAMES = ['ド', 'ド♯', 'レ', 'レ♯', 'ミ', 'ファ', 'ファ♯', 'ソ', 'ソ♯', 'ラ', 'ラ♯', 'シ'];
  const CENTS = [400, 300, 200, 150, 100, 70, 50, 30];       // 前半：2つの音の差（半音＝100）
  let k = 0, rel = [], abs = [], cur = null;
  function play() {
    if (k < 8) { tone(cur.a, 0, 0.8); tone(cur.b, 1.0, 0.8); } else tone(cur.m, 0, 1.2);
  }
  function next() {
    $('count').textContent = (k + 1) + ' / 16'; $('bar').style.width = (k / 16 * 100) + '%';
    if (k < 8) {
      const a = 57 + Math.random() * 12, up = Math.random() < .5;
      cur = { a, b: a + (up ? 1 : -1) * CENTS[k] / 100, up };
      $('part').textContent = '前半：2つの音のどちらが高い？'; $('ask').textContent = '2つ目の音は、1つ目より…';
      $('opts').className = 'syn-btns'; $('opts').innerHTML = '<button type="button" data-v="1">高い ↑</button><button type="button" data-v="0">低い ↓</button>';
    } else {
      cur = { m: 60 + Math.floor(Math.random() * 12) };
      $('part').textContent = '後半：鳴った音の名前は？'; $('ask').textContent = 'いま鳴った音は、ドレミのどれ？';
      $('opts').className = 'syn-btns'; $('opts').style.gridTemplateColumns = 'repeat(4,1fr)';
      $('opts').innerHTML = NAMES.map((n, i) => `<button type="button" data-v="${i}">${n}</button>`).join('') + '<button type="button" data-v="-1" style="grid-column:span 4;">分からない</button>';
    }
    play();
  }
  $('play').addEventListener('click', play);
  $('opts').addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return; const v = +b.dataset.v;
    if (k < 8) rel.push((v === 1) === cur.up);
    else { const t = (cur.m - 60) % 12, d = v < 0 ? 99 : Math.min((v - t + 12) % 12, (t - v + 12) % 12); abs.push({ exact: d === 0, near: d <= 1, skip: v < 0, name: NAMES[t] }); }
    k++; if (k < 16) next(); else done();
  });
  function done() {
    const r = rel.filter(Boolean).length, ex = abs.filter(a => a.exact).length, nr = abs.filter(a => a.near).length;
    const T = ex >= 6 ? ['🎼', '音に名前が聞こえるタイプ', '鳴った音の名前を、ほとんど当てました。研究で「絶対音感」と呼ばれる聞こえ方に近いかもしれません。']
            : r >= 7 ? ['🎵', 'わずかな高さの差まで聞き分けるタイプ', '半音よりずっと小さい差まで、どちらが高いかを聞き分けました。']
            : r >= 4 ? ['🎶', 'ふつうに聞き分けるタイプ', '大きな差ははっきり、小さな差では迷いました。多くの人はこのあたりです。']
            : ['🎧', '音の雰囲気で聞くタイプ', '高さの小さな差は、聞き分けにくかったようです。スピーカーの音や、まわりの音でも結果は変わります。'];
    NOU.finish({
      label: '前半：高さの聞き分け（8問中）', big: r, unit: ' / 8 問', emoji: T[0], typeName: T[1], advice: T[2],
      extraHTML: `<div class="syn-rows"><div><span class="k">前半：どちらが高いか</span><span class="syn-meter"><i style="width:${r / 8 * 100}%"></i></span><span class="v">${r} / 8</span></div><div><span class="k">後半：音の名前（ぴったり）</span><span class="syn-meter"><i style="width:${ex / 8 * 100}%"></i></span><span class="v">${ex} / 8</span></div><div><span class="k">後半：音の名前（となりの音まで）</span><span class="v">${nr} / 8</span></div></div>
        <p style="font-size:12px;color:var(--ink-3);">当てずっぽうでも、音の名前は12回に1回くらい当たります。8問中1〜2問のぴったりは、たまたまのこともあります。</p>`,
      share: `絶対音感・相対音感テストやってみた🎹 高さの聞き分け ${r}/8・音の名前 ${ex}/8 で「${T[1]}」でした。あなたの耳は何タイプ？`,
      cardTitle: 'わたしの耳のタイプ', cardLine: `聞き分け ${r}/8・音の名前 ${ex}/8`,
      draw: (x, R) => {
        [['どちらが高いか', rel, '#4FC6B4'], ['音の名前', abs.map(a => a.exact), '#F5BB5C']].forEach(([n, arr, c], row) => {
          const y = R.y + 70 + row * 250, cw = (R.w - 7 * 16) / 8;
          x.textAlign = 'left'; x.fillStyle = '#EEEAE3'; x.font = '800 40px ' + R.F; x.fillText(n, R.x, y);
          arr.forEach((v, i) => { x.fillStyle = v ? c : '#2A3C43'; x.beginPath(); x.roundRect(R.x + i * (cw + 16), y + 30, cw, 120, 14); x.fill();
            x.fillStyle = v ? '#0D1417' : '#8D9BA1'; x.textAlign = 'center'; x.font = '900 40px ' + R.F; x.fillText(v ? '○' : '×', R.x + i * (cw + 16) + cw / 2, y + 106); });
        });
      },
    });
  }
  function start() { k = 0; rel = []; abs = []; NOU.startPanels(); next(); }
  $('startBtn').addEventListener('click', start); $('againBtn').addEventListener('click', start);
""",
    "note": "前半で2つの音の高さの差を聞き分け、後半で鳴った音の名前（ドレミ）を当てるセルフテストです。前半は相対音感、後半は絶対音感の考え方をもとにしています。",
    "article": """
    <h2>絶対音感と相対音感のちがい</h2>
    <p><b>絶対音感</b>は、ほかの音とくらべなくても、鳴った音だけを聞いて「ソ」「ド♯」と名前が分かる聞こえ方です。<b>相対音感</b>は、2つの音をくらべて「こっちが高い」「3つ上の音」と分かる聞こえ方です。多くの人は、絶対音感は持っていなくても、相対音感はある程度持っています。</p>
    <p>このテストの前半は相対音感、後半は絶対音感の考え方で作っています。前半の差は、半音4つ分（400セント）から、半音の3分の1ほど（30セント）まで、だんだん小さくなります。</p>

    <h2>話す言葉で、絶対音感の人の多さが変わる？</h2>
    <p>アメリカの音楽学校と、中国の音楽学校の学生をくらべた研究では、<b>中国の学生のほうが、絶対音感の人がずっと多い</b>という結果でした（Deutsch ほか 2006）。中国語は、同じ音でも声の高さが変わると意味が変わる「声調言語」です。研究者たちは、小さいころから声の高さに意味がある言葉を使うことが、絶対音感と関係しているのではないかと考えています。</p>
    <p>日本語にも、「はし（箸）」と「はし（橋）」のように高さで意味を分ける言葉があります。あなたの結果は、どうだったでしょうか。</p>

    <h2>当てずっぽうでも当たることがある</h2>
    <p>後半は12個の音から選ぶので、当てずっぽうでも12回に1回くらいは当たります。8問中1〜2問のぴったりは、たまたまのこともあります。8問中6問以上をぴったり当てたときは、偶然ではなかなか起きない結果です。</p>

    <h2>結果の4つのタイプ</h2>
    <div class="tbl-scroll">
    <table class="seo-table">
    <tr><th>タイプ</th><th>どんな結果？</th></tr>
    <tr><td>🎼 音に名前が聞こえるタイプ</td><td>後半の音の名前を、8問中6問以上ぴったり当てた</td></tr>
    <tr><td>🎵 わずかな高さの差まで聞き分けるタイプ</td><td>前半を8問中7問以上</td></tr>
    <tr><td>🎶 ふつうに聞き分けるタイプ</td><td>前半を8問中4〜6問</td></tr>
    <tr><td>🎧 音の雰囲気で聞くタイプ</td><td>前半が8問中3問以下</td></tr>
    </table>
    </div>
    <p>スマホのスピーカー、イヤホン、まわりの音でも結果は変わります。音の高さの聞き分けは練習で上達することも多いので、楽器や歌をやっている人とくらべてみるのもおもしろいはずです。</p>
""",
    "faq": [
        ("このテストで絶対音感があるか分かりますか？", "いいえ。遊びのためのセルフテストで、検査ではありません。8問だけなので、たまたま当たることもあります。"),
        ("ドレミの名前を知らないと、後半はできませんか？", "後半は音の名前を答えるので、ドレミを知っている人向けです。前半の「高いか低いか」は、誰でも試せます。"),
        ("音が小さくて聞こえません。", "音量を少しずつ上げてください。大きくしすぎないように気をつけてください。イヤホンを使うと聞きやすくなります。"),
        ("答えは送信されますか？", "いいえ。答えはこの画面の中だけで使い、送信も保存もしません（サイト全体のアクセス解析については<a href=\"../../privacy/\">プライバシーポリシー</a>をご覧ください）。"),
    ],
    "refs": [
        "Deutsch D, Henthorn T, Marvin E, Xu H (2006). Absolute pitch among American and Chinese conservatory students: Prevalence differences, and evidence for a speech-related critical period. <i>Journal of the Acoustical Society of America</i>, 119(2), 719–722.",
    ],
    "related": [("mimi-nenrei", "👂", "耳年齢テスト（モスキート音）"), ("sakuchou-test", "🔊", "音の錯覚テスト（上がる？下がる？）"), ("rhythm-test", "🥁", "リズム感テスト"), ("kyokankaku-test", "🔤", "共感覚テスト（文字に色が見える？）")],
}
