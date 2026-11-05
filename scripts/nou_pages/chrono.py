# -*- coding: utf-8 -*-
# 十人十脳 第11話「朝型・夜型」と連動。既存の「朝型・夜型診断（クロノタイプ）」を同じURLのまま作り直した（2026-11-05）
PAGE = {
    "slug": "chrono",
    "title": "朝型・夜型診断（クロノタイプ）｜朝型か夜型かは生まれつき？8つの質問で試す｜シミュラボ",
    "desc": "あなたは朝型？夜型？起きる時刻・頭がさえる時間・眠くなる時刻など8つの質問で、あなたのクロノタイプ（朝型・夜型の傾向）を試すセルフテスト。約70万人の遺伝子を調べた研究で分かった「朝型の遺伝子」の話も解説。診断ではありません。",
    "og_title": "朝型か夜型かは、生まれつき？｜朝型・夜型診断",
    "og_desc": "8つの質問で、あなたのクロノタイプを。約70万人の遺伝子研究の話も。",
    "ld_name": "朝型・夜型診断（クロノタイプ）",
    "h1": "朝型・夜型診断（朝型か夜型かは、生まれつき？）",
    "lead": "同じ時間に起きても、朝からすっきり動ける人と、昼すぎまで頭がぼんやりする人がいます。朝型か夜型かの傾向は「クロノタイプ」と呼ばれ、遺伝子とも関係していることが分かってきました。8つの質問に答えてください。約1分です。",
    "start_h2": "⏰ 8つの質問に答えてね",
    "start_text": "仕事や学校の予定がない「自由な日」を思い浮かべて答えてください。いちばん近いものを選べばOKです。",
    "tag": "朝型夜型",
    "card_label": "朝型・夜型診断の結果",
    "card_footer": "朝型か夜型かは生まれつき？ → shimulabo.com",
    "stage_html": """
      <div class="syn-top"><span>自由な日を思い浮かべてね</span><span id="count">1 / 8</span></div>
      <div class="syn-bar"><i id="bar"></i></div>
      <div class="syn-big" id="em" style="font-size:56px;"></div>
      <div class="syn-ask" id="q" style="font-size:18px;font-weight:700;color:#EEEAE3;min-height:3em;"></div>
      <div class="syn-btns c1" id="opts"></div>
    """,
    "js": r"""
  const $ = NOU.$;
  // 点が大きいほど朝型（研究で使われる朝型・夜型の質問票の考え方をもとに、このページで作った質問）
  const Q = [
    ['🌅', '予定のない日、自然に目がさめるのは？', [['6時より前', 4], ['6〜8時', 3], ['8〜10時', 2], ['10時より後', 1]]],
    ['🌙', '予定のない日、自然に眠くなるのは？', [['22時より前', 4], ['22〜24時', 3], ['0〜2時', 2], ['2時より後', 1]]],
    ['🧠', 'いちばん頭がさえる時間帯は？', [['朝', 4], ['昼前〜昼すぎ', 3], ['夕方', 2], ['夜', 1]]],
    ['🍞', '起きて30分以内の食欲は？', [['しっかり食べられる', 4], ['まあ食べられる', 3], ['あまり食べたくない', 2], ['まったく食べたくない', 1]]],
    ['📝', '大事なテストを受けるなら？', [['朝8時', 4], ['昼11時', 3], ['夕方15時', 2], ['夜19時', 1]]],
    ['🏃', '運動するなら、いちばん体が動く時間は？', [['朝', 4], ['昼', 3], ['夕方', 2], ['夜', 1]]],
    ['⏰', '目ざましなしで、決めた時刻に起きられる？', [['ほぼ毎回起きられる', 4], ['わりと起きられる', 3], ['あまり起きられない', 2], ['ほぼ起きられない', 1]]],
    ['🤔', '自分は朝型？夜型？', [['はっきり朝型', 4], ['どちらかといえば朝型', 3], ['どちらかといえば夜型', 2], ['はっきり夜型', 1]]],
  ];
  let k = 0, ans = [];
  function show() { const [e, q, o] = Q[k]; $('em').textContent = e; $('q').textContent = q; $('count').textContent = (k + 1) + ' / 8'; $('bar').style.width = (k / 8 * 100) + '%';
    $('opts').innerHTML = o.map(([t, v]) => `<button type="button" data-v="${v}">${t}</button>`).join(''); }
  $('opts').addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; ans.push(+b.dataset.v); k++; if (k < 8) show(); else done(); });
  function done() {
    const s = ans.reduce((a, b) => a + b, 0);   // 8〜32
    const T = s >= 28 ? ['🌅', 'はっきり朝型', '朝から頭も体もよく動くタイプです。夜ふかしをすると、次の日にひびきやすいかもしれません。']
            : s >= 23 ? ['☀️', 'どちらかといえば朝型', '朝のほうが調子が出やすいタイプです。']
            : s >= 18 ? ['🌤️', 'まん中（どちらでもない）', '朝型と夜型のまん中あたりです。多くの人はこのあたりです。']
            : s >= 13 ? ['🌆', 'どちらかといえば夜型', '夕方から夜にかけて調子が上がりやすいタイプです。']
            : ['🌙', 'はっきり夜型', '夜になるほど頭がさえるタイプです。朝早い予定は、体にとって本当の「早朝」に近いのかもしれません。'];
    const pos = (32 - s) / 24;   // 0＝朝型 … 1＝夜型
    NOU.finish({
      label: '朝型の度合い（8〜32点・大きいほど朝型）', big: s, unit: ' / 32 点', emoji: T[0], typeName: T[1], advice: T[2],
      extraHTML: `<div style="margin-top:8px;"><div style="height:16px;border-radius:8px;background:linear-gradient(90deg,#F5BB5C,#4FC6B4,#3B6FD8);position:relative;"><span style="position:absolute;top:-6px;left:calc(${pos * 100}% - 8px);width:16px;height:28px;border-radius:6px;background:#14181d;"></span></div><div style="display:flex;justify-content:space-between;font-size:12px;color:var(--ink-3);margin-top:4px;"><span>🌅 朝型</span><span>🌙 夜型</span></div></div>`,
      share: `朝型・夜型診断やってみた⏰ ${s}/32点で「${T[1]}」でした。朝型か夜型かは、生まれつき？`,
      cardTitle: 'わたしのクロノタイプ', cardLine: `朝型の度合い ${s} / 32 点`,
      draw: (x, R) => {
        const y = R.y + 230, g = x.createLinearGradient(R.x, 0, R.x + R.w, 0); g.addColorStop(0, '#F5BB5C'); g.addColorStop(.5, '#4FC6B4'); g.addColorStop(1, '#3B6FD8');
        x.fillStyle = g; x.beginPath(); x.roundRect(R.x, y, R.w, 70, 35); x.fill();
        const px = R.x + pos * R.w; x.fillStyle = '#EEEAE3'; x.beginPath(); x.arc(px, y + 35, 52, 0, Math.PI * 2); x.fill();
        x.fillStyle = '#0D1417'; x.textAlign = 'center'; x.font = '400 56px ' + R.F; x.fillText(T[0], px, y + 55);
        x.fillStyle = '#EEEAE3'; x.font = '800 40px ' + R.F; x.textAlign = 'left'; x.fillText('🌅 朝型', R.x, y + 170); x.textAlign = 'right'; x.fillText('夜型 🌙', R.x + R.w, y + 170);
      },
    });
  }
  function start() { k = 0; ans = []; NOU.startPanels(); show(); }
  $('startBtn').addEventListener('click', start); $('againBtn').addEventListener('click', start);
""",
    "note": "自由な日の起きる時刻・眠くなる時刻・頭がさえる時間など8つの質問から、朝型・夜型の傾向（クロノタイプ）を出すセルフテストです。研究で使われる朝型・夜型の質問票の考え方をもとに、問題はこのページで作っています。",
    "article": """
    <h2>クロノタイプとは</h2>
    <p>人の体には、およそ1日のリズムで眠気や体温を上げ下げする「体内時計」があります。そのリズムが早めに進む人は<b>朝型</b>、遅めに進む人は<b>夜型</b>になります。この傾向を「クロノタイプ」と呼びます。</p>
    <p>朝型・夜型を調べる質問票は、1976年に作られたものが今もよく使われています（Horne・Östberg 1976）。このページの8問は、その考え方をもとに作った簡単なものです。</p>

    <h2>朝型か夜型かは、遺伝子とも関係がある</h2>
    <p>イギリスの研究チームは、<b>約70万人（697,828人）</b>の遺伝子とクロノタイプを調べました。その結果、朝型・夜型と関係する場所が遺伝子の中に<b>351か所</b>見つかりました（Jones ほか 2019）。そこには、体内時計を動かす遺伝子も多く含まれていました。</p>
    <p>腕に付ける機械で実際の眠る時間を測った8万5千人あまりでは、朝型の遺伝子をいちばん多く持つ5%の人は、いちばん少ない5%の人より、<b>眠る時刻の真ん中が25分早い</b>という結果でした（同じ研究）。一方で、これらの遺伝子は、睡眠の長さや質とは関係が見られませんでした。</p>
    <p>つまり、朝型か夜型かは<b>ある程度は生まれつき</b>で、努力だけで決まるものではないということです。</p>

    <h2>クロノタイプと上手につき合う</h2>
    <ul>
      <li>夜型の人にとって、朝早い予定は、体内時計では「まだ夜」の時間かもしれません</li>
      <li>大事な作業は、自分の頭がさえる時間帯に置くと進めやすくなります</li>
      <li>年齢や生活でも変わるので、ときどき試してみるのもおすすめです</li>
    </ul>

    <h2>結果の5つのタイプ</h2>
    <div class="tbl-scroll">
    <table class="seo-table">
    <tr><th>タイプ</th><th>点（8〜32）</th></tr>
    <tr><td>🌅 はっきり朝型</td><td>28点以上</td></tr>
    <tr><td>☀️ どちらかといえば朝型</td><td>23〜27点</td></tr>
    <tr><td>🌤️ まん中</td><td>18〜22点</td></tr>
    <tr><td>🌆 どちらかといえば夜型</td><td>13〜17点</td></tr>
    <tr><td>🌙 はっきり夜型</td><td>12点以下</td></tr>
    </table>
    </div>
""",
    "faq": [
        ("このテストで睡眠の病気が分かりますか？", "いいえ。遊びのためのセルフテストで、検査や診断ではありません。眠れない・起きられないなどで困っているときは、医療機関に相談してください。"),
        ("夜型は直せますか？", "朝の光を浴びるなどで生活のリズムを動かすことはできますが、朝型・夜型には遺伝子も関係していることが分かっています（Jones ほか 2019）。"),
        ("平日と休日で答えが変わります。", "このテストは、予定のない「自由な日」の自分で答えてください。平日は予定に合わせているので、本来のリズムが出にくいためです。"),
        ("答えは送信されますか？", "いいえ。答えはこの画面の中だけで使い、送信も保存もしません（サイト全体のアクセス解析については<a href=\"../../privacy/\">プライバシーポリシー</a>をご覧ください）。"),
    ],
    "refs": [
        "Jones SE, Lane JM, Wood AR, ほか (2019). Genome-wide association analyses of chronotype in 697,828 individuals provides insights into circadian rhythms. <i>Nature Communications</i>, 10, 343.",
        "Horne JA, Östberg O (1976). A self-assessment questionnaire to determine morningness-eveningness in human circadian rhythms. <i>International Journal of Chronobiology</i>, 4(2), 97–110.",
    ],
    "related": [("dress-iro", "👗", "ドレスの色テスト（白と金？青と黒？）"), ("jikan-kankaku", "⏱️", "時間の感じ方テスト（30秒ぴったり？）"), ("yume-type", "💭", "夢を見る人・見ない人テスト"), ("hsp-shindan", "🌿", "HSP診断（繊細さん）")],
}
