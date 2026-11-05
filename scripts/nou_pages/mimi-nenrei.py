# -*- coding: utf-8 -*-
# 十人十脳 第5話「耳年齢（モスキート音）」と連動（2026-11-05 新規）
PAGE = {
    "slug": "mimi-nenrei",
    "title": "耳年齢テスト（モスキート音）｜この音、聞こえますか？どこまで高い音が聞こえるか試す｜シミュラボ",
    "desc": "この音、聞こえますか？8,000Hzから20,000Hzまで、少しずつ高くなる音で、あなたの耳がどこまで高い音を聞き取れるかを試す耳年齢テスト。若い人にしか聞こえにくい約17,000Hzの「モスキート音」も入っています。年をとると高い音から聞こえにくくなる理由も解説。診断ではありません。",
    "og_title": "この音、聞こえますか？｜耳年齢テスト（モスキート音）",
    "og_desc": "少しずつ高くなる音。あなたの耳はどこまで聞こえる？",
    "ld_name": "耳年齢テスト（モスキート音）",
    "h1": "耳年齢テスト（この音、聞こえますか？）",
    "lead": "同じ部屋で同じ音を鳴らしても、聞こえる人と聞こえない人がいます。8,000Hz（ヘルツ）から20,000Hzまで、少しずつ高くなる音を鳴らします。どこまで聞こえるか、試してみましょう。約2分です。",
    "start_h2": "👂 はじめる前に、音量を小さめに",
    "start_text": "スマホやパソコンの音量を<b>小さめ</b>にしてから始めてください。最初に、音量を合わせるための音が鳴ります。イヤホンを使うと、聞き取りやすくなります。",
    "start_extra": """<div class="alert" style="text-align:left;margin-bottom:12px;">⚠️ <b>音量は上げすぎないでください。</b>高い音は聞こえにくくても、大きな音は耳を傷めることがあります。途中で気分が悪くなったら、すぐにやめてください。</div>""",
    "tag": "耳年齢テスト",
    "card_label": "耳年齢テストの結果",
    "card_footer": "この音、聞こえますか？ → shimulabo.com 耳年齢テスト",
    "stage_html": """
      <div class="syn-top"><span id="step">音量を合わせる</span><span id="count"></span></div>
      <div class="syn-bar"><i id="bar"></i></div>
      <div class="syn-big" id="hz" style="font-size:64px;">🔈</div>
      <div class="syn-ask" id="ask">ふつうの高さの音（1,000Hz）が鳴ります。<br>小さく聞こえるくらいに、端末の音量を合わせてね。</div>
      <button type="button" class="syn-go" id="play" style="background:#2A3C43;color:#EEEAE3;">▶ もう一度鳴らす</button>
      <div class="syn-btns" id="ans" style="margin-top:10px;"><button type="button" data-v="1">聞こえた</button><button type="button" data-v="0">聞こえない</button></div>
      <p class="syn-note">※ スピーカーやイヤホンによっては、高い音がそもそも出ないことがあります。そのときは結果が低めに出ます。</p>
    """,
    "js": r"""
  const $ = NOU.$;
  const HZ = [8000, 10000, 12000, 14000, 15000, 16000, 17000, 18000, 19000, 20000];
  let ctx = null, seq = [], k = -1, res = {}, misses = 0, fakeYes = false;
  function tone(f) {              // 小さめの音を1.2秒。f=0 は「音を出さない」確認用の問題
    if (!ctx) ctx = new (window.AudioContext || window.webkitAudioContext)();
    if (ctx.state === 'suspended') ctx.resume();
    if (!f) return;
    const o = ctx.createOscillator(), g = ctx.createGain(), t = ctx.currentTime;
    o.type = 'sine'; o.frequency.value = f;
    g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(0.05, t + 0.05); g.gain.setValueAtTime(0.05, t + 1.15); g.gain.linearRampToValueAtTime(0, t + 1.2);
    o.connect(g).connect(ctx.destination); o.start(t); o.stop(t + 1.25);
  }
  function show() {
    if (k < 0) { $('step').textContent = '音量を合わせる'; $('count').textContent = ''; $('hz').textContent = '🔈'; tone(1000); return; }
    const f = seq[k];
    $('step').textContent = '高い音のテスト'; $('count').textContent = (k + 1) + ' / ' + seq.length; $('bar').style.width = (k / seq.length * 100) + '%';
    $('hz').textContent = '🎵'; $('ask').innerHTML = 'この音、聞こえますか？<br><small style="color:#8D9BA1;">（音の高さは結果で発表します）</small>'; tone(f);
  }
  $('play').addEventListener('click', () => tone(k < 0 ? 1000 : seq[k]));
  $('ans').addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return; const yes = b.dataset.v === '1';
    if (k < 0) { k = 0; show(); return; }
    const f = seq[k];
    if (f === 0) { if (yes) fakeYes = true; }
    else { res[f] = yes; misses = yes ? 0 : misses + 1; }
    k++;
    if (k >= seq.length || misses >= 2) done(); else show();
  });
  function done() {
    const heard = HZ.filter(f => res[f]), top = heard.length ? Math.max(...heard) : 0;
    const T = top >= 17000 ? ['🦟', 'モスキート音が聞こえる耳', '約17,000Hz以上の高い音まで聞こえました。若い人にしか聞こえにくいと言われる「モスキート音」の高さです。']
            : top >= 14000 ? ['🔔', '高い音まで届く耳', '14,000〜16,000Hzあたりまで聞こえました。それより上の音は、聞こえにくかったようです。']
            : ['🎵', '高い音は控えめな耳', '14,000Hzより高い音は、聞こえにくかったようです。スピーカーやイヤホンが高い音を出せていないこともあります。'];
    const extra = (fakeYes ? '<div class="alert" style="text-align:left;">🔍 途中に1問だけ「音を鳴らさない問題」がありましたが、そこで「聞こえた」を選んでいました。結果は少し高めに出ているかもしれません。</div>' : '')
      + `<div class="syn-rows">${HZ.filter(f => f in res).map(f => `<div><span class="k">${f.toLocaleString()} Hz</span><span class="v">${res[f] ? '聞こえた ○' : '聞こえない ×'}</span></div>`).join('')}</div>`
      + '<p style="font-size:12px;color:var(--ink-3);">「耳年齢」の数字は出していません。聞こえ方は、使っている機械・音量・まわりの音で大きく変わるためです。</p>';
    NOU.finish({
      label: '聞こえたいちばん高い音', big: top ? top.toLocaleString() : '—', unit: ' Hz', emoji: T[0], typeName: T[1], advice: T[2], extraHTML: extra,
      share: `耳年齢テストやってみた👂 ${top ? top.toLocaleString() + 'Hz' : '8,000Hzより低い音'}まで聞こえて「${T[1]}」でした。この音、あなたは聞こえる？`,
      cardTitle: 'わたしの耳に届く音', cardLine: top ? `${top.toLocaleString()} Hz まで聞こえた` : '高い音は聞こえにくかった',
      draw: (x, r) => {
        const n = HZ.length, bw = (r.w - (n - 1) * 12) / n;
        HZ.forEach((f, i) => {
          const h = 120 + i * 38, xx = r.x + i * (bw + 12), y = r.y + 520 - h;
          x.fillStyle = res[f] ? (f >= 17000 ? '#F5BB5C' : '#4FC6B4') : '#2A3C43';
          x.beginPath(); x.roundRect(xx, y, bw, h, 12); x.fill();
          x.fillStyle = '#8D9BA1'; x.textAlign = 'center'; x.font = '700 24px ' + r.F; x.fillText((f / 1000) + 'k', xx + bw / 2, r.y + 556);
        });
      },
    });
  }
  function start() {
    // 低い音から順に。途中に1問だけ「音を鳴らさない問題」をまぜる
    seq = HZ.slice(); seq.splice(3 + Math.floor(Math.random() * 5), 0, 0);
    k = -1; res = {}; misses = 0; fakeYes = false; $('bar').style.width = '0%';
    $('ask').innerHTML = 'ふつうの高さの音（1,000Hz）が鳴ります。<br>小さく聞こえるくらいに、端末の音量を合わせてね。';
    NOU.startPanels(); show();
  }
  $('startBtn').addEventListener('click', start); $('againBtn').addEventListener('click', start);
""",
    "note": "8,000Hzから20,000Hzまで、少しずつ高くなる音を鳴らして、どこまで聞こえるかを試すセルフテストです。途中に1問だけ「音を鳴らさない問題」がまざっています。",
    "article": """
    <h2>年をとると、高い音から聞こえにくくなる</h2>
    <p>年齢とともに聞こえ方がゆっくり変わることを「加齢性難聴」と呼びます。研究のまとめでは、特に<b>高い音の聞こえ</b>と、音がどこから来たかを聞き分ける力が下がっていく、とされています（Sun ほか 2025）。</p>
    <p>アメリカの国立研究機関によると、アメリカでは<b>65〜74歳のおよそ3人に1人</b>、75歳より上では<b>およそ半分</b>の人が、聞こえにくさを感じています（NIDCD）。</p>

    <h2>「モスキート音」とは</h2>
    <p>2005年、イギリスで、店の前にたまる若者を立ち去らせるための装置が作られました。発明した人の説明では、<b>およそ17,000Hz</b>の音を、鳴らしたり止めたりするものです（NPR 2005）。年をとると聞こえにくくなる高さの音なので、主に若い人にだけ聞こえます。のちに、この音は「大人に聞こえない着信音」としても広まりました。</p>
    <p>このテストの17,000Hzの音が聞こえたら、その「モスキート音」の高さまで届いていることになります。</p>

    <h2>結果が機械で変わる理由</h2>
    <ul>
      <li>スマホのスピーカーや安いイヤホンは、高い音を出すのが苦手なことがあります。そのときは、耳ではなく機械のほうで音が止まっています</li>
      <li>音量の大きさ、まわりの音、部屋の広さでも聞こえ方は変わります</li>
      <li>だからこのページでは、「耳年齢◯歳」という数字は出していません。同じ機械で、家族や友だちと比べるのがおすすめです</li>
    </ul>

    <h2>耳を守るために</h2>
    <p>大きな音を長い時間聞くことは、聞こえを傷める原因になります。音量を下げる、大きな音のそばにいる時間を短くする、耳せんを使う、といったことが勧められています（NIDCD）。このテストも、<b>小さめの音量</b>で試してください。</p>

    <h2>結果の3つのタイプ</h2>
    <div class="tbl-scroll">
    <table class="seo-table">
    <tr><th>タイプ</th><th>聞こえたいちばん高い音</th></tr>
    <tr><td>🦟 モスキート音が聞こえる耳</td><td>17,000Hz以上</td></tr>
    <tr><td>🔔 高い音まで届く耳</td><td>14,000〜16,000Hz</td></tr>
    <tr><td>🎵 高い音は控えめな耳</td><td>14,000Hzより下</td></tr>
    </table>
    </div>
    <p>2回続けて「聞こえない」を選んだところで、テストは終わります。聞こえ方が気になるときは、耳鼻科で聴力の検査を受けられます。</p>
""",
    "faq": [
        ("このテストで聴力が分かりますか？", "いいえ。遊びのためのセルフテストで、聴力の検査や診断ではありません。使っている機械や音量で結果が大きく変わります。聞こえが気になるときは、耳鼻科で検査を受けられます。"),
        ("「耳年齢」の数字は出ないのですか？", "出していません。同じ人でも、スピーカーやイヤホン、音量、まわりの音で結果が変わるためです。同じ機械で、家族や友だちと比べてみてください。"),
        ("高い音が全然聞こえませんでした。", "スマホのスピーカーなど、高い音をそもそも出せない機械があります。イヤホンに変えて、もう一度試してみてください。"),
        ("音量はどのくらいにすればいいですか？", "最初の1,000Hzの音が、小さく聞こえるくらいです。それ以上は上げないでください。大きな音は耳を傷めることがあります。"),
        ("答えは送信されますか？", "いいえ。答えはこの画面の中だけで使い、送信も保存もしません（サイト全体のアクセス解析については<a href=\"../../privacy/\">プライバシーポリシー</a>をご覧ください）。"),
    ],
    "refs": [
        "Sun S, Zhao Q, He H, ほか (2025). Pathophysiological insights and therapeutic developments in age-related hearing loss: a narrative review. <i>Frontiers in Aging Neuroscience</i>, 17, 1657603.",
        "National Institute on Deafness and Other Communication Disorders (NIDCD). Age-Related Hearing Loss (Presbycusis).",
        "NPR (2005). Teens Turn 'Repeller' into Adult-Proof Ringtone.（発明者 Howard Stapleton 氏へのインタビュー）",
    ],
    "related": [("naigen-test", "💬", "頭の中の声テスト"), ("aphantasia-test", "🍎", "アファンタジア テスト（頭の中の映像）"), ("rhythm-test", "🥁", "リズム感テスト"), ("shikikaku-test", "🎨", "色覚テスト（あなたの目は何色型？）")],
}
