# -*- coding: utf-8 -*-
# 十人十脳 第8話「音の錯覚（同じ音が人によってちがって聞こえる）」と連動（2026-11-05 新規）
PAGE = {
    "slug": "sakuchou-test",
    "title": "音の錯覚テスト｜同じ2つの音、上がって聞こえる？下がって聞こえる？人によって答えが割れる錯聴｜シミュラボ",
    "desc": "同じ2つの音を聞いても、「上がった」と聞こえる人と「下がった」と聞こえる人がいます。研究で「トライトーン・パラドックス」と呼ばれる音の錯覚を、12問で試すセルフテスト。ずっと上がり続けるように聞こえる不思議な音も。診断ではありません。",
    "og_title": "同じ音なのに、上がる？下がる？｜音の錯覚テスト",
    "og_desc": "同じ2つの音で、答えが人によって割れる。あなたにはどう聞こえる？",
    "ld_name": "音の錯覚テスト（上がる？下がる？）",
    "h1": "音の錯覚テスト（同じ2つの音、上がる？下がる？）",
    "lead": "2つの音が続けて鳴ります。2つ目の音は、上がりましたか？下がりましたか？かんたんそうに見えて、この音は<b>人によって答えが割れる</b>ように作られています。全部で12問、約2分です。",
    "start_h2": "🔊 音量を小さめにして、はじめてね",
    "start_text": "1問ごとに、2つの音が続けて鳴ります。2つ目が「上がった」か「下がった」か、感じたとおりに答えてください。正解はありません。",
    "start_extra": """<button type="button" class="btn btn-ghost" id="shepard" style="margin-bottom:10px;">🌀 先に「ずっと上がり続ける音」を聞いてみる</button>""",
    "tag": "音の錯覚",
    "card_label": "音の錯覚テストの結果",
    "card_footer": "同じ音なのに、上がる？下がる？ → shimulabo.com",
    "stage_html": """
      <div class="syn-top"><span>2つ目の音は？</span><span id="count">1 / 12</span></div>
      <div class="syn-bar"><i id="bar"></i></div>
      <div class="syn-big" style="font-size:64px;">🔊</div>
      <div class="syn-ask">2つ目の音は、1つ目より…</div>
      <button type="button" class="syn-go" id="play" style="background:#2A3C43;color:#EEEAE3;">▶ もう一度鳴らす</button>
      <div class="syn-btns" id="opts" style="margin-top:10px;"><button type="button" data-v="1">上がった ↑</button><button type="button" data-v="0">下がった ↓</button></div>
    """,
    "js": r"""
  const $ = NOU.$;
  let ctx = null;
  // 「シェパード音」：1オクターブずつはなれた音を重ね、真ん中の高さほど大きくした音。どのオクターブの音かが分からなくなる
  function shepard(pc, t0, dur) {
    if (!ctx) ctx = new (window.AudioContext || window.webkitAudioContext)();
    if (ctx.state === 'suspended') ctx.resume();
    const t = ctx.currentTime + t0, g = ctx.createGain();
    g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(0.13, t + 0.03); g.gain.setValueAtTime(0.13, t + dur - 0.06); g.gain.linearRampToValueAtTime(0, t + dur);
    for (let oc = 0; oc < 8; oc++) {
      const f = 32.7 * Math.pow(2, oc + pc / 12), x = Math.log2(f / 262), a = Math.exp(-x * x / 1.6);
      const o = ctx.createOscillator(), gg = ctx.createGain(); o.frequency.value = f; gg.gain.value = a / 3; o.connect(gg).connect(g); o.start(t); o.stop(t + dur + .02);
    }
    g.connect(ctx.destination);
  }
  const PCN = ['ド', 'ド♯', 'レ', 'レ♯', 'ミ', 'ファ', 'ファ♯', 'ソ', 'ソ♯', 'ラ', 'ラ♯', 'シ'];
  let order = [], k = 0, ans = {};
  const play = () => { const pc = order[k]; shepard(pc, 0, 0.5); shepard((pc + 6) % 12, 0.62, 0.5); };   // 2つ目は、ちょうど半オクターブ（三全音）はなれた音
  function next() { $('count').textContent = (k + 1) + ' / 12'; $('bar').style.width = (k / 12 * 100) + '%'; play(); }
  $('play').addEventListener('click', play);
  $('opts').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; ans[order[k]] = b.dataset.v === '1'; k++; if (k < 12) next(); else done(); });
  $('shepard').addEventListener('click', () => { for (let i = 0; i < 24; i++) shepard(i % 12, i * 0.42, 0.38); });
  function done() {
    const up = Object.values(ans).filter(Boolean).length;
    const T = up >= 9 ? ['⬆️', 'ほとんど上がって聞こえるタイプ', '12問中ほとんどで「上がった」と聞こえました。同じ音でも、反対に「下がった」と聞こえる人がいます。']
            : up <= 3 ? ['⬇️', 'ほとんど下がって聞こえるタイプ', '12問中ほとんどで「下がった」と聞こえました。同じ音でも、反対に「上がった」と聞こえる人がいます。']
            : ['🔄', '途中で切りかわるタイプ', '音の高さによって、上がって聞こえたり下がって聞こえたりしました。研究で報告されている聞こえ方の多くは、このように音の高さで切りかわります。'];
    const ring = PCN.map((n, i) => `<span style="display:inline-block;width:3.4em;margin:2px;padding:4px 0;border-radius:6px;text-align:center;font-size:12px;font-weight:800;background:${ans[i] ? 'var(--teal)' : '#f5bb5c'};color:${ans[i] ? '#fff' : '#0D1417'}">${n}${ans[i] ? '↑' : '↓'}</span>`).join('');
    NOU.finish({
      label: '12問中、「上がった」と聞こえた数', big: up, unit: ' / 12 問', emoji: T[0], typeName: T[1], advice: T[2],
      extraHTML: `<p style="font-size:13px;margin:6px 0;">1つ目の音の高さ（ドレミ）ごとの答え：</p><div>${ring}</div><p style="font-size:12px;color:var(--ink-3);margin-top:6px;">どの高さで切りかわるかは、人によってちがいます。家族や友だちと比べてみてください。</p>`,
      share: `音の錯覚テストやってみた🔊 同じ音なのに、12問中${up}問で「上がった」と聞こえて「${T[1]}」でした。あなたにはどう聞こえる？`,
      cardTitle: 'わたしの耳の聞こえ方', cardLine: `12問中 ${up}問 が上がって聞こえた`,
      draw: (x, R) => {
        const cx = R.x + R.w / 2, cy = R.y + 280, r1 = 250, r2 = 150;
        PCN.forEach((n, i) => {
          const a0 = (i / 12) * Math.PI * 2 - Math.PI / 2 - Math.PI / 12 + 0.02, a1 = a0 + Math.PI / 6 - 0.04;
          x.beginPath(); x.arc(cx, cy, r1, a0, a1); x.arc(cx, cy, r2, a1, a0, true); x.closePath();
          x.fillStyle = ans[i] ? '#4FC6B4' : '#F5BB5C'; x.fill();
          const am = (a0 + a1) / 2; x.fillStyle = '#0D1417'; x.textAlign = 'center'; x.font = '900 30px ' + R.F; x.fillText(n, cx + Math.cos(am) * 200, cy + Math.sin(am) * 200 + 10);
        });
        x.fillStyle = '#EEEAE3'; x.font = '900 46px ' + R.F; x.fillText('↑ ' + Object.values(ans).filter(Boolean).length + '  ↓ ' + Object.values(ans).filter(v => !v).length, cx, cy + 16);
      },
    });
  }
  function start() { order = Array.from({ length: 12 }, (_, i) => i).sort(() => Math.random() - .5); k = 0; ans = {}; NOU.startPanels(); next(); }
  $('startBtn').addEventListener('click', start); $('againBtn').addEventListener('click', start);
""",
    "note": "ちょうど半オクターブはなれた2つの「シェパード音」を聞いて、上がったか下がったかを答えるセルフテストです。研究で「トライトーン・パラドックス」と呼ばれる錯覚の考え方をもとにしています。",
    "article": """
    <h2>トライトーン・パラドックスとは</h2>
    <p>ちょうど半オクターブ（ピアノの鍵盤で6つ分）はなれた2つの音を、続けて鳴らします。ふつうなら「上がった」か「下がった」かは誰が聞いても同じはずです。ところが、このテストの音では、<b>ある人には上がって聞こえ、別の人には同じ音が下がって聞こえる</b>ことが報告されています（Deutsch 1991）。</p>
    <p>使っているのは、1オクターブずつはなれた音をたくさん重ねて、どのオクターブの音か分からなくした「シェパード音」です。音の高さの「どのオクターブか」という手がかりを消すと、上がったか下がったかを決めているのは、聞いている人の頭のほうになります。</p>

    <h2>聞こえ方は、音の高さで切りかわる</h2>
    <p>研究では、上がって聞こえるか下がって聞こえるかは、<b>1つ目の音がドレミのどの音か</b>によって変わることが分かっています。そして、どの音で切りかわるかが、人によってちがうのです。このテストの結果で、どの音で「上がった」「下がった」が入れかわったかを見てみてください。</p>

    <h2>話す言葉と関係がある？</h2>
    <p>この錯覚を見つけたアメリカの研究者は、聞こえ方のちがいが、<b>その人が育った地域の言葉やなまり</b>、ふだん話す声の高さと関係していると報告しました（Deutsch 1991）。一方で、オランダ・イギリス・アメリカの人をくらべた別の研究では、話す声の高さとの関係は確かめられず、音の作り方によるちがいのほうが大きいという結果でした（Repp 1994）。なぜ人によって聞こえ方が分かれるのかは、まだ決着がついていません。</p>

    <h2>ずっと上がり続ける音</h2>
    <p>はじめる前のボタンで聞ける「ずっと上がり続ける音」も、同じシェパード音で作っています。ドからシまで上がって、またドに戻っているのに、戻ったところで下がった感じがしません。どこまでも上がり続けるように聞こえるはずです。</p>

    <h2>結果の3つのタイプ</h2>
    <div class="tbl-scroll">
    <table class="seo-table">
    <tr><th>タイプ</th><th>12問中「上がった」の数</th></tr>
    <tr><td>⬆️ ほとんど上がって聞こえるタイプ</td><td>9問以上</td></tr>
    <tr><td>🔄 途中で切りかわるタイプ</td><td>4〜8問</td></tr>
    <tr><td>⬇️ ほとんど下がって聞こえるタイプ</td><td>3問以下</td></tr>
    </table>
    </div>
    <p>家族や友だちと同じスピーカーで聞きくらべると、同じ音なのに答えが割れるのを体験できます。</p>
""",
    "faq": [
        ("正解はどちらですか？", "正解はありません。どちらにも聞こえるように作った音で、どう聞こえたかが答えです。"),
        ("毎回答えがちがいます。", "音の高さ（1つ目の音がドレミのどれか）によって聞こえ方が変わるので、問題によって答えが変わるのは自然なことです。"),
        ("スピーカーで結果は変わりますか？", "変わることがあります。低い音や高い音が出にくいスピーカーでは、音の印象が変わります。イヤホンでも試してみてください。"),
        ("答えは送信されますか？", "いいえ。答えはこの画面の中だけで使い、送信も保存もしません（サイト全体のアクセス解析については<a href=\"../../privacy/\">プライバシーポリシー</a>をご覧ください）。"),
    ],
    "refs": [
        "Deutsch D (1991). The Tritone Paradox: An Influence of Language on Music Perception. <i>Music Perception</i>, 8(4), 335–347.",
        "Repp BH (1994). The Tritone Paradox and the Pitch Range of the Speaking Voice: A Dubious Connection. <i>Music Perception</i>, 12(2), 227–255.",
    ],
    "related": [("onkan-test", "🎹", "絶対音感・相対音感テスト"), ("mimi-nenrei", "👂", "耳年齢テスト（モスキート音）"), ("sakushi-kaiten", "🌀", "回転の錯視テスト（どちら回り？）"), ("naigen-test", "💬", "頭の中の声テスト")],
}
