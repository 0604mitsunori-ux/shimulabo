# -*- coding: utf-8 -*-
"""シミュラボ：SEO強化の新規3本（年齢計算/出産予定日/割引計算機）。
   リッチな本文＋専用アニメーション付き。gen_sims11のTPL(write_all)を再利用。"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims11 import faq, write_all

LIFE = '人生・自分ごと'; KIDS = '子ども・育児'; MONEY = 'お金・時間'
SIMS = []
def add(**k): SIMS.append(k)

# ============================================================
# 1) 年齢計算（満年齢・数え年・干支・生まれてからの日数）
# ============================================================
add(id='nenrei-keisan', cat=LIFE, emoji='🎂',
  title='年齢計算｜満年齢・数え年・干支・生まれてからの日数を計算｜シミュラボ',
  desc='生年月日を入れるだけで、満年齢・数え年・干支・生まれてからの日数・次の誕生日までを一発計算する無料ツール。早見表つき。',
  ogtitle='年齢計算｜満年齢・数え年・干支・生きた日数', ogdesc='生年月日から満年齢・数え年・干支・生まれてからの日数を計算。',
  h1='年齢計算ツール',
  lead='生年月日を入れるだけで、満年齢・数え年・干支、そして「生まれてから今日まで何日生きたか」を一発で計算します。次の誕生日までの日数も分かります。',
  inputs='''    <h2>🎂 生年月日を入れる</h2>
    <div class="field"><label>生年月日</label><input type="date" id="bd" value="1995-05-15"></div>
    <button class="btn btn-primary" id="calcBtn">年齢を計算する</button>''',
  result='''      <div class="label">生まれてから今日まで</div>
      <div class="big"><span id="big">0</span><span class="unit">日</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">満年齢</div><div class="v accent" id="man">—</div></div>
      <div class="stat"><div class="k">数え年</div><div class="v" id="kazoe">—</div></div>
      <div class="stat"><div class="k">干支</div><div class="v" id="eto">—</div></div></div>
      <div class="anim-bar" id="lifeWrap"><span id="lifebar"></span><b id="lifepct">0%</b></div>
      <div class="anim-cap">人生100年のうち、いまここ（次の誕生日まで <span id="next">—</span>）</div>''',
  article='''    <div class="note" style="border-left:4px solid var(--teal)"><strong>結論</strong>：満年齢は「誕生日が来た回数」。日本の法律上は<b>誕生日の前日が終わる瞬間</b>に1歳増えます。数え年は生まれた時を1歳とし、正月ごとに1つ増えます。</div>
    <h2>満年齢と数え年の違い</h2>
    <p>ふだん私たちが使う年齢は「満年齢」で、誕生日を迎えるたびに1歳ずつ増えます。一方「数え年」は、生まれた時点を1歳とし、その後は元日（1月1日）を迎えるたびに1歳加える数え方です。七五三・厄年・長寿祝いなどの伝統行事では、いまも数え年が使われることがあります。</p>
    <div class="note"><strong>計算式</strong><br>満年齢 ＝ 今年 − 生まれ年 −（今年の誕生日がまだなら1）<br>数え年 ＝ 今年 − 生まれ年 ＋ 1<br>生きた日数 ＝ 今日 − 生年月日（日数）</div>
    <h2>干支（十二支）の早見</h2>
    <table class="seo-table">
      <tr><th>干支</th><th>主な生まれ年（西暦）</th></tr>
      <tr><td>子（ね・🐭）</td><td>1984 / 1996 / 2008 / 2020</td></tr>
      <tr><td>丑（うし・🐮）</td><td>1985 / 1997 / 2009 / 2021</td></tr>
      <tr><td>寅（とら・🐯）</td><td>1986 / 1998 / 2010 / 2022</td></tr>
      <tr><td>卯（う・🐰）</td><td>1987 / 1999 / 2011 / 2023</td></tr>
      <tr><td>辰（たつ・🐲）</td><td>1988 / 2000 / 2012 / 2024</td></tr>
      <tr><td>巳（み・🐍）</td><td>1989 / 2001 / 2013 / 2025</td></tr>
      <tr><td>午（うま・🐴）</td><td>1990 / 2002 / 2014 / 2026</td></tr>
      <tr><td>未（ひつじ・🐑）</td><td>1991 / 2003 / 2015 / 2027</td></tr>
      <tr><td>申（さる・🐵）</td><td>1992 / 2004 / 2016 / 2028</td></tr>
      <tr><td>酉（とり・🐔）</td><td>1993 / 2005 / 2017 / 2029</td></tr>
      <tr><td>戌（いぬ・🐶）</td><td>1994 / 2006 / 2018 / 2030</td></tr>
      <tr><td>亥（い・🐗）</td><td>1995 / 2007 / 2019 / 2031</td></tr>
    </table>
    <p>干支は「西暦 ÷ 12 の余り」で決まります。年が変わると一つずつ進み、12年で一周します。履歴書や手続きで使う和暦・西暦の確認にも、年齢計算はよく使われます。</p>
    <h2>よくある質問</h2>'''+faq([
      ('満年齢はいつ増えますか？','民法上は「誕生日の前日が終わる瞬間」に1歳増えます。そのため4月1日生まれは「早生まれ」として前の学年に入ります。'),
      ('数え年の出し方は？','その年の西暦から生まれ年を引いて1を足します（今年−生まれ年＋1）。誕生日に関係なく、元日で増えます。'),
      ('厄年は満年齢？数え年？','一般に厄年は数え年で数えます。神社・地域により扱いが異なる場合があります。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])
    +'''<h2>参考</h2><ul class="seo-refs"><li>「年齢計算ニ関スル法律」（年齢の数え方）</li><li>法務省・各自治体の年齢の数え方の解説</li></ul>''',
  js='''  const ETO=[['子','🐭'],['丑','🐮'],['寅','🐯'],['卯','🐰'],['辰','🐲'],['巳','🐍'],['午','🐴'],['未','🐑'],['申','🐵'],['酉','🐔'],['戌','🐶'],['亥','🐗']];
  function calc(){
    const v=$('bd').value; if(!v){return;}
    const bd=new Date(v+'T00:00:00'); const now=new Date(); now.setHours(0,0,0,0);
    if(bd>now){ $('sub').textContent='未来の日付です。生年月日を確認してください'; show(); return; }
    const days=Math.floor((now-bd)/86400000);
    let man=now.getFullYear()-bd.getFullYear();
    const had=(now.getMonth()>bd.getMonth())||(now.getMonth()===bd.getMonth()&&now.getDate()>=bd.getDate());
    if(!had)man--;
    const kazoe=now.getFullYear()-bd.getFullYear()+1;
    const e=ETO[((bd.getFullYear()%12)+8)%12]; // 西暦%12: 子=4 → index調整
    // 次の誕生日まで
    let nb=new Date(now.getFullYear(),bd.getMonth(),bd.getDate());
    if(nb<now)nb=new Date(now.getFullYear()+1,bd.getMonth(),bd.getDate());
    const toNext=Math.ceil((nb-now)/86400000);
    const pct=Math.max(0,Math.min(100,man/100*100));
    $('sub').textContent=`${bd.getFullYear()}年${bd.getMonth()+1}月${bd.getDate()}日 生まれ`;
    $('man').textContent=man+'歳'; $('kazoe').textContent=kazoe+'歳'; $('eto').textContent=e[1]+' '+e[0]+'年';
    $('next').textContent=(toNext===0?'今日が誕生日🎉':toNext+'日');
    $('lifebar').style.width='0%'; setTimeout(()=>{ $('lifebar').style.width=pct+'%'; },40); $('lifepct').textContent=man+'歳';
    SHARE=`年齢計算してみたら、生まれてから ${num(days)}日 生きてました🎂（満${man}歳・数え${kazoe}歳・${e[0]}年）`;
    show(); anim($('big'),0,days,1000);
  }''')

# ============================================================
# 2) 出産予定日 計算（妊娠週数・ネーゲレ概算）
# ============================================================
add(id='shussan-yotei', cat=KIDS, emoji='👶',
  title='出産予定日 計算｜最終月経から予定日・妊娠週数をチェック｜シミュラボ',
  desc='最終月経開始日から、出産予定日・現在の妊娠週数・予定日までの日数を計算する無料ツール。妊娠期間の早見表つき（目安）。',
  ogtitle='出産予定日 計算｜予定日と妊娠週数', ogdesc='最終月経開始日から出産予定日と妊娠週数を計算（目安）。',
  h1='出産予定日 計算ツール',
  lead='最終月経の開始日を入れるだけで、出産予定日・いまの妊娠週数・予定日まであと何日かを計算します（ネーゲレ概算法。あくまで目安です）。',
  inputs='''    <h2>👶 最終月経の開始日を入れる</h2>
    <div class="row"><div class="field"><label>最終月経の開始日</label><input type="date" id="lmp" value="2026-01-10"></div>
    <div class="field"><label>生理周期 <span class="hint">（日）</span></label><input type="number" id="cyc" value="28" min="20" max="45" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">予定日を計算する</button>''',
  result='''      <div class="ring-wrap seo-anim" id="stage">
        <svg class="prog-ring" viewBox="0 0 120 120" aria-hidden="true">
          <circle class="ring-bg" cx="60" cy="60" r="52"></circle>
          <circle class="ring-fg" id="ring" cx="60" cy="60" r="52" pathLength="100"></circle>
        </svg>
        <div class="ring-center"><div class="rc-num" id="rcNum">—</div><div class="rc-lab">週</div></div>
        <div class="anim-baby" id="baby">👶</div>
      </div>
      <div class="label">いまの妊娠週数（目安）</div>
      <div class="big"><span id="big">0</span><span class="unit">週</span><span class="unit" id="bigd"></span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">出産予定日</div><div class="v accent" id="due">—</div></div>
      <div class="stat"><div class="k">予定日まで</div><div class="v" id="left">—</div></div>
      <div class="stat"><div class="k">いまの時期</div><div class="v" id="phase">—</div></div></div>''',
  article='''    <div class="note" style="border-left:4px solid var(--teal)"><strong>結論</strong>：出産予定日は<b>最終月経の開始日＋280日（40週）</b>で概算します（ネーゲレ概算法）。妊娠週数も同じく最終月経開始日を「0週0日」として数えます。</div>
    <h2>妊娠週数の数え方</h2>
    <p>妊娠週数は、受精日ではなく<b>最終月経の開始日</b>を起点（妊娠0週0日）として数えます。一般的な28日周期の場合、排卵・受精は2週ごろ、出産予定日は40週0日（＝280日後）にあたります。周期が28日からずれる人は、そのぶん予定日を補正します。</p>
    <div class="note"><strong>計算式（ネーゲレ概算法）</strong><br>出産予定日 ＝ 最終月経開始日 ＋ 280日 ＋（生理周期 − 28日）<br>妊娠週数 ＝（今日 − 最終月経開始日）÷ 7</div>
    <h2>妊娠期間のめやす</h2>
    <table class="seo-table">
      <tr><th>区分</th><th>妊娠週数</th><th>めやす</th></tr>
      <tr><td>妊娠初期</td><td>〜15週</td><td>つわりの時期。心拍確認・初診</td></tr>
      <tr><td>妊娠中期（安定期）</td><td>16〜27週</td><td>体調が落ち着きやすい。性別が分かることも</td></tr>
      <tr><td>妊娠後期</td><td>28週〜</td><td>お腹が大きくなる。出産準備</td></tr>
      <tr><td>正産期</td><td>37〜41週</td><td>いつ生まれてもよい時期</td></tr>
    </table>
    <p>実際の出産日は予定日の前後にばらつき、予定日ちょうどに生まれる人はむしろ少数です。正確な妊娠週数・予定日は、妊婦健診の超音波検査で確定します。本ツールはあくまで目安としてご利用ください。</p>
    <h2>よくある質問</h2>'''+faq([
      ('予定日ちょうどに生まれますか？','予定日どおりに生まれる人は少数です。37〜41週の「正産期」ならいつ生まれても正常の範囲です。'),
      ('生理周期が不規則だと？','最終月経からの概算はずれやすくなります。正確には超音波検査（CRL）で予定日を補正します。'),
      ('受精日が分かる場合は？','受精日が分かるなら、その266日後が予定日のめやすです（排卵から数える方法）。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結し、入力内容はどこにも送信されません。')])
    +'''<h2>参考</h2><ul class="seo-refs"><li>日本産科婦人科学会「妊娠週数の数え方・分娩予定日」</li><li>ネーゲレ概算法（分娩予定日の算出）</li></ul>''',
  js='''  function ringSet(p){ $('ring').style.strokeDashoffset = (100 - Math.max(0,Math.min(100,p*100))).toFixed(1); }
  function hearts(n){ const st=$('stage'); for(let i=0;i<n;i++){ const s=document.createElement('span'); s.className='fly-heart'; s.textContent=['💗','💕','💓','✨'][i%4]; s.style.left=(15+Math.random()*70)+'%'; s.style.animationDelay=(Math.random()*0.7).toFixed(2)+'s'; st.appendChild(s); setTimeout(()=>s.remove(),2400); } }
  function calc(){
    const v=$('lmp').value; if(!v){return;}
    const lmp=new Date(v+'T00:00:00'); const cyc=Math.max(20,Math.min(45,+$('cyc').value||28));
    const now=new Date(); now.setHours(0,0,0,0);
    const due=new Date(lmp); due.setDate(due.getDate()+280+(cyc-28));
    const days=Math.floor((now-lmp)/86400000);
    const left=Math.ceil((due-now)/86400000);
    if(days<0||days>320){ $('sub').textContent='日付を確認してください（妊娠期間の範囲外です）'; show(); return; }
    const wk=Math.floor(days/7), wd=days%7;
    const pct=Math.max(0,Math.min(1,days/280));
    let phase; if(wk<16)phase='妊娠初期'; else if(wk<28)phase='安定期(中期)'; else if(wk<37)phase='妊娠後期'; else phase='正産期';
    const dd=`${due.getFullYear()}年${due.getMonth()+1}月${due.getDate()}日`;
    $('sub').textContent=`最終月経 ${lmp.getFullYear()}/${lmp.getMonth()+1}/${lmp.getDate()}・周期${cyc}日`;
    $('bigd').textContent=wd+'日'; $('rcNum').textContent=wk;
    $('due').textContent=dd; $('left').textContent=(left>=0?'あと'+left+'日':'予定日経過'); $('phase').textContent=phase;
    show();
    ringSet(0); setTimeout(()=>ringSet(pct),60);
    const b=$('baby'); b.classList.remove('pop'); void b.offsetWidth; b.classList.add('pop'); hearts(9);
    anim($('big'),0,wk,900);
    SHARE=`出産予定日を計算したら ${dd}、いま妊娠${wk}週${wd}日（${phase}）でした👶 予定日まであと${left>0?left:0}日！`;
  }''')

# ============================================================
# 3) 割引計算機（〇%オフ・節約額・税込）
# ============================================================
add(id='waribiki', cat=MONEY, emoji='🏷️',
  title='割引計算機｜〇%オフの値段・割引後価格・節約額を計算｜シミュラボ',
  desc='元の価格と割引率から、割引後の価格・節約できる額・税込価格を一発で計算する無料ツール。〇割引と〇%オフの早見表つき。',
  ogtitle='割引計算機｜〇%オフの値段と節約額', ogdesc='元の価格と割引率から割引後価格・節約額・税込を計算。',
  h1='割引計算機',
  lead='「30%オフっていくら？」をその場で計算。元の価格と割引率を入れるだけで、割引後の値段・節約できる額・税込価格が一瞬で分かります。',
  inputs='''    <h2>🏷️ 価格と割引率を入れる</h2>
    <div class="row"><div class="field"><label>元の価格 <span class="hint">（円）</span></label><input type="number" id="price" value="3000" min="0" inputmode="numeric"></div>
    <div class="field"><label>割引率 <span class="hint">（%）</span></label><input type="number" id="off" value="30" min="0" max="100" inputmode="numeric"></div></div>
    <div class="field"><label>元の価格は</label><select id="taxin"><option value="0" selected>税抜</option><option value="1">税込（10%）</option></select></div>
    <button class="btn btn-primary" id="calcBtn">割引後の値段を計算する</button>''',
  result='''      <div class="seo-anim ptag-stage" id="stage3"><div class="price-tag" id="ptag"><span id="ptagPct">30</span>% OFF</div></div>
      <div class="label">割引後の価格</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">節約できる額</div><div class="v accent" id="save">—</div></div>
      <div class="stat"><div class="k">割引率</div><div class="v" id="rate">—</div></div>
      <div class="stat"><div class="k">税込（10%）</div><div class="v" id="tax">—</div></div></div>''',
  article='''    <div class="note" style="border-left:4px solid var(--teal)"><strong>結論</strong>：割引後の価格は <b>元の価格 ×（1 − 割引率）</b>、節約額は <b>元の価格 × 割引率</b> で求まります。「3割引」＝30%オフです。</div>
    <h2>割引の計算方法</h2>
    <p>「○%オフ」は、元の価格からその割合ぶんを引いた金額になります。たとえば3,000円の30%オフなら、3,000×0.3＝900円が値引きされ、支払いは3,000−900＝2,100円です。暗算では「1割（10%）＝末尾の0を1つ取る」を基準にすると速く計算できます（3,000円の1割は300円、3割は900円）。</p>
    <div class="note"><strong>計算式</strong><br>割引後の価格 ＝ 元の価格 ×（1 − 割引率）<br>節約できる額 ＝ 元の価格 × 割引率<br>税込 ＝ 税抜 × 1.1</div>
    <h2>〇割引・〇%オフ 早見表</h2>
    <table class="seo-table">
      <tr><th>割引</th><th>支払う割合</th><th>1,000円なら</th><th>3,000円なら</th></tr>
      <tr><td>10%オフ（1割引）</td><td>90%</td><td>900円</td><td>2,700円</td></tr>
      <tr><td>20%オフ（2割引）</td><td>80%</td><td>800円</td><td>2,400円</td></tr>
      <tr><td>30%オフ（3割引）</td><td>70%</td><td>700円</td><td>2,100円</td></tr>
      <tr><td>50%オフ（半額）</td><td>50%</td><td>500円</td><td>1,500円</td></tr>
      <tr><td>70%オフ</td><td>30%</td><td>300円</td><td>900円</td></tr>
    </table>
    <h2>二重割引（クーポン＋セール）に注意</h2>
    <p>「30%オフのあと、さらに10%オフ」は合計40%オフにはなりません。30%オフ（残り70%）に10%オフをかけると 0.7×0.9＝0.63、つまり<b>37%オフ</b>が正解です。割引を重ねるときは掛け算で計算しましょう。</p>
    <h2>よくある質問</h2>'''+faq([
      ('「3割引」と「30%オフ」は同じ？','同じです。3割＝30%なので、どちらも元の価格の30%を値引きします。'),
      ('ポイント還元と割引はどちらがお得？','同じ率なら、その場で安くなる「割引」のほうがお得です。ポイントは使うまで価値が固定されず、有効期限もあるためです。'),
      ('税込価格から割引するには？','税込価格にそのまま割引率をかけてOKです。本ツールは「税抜／税込」を選べます。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])
    +'''<h2>参考</h2><ul class="seo-refs"><li>百分率（パーセント）の計算の基礎</li><li>消費税の税込・税抜計算</li></ul>''',
  js='''  function coins(n){ const st=$('stage3'); for(let i=0;i<n;i++){ const s=document.createElement('span'); s.className='coin-fall'; s.textContent=['🪙','💴','💰'][i%3]; s.style.left=(10+Math.random()*80)+'%'; s.style.animationDelay=(Math.random()*0.5).toFixed(2)+'s'; st.appendChild(s); setTimeout(()=>s.remove(),1600); } }
  function calc(){
    const p=Math.max(0,+$('price').value||0), off=Math.max(0,Math.min(100,+$('off').value||0))/100, taxin=$('taxin').value==='1';
    const after=p*(1-off), save=p*off;
    const nuki = taxin ? after/1.1 : after; const komi = taxin ? after : after*1.1;
    $('sub').textContent=`元 ${num(p)}円（${taxin?'税込':'税抜'}）の ${Math.round(off*100)}%オフ`;
    $('save').textContent=yen(save); $('rate').textContent=Math.round(off*100)+'%'; $('tax').textContent=yen(komi);
    $('ptagPct').textContent=Math.round(off*100);
    const tag=$('ptag'); tag.classList.remove('stamp'); void tag.offsetWidth; tag.classList.add('stamp');
    coins(Math.min(14, 4+Math.round(off*14)));
    show(); anim($('big'),p,after,900);
    SHARE=`割引計算機、${num(p)}円の${Math.round(off*100)}%オフは ${yen(after)}（${yen(save)}お得）でした🏷️`;
  }''')

if __name__=='__main__':
    write_all(SIMS)
    print(f'seo3 done. {len(SIMS)} sims.')
