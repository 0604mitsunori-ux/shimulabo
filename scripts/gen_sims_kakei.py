# -*- coding: utf-8 -*-
"""シミュラボ：新カテゴリ「家系・ルーツ」5本。家系・血縁を"数字で体感"する（先祖の人数/親等/血縁度/子孫/続柄の呼び方）。write_all再利用。"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims11 import faq, write_all

KAKEI = '家系・ルーツ'
SIMS = []
def add(**k): k['cat']=KAKEI; SIMS.append(k)
def C(t): return '<div class="note" style="border-left:4px solid var(--teal)"><strong>ポイント</strong>：'+t+'</div>'
def REF(items): return '<h2>参考</h2><ul class="seo-refs">'+''.join('<li>'+i+'</li>' for i in items)+'</ul>'

# ============================================================
# 1. 先祖の人数 計算（バズ・感動系／低KD）
# ============================================================
add(id='senzo-ninzu', emoji='🌳',
  title='先祖の人数 計算｜◯代前のご先祖は何人？あなたに繋がった命の数｜シミュラボ',
  desc='「10代前のご先祖は何人？」を一発計算。世代をさかのぼるとご先祖の人数はねずみ算式に増えます。あなたに命を繋いだ先祖の総数を体感できる無料ツール。',
  ogtitle='先祖の人数 計算｜◯代前のご先祖は何人？', ogdesc='◯代前のご先祖の人数と、繋がった命の総数を計算。',
  h1='先祖の人数 計算',
  lead='「10代前のご先祖は何人いる？」を一発計算。父母は2人、祖父母は4人…と、さかのぼるほど倍々に増えるご先祖の数を体感できます。',
  inputs='''    <h2>🌳 何代前を調べる？</h2>
    <div class="field"><label>さかのぼる世代 <span class="hint">（代前）</span></label><input type="number" id="n" value="10" min="1" max="40" inputmode="numeric"></div>
    <div class="field"><label>1世代の年数 <span class="hint">（年・目安）</span></label><input type="number" id="y" value="30" min="15" max="40" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">ご先祖の人数を見る</button>''',
  result='''      <div class="label">その代の直系ご先祖</div>
      <div class="big"><span id="big">0</span><span class="unit">人</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1〜その代までの合計</div><div class="v accent" id="total">—</div></div>
      <div class="stat"><div class="k">何年前ごろ</div><div class="v" id="years">—</div></div>
      <div class="stat"><div class="k">あなたに繋がった命</div><div class="v" id="inochi">—</div></div></div>''',
  article=C('直系のご先祖は、1代前（父母）＝2人、2代前（祖父母）＝4人…と<b>1代さかのぼるごとに2倍</b>に増えます。n代前のご先祖は 2ⁿ 人。だから10代前で1,024人、20代前ではなんと約104万人にもなります。')+'''
    <h2>ご先祖の人数 早見表</h2>
    <table class="seo-table"><tr><th>世代</th><th>その代のご先祖</th><th>年代の目安（1世代30年）</th></tr>
    <tr><td>5代前</td><td>32人</td><td>約150年前（幕末〜明治）</td></tr>
    <tr><td>10代前</td><td>1,024人</td><td>約300年前（江戸中期）</td></tr>
    <tr><td>15代前</td><td>32,768人</td><td>約450年前（戦国）</td></tr>
    <tr><td>20代前</td><td>約104万人</td><td>約600年前（室町）</td></tr>
    <tr><td>25代前</td><td>約3,355万人</td><td>約750年前（鎌倉）</td></tr>
    <tr><td>30代前</td><td>約10.7億人</td><td>約900年前（平安）</td></tr></table>
    <div class="note"><strong>※理論上の数字です</strong><br>さかのぼると人数が当時の人口を超えますが、これは<b>同じご先祖が複数の家系に重複して登場する（祖先の共有）</b>ため。実際にはもっと少ない人数のご先祖を、みんなが少しずつ共有しています。それでも「膨大な命のバトンの先に自分がいる」ことは変わりません。</div>
    <p>ご先祖との血のつながりの濃さは <a href="/sims/ketsuen/">血のつながり（血縁度）計算</a>、親戚の距離感は <a href="/sims/shinto-keisan/">親等 計算</a> で体感できます。逆に未来の子孫の数は <a href="/sims/shison-sim/">子孫シミュレーター</a> でどうぞ。</p>
    <h2>よくある質問</h2>'''+faq([
    ('10代前のご先祖は何人？','2の10乗で1,024人です。父母2人から倍々に増えるため、10代でこの人数になります。'),
    ('なぜ人口より多くなるの？','同じ人物が複数の家系に共通のご先祖として登場する「祖先の共有」が起きるためです。理論値と実際の人数はこの分だけ差が出ます。'),
    ('1世代は何年？','一般に25〜30年が目安とされます。本ツールでは年数を変更して年代の目安を調整できます。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['系図・世代の一般的な数え方（1世代≈25〜30年）']),
  js='''  function calc(){
    const n=Math.max(1,Math.min(40,Math.floor(+$('n').value||10)));
    const y=Math.max(15,Math.min(40,+$('y').value||30));
    const gen=Math.pow(2,n), total=Math.pow(2,n+1)-2;
    const years=n*y, seireki=2026-years;
    $('sub').textContent=`${n}代前 ＝ 約${years}年前（西暦${seireki}年ごろ）`;
    $('total').textContent=num(total)+'人';
    $('years').textContent='約'+num(years)+'年前';
    $('inochi').textContent=num(total+1)+'人';
    show();anim($('big'),0,gen,900);
    SHARE=`先祖の人数、${n}代前のご先祖は ${num(gen)}人（合計${num(total)}人）でした🌳 膨大な命のバトンの先に私がいる…！`;
  }''')

# ============================================================
# 2. 親等 計算（実用SEO：相続・忌引き・結婚）
# ============================================================
add(id='shinto-keisan', emoji='📐',
  title='親等 計算｜いとこは何親等？続柄から親等を早見｜シミュラボ',
  desc='続柄を選ぶだけで、親等（しんとう）と直系・傍系、結婚できる関係かどうかを表示する無料ツール。相続・忌引き・結婚の確認に。いとこは4親等など早見表付き。',
  ogtitle='親等 計算｜いとこは何親等？', ogdesc='続柄から親等・直系傍系・婚姻の可否を早見。',
  h1='親等 計算ツール',
  lead='「いとこは何親等？」を続柄を選ぶだけで判定。親等の数、直系・傍系の別、結婚できる関係かどうかまで分かります。相続・忌引き・結婚の確認に。',
  inputs='''    <h2>📐 続柄を選ぶ</h2>
    <div class="field"><label>あなたから見た相手</label><select id="rel">
      <option value="1|直系|父母・子ども">父母／子ども</option>
      <option value="2|直系|祖父母・孫">祖父母／孫</option>
      <option value="2|傍系|兄弟姉妹" selected>兄弟姉妹</option>
      <option value="3|直系|曾祖父母・ひ孫">曾祖父母／ひ孫</option>
      <option value="3|傍系|おじ・おば／甥・姪">おじ・おば／甥・姪</option>
      <option value="4|直系|高祖父母">高祖父母（曾祖父母の親）</option>
      <option value="4|傍系|いとこ">いとこ</option>
      <option value="5|傍系|いとこの子／親のいとこ">いとこの子／親のいとこ</option>
      <option value="6|傍系|はとこ（再従兄弟姉妹）">はとこ（またいとこ）</option>
    </select></div>
    <button class="btn btn-primary" id="calcBtn">親等を計算する</button>''',
  result='''      <div class="label">親等</div>
      <div class="big"><span id="big">0</span><span class="unit">親等</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">系統</div><div class="v accent" id="kei">—</div></div>
      <div class="stat"><div class="k">続柄</div><div class="v" id="rel2">—</div></div>
      <div class="stat"><div class="k">結婚できる？</div><div class="v" id="kon">—</div></div></div>''',
  article=C('親等（しんとう）は親族の遠近を数字で表したもの。本人から相手まで、世代を1つたどるごとに1親等ずつ数えます。父母は1親等、祖父母や兄弟姉妹は2親等、いとこは4親等です。')+'''
    <h2>親等の早見表</h2>
    <table class="seo-table"><tr><th>続柄</th><th>親等</th><th>系統</th></tr>
    <tr><td>父母・子</td><td>1親等</td><td>直系</td></tr>
    <tr><td>祖父母・孫</td><td>2親等</td><td>直系</td></tr>
    <tr><td>兄弟姉妹</td><td>2親等</td><td>傍系</td></tr>
    <tr><td>曾祖父母・ひ孫</td><td>3親等</td><td>直系</td></tr>
    <tr><td>おじ・おば／甥・姪</td><td>3親等</td><td>傍系</td></tr>
    <tr><td>いとこ</td><td>4親等</td><td>傍系</td></tr>
    <tr><td>はとこ（またいとこ）</td><td>6親等</td><td>傍系</td></tr></table>
    <p>結婚（婚姻）は、直系血族と3親等以内の傍系血族の間ではできません。<b>いとこ（4親等）同士は法律上、結婚できます</b>。相続や忌引きの範囲も親等をもとに決まる場面が多く、知っておくと便利です。詳しい血のつながりの濃さは <a href="/sims/ketsuen/">血縁度計算</a>、難しい続柄の呼び方は <a href="/sims/oitoko/">続柄・呼び方 判定</a> をどうぞ。</p>
    <h2>よくある質問</h2>'''+faq([
    ('いとこは何親等？','4親等（傍系血族）です。自分→親→祖父母→おじおば→いとこ、と4世代分たどります。'),
    ('いとこ同士は結婚できる？','日本の民法では、いとこ（4親等）同士の婚姻は認められています。禁止されるのは直系血族と3親等以内の傍系血族です。'),
    ('親等はどこで使う？','相続人の範囲、忌引き休暇の日数、婚姻の可否、扶養の範囲など、親族関係を扱う多くの場面で使われます。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['民法（親族・親等・婚姻の要件）']),
  js='''  function calc(){
    const v=($('rel').value||'2|傍系|兄弟姉妹').split('|');
    const shinto=+v[0], kei=v[1], rel=v[2];
    let kon;
    if(kei==='直系') kon='×（不可）';
    else kon = shinto>=4 ? '○（可能）' : '×（不可）';
    $('sub').textContent=`${rel}（${kei}血族）`;
    $('kei').textContent=kei; $('rel2').textContent=rel; $('kon').textContent=kon;
    show();anim($('big'),0,shinto,700);
    SHARE=`親等 計算、${rel}は「${shinto}親等（${kei}）」でした📐`;
  }''')

# ============================================================
# 3. 血のつながり（血縁度）計算
# ============================================================
add(id='ketsuen', emoji='🩸',
  title='血のつながり 計算｜親子・いとこの血縁度は何％？｜シミュラボ',
  desc='親子・きょうだい・いとこなど、続柄ごとの血のつながりの濃さ（血縁度）を％で表示する無料ツール。いとこは12.5%など、血縁の濃さを体感できます。',
  ogtitle='血のつながり 計算｜血縁度は何％？', ogdesc='続柄ごとの血縁度（血のつながりの濃さ）を％で表示。',
  h1='血のつながり（血縁度）計算',
  lead='親子は50%、いとこは12.5%…。続柄を選ぶと、血のつながりの濃さ（血縁度）を％で表示します。「どのくらい血がつながっているか」を体感できます。',
  inputs='''    <h2>🩸 続柄を選ぶ</h2>
    <div class="field"><label>あなたと相手の関係</label><select id="rel">
      <option value="50|親子">親子</option>
      <option value="50|兄弟姉妹（両親が同じ）" selected>兄弟姉妹（両親が同じ）</option>
      <option value="25|祖父母と孫">祖父母と孫</option>
      <option value="25|おじ・おば／甥・姪">おじ・おば／甥・姪</option>
      <option value="25|異母・異父きょうだい">異母・異父きょうだい</option>
      <option value="12.5|いとこ">いとこ</option>
      <option value="12.5|曾祖父母とひ孫">曾祖父母とひ孫</option>
      <option value="3.125|はとこ（またいとこ）">はとこ（またいとこ）</option>
    </select></div>
    <button class="btn btn-primary" id="calcBtn">血縁度を計算する</button>''',
  result='''      <div class="label">血のつながりの濃さ</div>
      <div class="big"><span id="big">0</span><span class="unit">%</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">分数でいうと</div><div class="v accent" id="bunsu">—</div></div>
      <div class="stat"><div class="k">続柄</div><div class="v" id="rel2">—</div></div>
      <div class="stat"><div class="k">親等の目安</div><div class="v" id="shinto">—</div></div></div>''',
  article=C('血縁度は「2人が平均してどれくらい同じ遺伝子を受け継いでいるか」を表す割合。世代を1つたどるごとに1/2ずつ薄まります。親子・きょうだいは50%、祖父母と孫やおじ甥は25%、いとこは12.5%です。')+'''
    <h2>血縁度の早見表</h2>
    <table class="seo-table"><tr><th>続柄</th><th>血縁度</th><th>分数</th></tr>
    <tr><td>親子／きょうだい</td><td>50%</td><td>1/2</td></tr>
    <tr><td>祖父母と孫／おじ甥</td><td>25%</td><td>1/4</td></tr>
    <tr><td>いとこ</td><td>12.5%</td><td>1/8</td></tr>
    <tr><td>はとこ</td><td>3.125%</td><td>1/32</td></tr></table>
    <p>「思ったより濃い／薄い」と感じたのではないでしょうか。遠いご先祖ほど血のつながりは薄くなりますが、その分たくさんの家系とつながっているとも言えます。ご先祖の人数は <a href="/sims/senzo-ninzu/">先祖の人数 計算</a>、親戚の距離は <a href="/sims/shinto-keisan/">親等 計算</a> で確かめられます。</p>
    <h2>よくある質問</h2>'''+faq([
    ('いとこはどれくらい血がつながってる？','血縁度は12.5%（8分の1）です。共通の祖父母から、それぞれ2世代分（各1/4）たどるためです。'),
    ('親子ときょうだいはなぜ同じ50%？','親子は必ず半分を受け継ぎ、きょうだいは平均して半分の遺伝子を共有するため、どちらも約50%になります。'),
    ('血縁度は相続に関係する？','相続の順位や割合は民法で別途定められており、血縁度そのものとは異なります。血縁度は遺伝的な近さの目安です。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['血縁度（近交・遺伝的関係の一般的な定義）']),
  js='''  function calc(){
    const v=($('rel').value||'50|兄弟姉妹').split('|');
    const pct=+v[0], rel=v[1];
    const denom=Math.round(100/pct);
    const shintoMap={'50':'1〜2親等','25':'2〜3親等','12.5':'4親等','3.125':'6親等'};
    $('sub').textContent=`${rel}の血のつながり`;
    $('bunsu').textContent=denom+'分の1'; $('rel2').textContent=rel;
    $('shinto').textContent=shintoMap[String(pct)]||'—';
    show();anim($('big'),0,pct,700, pct<10?1:0);
    SHARE=`血のつながり、${rel}は「${pct}%（${denom}分の1）」でした🩸`;
  }''')

# ============================================================
# 4. 子孫シミュレーター（逆方向・雑学）
# ============================================================
add(id='shison-sim', emoji='👶',
  title='子孫シミュレーター｜◯世代後にあなたの子孫は何人？｜シミュラボ',
  desc='1人あたりの子どもの数と世代数から、未来にあなたの子孫が何人になるかを計算する無料ツール。ねずみ算式に増える子孫の数を体感できます。',
  ogtitle='子孫シミュレーター｜◯世代後に子孫は何人？', ogdesc='子の数と世代数から、未来の子孫の人数を計算。',
  h1='子孫シミュレーター',
  lead='「10世代後に自分の子孫は何人？」を計算。1人あたりの子どもの数を決めると、未来へ向かってねずみ算式に増えていく子孫の数を体感できます。',
  inputs='''    <h2>👶 条件を入れる</h2>
    <div class="row"><div class="field"><label>1人あたりの子ども <span class="hint">（人）</span></label><input type="number" id="c" value="2" min="1" max="10" step="0.5" inputmode="decimal"></div>
    <div class="field"><label>何世代後 <span class="hint">（代）</span></label><input type="number" id="g" value="10" min="1" max="40" inputmode="numeric"></div></div>
    <div class="field"><label>1世代の年数 <span class="hint">（年）</span></label><input type="number" id="y" value="30" min="15" max="40" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">子孫の人数を見る</button>''',
  result='''      <div class="label">その世代の子孫</div>
      <div class="big"><span id="big">0</span><span class="unit">人</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">累計の子孫</div><div class="v accent" id="total">—</div></div>
      <div class="stat"><div class="k">何年後</div><div class="v" id="years">—</div></div>
      <div class="stat"><div class="k">西暦</div><div class="v" id="seireki">—</div></div></div>''',
  article=C('あなたの子どもがc人、その子どもたちもそれぞれc人…と続くと、g世代後の子孫は cᵍ 人。1人あたり2人でも、10世代後には1,024人になります。ご先祖をさかのぼるのと同じ「倍々の力」が、未来にも働きます。')+'''
    <h2>子孫の増え方（1人あたり2人の場合）</h2>
    <table class="seo-table"><tr><th>世代後</th><th>その世代の子孫</th><th>年代の目安</th></tr>
    <tr><td>5世代後</td><td>32人</td><td>約150年後</td></tr>
    <tr><td>10世代後</td><td>1,024人</td><td>約300年後</td></tr>
    <tr><td>15世代後</td><td>32,768人</td><td>約450年後</td></tr>
    <tr><td>20世代後</td><td>約104万人</td><td>約600年後</td></tr></table>
    <div class="note"><strong>※理論上の数字です</strong><br>実際は結婚・出生率・重複などで大きく変わります。あくまで「倍々で増えるとどうなるか」を体感するシミュレーションです。</div>
    <p>反対に、過去のご先祖の人数は <a href="/sims/senzo-ninzu/">先祖の人数 計算</a> で分かります。あわせて試すと、自分が「命のバトン」の途中にいることを実感できます。</p>
    <h2>よくある質問</h2>'''+faq([
    ('本当にこんなに増えるの？','これは全員がちょうどc人の子を持ち続けた場合の理論値です。実際は出生率や社会状況で大きく変動します。'),
    ('1人あたり2人だと人口は増える？','夫婦2人から子2人だと人口は横ばいですが、「1人の自分から見た子孫」は倍々に増えていきます。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['指数的増加（ねずみ算）の一般的な考え方']),
  js='''  function calc(){
    const c=Math.max(1,+$('c').value||2), g=Math.max(1,Math.min(40,Math.floor(+$('g').value||10))), y=Math.max(15,Math.min(40,+$('y').value||30));
    const gen=Math.pow(c,g);
    const total = c===1 ? c*g : c*(Math.pow(c,g)-1)/(c-1);
    const years=g*y, seireki=2026+years;
    $('sub').textContent=`1人${c}人の子・${g}世代後`;
    $('total').textContent=num(total)+'人';
    $('years').textContent='約'+num(years)+'年後';
    $('seireki').textContent=num(seireki)+'年';
    show();anim($('big'),0,gen,900);
    SHARE=`子孫シミュ、1人${c}人の子で${g}世代後の子孫は ${num(gen)}人でした👶`;
  }''')

# ============================================================
# 5. 続柄・呼び方 判定（はとこ・またいとこ等）
# ============================================================
add(id='oitoko', emoji='👨‍👩‍👧‍👦',
  title='続柄の呼び方 判定｜はとこ・またいとこ・大おじは何と呼ぶ？｜シミュラボ',
  desc='「いとこの子」「親のいとこ」など分かりにくい親戚の正しい呼び方・読み方・親等・血縁度を表示する無料ツール。はとこ・またいとこ・大おじの違いもすっきり。',
  ogtitle='続柄の呼び方 判定｜はとこ・大おじは？', ogdesc='分かりにくい親戚の正しい呼び方・親等・血縁度を表示。',
  h1='続柄・呼び方 判定',
  lead='「いとこの子」「親のいとこ」って何と呼ぶ？ 関係を選ぶと、正しい呼び方・読み方・親等・血のつながりまで一気に分かります。年賀状や法事での「あれ？」を解決。',
  inputs='''    <h2>👨‍👩‍👧‍👦 関係を選ぶ</h2>
    <div class="field"><label>その人はあなたの…</label><select id="rel">
      <option value="ico-ko">いとこの子ども</option>
      <option value="oya-ico">親のいとこ</option>
      <option value="ico-ico" selected>いとこのいとこ（親同士がいとこ）</option>
      <option value="sofu-kyodai">祖父母の兄弟姉妹</option>
      <option value="himago">孫の子ども</option>
      <option value="haigu-oya">配偶者の親</option>
    </select></div>
    <button class="btn btn-primary" id="calcBtn">呼び方を調べる</button>''',
  result='''      <div class="label">一般的な呼び方</div>
      <div class="big" style="font-size:30px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">正式な呼び方</div><div class="v accent" id="seishiki">—</div></div>
      <div class="stat"><div class="k">親等</div><div class="v" id="shinto">—</div></div>
      <div class="stat"><div class="k">血のつながり</div><div class="v" id="blood">—</div></div></div>''',
  article=C('親戚の呼び方は、世代がずれたり枝分かれしたりすると急に分かりにくくなります。「いとこの子」は<b>いとこ違い（従甥・従姪）</b>、「親同士がいとこ」なら<b>はとこ（またいとこ）</b>。関係を選ぶだけで正しい呼び方が分かります。')+'''
    <h2>分かりにくい続柄 早見表</h2>
    <table class="seo-table"><tr><th>関係</th><th>一般的な呼び方</th><th>正式な呼び方</th></tr>
    <tr><td>いとこの子ども</td><td>いとこ違い／いとこ甥・姪</td><td>従甥・従姪（じゅうせい・じゅうてつ）</td></tr>
    <tr><td>親のいとこ</td><td>いとこおじ・いとこおば</td><td>従叔父母（じゅうしゅくふぼ）</td></tr>
    <tr><td>親同士がいとこ</td><td>はとこ・またいとこ</td><td>再従兄弟姉妹（さいじゅうけいていしまい）</td></tr>
    <tr><td>祖父母の兄弟姉妹</td><td>大おじ・大おば</td><td>従祖父母（じゅうそふぼ）</td></tr></table>
    <p>親等の数え方は <a href="/sims/shinto-keisan/">親等 計算</a>、血のつながりの濃さは <a href="/sims/ketsuen/">血縁度計算</a> で数字にできます。ご先祖の人数は <a href="/sims/senzo-ninzu/">先祖の人数 計算</a> をどうぞ。</p>
    <h2>よくある質問</h2>'''+faq([
    ('はとことまたいとこは同じ？','はい、どちらも「親同士がいとこ」の関係で、正式には再従兄弟姉妹（6親等）です。地域により呼び方が変わります。'),
    ('いとこの子は何と呼ぶ？','一般に「いとこ違い」、正式には従甥（じゅうせい）・従姪（じゅうてつ）と呼びます。5親等です。'),
    ('データは送信されますか？','いいえ。判定はすべてブラウザ内で完結します。')])+REF(['親族の呼称（続柄の一般的な呼び方）']),
  js='''  function calc(){
    const R={
      'ico-ko':   {yobi:'いとこ違い', seishiki:'従甥・従姪（じゅうせい・じゅうてつ）', shinto:'5親等', blood:'約6.25%', sub:'あなたのいとこの子どもにあたります。'},
      'oya-ico':  {yobi:'いとこおじ・いとこおば', seishiki:'従叔父母（じゅうしゅくふぼ）', shinto:'5親等', blood:'約6.25%', sub:'あなたの親のいとこ。親戚の集まりで会う目上の方です。'},
      'ico-ico':  {yobi:'はとこ（またいとこ）', seishiki:'再従兄弟姉妹（さいじゅうけいていしまい）', shinto:'6親等', blood:'約3.125%', sub:'親同士がいとこ。祖父母の代でつながる関係です。'},
      'sofu-kyodai':{yobi:'大おじ・大おば', seishiki:'従祖父母（じゅうそふぼ）', shinto:'4親等', blood:'約6.25%', sub:'あなたの祖父母の兄弟姉妹にあたります。'},
      'himago':   {yobi:'ひ孫（曾孫）', seishiki:'曾孫（そうそん・ひまご）', shinto:'3親等', blood:'12.5%', sub:'あなたの孫の子ども。直系のひ孫です。'},
      'haigu-oya':{yobi:'義父・義母', seishiki:'姻族1親等（義理の父母）', shinto:'1親等（姻族）', blood:'0%（血縁なし）', sub:'配偶者の親。血のつながりはありませんが近い姻族です。'}
    };
    const r=R[$('rel').value]||R['ico-ico'];
    $('big').textContent=r.yobi;
    $('sub').textContent=r.sub;
    $('seishiki').textContent=r.seishiki; $('shinto').textContent=r.shinto; $('blood').textContent=r.blood;
    show();
    SHARE=`続柄・呼び方 判定、その人は「${r.yobi}」でした👨‍👩‍👧‍👦（${r.shinto}）`;
  }''')

if __name__=='__main__':
    write_all(SIMS)
    print(f'kakei done. {len(SIMS)} sims.')
