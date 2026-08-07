# -*- coding: utf-8 -*-
"""シミュラボ：SEO流入10本（低KD×実需KW・10カテゴリ分散）。write_all再利用。
KW根拠(Ahrefs jp): 有給付与25k/KD5・ジュニアシート20k/KD2・ボーナス平均14k/KD4・握力平均13k/KD1
・高齢者12k/KD2・アラサー12k/KD0・幼稚園10k/KD0・脈拍10k/KD2-4・独身税7.1k/KD1・バスト早見6.8k/KD2
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims11 import faq, write_all

SIMS = []
def add(**k): SIMS.append(k)
def C(t): return '<div class="note" style="border-left:4px solid var(--teal)"><strong>ポイント</strong>：'+t+'</div>'
def REF(items): return '<h2>参考</h2><ul class="seo-refs">'+''.join('<li>'+i+'</li>' for i in items)+'</ul>'

# ============================================================
# 1. 有給休暇 付与日数 計算（仕事・働き方）
# ============================================================
add(id='yukyu-fuyo', cat='仕事・働き方', emoji='🏖️',
  title='有給休暇 付与日数 計算|勤続年数で何日もらえる？パート比例付与も対応|シミュラボ',
  desc='勤続年数と週の労働日数を選ぶだけで、労働基準法どおりの有給休暇の付与日数を表示する無料ツール。フルタイムは半年で10日、パート・アルバイトの比例付与（週1〜4日勤務）にも対応。年5日の取得義務も解説。',
  ogtitle='有給休暇 付与日数 計算|何日もらえる？', ogdesc='勤続年数と週の労働日数から法定の有給付与日数を表示。パート比例付与対応。',
  h1='有給休暇 付与日数 計算',
  lead='「自分の有給って何日あるの？」を一発確認。勤続年数と週の労働日数を選ぶと、労働基準法で決まっている付与日数を表示します。パート・アルバイト（週1〜4日勤務）の比例付与にも対応。',
  inputs='''    <h2>🏖️ 働き方を選ぶ</h2>
    <div class="field"><label>勤続年数</label><select id="y">
      <option value="0">半年未満（付与前）</option>
      <option value="1" selected>半年〜1年半</option>
      <option value="2">1年半〜2年半</option>
      <option value="3">2年半〜3年半</option>
      <option value="4">3年半〜4年半</option>
      <option value="5">4年半〜5年半</option>
      <option value="6">5年半〜6年半</option>
      <option value="7">6年半以上</option>
    </select></div>
    <div class="field"><label>週の労働日数</label><select id="d">
      <option value="5" selected>週5日以上（または週30時間以上）</option>
      <option value="4">週4日</option>
      <option value="3">週3日</option>
      <option value="2">週2日</option>
      <option value="1">週1日</option>
    </select></div>
    <button class="btn btn-primary" id="calcBtn">付与日数を見る</button>''',
  result='''      <div class="label">法定の有給付与日数</div>
      <div class="big"><span id="big">0</span><span class="unit">日</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">区分</div><div class="v" id="kbn">—</div></div>
      <div class="stat"><div class="k">取得義務</div><div class="v accent" id="gimu">—</div></div>
      <div class="stat"><div class="k">次の付与</div><div class="v" id="next">—</div></div></div>''',
  article=C('有給休暇は<b>雇入れから6ヶ月</b>継続勤務し、全労働日の8割以上出勤すると付与されます。フルタイムなら初回10日。その後は1年ごとに増え、6年半で上限の<b>20日</b>に。パート・アルバイトでも週の労働日数に応じて必ず付与されます（比例付与）。')+'''
    <h2>有給休暇の付与日数 早見表（法定）</h2>
    <div class="tbl-scroll"><table class="seo-table"><tr><th>勤続年数</th><th>週5日〜</th><th>週4日</th><th>週3日</th><th>週2日</th><th>週1日</th></tr>
    <tr><td>半年</td><td>10日</td><td>7日</td><td>5日</td><td>3日</td><td>1日</td></tr>
    <tr><td>1年半</td><td>11日</td><td>8日</td><td>6日</td><td>4日</td><td>2日</td></tr>
    <tr><td>2年半</td><td>12日</td><td>9日</td><td>6日</td><td>4日</td><td>2日</td></tr>
    <tr><td>3年半</td><td>14日</td><td>10日</td><td>8日</td><td>5日</td><td>2日</td></tr>
    <tr><td>4年半</td><td>16日</td><td>12日</td><td>9日</td><td>6日</td><td>3日</td></tr>
    <tr><td>5年半</td><td>18日</td><td>13日</td><td>10日</td><td>6日</td><td>3日</td></tr>
    <tr><td>6年半〜</td><td>20日</td><td>15日</td><td>11日</td><td>7日</td><td>3日</td></tr></table></div>
    <p>年10日以上付与される人は、<b>年5日の取得が会社の義務</b>です（2019年〜）。取らせなかった会社には罰則もあります。未消化分は翌年まで繰り越せますが、時効は2年。余らせている有給をお金に換算すると意外な金額になります——<a href="/sims/yukyu/">有給消化シミュレーター</a>で確かめてみてください。</p>
    <h2>よくある質問</h2>'''+faq([
    ('パート・アルバイトにも有給はある？','あります。週1日勤務でも勤続半年で1日付与されます（比例付与）。「パートだから無い」は誤りです。'),
    ('繰り越しはできる？','できます。時効は2年なので、昨年の残りと今年の付与分を合わせて保有できます。'),
    ('週30時間以上働くパートは？','週の日数が4日以下でも、週30時間以上ならフルタイムと同じ日数（初回10日）が付与されます。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['労働基準法39条（年次有給休暇・比例付与）','働き方改革関連法（年5日の時季指定義務・2019年施行）']),
  js='''  function calc(){
    const T={5:[10,11,12,14,16,18,20],4:[7,8,9,10,12,13,15],3:[5,6,6,8,9,10,11],2:[3,4,4,5,6,6,7],1:[1,2,2,2,3,3,3]};
    const y=+$('y').value, d=+$('d').value;
    const days = y===0 ? 0 : T[d][Math.min(6,y-1)];
    const full = d===5;
    $('sub').textContent = y===0 ? '雇入れ半年後に最初の付与があります' : `${sel('y').text}・${sel('d').text}`;
    $('kbn').textContent = full ? '通常の労働者' : '比例付与';
    $('gimu').textContent = days>=10 ? '年5日 取得義務あり' : '義務対象外';
    $('next').textContent = y===0 ? '半年後に'+T[d][0]+'日' : (y>=7 ? '上限です' : '1年後に'+T[d][Math.min(6,y)]+'日');
    show(); anim($('big'),0,days,700);
    SHARE=`有給休暇 付与日数、私は年${days}日でした🏖️ あなたは何日？`;
  }''')

# ============================================================
# 2. ボーナス 平均 比較（お金・時間）
# ============================================================
add(id='bonus-heikin', cat='お金・時間', emoji='💰',
  title='ボーナス平均 いくら？年代別・企業規模別に自分と比較|シミュラボ',
  desc='あなたの年間ボーナスは平均より上？下？年代別・企業規模別の平均賞与額（目安）とくらべて、自分の位置を判定する無料ツール。ボーナスなしの会社の割合、平均何ヶ月分かも解説。',
  ogtitle='ボーナス平均 いくら？|年代・規模別に比較', ogdesc='年間ボーナスを年代別・企業規模別の平均と比較して自分の位置を判定。',
  h1='ボーナス平均 比較シミュレーター',
  lead='あなたの年間ボーナス、平均とくらべてどのくらい？ 年代と会社の規模を選ぶと、公的統計ベースの平均額（目安）とあなたの額を比較します。',
  inputs='''    <h2>💰 条件を入れる</h2>
    <div class="field"><label>あなたの年間ボーナス <span class="hint">（夏＋冬の合計・額面/万円）</span></label><input type="number" id="b" value="80" min="0" inputmode="numeric"></div>
    <div class="row"><div class="field"><label>年代</label><select id="age"><option value="45">20代前半</option><option value="70">20代後半</option><option value="90" selected>30代</option><option value="105">40代</option><option value="110">50代</option><option value="75">60代</option></select></div>
    <div class="field"><label>企業規模</label><select id="sz"><option value="0.65">〜29人</option><option value="0.85" selected>30〜99人</option><option value="1.05">100〜499人</option><option value="1.35">500人以上</option></select></div></div>
    <button class="btn btn-primary" id="calcBtn">平均と比較する</button>''',
  result='''      <div class="label">同条件の平均との差</div>
      <div class="big"><span id="big">0</span><span class="unit">万円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">同条件の平均（目安）</div><div class="v accent" id="avg">—</div></div>
      <div class="stat"><div class="k">あなた</div><div class="v" id="you">—</div></div>
      <div class="stat"><div class="k">判定</div><div class="v" id="hantei">—</div></div></div>''',
  article=C('民間企業の賞与は、夏・冬あわせて<b>年間でおよそ月給の2〜2.5ヶ月分</b>が平均的な水準です。ただし年代・企業規模・業種で大きく差があり、<b>賞与ゼロの事業所も約3割</b>あります。この比較はあくまで「支給がある人の平均目安」との比較です。')+'''
    <h2>年間ボーナスの平均目安（年代別）</h2>
    <div class="tbl-scroll"><table class="seo-table"><tr><th>年代</th><th>年間賞与の目安</th></tr>
    <tr><td>20代前半</td><td>約45万円</td></tr>
    <tr><td>20代後半</td><td>約70万円</td></tr>
    <tr><td>30代</td><td>約90万円</td></tr>
    <tr><td>40代</td><td>約105万円</td></tr>
    <tr><td>50代</td><td>約110万円（ピーク）</td></tr>
    <tr><td>60代</td><td>約75万円</td></tr></table></div>
    <p>※厚生労働省・国税庁の各種統計をもとにした概算の目安です。企業規模でも差が大きく、大企業（500人以上）は中小の1.5〜2倍になることも。額面から税金・社会保険料が引かれた手取りは<a href="/sims/shouyo-tedori/">ボーナス手取りシミュレーター</a>で、使い道の配分は<a href="/sims/bonus-tsukaimichi/">ボーナス使い道シミュレーター</a>でどうぞ。</p>
    <h2>よくある質問</h2>'''+faq([
    ('ボーナスがない会社は普通？','賞与制度がない・支給実績がない事業所は約3割あり、めずらしくありません。年俸制で月給に含む会社もあります。'),
    ('平均何ヶ月分？','支給がある企業では年間で月給の2〜2.5ヶ月分程度が平均的な水準です。公務員は年間約4.5ヶ月分です。'),
    ('この平均は正確？','公的統計をもとにした丸めた目安です。業種・地域・雇用形態で大きく変わるため、参考値としてご覧ください。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['厚生労働省 毎月勤労統計調査（賞与）','国税庁 民間給与実態統計調査']),
  js='''  function calc(){
    const b=Math.max(0,+$('b').value||0), base=+$('age').value, k=+$('sz').value;
    const avg=Math.round(base*k), diff=b-avg;
    let h; const r=avg>0?b/avg:0;
    if(r>=1.3)h='かなり上位'; else if(r>=1.05)h='平均より上'; else if(r>=0.95)h='ほぼ平均'; else if(r>=0.7)h='平均より下'; else h='平均を大きく下回る';
    $('sub').textContent = diff>=0 ? `同条件の平均より ${Math.abs(diff)}万円 多い` : `同条件の平均より ${Math.abs(diff)}万円 少ない`;
    $('avg').textContent=avg+'万円'; $('you').textContent=b+'万円'; $('hantei').textContent=h;
    show(); anim($('big'),0,Math.abs(diff),800);
    SHARE=`ボーナス平均比較、私は同条件の平均より${Math.abs(diff)}万円${diff>=0?'多い':'少ない'}（${h}）でした💰`;
  }''')

# ============================================================
# 3. 幼稚園・保育園 入園年齢 計算（子ども・育児）
# ============================================================
add(id='nyuen-nenrei', cat='子ども・育児', emoji='🎒',
  title='幼稚園は何歳から？入園年齢・年少年中年長 計算（早生まれ対応）|シミュラボ',
  desc='子どもの生年月日を入れるだけで、幼稚園に入れる年齢・年少/年中/年長になる年度・小学校入学の年をすべて表示する無料ツール。保育園は0歳から、幼稚園は満3歳から。早生まれの学年の決まり方も解説。',
  ogtitle='幼稚園は何歳から？入園年齢 計算', ogdesc='生年月日から年少・年中・年長の年度と小学校入学年をすべて表示。早生まれ対応。',
  h1='幼稚園・保育園 入園年齢 計算',
  lead='「うちの子、幼稚園はいつから？」を生年月日ひとつで解決。年少・年中・年長になる年度、満3歳入園ができる日、小学校入学の年まで、まとめて表示します。早生まれの学年計算にも対応。',
  inputs='''    <h2>🎒 お子さんの生年月日</h2>
    <div class="field"><label>生年月日</label><input type="date" id="bd" value="2024-06-15"></div>
    <button class="btn btn-primary" id="calcBtn">入園の年を計算する</button>''',
  result='''      <div class="label">年少（3年保育）で入園する年</div>
      <div class="big" style="font-size:34px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">満3歳入園できる日</div><div class="v" id="man3">—</div></div>
      <div class="stat"><div class="k">年中／年長</div><div class="v" id="nencho">—</div></div>
      <div class="stat"><div class="k">小学校入学</div><div class="v accent" id="shou">—</div></div></div>''',
  article=C('幼稚園は<b>満3歳から</b>入れます（学校教育法）。一般的な「年少（3年保育）」は、<b>4月1日時点で満3歳</b>になっている年度の4月から。保育園は0歳（産休明け〜）から入れます。学年の区切りは「4月2日生まれ〜翌年4月1日生まれ」がワンセットです。')+'''
    <h2>入園・入学の年齢早見</h2>
    <div class="tbl-scroll"><table class="seo-table"><tr><th>クラス</th><th>4月1日時点の年齢</th><th>施設</th></tr>
    <tr><td>0〜2歳児クラス</td><td>0〜2歳</td><td>保育園・こども園</td></tr>
    <tr><td>満3歳児クラス（プレ）</td><td>年度途中に満3歳</td><td>幼稚園（園による）</td></tr>
    <tr><td>年少</td><td>3歳</td><td>幼稚園・保育園・こども園</td></tr>
    <tr><td>年中</td><td>4歳</td><td>〃</td></tr>
    <tr><td>年長</td><td>5歳</td><td>〃</td></tr>
    <tr><td>小学1年生</td><td>6歳</td><td>小学校</td></tr></table></div>
    <h2>早生まれの学年はこう決まる</h2>
    <p>学年の区切りが「4月2日〜翌4月1日」なのは、法律上<b>誕生日の前日に歳をとる</b>ため。4月1日生まれの子は3月31日に満年齢が上がるので、ひとつ上の学年になります。1〜4月1日生まれ（早生まれ）は同学年の中で最大約1歳若く、入園時期も1年早く感じられます。</p>
    <p>幼稚園と保育園の費用のちがいは<a href="/sims/hoiku-youchi/">保育園 vs 幼稚園 コストシミュレーター</a>、教育費の総額は<a href="/sims/gakuhi/">学費総額シミュレーター</a>でどうぞ。</p>
    <h2>よくある質問</h2>'''+faq([
    ('幼稚園は何歳から入れる？','法律上は満3歳から。多くの園の「年少」は4月1日時点で3歳になっている子です。満3歳になった日から入れる「満3歳児入園」を受け付ける園もあります。'),
    ('保育園は何歳から？','0歳（多くは生後57日〜）から入れます。入園は年度途中でも可能ですが、自治体の利用調整（点数）があります。'),
    ('プレ幼稚園とは？','入園前の2歳児などを対象にした週1〜数回の教室です。本入園の優先枠になる園もあります。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['学校教育法26条（幼稚園の入園資格＝満3歳）','年齢計算ニ関スル法律（誕生日前日に加齢）']),
  js='''  function calc(){
    const v=$('bd').value; if(!v){alert('生年月日を入れてね');return;}
    const bd=new Date(v+'T00:00:00');
    // 学年基準：4/1時点で満3歳 → 誕生日が (年度年-3)/4/2 〜 (年度年-2)/4/1 の子が年少
    const by=bd.getFullYear(), bm=bd.getMonth()+1, bdd=bd.getDate();
    const early = (bm<4)||(bm===4&&bdd===1);      // 早生まれ（1/1〜4/1）
    // 年少＝4/1時点で満3歳。通常生まれ(4/2〜12/31)は誕生年+4年目の4月、早生まれは+3年目の4月
    const nenshoYear = by + (early?3:4);
    const man3=new Date(bd); man3.setFullYear(by+3); man3.setDate(man3.getDate()-1); // 満3歳になる日（誕生日前日加齢）
    $('big').textContent = nenshoYear + '年4月';
    $('sub').textContent = early ? '早生まれ（1/1〜4/1）なので、ひとつ上の学年グループです' : `${by}年${bm}月${bdd}日生まれ → 4月2日〜翌4月1日区切りで計算`;
    $('man3').textContent = `${man3.getFullYear()}年${man3.getMonth()+1}月${man3.getDate()}日〜`;
    $('nencho').textContent = `${nenshoYear+1}年／${nenshoYear+2}年`;
    $('shou').textContent = (nenshoYear+3) + '年4月';
    show();
    SHARE=`入園年齢 計算、うちの子の年少入園は${nenshoYear}年4月・小学校入学は${nenshoYear+3}年4月でした🎒`;
  }''')

# ============================================================
# 4. 高齢者は何歳から？判定（シニア・終活・介護）
# ============================================================
add(id='koreisha-itsu', cat='シニア・終活・介護', emoji='🎌',
  title='高齢者は何歳から？前期・後期高齢者や制度別の年齢を判定|シミュラボ',
  desc='「高齢者」の定義は制度によってバラバラ。年齢を入れると、前期/後期高齢者・介護保険・高齢者マーク・高齢受給者証・シニア割など、あなたが該当する制度をまとめて判定する無料ツール。WHOの定義も解説。',
  ogtitle='高齢者は何歳から？制度別に判定', ogdesc='年齢から前期/後期高齢者・介護保険・高齢者マークなど該当制度をまとめて判定。',
  h1='高齢者は何歳から？ 判定ツール',
  lead='「高齢者って結局何歳から？」——答えは<b>制度によって違います</b>。年齢を入れると、医療・介護・運転・年金などの各制度であなた（やご家族）がどう扱われるかをまとめて表示します。',
  inputs='''    <h2>🎌 年齢を入れる</h2>
    <div class="field"><label>年齢 <span class="hint">（歳）</span></label><input type="number" id="a" value="68" min="40" max="110" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">該当する制度を見る</button>''',
  result='''      <div class="label">一般的な区分</div>
      <div class="big" style="font-size:32px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">医療制度</div><div class="v" id="iryo">—</div></div>
      <div class="stat"><div class="k">介護保険</div><div class="v" id="kaigo">—</div></div>
      <div class="stat"><div class="k">運転関連</div><div class="v accent" id="unten">—</div></div></div>''',
  article=C('WHO（世界保健機関）や日本の統計では<b>65歳以上を高齢者</b>とし、65〜74歳を<b>前期高齢者</b>、75歳以上を<b>後期高齢者</b>と区分します。ただし介護保険は40歳から保険料負担、高齢者マークは70歳から、シニア割は50代から——と制度ごとに「高齢者」の線引きはバラバラです。')+'''
    <h2>制度別「何歳から」早見表</h2>
    <div class="tbl-scroll"><table class="seo-table"><tr><th>年齢</th><th>該当する制度・区分</th></tr>
    <tr><td>40歳</td><td>介護保険の保険料負担開始（第2号被保険者）</td></tr>
    <tr><td>50歳〜</td><td>各種シニア割引の対象になり始める（映画・携帯など）</td></tr>
    <tr><td>60歳</td><td>定年（企業による）・還暦</td></tr>
    <tr><td>65歳</td><td><b>前期高齢者</b>・介護保険第1号被保険者・年金の標準受給開始</td></tr>
    <tr><td>70歳</td><td>高齢者マーク（努力義務）・医療費2割負担（所得による）</td></tr>
    <tr><td>75歳</td><td><b>後期高齢者医療制度</b>・免許更新時に認知機能検査</td></tr></table></div>
    <p>「高齢者＝65歳」という区分は1950年代の国連文書に由来し、平均寿命が延びた現代では「75歳以上を高齢者とすべき」という学会提言（日本老年学会・2017年）もあります。敬老の日のお祝いを何歳から始めるかに決まりはなく、孫の誕生や退職を機にする家庭が多いようです。</p>
    <p>定年後の生活資金は<a href="/sims/rougo/">老後資金シミュレーター</a>、介護の備えは<a href="/sims/kaigo-hiyou/">介護費用シミュレーター</a>もどうぞ。</p>
    <h2>よくある質問</h2>'''+faq([
    ('高齢者は何歳からと決まっている？','ひとつの法律で統一されてはいません。統計・WHOでは65歳以上、医療制度では65歳（前期）と75歳（後期）、道路交通法の高齢者マークは70歳からです。'),
    ('高齢者マークは義務？','70歳以上は努力義務です。罰則はありませんが、表示すると幅寄せ等から保護されます。'),
    ('敬老の日は何歳から祝う？','決まりはありません。65歳や70歳、孫の誕生を機になど家庭それぞれです。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['WHO・国連の高齢者定義（65歳以上）','高齢者の医療の確保に関する法律（前期65歳／後期75歳）','道路交通法71条の5（高齢運転者標識・70歳）']),
  js='''  function calc(){
    const a=Math.max(40,Math.min(110,+$('a').value||65));
    let kbn, sub;
    if(a<50){kbn='現役世代';sub='介護保険料の負担は始まっています（40歳〜）。';}
    else if(a<60){kbn='プレシニア';sub='シニア割の対象になり始める年代です。';}
    else if(a<65){kbn='准高齢期';sub='統計上の高齢者（65歳〜）まであと'+(65-a)+'年です。';}
    else if(a<75){kbn='前期高齢者';sub='WHO・日本の統計で「高齢者」に区分される年齢です。';}
    else if(a<90){kbn='後期高齢者';sub='後期高齢者医療制度の対象です。';}
    else{kbn='超高齢期（卒寿〜）';sub='人生100年時代の大先輩です。';}
    $('big').textContent=kbn; $('sub').textContent=sub;
    $('iryo').textContent = a>=75?'後期高齢者医療':a>=70?'2割負担(所得による)':a>=65?'前期高齢者':'通常';
    $('kaigo').textContent = a>=65?'第1号被保険者':'第2号(40〜64歳)';
    $('unten').textContent = a>=75?'認知機能検査あり':a>=70?'高齢者マーク(努力義務)':'通常';
    show();
    SHARE=`高齢者は何歳から？判定——${a}歳は「${kbn}」でした🎌 制度で線引きが違うの知ってた？`;
  }''')

# ============================================================
# 5. ジュニアシート 何歳から何歳まで（クルマ・乗り物）
# ============================================================
add(id='junior-seat', cat='クルマ・乗り物', emoji='🚗',
  title='ジュニアシートは何歳から何歳まで？年齢と身長で判定（法律は6歳・安全は140cm）|シミュラボ',
  desc='チャイルドシートの法律義務は6歳未満。でも安全にシートベルトを使えるのは身長140cmから。子どもの年齢と身長を入れると、チャイルドシート/ジュニアシート/シートベルトのどれが正解かを判定する無料ツール。',
  ogtitle='ジュニアシートは何歳から何歳まで？', ogdesc='年齢と身長からチャイルドシート/ジュニアシート/ベルトOKを判定。法律6歳・安全140cm。',
  h1='ジュニアシート 何歳から何歳まで？ 判定',
  lead='法律の義務は「6歳未満」。でも本当に大事なのは<b>身長140cm</b>です。お子さんの年齢と身長を入れると、チャイルドシート・ジュニアシート・シートベルトのどれを使うべきかを判定します。',
  inputs='''    <h2>🚗 お子さんの情報</h2>
    <div class="row"><div class="field"><label>年齢 <span class="hint">（歳）</span></label><input type="number" id="a" value="5" min="0" max="12" inputmode="numeric"></div>
    <div class="field"><label>身長 <span class="hint">（cm）</span></label><input type="number" id="h" value="108" min="40" max="170" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">どれを使うべきか判定</button>''',
  result='''      <div class="label">判定</div>
      <div class="big" style="font-size:30px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">法律（道交法）</div><div class="v accent" id="hou">—</div></div>
      <div class="stat"><div class="k">シートベルトまで</div><div class="v" id="belt">—</div></div>
      <div class="stat"><div class="k">推奨</div><div class="v" id="osusume">—</div></div></div>''',
  article=C('道路交通法では<b>6歳未満</b>の子どもにチャイルドシート（幼児用補助装置）の使用が義務づけられています（違反は運転者に1点）。ただし6歳になっても、車のシートベルトは<b>身長約140cm以上</b>を想定して設計されているため、それまではジュニアシートの使用が強く推奨されます。')+'''
    <h2>年齢・体格別の目安</h2>
    <div class="tbl-scroll"><table class="seo-table"><tr><th>時期の目安</th><th>使うもの</th><th>向き・タイプ</th></tr>
    <tr><td>新生児〜1歳ごろ（〜13kg）</td><td>ベビーシート</td><td>後ろ向き</td></tr>
    <tr><td>1〜4歳ごろ（9〜18kg）</td><td>チャイルドシート</td><td>前向き（ハーネス式）</td></tr>
    <tr><td>3〜10歳ごろ（15〜36kg）</td><td>ジュニアシート</td><td>ブースター＋車のベルト</td></tr>
    <tr><td>身長140cm〜</td><td>シートベルトのみ</td><td>大人と同じ</td></tr></table></div>
    <p>140cm未満でシートベルトを使うと、肩ベルトが首に、腰ベルトがお腹にかかり、事故のとき重大なけがの原因になります。JAFや各メーカーも「6歳を過ぎても身長140cmまではジュニアシートを」と呼びかけています。なお、タクシーやバスに乗るときは義務が免除されます。</p>
    <p>チャイルドシートの後部座席への取り付けが最も安全です。車の維持費は<a href="/sims/kuruma-yosan/">車の維持費シミュレーター</a>もどうぞ。</p>
    <h2>よくある質問</h2>'''+faq([
    ('ジュニアシートは何歳から？','製品によりますが、目安は3歳ごろ・体重15kg以上から。それまではハーネス付きチャイルドシートが安全です。'),
    ('6歳になったらすぐ外していい？','法律の義務は外れますが、身長140cm未満のうちはジュニアシートの継続使用が強く推奨されます。小学校中〜高学年まで使う子も多いです。'),
    ('違反するとどうなる？','幼児用補助装置使用義務違反として運転者に違反点数1点が付きます（反則金はなし）。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['道路交通法71条の3第3項（6歳未満の幼児用補助装置使用義務）','JAF「チャイルドシートは身長140cmまで」の啓発資料']),
  js='''  function calc(){
    const a=Math.max(0,+$('a').value||0), h=Math.max(40,+$('h').value||100);
    let res, osu;
    if(a<1||h<75){res='ベビーシート（後ろ向き）'; osu='後ろ向きでの使用が最も安全';}
    else if(a<4&&h<100){res='チャイルドシート'; osu='ハーネス式で体を固定';}
    else if(h<140){res='ジュニアシート'; osu=a>=6?'義務は外れても140cmまで推奨':'法律上も使用義務あり';}
    else{res='シートベルトでOK'; osu='大人と同じ3点式ベルトで';}
    $('big').textContent=res;
    $('sub').textContent=`${a}歳・${h}cm の判定`;
    $('hou').textContent = a<6?'使用義務あり':'義務なし';
    $('belt').textContent = h>=140?'クリア':'あと'+(140-h)+'cm';
    $('osusume').textContent=osu;
    show();
    SHARE=`ジュニアシート判定、うちの子（${a}歳・${h}cm）は「${res}」でした🚗 法律は6歳・安全は140cm！`;
  }''')

# ============================================================
# 6. 独身税はいくら？（税金・確定申告）
# ============================================================
add(id='dokushin-zei', cat='税金・確定申告', emoji='🧾',
  title='独身税はいくら？子ども・子育て支援金を年収から計算（2026年4月開始）|シミュラボ',
  desc='「独身税」と話題の子ども・子育て支援金は2026年4月から医療保険とあわせて徴収。あなたの年収だと月いくら？を目安計算する無料ツール。独身者だけが払うわけではない事実、2026→2028年の段階スケジュールも解説。',
  ogtitle='独身税はいくら？年収から目安を計算', ogdesc='子ども・子育て支援金（2026年4月〜）の月負担目安を年収から概算。',
  h1='「独身税」はいくら？ 支援金 目安計算',
  lead='SNSで「独身税」と呼ばれている<b>子ども・子育て支援金</b>が、2026年4月から始まりました。あなたの年収だと月いくらになるのか、目安を計算します。<b>実は独身の人だけが払うものではありません</b>——正しい中身もあわせてどうぞ。',
  inputs='''    <h2>🧾 条件を入れる</h2>
    <div class="field"><label>年収（額面） <span class="hint">（万円）</span></label><input type="number" id="n" value="400" min="0" max="3000" inputmode="numeric"></div>
    <div class="field"><label>年度</label><select id="y"><option value="250" selected>2026年度（初年度）</option><option value="350">2027年度</option><option value="450">2028年度〜（満額）</option></select></div>
    <button class="btn btn-primary" id="calcBtn">月いくらか計算する</button>''',
  result='''      <div class="label">あなたの月負担の目安</div>
      <div class="big"><span id="big">0</span><span class="unit">円/月</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">年間だと</div><div class="v" id="year">—</div></div>
      <div class="stat"><div class="k">全体平均</div><div class="v accent" id="avg">—</div></div>
      <div class="stat"><div class="k">徴収方法</div><div class="v" id="how">—</div></div></div>''',
  article=C('「独身税」は俗称で、正式には<b>子ども・子育て支援金</b>。児童手当の拡充や育休給付の財源として、<b>公的医療保険の保険料に上乗せ</b>して徴収されます。医療保険に入っている人全員——<b>既婚でも子育て中でも</b>——が負担するため、「独身者だけに課される税」ではありません。')+'''
    <h2>徴収スケジュールと負担の目安</h2>
    <div class="tbl-scroll"><table class="seo-table"><tr><th>年度</th><th>加入者1人あたり平均（月）</th></tr>
    <tr><td>2026年度</td><td>約250円</td></tr>
    <tr><td>2027年度</td><td>約350円</td></tr>
    <tr><td>2028年度〜</td><td>約450円</td></tr></table></div>
    <p>実際の負担額は加入する医療保険（協会けんぽ・健保組合・国保など）と収入に応じて変わります。会社員は労使折半で給与天引き。本ツールは「平均450円＝平均的な年収の人」と仮定し、年収に比例させた<b>ざっくり目安</b>です。正確な額は加入先の保険者の案内をご確認ください。</p>
    <p>「独身税」という言葉が広まった背景には、子育て世帯には児童手当などの給付で還元される一方、独身者は負担だけが増える——という実感があります。制度の是非はさておき、まず自分の負担額を知ることが第一歩です。手取りへの影響は<a href="/sims/tedori/">手取り計算</a>、副業の税金は<a href="/sims/fukugyo-zei/">副業の税金シミュレーター</a>でどうぞ。</p>
    <h2>よくある質問</h2>'''+faq([
    ('独身税って本当にあるの？','「独身税」という税金はありません。子ども・子育て支援金の俗称です。医療保険加入者全員が負担し、独身者に限定した制度ではありません。'),
    ('いつから引かれる？','2026年4月分から、医療保険料とあわせて徴収が始まっています。給与明細の保険料項目に含まれます。'),
    ('金額は今後どうなる？','2026年度・約250円→2027年度・約350円→2028年度以降・約450円（加入者平均・月額）と段階的に上がる計画です。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['子ども・子育て支援法等の一部改正（2024年成立・支援金制度）','こども家庭庁 支援金制度の負担額試算（加入者平均 月250〜450円）']),
  js='''  function calc(){
    const n=Math.max(0,+$('n').value||0), base=+$('y').value;
    const AVG_INCOME=460;                       // 全体平均年収の仮定（万円）
    const m=Math.round(base*(n/AVG_INCOME));
    $('sub').textContent=`年収${n}万円・${sel('y').text}の目安（収入比例のざっくり計算）`;
    $('year').textContent=(m*12).toLocaleString('ja-JP')+'円';
    $('avg').textContent=base+'円/月';
    $('how').textContent='医療保険料に上乗せ';
    show(); anim($('big'),0,m,700);
    SHARE=`「独身税」（子ども・子育て支援金）、年収${n}万円だと月${m}円くらいの目安でした🧾 独身者だけの税じゃないの知ってた？`;
  }''')

# ============================================================
# 7. バストサイズ 計算・早見（美容・ファッション）
# ============================================================
add(id='bust-size', cat='美容・ファッション', emoji='🎀',
  title='バストサイズ 計算・早見表|トップとアンダーからカップ数を判定|シミュラボ',
  desc='トップバストとアンダーバストを入れるだけで、A〜Kカップとブラのサイズ表記（C70など）を判定する無料ツール。正しい測り方、カップ数の決まり方（差2.5cm刻み）、早見表つき。',
  ogtitle='バストサイズ 計算|カップ数を判定', ogdesc='トップとアンダーの差からカップ数とブラ表記を判定。早見表つき。',
  h1='バストサイズ 計算（カップ数 判定）',
  lead='トップバストとアンダーバストの2つの数字で、カップ数とブラのサイズ表記が分かります。「今のブラ、合ってる？」の確認にもどうぞ。',
  inputs='''    <h2>🎀 サイズを入れる</h2>
    <div class="row"><div class="field"><label>トップバスト <span class="hint">（胸のいちばん高い位置/cm）</span></label><input type="number" id="t" value="88" min="50" max="150" step="0.5" inputmode="decimal"></div>
    <div class="field"><label>アンダーバスト <span class="hint">（胸のすぐ下/cm）</span></label><input type="number" id="u" value="70" min="50" max="120" step="0.5" inputmode="decimal"></div></div>
    <button class="btn btn-primary" id="calcBtn">カップ数を判定する</button>''',
  result='''      <div class="label">あなたのサイズ</div>
      <div class="big" style="font-size:44px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">トップとの差</div><div class="v accent" id="sa">—</div></div>
      <div class="stat"><div class="k">アンダー区分</div><div class="v" id="under">—</div></div>
      <div class="stat"><div class="k">隣接サイズ</div><div class="v" id="tonari">—</div></div></div>''',
  article=C('カップ数は<b>「トップバスト − アンダーバスト」の差</b>で決まります。差が約10cmでAカップ、以降<b>2.5cm増えるごとに1カップ</b>上がります（JIS規格）。ブラの表記は「カップ＋アンダー」で、例えば差12.5cm・アンダー70cmなら「B70」です。')+'''
    <h2>カップ数 早見表（JIS）</h2>
    <div class="tbl-scroll"><table class="seo-table"><tr><th>トップ−アンダーの差</th><th>カップ</th></tr>
    <tr><td>約7.5cm</td><td>AA</td></tr>
    <tr><td>約10cm</td><td>A</td></tr>
    <tr><td>約12.5cm</td><td>B</td></tr>
    <tr><td>約15cm</td><td>C</td></tr>
    <tr><td>約17.5cm</td><td>D</td></tr>
    <tr><td>約20cm</td><td>E</td></tr>
    <tr><td>約22.5cm</td><td>F</td></tr>
    <tr><td>約25cm</td><td>G</td></tr></table></div>
    <h2>正しい測り方のコツ</h2>
    <ul>
    <li>メジャーは<b>床と水平</b>に。鏡の前で確認しながら測ると正確です。</li>
    <li>トップは胸のいちばん高いところ、アンダーは胸のふくらみのすぐ下。</li>
    <li>時間帯やむくみで1〜2cm変わることがあります。夕方より<b>朝〜昼</b>が安定。</li>
    <li>試着時はカップが浮かないか・アンダーが食い込まないかを確認。同じ表記でもメーカーで着け心地は変わります。</li>
    </ul>
    <p>サイズが変わったと感じたら、体重や姿勢の変化も影響しています。<a href="/sims/taiju/">半年後の体重シミュレーター</a>もあわせてどうぞ。</p>
    <h2>よくある質問</h2>'''+faq([
    ('隣のサイズと迷ったら？','「カップを1つ上げてアンダーを1つ下げる（またはその逆）」と容量が近い「兄弟サイズ」になります。B70とA75は近い容量です。'),
    ('左右で大きさが違う','多くの人にあることです。大きい方に合わせてパッドで調整するのが一般的です。'),
    ('測るタイミングは？','むくみの少ない朝〜昼、素肌かノンパッドのブラの上から測るのが安定します。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['JIS L4006（ファンデーションガーメントのサイズ）']),
  js='''  function calc(){
    const t=+$('t').value||0, u=+$('u').value||0;
    if(t<=u){alert('トップはアンダーより大きい値を入れてね');return;}
    const sa=t-u;
    const CUPS=['AA','A','B','C','D','E','F','G','H','I','J','K'];
    let ci=Math.round((sa-7.5)/2.5); ci=Math.max(0,Math.min(CUPS.length-1,ci));
    const cup=CUPS[ci];
    const und=Math.round(u/5)*5;
    $('big').textContent=cup+und;
    $('sub').textContent=`トップ${t}cm − アンダー${u}cm ＝ 差${sa.toFixed(1)}cm`;
    $('sa').textContent=sa.toFixed(1)+'cm';
    $('under').textContent=und+'（'+(und-2.5)+'〜'+(und+2.5)+'cm）';
    $('tonari').textContent=(ci>0?CUPS[ci-1]+(und+5):'')+(ci>0?' / ':'')+(ci<CUPS.length-1?CUPS[ci+1]+(und-5>=50?und-5:und):'');
    show();
    SHARE=`バストサイズ計算でサイズをチェックしました🎀 測り方のコツも分かる`;
  }''')

# ============================================================
# 8. 脈拍・心拍数の平均（健康・カラダ）
# ============================================================
add(id='myakuhaku-heikin', cat='健康・カラダ', emoji='💓',
  title='脈拍の平均は？安静時心拍数を年齢別の正常値とくらべてチェック|シミュラボ',
  desc='安静時の脈拍（心拍数）を入れると、年齢別の平均・正常範囲（成人60〜100bpm）とくらべて低め/標準/高めを判定する無料ツール。正しい測り方、アスリートの心拍が低い理由、受診の目安も解説。',
  ogtitle='脈拍の平均は？安静時心拍を判定', ogdesc='安静時脈拍を年齢別の平均・正常範囲と比較して判定。測り方も解説。',
  h1='脈拍・心拍数 平均チェック',
  lead='安静時の脈拍を測って入れると、年齢別の平均・正常範囲とくらべます。<b>手首に指3本を当てて15秒数え、4倍する</b>だけで測れます。',
  inputs='''    <h2>💓 測って入れる</h2>
    <div class="row"><div class="field"><label>安静時の脈拍 <span class="hint">（回/分）</span></label><input type="number" id="p" value="72" min="30" max="200" inputmode="numeric"></div>
    <div class="field"><label>年齢</label><select id="a"><option value="adult" selected>18歳以上（成人）</option><option value="teen">12〜17歳</option><option value="child">6〜11歳</option><option value="infant">1〜5歳</option></select></div></div>
    <button class="btn btn-primary" id="calcBtn">平均とくらべる</button>''',
  result='''      <div class="label">判定</div>
      <div class="big" style="font-size:32px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">正常範囲の目安</div><div class="v accent" id="range">—</div></div>
      <div class="stat"><div class="k">あなた</div><div class="v" id="you">—</div></div>
      <div class="stat"><div class="k">位置</div><div class="v" id="pos">—</div></div></div>''',
  article=C('安静時の心拍数（脈拍）の正常範囲は、成人でおよそ<b>60〜100回/分</b>。子どもは体が小さいぶん速く、鍛えたアスリートは<b>40〜60回/分</b>まで下がることもあります（スポーツ心臓）。一般に、安静時心拍が低めの人ほど心肺機能が高い傾向があります。')+'''
    <h2>年齢別の安静時心拍の目安</h2>
    <div class="tbl-scroll"><table class="seo-table"><tr><th>年齢</th><th>目安（回/分）</th></tr>
    <tr><td>1〜5歳</td><td>80〜140</td></tr>
    <tr><td>6〜11歳</td><td>75〜120</td></tr>
    <tr><td>12〜17歳</td><td>60〜105</td></tr>
    <tr><td>成人</td><td>60〜100</td></tr>
    <tr><td>鍛えた人</td><td>40〜60 のことも</td></tr></table></div>
    <h2>正しい測り方</h2>
    <ul>
    <li>起床後や、5分以上座って落ち着いた状態で測る（動いた直後はNG）。</li>
    <li>手首の親指側に人差し指・中指・薬指の3本を軽く当てる。</li>
    <li><b>15秒数えて4倍</b>する（スマートウォッチの安静時心拍でもOK）。</li>
    </ul>
    <div class="alert bad">※本ツールは一般的な目安による情報提供で、診断ではありません。安静時に脈が常に100超（頻脈）・50未満（徐脈）が続く、脈が飛ぶ・乱れる、動悸やめまいを伴う——といった場合は医療機関にご相談ください。</div>
    <p>運動時の目標心拍は<a href="/sims/shinpaku/">心拍ゾーン計算</a>、血圧が気になる方は<a href="/sims/ketsuatsu-check/">血圧チェック</a>もどうぞ。</p>
    <h2>よくある質問</h2>'''+faq([
    ('脈拍と心拍数は同じ？','ほぼ同じ意味で使われます。厳密には心臓の拍動が心拍、手首などで触れる拍動が脈拍で、不整脈があるとズレることがあります。'),
    ('低いほうが健康？','持久系の運動をしている人は低くなる傾向があり、一般に心肺機能の高さと関連します。ただし急に下がった・めまいを伴う場合は受診を。'),
    ('緊張やカフェインで変わる？','変わります。緊張・カフェイン・睡眠不足・発熱などで上がるため、落ち着いた同じ条件で測りましょう。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['安静時心拍数の一般的な正常範囲（成人60〜100bpm）','日本循環器学会等の一般向け解説（頻脈・徐脈の目安）']),
  js='''  function calc(){
    const p=Math.max(30,Math.min(200,+$('p').value||70));
    const R={adult:[60,100],teen:[60,105],child:[75,120],infant:[80,140]}[$('a').value];
    let h,sub;
    if(p<R[0]){h='低め（徐脈ぎみ）';sub='鍛えている人なら自然なことも。だるさ・めまいを伴うなら受診を。';}
    else if(p<=R[1]){h='正常範囲';sub='年齢相応の落ち着いた脈です。';}
    else{h='高め（頻脈ぎみ）';sub='緊張・カフェイン・睡眠不足でも上がります。安静時に続くなら受診を。';}
    $('big').textContent=h; $('sub').textContent=sub;
    $('range').textContent=R[0]+'〜'+R[1]+' 回/分';
    $('you').textContent=p+' 回/分';
    const pos=Math.round((p-R[0])/(R[1]-R[0])*100);
    $('pos').textContent = pos<0?'範囲より下':pos>100?'範囲より上':'範囲の'+pos+'%あたり';
    show();
    SHARE=`脈拍チェック、私の安静時${p}回/分は「${h}」でした💓`;
  }''')

# ============================================================
# 9. 握力 平均 比較（スポーツ・運動）
# ============================================================
add(id='akuryoku-heikin', cat='スポーツ・運動', emoji='💪',
  title='握力の平均は何kg？年齢別・男女別の平均と自分を比較|シミュラボ',
  desc='あなたの握力は平均より上？下？スポーツ庁の体力・運動能力調査に基づく年齢別・男女別の平均値（目安）とくらべて判定する無料ツール。中学生・高校生から70代まで対応。握力と健康寿命の関係も解説。',
  ogtitle='握力の平均は何kg？年齢別に比較', ogdesc='年齢別・男女別の握力平均とあなたの記録を比較して判定。',
  h1='握力 平均 比較シミュレーター',
  lead='あなたの握力、同年代の平均とくらべて強い？弱い？ 年齢・性別を選んで記録を入れると、全国調査ベースの平均値（目安）と比較します。',
  inputs='''    <h2>💪 記録を入れる</h2>
    <div class="row"><div class="field"><label>握力 <span class="hint">（kg・左右の平均か利き手）</span></label><input type="number" id="g" value="40" min="1" max="120" step="0.5" inputmode="decimal"></div>
    <div class="field"><label>性別</label><select id="s"><option value="m" selected>男性</option><option value="f">女性</option></select></div></div>
    <div class="field"><label>年代</label><select id="a">
      <option value="13">中学生（13〜15歳）</option>
      <option value="16">高校生（16〜18歳）</option>
      <option value="20" selected>20代</option><option value="30">30代</option><option value="40">40代</option>
      <option value="50">50代</option><option value="60">60代</option><option value="70">70代</option>
    </select></div>
    <button class="btn btn-primary" id="calcBtn">平均とくらべる</button>''',
  result='''      <div class="label">同年代の平均との差</div>
      <div class="big"><span id="big">0</span><span class="unit">kg</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">同年代の平均（目安）</div><div class="v accent" id="avg">—</div></div>
      <div class="stat"><div class="k">判定</div><div class="v" id="hantei">—</div></div>
      <div class="stat"><div class="k">ピーク年代</div><div class="v" id="peak">30代</div></div></div>''',
  article=C('握力の平均は<b>成人男性でおよそ45〜47kg、成人女性で27〜28kg</b>。30代でピークを迎え、その後ゆるやかに低下します。握力は全身の筋力をよく反映する指標で、<b>握力が強い人ほど健康寿命が長い</b>という研究報告が国内外で知られています。')+'''
    <h2>握力の平均 早見表（目安）</h2>
    <div class="tbl-scroll"><table class="seo-table"><tr><th>年代</th><th>男性</th><th>女性</th></tr>
    <tr><td>中学生</td><td>約30kg</td><td>約24kg</td></tr>
    <tr><td>高校生</td><td>約41kg</td><td>約26kg</td></tr>
    <tr><td>20代</td><td>約46kg</td><td>約28kg</td></tr>
    <tr><td>30代</td><td>約47kg</td><td>約28kg</td></tr>
    <tr><td>40代</td><td>約46kg</td><td>約28kg</td></tr>
    <tr><td>50代</td><td>約44kg</td><td>約26kg</td></tr>
    <tr><td>60代</td><td>約40kg</td><td>約24kg</td></tr>
    <tr><td>70代</td><td>約35kg</td><td>約22kg</td></tr></table></div>
    <p>※スポーツ庁「体力・運動能力調査」の結果をもとにした丸めた目安です。握力は「全身の筋力の窓」とも呼ばれ、中高年では<b>男性26kg未満・女性18kg未満</b>がサルコペニア（筋肉減少）のスクリーニング基準に使われます。ペットボトルのフタが開けにくくなったら要注意サインです。</p>
    <p>他の種目もチェックするなら<a href="/sims/tairyoku-hyouka/">体力テスト評価</a>、運動の消費カロリーは<a href="/sims/undo-calorie/">運動カロリー計算</a>もどうぞ。</p>
    <h2>よくある質問</h2>'''+faq([
    ('握力は何歳がピーク？','男女とも30代前後がピークで、以降は10年で2〜3kgずつ低下する傾向があります。'),
    ('左右どちらで測る？','体力テストでは左右2回ずつ測り、左右それぞれの良い方の平均を記録とします。利き手の方が2〜3kg強いのが普通です。'),
    ('握力を鍛えるには？','ハンドグリッパーだけでなく、懸垂・デッドリフトなど「握って支える」種目や、日常で重い物を運ぶことも効果的です。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['スポーツ庁 体力・運動能力調査（握力の年齢別平均）','サルコペニア診断基準 AWGS2019（握力 男性28kg未満/女性18kg未満の低筋力基準）']),
  js='''  function calc(){
    const AV={m:{13:30,16:41,20:46,30:47,40:46,50:44,60:40,70:35},f:{13:24,16:26,20:28,30:28,40:28,50:26,60:24,70:22}};
    const g=+$('g').value||0, s=$('s').value, a=$('a').value;
    const avg=AV[s][a], diff=g-avg, r=g/avg;
    let h; if(r>=1.25)h='かなり強い'; else if(r>=1.08)h='平均より強い'; else if(r>=0.92)h='ほぼ平均'; else if(r>=0.75)h='平均より弱め'; else h='かなり弱め';
    $('sub').textContent = diff>=0 ? `同年代平均より ${Math.abs(diff).toFixed(1)}kg 強い` : `同年代平均より ${Math.abs(diff).toFixed(1)}kg 弱い`;
    $('avg').textContent=avg+'kg'; $('hantei').textContent=h;
    show(); anim($('big'),0,Math.abs(diff),700,1);
    SHARE=`握力 平均比較、私は同年代平均より${Math.abs(diff).toFixed(1)}kg${diff>=0?'強い':'弱い'}（${h}）でした💪`;
  }''')

# ============================================================
# 10. アラサーは何歳から？判定（人生・自分ごと）
# ============================================================
add(id='arasa-hantei', cat='人生・自分ごと', emoji='🎂',
  title='アラサーは何歳から何歳まで？アラフォー・アラフィフも年齢判定|シミュラボ',
  desc='アラサーは何歳から？を年齢を入れるだけで判定する無料ツール。アラサー/アラフォー/アラフィフ/アラカン/アラハタの範囲（±2〜3歳説と25〜34歳説）、次の呼称まであと何年か、「初老」の本来の意味も解説。',
  ogtitle='アラサーは何歳から？年齢で判定', ogdesc='アラサー/アラフォー/アラフィフを年齢から判定。諸説の範囲も解説。',
  h1='アラサー・アラフォー 判定',
  lead='「自分ってもうアラサー？」を年齢ひとつで判定。アラハタからアラカンまで、いまの呼ばれ方と「次の呼称まであと何年か」を表示します。',
  inputs='''    <h2>🎂 年齢を入れる</h2>
    <div class="field"><label>年齢 <span class="hint">（歳）</span></label><input type="number" id="a" value="28" min="10" max="100" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">判定する</button>''',
  result='''      <div class="label">あなたはいま</div>
      <div class="big" style="font-size:40px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">範囲（±5歳説）</div><div class="v" id="hani">—</div></div>
      <div class="stat"><div class="k">次の呼称まで</div><div class="v accent" id="next">—</div></div>
      <div class="stat"><div class="k">ど真ん中度</div><div class="v" id="center">—</div></div></div>''',
  article=C('アラサーは「around 30（アラウンド・サーティー）」の略。<b>広い説では25〜34歳</b>、狭い説では27〜33歳ごろを指します。もともとは2000年代の女性ファッション誌が使い始めた言葉で、いまでは男女問わず定着しました。')+'''
    <h2>「アラ◯◯」早見表</h2>
    <div class="tbl-scroll"><table class="seo-table"><tr><th>呼称</th><th>中心</th><th>広い説（±5歳）</th></tr>
    <tr><td>アラハタ</td><td>20歳</td><td>15〜24歳</td></tr>
    <tr><td>アラサー</td><td>30歳</td><td>25〜34歳</td></tr>
    <tr><td>アラフォー</td><td>40歳</td><td>35〜44歳</td></tr>
    <tr><td>アラフィフ</td><td>50歳</td><td>45〜54歳</td></tr>
    <tr><td>アラカン（アラ還）</td><td>60歳</td><td>55〜64歳</td></tr>
    <tr><td>アラコキ</td><td>70歳</td><td>65〜74歳</td></tr></table></div>
    <h2>ちなみに「初老」は本来40歳</h2>
    <p>いまでは60代くらいのイメージで使われる「初老」ですが、<b>本来は40歳の異称</b>です。奈良〜平安時代の長寿の祝い「四十の賀」に由来し、当時の40歳は立派な長寿の入り口でした。言葉の感覚が時代とともにスライドしてきた好例です。</p>
    <p>実年齢より気になるのは中身かもしれません——<a href="/sims/mental-age/">精神年齢診断</a>、<a href="/sims/ojisan-do/">おじさん度診断</a>・<a href="/sims/obasan-do/">おばさん度診断</a>もどうぞ。</p>
    <h2>よくある質問</h2>'''+faq([
    ('アラサーは何歳から何歳まで？','広い説では25〜34歳、狭い説では27〜33歳ごろ。「30歳前後」を指す言葉で、厳密な定義はありません。'),
    ('25歳はアラサー？','広い説（±5歳）ならアラサー入りです。狭い説（±2〜3歳）ならまだ手前。本ツールは±5歳説で判定しています。'),
    ('アラサーの次は？','アラフォー（35〜44歳）です。判定結果に「次の呼称まであと何年」も表示されます。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['「アラサー」の語誌（2000年代の女性誌発祥の和製英語）','初老＝四十の賀（40歳の異称）の辞書的解説']),
  js='''  function calc(){
    const a=Math.max(10,Math.min(100,+$('a').value||28));
    const L=[['アラハタ',20],['アラサー',30],['アラフォー',40],['アラフィフ',50],['アラカン',60],['アラコキ',70],['アラハチ（傘寿前後）',80],['アラキュー（卒寿前後）',90]];
    let cur=null,next=null;
    for(const [name,c] of L){ if(a>=c-5&&a<=c+4){cur=[name,c];} }
    for(const [name,c] of L){ if(c-5>a){next=[name,c];break;} }
    if(!cur){cur=a<15?['10代前半',a]:['大台超え',100];}
    $('big').textContent=cur[0];
    $('sub').textContent=`${a}歳 →「${cur[0]}」（中心${cur[1]}歳・±5歳説で判定）`;
    $('hani').textContent=(cur[1]-5)+'〜'+(cur[1]+4)+'歳';
    $('next').textContent= next? 'あと'+(next[1]-5-a)+'年で'+next[0] : '—';
    const d=Math.abs(a-cur[1]);
    $('center').textContent= d===0?'ど真ん中！':d<=2?'ほぼ中心':'入り口/出口ぎわ';
    show();
    SHARE=`アラサー判定、${a}歳の私は「${cur[0]}」でした🎂 あなたはどれ？`;
  }''')

if __name__=='__main__':
    write_all(SIMS)
    print(f'fable10 done. {len(SIMS)} sims.')
