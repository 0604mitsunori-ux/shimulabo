# -*- coding: utf-8 -*-
"""シミュラボ：便利ツール 第2弾 10本（既存 slug=tool カテゴリに追加）。
gen_sims_tool の TPL/CAT/viz を流用（try無し＝calcバインド確実）。

seo_internal.py / gen_images.py のauto-importに 'gen_sims_tool2' を追加して使う。
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims11 import faq
from gen_sims_tool import TPL, CAT, viz
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SIMS=[]
def add(**k):
    k.setdefault('visual','')
    SIMS.append(k)

# ============================================================
# 1. 素因数分解（素因数分解 34000/KD0/TP21000）
# ============================================================
add(id='soinsu-bunkai', emoji='🔢', cat=CAT,
  title='素因数分解ツール｜数を素数の積に分解（約数の個数も）｜シミュラボ',
  desc='整数を入力するだけで素因数分解し、2×2×3のように素数の積で表示する無料ツール。約数の個数や素数判定もできます。中学・高校数学の確認に。',
  ogtitle='素因数分解ツール｜数を素数の積に分解', ogdesc='整数を素因数分解。約数の個数・素数判定も。無料の素因数分解ツール。',
  h1='素因数分解ツール',
  lead='整数を入れるだけで、素因数分解（素数のかけ算の形）にします。約数の個数や、素数かどうかも判定。数学の宿題や確認に。',
  inputs='''    <h2>🔢 整数を入れる</h2>
    <div class="field"><label>分解する整数 <span class="hint">（2以上）</span></label><input type="number" id="n" value="360" min="2" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">素因数分解する</button>''',
  result='''      <div class="label">素因数分解の結果</div>
      <div class="big" style="font-size:30px;word-break:break-all;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">約数の個数</div><div class="v accent" id="divc">—</div></div>
      <div class="stat"><div class="k">素数判定</div><div class="v" id="prime">—</div></div>
      <div class="stat"><div class="k">桁数</div><div class="v" id="keta">—</div></div></div>''',
  article='''    <div class="note"><strong>素因数分解とは</strong><br>その整数を「素数（1とその数自身でしか割れない数）」だけのかけ算で表すこと。例：360 ＝ 2³ × 3² × 5。</div>
    <h2>素因数分解のやり方</h2>
    <p>小さい素数（2,3,5,7…）で順番に割っていき、割り切れなくなるまで続けます。約数の個数は「各素数の指数に＋1したものの積」で求められます（360なら(3+1)(2+1)(1+1)＝24個）。最大公約数・最小公倍数を求めるときの基礎にもなります。</p>
    <h2>よくある質問</h2>'''+faq([
      ('大きい数も分解できる？','12桁程度まで対応していますが、非常に大きな素数の積は時間がかかる場合があります。'),
      ('1は素数？','いいえ。1は素数ではありません。素数は2以上で約数が2個の数です。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){let n=Math.trunc(+$('n').value||0);
    if(n<2||n>1e12){$('big').textContent='2以上の整数を入力';$('sub').textContent='—';$('divc').textContent='—';$('prime').textContent='—';$('keta').textContent='—';show();return;}
    const orig=n,fac={};let m=n;
    for(let d=2;d*d<=m;d++){while(m%d===0){fac[d]=(fac[d]||0)+1;m/=d;}}
    if(m>1)fac[m]=(fac[m]||0)+1;
    const keys=Object.keys(fac).map(Number).sort((a,b)=>a-b);
    const str=keys.map(p=>fac[p]>1?(p+'^'+fac[p]):String(p)).join(' × ');
    const divc=keys.reduce((a,p)=>a*(fac[p]+1),1);
    const isPrime=(keys.length===1&&fac[keys[0]]===1);
    $('big').textContent=str;$('sub').textContent=num(orig)+' を素因数分解';
    $('divc').textContent=num(divc)+'個';$('prime').textContent=isPrime?'素数です✨':'素数でない';$('keta').textContent=String(orig).length+'桁';
    SHARE=`素因数分解：${num(orig)} ＝ ${str} でした🔢`;show();}''')

# ============================================================
# 2. パスワード生成（パスワード 生成 18000/KD8/TP226000）★
# ============================================================
add(id='password-gen', emoji='🔑', cat=CAT,
  title='パスワード生成ツール｜安全で強いランダムパスワードを作成｜シミュラボ',
  desc='桁数や文字の種類（大文字・数字・記号）を選んで、安全で強いランダムなパスワードをその場で生成する無料ツール。強度判定つき。すべてブラウザ内で生成され送信されません。',
  ogtitle='パスワード生成ツール｜強いパスワードを作成', ogdesc='桁数・文字種を選んで強いランダムパスワードを生成。強度判定つき・無料。',
  h1='パスワード生成ツール',
  lead='桁数と使う文字（大文字・数字・記号）を選ぶだけで、安全で覚えにくい＝強いパスワードをその場で作ります。生成はすべて手元で行われ、外部に送信されません。',
  inputs='''    <h2>🔑 条件を選ぶ</h2>
    <div class="field"><label>桁数 <span class="hint">（4〜64）</span></label><input type="number" id="len" value="16" min="4" max="64" inputmode="numeric"></div>
    <div class="field"><label style="display:flex;gap:8px;align-items:center;"><input type="checkbox" id="upper" checked style="width:auto;"> 大文字 A-Z を含む</label></div>
    <div class="field"><label style="display:flex;gap:8px;align-items:center;"><input type="checkbox" id="numch" checked style="width:auto;"> 数字 0-9 を含む</label></div>
    <div class="field"><label style="display:flex;gap:8px;align-items:center;"><input type="checkbox" id="sym" checked style="width:auto;"> 記号 !@#$ を含む</label></div>
    <button class="btn btn-primary" id="calcBtn">パスワードを生成</button>''',
  result='''      <div class="label">生成されたパスワード</div>
      <div class="big" style="font-size:26px;font-family:monospace;word-break:break-all;user-select:all;"><span id="big">—</span></div>
      <div class="sub" id="sub">タップ＆長押しでコピーできます</div>
      <div class="statline"><div class="stat"><div class="k">強度</div><div class="v accent" id="strength">—</div></div>
      <div class="stat"><div class="k">文字の種類</div><div class="v" id="kinds">—</div></div>
      <div class="stat"><div class="k">桁数</div><div class="v" id="lenv">—</div></div></div>''',
  article='''    <div class="note"><strong>強いパスワードの条件</strong><br>① 長い（12桁以上推奨）② 大文字・小文字・数字・記号を混ぜる ③ 名前や誕生日など推測されやすい語を使わない ④ 使い回さない。</div>
    <h2>安全なパスワードの作り方</h2>
    <p>パスワードは「長くてランダム」なほど破られにくくなります。サービスごとに別々のパスワードを使い、パスワード管理アプリで保管するのがおすすめです。本ツールの生成はすべてあなたのブラウザ内で行われ、生成したパスワードはどこにも送信・保存されません。</p>
    <h2>よくある質問</h2>'''+faq([
      ('生成したパスワードは安全？','生成はブラウザ内で完結し、外部に送信しません。ただし大切なものは管理アプリで保管してください。'),
      ('記号が使えないサイトでは？','「記号を含む」のチェックを外して生成してください。'),
      ('似た文字（0とO）は？','見間違えやすい文字（0,O,1,l,I）は最初から除外しています。')]),
  js=r'''  function calc(){const len=clamp(Math.trunc(+$('len').value||12),4,64);
    let pool='abcdefghijkmnpqrstuvwxyz';let kinds=1;
    if($('upper').checked){pool+='ABCDEFGHJKLMNPQRSTUVWXYZ';kinds++;}
    if($('numch').checked){pool+='23456789';kinds++;}
    if($('sym').checked){pool+='!@#$%&*?-_=+';kinds++;}
    let pw='';const arr=(window.crypto&&crypto.getRandomValues)?crypto.getRandomValues(new Uint32Array(len)):null;
    for(let i=0;i<len;i++){const r=arr?arr[i]:Math.floor(Math.random()*4294967296);pw+=pool[r%pool.length];}
    const bits=len*Math.log2(pool.length);
    const st=bits<40?'弱い':bits<60?'ふつう':bits<80?'強い':'とても強い';
    $('big').textContent=pw;$('sub').textContent='タップ＆長押しでコピーできます';
    $('strength').textContent=st;$('kinds').textContent=kinds+'種類';$('lenv').textContent=len+'桁';
    SHARE=`パスワード生成ツールで ${len}桁・${st} のパスワードを作りました🔑（安全のため共有はしません）`;show();}''')

# ============================================================
# 3. 最大公約数・最小公倍数（最小公倍数 6000/KD0）
# ============================================================
add(id='koubaisu-yakusu', emoji='➗', cat=CAT,
  title='最小公倍数・最大公約数の計算機｜2〜3つの数で計算｜シミュラボ',
  desc='2つまたは3つの整数の最小公倍数（LCM）と最大公約数（GCD）を一発で計算する無料ツール。分数の通分や約分、周期の計算に。求め方も解説。',
  ogtitle='最小公倍数・最大公約数の計算機', ogdesc='2〜3つの数の最小公倍数(LCM)・最大公約数(GCD)を計算。無料。',
  h1='最小公倍数・最大公約数の計算機',
  lead='2つ（または3つ）の整数を入れるだけで、最小公倍数（LCM）と最大公約数（GCD）を計算します。通分・約分や、周期がそろうタイミングの計算に。',
  inputs='''    <h2>➗ 整数を入れる</h2>
    <div class="row"><div class="field"><label>数 1</label><input type="number" id="a" value="12" min="1" inputmode="numeric"></div>
    <div class="field"><label>数 2</label><input type="number" id="b" value="18" min="1" inputmode="numeric"></div></div>
    <div class="field"><label>数 3 <span class="hint">（任意・空欄でOK）</span></label><input type="number" id="c" value="" min="1" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">計算する</button>''',
  result='''      <div class="label">最小公倍数（LCM）</div>
      <div class="big"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">最大公約数（GCD）</div><div class="v accent" id="gcd">—</div></div></div>''',
  article='''    <div class="note"><strong>用語</strong><br>最大公約数（GCD）＝共通して割り切れる最大の数／最小公倍数（LCM）＝共通の倍数のうち最小の数。LCM ＝ a×b ÷ GCD で求まります。</div>
    <h2>最小公倍数・最大公約数の使いみち</h2>
    <p>分数の足し算では分母の最小公倍数で通分し、約分には最大公約数を使います。「2つの歯車が同時にスタート位置に戻るのは何回転後か」「2つのイベントが同じ日に重なるのは何日ごとか」といった周期の計算にも使われます。</p>
    <h2>よくある質問</h2>'''+faq([
      ('3つの数でも計算できる？','はい。数3に入力すると3つの数のLCM・GCDを計算します。'),
      ('求め方は？','ユークリッドの互除法でGCDを求め、LCMは a×b÷GCD で計算しています。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function gcd(x,y){x=Math.abs(x);y=Math.abs(y);while(y){[x,y]=[y,x%y];}return x||1;}
  function lcm(x,y){return x/gcd(x,y)*y;}
  function calc(){let a=Math.trunc(+$('a').value||0),b=Math.trunc(+$('b').value||0),cR=$('c').value,c=cR===''?null:Math.trunc(+cR||0);
    if(a<1||b<1||(c!==null&&c<1)){$('big').textContent='1以上の整数を入力';$('sub').textContent='—';$('gcd').textContent='—';show();return;}
    let g=gcd(a,b),l=lcm(a,b);if(c){g=gcd(g,c);l=lcm(l,c);}
    $('big').textContent=num(l);$('sub').textContent=c?`${a}, ${b}, ${c}`:`${a}, ${b}`;
    $('gcd').textContent=num(g);
    SHARE=`最小公倍数・最大公約数：${c?a+','+b+','+c:a+','+b} → LCM=${num(l)}・GCD=${num(g)} でした➗`;show();}''')

# ============================================================
# 4. 温度変換（摂氏 華氏 3600/KD0/TP5700）
# ============================================================
add(id='ondo-henkan', emoji='🌡️', cat=CAT,
  title='温度変換ツール｜摂氏・華氏・ケルビンを相互変換｜シミュラボ',
  desc='摂氏（℃）・華氏（℉）・ケルビン（K）を相互に変換できる無料の温度変換ツール。海外の天気やレシピのオーブン温度（華氏）の換算に便利です。',
  ogtitle='温度変換ツール｜摂氏・華氏・ケルビンを変換', ogdesc='℃⇔℉⇔Kを相互変換。海外の天気・オーブン温度の換算に。無料。',
  h1='温度変換ツール（摂氏・華氏・ケルビン）',
  lead='数値と単位を選ぶだけで、摂氏（℃）・華氏（℉）・ケルビン（K）に一度に変換します。海外の天気予報やレシピのオーブン温度（華氏）の換算に。',
  inputs='''    <h2>🌡️ 温度を入れる</h2>
    <div class="row"><div class="field"><label>温度</label><input type="number" id="v" value="100" step="any" inputmode="decimal"></div>
    <div class="field"><label>単位</label><select id="from"><option value="c">摂氏 ℃</option><option value="f">華氏 ℉</option><option value="k">ケルビン K</option></select></div></div>
    <button class="btn btn-primary" id="calcBtn">変換する</button>''',
  result='''      <div class="label">摂氏</div>
      <div class="big"><span id="big">—</span><span class="unit">℃</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">華氏</div><div class="v accent" id="f">—</div></div>
      <div class="stat"><div class="k">ケルビン</div><div class="v" id="k">—</div></div></div>''',
  article='''    <div class="note"><strong>変換式</strong><br>華氏→摂氏：(℉ − 32) × 5 ÷ 9／摂氏→華氏：℃ × 9 ÷ 5 ＋ 32／ケルビン：K ＝ ℃ ＋ 273.15</div>
    <h2>温度の単位について</h2>
    <p>日本では摂氏（℃）ですが、アメリカでは華氏（℉）が主流。華氏100度は摂氏約37.8度（人肌くらい）、華氏350度はオーブンの中温（約177℃）です。ケルビン（K）は科学で使う絶対温度で、摂氏に273.15を足した値です。</p>
    <h2>よくある質問</h2>'''+faq([
      ('華氏350度は摂氏何度？','約177℃です。アメリカのレシピでよく出てくるオーブン温度です。'),
      ('水が凍る・沸騰する温度は？','摂氏0℃＝華氏32℉（凍る）、摂氏100℃＝華氏212℉（沸騰）です。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const v=+$('v').value||0,u=$('from').value;let c;
    if(u==='c')c=v;else if(u==='f')c=(v-32)*5/9;else c=v-273.15;
    const f=c*9/5+32,k=c+273.15;
    $('big').textContent=num(c);$('sub').textContent=`入力：${num(v)} ${u==='c'?'℃':u==='f'?'℉':'K'}`;
    $('f').textContent=num(f)+' ℉';$('k').textContent=num(k)+' K';
    SHARE=`温度変換：${num(c)}℃ ＝ ${num(f)}℉ ＝ ${num(k)}K でした🌡️`;show();}''')

# ============================================================
# 5. アスペクト比計算（アスペクト比 計算 1900/KD0/TP12000）
# ============================================================
add(id='aspect-keisan', emoji='🖼️', cat=CAT,
  title='アスペクト比計算機｜縦横比を求める・サイズを比から計算｜シミュラボ',
  desc='幅と高さからアスペクト比（16:9など）を求めたり、比率を保ったまま片方のサイズから他方を計算できる無料ツール。動画・画像・デザインのサイズ調整に。',
  ogtitle='アスペクト比計算機｜縦横比を求める', ogdesc='幅と高さから16:9などの比を計算。比を保ってサイズ変換も。無料。',
  h1='アスペクト比計算機',
  lead='幅と高さを入れると、16:9のようなアスペクト比（縦横比）を求めます。さらに「新しい幅」を入れると、比率を保ったままの高さも計算。動画・画像・スライドのサイズ調整に。',
  inputs='''    <h2>🖼️ 幅と高さを入れる</h2>
    <div class="row"><div class="field"><label>幅 W</label><input type="number" id="w" value="1920" min="1" inputmode="numeric"></div>
    <div class="field"><label>高さ H</label><input type="number" id="h" value="1080" min="1" inputmode="numeric"></div></div>
    <div class="field"><label>新しい幅 <span class="hint">（任意・比を保って高さを計算）</span></label><input type="number" id="nw" value="" min="1" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">アスペクト比を計算</button>''',
  result='''      <div class="label">アスペクト比</div>
      <div class="big" style="font-size:38px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">小数の比</div><div class="v accent" id="dec">—</div></div>
      <div class="stat"><div class="k">新しい幅なら高さは</div><div class="v" id="nh">—</div></div></div>''',
  article='''    <div class="note"><strong>アスペクト比とは</strong><br>幅と高さの比のこと。16:9（地デジ・YouTube）、4:3（昔のTV）、1:1（Instagram）、9:16（スマホ縦・TikTok）などが代表的。</div>
    <h2>アスペクト比の使い方</h2>
    <p>動画や画像を別のサイズに変えるとき、アスペクト比を保たないと縦長・横長に歪んでしまいます。このツールは幅と高さから比を求め、最大公約数で「16:9」のように簡単な整数比にします。「幅を1280にしたいけど高さは？」も自動計算します。</p>
    <h2>よくある質問</h2>'''+faq([
      ('16:9のサイズ例は？','1920×1080、1280×720、3840×2160（4K）などが16:9です。'),
      ('比がきれいにならない','映像規格でない数値だと複雑な比になります。小数の比も併記しています。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function gcd(x,y){x=Math.abs(Math.round(x));y=Math.abs(Math.round(y));while(y){[x,y]=[y,x%y];}return x||1;}
  function calc(){const w=+$('w').value||0,h=+$('h').value||0,nw=$('nw').value;
    if(w<1||h<1){$('big').textContent='幅と高さを入力';show();return;}
    const g=gcd(w,h),rw=Math.round(w/g),rh=Math.round(h/g);
    $('big').textContent=rw+' : '+rh;$('sub').textContent=`${num(w)} × ${num(h)}`;
    $('dec').textContent='1 : '+num(h/w*100)/100+'　('+num(w/h*100)/100+':1)';
    $('nh').textContent=nw!==''?num((+nw)*h/w)+' px':'—';
    SHARE=`アスペクト比計算：${num(w)}×${num(h)} は ${rw}:${rh} でした🖼️`;show();}''')

# ============================================================
# 6. ローマ字変換（ローマ字 変換 1600/KD10/TP5400）
# ============================================================
add(id='romaji-henkan', emoji='🔡', cat=CAT,
  title='ローマ字変換ツール｜ひらがな・カタカナをローマ字に変換｜シミュラボ',
  desc='ひらがな・カタカナをローマ字（ヘボン式）に変換する無料ツール。名前や住所のローマ字表記、パスポート・英語表記の確認に。',
  ogtitle='ローマ字変換ツール｜かなをローマ字に変換', ogdesc='ひらがな・カタカナをヘボン式ローマ字に変換。名前・住所表記に。無料。',
  h1='ローマ字変換ツール',
  lead='ひらがな・カタカナを入れるだけで、ローマ字（ヘボン式に近い表記）に変換します。名前や地名のローマ字表記の確認に。',
  inputs='''    <h2>🔡 かなを入れる</h2>
    <input type="text" id="v" value="こんにちは" autocomplete="off" style="width:100%;font-size:18px;padding:12px;border:1.5px solid var(--line);border-radius:10px;">
    <button class="btn btn-primary" id="calcBtn" style="margin-top:10px;">ローマ字に変換</button>''',
  result='''      <div class="label">ローマ字</div>
      <div class="big" style="font-size:28px;word-break:break-all;user-select:all;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">先頭大文字</div><div class="v accent" id="cap">—</div></div>
      <div class="stat"><div class="k">すべて大文字</div><div class="v" id="upper">—</div></div></div>''',
  article='''    <div class="note"><strong>ヘボン式ローマ字</strong><br>パスポートなどで使われる表記。「し→shi」「ち→chi」「つ→tsu」「ふ→fu」「じ→ji」など。長音（伸ばす音）は通常そのまま表記しません。</div>
    <h2>ローマ字変換の使い方</h2>
    <p>名前や住所をローマ字で書くときに。本ツールはヘボン式に近い形で変換します。促音「っ」は次の子音を重ね（がっこう→gakkou）、撥音「ん」はnで表します。固有名詞は慣用表記が優先される場合があるため、公的書類では各機関の規定をご確認ください。</p>
    <h2>よくある質問</h2>'''+faq([
      ('漢字も変換できる？','いいえ。ひらがな・カタカナに対応しています。漢字はかなに直してから入力してください。'),
      ('ヘボン式と訓令式の違いは？','「し」をshi（ヘボン）かsi（訓令）かなどが異なります。本ツールはヘボン式寄りです。'),
      ('データは送信されますか？','いいえ。変換はすべてブラウザ内で完結します。')]),
  js=r'''  const M={'きゃ':'kya','きゅ':'kyu','きょ':'kyo','しゃ':'sha','しゅ':'shu','しょ':'sho','ちゃ':'cha','ちゅ':'chu','ちょ':'cho','にゃ':'nya','にゅ':'nyu','にょ':'nyo','ひゃ':'hya','ひゅ':'hyu','ひょ':'hyo','みゃ':'mya','みゅ':'myu','みょ':'myo','りゃ':'rya','りゅ':'ryu','りょ':'ryo','ぎゃ':'gya','ぎゅ':'gyu','ぎょ':'gyo','じゃ':'ja','じゅ':'ju','じょ':'jo','びゃ':'bya','びゅ':'byu','びょ':'byo','ぴゃ':'pya','ぴゅ':'pyu','ぴょ':'pyo',
    'あ':'a','い':'i','う':'u','え':'e','お':'o','か':'ka','き':'ki','く':'ku','け':'ke','こ':'ko','さ':'sa','し':'shi','す':'su','せ':'se','そ':'so','た':'ta','ち':'chi','つ':'tsu','て':'te','と':'to','な':'na','に':'ni','ぬ':'nu','ね':'ne','の':'no','は':'ha','ひ':'hi','ふ':'fu','へ':'he','ほ':'ho','ま':'ma','み':'mi','む':'mu','め':'me','も':'mo','や':'ya','ゆ':'yu','よ':'yo','ら':'ra','り':'ri','る':'ru','れ':'re','ろ':'ro','わ':'wa','を':'o','ん':'n','が':'ga','ぎ':'gi','ぐ':'gu','げ':'ge','ご':'go','ざ':'za','じ':'ji','ず':'zu','ぜ':'ze','ぞ':'zo','だ':'da','ぢ':'ji','づ':'zu','で':'de','ど':'do','ば':'ba','び':'bi','ぶ':'bu','べ':'be','ぼ':'bo','ぱ':'pa','ぴ':'pi','ぷ':'pu','ぺ':'pe','ぽ':'po','ー':'','、':', ','。':'. ','　':' ',' ':' '};
  function kata2hira(s){return s.replace(/[ァ-ヶ]/g,c=>String.fromCharCode(c.charCodeAt(0)-0x60));}
  function conv(src){let s=kata2hira(src),out='',i=0;
    while(i<s.length){
      if(s[i]==='っ'){ // 促音：次の子音を重ねる
        const two=s.substr(i+1,2),one=s.substr(i+1,1);let r=M[two]||M[one];
        if(r&&/^[a-z]/.test(r)){out+=r[0];i++;continue;}else{i++;continue;}}
      const two=s.substr(i,2);if(M[two]){out+=M[two];i+=2;continue;}
      const one=s[i];if(M[one]!==undefined){out+=M[one];i++;continue;}
      out+=one;i++;}
    return out;}
  function calc(){const src=$('v').value||'';const r=conv(src);
    $('big').textContent=r||'—';$('sub').textContent='入力：'+src;
    $('cap').textContent=r?(r.charAt(0).toUpperCase()+r.slice(1)):'—';$('upper').textContent=r.toUpperCase()||'—';
    SHARE=`ローマ字変換：「${src}」→「${r}」でした🔡`;show();}''')

# ============================================================
# 7. 平均計算（平均 計算 1200/KD0/TP9900）
# ============================================================
add(id='heikin-keisan', emoji='📊', cat=CAT,
  title='平均値計算ツール｜複数の数の平均・合計・中央値を計算｜シミュラボ',
  desc='数値をまとめて入力するだけで、平均・合計・個数・最大・最小・中央値を一度に計算する無料ツール。テストの点数や記録の集計に。',
  ogtitle='平均値計算ツール｜平均・合計・中央値を計算', ogdesc='複数の数の平均・合計・個数・最大最小・中央値を一発計算。無料。',
  h1='平均値計算ツール',
  lead='数値をカンマ・スペース・改行で区切って入れるだけ。平均・合計・個数・最大・最小・中央値をまとめて計算します。テストの点数や記録の集計に。',
  inputs='''    <h2>📊 数値を入れる</h2>
    <p style="color:var(--ink-2);font-size:13px;margin:-2px 0 6px;">カンマ・スペース・改行で区切ってください</p>
    <textarea id="v" rows="4" placeholder="例：80, 75, 92, 60, 88" style="width:100%;font-size:15px;padding:12px;border:1.5px solid var(--line);border-radius:10px;">80, 75, 92, 60, 88</textarea>
    <button class="btn btn-primary" id="calcBtn" style="margin-top:10px;">計算する</button>''',
  result='''      <div class="label">平均</div>
      <div class="big"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">合計 / 個数</div><div class="v accent" id="sumc">—</div></div>
      <div class="stat"><div class="k">最大 / 最小</div><div class="v" id="mm">—</div></div>
      <div class="stat"><div class="k">中央値</div><div class="v" id="med">—</div></div></div>''',
  article='''    <div class="note"><strong>用語</strong><br>平均＝合計÷個数／中央値＝小さい順に並べたときの真ん中の値。極端な値があるときは中央値のほうが実感に近いことがあります。</div>
    <h2>平均値の計算</h2>
    <p>テストの点数、毎日の記録、売上などの平均をまとめて計算します。平均は全体の傾向をつかむのに便利ですが、1つだけ極端に大きい/小さい値があると引っ張られます。そんなときは中央値も合わせて見るのがおすすめです。</p>
    <h2>よくある質問</h2>'''+faq([
      ('区切りは何が使える？','カンマ・スペース・改行のどれでもOKです。混在しても大丈夫。'),
      ('小数も計算できる？','はい。小数を含めて計算できます。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const raw=$('v').value||'';const nums=raw.split(/[^0-9.\-]+/).filter(x=>x!==''&&!isNaN(+x)).map(Number);
    if(nums.length===0){$('big').textContent='数値を入力';$('sub').textContent='—';$('sumc').textContent='—';$('mm').textContent='—';$('med').textContent='—';show();return;}
    const sum=nums.reduce((a,b)=>a+b,0),avg=sum/nums.length;
    const sorted=nums.slice().sort((a,b)=>a-b),n=sorted.length;
    const med=n%2?sorted[(n-1)/2]:(sorted[n/2-1]+sorted[n/2])/2;
    $('big').textContent=num(avg);$('sub').textContent=nums.length+'個の平均';
    $('sumc').textContent=num(sum)+' / '+nums.length;$('mm').textContent=num(sorted[n-1])+' / '+num(sorted[0]);$('med').textContent=num(med);
    SHARE=`平均値計算：${nums.length}個の平均は ${num(avg)} でした📊`;show();}''')

# ============================================================
# 8. 時給計算（時給 計算 900/KD2/TP48000）
# ============================================================
add(id='jikyu-keisan', emoji='💴', cat=CAT,
  title='時給計算機｜時給から日給・月収・年収を計算（手取り目安も）｜シミュラボ',
  desc='時給と1日の労働時間・月の出勤日数から、日給・週給・月収・年収を計算する無料ツール。手取りのおおよその目安も表示。バイト・パートの収入計算に。',
  ogtitle='時給計算機｜時給から月収・年収を計算', ogdesc='時給と労働時間・出勤日数から日給・月収・年収を計算。手取り目安も。',
  h1='時給計算機（日給・月収・年収）',
  lead='時給・1日の労働時間・月の出勤日数を入れると、日給・週給・月収・年収を計算します。手取りのおおよその目安も。バイト・パートの収入見込みに。',
  inputs='''    <h2>💴 条件を入れる</h2>
    <div class="row"><div class="field"><label>時給 <span class="hint">（円）</span></label><input type="number" id="w" value="1100" min="0" inputmode="numeric"></div>
    <div class="field"><label>1日の労働時間 <span class="hint">（時間）</span></label><input type="number" id="h" value="8" min="0" step="0.5" inputmode="decimal"></div></div>
    <div class="field"><label>月の出勤日数 <span class="hint">（日）</span></label><input type="number" id="d" value="20" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">月収・年収を計算</button>''',
  result='''      <div class="label">月収（額面）</div>
      <div class="big" style="font-size:30px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">日給</div><div class="v" id="day">—</div></div>
      <div class="stat"><div class="k">年収（額面）</div><div class="v accent" id="year">—</div></div>
      <div class="stat"><div class="k">手取り月収の目安</div><div class="v" id="net">—</div></div></div>''',
  article='''    <div class="note"><strong>計算式</strong><br>日給 ＝ 時給 × 1日の時間／月収 ＝ 日給 × 出勤日数／年収 ＝ 月収 × 12。手取りは額面の約80%が目安（収入や扶養で変わります）。</div>
    <h2>時給から月収・年収を計算</h2>
    <p>「時給1,100円で月20日・8時間働くと月収・年収はいくら？」がすぐ分かります。手取りは社会保険・税金が引かれるため、額面の約8割が目安。扶養の範囲（年103万・130万の壁など）を意識する場合の確認にも使えます。</p>
    <h2>よくある質問</h2>'''+faq([
      ('手取りはなぜ8割？','社会保険料や所得税・住民税が引かれるためです。収入や条件で変わるので目安です。'),
      ('交通費は含む？','本ツールは含みません。別途加算してください。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const w=+$('w').value||0,h=+$('h').value||0,d=+$('d').value||0;
    const day=w*h,month=day*d,year=month*12;
    $('big').textContent=yen(month);$('sub').textContent=`時給${num(w)}円 × ${h}時間 × 月${d}日`;
    $('day').textContent=yen(day);$('year').textContent=yen(year);$('net').textContent=yen(month*0.8);
    SHARE=`時給計算機：時給${num(w)}円で月収 約${yen(month)}・年収 約${yen(year)} でした💴`;show();}''')

# ============================================================
# 9. 全角・半角変換（全角 半角 変換 400/KD0/TP19000）
# ============================================================
add(id='zenkaku-hankaku', emoji='🔠', cat=CAT,
  title='全角・半角変換ツール｜英数字・記号・カナをまとめて変換｜シミュラボ',
  desc='文章中の英数字・記号・カタカナを、全角⇔半角にまとめて変換する無料ツール。フォーム入力エラーやデータ整形、表記ゆれの統一に便利です。',
  ogtitle='全角・半角変換ツール｜英数字・カナを変換', ogdesc='英数字・記号・カナを全角⇔半角に一括変換。表記ゆれの統一に。無料。',
  h1='全角・半角変換ツール',
  lead='英数字・記号・カタカナを、全角と半角でまとめて変換します。「半角で入力してください」のフォームエラーや、データの表記ゆれの統一に。',
  inputs='''    <h2>🔠 文章を入れる</h2>
    <textarea id="v" rows="3" placeholder="変換したい文章" style="width:100%;font-size:15px;padding:12px;border:1.5px solid var(--line);border-radius:10px;">ＡＢＣ１２３ｱｲｳ</textarea>
    <div class="field" style="margin-top:10px;"><label>変換方向</label><select id="mode"><option value="half">→ 半角に変換</option><option value="full">→ 全角に変換</option></select></div>
    <button class="btn btn-primary" id="calcBtn">変換する</button>''',
  result='''      <div class="label">変換結果</div>
      <div class="big" style="font-size:24px;word-break:break-all;user-select:all;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">文字数</div><div class="v accent" id="len">—</div></div></div>''',
  article='''    <div class="note"><strong>全角・半角とは</strong><br>全角は「ＡＢＣ１２３」のように1文字ぶんの幅、半角は「ABC123」と半分の幅。見た目が似ていてもコンピュータ上は別の文字として扱われます。</div>
    <h2>全角・半角変換の使い方</h2>
    <p>「電話番号は半角で」というフォームでエラーが出るとき、全角で入力した数字を半角に直せます。逆に、表記をそろえたいときは全角に統一も可能。英数字・記号・カタカナに対応しています。</p>
    <h2>よくある質問</h2>'''+faq([
      ('カタカナも変換できる？','はい。半角カナ⇔全角カナに対応しています（濁点も結合します）。'),
      ('ひらがなは？','ひらがなには半角がないため変換対象外です。'),
      ('データは送信されますか？','いいえ。変換はすべてブラウザ内で完結します。')]),
  js=r'''  const HANKANA={'ｱ':'ア','ｲ':'イ','ｳ':'ウ','ｴ':'エ','ｵ':'オ','ｶ':'カ','ｷ':'キ','ｸ':'ク','ｹ':'ケ','ｺ':'コ','ｻ':'サ','ｼ':'シ','ｽ':'ス','ｾ':'セ','ｿ':'ソ','ﾀ':'タ','ﾁ':'チ','ﾂ':'ツ','ﾃ':'テ','ﾄ':'ト','ﾅ':'ナ','ﾆ':'ニ','ﾇ':'ヌ','ﾈ':'ネ','ﾉ':'ノ','ﾊ':'ハ','ﾋ':'ヒ','ﾌ':'フ','ﾍ':'ヘ','ﾎ':'ホ','ﾏ':'マ','ﾐ':'ミ','ﾑ':'ム','ﾒ':'メ','ﾓ':'モ','ﾔ':'ヤ','ﾕ':'ユ','ﾖ':'ヨ','ﾗ':'ラ','ﾘ':'リ','ﾙ':'ル','ﾚ':'レ','ﾛ':'ロ','ﾜ':'ワ','ｦ':'ヲ','ﾝ':'ン','ｧ':'ァ','ｨ':'ィ','ｩ':'ゥ','ｪ':'ェ','ｫ':'ォ','ｯ':'ッ','ｬ':'ャ','ｭ':'ュ','ｮ':'ョ','ﾞ':'゛','ﾟ':'゜','ｰ':'ー','｡':'。','｢':'「','｣':'」','､':'、','･':'・'};
  function toHalf(s){s=s.replace(/[Ａ-Ｚａ-ｚ０-９]/g,c=>String.fromCharCode(c.charCodeAt(0)-0xFEE0));
    s=s.replace(/[！-～]/g,c=>String.fromCharCode(c.charCodeAt(0)-0xFEE0));return s.replace(/　/g,' ');}
  function toFull(s){let r='';for(const c of s){if(HANKANA[c]){r+=HANKANA[c];continue;}
    if(/[A-Za-z0-9]/.test(c)||/[!-~]/.test(c)){r+=String.fromCharCode(c.charCodeAt(0)+0xFEE0);}else if(c===' '){r+='　';}else r+=c;}
    r=r.replace(/([カ-ト])゛/g,(m,k)=>String.fromCharCode(k.charCodeAt(0)+1));return r;}
  function calc(){const src=$('v').value||'',mode=$('mode').value;
    const r=mode==='half'?toHalf(src):toFull(src);
    $('big').textContent=r||'—';$('sub').textContent=(mode==='half'?'半角に変換':'全角に変換');
    $('len').textContent=Array.from(r).length+'字';
    SHARE=`全角・半角変換ツールで変換しました🔠`;show();}''')

# ============================================================
# 10. 図形の面積計算（円の面積 計算 100/KD0/TP7000）
# ============================================================
add(id='menseki-keisan', emoji='📐', cat=CAT,
  title='面積計算ツール｜円・三角形・長方形・台形の面積を計算｜シミュラボ',
  desc='円・正方形・長方形・三角形・台形・平行四辺形の面積を、必要な長さを入れるだけで計算する無料ツール。円は円周も表示。算数・DIY・土地の計算に。',
  ogtitle='面積計算ツール｜円・三角形・台形の面積', ogdesc='円・長方形・三角形・台形などの面積を計算。円周も。無料の面積計算。',
  h1='面積計算ツール（円・三角形・台形ほか）',
  lead='図形を選んで長さを入れるだけで面積を計算します。円・正方形・長方形・三角形・台形・平行四辺形に対応。円は円周も表示します。',
  inputs='''    <h2>📐 図形と長さを入れる</h2>
    <div class="field"><label>図形</label><select id="shape"><option value="circle">円</option><option value="rect">長方形</option><option value="square">正方形</option><option value="tri">三角形</option><option value="trapezoid">台形</option><option value="para">平行四辺形</option></select></div>
    <div class="row"><div class="field"><label id="la">半径</label><input type="number" id="a" value="5" step="any" min="0" inputmode="decimal"></div>
    <div class="field"><label id="lb">（不要）</label><input type="number" id="b" value="0" step="any" min="0" inputmode="decimal"></div></div>
    <div class="field"><label id="lc">（不要）</label><input type="number" id="c" value="0" step="any" min="0" inputmode="decimal"></div>
    <button class="btn btn-primary" id="calcBtn">面積を計算</button>''',
  result='''      <div class="label">面積</div>
      <div class="big"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">参考</div><div class="v accent" id="extra">—</div></div></div>''',
  article='''    <div class="note"><strong>面積の公式</strong><br>円＝半径×半径×π／長方形＝縦×横／三角形＝底辺×高さ÷2／台形＝(上底＋下底)×高さ÷2／平行四辺形＝底辺×高さ</div>
    <h2>面積の計算</h2>
    <p>図形を選ぶと必要な入力欄のラベルが切り替わります。算数の宿題はもちろん、部屋や土地の広さ、花壇やDIYのサイズ計算にも。円を選ぶと面積に加えて円周も表示します。</p>
    <h2>よくある質問</h2>'''+faq([
      ('単位は？','入力した長さの単位の2乗が面積の単位になります（cmで入れればcm²）。'),
      ('円周率は？','π＝3.14159…で計算しています。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  const CFG={circle:['半径','（不要）','（不要）'],rect:['縦','横','（不要）'],square:['一辺','（不要）','（不要）'],tri:['底辺','高さ','（不要）'],trapezoid:['上底','下底','高さ'],para:['底辺','高さ','（不要）']};
  function fill(){const s=$('shape').value,c=CFG[s];$('la').textContent=c[0];$('lb').textContent=c[1];$('lc').textContent=c[2];
    $('b').parentElement.style.opacity=c[1]==='（不要）'?'.4':'1';$('c').parentElement.style.opacity=c[2]==='（不要）'?'.4':'1';}
  $('shape').addEventListener('change',fill);
  function calc(){const s=$('shape').value,a=+$('a').value||0,b=+$('b').value||0,c=+$('c').value||0;let area,extra='—';
    if(s==='circle'){area=a*a*Math.PI;extra='円周 '+num(2*a*Math.PI);}
    else if(s==='rect'){area=a*b;extra='周囲 '+num(2*(a+b));}
    else if(s==='square'){area=a*a;extra='周囲 '+num(4*a);}
    else if(s==='tri'){area=a*b/2;}
    else if(s==='trapezoid'){area=(a+b)*c/2;}
    else{area=a*b;}
    $('big').textContent=num(area);$('sub').textContent=sel('shape').text+'の面積';$('extra').textContent=extra;
    SHARE=`面積計算：${sel('shape').text}の面積は ${num(area)} でした📐`;show();}
  fill();''')

# ============================================================
def render():
    for s in SIMS:
        d=os.path.join(ROOT,'sims',s['id']); os.makedirs(d,exist_ok=True)
        html=(TPL.replace('__TITLE__',s['title']).replace('__DESC__',s['desc'])
              .replace('__OGTITLE__',s['ogtitle']).replace('__OGDESC__',s['ogdesc'])
              .replace('__CAT__',s['cat']).replace('__H1__',s['h1']).replace('__LEAD__',s['lead'])
              .replace('__INPUTS__',s['inputs']).replace('__RESULT__',s['result'])
              .replace('__VISUAL__',s['visual']).replace('__ARTICLE__',s['article'])
              .replace('__JS__',s['js']).replace('__ID__',s['id']))
        with open(os.path.join(d,'index.html'),'w',encoding='utf-8') as f: f.write(html)
        print('created sims/'+s['id'])

if __name__=='__main__':
    render()
    print(f'tool2 done. {len(SIMS)} sims.')
