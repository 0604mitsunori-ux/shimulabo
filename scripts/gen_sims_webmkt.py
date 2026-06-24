# -*- coding: utf-8 -*-
"""シミュラボ：Webマーケ計算10本＋LLMO対応度診断1本（既存 slug=marketing に追加）。
CTA（AIMA5実行型LLMO）は patch_llmo_cta.py で別途挿入（marketingカテゴリ自動検出）。
gen_sims_tool の TPL/viz を流用（try無し）。

seo_internal.py / gen_images.py のauto-importに 'gen_sims_webmkt' を追加して使う。
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims11 import faq
from gen_sims_tool import TPL, viz
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CAT = 'マーケティング'
SIMS=[]
def add(**k):
    k.setdefault('visual','')
    SIMS.append(k)

def art(note, body, faqs):
    return ('    <div class="note"><strong>計算式</strong><br>'+note+'</div>\n    <h2>'+body[0]+'</h2>\n    <p>'+body[1]+'</p>\n    <h2>よくある質問</h2>'+faq(faqs))

# ============================================================
# 1. コンバージョン率（CVR）計算機（コンバージョン率 4200/KD4）
# ============================================================
add(id='cvr-keisan', emoji='🎯', cat=CAT,
  title='コンバージョン率（CVR）計算機｜CV数とアクセスから一発計算｜シミュラボ',
  desc='サイトのアクセス数（セッション）とコンバージョン数から、コンバージョン率（CVR）を計算する無料ツール。100アクセスあたりのCVや、目標CVに必要なアクセス数も分かります。',
  ogtitle='コンバージョン率（CVR）計算機', ogdesc='アクセス数とCV数からCVRを計算。無料のコンバージョン率計算機。',
  h1='コンバージョン率（CVR）計算機',
  lead='サイトのアクセス数（セッション）とコンバージョン（CV）数を入れるだけで、コンバージョン率（CVR）を計算します。広告やLPの成果チェックに。',
  inputs='''    <h2>🎯 数字を入れる</h2>
    <div class="row"><div class="field"><label>アクセス数 <span class="hint">（セッション）</span></label><input type="number" id="s" value="2000" min="0" inputmode="numeric"></div>
    <div class="field"><label>コンバージョン数 <span class="hint">（件）</span></label><input type="number" id="cv" value="40" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">CVRを計算</button>''',
  result='''      <div class="label">コンバージョン率（CVR）</div>
      <div class="big"><span id="big">0</span><span class="unit">％</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1CVに必要なアクセス</div><div class="v accent" id="need">—</div></div>
      <div class="stat"><div class="k">100アクセスで</div><div class="v" id="per100">—</div></div>
      <div class="stat"><div class="k">月1万アクセスなら</div><div class="v" id="man">—</div></div></div>''',
  visual=viz(480,70,500),
  article=art('CVR（％）＝ コンバージョン数 ÷ アクセス数 × 100',
    ['コンバージョン率（CVR）とは','CVR（Conversion Rate）は、サイトを訪れた人のうち、購入・申込・問い合わせなどの成果（コンバージョン）に至った割合です。広告・LP・サイト改善の効果を測る基本指標。ECで1〜3％、BtoBのリード獲得で1〜2％あたりが一つの目安とされます（業種で差があります）。'],
    [('CVRの平均は？','業種・商材で大きく異なります。自社の過去データと比較し、改善できているかで見るのがおすすめです。'),
     ('CVRを上げるには？','LPの分かりやすさ、入力フォームの簡素化、訴求の見直し、流入の質改善などが効きます。'),
     ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const s=Math.max(0,+$('s').value||0),cv=Math.max(0,+$('cv').value||0);
    const cvr=s>0?cv/s*100:0;
    $('sub').textContent=`${num(s)}アクセス中 ${num(cv)}件CV`;
    $('need').textContent=cv>0?num(s/cv)+'アクセス':'—';$('per100').textContent=num(cvr)+'件';$('man').textContent=num(cvr*100)+'件';
    SHARE=`コンバージョン率（CVR）計算機、CVRは ${num(cvr)}％ でした🎯`;show();anim(cvr);bar(clamp(cvr,0,Math.max(10,cvr)),Math.max(10,cvr));}
  function anim(v){const el=$('big'),t0=performance.now();(function s(n){const p=Math.min(1,(n-t0)/700),e=1-Math.pow(1-p,3);el.textContent=num(v*e);if(p<1)requestAnimationFrame(s);})(performance.now());}
  function bar(v,mx){const c=$('viz'),x=c.getContext('2d'),W=c.width,H=c.height,bx=16,bw=W-32,by=H/2-12;cancelAnimationFrame(raf);
    const t0=performance.now();function f(n){const p=Math.min(1,(n-t0)/700);x.fillStyle='#0b1530';x.fillRect(0,0,W,H);
      x.fillStyle='rgba(255,255,255,.1)';x.fillRect(bx,by,bw,24);const g=x.createLinearGradient(bx,0,bx+bw,0);g.addColorStop(0,'#0fb5c4');g.addColorStop(1,'#6366f1');
      x.fillStyle=g;x.fillRect(bx,by,bw*(v/mx)*p,24);x.fillStyle='#fff';x.font='bold 13px sans-serif';x.textAlign='center';x.fillText(num(v*p)+'%',W/2,by+42);
      if(p<1)raf=requestAnimationFrame(f);}raf=requestAnimationFrame(f);}''')

# ============================================================
# 2. CPA（顧客獲得単価）計算機（cpa 計算 450/KD0）
# ============================================================
add(id='cpa-keisan', emoji='💰', cat=CAT,
  title='CPA計算機｜広告費とCV数から顧客獲得単価を計算｜シミュラボ',
  desc='広告費とコンバージョン数から、CPA（顧客獲得単価／1件あたりの獲得コスト）を計算する無料ツール。目標CPAとの比較や、限界CPAの考え方も解説します。',
  ogtitle='CPA計算機｜顧客獲得単価を計算', ogdesc='広告費とCV数からCPA（獲得単価）を計算。無料のCPA計算機。',
  h1='CPA計算機（顧客獲得単価）',
  lead='広告費とコンバージョン数を入れるだけで、CPA（1件あたりの獲得コスト）を計算します。広告の費用対効果チェックに。',
  inputs='''    <h2>💰 数字を入れる</h2>
    <div class="row"><div class="field"><label>広告費 <span class="hint">（円）</span></label><input type="number" id="cost" value="300000" min="0" inputmode="numeric"></div>
    <div class="field"><label>コンバージョン数 <span class="hint">（件）</span></label><input type="number" id="cv" value="60" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>1件の利益（任意・採算判定用） <span class="hint">（円）</span></label><input type="number" id="profit" value="0" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">CPAを計算</button>''',
  result='''      <div class="label">CPA（顧客獲得単価）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1件あたり</div><div class="v accent" id="per">—</div></div>
      <div class="stat"><div class="k">100件獲得に</div><div class="v" id="h100">—</div></div>
      <div class="stat"><div class="k">採算判定</div><div class="v" id="ok">—</div></div></div>''',
  article=art('CPA（円）＝ 広告費 ÷ コンバージョン数',
    ['CPA（顧客獲得単価）とは','CPA（Cost Per Acquisition）は、1件のコンバージョン（顧客・申込）を獲得するのにかかった広告費です。1件あたりの利益（粗利やLTV）より低ければ採算が合います。CPAを下げるか、1件あたりの価値（LTV）を上げるのが広告改善の基本です。'],
    [('目標CPAはどう決める？','1件あたりの利益（またはLTV）を上限の目安にします。利益＞CPAなら黒字です。'),
     ('CPAを下げるには？','CVR改善、無駄なキーワード/配信先の停止、広告文・LPの改善などが有効です。'),
     ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const cost=Math.max(0,+$('cost').value||0),cv=Math.max(0,+$('cv').value||0),pr=Math.max(0,+$('profit').value||0);
    const cpa=cv>0?cost/cv:0;
    $('sub').textContent=`広告費${yen(cost)} ÷ ${num(cv)}件`;
    $('per').textContent=yen(cpa);$('h100').textContent=yen(cpa*100);
    $('ok').textContent=pr>0?(pr>=cpa?'黒字 ◎':'赤字 ×'):'—';
    SHARE=`CPA計算機、顧客獲得単価は ${yen(cpa)} でした💰`;show();anim(cpa);}
  function anim(v){const el=$('big'),t0=performance.now();(function s(n){const p=Math.min(1,(n-t0)/700),e=1-Math.pow(1-p,3);el.textContent=Math.round(v*e).toLocaleString('ja-JP');if(p<1)requestAnimationFrame(s);})(performance.now());}''')

# ============================================================
# 3. CPC（クリック単価）計算機（cpc 計算 200/KD0/TP500）
# ============================================================
add(id='cpc-keisan', emoji='🖱️', cat=CAT,
  title='CPC計算機｜広告費とクリック数からクリック単価を計算｜シミュラボ',
  desc='広告費とクリック数から、CPC（クリック単価）を計算する無料ツール。表示回数を入れればクリック率（CTR）も同時に分かります。リスティング・SNS広告の分析に。',
  ogtitle='CPC計算機｜クリック単価を計算', ogdesc='広告費とクリック数からCPC（クリック単価）を計算。CTRも。無料。',
  h1='CPC計算機（クリック単価）',
  lead='広告費とクリック数を入れるとCPC（1クリックあたりの費用）を計算。表示回数も入れれば、クリック率（CTR）も同時に出ます。',
  inputs='''    <h2>🖱️ 数字を入れる</h2>
    <div class="row"><div class="field"><label>広告費 <span class="hint">（円）</span></label><input type="number" id="cost" value="100000" min="0" inputmode="numeric"></div>
    <div class="field"><label>クリック数</label><input type="number" id="clicks" value="1250" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>表示回数（任意・CTR用） <span class="hint">（インプレッション）</span></label><input type="number" id="imp" value="0" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">CPCを計算</button>''',
  result='''      <div class="label">CPC（クリック単価）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">クリック率（CTR）</div><div class="v accent" id="ctr">—</div></div>
      <div class="stat"><div class="k">1000クリックで</div><div class="v" id="k1000">—</div></div></div>''',
  article=art('CPC（円）＝ 広告費 ÷ クリック数／CTR（％）＝ クリック数 ÷ 表示回数 × 100',
    ['CPC（クリック単価）とは','CPC（Cost Per Click）は1クリックあたりにかかった広告費です。リスティング広告やSNS広告の入札・費用管理の基本指標。CPCが高すぎる場合は、キーワードの見直しや品質スコア（広告の関連性）の改善でコストを下げられます。'],
    [('CTRも分かる？','表示回数を入れると、クリック率（CTR）も計算します。'),
     ('CPCを下げるには？','広告の関連性を高める、除外キーワード設定、ターゲティング精度の向上などが有効です。'),
     ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const cost=Math.max(0,+$('cost').value||0),cl=Math.max(0,+$('clicks').value||0),imp=Math.max(0,+$('imp').value||0);
    const cpc=cl>0?cost/cl:0,ctr=imp>0?cl/imp*100:0;
    $('sub').textContent=`広告費${yen(cost)} ÷ ${num(cl)}クリック`;
    $('ctr').textContent=imp>0?num(ctr)+'％':'（表示回数未入力）';$('k1000').textContent=yen(cpc*1000);
    SHARE=`CPC計算機、クリック単価は ${yen(cpc)} でした🖱️`;show();anim(cpc);}
  function anim(v){const el=$('big'),t0=performance.now();(function s(n){const p=Math.min(1,(n-t0)/700),e=1-Math.pow(1-p,3);el.textContent=Math.round(v*e).toLocaleString('ja-JP');if(p<1)requestAnimationFrame(s);})(performance.now());}''')

# ============================================================
# 4. CPM（広告表示単価）計算機（cpm 計算 500/KD1/TP800）
# ============================================================
add(id='cpm-keisan', emoji='📺', cat=CAT,
  title='CPM計算機｜広告費と表示回数から1000回表示単価を計算｜シミュラボ',
  desc='広告費と表示回数（インプレッション）から、CPM（1000回表示あたりの費用）を計算する無料ツール。ディスプレイ広告・SNS広告の費用比較に。',
  ogtitle='CPM計算機｜1000回表示単価を計算', ogdesc='広告費と表示回数からCPM（1000回表示単価）を計算。無料のCPM計算機。',
  h1='CPM計算機（1000回表示単価）',
  lead='広告費と表示回数（インプレッション）を入れると、CPM（1000回表示あたりの費用）を計算します。認知系・ディスプレイ広告の比較に。',
  inputs='''    <h2>📺 数字を入れる</h2>
    <div class="row"><div class="field"><label>広告費 <span class="hint">（円）</span></label><input type="number" id="cost" value="50000" min="0" inputmode="numeric"></div>
    <div class="field"><label>表示回数 <span class="hint">（インプレッション）</span></label><input type="number" id="imp" value="200000" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">CPMを計算</button>''',
  result='''      <div class="label">CPM（1000回表示単価）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1表示あたり</div><div class="v accent" id="per1">—</div></div>
      <div class="stat"><div class="k">100万表示の費用</div><div class="v" id="m">—</div></div></div>''',
  article=art('CPM（円）＝ 広告費 ÷ 表示回数 × 1000',
    ['CPM（インプレッション単価）とは','CPM（Cost Per Mille）は、広告が1000回表示されるごとにかかる費用です。クリックではなく「表示（認知）」を重視する広告で使われます。同じ予算でどれだけ多くの人に見てもらえるかを比較するときの指標です。'],
    [('CPCとの違いは？','CPCはクリックごと、CPMは表示ごとの課金です。認知拡大はCPM、成果獲得はCPC/CPAで見ます。'),
     ('CPMの相場は？','媒体・ターゲティングで大きく変わります。同条件での比較に使うのが有効です。'),
     ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const cost=Math.max(0,+$('cost').value||0),imp=Math.max(0,+$('imp').value||0);
    const cpm=imp>0?cost/imp*1000:0;
    $('sub').textContent=`広告費${yen(cost)} ÷ ${num(imp)}表示 × 1000`;
    $('per1').textContent=yen(imp>0?cost/imp:0);$('m').textContent=yen(cpm*1000);
    SHARE=`CPM計算機、1000回表示単価は ${yen(cpm)} でした📺`;show();anim(cpm);}
  function anim(v){const el=$('big'),t0=performance.now();(function s(n){const p=Math.min(1,(n-t0)/700),e=1-Math.pow(1-p,3);el.textContent=Math.round(v*e).toLocaleString('ja-JP');if(p<1)requestAnimationFrame(s);})(performance.now());}''')

# ============================================================
# 5. 解約率・チャーンレート計算機（チャーンレート 2100/KD1）
# ============================================================
add(id='churn-keisan', emoji='📉', cat=CAT,
  title='解約率（チャーンレート）計算機｜継続率・平均継続月数も｜シミュラボ',
  desc='期間中の解約数と顧客数から、解約率（チャーンレート）・継続率・平均継続期間を計算する無料ツール。サブスク・会員サービスの数値管理に。',
  ogtitle='解約率（チャーンレート）計算機', ogdesc='解約数と顧客数から解約率・継続率・平均継続月数を計算。無料。',
  h1='解約率（チャーンレート）計算機',
  lead='期首の顧客数と、その期間に解約した数を入れると、解約率（チャーンレート）・継続率・平均継続期間を計算します。サブスク・会員ビジネスに。',
  inputs='''    <h2>📉 数字を入れる</h2>
    <div class="row"><div class="field"><label>期首の顧客数</label><input type="number" id="start" value="1000" min="0" inputmode="numeric"></div>
    <div class="field"><label>解約した数 <span class="hint">（その月など）</span></label><input type="number" id="churned" value="50" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">解約率を計算</button>''',
  result='''      <div class="label">解約率（チャーンレート）</div>
      <div class="big"><span id="big">0</span><span class="unit">％</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">継続率</div><div class="v accent" id="keep">—</div></div>
      <div class="stat"><div class="k">平均継続期間</div><div class="v" id="life">—</div></div>
      <div class="stat"><div class="k">1年後の残存(概算)</div><div class="v" id="y1">—</div></div></div>''',
  article=art('解約率（％）＝ 解約数 ÷ 期首の顧客数 × 100／平均継続期間 ≒ 1 ÷ 解約率',
    ['チャーンレート（解約率）とは','チャーンレート（Churn Rate）は、一定期間に解約・離脱した顧客の割合です。サブスクや会員サービスの健全性を示す重要指標。月次の解約率が5％なら、平均継続期間はおよそ20ヶ月（1÷0.05）が目安です。解約率を1ポイント下げるだけで、LTVは大きく伸びます。'],
    [('平均継続期間の出し方は？','月次解約率の逆数（1÷解約率）が目安です。解約率5％＝約20ヶ月。'),
     ('解約率を下げるには？','オンボーディング改善、利用定着の支援、サポート強化、休眠前のフォローなどが有効です。'),
     ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const st=Math.max(0,+$('start').value||0),ch=Math.max(0,+$('churned').value||0);
    const churn=st>0?ch/st*100:0,keep=100-churn;
    const life=churn>0?100/churn:0;const y1=st*Math.pow(keep/100,12);
    $('sub').textContent=`${num(st)}人中 ${num(ch)}人が解約`;
    $('keep').textContent=num(keep)+'％';$('life').textContent=churn>0?num(life)+'ヶ月':'—';$('y1').textContent=num(y1)+'人';
    SHARE=`解約率（チャーンレート）計算機、解約率は ${num(churn)}％（平均継続 約${num(life)}ヶ月）でした📉`;show();anim(churn);}
  function anim(v){const el=$('big'),t0=performance.now();(function s(n){const p=Math.min(1,(n-t0)/700),e=1-Math.pow(1-p,3);el.textContent=num(v*e);if(p<1)requestAnimationFrame(s);})(performance.now());}''')

# ============================================================
# 6. 客単価計算機（客単価 計算 700/KD0/TP1000）
# ============================================================
add(id='kyakutanka-keisan', emoji='🧾', cat=CAT,
  title='客単価計算機｜売上と客数から客単価を計算（目標逆算も）｜シミュラボ',
  desc='売上と客数から客単価を計算する無料ツール。目標売上を入れれば、必要な客数や、客単価を上げたときの売上シミュレーションもできます。店舗・ECの数値管理に。',
  ogtitle='客単価計算機｜売上と客数から計算', ogdesc='売上÷客数で客単価を計算。目標売上の逆算も。無料の客単価計算機。',
  h1='客単価計算機',
  lead='売上と客数を入れると客単価を計算します。目標売上を入れれば「あと何人必要か」「客単価を上げると売上はどうなるか」も分かります。',
  inputs='''    <h2>🧾 数字を入れる</h2>
    <div class="row"><div class="field"><label>売上 <span class="hint">（円）</span></label><input type="number" id="sales" value="1500000" min="0" inputmode="numeric"></div>
    <div class="field"><label>客数 <span class="hint">（人・件）</span></label><input type="number" id="cust" value="500" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>目標売上（任意） <span class="hint">（円）</span></label><input type="number" id="target" value="0" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">客単価を計算</button>''',
  result='''      <div class="label">客単価</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">目標売上に必要な客数</div><div class="v accent" id="need">—</div></div>
      <div class="stat"><div class="k">客単価+10%で売上</div><div class="v" id="up">—</div></div></div>''',
  article=art('客単価（円）＝ 売上 ÷ 客数',
    ['客単価とは','客単価は、1人（1件）あたりの平均購入額です。売上は「客数 × 客単価」で決まるため、売上を伸ばすには客数を増やすか、客単価を上げるかの2通り。セット販売・アップセル・クロスセルで客単価を10％上げるだけでも、売上は大きく変わります。'],
    [('客単価を上げるには？','まとめ買い提案、上位プラン、関連商品のおすすめ（クロスセル）などが定番です。'),
     ('客数と客単価どちらを優先？','既存客への施策（客単価）は低コストで効果が出やすいことが多いです。'),
     ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const sa=Math.max(0,+$('sales').value||0),cu=Math.max(0,+$('cust').value||0),tg=Math.max(0,+$('target').value||0);
    const t=cu>0?sa/cu:0;
    $('sub').textContent=`売上${yen(sa)} ÷ ${num(cu)}人`;
    $('need').textContent=(tg>0&&t>0)?num(tg/t)+'人':'（目標未入力）';$('up').textContent=yen(sa*1.1);
    SHARE=`客単価計算機、客単価は ${yen(t)} でした🧾`;show();anim(t);}
  function anim(v){const el=$('big'),t0=performance.now();(function s(n){const p=Math.min(1,(n-t0)/700),e=1-Math.pow(1-p,3);el.textContent=Math.round(v*e).toLocaleString('ja-JP');if(p<1)requestAnimationFrame(s);})(performance.now());}''')

# ============================================================
# 7. リスティング広告 費用シミュレーター（リスティング広告 費用 1100/KD0）
# ============================================================
add(id='listing-hiyou', emoji='🔎', cat=CAT,
  title='リスティング広告 費用シミュレーター｜月額予算とCV数の目安｜シミュラボ',
  desc='クリック単価（CPC）と目標クリック数、想定CVRから、リスティング広告の月額費用・獲得できるCV数・CPAの目安を試算する無料シミュレーター。',
  ogtitle='リスティング広告 費用シミュレーター', ogdesc='CPC・クリック数・CVRから月額費用とCV数・CPAを試算。無料。',
  h1='リスティング広告 費用シミュレーター',
  lead='クリック単価・目標クリック数・想定CVRを入れると、リスティング広告の月額費用と、獲得できるCV数・CPAの目安を試算します。出稿前の予算検討に。',
  inputs='''    <h2>🔎 条件を入れる</h2>
    <div class="row"><div class="field"><label>クリック単価（CPC） <span class="hint">（円）</span></label><input type="number" id="cpc" value="80" min="0" inputmode="numeric"></div>
    <div class="field"><label>月の目標クリック数</label><input type="number" id="clicks" value="2000" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>想定CVR <span class="hint">（％）</span></label><input type="number" id="cvr" value="2" min="0" step="any" inputmode="decimal"></div>
    <button class="btn btn-primary" id="calcBtn">費用とCVを試算</button>''',
  result='''      <div class="label">月額の広告費（目安）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">想定CV数</div><div class="v accent" id="cv">—</div></div>
      <div class="stat"><div class="k">CPA（獲得単価）</div><div class="v" id="cpa">—</div></div>
      <div class="stat"><div class="k">年間費用</div><div class="v" id="year">—</div></div></div>''',
  article=art('月額費用 ＝ CPC × クリック数／CV数 ＝ クリック数 × CVR／CPA ＝ 月額費用 ÷ CV数',
    ['リスティング広告の費用感','リスティング広告（検索連動型広告）は、クリックされた分だけ費用がかかる仕組み。月額費用は「クリック単価 × クリック数」で決まります。出稿前に、想定CVRからCV数とCPAを見積もっておくと、予算が成果に見合うか判断できます。'],
    [('予算はいくらから？','媒体に最低額の縛りはほぼありません。まず小さく始めてCPAを見ながら調整するのが定石です。'),
     ('CPCはどう決まる？','キーワードの競合状況と広告の品質で変動します。人気KWほど高くなりがちです。'),
     ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const cpc=Math.max(0,+$('cpc').value||0),cl=Math.max(0,+$('clicks').value||0),cvr=Math.max(0,+$('cvr').value||0);
    const cost=cpc*cl,cv=cl*cvr/100,cpa=cv>0?cost/cv:0;
    $('sub').textContent=`CPC${num(cpc)}円 × ${num(cl)}クリック`;
    $('cv').textContent=num(cv)+'件';$('cpa').textContent=cv>0?yen(cpa):'—';$('year').textContent=yen(cost*12);
    SHARE=`リスティング広告 費用シミュ、月額 約${yen(cost)}で 約${num(cv)}件CV（CPA${yen(cpa)}）の試算でした🔎`;show();anim(cost);}
  function anim(v){const el=$('big'),t0=performance.now();(function s(n){const p=Math.min(1,(n-t0)/700),e=1-Math.pow(1-p,3);el.textContent=Math.round(v*e).toLocaleString('ja-JP');if(p<1)requestAnimationFrame(s);})(performance.now());}''')

# ============================================================
# 8. 集客ファネル試算（セッション→CV→売上）
# ============================================================
add(id='funnel-cv', emoji='🌀', cat=CAT,
  title='集客ファネル試算｜アクセス→CV→売上とCVR改善インパクト｜シミュラボ',
  desc='月間アクセス数・CVR・客単価から、コンバージョン数と売上を試算し、CVRを1ポイント改善したときの売上増加（改善インパクト）も計算する無料シミュレーター。',
  ogtitle='集客ファネル試算｜アクセス→CV→売上', ogdesc='アクセス・CVR・客単価からCV数と売上を試算。CVR改善の効果も。',
  h1='集客ファネル試算（アクセス→CV→売上）',
  lead='月間アクセス数・CVR・客単価を入れると、コンバージョン数と売上を試算します。さらに「CVRを1ポイント上げたら売上はいくら増えるか」も計算。改善の優先度づけに。',
  inputs='''    <h2>🌀 条件を入れる</h2>
    <div class="row"><div class="field"><label>月間アクセス数 <span class="hint">（セッション）</span></label><input type="number" id="s" value="10000" min="0" inputmode="numeric"></div>
    <div class="field"><label>CVR <span class="hint">（％）</span></label><input type="number" id="cvr" value="2" min="0" step="any" inputmode="decimal"></div></div>
    <div class="field"><label>客単価 <span class="hint">（円）</span></label><input type="number" id="aov" value="8000" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">売上を試算</button>''',
  result='''      <div class="label">月間の想定売上</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">月間CV数</div><div class="v accent" id="cv">—</div></div>
      <div class="stat"><div class="k">CVR+1ptで売上</div><div class="v" id="plus">—</div></div>
      <div class="stat"><div class="k">アクセス2倍なら</div><div class="v" id="x2">—</div></div></div>''',
  article=art('CV数 ＝ アクセス × CVR／売上 ＝ CV数 × 客単価',
    ['集客ファネルの考え方','売上は「アクセス × CVR × 客単価」の掛け算で決まります。どこを伸ばすと最も効くかは状況次第。アクセスが多いのにCVRが低いならサイト改善、CVRは高いのにアクセスが少ないなら集客（SEO・LLMO・広告）が効きます。本ツールでCVR改善インパクトを見て、優先順位をつけましょう。'],
    [('どこを改善すべき？','「アクセス × CVR × 客単価」のうち、いちばん弱い箇所が伸びしろです。'),
     ('CVR+1ptはどれくらい効く？','本ツールの「CVR+1ptで売上」で具体額を確認できます。アクセスが多いほど効果大です。'),
     ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const s=Math.max(0,+$('s').value||0),cvr=Math.max(0,+$('cvr').value||0),aov=Math.max(0,+$('aov').value||0);
    const cv=s*cvr/100,sales=cv*aov;const plus=s*(cvr+1)/100*aov;
    $('sub').textContent=`${num(s)}アクセス × CVR${num(cvr)}％ × ${yen(aov)}`;
    $('cv').textContent=num(cv)+'件';$('plus').textContent=yen(plus)+'（+'+yen(plus-sales)+'）';$('x2').textContent=yen(sales*2);
    SHARE=`集客ファネル試算、月間売上 約${yen(sales)}（CV ${num(cv)}件）。CVR+1ptで +${yen(plus-sales)}🌀`;show();anim(sales);}
  function anim(v){const el=$('big'),t0=performance.now();(function s(n){const p=Math.min(1,(n-t0)/700),e=1-Math.pow(1-p,3);el.textContent=Math.round(v*e).toLocaleString('ja-JP');if(p<1)requestAnimationFrame(s);})(performance.now());}''')

# ============================================================
# 9. MEO来店効果シミュレーター（meo 効果 90/KD0）
# ============================================================
add(id='meo-raiten', emoji='📍', cat=CAT,
  title='MEO来店効果シミュレーター｜地図検索からの来店数を試算｜シミュラボ',
  desc='地域の月間検索数・地図での表示率・来店率から、MEO（Googleマップ対策）による月間の来店数を試算し、上位表示で表示率が上がったときの来店増も計算する無料シミュレーター。',
  ogtitle='MEO来店効果シミュレーター｜地図検索からの来店', ogdesc='地域検索数・表示率・来店率からMEOの来店数を試算。改善効果も。',
  h1='MEO来店効果シミュレーター',
  lead='「地域名＋業種」の月間検索数・地図での表示率・来店率を入れると、MEO（マップ対策）からの月間来店数を試算します。上位表示で表示率が上がると来店がどれだけ増えるかも。',
  inputs='''    <h2>📍 条件を入れる</h2>
    <div class="row"><div class="field"><label>月間の地域検索数 <span class="hint">（地域名＋業種）</span></label><input type="number" id="search" value="3000" min="0" inputmode="numeric"></div>
    <div class="field"><label>地図での表示率 <span class="hint">（％・自店が表示される割合）</span></label><input type="number" id="view" value="20" min="0" max="100" inputmode="numeric"></div></div>
    <div class="field"><label>表示からの来店・連絡率 <span class="hint">（％）</span></label><input type="number" id="visit" value="6" min="0" max="100" step="any" inputmode="decimal"></div>
    <button class="btn btn-primary" id="calcBtn">来店数を試算</button>''',
  result='''      <div class="label">MEO経由の月間来店数（目安）</div>
      <div class="big"><span id="big">0</span><span class="unit">件</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">月間の地図表示回数</div><div class="v accent" id="views">—</div></div>
      <div class="stat"><div class="k">表示率を+20ptにすると</div><div class="v" id="up">—</div></div>
      <div class="stat"><div class="k">年間の来店数</div><div class="v" id="year">—</div></div></div>''',
  article=art('地図表示回数 ＝ 地域検索数 × 表示率／来店数 ＝ 地図表示回数 × 来店率',
    ['MEOの来店効果','MEO（Map Engine Optimization＝Googleマップ対策）は、「地域名＋業種」で検索したユーザーに、地図の上位で自店を表示させる施策です。上位に表示されるほど見られる回数（表示率）が増え、来店・電話・経路検索につながります。表示率を上げることが来店増に直結します。'],
    [('表示率はどう上げる？','Googleビジネスプロフィールの最新化、写真・投稿の更新、口コミ獲得と返信、NAP情報の統一などが基本です。'),
     ('LLMOとの関係は？','地図やAI（ChatGPT等）に正しく情報を伝える土台づくりは共通します。AIに選ばれる店づくり（LLMO）として一体で取り組むと効果的です。'),
     ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const se=Math.max(0,+$('search').value||0),vw=clamp(+$('view').value||0,0,100),vi=clamp(+$('visit').value||0,0,100);
    const views=se*vw/100,visits=views*vi/100;const up=se*Math.min(100,vw+20)/100*vi/100;
    $('sub').textContent=`検索${num(se)} × 表示率${num(vw)}％ × 来店率${num(vi)}％`;
    $('views').textContent=num(views)+'回';$('up').textContent=num(up)+'件（+'+num(up-visits)+'）';$('year').textContent=num(visits*12)+'件';
    SHARE=`MEO来店効果シミュ、地図検索からの月間来店は 約${num(visits)}件。表示率+20ptで +${num(up-visits)}件📍`;show();anim(visits);}
  function anim(v){const el=$('big'),t0=performance.now();(function s(n){const p=Math.min(1,(n-t0)/700),e=1-Math.pow(1-p,3);el.textContent=Math.round(v*e).toLocaleString('ja-JP');if(p<1)requestAnimationFrame(s);})(performance.now());}''')

# ============================================================
# 10. 広告予算シミュレーター（予算→クリック→CV→売上）
# ============================================================
add(id='kokoku-yosan', emoji='📊', cat=CAT,
  title='広告予算シミュレーター｜予算からクリック・CV・売上・ROASを試算｜シミュラボ',
  desc='月の広告予算・クリック単価（CPC）・CVR・客単価を入れると、獲得できるクリック数・CV数・売上・ROAS・CPAをまとめて試算する無料シミュレーター。',
  ogtitle='広告予算シミュレーター｜CV・売上・ROASを試算', ogdesc='予算・CPC・CVR・客単価からクリック数・CV・売上・ROAS・CPAを試算。',
  h1='広告予算シミュレーター',
  lead='月の広告予算・CPC・CVR・客単価を入れるだけで、クリック数・CV数・売上・ROAS・CPAをまとめて試算します。予算配分の検討に。',
  inputs='''    <h2>📊 条件を入れる</h2>
    <div class="row"><div class="field"><label>月の広告予算 <span class="hint">（円）</span></label><input type="number" id="budget" value="300000" min="0" inputmode="numeric"></div>
    <div class="field"><label>クリック単価（CPC） <span class="hint">（円）</span></label><input type="number" id="cpc" value="100" min="1" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>CVR <span class="hint">（％）</span></label><input type="number" id="cvr" value="2" min="0" step="any" inputmode="decimal"></div>
    <div class="field"><label>客単価 <span class="hint">（円）</span></label><input type="number" id="aov" value="15000" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">成果を試算</button>''',
  result='''      <div class="label">想定売上（月）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">ROAS</div><div class="v accent" id="roas">—</div></div>
      <div class="stat"><div class="k">CV数 / CPA</div><div class="v" id="cvcpa">—</div></div>
      <div class="stat"><div class="k">クリック数</div><div class="v" id="clicks">—</div></div></div>''',
  article=art('クリック数 ＝ 予算 ÷ CPC／CV数 ＝ クリック数 × CVR／売上 ＝ CV数 × 客単価／ROAS ＝ 売上 ÷ 予算 × 100',
    ['広告予算と成果の関係','広告は「予算 → クリック → CV → 売上」とつながっています。各段階の数値（CPC・CVR・客単価）を入れることで、予算からどれくらいの売上が見込めるか、ROAS（広告費用対効果）はどうかを事前に試算できます。ROASが100％を超えれば、広告費以上の売上が立つ計算です（利益で見るなら粗利率も加味を）。'],
    [('ROASとROIの違いは？','ROASは売上ベース、ROIは利益ベースの指標です。黒字判断は粗利を加味したROIで見ます。'),
     ('どの数値を改善すべき？','CVRと客単価は売上に直結します。CPCはコスト側。バランスを見て改善を。'),
     ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js=r'''  function calc(){const b=Math.max(0,+$('budget').value||0),cpc=Math.max(1,+$('cpc').value||1),cvr=Math.max(0,+$('cvr').value||0),aov=Math.max(0,+$('aov').value||0);
    const clicks=b/cpc,cv=clicks*cvr/100,sales=cv*aov,roas=b>0?sales/b*100:0,cpa=cv>0?b/cv:0;
    $('sub').textContent=`予算${yen(b)}・CPC${num(cpc)}円・CVR${num(cvr)}％`;
    $('roas').textContent=num(roas)+'％';$('cvcpa').textContent=num(cv)+'件 / '+(cv>0?yen(cpa):'—');$('clicks').textContent=num(clicks)+'クリック';
    SHARE=`広告予算シミュ、予算${yen(b)}で想定売上 約${yen(sales)}（ROAS ${num(roas)}％）でした📊`;show();anim(sales);}
  function anim(v){const el=$('big'),t0=performance.now();(function s(n){const p=Math.min(1,(n-t0)/700),e=1-Math.pow(1-p,3);el.textContent=Math.round(v*e).toLocaleString('ja-JP');if(p<1)requestAnimationFrame(s);})(performance.now());}''')

# ============================================================
# 11. 店舗のLLMO対応度診断（診断・AIに選ばれる店チェック）
# ============================================================
QUIZ = [
  ['Googleビジネスプロフィールを登録し、最新の状態に保っている',[['できている',2],['ある程度',1],['できていない',0]]],
  ['店名・住所・電話番号（NAP）が、自社サイトや各掲載先で統一されている',[['できている',2],['ある程度',1],['できていない',0]]],
  ['口コミに返信している',[['できている',2],['ある程度',1],['できていない',0]]],
  ['地図・ポータル・各種サービスに店舗情報を掲載している（サイテーション）',[['できている',2],['ある程度',1],['できていない',0]]],
  ['ChatGPTなどのAIに、自店が正しく紹介されるか確認したことがある',[['できている',2],['ある程度',1],['したことがない',0]]],
  ['写真・営業時間・商品/サービス情報を定期的に更新している',[['できている',2],['ある程度',1],['できていない',0]]],
  ['「地域名＋業種」で検索したとき、地図で上位に表示される',[['されている',2],['たまに',1],['されない/不明',0]]],
  ['競合店と比べて、口コミ件数・評価で見劣りしない',[['勝っている',2],['同程度',1],['負けている/不明',0]]],
]
add(id='llmo-check', emoji='🤖', cat=CAT,
  title='店舗のLLMO対応度診断｜AIに選ばれる店かを8問でチェック｜シミュラボ',
  desc='ChatGPTなどの生成AIや地図検索に「選ばれる店」になれているか（LLMO対応度）を、8問でセルフチェックする無料診断。GBP・NAP・口コミ・サイテーションなどの観点から、今の対応度と次の一手が分かります。',
  ogtitle='店舗のLLMO対応度診断｜AIに選ばれる店？', ogdesc='8問で店舗のLLMO対応度をセルフチェック。AI・地図検索の集客の伸びしろが分かる。',
  h1='店舗のLLMO対応度診断',
  lead='ChatGPTなどのAIや地図検索に「選ばれる店」になれていますか？GBP・NAP・口コミ・サイテーションなど8つの観点で、今のLLMO対応度をセルフチェック。集客の伸びしろが分かります。',
  inputs='''    <h2>🤖 8つの質問に答えてね</h2>
    <p style="color:var(--ink-2);font-size:13px;margin:-4px 0 6px;">店舗の現状に近いものを選んでください。<span id="prog" style="font-weight:800;color:var(--teal-d);">0 / 8 問</span></p>
    <div id="quiz" class="quiz"></div>
    <button class="btn btn-primary" id="calcBtn" style="margin-top:8px;">対応度を見る</button>''',
  result='''      <div class="label">あなたの店舗のLLMO対応度</div>
      <div id="emoji" style="font-size:60px;line-height:1.1;">🤖</div>
      <div class="big" style="font-size:26px;"><span id="big">—</span></div>
      <div class="sub" id="score">—</div>
      <div class="alert good" id="advice" style="text-align:left;margin-top:14px;">—</div>''',
  visual=viz(480,80,500),
  article=art('対応度スコア ＝ 8項目（各2点）の合計（最大16点）',
    ['LLMOとは？店舗がやるべきこと','LLMO（Large Language Model Optimization）は、ChatGPTなどの生成AIや、AIを使った地図・検索に「正しく・好意的に」自店を紹介してもらうための対策です。土台になるのは、Googleビジネスプロフィール（MEO）の整備、NAP情報（店名・住所・電話）の統一、口コミの獲得と返信、各サービスへの掲載（サイテーション）など。これらが整っているほど、AIにも地図にも「選ばれる店」に近づきます。'],
    [('LLMOとMEOは何が違う？','MEOは地図検索（Googleマップ）対策、LLMOは生成AIを含む“AIに選ばれる”ための対策です。土台の多くは共通します。'),
     ('何から始めればいい？','まずGoogleビジネスプロフィールの整備とNAPの統一、口コミ対応から。スコアの低かった項目が伸びしろです。'),
     ('この診断は何のため？','現状の対応度を把握し、次の一手を決めるためのセルフチェックです。')]),
  js=('  const Q=' + json.dumps(QUIZ, ensure_ascii=False) + r''';
  const BANDS=[[6,'🔴','未対応（伸びしろ大）','AI・地図検索の集客はこれから。まずGBP整備・NAP統一・口コミ対応から始めると、大きく伸びる余地があります。'],[11,'🟡','対応は道半ば','基本はできつつある状態。サイテーション整備やAIでの見え方チェックなど、一段上の対策で差がつきます。'],[16,'🟢','よく対応できている','土台はしっかり。あとは継続的な更新と、AIでの表示モニタリングで優位を保ちましょう。']];
  const wrap=$('quiz');
  Q.forEach((qq,i)=>{const d=document.createElement('div');d.className='q';
    let h='<p class="qt"><b>Q'+(i+1)+'.</b> '+qq[0]+'</p><div class="opts" style="grid-template-columns:1fr;">';
    qq[1].forEach(o=>{h+='<button type="button" class="opt" data-q="'+i+'" data-p="'+o[1]+'">'+o[0]+'</button>';});
    d.innerHTML=h+'</div>';wrap.appendChild(d);});
  wrap.addEventListener('click',e=>{const b=e.target.closest('.opt');if(!b)return;const qi=b.dataset.q;
    wrap.querySelectorAll('.opt[data-q="'+qi+'"]').forEach(o=>o.classList.toggle('on',o===b));
    const p=$('prog');if(p)p.textContent=document.querySelectorAll('#quiz .opt.on').length+' / '+Q.length+' 問';});
  function calc(){const on=document.querySelectorAll('#quiz .opt.on');
    if(on.length<Q.length){alert('あと'+(Q.length-on.length)+'問！全部の質問に答えてね');
      const qs=document.querySelectorAll('#quiz .q');for(let j=0;j<qs.length;j++){if(!qs[j].querySelector('.opt.on')){qs[j].scrollIntoView({behavior:'smooth',block:'center'});break;}}return;}
    let s=0;on.forEach(b=>s+=(+b.dataset.p||0));
    let band=BANDS[BANDS.length-1];for(const bd of BANDS){if(s<=bd[0]){band=bd;break;}}
    $('emoji').textContent=band[1];$('big').textContent=band[2];$('score').textContent='対応度スコア '+s+' / 16';$('advice').textContent='💡 '+band[3];
    SHARE='店舗のLLMO対応度診断、私の店は「'+band[2]+'」（'+s+'/16）でした🤖 AIに選ばれる店になろう。';
    show();drawScore(s,16);}
  function drawScore(s,mx){const c=$('viz'),x=c.getContext('2d'),W=c.width,H=c.height,bx=20,bw=W-40,by=H/2-11;cancelAnimationFrame(raf);
    const t0=performance.now();function f(n){const p=Math.min(1,(n-t0)/800);x.fillStyle='#0b1530';x.fillRect(0,0,W,H);
      x.fillStyle='rgba(255,255,255,.1)';x.fillRect(bx,by,bw,22);const g=x.createLinearGradient(bx,0,bx+bw,0);g.addColorStop(0,'#f43f5e');g.addColorStop(0.5,'#fbbf24');g.addColorStop(1,'#34d399');
      x.save();x.beginPath();x.rect(bx,by,bw*(s/mx)*p,22);x.clip();x.fillStyle=g;x.fillRect(bx,by,bw,22);x.restore();
      x.fillStyle='#fff';x.font='bold 13px sans-serif';x.textAlign='center';x.fillText(Math.round(s*p)+' / '+mx,W/2,by+40);
      if(p<1)raf=requestAnimationFrame(f);}raf=requestAnimationFrame(f);}'''))

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
    print(f'webmkt done. {len(SIMS)} sims.')
