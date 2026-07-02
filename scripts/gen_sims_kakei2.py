# -*- coding: utf-8 -*-
"""シミュラボ：「家系・ルーツ」追加10本（仏事・血縁遺伝・親族呼称・ルーツ）。write_all再利用。既存カテゴリkakeiに追加。"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims11 import faq, write_all

KAKEI = '家系・ルーツ'
SIMS = []
def add(**k): k['cat']=KAKEI; SIMS.append(k)
def C(t): return '<div class="note" style="border-left:4px solid var(--teal)"><strong>ポイント</strong>：'+t+'</div>'
def REF(items): return '<h2>参考</h2><ul class="seo-refs">'+''.join('<li>'+i+'</li>' for i in items)+'</ul>'

# ============================================================
# 1. 忌引き 日数 早見
# ============================================================
add(id='kibiki', emoji='🕊️',
  title='忌引き 日数 早見｜続柄別に何日休める？会社・学校の目安｜シミュラボ',
  desc='亡くなった方との続柄から、忌引き休暇の日数の一般的な目安を表示する無料ツール。配偶者10日・父母7日など、会社や学校でよく使われる日数の目安が分かります。',
  ogtitle='忌引き 日数 早見｜続柄別に何日休める？', ogdesc='続柄から忌引き休暇の日数の一般的な目安を表示。',
  h1='忌引き 日数 早見',
  lead='「祖父母だと忌引きは何日？」を続柄を選ぶだけで確認。会社・学校で一般的に用いられる忌引き休暇の日数の目安を表示します（正式には各規定によります）。',
  inputs='''    <h2>🕊️ 続柄を選ぶ</h2>
    <div class="field"><label>亡くなった方はあなたの…</label><select id="rel">
      <option value="10|配偶者">配偶者</option>
      <option value="7|父母（実父母）" selected>父母</option>
      <option value="5|子ども">子ども</option>
      <option value="3|祖父母">祖父母</option>
      <option value="3|兄弟姉妹">兄弟姉妹</option>
      <option value="1|孫">孫</option>
      <option value="1|おじ・おば">おじ・おば</option>
      <option value="3|配偶者の父母">配偶者の父母</option>
      <option value="1|配偶者の祖父母・兄弟姉妹">配偶者の祖父母・兄弟姉妹</option>
    </select></div>
    <button class="btn btn-primary" id="calcBtn">忌引き日数を見る</button>''',
  result='''      <div class="label">忌引き日数の目安</div>
      <div class="big"><span id="big">0</span><span class="unit">日</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">続柄</div><div class="v accent" id="rel2">—</div></div>
      <div class="stat"><div class="k">数え方</div><div class="v" id="kazoe">—</div></div>
      <div class="stat"><div class="k">性質</div><div class="v" id="seishitsu">—</div></div></div>''',
  article=C('忌引き（きびき）は、近親者が亡くなったときに喪に服すための休暇です。<b>法律で定められた休暇ではなく、会社の就業規則や学校の規定で決められる慣例</b>のため、日数は勤務先・学校によって異なります。本ツールは一般によく使われる目安です。')+'''
    <h2>忌引き日数の一般的な目安</h2>
    <table class="seo-table"><tr><th>続柄</th><th>日数の目安</th></tr>
    <tr><td>配偶者</td><td>10日</td></tr>
    <tr><td>父母（実父母）</td><td>7日</td></tr>
    <tr><td>子ども</td><td>5日</td></tr>
    <tr><td>祖父母・兄弟姉妹</td><td>3日</td></tr>
    <tr><td>配偶者の父母</td><td>3日</td></tr>
    <tr><td>孫・おじおば・配偶者の祖父母</td><td>1日</td></tr></table>
    <p>喪主を務める場合は日数が長めに設定されることもあります。日数の数え方（亡くなった日から／葬儀日から）や連続・分割の扱いも規定によります。続柄の距離感は <a href="/sims/shinto-keisan/">親等 計算</a>、法要の時期は <a href="/sims/shijukunichi/">四十九日・忌日 計算</a> で確認できます。</p>
    <h2>よくある質問</h2>'''+faq([
    ('忌引きは法律で決まってる？','いいえ。法定の休暇ではなく、会社の就業規則や学校の規定による慣例です。必ず勤務先・学校にご確認ください。'),
    ('祖父母の忌引きは何日？','一般的な目安は3日ですが、規定により1〜3日と幅があります。'),
    ('土日はカウントする？','連続日数で数える場合が多いですが、扱いは規定によります。'),
    ('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')])+REF(['一般的な忌引き（慶弔休暇）日数の目安']),
  js='''  function calc(){
    const v=($('rel').value||'7|父母').split('|'); const d=+v[0], rel=v[1];
    $('sub').textContent=`${rel}が亡くなった場合の目安`;
    $('rel2').textContent=rel; $('kazoe').textContent='連続日数が一般的'; $('seishitsu').textContent='会社/学校の慣例';
    show();anim($('big'),0,d,700);
    SHARE=`忌引き日数の目安、${rel}は「${d}日」でした🕊️（規定により異なります）`;
  }''')

# ============================================================
# 2. 四十九日・忌日 計算
# ============================================================
add(id='shijukunichi', emoji='🪷',
  title='四十九日 計算｜命日から初七日・四十九日・百箇日はいつ？｜シミュラボ',
  desc='亡くなった日（命日）を入れるだけで、初七日・四十九日（忌明け）・百箇日の日付を自動計算する無料ツール。法要の準備・日程調整に。命日を1日目に数えます。',
  ogtitle='四十九日 計算｜命日から法要日はいつ？', ogdesc='命日から初七日・四十九日・百箇日の日付を計算。',
  h1='四十九日・忌日 計算',
  lead='命日を入れるだけで、初七日・四十九日（忌明け）・百箇日の日付を自動計算。法要の準備や日程調整にお使いください。',
  inputs='''    <h2>🪷 命日を入れる</h2>
    <div class="field"><label>亡くなった日（命日）</label><input type="date" id="d" value="2026-01-15"></div>
    <button class="btn btn-primary" id="calcBtn">忌日を計算する</button>''',
  result='''      <div class="label">四十九日（忌明け）</div>
      <div class="big" style="font-size:26px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">初七日</div><div class="v accent" id="sho">—</div></div>
      <div class="stat"><div class="k">百箇日</div><div class="v" id="hyaku">—</div></div>
      <div class="stat"><div class="k">命日から</div><div class="v" id="days">—</div></div></div>''',
  article=C('仏式では<b>命日（亡くなった日）を1日目</b>と数えます。そのため初七日は命日を含めて7日目、四十九日（七七日・忌明け）は49日目になります。地域や宗派で数え方が変わることもあります（関西などで前日起点とする例も）。')+'''
    <h2>忌日（きにち）の数え方</h2>
    <table class="seo-table"><tr><th>法要</th><th>命日から</th></tr>
    <tr><td>初七日（しょなのか）</td><td>7日目（＋6日）</td></tr>
    <tr><td>二七日〜六七日</td><td>14・21・28・35・42日目</td></tr>
    <tr><td>四十九日（七七日・忌明け）</td><td>49日目（＋48日）</td></tr>
    <tr><td>百箇日（ひゃっかにち）</td><td>100日目（＋99日）</td></tr></table>
    <p>四十九日を過ぎると忌明けとなり、初盆（新盆）を迎える準備に入ります。初盆の時期は <a href="/sims/niibon/">初盆・新盆はいつ</a>、一周忌以降は <a href="/sims/kaiki/">回忌・年忌 早見</a> で確認できます。</p>
    <h2>よくある質問</h2>'''+faq([
    ('四十九日は命日から何日後？','命日を1日目と数えるため、命日の48日後（49日目）です。本ツールが自動計算します。'),
    ('実際の法要は当日にやる？','近年は参列しやすい直前の土日に繰り上げて行うことが多いです。菩提寺とご相談ください。'),
    ('地域で数え方が違う？','命日の前日を1日目とする地域もあります。詳しくは菩提寺・地域の慣習に従ってください。'),
    ('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')])+REF(['四十九日・忌日の一般的な数え方（仏式）']),
  js='''  function calc(){
    const s=$('d').value; if(!s){alert('命日を入れてね');return;}
    const base=new Date(s+'T00:00:00');
    const W=['日','月','火','水','木','金','土'];
    function fmt(dt){return `${dt.getFullYear()}年${dt.getMonth()+1}月${dt.getDate()}日(${W[dt.getDay()]})`;}
    function add(n){const dt=new Date(base);dt.setDate(dt.getDate()+n);return dt;}
    const sho=add(6), yon=add(48), hyaku=add(99);
    $('big').textContent=fmt(yon);
    $('sub').textContent='※命日を1日目に数えた場合';
    $('sho').textContent=fmt(sho); $('hyaku').textContent=fmt(hyaku); $('days').textContent='49日目';
    show();
    SHARE=`四十九日 計算、忌明けは ${fmt(yon)} でした🪷`;
  }''')

# ============================================================
# 3. 回忌・年忌 早見
# ============================================================
add(id='kaiki', emoji='🕯️',
  title='回忌 早見｜没年から一周忌・三回忌・七回忌は西暦何年？｜シミュラボ',
  desc='亡くなった年を入れるだけで、一周忌・三回忌・七回忌・十三回忌・三十三回忌など各年忌法要が西暦何年になるかを計算する無料ツール。三回忌は没後満2年です。',
  ogtitle='回忌 早見｜三回忌・七回忌は何年？', ogdesc='没年から各回忌法要の西暦を計算（三回忌＝没後満2年）。',
  h1='回忌・年忌 早見',
  lead='亡くなった年を入れると、一周忌・三回忌・七回忌…と各年忌法要が西暦何年になるかを一覧表示。「三回忌なのに満2年？」の混乱もすっきり解決します。',
  inputs='''    <h2>🕯️ 亡くなった年を入れる</h2>
    <div class="field"><label>没年（西暦）</label><input type="number" id="y" value="2025" min="1900" max="2100" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">回忌を計算する</button>''',
  result='''      <div class="label">三回忌（没後満2年）</div>
      <div class="big"><span id="big">—</span><span class="unit">年</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">一周忌</div><div class="v accent" id="ichi">—</div></div>
      <div class="stat"><div class="k">七回忌</div><div class="v" id="nana">—</div></div>
      <div class="stat"><div class="k">三十三回忌</div><div class="v" id="san">—</div></div></div>''',
  article=C('回忌（年忌）は<b>亡くなった年を1回目と数えます</b>。だから一周忌だけは「没後満1年」ですが、三回忌は「没後満2年」、七回忌は「没後満6年」…と、回忌の数字マイナス1年になります。ここが混乱しやすいポイントです。')+'''
    <h2>年忌法要 早見表</h2>
    <table class="seo-table"><tr><th>法要</th><th>没後</th></tr>
    <tr><td>一周忌</td><td>満1年</td></tr>
    <tr><td>三回忌</td><td>満2年</td></tr>
    <tr><td>七回忌</td><td>満6年</td></tr>
    <tr><td>十三回忌</td><td>満12年</td></tr>
    <tr><td>十七回忌</td><td>満16年</td></tr>
    <tr><td>二十三回忌</td><td>満22年</td></tr>
    <tr><td>三十三回忌（弔い上げ）</td><td>満32年</td></tr></table>
    <p>三十三回忌をもって「弔い上げ（とむらいあげ）」とし、年忌法要を締めくくる家が多いです。四十九日までの忌日は <a href="/sims/shijukunichi/">四十九日・忌日 計算</a>、初盆は <a href="/sims/niibon/">初盆・新盆はいつ</a> をどうぞ。</p>
    <h2>よくある質問</h2>'''+faq([
    ('三回忌はいつ？','亡くなった年を1回目と数えるため、没後満2年（没年＋2年）に行います。'),
    ('なぜ回忌と満年数がずれる？','没年を1回目と数える「数え」の考え方だからです。回忌の数字から1を引くと満年数になります。'),
    ('弔い上げは何回忌？','三十三回忌（または五十回忌）で年忌法要を締めくくるのが一般的です。'),
    ('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')])+REF(['年忌法要（回忌）の一般的な数え方']),
  js='''  function calc(){
    const y=Math.floor(+$('y').value||2025);
    $('big').textContent=(y+2);
    $('sub').textContent=`没年 ${y}年 を1回目として計算`;
    $('ichi').textContent=(y+1)+'年'; $('nana').textContent=(y+6)+'年'; $('san').textContent=(y+32)+'年';
    show();
    SHARE=`回忌 早見、${y}年に亡くなった方の三回忌は ${y+2}年 でした🕯️`;
  }''')

# ============================================================
# 4. 初盆・新盆はいつ
# ============================================================
add(id='niibon', emoji='🏮',
  title='初盆・新盆はいつ？｜命日から初盆の年を計算（四十九日基準）｜シミュラボ',
  desc='亡くなった日から、四十九日の忌明け後に初めて迎えるお盆＝初盆（新盆）が何年の8月（または7月）になるかを計算する無料ツール。忌明け前なら翌年になります。',
  ogtitle='初盆・新盆はいつ？｜初盆の年を計算', ogdesc='命日と四十九日から初盆（新盆）の年を計算。',
  h1='初盆・新盆はいつ？',
  lead='「今年が初盆？それとも来年？」を命日から判定。四十九日の忌明けを過ぎてから初めて迎えるお盆が初盆（新盆）です。忌明け前にお盆が来る場合は翌年になります。',
  inputs='''    <h2>🏮 命日とお盆の時期</h2>
    <div class="field"><label>亡くなった日（命日）</label><input type="date" id="d" value="2026-05-01"></div>
    <div class="field"><label>お盆の時期（地域）</label><select id="bon"><option value="8" selected>8月盆（8/13〜16・多くの地域）</option><option value="7">7月盆（7/13〜16・東京都心部など）</option></select></div>
    <button class="btn btn-primary" id="calcBtn">初盆の年を見る</button>''',
  result='''      <div class="label">初盆（新盆）を迎える年</div>
      <div class="big" style="font-size:28px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">四十九日（忌明け）</div><div class="v accent" id="yon">—</div></div>
      <div class="stat"><div class="k">お盆の時期</div><div class="v" id="bonv">—</div></div>
      <div class="stat"><div class="k">判定</div><div class="v" id="hantei">—</div></div></div>''',
  article=C('初盆（はつぼん）・新盆（にいぼん／あらぼん）は、<b>四十九日の忌明けを過ぎてから初めて迎えるお盆</b>のこと。命日からお盆までが四十九日に満たない場合、その年ではなく翌年が初盆になります。')+'''
    <h2>初盆の判定の考え方</h2>
    <ul>
    <li>四十九日（忌明け）を計算する（命日を1日目に数えて49日目）</li>
    <li>その年のお盆（多くは8/13〜16、東京都心部などは7/13〜16）より前に忌明けしていれば <b>その年が初盆</b></li>
    <li>お盆までに忌明けしなければ <b>翌年が初盆</b></li>
    </ul>
    <p>四十九日の日付は <a href="/sims/shijukunichi/">四十九日・忌日 計算</a>、一周忌以降は <a href="/sims/kaiki/">回忌・年忌 早見</a> で確認できます。地域・宗派により考え方が異なる場合があります。</p>
    <h2>よくある質問</h2>'''+faq([
    ('初盆と新盆は違う？','読み方が違うだけで同じ意味です。地域により「はつぼん」「にいぼん」「あらぼん」と呼びます。'),
    ('四十九日前にお盆が来たら？','その年は初盆にせず、翌年のお盆が初盆になります。本ツールが自動で判定します。'),
    ('お盆は7月？8月？','多くの地域は8月（月遅れ盆）、東京都心部などは7月です。地域に合わせて選んでください。'),
    ('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')])+REF(['初盆・新盆の一般的な考え方（四十九日基準）']),
  js='''  function calc(){
    const s=$('d').value; if(!s){alert('命日を入れてね');return;}
    const bonM=+$('bon').value||8;
    const base=new Date(s+'T00:00:00');
    const W=['日','月','火','水','木','金','土'];
    const yon=new Date(base); yon.setDate(yon.getDate()+48);
    function fmt(dt){return `${dt.getFullYear()}年${dt.getMonth()+1}月${dt.getDate()}日(${W[dt.getDay()]})`;}
    // その年のお盆最終日(16日)
    let bonYear=yon.getFullYear();
    const bonEndThatYear=new Date(bonYear, bonM-1, 16);
    if(yon > bonEndThatYear){ bonYear += 1; }
    $('big').textContent=`${bonYear}年 ${bonM}月`;
    $('sub').textContent='※四十九日の忌明け後、最初のお盆';
    $('yon').textContent=fmt(yon); $('bonv').textContent=`${bonM}/13〜16`;
    $('hantei').textContent=(bonYear===yon.getFullYear()?'当年が初盆':'翌年が初盆');
    show();
    SHARE=`初盆・新盆、初盆を迎えるのは ${bonYear}年${bonM}月 でした🏮`;
  }''')

# ============================================================
# 5. 血液型 遺伝 確率
# ============================================================
add(id='ketsueki-iden', emoji='🩸',
  title='血液型 遺伝｜両親の血液型から子どもは何型？生まれる可能性を判定｜シミュラボ',
  desc='父と母の血液型（ABO）を選ぶと、生まれる可能性のある子どもの血液型と、生まれない血液型を判定する無料ツール。A×Bは全型の可能性など、遺伝の仕組みが分かります。',
  ogtitle='血液型 遺伝｜子どもは何型になる？', ogdesc='両親の血液型から、生まれる可能性のある子の血液型を判定。',
  h1='血液型 遺伝 判定',
  lead='父と母の血液型を選ぶだけで、生まれる可能性のある子どもの血液型が分かります。「うちの子は何型になりうる？」の疑問に、ABO遺伝の仕組みからお答えします。',
  inputs='''    <h2>🩸 両親の血液型</h2>
    <div class="row"><div class="field"><label>父の血液型</label><select id="f"><option value="A" selected>A型</option><option value="B">B型</option><option value="O">O型</option><option value="AB">AB型</option></select></div>
    <div class="field"><label>母の血液型</label><select id="m"><option value="A">A型</option><option value="B" selected>B型</option><option value="O">O型</option><option value="AB">AB型</option></select></div></div>
    <button class="btn btn-primary" id="calcBtn">子どもの血液型を見る</button>''',
  result='''      <div class="label">生まれる可能性のある血液型</div>
      <div class="big" style="font-size:30px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">両親</div><div class="v accent" id="oya">—</div></div>
      <div class="stat"><div class="k">生まれない型</div><div class="v" id="nashi">—</div></div>
      <div class="stat"><div class="k">パターン</div><div class="v" id="pat">—</div></div></div>''',
  article=C('ABO式血液型は、A・B・Oの3種類の遺伝子（O は潜性）の組み合わせで決まります。両親からそれぞれ1つずつ受け継ぐため、<b>親と違う血液型の子が生まれることもあります</b>。例えばA型×B型からは、A・B・O・ABの全4型が生まれる可能性があります。')+'''
    <h2>両親の血液型と子どもの血液型</h2>
    <table class="seo-table"><tr><th>両親</th><th>生まれうる子</th></tr>
    <tr><td>O × O</td><td>O</td></tr>
    <tr><td>A × O</td><td>A・O</td></tr>
    <tr><td>A × A</td><td>A・O</td></tr>
    <tr><td>A × B</td><td>A・B・O・AB（全型）</td></tr>
    <tr><td>AB × O</td><td>A・B</td></tr>
    <tr><td>AB × AB</td><td>A・B・AB</td></tr></table>
    <p>※実際に何型が生まれるかの確率は、両親の遺伝子型（AA型かAO型かなど）によって変わります。本ツールは「生まれる可能性のある型」を判定します。血のつながりの濃さは <a href="/sims/ketsuen/">血縁度計算</a> でどうぞ。</p>
    <h2>よくある質問</h2>'''+faq([
    ('親と違う血液型の子が生まれるのはなぜ？','親がO遺伝子を隠し持っている（AO型など）ためです。両親がA型でも、子がO型になることがあります。'),
    ('A型×B型からO型やAB型は生まれる？','はい。A型×B型は、両親の遺伝子型によりA・B・O・ABの全4型が生まれる可能性があります。'),
    ('確率まで分かる？','正確な確率は両親の遺伝子型が必要です。本ツールは可能性のある型を示します。'),
    ('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')])+REF(['ABO式血液型の遺伝（メンデル遺伝の一般的な解説）']),
  js='''  function calc(){
    const f=$('f').value, m=$('m').value;
    const G={A:['A','O'],B:['B','O'],O:['O','O'],AB:['A','B']};
    const set=new Set();
    for(const a of G[f]) for(const b of G[m]){
      const p=[a,b];
      if(p.includes('A')&&p.includes('B')) set.add('AB');
      else if(p.includes('A')) set.add('A');
      else if(p.includes('B')) set.add('B');
      else set.add('O');
    }
    const order=['A','B','O','AB'];
    const yes=order.filter(x=>set.has(x));
    const no=order.filter(x=>!set.has(x));
    $('big').textContent=yes.join('・')+'型';
    $('sub').textContent=`父 ${f}型 × 母 ${m}型 の場合`;
    $('oya').textContent=`${f}型 × ${m}型`;
    $('nashi').textContent=no.length?no.join('・')+'型':'なし';
    $('pat').textContent=yes.length+'種類';
    show();
    SHARE=`血液型 遺伝、${f}型×${m}型の子は「${yes.join('・')}型」の可能性でした🩸`;
  }''')

# ============================================================
# 6. ハーフ・クォーター 血の割合
# ============================================================
add(id='quarter-blood', emoji='🌍',
  title='ハーフ・クォーター 計算｜先祖のルーツで血の割合は何分の1？｜シミュラボ',
  desc='何世代前の祖先が海外ルーツかを選ぶと、自分に受け継がれた血の割合（ハーフ=1/2、クォーター=1/4など）を計算する無料ツール。ミックスの世代呼称も分かります。',
  ogtitle='ハーフ・クォーター 計算｜血の割合は？', ogdesc='祖先のルーツの世代から、受け継いだ血の割合を計算。',
  h1='ハーフ・クォーター 血の割合 計算',
  lead='「祖父母の1人が外国出身だと自分はクォーター？」を計算。ルーツを持つ祖先が何世代前かと人数から、受け継いだ血の割合を％と分数で表示します。',
  inputs='''    <h2>🌍 ルーツの祖先</h2>
    <div class="field"><label>海外ルーツの祖先の世代</label><select id="gen">
      <option value="1">親（1代前）＝ハーフ</option>
      <option value="2" selected>祖父母（2代前）＝クォーター</option>
      <option value="3">曾祖父母（3代前）</option>
      <option value="4">高祖父母（4代前）</option>
      <option value="5">5代前</option>
    </select></div>
    <div class="field"><label>そのルーツを持つ祖先の人数 <span class="hint">（人）</span></label><input type="number" id="k" value="1" min="1" max="16" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">血の割合を計算する</button>''',
  result='''      <div class="label">受け継いだ血の割合</div>
      <div class="big"><span id="big">0</span><span class="unit">%</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">分数でいうと</div><div class="v accent" id="bunsu">—</div></div>
      <div class="stat"><div class="k">呼び方の目安</div><div class="v" id="yobi">—</div></div>
      <div class="stat"><div class="k">祖先の世代</div><div class="v" id="genv">—</div></div></div>''',
  article=C('先祖から受け継ぐ血（遺伝）は、1世代さかのぼるごとに半分になります。親が外国出身ならその子は1/2（ハーフ）、祖父母の1人なら1/4（クォーター）、曾祖父母の1人なら1/8です。')+'''
    <h2>血の割合の早見表</h2>
    <table class="seo-table"><tr><th>ルーツの祖先</th><th>血の割合</th><th>呼び方</th></tr>
    <tr><td>親（1人）</td><td>50%（1/2）</td><td>ハーフ</td></tr>
    <tr><td>祖父母（1人）</td><td>25%（1/4）</td><td>クォーター</td></tr>
    <tr><td>曾祖父母（1人）</td><td>12.5%（1/8）</td><td>1/8（エイス）</td></tr>
    <tr><td>高祖父母（1人）</td><td>6.25%（1/16）</td><td>1/16</td></tr></table>
    <p>複数の祖先がそのルーツを持つ場合は、その分だけ割合が足し合わされます（例：祖父母2人なら1/4＋1/4＝1/2）。血のつながりの濃さは <a href="/sims/ketsuen/">血縁度計算</a>、ご先祖の人数は <a href="/sims/senzo-ninzu/">先祖の人数 計算</a> でどうぞ。</p>
    <h2>よくある質問</h2>'''+faq([
    ('クォーターって何分の1？','1/4（25%）です。祖父母4人のうち1人が外国ルーツの場合にあたります。'),
    ('祖父母2人が外国出身だと？','1/4が2人分で1/2（50%）になります。人数を2にして計算してください。'),
    ('血の割合は法律や国籍と関係ある？','いいえ。これは遺伝の受け継ぎの目安で、国籍とは別の話です。'),
    ('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')])+REF(['遺伝の受け継ぎ（世代ごとに1/2）の一般的な考え方']),
  js='''  function calc(){
    const gen=Math.max(1,Math.min(5,+$('gen').value||2));
    const k=Math.max(1,Math.min(Math.pow(2,gen),+$('k').value||1));
    let pct=k/Math.pow(2,gen)*100; if(pct>100)pct=100;
    const denom=Math.pow(2,gen);
    const label=pct>=100?'フル':pct===50?'ハーフ':pct===25?'クォーター':pct===12.5?'1/8':pct===6.25?'1/16':'約'+pct.toFixed(2)+'%';
    const gname={1:'親',2:'祖父母',3:'曾祖父母',4:'高祖父母',5:'5代前'}[gen];
    $('sub').textContent=`${gname}のうち${k}人が海外ルーツ`;
    $('bunsu').textContent=(k+'/'+denom);
    $('yobi').textContent=label;
    $('genv').textContent=gname;
    show();anim($('big'),0,pct,700, pct%1===0?0:2);
    SHARE=`ハーフ・クォーター計算、私の海外ルーツの血は「${pct%1===0?pct:pct.toFixed(2)}%（${k}/${denom}）」でした🌍`;
  }''')

# ============================================================
# 7. 親族の範囲 判定（6親等）
# ============================================================
add(id='shinzoku-hani', emoji='📜',
  title='親族の範囲 判定｜この人は法律上の親族？6親等内血族・3親等内姻族｜シミュラボ',
  desc='系統（血族・姻族）と親等を選ぶと、民法上の「親族」の範囲（6親等内の血族／配偶者／3親等内の姻族）に入るかどうかを判定する無料ツール。',
  ogtitle='親族の範囲 判定｜法律上の親族はどこまで？', ogdesc='血族・姻族と親等から、民法上の親族かどうかを判定。',
  h1='親族の範囲 判定',
  lead='「はとこは法律上の親族？」を判定。民法では親族の範囲を「6親等内の血族・配偶者・3親等内の姻族」と定めています。系統と親等を選ぶだけでチェックできます。',
  inputs='''    <h2>📜 相手との関係</h2>
    <div class="field"><label>系統</label><select id="kei"><option value="血族" selected>血族（血のつながり）</option><option value="姻族">姻族（配偶者側の親族）</option><option value="配偶者">配偶者本人</option></select></div>
    <div class="field"><label>親等 <span class="hint">（配偶者は選択不要）</span></label><select id="shinto"><option value="1">1親等</option><option value="2">2親等</option><option value="3">3親等</option><option value="4" selected>4親等（いとこ等）</option><option value="5">5親等</option><option value="6">6親等（はとこ等）</option><option value="7">7親等</option></select></div>
    <button class="btn btn-primary" id="calcBtn">親族か判定する</button>''',
  result='''      <div class="label">判定</div>
      <div class="big" style="font-size:28px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">系統</div><div class="v accent" id="keiv">—</div></div>
      <div class="stat"><div class="k">親等</div><div class="v" id="shintov">—</div></div>
      <div class="stat"><div class="k">親族の上限</div><div class="v" id="joge">—</div></div></div>''',
  article=C('民法では「親族」を、<b>①6親等内の血族 ②配偶者 ③3親等内の姻族</b>と定めています（民法725条）。血族はかなり遠い「はとこ（6親等）」まで親族ですが、姻族（配偶者側）は3親等以内までと範囲が狭くなります。')+'''
    <h2>親族の範囲（民法725条）</h2>
    <table class="seo-table"><tr><th>区分</th><th>親族の範囲</th></tr>
    <tr><td>血族</td><td>6親等以内（はとこ・6親等の甥姪まで）</td></tr>
    <tr><td>配偶者</td><td>親等なし・常に親族</td></tr>
    <tr><td>姻族</td><td>3親等以内（配偶者の甥姪・おじおばまで）</td></tr></table>
    <p>親等の数え方は <a href="/sims/shinto-keisan/">親等 計算</a>、難しい続柄の呼び方は <a href="/sims/oitoko/">続柄・呼び方 判定</a> をどうぞ。相続や扶養など、法律上の親族の範囲が関係する場面は少なくありません。</p>
    <h2>よくある質問</h2>'''+faq([
    ('親族はどこまで？','血族は6親等以内、姻族は3親等以内、そして配偶者です（民法725条）。'),
    ('はとこは親族？','はい。はとこは6親等の血族なので、法律上の親族に含まれます。'),
    ('配偶者の兄弟は親族？','配偶者の兄弟姉妹は2親等の姻族なので、3親等以内＝親族に含まれます。'),
    ('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')])+REF(['民法725条（親族の範囲）']),
  js='''  function calc(){
    const kei=$('kei').value; const shinto=+$('shinto').value||4;
    let ok, joge, sub;
    if(kei==='配偶者'){ ok=true; joge='配偶者は常に親族'; sub='配偶者は親等に関わらず親族です。'; }
    else if(kei==='血族'){ ok=shinto<=6; joge='6親等以内'; sub=ok?`${shinto}親等の血族は親族の範囲内です。`:`${shinto}親等の血族は親族の範囲外です。`; }
    else { ok=shinto<=3; joge='3親等以内'; sub=ok?`${shinto}親等の姻族は親族の範囲内です。`:`${shinto}親等の姻族は親族の範囲外です（姻族は3親等まで）。`; }
    $('big').textContent=ok?'✅ 親族です':'— 親族の範囲外';
    $('sub').textContent=sub;
    $('keiv').textContent=kei; $('shintov').textContent=(kei==='配偶者'?'—':shinto+'親等'); $('joge').textContent=joge;
    show();
    SHARE=`親族の範囲 判定、${kei}${kei==='配偶者'?'':'（'+shinto+'親等）'}は「${ok?'親族':'親族の範囲外'}」でした📜`;
  }''')

# ============================================================
# 8. 直系の呼び方 早見（玄孫・高祖父母）
# ============================================================
add(id='sonzoku-yobi', emoji='👴',
  title='玄孫・高祖父母の呼び方｜直系の先祖・子孫の呼称と読み方 早見｜シミュラボ',
  desc='「孫の孫は玄孫（やしゃご）」「祖父母の親は曾祖父母」など、直系の先祖・子孫の正しい呼び方と読み方を世代から表示する無料ツール。何代さかのぼる・くだるかで判定。',
  ogtitle='玄孫・高祖父母の呼び方｜直系の呼称早見', ogdesc='直系の先祖・子孫の呼び方と読み方を世代から表示。',
  h1='直系の呼び方 早見',
  lead='「孫の孫って何て呼ぶ？」を解決。先祖方向・子孫方向と世代数を選ぶと、直系の正しい呼び方と読み方（玄孫＝やしゃご、高祖父母＝こうそふぼ 等）を表示します。',
  inputs='''    <h2>👴 方向と世代</h2>
    <div class="field"><label>どちら方向？</label><select id="dir"><option value="down" selected>子孫の方向（子・孫・ひ孫…）</option><option value="up">先祖の方向（父母・祖父母…）</option></select></div>
    <div class="field"><label>何世代分？ <span class="hint">（1〜7）</span></label><input type="number" id="n" value="4" min="1" max="7" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">呼び方を調べる</button>''',
  result='''      <div class="label">呼び方</div>
      <div class="big" style="font-size:30px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">読み方</div><div class="v accent" id="yomi">—</div></div>
      <div class="stat"><div class="k">親等</div><div class="v" id="shinto">—</div></div>
      <div class="stat"><div class="k">世代</div><div class="v" id="gen">—</div></div></div>''',
  article=C('直系（親子の縦のつながり）の呼び方は、さかのぼると父母→祖父母→曾祖父母→高祖父母、くだると子→孫→ひ孫→玄孫（やしゃご）→来孫（らいそん）と続きます。世代が離れるほど耳慣れない呼び名になります。')+'''
    <h2>直系の呼び方 早見表</h2>
    <table class="seo-table"><tr><th>世代</th><th>先祖方向</th><th>子孫方向</th></tr>
    <tr><td>1</td><td>父母</td><td>子</td></tr>
    <tr><td>2</td><td>祖父母</td><td>孫</td></tr>
    <tr><td>3</td><td>曾祖父母（そうそふぼ）</td><td>曾孫・ひ孫（そうそん）</td></tr>
    <tr><td>4</td><td>高祖父母（こうそふぼ）</td><td>玄孫（やしゃご・げんそん）</td></tr>
    <tr><td>5</td><td>五世の祖（ごせいのそ）</td><td>来孫（らいそん）</td></tr>
    <tr><td>6</td><td>六世の祖</td><td>昆孫（こんそん）</td></tr>
    <tr><td>7</td><td>七世の祖</td><td>仍孫（じょうそん）</td></tr></table>
    <p>傍系（いとこ・はとこ等）の呼び方は <a href="/sims/oitoko/">続柄・呼び方 判定</a>、親等は <a href="/sims/shinto-keisan/">親等 計算</a> をどうぞ。</p>
    <h2>よくある質問</h2>'''+faq([
    ('孫の孫は何と呼ぶ？','玄孫（やしゃご／げんそん）です。あなたから4世代下の直系の子孫にあたります。'),
    ('祖父母の親は？','曾祖父母（そうそふぼ）です。さらにその親は高祖父母（こうそふぼ）と呼びます。'),
    ('直系は何親等？','直系は世代の数がそのまま親等になります（子・父母＝1親等、孫・祖父母＝2親等…）。'),
    ('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')])+REF(['直系尊属・卑属の一般的な呼称']),
  js='''  function calc(){
    const dir=$('dir').value; const n=Math.max(1,Math.min(7,Math.floor(+$('n').value||4)));
    const UP={1:['父母','ふぼ'],2:['祖父母','そふぼ'],3:['曾祖父母','そうそふぼ'],4:['高祖父母','こうそふぼ'],5:['五世の祖','ごせいのそ'],6:['六世の祖','ろくせいのそ'],7:['七世の祖','しちせいのそ']};
    const DN={1:['子','こ'],2:['孫','まご'],3:['曾孫（ひ孫）','そうそん・ひまご'],4:['玄孫','やしゃご・げんそん'],5:['来孫','らいそん'],6:['昆孫','こんそん'],7:['仍孫','じょうそん']};
    const t=(dir==='up'?UP:DN)[n];
    $('big').textContent=t[0];
    $('sub').textContent=(dir==='up'?`あなたから${n}世代さかのぼった直系のご先祖`:`あなたから${n}世代くだった直系の子孫`);
    $('yomi').textContent=t[1]; $('shinto').textContent=n+'親等'; $('gen').textContent=(dir==='up'?n+'代上':n+'代下');
    show();
    SHARE=`直系の呼び方、${dir==='up'?n+'代上':n+'代下'}は「${t[0]}（${t[1]}）」でした👴`;
  }''')

# ============================================================
# 9. 西暦→何代前（ルーツ逆算）
# ============================================================
add(id='sedai-sakanobori', emoji='📜',
  title='何代前？計算｜西暦◯年のご先祖はあなたの何代前・何時代？｜シミュラボ',
  desc='西暦（年）を入れると、その頃のご先祖があなたから何代前にあたるか、その代の直系ご先祖は何人か、どの時代かを計算する無料ツール。家系のルーツ探しに。',
  ogtitle='何代前？計算｜西暦から世代をさかのぼる', ogdesc='西暦から、その頃のご先祖が何代前・何時代かを計算。',
  h1='何代前？ 計算（ルーツ逆算）',
  lead='「江戸時代のご先祖は自分の何代前？」を西暦から逆算。その頃のご先祖が何代前にあたるか、その代の直系ご先祖の人数、時代区分までまとめて表示します。',
  inputs='''    <h2>📜 さかのぼる西暦</h2>
    <div class="row"><div class="field"><label>西暦（年）</label><input type="number" id="y" value="1700" min="0" max="2026" inputmode="numeric"></div>
    <div class="field"><label>1世代の年数 <span class="hint">（年）</span></label><input type="number" id="g" value="30" min="15" max="40" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">何代前か計算する</button>''',
  result='''      <div class="label">およそ何代前</div>
      <div class="big"><span id="big">0</span><span class="unit">代前</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">何年前</div><div class="v accent" id="years">—</div></div>
      <div class="stat"><div class="k">その代の直系ご先祖</div><div class="v" id="ninzu">—</div></div>
      <div class="stat"><div class="k">時代</div><div class="v" id="jidai">—</div></div></div>''',
  article=C('1世代を約30年とすると、世代数 ＝ さかのぼる年数 ÷ 30 で概算できます。例えば約300年前（江戸中期）なら10代前、その代の直系ご先祖は2の10乗で1,024人になります。')+'''
    <h2>年代と世代・時代の目安</h2>
    <table class="seo-table"><tr><th>西暦</th><th>約何代前</th><th>時代</th></tr>
    <tr><td>1870年ごろ</td><td>約5代前</td><td>幕末〜明治</td></tr>
    <tr><td>1720年ごろ</td><td>約10代前</td><td>江戸中期</td></tr>
    <tr><td>1570年ごろ</td><td>約15代前</td><td>戦国</td></tr>
    <tr><td>1420年ごろ</td><td>約20代前</td><td>室町</td></tr>
    <tr><td>1270年ごろ</td><td>約25代前</td><td>鎌倉</td></tr></table>
    <p>ご先祖の人数そのものは <a href="/sims/senzo-ninzu/">先祖の人数 計算</a>、血のつながりは <a href="/sims/ketsuen/">血縁度計算</a> でどうぞ。戸籍でたどれるのは一般に江戸末期〜明治初期（4〜5代前ごろ）までとされます。</p>
    <h2>よくある質問</h2>'''+faq([
    ('江戸時代のご先祖は何代前？','江戸中期（約300年前）なら約10代前が目安です。1世代の年数の取り方で前後します。'),
    ('戸籍は何代前までたどれる？','現存する戸籍では、一般に江戸末期〜明治初期生まれ（4〜5代前ごろ）までさかのぼれることが多いです。'),
    ('1世代は何年？','25〜30年が目安です。本ツールでは年数を変えて調整できます。'),
    ('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')])+REF(['系図・世代の一般的な数え方（1世代≈25〜30年）']),
  js='''  function calc(){
    const y=Math.min(2026,Math.floor(+$('y').value||1700));
    const g=Math.max(15,Math.min(40,+$('g').value||30));
    const years=Math.max(0,2026-y);
    const gen=Math.max(0,Math.round(years/g));
    const ninzu=Math.pow(2,gen);
    let jidai;
    if(y>=1989)jidai='平成・令和';else if(y>=1926)jidai='昭和';else if(y>=1912)jidai='大正';else if(y>=1868)jidai='明治';else if(y>=1603)jidai='江戸';else if(y>=1573)jidai='安土桃山';else if(y>=1467)jidai='戦国';else if(y>=1336)jidai='室町';else if(y>=1185)jidai='鎌倉';else if(y>=794)jidai='平安';else if(y>=710)jidai='奈良';else jidai='それ以前';
    $('sub').textContent=`西暦${y}年 ＝ 約${num(years)}年前（${jidai}時代）`;
    $('years').textContent='約'+num(years)+'年前';
    $('ninzu').textContent=num(ninzu)+'人';
    $('jidai').textContent=jidai;
    show();anim($('big'),0,gen,700);
    SHARE=`何代前？計算、西暦${y}年のご先祖は約${gen}代前（${jidai}時代・その代${num(ninzu)}人）でした📜`;
  }''')

# ============================================================
# 10. 親戚は何人？（家系の広がり概算）
# ============================================================
add(id='shinseki-count', emoji='👪',
  title='親戚は何人？計算｜祖父母を起点に、いとこ・親戚の人数を概算｜シミュラボ',
  desc='共通の祖先（祖父母・曾祖父母）と1家族あたりの子どもの数から、いとこ・はとこを含む親戚の人数を概算する無料ツール。家系の広がりを数字で体感できます。',
  ogtitle='親戚は何人？｜いとこ・親戚の人数を概算', ogdesc='祖先と子どもの数から、いとこ等の親戚人数を概算。',
  h1='親戚は何人？ 計算',
  lead='「いとこって全部で何人になる？」を概算。共通の祖先と1家族の子どもの数から、あなたの世代に広がる親戚（いとこ・はとこ）の人数を計算します。家系の広がりを体感。',
  inputs='''    <h2>👪 条件を入れる</h2>
    <div class="field"><label>共通の祖先</label><select id="base"><option value="2" selected>祖父母（いとこの広がり）</option><option value="3">曾祖父母（はとこの広がり）</option></select></div>
    <div class="field"><label>1家族あたりの子ども <span class="hint">（人）</span></label><input type="number" id="c" value="2" min="1" max="8" step="0.5" inputmode="decimal"></div>
    <button class="btn btn-primary" id="calcBtn">親戚の人数を見る</button>''',
  result='''      <div class="label">起点の子孫（親戚）の総数</div>
      <div class="big"><span id="big">0</span><span class="unit">人</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">あなたの世代（自分含む）</div><div class="v accent" id="same">—</div></div>
      <div class="stat"><div class="k">いとこ／はとこ</div><div class="v" id="itoko">—</div></div>
      <div class="stat"><div class="k">親世代</div><div class="v" id="oya">—</div></div></div>''',
  article=C('共通の祖先から「1家族あたりc人の子ども」が続くと仮定すると、祖父母を起点にした孫の世代（あなたといとこ）は c×c＝c²人。曾祖父母を起点にすればひ孫の世代（あなたとはとこ）は c³人に広がります。')+'''
    <h2>親戚の広がり（1家族2人の場合）</h2>
    <table class="seo-table"><tr><th>起点</th><th>あなたの世代</th><th>いとこ／はとこ</th></tr>
    <tr><td>祖父母</td><td>孫 4人</td><td>いとこ 2人</td></tr>
    <tr><td>曾祖父母</td><td>ひ孫 8人</td><td>はとこ 6人</td></tr></table>
    <div class="note"><strong>※理論上の概算です</strong><br>実際は各家庭の子どもの数がばらつくため、目安としてお楽しみください。</div>
    <p>血のつながりの濃さは <a href="/sims/ketsuen/">血縁度計算</a>、続柄の呼び方は <a href="/sims/oitoko/">続柄・呼び方 判定</a>、未来の子孫の数は <a href="/sims/shison-sim/">子孫シミュレーター</a> でどうぞ。</p>
    <h2>よくある質問</h2>'''+faq([
    ('いとこは何人が普通？','各家庭2人なら、いとこは平均2人程度が目安です。おじおばの数と子どもの数で変わります。'),
    ('はとこはどこまで数える？','曾祖父母を共通の祖先とする同世代がはとこです。本ツールで概算できます。'),
    ('正確な人数は分かる？','各家庭の子どもの数がばらつくため、あくまで理論上の概算です。'),
    ('データは送信されますか？','いいえ。すべてブラウザ内で完結します。')])+REF(['家系の広がり（指数的増加）の一般的な考え方']),
  js='''  function calc(){
    const base=+$('base').value||2; const c=Math.max(1,+$('c').value||2);
    let total=0; for(let k=1;k<=base;k++) total+=Math.pow(c,k);   // 起点の全子孫（子〜あなたの世代）
    const same=Math.pow(c,base);        // あなたの世代（孫 or ひ孫）
    const oya=Math.pow(c,base-1);       // 親世代（起点の子 or 孫）
    const itoko=Math.max(0,same-c);     // 同世代の親戚（自分の家庭c人＝自分と兄弟を除く）
    const baseName=base===2?'祖父母':'曾祖父母';
    const sameName=base===2?'孫':'ひ孫';
    const itokoName=base===2?'いとこ':'はとこ';
    $('sub').textContent=`${baseName}を起点・1家族${c}人の子`;
    $('same').textContent=`${sameName} ${num(same)}人`;
    $('itoko').textContent=`${itokoName} 約${num(itoko)}人`;
    $('oya').textContent=num(oya)+'人';
    show();anim($('big'),0,total,800);
    SHARE=`親戚は何人？${baseName}を起点に、${itokoName}を含む同世代は${num(same)}人でした👪`;
  }''')

if __name__=='__main__':
    write_all(SIMS)
    print(f'kakei2 done. {len(SIMS)} sims.')
