# -*- coding: utf-8 -*-
"""シミュラボ：上位KWの横展開12本（大学出席率3=teacher / 守護霊3=uranai / 車電車3=car / おじおば3=life）。write_all再利用。"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims11 import faq, write_all

SIMS = []
def add(**k): SIMS.append(k)
def C(t): return '<div class="note" style="border-left:4px solid var(--teal)"><strong>ポイント</strong>：'+t+'</div>'
def REF(items): return '<h2>参考</h2><ul class="seo-refs">'+''.join('<li>'+i+'</li>' for i in items)+'</ul>'

TEACHER='教員・先生'; URANAI='占い・診断'; CAR='クルマ・乗り物'; LIFE='人生・自分ごと'

# 占い（生年月日シード）用テンプレ
URES = '''      <div class="label">__L__</div>
      <div id="emoji" style="font-size:60px;line-height:1.1;">🔮</div>
      <div class="big" style="font-size:24px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="desc" style="text-align:left;margin-top:12px;">—</div>'''
BD = '''    <h2>__H__</h2>
    <div class="field"><label>あなたの生年月日</label><input type="date" id="bd" value="1995-07-07"></div>
    <button class="btn btn-primary" id="calcBtn">診断する 🔮</button>'''
def useed_js(res, stpl):
    return ('  const RES='+json.dumps(res,ensure_ascii=False)+';\n'
            + r'''  function h(s){let x=2166136261;for(let i=0;i<s.length;i++){x^=s.charCodeAt(i);x=Math.imul(x,16777619);}return x>>>0;}
  function calc(){const bd=$('bd').value;if(!bd){alert('生年月日を入れてね');return;}
    const r=RES[h(bd)%RES.length];
    $('emoji').textContent=r[0];$('big').textContent=r[1];$('sub').textContent='診断結果';$('desc').textContent='✨ '+r[2];
    show();SHARE='''+json.dumps(stpl,ensure_ascii=False)+r'''.replace('{n}',r[1]);}''')

# クイズ用（チェック数→％）
def quiz(items, bands, stpl, htitle, emoji):
    n=len(items)
    inputs = '    <h2>'+emoji+' あてはまるものをチェック</h2>\n' + '\n'.join(
      '    <label style="display:flex;gap:10px;align-items:flex-start;padding:10px 12px;border:1.5px solid var(--line);border-radius:10px;margin-bottom:8px;cursor:pointer;"><input type="checkbox" id="q%d" style="margin-top:3px;width:18px;height:18px;flex:none;"><span>%s</span></label>' % (i+1,t)
      for i,t in enumerate(items)) + '\n    <button class="btn btn-primary" id="calcBtn">診断する</button>'
    result = '''      <div class="label">__L__</div>
      <div class="big"><span id="big">0</span><span class="unit">%</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">タイプ</div><div class="v accent" id="type">—</div></div>
      <div class="stat"><div class="k">あてはまった数</div><div class="v" id="cnt">—</div></div>
      <div class="stat"><div class="k">ひとこと</div><div class="v" id="adv">—</div></div></div>'''.replace('__L__', htitle)
    js = ('  const N='+str(n)+', BANDS='+json.dumps(bands,ensure_ascii=False)+';\n'
          + r'''  function calc(){let c=0;for(let i=1;i<=N;i++){const e=$('q'+i);if(e&&e.checked)c++;}
    const pct=Math.round(c/N*100);
    let b=BANDS[BANDS.length-1];for(const x of BANDS){if(pct<=x[0]){b=x;break;}}
    $('sub').textContent=b[1]; $('type').textContent=b[1]; $('cnt').textContent=c+'/'+N+'個'; $('adv').textContent=b[2];
    show();anim($('big'),0,pct,800);
    SHARE='''+json.dumps(stpl,ensure_ascii=False)+r'''.replace('{p}',pct).replace('{t}',b[1]);}''')
    return inputs, result, js

# ============================================================
# 大学 出席率クラスタ（teacher）
# ============================================================
add(id='daigaku-shusseki', cat=TEACHER, emoji='🎓',
  title='大学 出席率 計算｜全15回で単位が取れる？出席何回で認定？｜シミュラボ',
  desc='大学の1科目（全15回など）の出席回数・欠席回数から、出席率と単位認定ライン（3分の2以上など）を満たすか、あと何回休めるかを計算する大学生向け無料ツール。',
  ogtitle='大学 出席率 計算｜単位は取れる？', ogdesc='全授業回数と欠席から出席率・単位認定・あと何回休めるかを計算。',
  h1='大学 出席率 計算',
  lead='大学の1科目について、出席率と「単位認定ラインを満たしているか」「あと何回休めるか」を計算します。全15回など授業回数を入れて、欠席のリスクをチェック。',
  inputs='''    <h2>🎓 条件を入れる</h2>
    <div class="row"><div class="field"><label>全授業回数 <span class="hint">（回・予定含む）</span></label><input type="number" id="total" value="15" min="1" inputmode="numeric"></div>
    <div class="field"><label>これまでの欠席回数 <span class="hint">（回）</span></label><input type="number" id="abs" value="3" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>単位認定に必要な出席</label><select id="line"><option value="2/3" selected>3分の2以上（約66.7%）</option><option value="3/4">4分の3以上（75%）</option><option value="4/5">80%以上</option></select></div>
    <button class="btn btn-primary" id="calcBtn">出席率を計算する</button>''',
  result='''      <div class="label">現時点の出席率</div>
      <div class="big"><span id="big">0</span><span class="unit">%</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">単位認定</div><div class="v accent" id="hantei">—</div></div>
      <div class="stat"><div class="k">あと休める回数</div><div class="v" id="left">—</div></div>
      <div class="stat"><div class="k">必要な最低出席</div><div class="v" id="need">—</div></div></div>''',
  article=C('大学の多くの科目は<b>全15回で構成され、3分の2以上（＝10回以上）の出席</b>を単位認定の条件とするのが一般的です。欠席が全体の3分の1（15回なら5回）を超えると、試験を受けても単位が認定されないことがあります。')+'''
    <h2>全15回・3分の2の目安</h2>
    <table class="seo-table"><tr><th>欠席回数</th><th>出席率</th><th>単位認定（3分の2）</th></tr>
    <tr><td>0〜3回</td><td>80%以上</td><td>◎ 問題なし</td></tr>
    <tr><td>4回</td><td>約73%</td><td>○ ギリギリ圏内</td></tr>
    <tr><td>5回</td><td>約67%</td><td>△ ボーダー</td></tr>
    <tr><td>6回以上</td><td>60%以下</td><td>× 認定されない恐れ</td></tr></table>
    <p>正確な基準は各科目のシラバス・大学の学則をご確認ください。遅刻を欠席に換算する場合は <a href="/sims/chiko-soutai/">遅刻・早退→欠席換算</a>、目標からの逆算は <a href="/sims/hisho-nissu/">必要出席日数 計算</a>、要件チェックは <a href="/sims/shinkyu-hantei/">進級・卒業の出席条件 判定</a>、卒業単位は <a href="/sims/sotsugyo-tani/">卒業単位 計算</a> もどうぞ。</p>
    <h2>よくある質問</h2>'''+faq([
    ('大学は何回まで休める？','全15回なら、3分の2出席（10回）を満たすには欠席5回までが目安です。ただし科目により基準は異なります。'),
    ('出席点はどう影響する？','出席が成績評価に含まれる科目も多く、その場合は休むほど成績も下がります。シラバスで配点を確認しましょう。'),
    ('公欠（大学が認める欠席）は？','忌引きや大学行事などの公欠は欠席に数えない扱いが一般的ですが、手続きが必要です。学生課にご確認ください。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['大学の単位認定における出席要件（一般的な目安）']),
  js='''  function calc(){
    const t=Math.max(1,+$('total').value||15), a=Math.max(0,+$('abs').value||0);
    const fr=($('line').value||'2/3').split('/'), nu=+fr[0]||2, de=+fr[1]||3;
    const out=Math.max(0,t-a), rate=out/t*100;
    const need=Math.ceil(t*nu/de - 1e-9), allow=t-need, left=allow-a, ok=out>=need;
    $('sub').textContent=`全${t}回中 ${a}回欠席`;
    $('hantei').textContent=ok?'✅ 認定圏内':'⚠️ 危険';
    $('left').textContent=(left>=0?'あと'+left+'回':'超過'+(-left)+'回');
    $('need').textContent=need+'回以上';
    show();anim($('big'),0,rate,800,1);
    SHARE=`大学 出席率 計算、出席率${rate.toFixed(1)}%で${ok?'単位認定圏内✅':'危険⚠️'}でした🎓`;
  }''')

add(id='sotsugyo-tani', cat=TEACHER, emoji='📜',
  title='卒業単位 計算｜あと何単位？残りの学期で1学期いくつ取れば卒業？｜シミュラボ',
  desc='卒業に必要な総単位・取得済み単位・残りの学期数から、卒業まであと何単位必要か、1学期あたり何単位取ればよいか、進捗率を計算する大学生向け無料ツール。',
  ogtitle='卒業単位 計算｜あと何単位で卒業？', ogdesc='必要単位・取得単位・残り学期から卒業までの単位を計算。',
  h1='卒業単位 計算',
  lead='卒業まであと何単位？ 必要な総単位・取得済み単位・残りの学期から、卒業に必要な残り単位と「1学期あたり何単位取ればよいか」を計算します。履修計画づくりに。',
  inputs='''    <h2>📜 条件を入れる</h2>
    <div class="row"><div class="field"><label>卒業に必要な総単位 <span class="hint">（例:124）</span></label><input type="number" id="tot" value="124" min="1" inputmode="numeric"></div>
    <div class="field"><label>取得済みの単位 <span class="hint">（単位）</span></label><input type="number" id="got" value="60" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>残りの学期数 <span class="hint">（学期）</span></label><input type="number" id="sem" value="4" min="1" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">卒業単位を計算する</button>''',
  result='''      <div class="label">卒業まであと</div>
      <div class="big"><span id="big">0</span><span class="unit">単位</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">進捗率</div><div class="v accent" id="prog">—</div></div>
      <div class="stat"><div class="k">1学期あたり</div><div class="v" id="per">—</div></div>
      <div class="stat"><div class="k">卒業ライン</div><div class="v" id="line2">—</div></div></div>''',
  article=C('4年制大学の卒業には<b>124単位以上</b>が必要とされることが多いです（学部により異なる）。半期ごとに計画的に取得しないと、4年次に単位が足りず留年…ということも。残り学期での1学期あたり必要単位を把握しておきましょう。')+'''
    <h2>卒業単位の目安（124単位の場合）</h2>
    <table class="seo-table"><tr><th>学年</th><th>取得の目安（累計）</th></tr>
    <tr><td>1年終了</td><td>約36単位</td></tr>
    <tr><td>2年終了</td><td>約68単位</td></tr>
    <tr><td>3年終了</td><td>約100単位</td></tr>
    <tr><td>4年終了</td><td>124単位（卒業）</td></tr></table>
    <p>1学期あたり16〜18単位前後が標準ペースです。出席で単位を落とさないために <a href="/sims/daigaku-shusseki/">大学 出席率 計算</a>、進級要件は <a href="/sims/ryunen-tani/">進級・留年 単位ボーダー 判定</a>、成績は <a href="/sims/gpa/index.html">GPA計算</a> もどうぞ。</p>
    <h2>よくある質問</h2>'''+faq([
    ('大学の卒業単位は何単位？','多くの4年制大学で124単位以上です。学部・学科により必修/選択の内訳や総単位は異なります。'),
    ('1学期に何単位まで取れる？','履修上限（CAP制）を設ける大学が多く、1学期20〜24単位程度が上限のことが多いです。'),
    ('留年しないためには？','各学年の進級要件（必要単位数）を満たすことが必要です。早めに逆算して計画しましょう。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['大学設置基準（卒業要件124単位）']),
  js='''  function calc(){
    const tot=Math.max(1,+$('tot').value||124), got=Math.max(0,+$('got').value||60), sem=Math.max(1,+$('sem').value||4);
    const remain=Math.max(0,tot-got), per=Math.ceil(remain/sem), prog=got/tot*100;
    $('sub').textContent=`必要${tot}単位中 ${got}単位取得`;
    $('prog').textContent=prog.toFixed(0)+'%'; $('per').textContent=per+'単位/学期'; $('line2').textContent=tot+'単位';
    show();anim($('big'),0,remain,800);
    SHARE=`卒業単位 計算、あと${remain}単位（1学期あたり約${per}単位）でした📜`;
  }''')

add(id='ryunen-tani', cat=TEACHER, emoji='⚠️',
  title='進級・留年 単位ボーダー 判定｜必要単位に足りてる？留年チェック｜シミュラボ',
  desc='次の学年に上がるために必要な単位数と、取得（見込み）単位から、進級できるか・留年の危険があるか・あと何単位必要かを判定する大学生向け無料ツール。',
  ogtitle='進級・留年 判定｜単位は足りてる？', ogdesc='進級に必要な単位と取得見込みから、進級/留年を判定。',
  h1='進級・留年 単位ボーダー 判定',
  lead='「この単位数で進級できる？」を判定。進級（次学年へ上がる）に必要な単位と、取得・取得見込みの単位から、進級圏内か・あと何単位必要かをチェックします。',
  inputs='''    <h2>⚠️ 条件を入れる</h2>
    <div class="row"><div class="field"><label>進級に必要な単位 <span class="hint">（単位）</span></label><input type="number" id="need" value="30" min="0" inputmode="numeric"></div>
    <div class="field"><label>取得・取得見込みの単位 <span class="hint">（単位）</span></label><input type="number" id="got" value="24" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">進級できるか判定する</button>''',
  result='''      <div class="label">進級まで あと</div>
      <div class="big"><span id="big">0</span><span class="unit">単位</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">判定</div><div class="v accent" id="hantei">—</div></div>
      <div class="stat"><div class="k">必要単位</div><div class="v" id="need2">—</div></div>
      <div class="stat"><div class="k">取得見込み</div><div class="v" id="got2">—</div></div></div>''',
  article=C('大学には、次の学年へ上がるための「進級要件（必要単位数）」を定めている学部があります（特に医・歯・薬・理工系など）。要件を満たさないと、同じ学年をもう一度やり直す＝<b>留年（原級留置）</b>になります。')+'''
    <p>進級要件がない（累積で卒業単位を満たせばよい）大学・学部も多くあります。まずは自分の学部の進級要件を確認しましょう。要件がある場合、本ツールで「あと何単位で進級圏内か」をチェックできます。</p>
    <p>卒業までの総単位は <a href="/sims/sotsugyo-tani/">卒業単位 計算</a>、出席で単位を落とさないために <a href="/sims/daigaku-shusseki/">大学 出席率 計算</a> もあわせてどうぞ。</p>
    <h2>よくある質問</h2>'''+faq([
    ('進級要件はどの大学にもある？','いいえ。学部によります。医歯薬・理工系などで設けられることが多く、要件がない大学・学部もあります。'),
    ('留年するとどうなる？','同じ学年をやり直します。学費が追加でかかる、就活の時期がずれるなどの影響があります。'),
    ('必要単位が分からない','履修要項・学生便覧に記載があります。不明なら学生課・教務課に確認しましょう。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['大学の進級要件（原級留置）の一般的な考え方']),
  js='''  function calc(){
    const need=Math.max(0,+$('need').value||30), got=Math.max(0,+$('got').value||24);
    const short=Math.max(0,need-got), ok=got>=need;
    $('sub').textContent=`進級要件${need}単位・取得見込み${got}単位`;
    $('hantei').textContent=ok?'✅ 進級圏内':'⚠️ 留年注意';
    $('need2').textContent=need+'単位'; $('got2').textContent=got+'単位';
    show();anim($('big'),0,short,700);
    SHARE=`進級・留年 判定、あと${short}単位で${ok?'進級圏内✅':'留年注意⚠️'}でした⚠️`;
  }''')

# ============================================================
# 守護霊クラスタ（uranai・生年月日シード）
# ============================================================
add(id='shugo-animal', cat=URANAI, emoji='🐺',
  title='守護動物診断｜あなたのスピリットアニマルは？生年月日で占う｜シミュラボ',
  desc='生年月日から、あなたを守り導くとされる守護動物（スピリットアニマル）を占う無料のエンタメ占い。動物ごとの性質や、守られている運勢のヒントが分かります。守護霊診断とあわせて。',
  ogtitle='守護動物診断｜スピリットアニマルは？', ogdesc='生年月日からあなたの守護動物（スピリットアニマル）を占う。',
  h1='守護動物（スピリットアニマル）診断',
  lead='あなたのそばには、どんな守護動物がいるのでしょう。生年月日から、あなたを守り導くとされるスピリットアニマルを占い、その性質や運勢のヒントを表示します。',
  inputs=BD.replace('__H__','🐺 生年月日を入れてね'),
  result=URES.replace('__L__','あなたの守護動物は'),
  visual='',
  article=C('スピリットアニマル（守護動物）は、ネイティブアメリカンなどの文化に見られる、その人に寄り添い導くとされる象徴的な動物のこと。動物ごとに象徴する性質があり、自分の強みや大切にすべきことを知るきっかけとして親しまれています。')+'''
    <h2>守護動物とその象徴</h2>
    <table class="seo-table"><tr><th>動物</th><th>象徴する力</th></tr>
    <tr><td>🐺 狼</td><td>独立心・直感・仲間との絆</td></tr>
    <tr><td>🦅 鷲</td><td>広い視野・決断力</td></tr>
    <tr><td>🐻 熊</td><td>包容力・芯の強さ</td></tr>
    <tr><td>🐉 龍</td><td>強運・飛躍</td></tr>
    <tr><td>🦊 狐</td><td>機転・知恵</td></tr>
    <tr><td>🐢 亀</td><td>忍耐・長寿</td></tr></table>
    <p>自分を守る存在をもっと知りたい方は、<a href="/sims/shugorei/">守護霊診断</a>・<a href="/sims/shugoshin/">守護神診断</a>・<a href="/sims/power-stone/">守護のパワーストーン診断</a>もあわせてどうぞ。</p>
    <div class="note"><strong>※エンタメ占いです。</strong>深い悩みや本格的な鑑定は、電話占いなどプロにご相談を。</div>
    <h2>よくある質問</h2>'''+faq([
    ('スピリットアニマルとは？','その人に寄り添い導くとされる象徴的な動物のこと。性格タイプ診断のように楽しめます。'),
    ('守護動物は変わる？','人生の段階で寄り添う動物が変わるという考え方もあります。時期をおいて占い直すのも一興です。'),
    ('本格的に視てもらいたい','霊感のある占い師に電話で相談する方法もあります（下の案内をご参照ください）。'),
    ('データは送信されますか？','いいえ。占いはすべてブラウザ内で完結します。')])+REF(['スピリットアニマル（象徴動物）の一般的な考え方']),
  js=useed_js(
    [['🐺','狼（ウルフ）','独立心と直感の守り。孤高に道を切り開くあなたを支えます。'],
     ['🦅','鷲（イーグル）','高い視点と決断力の守り。大局を見通し、チャンスを掴みます。'],
     ['🐻','熊（ベア）','包容力と芯の強さの守り。いざという時の底力を与えます。'],
     ['🐬','イルカ（ドルフィン）','調和と癒やしの守り。人との縁を豊かにしてくれます。'],
     ['🦊','狐（フォックス）','機転と知恵の守り。ピンチを賢く切り抜ける力に。'],
     ['🐢','亀（タートル）','忍耐と長寿の守り。着実な歩みを後押しします。'],
     ['🐉','龍（ドラゴン）','強運と飛躍の守り。大きなチャンスを呼び込みます。'],
     ['🦋','蝶（バタフライ）','変化と成長の守り。新しい自分へと導きます。']],
    '守護動物診断、私のスピリットアニマルは「{n}」でした🐺 あなたは？'))

add(id='shugorei-level', cat=URANAI, emoji='🛡️',
  title='守護霊の強さ診断｜あなたの守護霊パワーはレベルいくつ？｜シミュラボ',
  desc='生年月日から、あなたを守る守護霊の「強さ（レベル）」とタイプを占う無料のエンタメ占い。守護霊パワーのランク（SS〜C）や守られている運勢が分かります。守護霊診断とあわせて。',
  ogtitle='守護霊の強さ診断｜守護霊レベルは？', ogdesc='生年月日から守護霊の強さ（レベル）とタイプを占う。',
  h1='守護霊の強さ（レベル）診断',
  lead='あなたを守る守護霊は、どのくらい強い存在なのでしょう。生年月日から守護霊パワーをレベル（pt）とランクで表示し、守護霊のタイプと運勢のヒントを占います。',
  inputs=BD.replace('__H__','🛡️ 生年月日を入れてね'),
  result='''      <div class="label">あなたの守護霊レベル</div>
      <div class="big"><span id="big">0</span><span class="unit">pt</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">ランク</div><div class="v accent" id="rank">—</div></div>
      <div class="stat"><div class="k">守護霊タイプ</div><div class="v" id="type">—</div></div>
      <div class="stat"><div class="k">守護の傾向</div><div class="v" id="adv">—</div></div></div>''',
  visual='',
  article=C('守護霊は、あなたを陰ながら見守り支えてくれるとされるスピリチュアルな存在。この診断では、生年月日をもとに守護霊の「強さ」をレベル（pt）とランク（SS〜C）で表し、守護霊のタイプを占います。エンタメとしてお楽しみください。')+'''
    <h2>守護霊レベルのランク</h2>
    <table class="seo-table"><tr><th>ランク</th><th>目安（pt）</th></tr>
    <tr><td>SS</td><td>90pt以上（非常に強い守り）</td></tr>
    <tr><td>S</td><td>80〜89pt</td></tr>
    <tr><td>A</td><td>70〜79pt</td></tr>
    <tr><td>B</td><td>60〜69pt</td></tr>
    <tr><td>C</td><td>59pt以下</td></tr></table>
    <p>守護霊のタイプそのものは <a href="/sims/shugorei/">守護霊診断</a>、守護動物は <a href="/sims/shugo-animal/">守護動物診断</a>、守り石は <a href="/sims/power-stone/">守護のパワーストーン診断</a> でどうぞ。</p>
    <div class="note"><strong>※エンタメ占いです。</strong>深い悩みや本格的な鑑定は、電話占いなどプロにご相談を。</div>
    <h2>よくある質問</h2>'''+faq([
    ('レベルが低いと守られてない？','いいえ。レベルはエンタメの演出です。強さに関わらず守護霊は見守ってくれるという考え方でお楽しみください。'),
    ('同じ生年月日なら結果は同じ？','はい。生年月日から決定論的に算出しているため、いつ占っても同じ結果になります。'),
    ('本格的に視てもらいたい','霊感のある占い師に電話で相談する方法もあります（下の案内をご参照ください）。'),
    ('データは送信されますか？','いいえ。占いはすべてブラウザ内で完結します。')])+REF(['守護霊（スピリチュアルな概念）の一般的な解説']),
  js='  const TYPES='+json.dumps([
     ['🛡️','守護の盾型','ピンチのときほど守りが固くなる、頼れる守護霊です。'],
     ['🔥','闘志の炎型','勝負どきに力をくれる、情熱的な守護霊です。'],
     ['🌊','癒やしの水型','心を穏やかに整える、やさしい守護霊です。'],
     ['🌟','導きの星型','迷ったとき正しい道を照らす守護霊です。'],
     ['🌙','神秘の月型','直感やご縁を高める、スピリチュアルな守護霊です。'],
     ['🌈','幸運の虹型','ピンチをチャンスに変える、強運の守護霊です。']],ensure_ascii=False)+''';
  function h(s){let x=2166136261;for(let i=0;i<s.length;i++){x^=s.charCodeAt(i);x=Math.imul(x,16777619);}return x>>>0;}
  function calc(){const bd=$('bd').value;if(!bd){alert('生年月日を入れてね');return;}
    const x=h(bd), score=40+x%60, t=TYPES[x%TYPES.length];
    const rank=score>=90?'SS':score>=80?'S':score>=70?'A':score>=60?'B':'C';
    $('sub').textContent=t[0]+' '+t[1]+'のあなた';
    $('rank').textContent=rank; $('type').textContent=t[0]+' '+t[1]; $('adv').textContent=t[2];
    show();anim($('big'),0,score,900);
    SHARE=`守護霊の強さ診断、私の守護霊レベルは${score}pt（ランク${rank}・${t[1]}）でした🛡️`;
  }''')

add(id='power-stone', cat=URANAI, emoji='💎',
  title='守護のパワーストーン診断｜あなたを守る石は？生年月日で占う｜シミュラボ',
  desc='生年月日から、あなたを守り運気を高めるとされるパワーストーン（守り石）を占う無料のエンタメ占い。石ごとの意味や、守られている運勢のヒントが分かります。守護霊診断とあわせて。',
  ogtitle='守護のパワーストーン診断｜守り石は？', ogdesc='生年月日からあなたの守護パワーストーンを占う。',
  h1='守護のパワーストーン診断',
  lead='あなたを守り、運気を高めてくれるパワーストーンは何でしょう。生年月日から、あなたの「守り石」を占い、その石が持つ意味や運勢のヒントを表示します。',
  inputs=BD.replace('__H__','💎 生年月日を入れてね'),
  result=URES.replace('__L__','あなたの守り石は'),
  visual='',
  article=C('パワーストーンは、古くから世界各地で「お守り」として大切にされてきた天然石。石ごとに象徴する意味（癒やし・金運・厄除けなど）があり、身につけることで前向きになれるお守りとして親しまれています。')+'''
    <h2>パワーストーンの意味</h2>
    <table class="seo-table"><tr><th>石</th><th>象徴する運</th></tr>
    <tr><td>💎 水晶</td><td>浄化・万能・全体運</td></tr>
    <tr><td>💜 アメジスト</td><td>癒やし・直感</td></tr>
    <tr><td>🌸 ローズクォーツ</td><td>恋愛・人間関係</td></tr>
    <tr><td>🐯 タイガーアイ</td><td>金運・決断</td></tr>
    <tr><td>🖤 オニキス</td><td>厄除け・意志</td></tr>
    <tr><td>💚 翡翠</td><td>健康・長寿</td></tr></table>
    <p>ほかの守りも気になる方は、<a href="/sims/shugorei/">守護霊診断</a>・<a href="/sims/shugo-animal/">守護動物診断</a>・<a href="/sims/aura-color/">オーラカラー診断</a>もあわせてどうぞ。</p>
    <div class="note"><strong>※エンタメ占いです。</strong>深い悩みや本格的な鑑定は、電話占いなどプロにご相談を。</div>
    <h2>よくある質問</h2>'''+faq([
    ('パワーストーンに効果はある？','科学的な裏づけはありません。前向きになれるお守りとしてお楽しみください。'),
    ('複数持ってもいい？','組み合わせて持つ人も多いです。まずはこの診断の石をきっかけにしてみてください。'),
    ('本格的に視てもらいたい','運勢や相性を詳しく鑑定してほしいときは、電話占いなどでプロに相談する方法もあります。'),
    ('データは送信されますか？','いいえ。占いはすべてブラウザ内で完結します。')])+REF(['パワーストーン（天然石）の一般的な意味']),
  js=useed_js(
    [['💎','水晶（クリスタル）','浄化と万能の守り。全体運を底上げしてくれます。'],
     ['💜','アメジスト','癒やしと直感の守り。心の安定をもたらします。'],
     ['🌸','ローズクォーツ','愛と人間関係の守り。優しさと魅力を高めます。'],
     ['🐯','タイガーアイ','金運と決断の守り。ここぞの勝負を後押しします。'],
     ['💚','翡翠（ヒスイ）','健康と長寿の守り。穏やかな幸運を呼びます。'],
     ['🔵','ラピスラズリ','幸運と知性の守り。道を切り開く力になります。'],
     ['🖤','オニキス','厄除けと意志の守り。邪気からあなたを守ります。'],
     ['🌊','ターコイズ','旅と成功の守り。挑戦するあなたを守護します。']],
    '守護のパワーストーン診断、私の守り石は「{n}」でした💎 あなたは？'))

# ============================================================
# 車 vs 電車クラスタ（car）
# ============================================================
add(id='shinkansen-car', cat=CAR, emoji='🚄',
  title='新幹線 vs 車 どっちが安い｜帰省・長距離、人数別に比較｜シミュラボ',
  desc='距離・人数・燃費・ガソリン代・高速代・新幹線運賃から、帰省や長距離移動で車と新幹線のどちらが安いか、損益分岐の人数を計算する無料ツール。人数が多いほど車が有利。',
  ogtitle='新幹線 vs 車 どっちが安い？', ogdesc='距離・人数から帰省の車と新幹線の費用を比較、損益分岐人数も。',
  h1='新幹線 vs 車 どっちが安い？',
  lead='帰省や旅行の長距離移動、車と新幹線どっちが安い？ 距離・人数・燃費・高速代・新幹線運賃から往復費用を比較し、「何人以上なら車がお得か」も計算します。',
  inputs='''    <h2>🚄 条件を入れる（片道ベース）</h2>
    <div class="row"><div class="field"><label>片道の距離 <span class="hint">（km）</span></label><input type="number" id="km" value="400" min="1" inputmode="numeric"></div>
    <div class="field"><label>移動する人数 <span class="hint">（人）</span></label><input type="number" id="nin" value="2" min="1" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>燃費 <span class="hint">（km/L）</span></label><input type="number" id="nenpi" value="15" min="1" inputmode="decimal"></div>
    <div class="field"><label>ガソリン <span class="hint">（円/L）</span></label><input type="number" id="gas" value="170" min="1" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>高速代（片道） <span class="hint">（円）</span></label><input type="number" id="kohi" value="8000" min="0" inputmode="numeric"></div>
    <div class="field"><label>新幹線（片道・1人） <span class="hint">（円）</span></label><input type="number" id="shin" value="11000" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">どっちが安いか計算する</button>''',
  result='''      <div class="label">費用の差（往復）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">車（往復）</div><div class="v accent" id="carv">—</div></div>
      <div class="stat"><div class="k">新幹線（往復）</div><div class="v" id="trainv">—</div></div>
      <div class="stat"><div class="k">損益分岐</div><div class="v" id="be">—</div></div></div>''',
  article=C('車は高速代とガソリン代が「人数に関わらず一定」なのに対し、新幹線は「1人ずつ運賃がかかる」のが最大の違い。だから<b>人数が多いほど車が有利</b>になります。1〜2人なら新幹線、家族4人なら車が安い、という分かれ方が典型です。')+'''
    <h2>車と新幹線の費用のしくみ</h2>
    <ul>
    <li><b>車</b>＝（距離 ÷ 燃費 × ガソリン単価）＋ 高速代（人数に関係なく一定）</li>
    <li><b>新幹線</b>＝ 片道運賃 × 人数（人数に比例して増える）</li>
    </ul>
    <p>※車は駐車場代や疲労、新幹線は乗換や時間も加味して選びましょう。通勤の比較は <a href="/sims/tsukin-car/index.html">車通勤 vs 電車通勤</a>、飛行機との比較は <a href="/sims/lcc-shinkansen/index.html">LCC vs 新幹線</a>、ガソリン代は <a href="/sims/gasolinedai/index.html">ガソリン代計算</a> もどうぞ。</p>
    <h2>よくある質問</h2>'''+faq([
    ('何人なら車が安い？','距離や高速代によりますが、目安は2〜3人以上。本ツールが損益分岐の人数を計算します。'),
    ('高速代はどう調べる？','NEXCOの料金検索やカーナビ、地図アプリの経路検索で片道料金を確認できます。ETC割引も考慮を。'),
    ('駐車場代は？','帰省先や旅行先の駐車場代がかかる場合は、車側にその分を足して考えてください。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['交通費の比較（一般的な計算方法）']),
  js='''  function calc(){
    const km=Math.max(1,+$('km').value||400), nin=Math.max(1,+$('nin').value||2);
    const nenpi=Math.max(1,+$('nenpi').value||15), gas=Math.max(1,+$('gas').value||170);
    const kohi=Math.max(0,+$('kohi').value||8000), shin=Math.max(0,+$('shin').value||11000);
    const carOne=km/nenpi*gas+kohi, car=carOne*2, train=shin*nin*2;
    const diff=Math.abs(car-train), carCheaper=car<=train;
    const be=shin>0?Math.max(1,Math.ceil(car/(shin*2))):0;
    $('sub').textContent=carCheaper?`車のほうが ${num(diff)}円 お得`:`新幹線のほうが ${num(diff)}円 お得`;
    $('carv').textContent=num(car)+'円'; $('trainv').textContent=num(train)+'円'; $('be').textContent=be+'人以上で車';
    show();anim($('big'),0,diff,800);
    SHARE=`新幹線 vs 車、${km}km×${nin}人は${carCheaper?'車':'新幹線'}が${num(diff)}円お得でした🚄🚗`;
  }''')

add(id='teiki-kaisu', cat=CAR, emoji='🎫',
  title='定期券 vs 都度払い どっちが得｜通勤日数で損益分岐を計算｜シミュラボ',
  desc='片道運賃・1ヶ月の通勤日数・定期代から、定期券と都度払い（ICカード）のどちらが得か、月何日乗れば定期がお得になるか（損益分岐日数）を計算する無料ツール。',
  ogtitle='定期券 vs 都度払い どっちが得？', ogdesc='通勤日数と定期代から、定期券が得か損益分岐日数を計算。',
  h1='定期券 vs 都度払い どっちが得？',
  lead='テレワークが増えて「定期券、もったいないかも？」という人へ。片道運賃・月の通勤日数・定期代から、定期と都度払いのどちらが得か、損益分岐の日数を計算します。',
  inputs='''    <h2>🎫 条件を入れる</h2>
    <div class="row"><div class="field"><label>片道の運賃 <span class="hint">（円）</span></label><input type="number" id="one" value="320" min="0" inputmode="numeric"></div>
    <div class="field"><label>1ヶ月の通勤日数 <span class="hint">（日）</span></label><input type="number" id="days" value="20" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>1ヶ月の定期代 <span class="hint">（円）</span></label><input type="number" id="teiki" value="10500" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">どっちが得か計算する</button>''',
  result='''      <div class="label">1ヶ月の差額</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">都度払い</div><div class="v accent" id="tsudov">—</div></div>
      <div class="stat"><div class="k">定期代</div><div class="v" id="teikiv">—</div></div>
      <div class="stat"><div class="k">損益分岐</div><div class="v" id="be">—</div></div></div>''',
  article=C('定期券は「一定額で乗り放題」なので、乗る日数が多いほど得。逆に<b>テレワークなどで通勤日数が少ないと、都度払い（ICカード）のほうが安くなる</b>ことがあります。損益分岐は「定期代 ÷ 往復運賃」で、その日数以上乗れば定期がお得です。')+'''
    <h2>損益分岐の考え方</h2>
    <ul>
    <li><b>都度払い</b>＝ 片道運賃 × 2 × 通勤日数</li>
    <li><b>損益分岐日数</b>＝ 定期代 ÷（片道運賃 × 2）</li>
    <li>通勤日数がこの日数より多ければ<b>定期がお得</b>、少なければ都度払いがお得</li>
    </ul>
    <p>※定期は休日の私用にも使え、区間内乗り降り自由という利点もあります。車通勤との比較は <a href="/sims/tsukin-car/index.html">車通勤 vs 電車通勤</a> もどうぞ。</p>
    <h2>よくある質問</h2>'''+faq([
    ('週何日出社なら定期が得？','片道320円・定期10,500円なら損益分岐は約17日/月＝週4日程度。週3日以下なら都度払いが得な場合が多いです。'),
    ('回数券は？','回数券は都度払いより少し割安なことがありますが、廃止する路線も増えています。ICのポイント還元も比較を。'),
    ('3ヶ月・6ヶ月定期は？','長期定期はさらに割安です。継続利用が確実なら長期のほうがお得になります。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['定期券と都度払いの損益分岐（一般的な計算）']),
  js='''  function calc(){
    const one=Math.max(0,+$('one').value||320), days=Math.max(0,+$('days').value||20), teiki=Math.max(0,+$('teiki').value||10500);
    const tsudo=one*2*days, diff=Math.abs(tsudo-teiki), teikiToku=teiki<=tsudo;
    const be=one>0?Math.ceil(teiki/(one*2)):0;
    $('sub').textContent=teikiToku?`定期のほうが 月${num(diff)}円 お得`:`都度払いのほうが 月${num(diff)}円 お得`;
    $('tsudov').textContent=num(tsudo)+'円'; $('teikiv').textContent=num(teiki)+'円'; $('be').textContent='月'+be+'日以上で定期';
    show();anim($('big'),0,diff,700);
    SHARE=`定期 vs 都度払い、月${days}日通勤なら${teikiToku?'定期':'都度払い'}が月${num(diff)}円お得でした🎫`;
  }''')

add(id='taxi-densha', cat=CAR, emoji='🚕',
  title='タクシー vs 電車 どっちが得｜距離・人数・深夜割増で比較｜シミュラボ',
  desc='距離・人数・電車運賃・タクシーの初乗り/加算・深夜割増から、タクシーと電車のどちらが得かを概算する無料ツール。人数で割ればタクシーが得なことも。',
  ogtitle='タクシー vs 電車 どっちが得？', ogdesc='距離・人数・深夜割増からタクシーと電車の料金を概算比較。',
  h1='タクシー vs 電車 どっちが得？',
  lead='「この距離ならタクシーでもいい？」を概算。距離・人数・電車運賃・タクシー料金・深夜割増から、どちらが得か、タクシーは1人あたりいくらかを計算します。',
  inputs='''    <h2>🚕 条件を入れる</h2>
    <div class="row"><div class="field"><label>距離 <span class="hint">（km）</span></label><input type="number" id="km" value="5" min="0" step="0.5" inputmode="decimal"></div>
    <div class="field"><label>人数 <span class="hint">（人）</span></label><input type="number" id="nin" value="3" min="1" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>電車運賃（1人） <span class="hint">（円）</span></label><input type="number" id="train" value="250" min="0" inputmode="numeric"></div>
    <div class="field"><label>深夜割増</label><select id="wari"><option value="0" selected>なし（昼）</option><option value="0.2">2割増（深夜）</option></select></div></div>
    <div class="row"><div class="field"><label>タクシー初乗り <span class="hint">（円）</span></label><input type="number" id="hatsu" value="500" min="0" inputmode="numeric"></div>
    <div class="field"><label>加算 <span class="hint">（円/km・概算）</span></label><input type="number" id="per" value="350" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">どっちが得か計算する</button>''',
  result='''      <div class="label">料金の差</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">タクシー（概算）</div><div class="v accent" id="taxiv">—</div></div>
      <div class="stat"><div class="k">電車（人数分）</div><div class="v" id="trainv">—</div></div>
      <div class="stat"><div class="k">タクシー1人あたり</div><div class="v" id="head">—</div></div></div>''',
  article=C('タクシーは「1台の料金をみんなで割れる」のが強み。<b>人数が多いほど1人あたりが安くなり</b>、短距離・複数人なら電車より得なこともあります。深夜は電車が終わっている・割増になる点も判断材料です。')+'''
    <h2>タクシー料金の目安</h2>
    <ul>
    <li><b>タクシー</b>≒（初乗り ＋ 距離 × 加算/km）×（深夜は約1.2倍）</li>
    <li><b>電車</b>＝ 運賃 × 人数</li>
    <li>短距離＋複数人＝タクシーが得になりやすい／長距離＝電車が得</li>
    </ul>
    <div class="note"><strong>※料金は概算です。</strong>実際の初乗り距離・加算距離・割増率は地域・会社で異なります。正確な料金は配車アプリの見積もりをご確認ください。</div>
    <p>長距離の比較は <a href="/sims/shinkansen-car/">新幹線 vs 車</a>、通勤は <a href="/sims/tsukin-car/index.html">車通勤 vs 電車通勤</a> もどうぞ。</p>
    <h2>よくある質問</h2>'''+faq([
    ('何人ならタクシーが得？','短距離なら3〜4人で割ると電車並みになることも。本ツールで1人あたりを確認できます。'),
    ('深夜料金はどれくらい？','多くの地域で22時〜翌5時ごろに約2割増になります。終電後は有力な選択肢です。'),
    ('料金は正確？','初乗り・加算は地域差が大きいため概算です。正確には配車アプリの事前見積もりをご利用ください。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])+REF(['タクシー運賃（初乗り・加算・深夜割増の一般的な仕組み）']),
  js='''  function calc(){
    const km=Math.max(0,+$('km').value||5), nin=Math.max(1,+$('nin').value||1);
    const hatsu=Math.max(0,+$('hatsu').value||500), per=Math.max(0,+$('per').value||350), wari=+$('wari').value||0;
    const train1=Math.max(0,+$('train').value||250);
    const taxi=Math.round((hatsu+km*per)*(1+wari)), train=train1*nin;
    const diff=Math.abs(taxi-train), taxiCheaper=taxi<=train, head=Math.round(taxi/nin);
    $('sub').textContent=taxiCheaper?`タクシーのほうが ${num(diff)}円 お得`:`電車のほうが ${num(diff)}円 お得`;
    $('taxiv').textContent='約'+num(taxi)+'円'; $('trainv').textContent=num(train)+'円'; $('head').textContent='約'+num(head)+'円';
    show();anim($('big'),0,diff,700);
    SHARE=`タクシー vs 電車、${km}km×${nin}人は${taxiCheaper?'タクシー':'電車'}が${num(diff)}円お得でした🚕`;
  }''')

# ============================================================
# おじさん・おばさん・若者度クラスタ（life・クイズ）
# ============================================================
_oji_in,_oji_res,_oji_js = quiz(
  ['若い芸能人やアイドルの名前が出てこない','立ち上がるとき「よっこいしょ」と言う','LINEやメールで句読点をきっちり打つ','新しいアプリを覚えるのが億劫','「最近の若い子は」と思うことがある','健康や血圧・健康診断が気になり始めた','昔の武勇伝・自慢話をしがち','絵文字より「(笑)」を使いがち','脂っこいもの・濃い味がきつくなった','スマホの文字を大きめに設定している'],
  [[20,'まだまだ若手','おじさん度は低め。フレッシュな感性を大切に。'],[45,'おじさん予備軍','油断するとおじさん化。新しいものにも触れてみて。'],[70,'立派なおじさん','安定のおじさん力。渋さは武器にもなります。'],[100,'大ベテランおじさん','貫禄十分。若い人へのリスペクトも忘れずに。']],
  'おじさん度診断、私のおじさん度は{p}%（{t}）でした🧔 あなたは？','おじさん度診断','🧔')
add(id='ojisan-do', cat=LIFE, emoji='🧔',
  title='おじさん度診断｜あなたのおじさん化、何％進んでる？チェック｜シミュラボ',
  desc='10個のあるあるチェックに答えるだけで、あなたの「おじさん度」を％で診断する無料ツール。おじさん化のサインをセルフチェック。精神年齢診断とあわせてどうぞ。',
  ogtitle='おじさん度診断｜おじさん化は何％？', ogdesc='10のあるあるチェックであなたのおじさん度を％診断。',
  h1='おじさん度診断',
  lead='気づかぬうちに進む「おじさん化」。10個のあるあるチェックに答えるだけで、あなたのおじさん度を％で診断します。当てはまるものにチェックを入れてください。',
  inputs=_oji_in, result=_oji_res.replace('__L__','あなたのおじさん度'), visual='',
  article=C('「おじさん度」は、加齢とともに出やすくなる言動・習慣のあるあるチェックです。数が多いほどおじさん度が高め。あくまでエンタメですが、若々しさを保つヒントにもなります。')+'''
    <p>「おじさん化」は年齢そのものより<b>習慣や気持ちの持ちよう</b>で進みます。新しいことに触れる、姿勢を正す、口ぐせを見直すだけでも印象は変わります。</p>
    <p>女性版は <a href="/sims/obasan-do/">おばさん度診断</a>、逆に若さを測るなら <a href="/sims/wakamono-do/">若者度（Z世代度）診断</a>、心の年齢は <a href="/sims/mental-age/index.html">精神年齢診断</a> でどうぞ。</p>
    <h2>よくある質問</h2>'''+faq([
    ('おじさん度が高いと悪いこと？','いいえ。渋みや落ち着きは魅力にもなります。エンタメとして楽しみつつ、若々しさのヒントにしてください。'),
    ('何歳から「おじさん」？','明確な基準はありません。年齢より言動や気持ちの持ちようが大きく影響します。'),
    ('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')])+REF(['加齢に伴う行動変化（一般的なあるある）']),
  js=_oji_js)

_oba_in,_oba_res,_oba_js = quiz(
  ['スーパーの試食をつい受け取る','バッグに飴やのど飴が入っている','「あら」「まあ」が口ぐせ','店員さんや近所の人によく話しかける','待ち時間につい世間話をしてしまう','若い人に「これ食べる?」とあげたくなる','記念写真で真ん中に行きがち','服は見た目より「動きやすさ」重視','値段のシールをつい見て比較する','電車で席が空くとすぐ座りたくなる'],
  [[20,'まだまだお姉さん','おばさん度は低め。フレッシュさをキープ。'],[45,'おばさん予備軍','ちょいちょい出てるかも。楽しみつつ意識してみて。'],[70,'立派なおばさん','安定のおばさん力。親しみやすさは大きな魅力。'],[100,'大ベテランおばさん','貫禄と包容力たっぷり。周りに愛されるタイプ。']],
  'おばさん度診断、私のおばさん度は{p}%（{t}）でした👜 あなたは？','おばさん度診断','👜')
add(id='obasan-do', cat=LIFE, emoji='👜',
  title='おばさん度診断｜あなたのおばさん度、何％？あるあるチェック｜シミュラボ',
  desc='10個のあるあるチェックに答えるだけで、あなたの「おばさん度」を％で診断する無料ツール。おばさんあるあるをセルフチェック。精神年齢診断とあわせてどうぞ。',
  ogtitle='おばさん度診断｜おばさん度は何％？', ogdesc='10のあるあるチェックであなたのおばさん度を％診断。',
  h1='おばさん度診断',
  lead='親しみやすさの裏返し？「おばさん度」を10個のあるあるチェックで診断します。当てはまるものにチェックを入れると、あなたのおばさん度を％で表示します。',
  inputs=_oba_in, result=_oba_res.replace('__L__','あなたのおばさん度'), visual='',
  article=C('「おばさん度」は、年齢を重ねるほど出やすい親しみやすさや生活感のあるあるチェックです。数が多いほどおばさん度が高め。ネガティブに捉えず、包容力や気さくさの表れとして楽しんでください。')+'''
    <p>「おばさんっぽさ」は多くが<b>気さくさ・面倒見のよさ</b>の裏返し。魅力でもあります。気になる人は、姿勢や装いを少し意識するだけで印象が変わります。</p>
    <p>男性版は <a href="/sims/ojisan-do/">おじさん度診断</a>、若さを測るなら <a href="/sims/wakamono-do/">若者度（Z世代度）診断</a>、心の年齢は <a href="/sims/mental-age/index.html">精神年齢診断</a> でどうぞ。</p>
    <h2>よくある質問</h2>'''+faq([
    ('おばさん度が高いと悪いこと？','いいえ。気さくさや面倒見のよさは大きな魅力です。エンタメとしてお楽しみください。'),
    ('何歳から「おばさん」？','明確な基準はありません。年齢より言動や気持ちが影響します。'),
    ('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')])+REF(['加齢に伴う行動変化（一般的なあるある）']),
  js=_oba_js)

_waka_in,_waka_res,_waka_js = quiz(
  ['動画はほぼ倍速で見る','「タイパ（時間対効果）」を重視する','調べ物はGoogleよりSNS（Instagram/TikTok）','電話は苦手、連絡は文字派','サブスクを3つ以上使っている','「了解」より「り」「おk」で返すことがある','支払いは現金よりキャッシュレス派','テレビよりYouTube・配信をよく見る','知らない言葉はすぐスマホで調べる','リアタイ視聴より見逃し・アーカイブ派'],
  [[20,'昭和マインド','若者度は低め。マイペースが一番です。'],[45,'おじおば寄り','少し時代とズレ気味かも。たまに若者文化に触れてみて。'],[70,'イマドキ寄り','なかなかの若者度。感度は高めです。'],[100,'ドンピシャZ世代','完全にイマドキ。トレンドの最前線を走っています。']],
  '若者度診断、私の若者度は{p}%（{t}）でした📱 あなたは？','若者度（Z世代度）診断','📱')
add(id='wakamono-do', cat=LIFE, emoji='📱',
  title='若者度診断｜あなたのZ世代度は何％？イマドキ度チェック｜シミュラボ',
  desc='10個のイマドキ行動チェックで、あなたの「若者度（Z世代度）」を％診断する無料ツール。昭和マインド〜ドンピシャZ世代まで判定。おじさん・おばさん度診断とあわせて。',
  ogtitle='若者度診断｜あなたのZ世代度は？', ogdesc='10のイマドキ行動チェックで若者度（Z世代度）を％診断。',
  h1='若者度（Z世代度）診断',
  lead='あなたはどれだけイマドキ？ タイパ・倍速・SNS検索など10個の行動チェックで、若者度（Z世代度）を％診断します。当てはまるものにチェックを入れてください。',
  inputs=_waka_in, result=_waka_res.replace('__L__','あなたの若者度'), visual='',
  article=C('「若者度（Z世代度）」は、いまの若い世代に多い価値観・行動のチェックです。タイパ重視、SNSで検索、キャッシュレス、倍速視聴…数が多いほどイマドキ度が高めになります。')+'''
    <p>世代の違いはどちらが良い・悪いではなく<b>環境の違い</b>。相手の世代の行動を知ると、家庭や職場のコミュニケーションもスムーズになります。</p>
    <p>反対に測るなら <a href="/sims/ojisan-do/">おじさん度診断</a>・<a href="/sims/obasan-do/">おばさん度診断</a>、心の年齢は <a href="/sims/mental-age/index.html">精神年齢診断</a> でどうぞ。</p>
    <h2>よくある質問</h2>'''+faq([
    ('Z世代って何歳くらい？','おおむね1990年代後半〜2010年代初め生まれを指すことが多いですが、明確な定義はありません。'),
    ('若者度が低いとダメ？','いいえ。世代ごとの良さがあります。エンタメとして楽しみ、世代間理解のきっかけにしてください。'),
    ('データは送信されますか？','いいえ。診断はすべてブラウザ内で完結します。')])+REF(['世代（Z世代など）ごとの行動傾向（一般的な解説）']),
  js=_waka_js)

if __name__=='__main__':
    write_all(SIMS)
    print(f'boost done. {len(SIMS)} sims.')
