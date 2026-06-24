# -*- coding: utf-8 -*-
"""シミュラボ：妊娠・出産・妊活 4本（新カテゴリ slug=ninkatsu）。排卵日・妊娠週数・生理周期・基礎体温。
new Date()で日付計算。YMYL配慮の免責付き（避妊には使えない旨も明記）。
gen_sims_tool TPL流用。seo_internal.py / gen_images.py のauto-importに 'gen_sims_ninkatsu' を追加。
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims11 import faq
from gen_sims_tool import TPL, viz
from sim_quiz import make_engines
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CAT = '妊娠・出産・妊活'
SIMS = []
tally_quiz, num_quiz, band_quiz, add, q_article, render = make_engines(SIMS, CAT, TPL, viz)
NIN = '※生理周期には個人差があり、計算はあくまで目安です。避妊・妊娠の判断には使えません。心配なことは医療機関にご相談ください。'

RES_TEXT = '''      <div class="label">__LBL__</div>
      <div id="emoji" style="font-size:46px;line-height:1.1;">🌸</div>
      <div class="big" style="font-size:24px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="desc" style="text-align:left;margin-top:14px;">—</div>'''

# ============================================================
# 1. 排卵日計算（排卵日 計算 2700/KD0/TP23000）★
# ============================================================
add(id='hairan-keisan', emoji='🌸',
  title='排卵日計算機｜生理開始日と周期から排卵日・妊娠しやすい時期｜シミュラボ',
  desc='最終の生理開始日と生理周期を入れるだけで、次の排卵日の予測と、妊娠しやすい時期（タイミング）の目安が分かる無料ツール。妊活の参考に。※避妊には使えません。',
  ogtitle='排卵日計算機｜排卵日・妊娠しやすい時期', ogdesc='生理開始日と周期から排卵日・妊娠しやすい時期を予測。',
  h1='排卵日計算機',
  lead='次の排卵はいつ?最終の生理開始日と周期を入れると、排卵日の予測と妊娠しやすい時期の目安を表示します。妊活のタイミングの参考に。',
  inputs='''    <h2>🌸 生理の情報を入れる</h2>
    <div class="field"><label>最終の生理開始日</label><input type="date" id="last" value="2026-06-01"></div>
    <div class="field"><label>生理周期 <span class="hint">日（一般に25〜38日）</span></label><input type="number" id="cycle" value="28" min="20" max="45" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">排卵日を計算</button>''',
  result=RES_TEXT.replace('__LBL__','排卵日の予測'),
  article='''    <div class="note"><strong>計算の考え方</strong><br>次回生理予定日 ＝ 最終生理開始日 ＋ 周期／排卵日 ≒ 次回生理予定日 − 14日／妊娠しやすい時期 ≒ 排卵日の5日前〜翌日</div>
    <h2>排卵日と妊娠しやすい時期</h2>
    <p>排卵は、次の生理が始まる約14日前に起こるとされます。精子は数日生きられるため、妊娠しやすいのは「排卵日の数日前〜排卵当日」です。本ツールは生理周期から機械的に予測しますが、排卵のタイミングは体調やストレスで前後します。より正確に知りたい場合は、基礎体温や排卵検査薬を併用しましょう。'''+NIN+'''</p>
    <h2>よくある質問</h2>'''+faq([
      ('周期が分からない','一般的な28日で計算できます。ばらつく場合は平均を入れてみてください。'),
      ('避妊に使える？','いいえ。排卵は前後するため、避妊の判断には使えません。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function fmt(d){return (d.getMonth()+1)+'月'+d.getDate()+'日('+['日','月','火','水','木','金','土'][d.getDay()]+')';}
  function calc(){const lv=$('last').value;if(!lv){$('big').textContent='—';$('sub').textContent='生理開始日を入れてね';show();return;}
    const last=new Date(lv),cyc=Math.max(20,Math.min(45,+$('cycle').value||28));
    const next=new Date(last);next.setDate(last.getDate()+cyc);
    const ov=new Date(next);ov.setDate(next.getDate()-14);
    const s=new Date(ov);s.setDate(ov.getDate()-5);const e=new Date(ov);e.setDate(ov.getDate()+1);
    $('emoji').textContent='🌸';$('big').textContent=fmt(ov)+' ごろ';$('sub').textContent='次回生理予定：'+fmt(next);
    $('desc').textContent='💕 妊娠しやすい時期の目安は '+fmt(s)+' 〜 '+fmt(e)+' ごろ。あくまで予測で、排卵は前後します。';
    SHARE='排卵日計算機、次の排卵日は '+fmt(ov)+' ごろの予測でした🌸';show();}
''')

# ============================================================
# 2. 妊娠週数計算（妊娠週数 計算 2600/KD2/TP46000）★★
# ============================================================
add(id='ninshin-shusu', emoji='🤰',
  title='妊娠週数計算機｜最終生理日から今は妊娠何週？出産予定日も｜シミュラボ',
  desc='最終の生理開始日を入れるだけで、今日時点の妊娠週数・妊娠月数・妊娠期（初期/中期/後期）と、出産予定日を計算する無料ツール。妊娠の経過チェックに。',
  ogtitle='妊娠週数計算機｜今は妊娠何週？', ogdesc='最終生理日から妊娠週数・月数・出産予定日を計算。',
  h1='妊娠週数計算機',
  lead='今、妊娠何週?最終の生理開始日を入れると、今日時点の妊娠週数・月数・妊娠期と、出産予定日を計算します。',
  inputs='''    <h2>🤰 最終の生理開始日</h2>
    <div class="field"><label>最終の生理開始日</label><input type="date" id="last" value="2026-03-01"></div>
    <div class="field"><label>基準日 <span class="hint">（空欄で今日）</span></label><input type="date" id="base"></div>
    <button class="btn btn-primary" id="calcBtn">妊娠週数を計算</button>''',
  result='''      <div class="label">妊娠週数（今日時点）</div>
      <div class="big" style="font-size:30px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">妊娠月数</div><div class="v" id="month">—</div></div>
      <div class="stat"><div class="k">妊娠期</div><div class="v accent" id="tri">—</div></div>
      <div class="stat"><div class="k">出産予定日</div><div class="v" id="due">—</div></div></div>''',
  article='''    <div class="note"><strong>計算の考え方</strong><br>妊娠週数 ＝ 最終生理開始日からの日数 ÷ 7（最終生理開始日を0週0日とする）／出産予定日 ＝ 最終生理開始日 ＋ 280日（40週0日）</div>
    <h2>妊娠週数の数え方</h2>
    <p>妊娠週数は、最終生理の開始日を「0週0日」として数えます（排卵・受精は約2週0日ごろ）。妊娠期間は約40週（280日）で、出産予定日は最終生理開始日に280日を足して求めます。妊娠15週までを初期、16〜27週を中期、28週以降を後期と呼びます。実際の週数は、超音波検査で修正されることがあります。'''+NIN+'''</p>
    <h2>よくある質問</h2>'''+faq([
      ('予定日とずれることはある？','はい。実際は検診の超音波で週数・予定日が修正されることがあります。'),
      ('生理不順だと？','正確性が下がります。受診時の超音波での確認が確実です。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function fmt(d){return d.getFullYear()+'年'+(d.getMonth()+1)+'月'+d.getDate()+'日';}
  function calc(){const lv=$('last').value;if(!lv){$('big').textContent='—';$('sub').textContent='最終生理開始日を入れてね';show();return;}
    const last=new Date(lv),base=$('base').value?new Date($('base').value):new Date();
    const days=Math.floor((base-last)/86400000);
    if(days<0){$('big').textContent='—';$('sub').textContent='基準日が生理開始日より前です';show();return;}
    const w=Math.floor(days/7),d=days%7;const month=Math.floor(w/4)+1;
    let tri=w<=15?'妊娠初期':w<=27?'妊娠中期':'妊娠後期';
    const due=new Date(last);due.setDate(last.getDate()+280);
    $('big').textContent='妊娠 '+w+'週'+d+'日';$('sub').textContent='最終生理開始日からの経過：'+days+'日';
    $('month').textContent='妊娠'+month+'ヶ月';$('tri').textContent=tri;$('due').textContent=fmt(due);
    SHARE='妊娠週数計算機、今日時点で妊娠'+w+'週'+d+'日（'+tri+'）でした🤰';show();}
''')

# ============================================================
# 3. 生理周期計算（生理周期 計算 2400/KD0/TP8500）★
# ============================================================
add(id='seiri-cycle', emoji='📅',
  title='生理周期計算機｜次の生理日・排卵日・今のカラダの時期｜シミュラボ',
  desc='最終の生理開始日と周期から、次回・次々回の生理予定日、排卵予定日、今がどの時期（月経期・卵胞期・排卵期・黄体期）かが分かる無料ツール。体調管理に。',
  ogtitle='生理周期計算機｜次の生理・排卵・今の時期', ogdesc='生理開始日と周期から次の生理日・排卵日・今の時期を表示。',
  h1='生理周期計算機',
  lead='次の生理はいつ?今はどの時期?最終の生理開始日と周期を入れると、次回・次々回の生理予定日、排卵予定、そして今のカラダの時期を表示します。',
  inputs='''    <h2>📅 生理の情報を入れる</h2>
    <div class="field"><label>最終の生理開始日</label><input type="date" id="last" value="2026-06-01"></div>
    <div class="field"><label>生理周期 <span class="hint">日</span></label><input type="number" id="cycle" value="28" min="20" max="45" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">周期を計算</button>''',
  result='''      <div class="label">今のカラダの時期（目安）</div>
      <div class="big" style="font-size:24px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">次の生理予定</div><div class="v accent" id="next1">—</div></div>
      <div class="stat"><div class="k">次々回の生理</div><div class="v" id="next2">—</div></div>
      <div class="stat"><div class="k">排卵予定</div><div class="v" id="ov">—</div></div></div>''',
  article='''    <div class="note"><strong>4つの時期</strong><br>月経期（生理中）→ 卵胞期（生理後〜排卵前）→ 排卵期（排卵前後）→ 黄体期（排卵後〜次の生理前）</div>
    <h2>生理周期と4つの時期</h2>
    <p>生理周期は、ホルモンの変化により大きく4つの時期に分かれます。卵胞期は心身が安定し調子が上がりやすく、排卵期は妊娠しやすい時期。黄体期はPMS（生理前の不調）が出やすい時期です。自分の周期を把握すると、体調や予定の管理に役立ちます。周期には個人差があり、ストレスや体調で変動します。'''+NIN+'''</p>
    <h2>よくある質問</h2>'''+faq([
      ('周期がバラバラ','平均を入れてみてください。大きく乱れる場合は受診も検討を。'),
      ('PMSがつらい','黄体期に不調が出やすいです。つらい場合は医療機関に相談を。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function fmt(d){return (d.getMonth()+1)+'/'+d.getDate()+'('+['日','月','火','水','木','金','土'][d.getDay()]+')';}
  function calc(){const lv=$('last').value;if(!lv){$('big').textContent='—';$('sub').textContent='生理開始日を入れてね';show();return;}
    const last=new Date(lv),cyc=Math.max(20,Math.min(45,+$('cycle').value||28));
    const next1=new Date(last);next1.setDate(last.getDate()+cyc);
    const next2=new Date(last);next2.setDate(last.getDate()+cyc*2);
    const ov=new Date(next1);ov.setDate(next1.getDate()-14);
    const today=new Date();const dd=Math.floor((today-last)/86400000)%cyc;const day=(dd+cyc)%cyc;
    const ovDay=cyc-14;let phase;
    if(day<=4)phase='月経期（生理中ごろ）';else if(day<ovDay-1)phase='卵胞期（調子が上がりやすい）';
    else if(day<=ovDay+1)phase='排卵期（妊娠しやすい）';else phase='黄体期（PMSが出やすい）';
    $('big').textContent=phase;$('sub').textContent='周期'+cyc+'日・開始から約'+day+'日目';
    $('next1').textContent=fmt(next1);$('next2').textContent=fmt(next2);$('ov').textContent=fmt(ov)+' ごろ';
    SHARE='生理周期計算機、今は「'+phase+'」、次の生理は '+fmt(next1)+' 予定でした📅';show();}
''')

# ============================================================
# 4. 基礎体温 判定（基礎体温 8700/KD3）
# ============================================================
add(id='kiso-taion', emoji='🌡️',
  title='基礎体温の高温期・低温期 判定｜今日の体温は高温相？低温相？｜シミュラボ',
  desc='今日の基礎体温と、あなたの低温期の平均から、今が高温期か低温期かの目安を判定する無料ツール。排卵のタイミングや妊活の参考に。基礎体温の見方も解説。',
  ogtitle='基礎体温の高温期・低温期 判定', ogdesc='今日の基礎体温から高温相/低温相の目安を判定。',
  h1='基礎体温の高温期・低温期 判定',
  lead='今日の基礎体温は高温期?低温期?今日の体温と低温期の平均を入れると、どちらの相にあたるかの目安を判定します。排卵のサインの参考に。',
  inputs='''    <h2>🌡️ 基礎体温を入れる</h2>
    <div class="field"><label>今日の基礎体温 <span class="hint">℃</span></label><input type="number" id="t" value="36.7" step="0.01" inputmode="decimal"></div>
    <div class="field"><label>低温期の平均 <span class="hint">℃（分からなければ36.40）</span></label><input type="number" id="base" value="36.40" step="0.01" inputmode="decimal"></div>
    <button class="btn btn-primary" id="calcBtn">高温期・低温期を判定</button>''',
  result='''      <div class="label">今日の判定</div>
      <div id="emoji" style="font-size:46px;">🌡️</div>
      <div class="big" style="font-size:24px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="desc" style="text-align:left;margin-top:14px;">—</div>''',
  article='''    <div class="note"><strong>高温期・低温期とは</strong><br>排卵を境に、低温期（卵胞期）から高温期（黄体期）へ移行します。一般に低温期と高温期の差は0.3℃以上が目安です。</div>
    <h2>基礎体温の見方</h2>
    <p>基礎体温は、毎朝起きてすぐ安静時に測る体温です。排卵が起こると黄体ホルモンの働きで体温が上がり、約2週間の「高温期」に入ります。低温期と高温期の差はおよそ0.3〜0.5℃。きれいな二相に分かれていれば、排卵があるサインとされます。1日の値だけでなく、毎日記録してグラフで見ることが大切です。'''+NIN+'''</p>
    <h2>よくある質問</h2>'''+faq([
      ('二相に分かれない','排卵がうまくいっていない可能性も。気になる場合は受診を。'),
      ('いつ測るの？','朝、目が覚めてすぐ、体を動かす前に婦人体温計で測ります。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const t=+$('t').value||0,base=+$('base').value||36.4;const diff=Math.round((t-base)*100)/100;
    let emoji,head,desc;
    if(diff>=0.3){emoji='☀️';head='高温相の可能性';desc='低温期の平均より'+diff.toFixed(2)+'℃高めです。排卵後の「高温期（黄体期）」に入っている可能性があります。';}
    else if(diff>=0.1){emoji='🌤️';head='移行期かも';desc='低温期よりやや高めです。これから高温期に入る、または個人差の範囲かもしれません。数日の記録で判断しましょう。';}
    else{emoji='❄️';head='低温相の可能性';desc='低温期の範囲内です。排卵前の「低温期（卵胞期）」の可能性があります。';}
    $('emoji').textContent=emoji;$('big').textContent=head;$('sub').textContent='今日 '+t.toFixed(2)+'℃ ／ 低温期平均との差 '+(diff>=0?'+':'')+diff.toFixed(2)+'℃';
    $('desc').textContent='📌 '+desc+' ※1日の値だけでなく毎日の記録が大切です。';
    SHARE='基礎体温の判定、今日は「'+head+'」でした🌡️';show();}
''')

if __name__=='__main__':
    render()
    print(f'ninkatsu done. {len(SIMS)} sims.')
