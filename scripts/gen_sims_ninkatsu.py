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

# ============================================================
# 5. 産休・育休 期間計算（産休 いつから 18000/KD4/TP79000）★★★
# ============================================================
add(id='sankyu-ikukyu', emoji='🗓️',
  title='産休・育休の期間計算機｜出産予定日から産休はいつから？育休いつまで？｜シミュラボ',
  desc='出産予定日を入れるだけで、産前・産後休業の期間と、育児休業の開始日・原則の終了日（子が1歳）・延長の目安が分かる無料ツール。仕事の引き継ぎや復帰計画に。',
  ogtitle='産休・育休の期間計算機｜いつからいつまで？', ogdesc='出産予定日から産前産後休業・育休の期間を計算。',
  h1='産休・育休の期間計算機',
  lead='産休っていつから?育休はいつまで?出産予定日を入れると、産前・産後休業と育児休業の期間の目安を表示します。職場への相談や復帰計画に。',
  inputs='''    <h2>🗓️ 出産予定日を入れる</h2>
    <div class="field"><label>出産予定日</label><input type="date" id="due" value="2026-10-01"></div>
    <button class="btn btn-primary" id="calcBtn">産休・育休の期間を見る</button>''',
  result='''      <div class="label">産前休業の開始日（目安）</div>
      <div class="big" style="font-size:26px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">産後休業の終了</div><div class="v" id="ago">—</div></div>
      <div class="stat"><div class="k">育休 開始</div><div class="v accent" id="ikustart">—</div></div>
      <div class="stat"><div class="k">育休 終了（原則・子が1歳）</div><div class="v" id="ikuend">—</div></div></div>''',
  article='''    <div class="note"><strong>期間の考え方</strong><br>産前休業：出産予定日の6週間前（42日前）から取得可／産後休業：出産日の翌日から8週間（56日）※原則／育児休業：産後休業の翌日〜原則子が1歳になる前日（保育園に入れない等で1歳6か月・最長2歳まで延長可）</div>
    <h2>産休・育休の期間</h2>
    <p>産前休業は出産予定日の6週間前から、産後休業は出産日の翌日から8週間です（産後6週間は就業不可、その後は本人が希望し医師が認めれば就業可）。育児休業はその後、原則として子が1歳になる前日まで取得できます。保育園に入れないなどの事情があれば1歳6か月、さらに2歳まで延長が可能です。本ツールは出産予定日をもとにした目安で、実際の出産日でずれます。'''+'※制度の詳細・延長要件は勤務先や役所でご確認ください。'+'''</p>
    <h2>よくある質問</h2>'''+faq([
      ('予定日とずれたら？','実際の出産日を基準に産後休業・育休が決まります。出産後に再確認しましょう。'),
      ('男性も育休を取れる？','取れます。「産後パパ育休」など男性向けの制度もあります。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function fmt(d){return d.getFullYear()+'年'+(d.getMonth()+1)+'月'+d.getDate()+'日';}
  function calc(){const dv=$('due').value;if(!dv){$('big').textContent='—';$('sub').textContent='出産予定日を入れてね';show();return;}
    const due=new Date(dv);
    const sanzen=new Date(due);sanzen.setDate(due.getDate()-42);
    const sango=new Date(due);sango.setDate(due.getDate()+56);
    const iku=new Date(sango);iku.setDate(sango.getDate()+1);
    const ikuend=new Date(due);ikuend.setFullYear(due.getFullYear()+1);ikuend.setDate(ikuend.getDate()-1);
    $('big').textContent=fmt(sanzen);$('sub').textContent='出産予定日 '+fmt(due)+' の6週間前';
    $('ago').textContent=fmt(sango);$('ikustart').textContent=fmt(iku);$('ikuend').textContent=fmt(ikuend);
    SHARE='産休・育休の期間計算、産休は '+fmt(sanzen)+' から・育休は子が1歳になる '+fmt(ikuend)+' まで（目安）でした🗓️';show();}
''')

# ============================================================
# 6. 陣痛間隔タイマー（陣痛 間隔 3500/KD2/TP11000）★★
# ============================================================
add(id='jintsuu-kankaku', emoji='⏱️',
  title='陣痛間隔タイマー｜タップで陣痛の間隔を計測・病院連絡の目安｜シミュラボ',
  desc='陣痛がくるたびにボタンをタップするだけで、陣痛の間隔（分）を自動で計測・記録する無料タイマー。初産・経産別に、病院へ連絡する目安もお知らせします。',
  ogtitle='陣痛間隔タイマー｜間隔を計測・病院連絡の目安', ogdesc='タップで陣痛の間隔を計測。病院連絡の目安も表示。',
  h1='陣痛間隔タイマー',
  lead='陣痛がきたらタップするだけ!間隔（分）を自動で計測・記録します。初産・経産別に、病院へ連絡する目安もお知らせ。落ち着いて測りましょう。',
  inputs='''    <h2>⏱️ 陣痛がきたらタップ</h2>
    <div class="field"><label>お産の回数</label><select id="kaisu"><option value="10" selected>初産（はじめての出産）</option><option value="15">経産（出産経験あり）</option></select></div>
    <div id="jlist" style="margin:8px 0;font-size:14px;color:var(--ink-2);min-height:24px;"></div>
    <button class="btn btn-primary" id="calcBtn" style="font-size:18px;padding:16px;">🔴 陣痛がきた（タップ）</button>
    <button class="btn btn-ghost" id="reset" style="margin-top:8px;">リセット</button>''',
  result='''      <div class="label">直近の陣痛間隔（平均）</div>
      <div class="big"><span id="big">—</span><span class="unit">分</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="advice" style="text-align:left;margin-top:12px;">—</div>''',
  article='''    <div class="note"><strong>使い方</strong><br>陣痛（おなかの張り）が始まった瞬間に「陣痛がきた」をタップ。次の陣痛でまたタップすると、その間隔が記録されます。<br><b>※規則的な間隔・破水・出血などがあれば、本ツールの数値にかかわらず産院に連絡してください。</b></div>
    <h2>陣痛の間隔と病院へ行くタイミング</h2>
    <p>陣痛は、子宮が収縮しておなかが張る痛みで、お産が近づくと間隔が短く・規則的になっていきます。一般的に、初産では陣痛が<b>10分間隔</b>（または1時間に6回）になったら、経産婦では<b>15分間隔</b>になったら産院に連絡する目安とされます。ただし、破水した・出血が多い・痛みが強く不安なときは、間隔に関わらずすぐ連絡を。本ツールは間隔を測る補助です。'''+'※医療行為ではありません。気になる症状があれば必ず産院・医療機関にご連絡ください。'+'''</p>
    <h2>よくある質問</h2>'''+faq([
      ('間隔はどこからどこまで？','一般に「陣痛の始まり」から「次の陣痛の始まり」までを1回の間隔として測ります。'),
      ('破水したら？','間隔に関わらず、すぐに産院へ連絡してください。'),
      ('データは送信されますか？','いいえ。計測はすべてブラウザ内で完結します。')]),
  js=r'''  let times=[];const list=$('jlist');
  function fmtT(d){return d.getHours()+':'+('0'+d.getMinutes()).slice(-2)+':'+('0'+d.getSeconds()).slice(-2);}
  function render(){if(times.length===0){list.textContent='まだ記録がありません。陣痛がきたらタップしてね。';return;}
    let h='記録：';const last=times.slice(-6);
    for(let i=0;i<last.length;i++){h+='<span style="display:inline-block;margin:2px 6px 2px 0">'+fmtT(new Date(last[i].t))+(last[i].iv!=null?('（'+last[i].iv.toFixed(1)+'分）'):'' )+'</span>';}
    list.innerHTML=h;}
  function calc(){const now=Date.now();const prev=times.length?times[times.length-1].t:null;
    const iv=prev!=null?(now-prev)/60000:null;times.push({t:now,iv:iv});render();
    const ivs=times.filter(x=>x.iv!=null).map(x=>x.iv);
    if(ivs.length===0){$('big').textContent='—';$('sub').textContent='次の陣痛でタップすると間隔が出ます';$('advice').className='alert good';$('advice').textContent='⏱️ 1回目を記録しました。次の陣痛がきたら、またタップしてね。';show();return;}
    const recent=ivs.slice(-3);const avg=recent.reduce((a,b)=>a+b,0)/recent.length;
    const th=+$('kaisu').value;$('big').textContent=avg.toFixed(1);$('sub').textContent='直近'+recent.length+'回の平均（記録'+ivs.length+'回）';
    if(avg<=th){$('advice').className='alert warn';$('advice').textContent='🏥 間隔が'+th+'分以下になっています（'+( $('kaisu').value=='10'?'初産':'経産')+'の連絡目安）。産院に連絡しましょう。※破水・出血・強い痛みがあれば間隔に関わらずすぐ連絡を。';}
    else{$('advice').className='alert good';$('advice').textContent='🤰 まだ間隔があります。落ち着いて記録を続けましょう。'+th+'分間隔が連絡の目安です（破水等があればすぐ連絡を）。';}
    show();}
  const rs=$('reset');if(rs)rs.addEventListener('click',()=>{times=[];render();$('resultPanel').style.display='none';});
  render();
''')

# ============================================================
# 7. 出産費用・自己負担シミュ（出産費用 7500 + 出産育児一時金 7200/TP21000）★★
# ============================================================
add(id='shussan-hiyou', emoji='💰',
  title='出産費用シミュレーター｜出産育児一時金を引いた自己負担はいくら？｜シミュラボ',
  desc='分娩・入院費から出産育児一時金（原則50万円）を差し引いた、出産費用の自己負担の目安を計算する無料ツール。正常分娩・帝王切開の選択や、地域差も考慮。',
  ogtitle='出産費用シミュレーター｜自己負担はいくら？', ogdesc='分娩入院費から一時金50万を引いた自己負担を計算。',
  h1='出産費用シミュレーター',
  lead='出産って結局いくらかかる?分娩・入院費から、出産育児一時金（原則50万円）を引いた自己負担の目安を計算します。出産前の準備に。',
  inputs='''    <h2>💰 条件を入れる</h2>
    <div class="field"><label>出産方法・部屋</label><select id="type">
      <option value="500000" selected>正常分娩（平均的な総額 約50万円）</option><option value="600000">正常分娩・個室など（約60万円）</option>
      <option value="450000">里帰り・地方（約45万円）</option><option value="650000">帝王切開（自己負担分含む 約65万円）</option></select></div>
    <div class="field"><label>出産育児一時金 <span class="hint">円（原則50万円）</span></label><input type="number" id="ichiji" value="500000" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">自己負担を計算</button>''',
  result='''      <div class="label">自己負担の目安</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">分娩・入院費の目安</div><div class="v" id="total">—</div></div>
      <div class="stat"><div class="k">出産育児一時金</div><div class="v accent" id="ichi">—</div></div></div>''',
  article='''    <div class="note"><strong>計算の考え方</strong><br>自己負担 ＝ 分娩・入院費 − 出産育児一時金（2023年4月から原則50万円）<br>※多くは「直接支払制度」で、病院窓口での支払いは差額のみになります。</div>
    <h2>出産費用と自己負担</h2>
    <p>出産（正常分娩）は病気ではないため健康保険が使えず、費用は全額自己負担が原則ですが、加入している健康保険から「出産育児一時金」として原則50万円が支給されます。多くの病院では「直接支払制度」が使え、窓口での支払いは費用から一時金を引いた差額だけ。費用が一時金を下回れば、差額が後から支給されます。費用は地域差が大きく、首都圏や個室利用では高くなる傾向です。帝王切開は手術部分に保険が適用され、高額療養費の対象にもなります。'''+'※金額は目安です。実際の費用・制度は医療機関や加入保険でご確認ください。'+'''</p>
    <h2>よくある質問</h2>'''+faq([
      ('一時金はどうやってもらう？','多くは「直接支払制度」で病院へ直接支払われ、差額だけ窓口で精算します。'),
      ('帝王切開は安くなる？','手術部分に保険が適用され、高額療養費制度の対象にもなります。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const total=+$('type').value||0,ichi=Math.max(0,+$('ichiji').value||0);
    const jiko=Math.max(0,total-ichi);
    $('sub').textContent=sel('type').text.split('（')[0]+' − 一時金'+num(ichi)+'円';
    $('total').textContent=yen(total);$('ichi').textContent=yen(ichi);
    SHARE='出産費用シミュ、自己負担の目安は約'+yen(jiko)+'（費用'+yen(total)+'−一時金'+yen(ichi)+'）でした💰';show();
    const el=$('big'),t0=performance.now();(function s(n){const p=Math.min(1,(n-t0)/700);el.textContent=Math.round(jiko*p).toLocaleString('ja-JP');if(p<1)requestAnimationFrame(s);else el.textContent=jiko.toLocaleString('ja-JP');})(performance.now());}
''')

if __name__=='__main__':
    render()
    print(f'ninkatsu done. {len(SIMS)} sims.')
