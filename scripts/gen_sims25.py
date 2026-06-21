# -*- coding: utf-8 -*-
"""シミュラボ：全カテゴリ3本ずつ補充 その4（sports/oshi/mental）。"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims11 import faq, write_all

SIMS=[]
def add(**k): SIMS.append(k)

def q(label, id, opts):
    o=''.join(f'<option value="{v}"{" selected" if i==1 else ""}>{t}</option>' for i,(v,t) in enumerate(opts))
    return f'<div class="field"><label>{label}</label><select id="{id}">{o}</select></div>'

# ===== スポーツ・運動 =====
add(id='yakyu-kyusoku', cat='スポーツ・運動', emoji='⚾',
  title='球速→反応時間シミュレーター｜時速◯kmの球、手元まで何秒？｜シミュラボ',
  desc='ピッチャーの球速とマウンドからの距離から、ボールが手元に届くまでの時間を計算し、打者の反応の難しさを体感できる無料シミュレーター。',
  ogtitle='球速→反応時間｜手元まで何秒？', ogdesc='球速と距離から、ボールが届くまでの時間を計算。',
  h1='球速→反応時間シミュレーター',
  lead='時速140kmの球は、手元に届くまで何秒？球速と距離から、ボールの到達時間を計算します。プロのバッターのすごさが数字で分かります。',
  inputs='''    <h2>⚾ 条件を入れる</h2>
    <div class="row"><div class="field"><label>球速 <span class="hint">（km/h）</span></label><input type="number" id="kmh" value="140" min="1" inputmode="numeric"></div>
    <div class="field"><label>距離 <span class="hint">（m・本塁まで18.44）</span></label><input type="number" id="dist" value="18.44" min="1" step="0.01" inputmode="decimal"></div></div>
    <button class="btn btn-primary" id="calcBtn">到達時間を見る</button>''',
  result='''      <div class="label">手元に届くまでの時間</div>
      <div class="big"><span id="big">0</span><span class="unit">秒</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">ミリ秒</div><div class="v accent" id="ms">—</div></div>
      <div class="stat"><div class="k">秒速</div><div class="v" id="mps">—</div></div>
      <div class="stat"><div class="k">人の反応(約0.2秒)と</div><div class="v" id="vs">—</div></div></div>''',
  article='''    <h2>バッターはすごい</h2>
    <div class="note"><strong>計算式</strong><br>到達時間 ＝ 距離 ÷ 秒速（秒速 ＝ km/h ÷ 3.6）</div>
    <p>時速140kmの球は約0.47秒で手元に到達。人間の反応速度が約0.2秒なので、見てから振るのでは間に合いません。だからバッターは「予測」して振っているのです。スポーツの奥深さ。</p>
    <h2>よくある質問</h2>'''+faq([('変化球は？','球速だけの単純計算です。変化球はさらに難易度が上がります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const kmh=Math.max(1,+$('kmh').value||1),dist=Math.max(1,+$('dist').value||1);const mps=kmh/3.6,t=dist/mps;
    $('sub').textContent=`時速${kmh}km・${dist}m`;$('ms').textContent=num(t*1000)+'ms';$('mps').textContent=mps.toFixed(1)+'m/s';$('vs').textContent=(t<0.2?'間に合わない！':'ギリ反応可');
    SHARE=`球速→反応時間シミュ、時速${kmh}kmの球は手元まで${t.toFixed(2)}秒(${num(t*1000)}ms)でした⚾\\nバッターってすごい…！👇`;show();anim($('big'),0,t,900,2);}''')

add(id='vertical-jump', cat='スポーツ・運動', emoji='🦘',
  title='垂直跳び 評価シミュレーター｜あなたのジャンプ力は？｜シミュラボ',
  desc='垂直跳びの記録と性別から、滞空時間とジャンプ力の評価レベルを判定する無料シミュレーター。',
  ogtitle='垂直跳び 評価｜あなたのジャンプ力は？', ogdesc='垂直跳びの記録から、滞空時間と評価レベルを判定。',
  h1='垂直跳び 評価シミュレーター',
  lead='あなたの垂直跳び、どのレベル？記録と性別から、滞空時間とジャンプ力の評価を判定します。バスケ・バレー好きにも。',
  inputs='''    <h2>🦘 条件を入れる</h2>
    <div class="row"><div class="field"><label>垂直跳びの記録 <span class="hint">（cm）</span></label><input type="number" id="cm" value="50" min="1" max="120" inputmode="numeric"></div>
    <div class="field"><label>性別</label><select id="sex"><option value="m">男性</option><option value="f">女性</option></select></div></div>
    <button class="btn btn-primary" id="calcBtn">評価を見る</button>''',
  result='''      <div class="label">ジャンプ力 評価スコア</div>
      <div class="big"><span id="big">0</span><span class="unit">点</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">滞空時間</div><div class="v accent" id="air">—</div></div>
      <div class="stat"><div class="k">評価</div><div class="v" id="rank">—</div></div>
      <div class="stat"><div class="k">記録</div><div class="v" id="cv">—</div></div></div>''',
  article='''    <h2>ジャンプ力の目安</h2>
    <div class="note"><strong>計算式</strong><br>滞空時間 ＝ 2 × √(2 × 跳躍高 ÷ 9.8)<br>評価は性別ごとの一般的な平均（男性約55cm／女性約40cm）を基準にしています。</div>
    <p>垂直跳びは下半身の瞬発力の指標。ジャンプ系の競技はもちろん、走りや瞬発力にも関わります。スクワットやジャンプトレーニングで伸ばせます。</p>
    <h2>よくある質問</h2>'''+faq([('平均は？','成人男性で約55cm、女性で約40cmが一つの目安です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const cm=Math.max(1,+$('cm').value||1),sex=$('sex').value;const base=sex==='m'?55:40;
    const air=2*Math.sqrt(2*(cm/100)/9.8),score=Math.max(10,Math.min(99,Math.round(cm/base*55)));
    let r;if(score>=75)r='アスリート級🏆';else if(score>=55)r='平均以上';else if(score>=40)r='平均的';else r='これから伸びる';
    $('sub').textContent=`${cm}cm・${sex==='m'?'男性':'女性'}`;$('air').textContent=num(air*1000)+'ms';$('rank').textContent=r;$('cv').textContent=cm+'cm';
    SHARE=`垂直跳び 評価シミュ、私は${cm}cm・スコア${score}点(${r})でした🦘\\n滞空時間${num(air*1000)}ms！あなたは？👇`;show();anim($('big'),0,score,900);}''')

add(id='undou-shukan', cat='スポーツ・運動', emoji='📆',
  title='運動習慣カロリーシミュレーター｜続けると年でどれだけ燃える？｜シミュラボ',
  desc='週の運動回数・1回の時間・種目・体重から、運動習慣で年間・生涯に消費するカロリーと脂肪量を計算する無料シミュレーター。',
  ogtitle='運動習慣カロリー｜続けると年でどれだけ燃える？', ogdesc='週の運動から、年間・生涯の消費カロリーを計算。',
  h1='運動習慣カロリーシミュレーター',
  lead='週◯回の運動を続けると、年でどれだけ燃える？運動の頻度・時間・種目から、年間・生涯の消費カロリーと脂肪量を出します。継続のモチベーションに。',
  inputs='''    <h2>📆 条件を入れる</h2>
    <div class="row"><div class="field"><label>週の運動回数 <span class="hint">（回）</span></label><input type="number" id="freq" value="3" min="0" max="14" inputmode="numeric"></div>
    <div class="field"><label>1回の時間 <span class="hint">（分）</span></label><input type="number" id="min" value="30" min="0" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>種目</label><select id="met"><option value="3.5">ウォーキング</option><option value="7" selected>ジョギング</option><option value="8">水泳</option><option value="6">サイクリング</option><option value="5">筋トレ</option></select></div>
    <div class="field"><label>体重 <span class="hint">（kg）</span></label><input type="number" id="w" value="60" min="20" max="200" inputmode="numeric"></div></div>
    <div class="field"><label>続ける年数 <span class="hint">（年）</span></label><input type="number" id="yr" value="10" min="1" max="60" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">消費カロリーを見る</button>''',
  result='''      <div class="label">年間の消費カロリー</div>
      <div class="big"><span id="big">0</span><span class="unit">kcal</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">年間の脂肪換算</div><div class="v accent" id="fat">—</div></div>
      <div class="stat"><div class="k">続ける年数で</div><div class="v" id="total">—</div></div>
      <div class="stat"><div class="k">1回あたり</div><div class="v" id="per">—</div></div></div>''',
  article='''    <h2>継続は力</h2>
    <div class="note"><strong>計算式</strong><br>1回の消費 ＝ METs × 3.5 × 体重 ÷ 200 × 時間<br>年間 ＝ 1回の消費 × 週の回数 × 52</div>
    <p>1回は小さくても、続けると驚きの量に。運動は消費カロリーだけでなく、筋力・心肺・メンタルにも好影響。「続けられる種目・頻度」を選ぶのが何より大切です。</p>
    <h2>よくある質問</h2>'''+faq([('食事制限と比べると？','運動は維持と健康に強い。食事と組み合わせるのが効果的です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const freq=Math.max(0,+$('freq').value||0),min=Math.max(0,+$('min').value||0),met=+$('met').value||7,w=Math.max(1,+$('w').value||1),yr=Math.max(1,+$('yr').value||1);
    const per=met*3.5*w/200*min,year=per*freq*52,total=year*yr;
    $('sub').textContent=`週${freq}回 × ${min}分 ・ ${sel('met').text}`;$('fat').textContent=num(year/7.2)+'g';$('total').textContent=num(total)+'kcal';$('per').textContent=num(per)+'kcal';
    SHARE=`運動習慣カロリーシミュ、年${num(year)}kcal・脂肪${num(year/7.2)}g燃える計算でした📆\\n継続は力なり！👇`;show();anim($('big'),0,year,900);}''')

# ===== 推し活・エンタメ =====
add(id='oshi-anniv', cat='推し活・エンタメ', emoji='🎂',
  title='推しの誕生日カウントダウン｜次の生誕祭まであと何日？｜シミュラボ',
  desc='推しの誕生日を入れると、次の誕生日（生誕祭）まであと何日かと、お祝い準備の目安を表示するエンタメシミュレーター。',
  ogtitle='推しの誕生日カウントダウン｜あと何日？', ogdesc='推しの誕生日から、次の生誕祭までの日数を表示。',
  h1='推しの誕生日カウントダウン',
  lead='推しの誕生日（生誕祭）まで、あと何日？誕生日を入れると、次のお祝いまでのカウントダウンを表示します。祭壇やプレゼントの準備計画に。',
  inputs='''    <h2>🎂 推しの誕生日を入れる</h2>
    <div class="field"><label>推しの誕生日</label><input type="date" id="d" value="2000-07-07"></div>
    <button class="btn btn-primary" id="calcBtn">カウントダウン</button>''',
  result='''      <div class="label">次の生誕祭まで</div>
      <div class="big"><span id="big">0</span><span class="unit">日</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">次の誕生日</div><div class="v accent" id="next">—</div></div>
      <div class="stat"><div class="k">準備できる週末</div><div class="v" id="week">—</div></div>
      <div class="stat"><div class="k">今日が誕生日なら</div><div class="v" id="today">—</div></div></div>''',
  article='''    <h2>生誕祭を全力で</h2>
    <p>推しの誕生日は、ファンにとって一年の一大イベント。あと何日かが分かれば、祭壇づくり・プレゼント・SNS企画の準備もばっちり。残りの週末の数も表示するので、計画的にお祝いの準備を進められます。</p>
    <h2>よくある質問</h2>'''+faq([('複数推しでも使える？','一人ずつ入れて、それぞれカウントダウンしてください。'),('入力した誕生日は送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const v=$('d').value;if(!v){alert('誕生日を選んでね');return;}
    const b=new Date(v);const T=new Date();T.setHours(0,0,0,0);
    let next=new Date(T.getFullYear(),b.getMonth(),b.getDate());if(next<T)next=new Date(T.getFullYear()+1,b.getMonth(),b.getDate());
    const days=Math.round((next-T)/86400000);
    $('sub').textContent=`${b.getMonth()+1}月${b.getDate()}日生まれ`;$('next').textContent=`${next.getMonth()+1}/${next.getDate()}`;$('week').textContent=Math.floor(days/7)+'回';$('today').textContent=days===0?'おめでとう🎉':'—';
    SHARE=`推しの誕生日カウントダウン、次の生誕祭まであと${days}日でした🎂\\n全力でお祝いするぞ…！👇`;show();anim($('big'),0,days,900);}''')

add(id='cosplay-hiyou', cat='推し活・エンタメ', emoji='🎽',
  title='コスプレ費用シミュレーター｜1キャラ揃えるといくら？｜シミュラボ',
  desc='衣装・ウィッグ・小物・カラコンなどの費用と、年に作る衣装数から、コスプレにかかる費用を試算する無料シミュレーター。',
  ogtitle='コスプレ費用シミュレーター｜1キャラいくら？', ogdesc='衣装・ウィッグ・小物から、コスプレ費用を試算。',
  h1='コスプレ費用シミュレーター',
  lead='1キャラ完成させるのにいくらかかる？衣装・ウィッグ・小物の費用と、年に作る数から、コスプレにかかる費用を出します。沼の深さの可視化に。',
  inputs='''    <h2>🎽 条件を入れる（1キャラ分）</h2>
    <div class="row"><div class="field"><label>衣装 <span class="hint">（円）</span></label><input type="number" id="cos" value="15000" min="0" inputmode="numeric"></div>
    <div class="field"><label>ウィッグ <span class="hint">（円）</span></label><input type="number" id="wig" value="5000" min="0" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>小物・カラコン等 <span class="hint">（円）</span></label><input type="number" id="item" value="8000" min="0" inputmode="numeric"></div>
    <div class="field"><label>年に作るキャラ数</label><input type="number" id="n" value="3" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">費用を見る</button>''',
  result='''      <div class="label">1キャラあたりの費用</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">年間の費用</div><div class="v accent" id="year">—</div></div>
      <div class="stat"><div class="k">撮影・遠征は別</div><div class="v" id="note2">—</div></div>
      <div class="stat"><div class="k">年のキャラ数</div><div class="v" id="nv">—</div></div></div>''',
  article='''    <h2>計算方法</h2>
    <div class="note"><strong>計算式</strong><br>1キャラ ＝ 衣装 ＋ ウィッグ ＋ 小物<br>年間 ＝ 1キャラ × 年に作る数</div>
    <p>衣装は購入か自作かで大きく変わります。ウィッグや小物は使い回せることも。さらに撮影スタジオ・イベント参加費・交通費もかかるので、トータルで見ると立派な趣味投資。好きを楽しんで。</p>
    <h2>よくある質問</h2>'''+faq([('自作なら安い？','布・型紙代で抑えられますが、時間と技術が必要。既製品とのバランスで。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const cos=Math.max(0,+$('cos').value||0),wig=Math.max(0,+$('wig').value||0),item=Math.max(0,+$('item').value||0),n=Math.max(0,+$('n').value||0);
    const per=cos+wig+item,year=per*n;
    $('sub').textContent=`衣装${num(cos)}＋ウィッグ${num(wig)}＋小物${num(item)}`;$('year').textContent=yen(year);$('note2').textContent='+α';$('nv').textContent=n+'体';
    SHARE=`コスプレ費用シミュ、1キャラ${yen(per)}・年で${yen(year)}でした🎽\\n好きへの投資！👇`;show();anim($('big'),0,per,900);}''')

add(id='hakooshi', cat='推し活・エンタメ', emoji='📦',
  title='箱推し費用シミュレーター｜グループ全員推すといくら？｜シミュラボ',
  desc='推しメンバーの人数と1人あたりの年間費用から、箱推し（グループ全員推し）の年間・生涯費用と単推しとの差を試算するエンタメシミュレーター。',
  ogtitle='箱推し費用シミュレーター｜全員推すといくら？', ogdesc='推しの人数と1人あたり費用から、箱推しの費用を試算。',
  h1='箱推し費用シミュレーター',
  lead='メンバー全員推す「箱推し」、お財布事情は？推しの人数と1人あたりの年間費用から、箱推しの費用と単推しとの差を出します（愛は無限、お金は有限）。',
  inputs='''    <h2>📦 条件を入れる</h2>
    <div class="row"><div class="field"><label>推しメンバーの人数</label><input type="number" id="n" value="5" min="1" max="100" inputmode="numeric"></div>
    <div class="field"><label>1人あたり年間費用 <span class="hint">（円）</span></label><input type="number" id="per" value="50000" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">箱推し費用を見る</button>''',
  result='''      <div class="label">箱推しの年間費用</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1ヶ月あたり</div><div class="v" id="mo">—</div></div>
      <div class="stat"><div class="k">単推しとの差</div><div class="v accent" id="diff">—</div></div>
      <div class="stat"><div class="k">10年で</div><div class="v" id="y10">—</div></div></div>''',
  article='''    <h2>箱推しは愛が深い</h2>
    <div class="note"><strong>計算式</strong><br>年間費用 ＝ 推しの人数 × 1人あたりの年間費用</div>
    <p>全員を応援したい気持ち、素敵です。ただ人数分かかるので、グッズは厳選する・現場は絞る、などメリハリも大切。無理なく長く応援できるペースを見つけてください。</p>
    <h2>よくある質問</h2>'''+faq([('単推しより高い？','人数分かかるので高くなりがち。その分、箱の魅力を丸ごと楽しめます。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const n=Math.max(1,+$('n').value||1),per=Math.max(0,+$('per').value||0);const year=n*per,diff=(n-1)*per;
    $('sub').textContent=`${n}人 × 年${num(per)}円`;$('mo').textContent=yen(year/12);$('diff').textContent='+'+yen(diff);$('y10').textContent=yen(year*10);
    SHARE=`箱推し費用シミュ、${n}人箱推しで年${yen(year)}でした📦\\n愛は無限、お財布は有限…！👇`;show();anim($('big'),0,year,900);}''')

# ===== メンタル・自己分析 =====
add(id='motivation-type', cat='メンタル・自己分析', emoji='🔥',
  title='モチベーションタイプ診断｜あなたのやる気の源は？｜シミュラボ',
  desc='何にやる気を感じるかの質問から、あなたのモチベーションの源泉タイプ（達成・承認・貢献・探究・自由）を診断する無料の自己分析。',
  ogtitle='モチベーションタイプ診断｜やる気の源は？', ogdesc='質問からあなたのモチベーションの源泉を診断。',
  h1='モチベーションタイプ診断',
  lead='何があなたを動かす？やる気のスイッチは人によって違います。5つの質問から、あなたのモチベーションの源泉タイプを診断します。仕事や勉強の続け方のヒントに。',
  inputs='''    <h2>🔥 やる気が出るのは？</h2>
'''+q('いちばん嬉しいのは','q1',[('tassei','目標を達成したとき'),('shounin','人に認められたとき'),('kouken','人の役に立てたとき')])
   +q('頑張れるのは','q2',[('tassei','記録や成果が見えるとき'),('jiyuu','自分のやり方でできるとき'),('tankyu','新しいことを学べるとき')])
   +q('落ち込むのは','q3',[('shounin','評価されないとき'),('kouken','誰の役にも立てないとき'),('jiyuu','自由がきかないとき')])
   +q('理想の働き方は','q4',[('jiyuu','裁量が大きい'),('tassei','成果で評価される'),('tankyu','学びが多い')])
   +q('ごほうびは','q5',[('shounin','称賛・感謝の言葉'),('tassei','達成感そのもの'),('kouken','誰かの笑顔')])
   +'    <button class="btn btn-primary" id="calcBtn">タイプを診断する</button>',
  result='''      <div class="label">あなたのやる気の源は</div>
      <div class="big" style="font-size:36px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="adv" style="text-align:left;margin-top:18px;">—</div>''',
  article='''    <h2>やる気のスイッチを知る</h2>
    <p>自分のモチベーションの源泉を知ると、続かない・やる気が出ない理由が分かります。どのタイプも素晴らしい原動力。自分のスイッチに合った環境・目標設定をすると、力を発揮しやすくなります。</p>
    <h2>よくある質問</h2>'''+faq([('複数あてはまる','人は複数の源泉を持ちます。最も多い傾向を「核」として活かしてください。'),('入力内容は送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]),
  js='''  function calc(){const c={tassei:0,shounin:0,kouken:0,tankyu:0,jiyuu:0};
    for(const id of ['q1','q2','q3','q4','q5'])c[$(id).value]++;
    const top=Object.keys(c).reduce((a,b)=>c[a]>=c[b]?a:b);
    const M={tassei:['達成タイプ','目標と成果が原動力。数値化した目標を立てると燃えるタイプ。'],shounin:['承認タイプ','認められることが力に。成果を発信し、評価される環境で輝きます。'],kouken:['貢献タイプ','人の役に立つことが喜び。「ありがとう」が最高のごほうび。'],tankyu:['探究タイプ','学びと成長が原動力。新しい知識・スキルが燃料になります。'],jiyuu:['自由タイプ','裁量と自分らしさが大事。任せてもらえると力を発揮します。']};
    const t=M[top];$('big').textContent=t[0];$('sub').textContent='5つの質問から導いたあなたの源泉';$('adv').textContent='🔥 '+t[1];
    SHARE=`モチベーションタイプ診断、私は「${t[0]}」でした🔥\\n${t[1]}\\nあなたは？👇`;show();}''')

add(id='kansha-do', cat='メンタル・自己分析', emoji='🙏',
  title='幸福度・感謝度チェック｜小さな幸せに気づけてる？｜シミュラボ',
  desc='日々の感謝や幸せの感じ方についての6項目から、今の幸福度・感謝度の目安をチェックし、幸福度を上げるヒントを提案する無料の自己分析。',
  ogtitle='幸福度・感謝度チェック｜小さな幸せに気づけてる？', ogdesc='6項目で幸福度・感謝度をチェック＋上げるヒント。',
  h1='幸福度・感謝度チェック',
  lead='幸せは「気づく力」とも言われます。日々の感謝や幸せの感じ方についての6つの質問から、今の幸福度・感謝度の目安をチェックします。',
  inputs='''    <h2>🙏 最近のあなたは？</h2>
'''+q('小さな幸せに','q1',[('4','よく気づける'),('2','時々'),('0','あまり気づけない')])
   +q('「ありがとう」を','q2',[('4','よく口にする'),('2','時々'),('0','あまり言わない')])
   +q('今の生活に','q3',[('4','満足している'),('2','まあまあ'),('0','不満が多い')])
   +q('夜寝る前の気分は','q4',[('4','穏やか'),('2','普通'),('0','モヤモヤ')])
   +q('人と比べて','q5',[('4','自分の幸せを感じる'),('2','どちらとも'),('0','落ち込む')])
   +q('好きなこと・人が','q6',[('4','たくさんある'),('2','少しある'),('0','思いつかない')])
   +'    <button class="btn btn-primary" id="calcBtn">幸福度をチェック</button>',
  result='''      <div class="label">あなたの幸福度・感謝度</div>
      <div class="big"><span id="big">0</span><span class="unit">点</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="adv" style="text-align:left;margin-top:18px;">—</div>''',
  article='''    <h2>幸福度は育てられる</h2>
    <p>幸せは「すでにあるもの」に気づく力でもあります。寝る前に良かったことを3つ思い出す（スリー・グッド・シングス）、感謝を言葉にする——こうした小さな習慣で幸福度は高められると言われます。</p>
    <div class="note">💡 セルフチェックの目安です。気分の落ち込みが続くときは、無理せず専門家や相談窓口を頼ってください。</div>
    <h2>よくある質問</h2>'''+faq([('低かったら？','まずは「良かったこと3つ」を寝る前に書く習慣から。少しずつ変わります。'),('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]),
  js='''  function calc(){let s=0;for(const id of ['q1','q2','q3','q4','q5','q6'])s+=(+$(id).value||0);const pct=Math.round(s/24*100);
    let a;if(pct>=70)a='幸せ感度が高い！小さな喜びに気づける素敵な心です。その習慣を大切に🙏';else if(pct>=40)a='ほどよいバランス。寝る前に「良かったこと3つ」を思い出すと、もっと上がります。';else a='今は少しお疲れかも。完璧を求めず、身近な小さな幸せ探しから始めてみて。';
    $('sub').textContent='6項目のセルフチェック結果（100点満点）';$('adv').textContent='🙏 '+a;
    SHARE=`幸福度・感謝度チェック、私は${pct}点でした🙏\\n小さな幸せ、大事にしよ。あなたは？👇`;show();anim($('big'),0,pct,900);}''')

add(id='shuuchu-type', cat='メンタル・自己分析', emoji='🎯',
  title='集中タイプ診断｜あなたが集中しやすいスタイルは？｜シミュラボ',
  desc='集中の仕方についての5つの質問から、あなたの集中タイプ（短距離型・長距離型・環境依存型など）を診断する無料の自己分析。',
  ogtitle='集中タイプ診断｜集中しやすいスタイルは？', ogdesc='5問であなたの集中タイプを診断＋集中のコツ。',
  h1='集中タイプ診断',
  lead='集中の仕方は人それぞれ。自分のタイプを知ると、勉強や仕事の効率がぐっと上がります。5つの質問から、あなたの集中タイプを診断します。',
  inputs='''    <h2>🎯 集中について教えて</h2>
'''+q('集中が続くのは','q1',[('long','長時間でも平気'),('short','短時間で区切るほうがいい')])
   +q('はかどる場所は','q2',[('env','静かな決まった場所'),('any','どこでも割と平気')])
   +q('作業前は','q3',[('plan','手順を決めてから'),('go','とりあえず始める')])
   +q('音は','q4',[('env','無音/一定の音が良い'),('any','あまり気にしない')])
   +q('やる気は','q5',[('go','始めると出てくる'),('plan','準備して高めてから')])
   +'    <button class="btn btn-primary" id="calcBtn">集中タイプを診断する</button>',
  result='''      <div class="label">あなたの集中タイプ</div>
      <div class="big" style="font-size:34px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="adv" style="text-align:left;margin-top:18px;">—</div>''',
  article='''    <h2>集中のクセを味方に</h2>
    <p>長時間集中できる人、短く区切るほうが良い人、環境で大きく変わる人——どれが良い悪いではなく「自分に合うやり方」を知るのが大事。タイプに合わせて環境や時間配分を整えると、無理なく集中できます。</p>
    <h2>よくある質問</h2>'''+faq([('集中力がない？','タイプが合っていないだけかも。短時間型ならポモドーロが効きます。'),('入力内容は送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')]),
  js='''  function calc(){let long=0,env=0,plan=0;
    if($('q1').value==='long')long++;if($('q2').value==='env')env++;if($('q3').value==='plan')plan++;if($('q4').value==='env')env++;if($('q5').value==='plan')plan++;
    let t,d;
    if(long>=1&&env>=1){t='じっくり没頭型';d='静かな環境で長時間集中できるタイプ。まとまった時間と場所を確保すると最大の力を発揮します。';}
    else if(long<1){t='短距離集中型';d='短く区切るほうが冴えるタイプ。ポモドーロ(25分集中)で小刻みに進めると◎。';}
    else if(env<1){t='どこでも集中型';d='場所を選ばず集中できる器用なタイプ。スキマ時間の活用が得意。';}
    else {t='準備型集中タイプ';d='段取りを整えてから力を出すタイプ。前日に手順を決めておくとスムーズです。';}
    $('big').textContent=t;$('sub').textContent='5つの質問から導いたあなたの集中スタイル';$('adv').textContent='🎯 '+d;
    SHARE=`集中タイプ診断、私は「${t}」でした🎯\\n${d}\\nあなたは？👇`;show();}''')

if __name__=='__main__':
    write_all(SIMS)
    print(f'batch4 done. {len(SIMS)} sims.')
