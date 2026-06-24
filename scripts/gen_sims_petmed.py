# -*- coding: utf-8 -*-
"""シミュラボ：ペット予防薬の年間費用シミュレーター（既存 slug=pet カテゴリに追加）。
YMYL配慮：安全最優先・費用の目安ツール（医療アドバイスではない）。
結果欄に安全注意＋個人輸入アフィリのバナー（※広告明記・rel=sponsored nofollow）。
gen_sims_tool の TPL/viz を流用（try無し）。

seo_internal.py / gen_images.py のauto-importに 'gen_sims_petmed' を追加して使う。
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims11 import faq
from gen_sims_tool import TPL, viz
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CAT = 'ペット'

SAFETY = '''      <div class="alert" style="background:#fef2f2;border:1.5px solid #fca5a5;border-radius:12px;padding:14px;text-align:left;margin:16px 0 0;color:#7f1d1d;">
        <strong>⚠️ 投薬の前に、必ず動物病院へ</strong>
        <ul style="margin:8px 0 0;padding-left:18px;font-size:13px;line-height:1.85;">
          <li>フィラリア予防薬は、投与前に動物病院での<b>フィラリア感染検査が必須</b>です。感染している犬に予防薬を与えると、重い副作用が出ることがあります。</li>
          <li>薬の種類・量は体重や健康状態で変わります。<b>自己判断での投薬は避けてください。</b></li>
          <li>個人輸入は自分のペット用なら可能ですが、<b>偽造品・品質・用量のリスク</b>があります。正規品・信頼できる販売元を選び、不安な点は獣医師にご相談を。</li>
          <li>持病・妊娠中・幼齢・高齢のペットは、特に獣医師の指示に従ってください。</li>
          <li>本ツールは<b>費用の目安</b>であり、医療上のアドバイスではありません。</li>
        </ul>
      </div>'''

BANNER = '''      <div style="margin-top:16px;padding:14px;background:#fff7ed;border:1.5px solid #fdba74;border-radius:14px;text-align:center;">
        <div style="font-size:11.5px;font-weight:800;color:#9a3412;margin-bottom:8px;line-height:1.6;">※広告（アフィリエイト）｜個人輸入は自己責任です。投薬の前に必ず動物病院でフィラリア検査・診察を受けてください。</div>
        <a href="https://oneclck.net/contents/ard.php?id=UP017900&adwares=up920059" target="_blank" rel="sponsored nofollow noopener">
          <img src="https://oneclck.net/contents/photos/bn_up_new-membership-blank_480_360.jpg" alt="ペットの薬の個人輸入（広告）" style="width:100%;max-width:480px;height:auto;border:0;border-radius:8px;">
        </a>
      </div>'''

SIMS=[dict(id='pet-yobou-hiyou', emoji='🐾', cat=CAT,
  title='ペット予防薬の年間費用シミュレーター｜フィラリア・ノミダニはいくら？｜シミュラボ',
  desc='犬・猫のフィラリア予防やノミ・マダニ予防にかかる年間費用の目安を計算する無料シミュレーター。動物病院と個人輸入のおおよその費用比較も。※投薬前に必ず動物病院でフィラリア検査を。',
  ogtitle='ペット予防薬の年間費用シミュレーター｜いくら？', ogdesc='犬・猫のフィラリア・ノミダニ予防の年間費用の目安を計算。※検査は必ず動物病院で。',
  h1='ペット予防薬の年間費用シミュレーター',
  lead='犬・猫のフィラリア予防やノミ・マダニ予防に、1年でどれくらいかかる？予防の月数と1ヶ月あたりの薬代から、年間費用の目安を計算します。費用を見える化して、無理のない予防計画に。<b>投薬の前には必ず動物病院でフィラリア検査・診察を受けてください。</b>',
  inputs='''    <h2>🐾 条件を入れる</h2>
    <div class="row"><div class="field"><label>ペット</label><select id="type"><option value="dog">犬</option><option value="cat">猫</option></select></div>
    <div class="field"><label>体重 <span class="hint">（kg・薬量の参考）</span></label><input type="number" id="w" value="5" min="0" step="0.1" inputmode="decimal"></div></div>
    <div class="row"><div class="field"><label>フィラリア予防 <span class="hint">（月数・0〜12）</span></label><input type="number" id="fm" value="7" min="0" max="12" inputmode="numeric"></div>
    <div class="field"><label>その1ヶ月分の薬代 <span class="hint">（円・病院目安）</span></label><input type="number" id="fc" value="1200" min="0" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>ノミ・マダニ予防 <span class="hint">（月数・0〜12）</span></label><input type="number" id="nm" value="12" min="0" max="12" inputmode="numeric"></div>
    <div class="field"><label>その1ヶ月分の薬代 <span class="hint">（円・病院目安）</span></label><input type="number" id="nc" value="1600" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">年間費用を見る</button>''',
  result='''      <div class="label">予防薬の年間費用（動物病院の目安）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">フィラリア予防</div><div class="v" id="fil">—</div></div>
      <div class="stat"><div class="k">ノミ・マダニ予防</div><div class="v" id="nomi">—</div></div>
      <div class="stat"><div class="k">月あたり平均</div><div class="v accent" id="permonth">—</div></div></div>
      <div class="viz-wrap" style="margin-top:14px;">''' + viz(480,110,500) + '''</div>
      <div class="note" style="margin-top:14px;text-align:left;"><strong>費用を抑えたいときは</strong><br>同じ予防薬でも、個人輸入だと動物病院より安く手に入ることがあります（上のグラフの概算は病院の目安の約45%。送料・代行手数料・正規品かどうかで変わります）。ただし<b>個人輸入でも、フィラリア検査・診察は動物病院で受ける必要があります</b>。検査・診察料は別途かかります。</div>'''
      + SAFETY + BANNER,
  visual='',
  article='''    <div class="note" style="border-left:4px solid var(--teal)"><strong>結論</strong>：犬のフィラリア＋ノミ・マダニ予防は、動物病院で<b>年間およそ2〜4万円</b>が一つの目安（体重・薬の種類・予防月数で変わります）。同じ薬を個人輸入すると費用を抑えられる場合がありますが、<b>フィラリア検査・診察は必ず動物病院で</b>受けてください。</div>
    <h2>フィラリア・ノミダニ予防にかかる費用</h2>
    <p>フィラリア予防は、蚊の出る時期に合わせて月1回投与するのが一般的（地域により年5〜12ヶ月）。ノミ・マダニ予防は通年が推奨されることが多く、薬代は体重や薬の種類（飲み薬・スポット・チュアブル）で変わります。上のシミュレーターで、予防月数と1ヶ月あたりの薬代を入れると、年間のおおよその費用が分かります。</p>
    <h2>動物病院と個人輸入、費用の違い</h2>
    <p>同じ有効成分の予防薬でも、個人輸入（自分のペット用）だと動物病院より安く入手できることがあります。一方で、<b>偽造品や品質のばらつき、用量の取り違えといったリスク</b>もあります。価格だけで選ばず、正規品・信頼できる販売元を選ぶことが大切です。</p>
    <div class="note" style="background:#fef2f2;border:1px solid #fca5a5;"><strong>いちばん大切なこと：フィラリア予防の前に必ず検査を</strong><br>すでにフィラリアに感染している犬に予防薬を与えると、重い副作用（ショックなど）を起こす危険があります。毎シーズン、投薬を始める前に<b>動物病院でフィラリア感染検査</b>を受けてください。これは費用を抑える・抑えないにかかわらず、省略してはいけない大切なステップです。</p></div>
    <h2>よくある質問</h2>'''+faq([
      ('個人輸入は違法ですか？','自分が飼っているペット用に、数量の範囲内で個人輸入することは認められています（販売・譲渡は不可）。詳しくは動物医薬品検査所などの公的情報をご確認ください。'),
      ('フィラリア検査は受けなくていい？','いいえ。投薬前のフィラリア感染検査は必須です。感染犬への予防薬投与は危険なため、毎シーズン動物病院で検査を受けてください。'),
      ('どれくらい安くなりますか？','ケースにより様々で、断定できません。送料・代行手数料・為替・正規品かどうかで変わります。安さだけでなく安全面で選んでください。'),
      ('このツールは医療アドバイスですか？','いいえ。費用の目安を出すツールです。薬の選択・投与は必ず獣医師にご相談ください。'),
      ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')])
    +'''<h2>参考</h2><ul class="seo-refs"><li>農林水産省 動物医薬品検査所「動物用医薬品の個人輸入について」</li><li>公益社団法人 日本獣医師会「フィラリア症の予防」</li><li>各動物病院の予防・検査案内</li></ul>
    <p style="font-size:12px;color:var(--ink-2);">※本ページには広告（アフィリエイト）を含みます。価格・在庫・取り扱いは各サイトでご確認ください。投薬の前に必ず動物病院を受診してください。</p>''',
  js=r'''  function calc(){const type=$('type').value,w=+$('w').value||0;
    const fm=clamp(Math.trunc(+$('fm').value||0),0,12),nm=clamp(Math.trunc(+$('nm').value||0),0,12);
    const fc=Math.max(0,+$('fc').value||0),nc=Math.max(0,+$('nc').value||0);
    const fil=fm*fc,nomi=nm*nc,hospital=fil+nomi;const importEst=Math.round(hospital*0.45);
    $('big').textContent=num(hospital);$('sub').textContent=`${type==='dog'?'犬':'猫'}・${w}kg／フィラリア${fm}ヶ月＋ノミダニ${nm}ヶ月`;
    $('fil').textContent=yen(fil);$('nomi').textContent=yen(nomi);$('permonth').textContent=yen(hospital/12);
    SHARE=`ペット予防薬の年間費用シミュ、フィラリア＋ノミダニ予防は年間 約${yen(hospital)}でした🐾（※投薬前に必ず動物病院でフィラリア検査を）`;
    show();anim(hospital);drawBars(hospital,importEst);}
  function anim(v){const el=$('big'),t0=performance.now();(function s(n){const p=Math.min(1,(n-t0)/800),e=1-Math.pow(1-p,3);el.textContent=Math.round(v*e).toLocaleString('ja-JP');if(p<1)requestAnimationFrame(s);})(performance.now());}
  function drawBars(hosp,imp){const c=$('viz'),x=c.getContext('2d'),W=c.width,H=c.height;cancelAnimationFrame(raf);
    const mx=Math.max(hosp,1),bx=110,bw=W-150,t0=performance.now();
    function f(n){const p=Math.min(1,(n-t0)/800);x.fillStyle='#0b1530';x.fillRect(0,0,W,H);
      function bar(y,label,val,col){x.fillStyle='#fff';x.font='12px sans-serif';x.textAlign='right';x.fillText(label,bx-10,y+16);
        x.fillStyle='rgba(255,255,255,.1)';x.fillRect(bx,y,bw,20);x.fillStyle=col;x.fillRect(bx,y,bw*(val/mx)*p,20);
        x.fillStyle='#fff';x.font='bold 12px sans-serif';x.textAlign='left';x.fillText('¥'+Math.round(val*p).toLocaleString('ja-JP'),bx+6,y+15);}
      bar(26,'動物病院',hosp,'#6366f1');bar(64,'個人輸入(概算)',imp,'#34d399');
      if(p<1)raf=requestAnimationFrame(f);}raf=requestAnimationFrame(f);}''')]

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
    print(f'petmed done. {len(SIMS)} sims.')
