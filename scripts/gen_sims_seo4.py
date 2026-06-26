# -*- coding: utf-8 -*-
"""シミュラボ：SEO強化の新規3本（厄年早見/失業保険/住宅ローン借入可能額）。
   リッチ本文＋専用アニメ。gen_sims11のTPL(write_all)を再利用。CTAなしカテゴリに投入。"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims11 import faq, write_all

MANNER = '冠婚葬祭・贈り物'; WORK = '仕事・働き方'; FIN = 'マネー・保険・不動産'
SIMS = []
def add(**k): SIMS.append(k)

# ============================================================
# 1) 厄年早見（男女・前厄/本厄/後厄・数え年）
# ============================================================
add(id='yakudoshi', cat=MANNER, emoji='⛩️',
  title='厄年早見｜生年月日から前厄・本厄・後厄・大厄を自動判定｜シミュラボ',
  desc='生年月日と性別を入れるだけで、今年の数え年と前厄・本厄・後厄・大厄かどうかを自動判定。男女別の厄年早見表つきの無料ツール。',
  ogtitle='厄年早見｜あなたは今年、厄年？', ogdesc='生年月日から数え年と前厄・本厄・後厄を自動判定（男女別）。',
  h1='厄年 早見ツール',
  lead='生年月日と性別を入れるだけで、今年の数え年と「前厄・本厄・後厄・大厄」かどうかを自動で判定します。次の厄年がいつ来るかも分かります。',
  inputs='''    <h2>⛩️ 生年月日を入れる</h2>
    <div class="row"><div class="field"><label>生年月日</label><input type="date" id="bd" value="1992-08-20"></div>
    <div class="field"><label>性別</label><select id="sex"><option value="m">男性</option><option value="f" selected>女性</option></select></div></div>
    <button class="btn btn-primary" id="calcBtn">厄年か調べる</button>''',
  result='''      <div class="label">今年の数え年</div>
      <div class="big"><span id="big">0</span><span class="unit">歳</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">今年は</div><div class="v accent" id="state">—</div></div>
      <div class="stat"><div class="k">次の厄年</div><div class="v" id="next">—</div></div>
      <div class="stat"><div class="k">満年齢</div><div class="v" id="manv">—</div></div></div>
      <div class="yaku-steps" id="yakuSteps"></div>
      <div class="anim-cap">前厄・本厄・後厄の3年間が「厄」とされます</div>''',
  article='''    <div class="note" style="border-left:4px solid var(--teal)"><strong>結論</strong>：厄年は<b>数え年</b>で数えます。本厄の前後1年（前厄・後厄）も含めた3年間が「厄」の期間。男性の42歳・女性の33歳は<b>大厄</b>とされます。</div>
    <h2>厄年とは</h2>
    <p>厄年は、人生の節目で災いが起こりやすいとされる年齢で、平安時代から続く風習です。数え年で数え、本厄の前後（前厄・後厄）を合わせた3年間を慎重に過ごすとされます。とくに男性42歳・女性33歳は「大厄」と呼ばれ、最も注意する年とされています（科学的根拠ではなく伝統的な考え方です）。</p>
    <h2>男女別・厄年早見表（数え年）</h2>
    <table class="seo-table">
      <tr><th>区分</th><th>男性</th><th>女性</th></tr>
      <tr><td>前厄</td><td>24・41・60</td><td>18・32・36・60</td></tr>
      <tr><td>本厄</td><td>25・<b>42(大厄)</b>・61</td><td>19・<b>33(大厄)</b>・37・61</td></tr>
      <tr><td>後厄</td><td>26・43・62</td><td>20・34・38・62</td></tr>
    </table>
    <div class="note"><strong>数え年の出し方</strong><br>数え年 ＝ 今年 − 生まれ年 ＋ 1<br>（生まれた時を1歳とし、元日ごとに1つ増える数え方）</div>
    <h2>厄払いはいつ行く？</h2>
    <p>厄払い（厄除け）は、年明けから節分（2月3日ごろ）までに行うのが一般的とされますが、一年を通して受け付けている神社・お寺が多くあります。前厄から後厄まで毎年行く人もいます。</p>
    <h2>よくある質問</h2>'''+faq([
      ('厄年は満年齢ですか？','いいえ、数え年で数えるのが一般的です。本ツールも数え年で判定しています。'),
      ('大厄とは？','男性42歳・女性33歳の本厄をとくに「大厄」と呼びます。語呂合わせ（42＝死に、33＝散々）が由来とされます。'),
      ('厄払いに行かないとダメ？','風習であり義務ではありません。気持ちの区切りとして行く人が多いです。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])
    +'''<h2>参考</h2><ul class="seo-refs"><li>神社本庁「厄年・厄除け」</li><li>各神社・寺院の厄年の数え方</li></ul>''',
  js='''  const HON={m:[25,42,61],f:[19,33,37,61]}, TAI={m:42,f:33};
  function calc(){
    const v=$('bd').value; if(!v){return;}
    const sex=$('sex').value; const bd=new Date(v+'T00:00:00'); const now=new Date(); now.setHours(0,0,0,0);
    if(bd>now){ $('sub').textContent='生年月日を確認してください'; show(); return; }
    const kazoe=now.getFullYear()-bd.getFullYear()+1;
    let man=now.getFullYear()-bd.getFullYear(); const had=(now.getMonth()>bd.getMonth())||(now.getMonth()===bd.getMonth()&&now.getDate()>=bd.getDate()); if(!had)man--;
    const hons=HON[sex];
    let cur=null;
    for(const h of hons){ if(kazoe===h-1)cur={t:'前厄',h:h}; else if(kazoe===h)cur={t:(h===TAI[sex]?'本厄（大厄）':'本厄'),h:h}; else if(kazoe===h+1)cur={t:'後厄',h:h}; }
    const all=[]; hons.forEach(h=>{all.push(h-1);all.push(h);all.push(h+1);});
    const future=all.filter(a=>a>kazoe).sort((a,b)=>a-b); const nextAge=future.length?future[0]:null;
    let relH=cur?cur.h:(hons.find(h=>h+1>=kazoe)||hons[hons.length-1]);
    const steps=[[relH-1,'前厄'],[relH,(relH===TAI[sex]?'本厄(大厄)':'本厄')],[relH+1,'後厄']];
    $('yakuSteps').innerHTML=steps.map(s=>`<div class="yaku-step${s[0]===kazoe?' on':''}"><div class="lab">${s[1]}</div><div class="age">数え${s[0]}歳</div></div>`).join('');
    $('state').textContent=cur?cur.t:'厄年ではありません';
    $('next').textContent=nextAge?`数え${nextAge}歳（あと${nextAge-kazoe}年）`:'なし';
    $('manv').textContent=man+'歳';
    $('sub').textContent=`${bd.getFullYear()}年${bd.getMonth()+1}月${bd.getDate()}日・${sex==='m'?'男性':'女性'}`;
    show(); anim($('big'),0,kazoe,800);
    SHARE=cur?`厄年早見、私は今年「${cur.t}」（数え${kazoe}歳）でした⛩️ 厄払い行こうかな…`:`厄年早見、今年は厄年じゃないみたい。次は数え${nextAge}歳⛩️`;
  }''')

# ============================================================
# 2) 失業保険（基本手当）いくらもらえる
# ============================================================
add(id='shitsugyo-hoken', cat=WORK, emoji='🧾',
  title='失業保険 計算｜基本手当はいくら・何日もらえる？（目安）｜シミュラボ',
  desc='退職前の月給・年齢・雇用保険の加入年数・退職理由から、失業保険（基本手当）の日額・給付日数・受け取れる総額の目安を計算する無料ツール。',
  ogtitle='失業保険 計算｜基本手当はいくらもらえる？', ogdesc='月給・年齢・加入年数・退職理由から基本手当の総額の目安を計算。',
  h1='失業保険（基本手当）計算ツール',
  lead='会社を辞めたら失業保険（基本手当）はいくら・何日もらえる？退職前の月給・年齢・加入年数・退職理由から、受け取れる総額の目安を計算します。',
  inputs='''    <h2>🧾 条件を入れる</h2>
    <div class="row"><div class="field"><label>退職前6ヶ月の月給 <span class="hint">（額面・万円）</span></label><input type="number" id="g" value="30" min="0" inputmode="numeric"></div>
    <div class="field"><label>年齢</label><select id="age"><option value="0">〜29歳</option><option value="1" selected>30〜44歳</option><option value="2">45〜59歳</option><option value="3">60〜64歳</option></select></div></div>
    <div class="row"><div class="field"><label>雇用保険の加入年数</label><select id="yr"><option value="0">1年未満</option><option value="1">1〜4年</option><option value="2" selected>5〜9年</option><option value="3">10〜19年</option><option value="4">20年以上</option></select></div>
    <div class="field"><label>退職理由</label><select id="reason"><option value="self" selected>自己都合</option><option value="comp">会社都合・特定理由</option></select></div></div>
    <button class="btn btn-primary" id="calcBtn">もらえる額を見る</button>''',
  result='''      <div class="label">受け取れる総額（目安）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">基本手当 日額</div><div class="v accent" id="dayAmt">—</div></div>
      <div class="stat"><div class="k">給付日数</div><div class="v" id="days">—</div></div>
      <div class="stat"><div class="k">給付率</div><div class="v" id="rate">—</div></div></div>
      <div class="anim-bar" id="bar3wrap"><span id="bar3"></span><b id="bar3l"></b></div>
      <div class="anim-cap">給付日数（最大330日のうち）</div>''',
  article='''    <div class="note" style="border-left:4px solid var(--teal)"><strong>結論</strong>：失業保険（基本手当）は <b>基本手当日額 × 給付日数</b>。日額は退職前の賃金の約<b>50〜80%</b>、給付日数は年齢・加入年数・退職理由で決まります。</div>
    <h2>失業保険（基本手当）のしくみ</h2>
    <p>会社を退職して求職活動をする間、雇用保険から支給されるのが「基本手当（いわゆる失業保険）」です。退職前6ヶ月の給与から「賃金日額」を求め、その50〜80%が1日あたりの基本手当日額になります。賃金が低い人ほど給付率は高くなります。</p>
    <div class="note"><strong>計算の流れ</strong><br>賃金日額 ＝ 退職前6ヶ月の給与総額 ÷ 180<br>基本手当日額 ＝ 賃金日額 × 給付率(50〜80%)<br>総額 ＝ 基本手当日額 × 給付日数</div>
    <h2>給付日数のめやす</h2>
    <table class="seo-table">
      <tr><th>退職理由</th><th>加入1〜4年</th><th>5〜9年</th><th>10〜19年</th><th>20年〜</th></tr>
      <tr><td>自己都合</td><td>90日</td><td>90日</td><td>120日</td><td>150日</td></tr>
      <tr><td>会社都合（30〜44歳）</td><td>120日</td><td>180日</td><td>240日</td><td>270日</td></tr>
      <tr><td>会社都合（45〜59歳）</td><td>180日</td><td>240日</td><td>270日</td><td>330日</td></tr>
    </table>
    <p>自己都合退職には原則「2〜3ヶ月の給付制限」があり、すぐには受け取れません。会社都合（倒産・解雇など）や特定理由離職者は給付制限がなく、給付日数も手厚くなります。受給には「ハローワークでの求職申込」と一定の被保険者期間が必要です。<b>本ツールは目安です</b>（実際の額は離職票の賃金額で決まります）。</p>
    <h2>よくある質問</h2>'''+faq([
      ('いつから振り込まれる？','会社都合は申込後すぐ（待機7日後）、自己都合は給付制限期間（2〜3ヶ月）の後に始まります。'),
      ('上限額はある？','基本手当日額には年齢ごとの上限があります（おおむね7,000〜8,500円前後）。本ツールも上限を反映しています。'),
      ('もらいながらバイトできる？','一定の範囲なら可能ですが、収入・時間によって減額や先送りになります。ハローワークへの申告が必要です。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])
    +'''<h2>参考</h2><ul class="seo-refs"><li>厚生労働省・ハローワーク「基本手当について」</li><li>雇用保険の給付日数・給付率</li></ul>''',
  js='''  function gdays(reason,age,y){
    if(reason==='self'){ return [90,90,90,120,150][y]; }
    const T=[[90,90,120,180,180],[90,120,180,240,270],[90,180,240,270,330],[90,150,180,210,240]];
    return T[age][y];
  }
  function calc(){
    const g=Math.max(0,+$('g').value||0)*10000, age=+$('age').value||0, y=+$('yr').value||0, reason=$('reason').value;
    const w=g*6/180; // 賃金日額(月給×6ヶ月÷180)
    let r; if(w<=5030)r=0.8; else if(w<=12330)r=0.5+(12330-w)/(12330-5030)*0.3; else r=0.5;
    let dayAmt=w*r; const cap=[6945,7715,8490,8490][age]; dayAmt=Math.min(dayAmt,cap);
    const d=gdays(reason,age,y), total=dayAmt*d;
    $('sub').textContent=`月給${num(g/10000)}万円・${['〜29','30〜44','45〜59','60〜64'][age]}歳・加入${['<1','1〜4','5〜9','10〜19','20〜'][y]}年・${reason==='self'?'自己都合':'会社都合'}`;
    $('dayAmt').textContent=yen(dayAmt); $('days').textContent=d+'日'; $('rate').textContent=Math.round(r*100)+'%';
    const pct=Math.round(d/330*100); $('bar3').style.width='0%'; setTimeout(()=>{$('bar3').style.width=pct+'%';},40); $('bar3l').textContent=d+'日';
    show(); anim($('big'),0,total,900);
    SHARE=`失業保険シミュ、基本手当は日額${yen(dayAmt)}×${d}日＝総額 約${yen(total)}の計算でした🧾（目安）`;
  }''')

# ============================================================
# 3) 住宅ローン 借入可能額
# ============================================================
add(id='kariire-kanou', cat=FIN, emoji='🏠',
  title='住宅ローン 借入可能額シミュレーター｜年収からいくら借りられる？｜シミュラボ',
  desc='年収・返済負担率・審査金利・返済期間から、住宅ローンの借入可能額・月々の返済額・年収倍率の目安を計算する無料シミュレーター。',
  ogtitle='住宅ローン 借入可能額｜年収からいくら借りられる？', ogdesc='年収・返済負担率・審査金利から借入可能額と年収倍率を計算。',
  h1='住宅ローン 借入可能額シミュレーター',
  lead='年収からいくらまで住宅ローンを組める？年収・返済負担率・審査金利・返済期間から、借入可能額・月々の返済額・年収倍率の目安を計算します。',
  inputs='''    <h2>🏠 条件を入れる</h2>
    <div class="row"><div class="field"><label>年収（額面） <span class="hint">（万円）</span></label><input type="number" id="y" value="500" min="0" inputmode="numeric"></div>
    <div class="field"><label>返済負担率 <span class="hint">（%）</span></label><input type="number" id="burden" value="35" min="10" max="50" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>審査金利 <span class="hint">（%・年）</span></label><input type="number" id="rate" value="3.5" min="0" max="10" step="0.1" inputmode="decimal"></div>
    <div class="field"><label>返済期間 <span class="hint">（年）</span></label><input type="number" id="yrs" value="35" min="1" max="50" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">借入可能額を見る</button>''',
  result='''      <div class="ptag-stage seo-anim" id="hstage"><div class="pop-emoji" id="house">🏠</div></div>
      <div class="label">借入可能額（目安）</div>
      <div class="big"><span id="big">0</span><span class="unit">万円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">月々の返済目安</div><div class="v accent" id="monthly">—</div></div>
      <div class="stat"><div class="k">年収倍率</div><div class="v" id="bai">—</div></div>
      <div class="stat"><div class="k">年間返済可能額</div><div class="v" id="annual">—</div></div></div>
      <div class="anim-bar" id="bWrap"><span id="bBar"></span><b id="bLab"></b></div>
      <div class="anim-cap">年収倍率（無理のない目安は5〜7倍前後）</div>''',
  article='''    <div class="note" style="border-left:4px solid var(--teal)"><strong>結論</strong>：借入可能額は <b>年収 × 返済負担率 ÷ 年間返済係数</b> で決まります。審査金利が高いほど、借りられる額は小さくなります。</div>
    <h2>借入可能額の決まり方</h2>
    <p>金融機関は「年収に対する年間返済額の割合（返済負担率）」の上限を決めており、その範囲内で借りられる額が決まります。たとえば年収500万円・返済負担率35%なら、年間の返済可能額は175万円。これを返済期間と「審査金利」で割り戻すと、借入可能額が求まります。</p>
    <div class="note"><strong>計算式（元利均等）</strong><br>年間返済可能額 ＝ 年収 × 返済負担率<br>借入可能額 ＝ 月々の返済可能額 ÷ ｛r(1+r)ⁿ /((1+r)ⁿ−1)｝<br>（r＝審査金利/12、n＝返済回数）</div>
    <h2>返済負担率の目安</h2>
    <table class="seo-table">
      <tr><th>年収</th><th>返済負担率の上限の目安</th></tr>
      <tr><td>〜400万円未満</td><td>30%</td></tr>
      <tr><td>400万円以上</td><td>35%</td></tr>
    </table>
    <p>注意したいのは、<b>審査金利と実際の適用金利は違う</b>こと。審査では金利上昇に備えて3〜4%程度の高めの「審査金利」で計算されることが多く、実際に借りられる額は変わります。また、自動車ローンやカードのリボなど他の借入があると、そのぶん借入可能額は減ります。</p>
    <h2>「借りられる額」と「返せる額」は別</h2>
    <p>借入可能額はあくまで上限です。無理のない返済額は「手取りの20〜25%以内」が目安とされ、年収倍率では5〜7倍前後が安心ラインと言われます。教育費や老後資金とのバランスで、上限いっぱいではなく余裕を持った金額にするのがおすすめです。</p>
    <h2>よくある質問</h2>'''+faq([
      ('年収倍率って何倍が普通？','フラット35の利用者では年収の6〜7倍程度が中心ですが、無理のない目安は5〜7倍前後とされています。'),
      ('審査金利は何%で計算する？','金融機関により異なりますが、3〜4%程度で審査することが多いです。本ツールは初期値3.5%です。'),
      ('ペアローンなら増える？','夫婦の年収を合算すれば借入可能額は増えますが、どちらかが働けなくなるリスクも考慮しましょう。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])
    +'''<h2>参考</h2><ul class="seo-refs"><li>住宅金融支援機構「フラット35」返済負担率</li><li>元利均等返済の計算方法</li></ul>''',
  js='''  function calc(){
    const y=Math.max(0,+$('y').value||0)*10000, burden=Math.max(0,Math.min(100,+$('burden').value||35))/100, ri=Math.max(0,+$('rate').value||0)/100/12, n=Math.max(1,+$('yrs').value||35)*12;
    const annual=y*burden, monthly=annual/12;
    let P; if(ri<=0){P=monthly*n;} else { const f=ri*Math.pow(1+ri,n)/(Math.pow(1+ri,n)-1); P=monthly/f; }
    const bai=y>0?P/y:0;
    $('sub').textContent=`年収${num(y/10000)}万円・負担率${Math.round(burden*100)}%・審査金利${$('rate').value}%・${$('yrs').value}年`;
    $('monthly').textContent=yen(monthly); $('bai').textContent=bai.toFixed(1)+'倍'; $('annual').textContent=yen(annual);
    const pct=Math.max(0,Math.min(100,bai/10*100)); $('bBar').style.width='0%'; setTimeout(()=>{$('bBar').style.width=pct+'%';},40); $('bLab').textContent=bai.toFixed(1)+'倍';
    const h=$('house'); h.classList.remove('on'); void h.offsetWidth; h.classList.add('on');
    show(); anim($('big'),0,P/10000,900);
    SHARE=`住宅ローン借入可能額シミュ、年収${num(y/10000)}万円なら 約${num(P/10000)}万円（年収の${bai.toFixed(1)}倍）まで借りられる計算でした🏠`;
  }''')

if __name__=='__main__':
    write_all(SIMS)
    print(f'seo4 done. {len(SIMS)} sims.')
