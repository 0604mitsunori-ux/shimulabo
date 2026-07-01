# -*- coding: utf-8 -*-
"""シミュラボ：教員・先生カテゴリ 15本。結果ページに通知表作成ツールのCTA入り。"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims11 import faq
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGO = '''<span class="mark">
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M9 3h6M10 3v5.2L5.4 16.4A2.4 2.4 0 0 0 7.5 20h9a2.4 2.4 0 0 0 2.1-3.6L14 8.2V3" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M7.7 14.5h8.6" stroke="#fff" stroke-width="1.8" stroke-linecap="round"/>
          <circle cx="10.3" cy="16.7" r="1" fill="#fff"/>
          <circle cx="13.4" cy="17.4" r=".7" fill="#fff"/>
        </svg>
      </span>'''

# 通知表作成ツールへの訴求CTA（結果欄に表示）
CTA = '''      <a class="cta-box" href="https://piyopiyo-teacher.com/?page_id=1103" target="_blank" rel="noopener" style="display:block;text-decoration:none;text-align:left;margin-top:20px;background:linear-gradient(135deg,#fff7ed,#ffedd5);border:1.5px solid #fcd34d;border-radius:14px;padding:16px 18px;">
        <div style="font-weight:900;color:#b45309;font-size:15px;">📝 通知表の所見づくり、もっとラクに。</div>
        <div style="font-size:13px;color:var(--ink-2);margin-top:5px;line-height:1.6;">観点を選ぶだけで自然な所見文が完成。先生のための「通知表 所見作成ツール」を無料で試せます。</div>
        <div style="margin-top:10px;font-weight:800;color:#b45309;font-size:13px;">所見作成ツールを使ってみる →</div>
      </a>'''

TPL = '''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<meta name="description" content="__DESC__">
<meta property="og:title" content="__OGTITLE__">
<meta property="og:description" content="__OGDESC__">
<meta property="og:type" content="website">
<link rel="stylesheet" href="../../assets/style.css">
</head>
<body>

<header class="site-header">
  <div class="inner">
    <a class="brand" href="../../index.html">
      ''' + LOGO + '''
      <span class="name">シミュ<b>ラボ</b></span>
    </a>
    <span class="spacer"></span>
    <a class="back" href="../../index.html">← 一覧へ</a>
  </div>
</header>

<main class="wrap">

  <div class="sim-head">
    <div class="cat">__CAT__</div>
    <h1>__H1__</h1>
    <p class="lead">__LEAD__</p>
  </div>

  <section class="panel">
__INPUTS__
  </section>

  <section class="panel" id="resultPanel" style="display:none">
    <div class="result">
__RESULT__
''' + CTA + '''
      <div style="text-align:center;margin-top:14px;"><span id="shareCount" class="share-count" style="display:none"></span></div>
      <div class="share-row">
        <button class="btn btn-x" id="shareBtn">𝕏 で結果をシェア</button>
        <button class="btn btn-ghost" id="copyBtn">結果をコピー</button>
      </div>
    </div>
  </section>

  <article class="article">
__ARTICLE__
  </article>

  <section class="req-banner">
    <h2>💡 こんなシミュも見てみたい？</h2>
    <p>あなたの「これ数字で見たい」を送ってください。投票で人気の案から実際に作ります。</p>
    <a class="btn btn-primary" style="width:auto;display:inline-flex;padding:14px 30px;" href="../../request/index.html">リクエストする →</a>
    <div style="margin-top:12px;"><a href="../../board/index.html" style="font-size:13px;font-weight:800;">🗳️ みんなのリクエストに投票する →</a></div>
  </section>

</main>

<footer class="site-footer">
  <div class="inner">
    <p><a href="../../index.html">← シミュラボ トップへ戻る</a></p>
    <p style="margin-top:10px;opacity:.7">© 2026 シミュラボ</p>
  </div>
</footer>

<script>
(() => {
  const $ = (id) => document.getElementById(id);
  const yen = (n) => '¥' + Math.round(n).toLocaleString('ja-JP');
  const num = (n) => Math.round(n).toLocaleString('ja-JP');
  const sel = (id) => { const e=$(id); return e.options[e.selectedIndex]; };
  let SHARE = '';
  function anim(el, from, to, dur, dec){ const t0=performance.now(); (function s(n){const p=Math.min(1,(n-t0)/dur);const e=1-Math.pow(1-p,3);const v=from+(to-from)*e;el.textContent=(dec!=null?v.toFixed(dec):Math.round(v).toLocaleString('ja-JP'));if(p<1)requestAnimationFrame(s);})(performance.now()); }
  function show(){ $('resultPanel').style.display=''; $('resultPanel').scrollIntoView({behavior:'smooth',block:'start'}); }
__JS__
  $('calcBtn').addEventListener('click', calc);
  $('shareBtn').addEventListener('click', () => window.open('https://twitter.com/intent/tweet?text='+encodeURIComponent(SHARE)+'&url='+encodeURIComponent(location.href)+'&hashtags='+encodeURIComponent('シミュラボ,教員'),'_blank','noopener'));
  $('copyBtn').addEventListener('click', async () => { try{ await navigator.clipboard.writeText(SHARE+'\\n'+location.href); $('copyBtn').textContent='コピーしました ✓'; setTimeout(()=>$('copyBtn').textContent='結果をコピー',1600);}catch{alert(SHARE);} });
})();
</script>
<script src="../../assets/result-fx.js"></script>
<script src="../../assets/share-counter.js"></script>
<script>ShareCounter.initSim({ simId:'__ID__', badgeEl:document.getElementById('shareCount'), shareBtnIds:['shareBtn'] });</script>
</body>
</html>
'''

T = '教員・先生'
SIMS = []
def add(**k): SIMS.append(k)

add(id='seiseki-hyotei', cat=T, emoji='📊',
  title='観点別評価→評定シミュレーター｜A/B/Cから5段階評定に｜シミュラボ',
  desc='3観点（知識・技能／思考・判断・表現／主体的に学習に取り組む態度）のA・B・C評価から、5段階の評定の目安を自動算出する先生向け無料ツール。',
  ogtitle='観点別評価→評定シミュレーター｜5段階評定に', ogdesc='3観点のA/B/Cから5段階評定の目安を算出。',
  h1='観点別評価→評定シミュレーター',
  lead='3観点のA・B・C評価を選ぶと、5段階の評定の目安を表示します。評定づけの確認や、児童生徒・保護者への説明準備に（最終判断は各校の基準で）。',
  inputs='''    <h2>📊 観点別評価を選ぶ</h2>
    <div class="field"><label>① 知識・技能</label><select id="q1"><option value="3">A（十分満足）</option><option value="2" selected>B（おおむね満足）</option><option value="1">C（努力を要する）</option></select></div>
    <div class="field"><label>② 思考・判断・表現</label><select id="q2"><option value="3">A</option><option value="2" selected>B</option><option value="1">C</option></select></div>
    <div class="field"><label>③ 主体的に学習に取り組む態度</label><select id="q3"><option value="3">A</option><option value="2" selected>B</option><option value="1">C</option></select></div>
    <button class="btn btn-primary" id="calcBtn">評定の目安を見る</button>''',
  result='''      <div class="label">5段階評定の目安</div>
      <div class="big"><span id="big">0</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">観点の合計</div><div class="v accent" id="sum">—</div></div>
      <div class="stat"><div class="k">評価の組合せ</div><div class="v" id="combo">—</div></div>
      <div class="stat"><div class="k">判定の目安</div><div class="v" id="note2">—</div></div></div>''',
  article='''    <h2>観点別評価と評定</h2>
    <div class="note"><strong>目安の考え方</strong><br>3観点の合計（A=3/B=2/C=1）で：9→5／8→4／7→4／6→3／5→3／4→2／3→1 を目安に。<br>※学校・自治体で基準は異なります。最終判断は各校の評価規準に従ってください。</div>
    <p>観点別評価から評定への変換は、学校ごとに細かなルールがあります。本ツールは一般的な目安で、評定づけの考え方を確認する補助としてお使いください。</p>
    <h2>よくある質問</h2>'''+faq([('そのまま使える？','一般的な目安です。必ず各校の評価規準で最終判断してください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const a=+$('q1').value,b=+$('q2').value,c=+$('q3').value,s=a+b+c;
    let h; if(s>=9)h=5; else if(s>=7)h=4; else if(s>=5)h=3; else if(s>=4)h=2; else h=1;
    const lt=v=>v===3?'A':v===2?'B':'C';
    $('sub').textContent='3観点の評価から算出した目安';
    $('sum').textContent=s+'点'; $('combo').textContent=lt(a)+lt(b)+lt(c); $('note2').textContent='評定 '+h;
    SHARE=`観点別評価→評定シミュ、評定の目安は「${h}」でした📊（${lt(a)}${lt(b)}${lt(c)}）`;
    show(); anim($('big'),0,h,800);
  }''')

add(id='test-toukei', cat=T, emoji='📈',
  title='テスト統計シミュレーター｜平均点・最高最低・標準偏差を一発計算｜シミュラボ',
  desc='点数を貼り付けるだけで、クラスの平均点・最高点・最低点・range・標準偏差を自動計算する先生向け無料ツール。',
  ogtitle='テスト統計シミュレーター｜平均・標準偏差を計算', ogdesc='点数を貼り付けて平均・最高最低・標準偏差を計算。',
  h1='テスト統計シミュレーター',
  lead='テストの点数をカンマやスペース、改行で区切って貼り付けるだけ。平均点・最高最低・標準偏差を一発で計算します。成績処理の下調べに。',
  inputs='''    <h2>📈 点数を貼り付け</h2>
    <div class="field"><label>点数（カンマ・スペース・改行区切り）</label><textarea id="scores" rows="4" style="width:100%;padding:12px;border:1.5px solid var(--line);border-radius:12px;font-size:15px;">72, 85, 60, 90, 45, 78, 88, 65, 70, 95</textarea></div>
    <button class="btn btn-primary" id="calcBtn">統計を計算する</button>''',
  result='''      <div class="label">クラスの平均点</div>
      <div class="big"><span id="big">0</span><span class="unit">点</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">最高 / 最低</div><div class="v accent" id="hl">—</div></div>
      <div class="stat"><div class="k">標準偏差</div><div class="v" id="sd">—</div></div>
      <div class="stat"><div class="k">人数</div><div class="v" id="n">—</div></div></div>''',
  article='''    <h2>計算する指標</h2>
    <div class="note"><strong>計算式</strong><br>平均 ＝ 合計 ÷ 人数／標準偏差 ＝ √(各点と平均の差の2乗の平均)</div>
    <p>平均点だけでなく、標準偏差（点数のばらつき）を見ると、問題の難易度やクラスの理解の幅が分かります。範囲（最高−最低）も指導の参考に。</p>
    <h2>よくある質問</h2>'''+faq([('偏差値は出る？','個人の偏差値は「偏差値計算シミュ」をご利用ください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const arr=($('scores').value.match(/-?\\d+(?:\\.\\d+)?/g)||[]).map(Number);
    if(!arr.length){alert('点数を入力してね');return;}
    const n=arr.length, sum=arr.reduce((a,b)=>a+b,0), mean=sum/n;
    const sd=Math.sqrt(arr.reduce((a,b)=>a+(b-mean)*(b-mean),0)/n);
    $('sub').textContent=`${n}人ぶんの点数から`;
    $('hl').textContent=Math.max(...arr)+' / '+Math.min(...arr); $('sd').textContent=sd.toFixed(1); $('n').textContent=n+'人';
    SHARE=`テスト統計シミュ、平均${mean.toFixed(1)}点・標準偏差${sd.toFixed(1)}でした📈`;
    show(); anim($('big'),0,mean,800,1);
  }''')

add(id='naishin-keisan', cat=T, emoji='🎯',
  title='内申点 計算シミュレーター｜9教科の評定から内申点を算出｜シミュラボ',
  desc='主要5教科・実技4教科の評定合計と傾斜配点から、高校受験で使われる内申点（調査書点）の目安を計算する無料ツール。',
  ogtitle='内申点 計算シミュレーター｜内申点を算出', ogdesc='9教科の評定と傾斜配点から内申点の目安を計算。',
  h1='内申点 計算シミュレーター',
  lead='9教科の評定から内申点（調査書点）の目安を計算します。実技教科を2倍にする傾斜配点にも対応。受験指導・進路相談の準備に。',
  inputs='''    <h2>🎯 評定を入れる</h2>
    <div class="row"><div class="field"><label>主要5教科の評定合計 <span class="hint">（最大25）</span></label><input type="number" id="main" value="18" min="0" max="25" inputmode="numeric"></div>
    <div class="field"><label>実技4教科の評定合計 <span class="hint">（最大20）</span></label><input type="number" id="jitsu" value="14" min="0" max="20" inputmode="numeric"></div></div>
    <div class="field"><label>実技教科の傾斜</label><select id="kei"><option value="1">傾斜なし（9教科×5＝45満点）</option><option value="2" selected>実技2倍（多くの公立で採用）</option></select></div>
    <button class="btn btn-primary" id="calcBtn">内申点を計算する</button>''',
  result='''      <div class="label">内申点の目安</div>
      <div class="big"><span id="big">0</span><span class="unit">点</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">満点</div><div class="v accent" id="man">—</div></div>
      <div class="stat"><div class="k">主要5教科</div><div class="v" id="mv">—</div></div>
      <div class="stat"><div class="k">実技4教科(傾斜後)</div><div class="v" id="jv">—</div></div></div>''',
  article='''    <h2>内申点とは</h2>
    <div class="note"><strong>計算式</strong><br>内申点 ＝ 主要5教科の評定合計 ＋ 実技4教科の評定合計 × 傾斜<br>傾斜なし=45満点／実技2倍=65満点（自治体により異なる）</div>
    <p>内申点（調査書点）の計算方法は都道府県で大きく異なります。本ツールは代表的なパターンの目安です。正確な計算は各自治体の選抜要項をご確認ください。</p>
    <h2>よくある質問</h2>'''+faq([('うちの県と違う','自治体ごとに学年の重みや満点が異なります。目安としてお使いください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const m=Math.max(0,+$('main').value||0),j=Math.max(0,+$('jitsu').value||0),k=+$('kei').value||1;
    const score=m+j*k, man=25+20*k;
    $('sub').textContent=`実技${k===2?'2倍':'傾斜なし'}`;
    $('man').textContent=man+'点満点'; $('mv').textContent=m+'点'; $('jv').textContent=(j*k)+'点';
    SHARE=`内申点 計算シミュ、内申点は${score}点（${man}点満点）でした🎯`;
    show(); anim($('big'),0,score,800);
  }''')

add(id='shoken-jitan', cat=T, emoji='📝',
  title='所見作成 時短シミュレーター｜通知表の所見、何時間かかってる？｜シミュラボ',
  desc='児童生徒数と1人あたりの所見作成時間から、所見づくりの総作業時間と、ツール活用でどれだけ時短できるかを試算する先生向け無料ツール。',
  ogtitle='所見作成 時短シミュレーター｜何時間かかってる？', ogdesc='人数と1人の所見時間から総作業時間と時短効果を試算。',
  h1='所見作成 時短シミュレーター',
  lead='通知表の所見、クラス全員分で何時間かかっていますか？人数と1人あたりの時間から総作業時間を計算。作成ツールを使った場合の時短効果も出します。',
  inputs='''    <h2>📝 条件を入れる</h2>
    <div class="row"><div class="field"><label>児童生徒数 <span class="hint">（人）</span></label><input type="number" id="n" value="35" min="1" inputmode="numeric"></div>
    <div class="field"><label>1人の所見にかかる時間 <span class="hint">（分）</span></label><input type="number" id="min" value="15" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>ツール活用で1人あたり <span class="hint">（分・目安5分）</span></label><input type="number" id="tool" value="5" min="0" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">作業時間を見る</button>''',
  result='''      <div class="label">所見づくりの総作業時間</div>
      <div class="big"><span id="big">0</span><span class="unit">時間</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">ツール活用なら</div><div class="v accent" id="after">—</div></div>
      <div class="stat"><div class="k">短縮できる時間</div><div class="v" id="save">—</div></div>
      <div class="stat"><div class="k">学期3回ぶん短縮</div><div class="v" id="year">—</div></div></div>''',
  article='''    <h2>所見作成の負担</h2>
    <div class="note"><strong>計算式</strong><br>総作業時間 ＝ 人数 × 1人の所見時間／短縮 ＝（現状 − ツール活用時）× 人数</div>
    <p>所見作成は学期末の大きな負担。文例から選んで整える「所見作成ツール」を使うと、1人あたりの時間をぐっと縮められます。浮いた時間を子どもと向き合う時間に。</p>
    <h2>よくある質問</h2>'''+faq([('質は落ちない？','文例をベースに自分の言葉で調整すれば、質を保ちつつ時短できます。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const n=Math.max(0,+$('n').value||0),mi=Math.max(0,+$('min').value||0),t=Math.max(0,+$('tool').value||0);
    const total=n*mi/60, after=n*t/60, save=total-after;
    $('sub').textContent=`${n}人 × ${mi}分`;
    $('after').textContent=after.toFixed(1)+'時間'; $('save').textContent=save.toFixed(1)+'時間'; $('year').textContent=(save*3).toFixed(1)+'時間';
    SHARE=`所見作成 時短シミュ、今は${total.toFixed(1)}時間→ツール活用で${after.toFixed(1)}時間に📝（${save.toFixed(1)}時間の時短！）`;
    show(); anim($('big'),0,total,800,1);
  }''')

add(id='saiten-jikan', cat=T, emoji='✅',
  title='採点時間シミュレーター｜テスト採点、何時間かかる？｜シミュラボ',
  desc='人数・問題数・1問あたりの採点時間から、テスト採点にかかる総時間を試算する先生向け無料ツール。',
  ogtitle='採点時間シミュレーター｜採点に何時間？', ogdesc='人数・問題数・1問の採点時間から総採点時間を試算。',
  h1='採点時間シミュレーター',
  lead='そのテスト、採点に何時間かかる？人数・問題数・1問あたりの採点時間から、総採点時間を見積もります。テスト設計や時間確保の目安に。',
  inputs='''    <h2>✅ 条件を入れる</h2>
    <div class="row"><div class="field"><label>人数 <span class="hint">（人）</span></label><input type="number" id="n" value="35" min="1" inputmode="numeric"></div>
    <div class="field"><label>問題数 <span class="hint">（問）</span></label><input type="number" id="q" value="25" min="1" inputmode="numeric"></div></div>
    <div class="field"><label>1問あたりの採点時間 <span class="hint">（秒）</span></label><input type="number" id="sec" value="8" min="1" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">採点時間を見る</button>''',
  result='''      <div class="label">採点にかかる総時間</div>
      <div class="big"><span id="big">0</span><span class="unit">時間</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1人あたり</div><div class="v" id="per">—</div></div>
      <div class="stat"><div class="k">採点する答案の数</div><div class="v accent" id="total">—</div></div>
      <div class="stat"><div class="k">分にすると</div><div class="v" id="mn">—</div></div></div>''',
  article='''    <h2>計算式</h2>
    <div class="note"><strong>計算式</strong><br>総採点時間 ＝ 人数 × 問題数 × 1問の採点時間</div>
    <p>記述問題が多いと1問あたりの時間が伸びます。選択・短答を増やす、ルーブリックを用意する、などで採点時間は短縮できます。観点別の集計とあわせて計画を。</p>
    <h2>よくある質問</h2>'''+faq([('記述の採点は？','1問あたりの秒数を長め（30〜60秒）に設定して見積もってください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const n=Math.max(0,+$('n').value||0),q=Math.max(0,+$('q').value||0),s=Math.max(0,+$('sec').value||0);
    const totalSec=n*q*s, h=totalSec/3600;
    $('sub').textContent=`${n}人 × ${q}問 × ${s}秒`;
    $('per').textContent=num(q*s/60)+'分'; $('total').textContent=num(n*q)+'問'; $('mn').textContent=num(totalSec/60)+'分';
    SHARE=`採点時間シミュ、このテストの採点は約${h.toFixed(1)}時間かかる計算でした✅`;
    show(); anim($('big'),0,h,800,1);
  }''')

add(id='sekigae-pattern', cat=T, emoji='🔀',
  title='席替えパターン数シミュレーター｜何通りの席順がある？｜シミュラボ',
  desc='クラスの人数から、席替えの並び方が何通りあるか（順列）を計算するエンタメ教員向けツール。天文学的な数を体感できます。',
  ogtitle='席替えパターン数｜何通りの席順がある？', ogdesc='人数から席替えの並び方の通り数を計算。',
  h1='席替えパターン数シミュレーター',
  lead='クラスの席替え、全部で何通りある？人数から並び方（順列＝人数の階乗）を計算します。結果は天文学的——子どもに見せると盛り上がります。',
  inputs='''    <h2>🔀 人数を入れる</h2>
    <div class="field"><label>クラスの人数 <span class="hint">（人）</span></label><input type="number" id="n" value="30" min="1" max="100" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">パターン数を見る</button>''',
  result='''      <div class="label">席順のパターン数</div>
      <div class="big" style="font-size:34px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">桁数</div><div class="v accent" id="keta">—</div></div>
      <div class="stat"><div class="k">毎日変えても</div><div class="v" id="days">—</div></div>
      <div class="stat"><div class="k">宇宙の星(約10²²個)と</div><div class="v" id="uni">—</div></div></div>''',
  article='''    <h2>階乗のすごさ</h2>
    <div class="note"><strong>計算式</strong><br>パターン数 ＝ 人数の階乗（n!）＝ n × (n−1) × … × 2 × 1</div>
    <p>30人なら約2.65×10³²通り。毎日席替えしても、宇宙が終わっても回りきれません。「組み合わせの爆発」を実感できる、算数・数学の導入ネタにもぴったりです。</p>
    <h2>よくある質問</h2>'''+faq([('正確な数は？','桁が大きすぎるため、指数表記（×10のN乗）で表示しています。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const n=Math.max(1,Math.min(100,+$('n').value||1));
    let L=0; for(let k=2;k<=n;k++) L+=Math.log10(k);
    const exp=Math.floor(L), mant=Math.pow(10,L-exp);
    const keta=exp+1;
    $('big').textContent=mant.toFixed(2)+' × 10^'+exp+' 通り';
    $('sub').textContent=`${n}人の席替え（${n}! 通り）`;
    $('keta').textContent=keta+'桁'; $('days').textContent='回りきれない'; $('uni').textContent=(exp>=22?'比べ物にならない多さ':'星より少ない');
    SHARE=`席替えパターン数シミュ、${n}人だと約 ${mant.toFixed(2)}×10^${exp} 通り🔀 宇宙の星より多い…！`;
    show();
  }''')

add(id='class-kumiawase', cat=T, emoji='🧩',
  title='クラス分け組み合わせシミュレーター｜何通りの分け方がある？｜シミュラボ',
  desc='学年の人数とクラス数から、クラス分け（組み分け）の組み合わせが何通りあるかを計算する教員向けツール。クラス編成の大変さを可視化。',
  ogtitle='クラス分け組み合わせ｜何通りの分け方？', ogdesc='人数とクラス数からクラス分けの組み合わせ数を計算。',
  h1='クラス分け組み合わせシミュレーター',
  lead='学年をクラスに分ける方法は何通り？人数とクラス数から組み合わせの数を計算します。クラス編成がいかに大変か（組み合わせ爆発）が分かります。',
  inputs='''    <h2>🧩 条件を入れる</h2>
    <div class="row"><div class="field"><label>学年の人数 <span class="hint">（人）</span></label><input type="number" id="n" value="80" min="2" max="400" inputmode="numeric"></div>
    <div class="field"><label>クラス数 <span class="hint">（クラス）</span></label><input type="number" id="c" value="2" min="2" max="12" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">組み合わせ数を見る</button>''',
  result='''      <div class="label">クラス分けの組み合わせ</div>
      <div class="big" style="font-size:34px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">桁数</div><div class="v accent" id="keta">—</div></div>
      <div class="stat"><div class="k">1クラスの人数</div><div class="v" id="size">—</div></div>
      <div class="stat"><div class="k">手作業だと</div><div class="v" id="hand">—</div></div></div>''',
  article='''    <h2>クラス編成は組み合わせの嵐</h2>
    <div class="note"><strong>計算の考え方</strong><br>n人を均等なクラスに分ける場合の組み合わせ数（多項係数）を概算しています。実際は成績・性別・人間関係などの条件が加わり、さらに複雑になります。</div>
    <p>条件を満たすクラス分けを手作業で探すのは至難の業。だからこそ、条件を考慮して自動で分けるツールの出番です。組み合わせ爆発を体感してみてください。</p>
    <h2>よくある質問</h2>'''+faq([('条件付きだと？','成績均等・男女比・NG関係などの条件が入ると、現実的な候補はぐっと絞られます。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const n=Math.max(2,+$('n').value||2),c=Math.max(2,+$('c').value||2);
    const size=Math.round(n/c);
    // 多項係数 n! / (size!^c) を log10 で概算
    let L=0; for(let k=2;k<=n;k++) L+=Math.log10(k);
    let Ls=0; for(let k=2;k<=size;k++) Ls+=Math.log10(k);
    L-=Ls*c; if(L<0)L=0;
    const exp=Math.floor(L), mant=Math.pow(10,L-exp);
    $('big').textContent=(exp>=2?mant.toFixed(2)+' × 10^'+exp:Math.round(Math.pow(10,L)))+' 通り';
    $('sub').textContent=`${n}人を${c}クラスに`;
    $('keta').textContent=(exp+1)+'桁'; $('size').textContent='約'+size+'人'; $('hand').textContent='探すのは至難';
    SHARE=`クラス分け組み合わせシミュ、${n}人を${c}クラスは約 ${mant.toFixed(2)}×10^${exp} 通り🧩 編成って大変…！`;
    show();
  }''')

add(id='han-wake', cat=T, emoji='👥',
  title='班分けシミュレーター｜何班になる？余りは？｜シミュラボ',
  desc='クラスの人数と1班の人数から、班の数・余りの人数・班ごとの人数の調整方法を表示する先生向け無料ツール。',
  ogtitle='班分けシミュレーター｜何班になる？', ogdesc='人数と1班の人数から班の数・余りを計算。',
  h1='班分けシミュレーター',
  lead='グループ活動や給食の班、何班になる？人数と1班の人数から、班の数と余りの人数、調整の目安を出します。',
  inputs='''    <h2>👥 条件を入れる</h2>
    <div class="row"><div class="field"><label>クラスの人数 <span class="hint">（人）</span></label><input type="number" id="n" value="36" min="1" inputmode="numeric"></div>
    <div class="field"><label>1班の人数 <span class="hint">（人）</span></label><input type="number" id="g" value="4" min="1" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">班分けを見る</button>''',
  result='''      <div class="label">できる班の数</div>
      <div class="big"><span id="big">0</span><span class="unit">班</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">余りの人数</div><div class="v accent" id="amari">—</div></div>
      <div class="stat"><div class="k">調整案</div><div class="v" id="plan">—</div></div>
      <div class="stat"><div class="k">1班</div><div class="v" id="size">—</div></div></div>''',
  article='''    <h2>班分けの考え方</h2>
    <div class="note"><strong>計算式</strong><br>班の数 ＝ 人数 ÷ 1班の人数（あまりは数班に1人ずつ振り分け）</div>
    <p>きっちり割り切れないときは、余りを数班に1人ずつ足すのが定番。人数の偏りが出ないよう調整しましょう。係や役割分担の計画にも。</p>
    <h2>よくある質問</h2>'''+faq([('均等にしたい','余りの人数を、班数のうち何班かに1人ずつ加えると均等に近づきます。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const n=Math.max(1,+$('n').value||1),g=Math.max(1,+$('g').value||1);
    const groups=Math.floor(n/g), amari=n%g;
    $('sub').textContent=`${n}人 ÷ 1班${g}人`;
    $('amari').textContent=amari+'人'; $('plan').textContent= amari===0?'ぴったり！':amari+'班を'+(g+1)+'人に'; $('size').textContent=g+'人';
    SHARE=`班分けシミュ、${n}人を${g}人班にすると${groups}班（余り${amari}人）でした👥`;
    show(); anim($('big'),0,groups,800);
  }''')

add(id='shusseki-ritsu', cat=T, emoji='📅',
  title='出席率シミュレーター｜欠席日数から出席率を計算｜シミュラボ',
  desc='授業日数と欠席日数から、出席率と「皆勤まであと何日休めるか」の目安を計算する先生・保護者向け無料ツール。',
  ogtitle='出席率シミュレーター｜出席率を計算', ogdesc='授業日数と欠席日数から出席率を計算。',
  h1='出席率シミュレーター',
  lead='授業日数と欠席日数から、出席率を計算します。進級・進学の出席要件の確認や、保護者面談の資料づくりに。',
  inputs='''    <h2>📅 条件を入れる</h2>
    <div class="row"><div class="field"><label>授業日数（これまで） <span class="hint">（日）</span></label><input type="number" id="total" value="120" min="1" inputmode="numeric"></div>
    <div class="field"><label>欠席日数 <span class="hint">（日）</span></label><input type="number" id="abs" value="5" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>年間の授業日数 <span class="hint">（日・見込み）</span></label><input type="number" id="year" value="200" min="1" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">出席率を見る</button>''',
  result='''      <div class="label">現在の出席率</div>
      <div class="big"><span id="big">0</span><span class="unit">%</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">出席日数</div><div class="v" id="att">—</div></div>
      <div class="stat"><div class="k">年間で9割維持には</div><div class="v accent" id="keep">—</div></div>
      <div class="stat"><div class="k">欠席日数</div><div class="v" id="absv">—</div></div></div>''',
  article='''    <h2>出席率の計算方法</h2>
    <div class="note"><strong>計算式</strong><br>出席率（％）＝（授業日数 − 欠席日数）÷ 授業日数 × 100</div>
    <p>出席率は「これまでの授業日数のうち、実際に出席した日数の割合」です。たとえば授業日数120日で欠席が5日なら、出席率は (120−5)÷120×100 ＝ <b>約95.8％</b> になります。進級・進学・皆勤の判定、保護者面談の資料づくりなどに使われる基本の数字です。</p>
    <h2>出席率の早見表（年間200日の場合）</h2>
    <p>年間授業日数を200日としたときの、欠席日数ごとの出席率の目安です。自分の状況に近いところを確認してみてください。</p>
    <div style="overflow-x:auto;">
    <table>
    <thead><tr><th>欠席日数</th><th>出席率</th><th>目安</th></tr></thead>
    <tbody>
    <tr><td>0日</td><td>100%</td><td>皆勤</td></tr>
    <tr><td>5日</td><td>97.5%</td><td>非常に良好</td></tr>
    <tr><td>10日</td><td>95.0%</td><td>良好</td></tr>
    <tr><td>20日</td><td>90.0%</td><td>ひとつの目安ライン</td></tr>
    <tr><td>40日</td><td>80.0%</td><td>注意（要件に注意）</td></tr>
    <tr><td>60日</td><td>70.0%</td><td>進級・単位に影響も</td></tr>
    </tbody>
    </table>
    </div>
    <h2>学校段階別・出席率の考え方</h2>
    <p>出席日数・出席率の「基準」は学校や自治体、大学の学部によって大きく異なります。あくまで一般的な傾向として、次のような違いがあります（正確な基準は必ず在籍校の規定をご確認ください）。</p>
    <ul>
    <li><b>小学校・中学校</b>……義務教育のため出席率だけで留年になることは通常ありませんが、欠席が続くと「欠席日数」が指導要録に記録されます。年間30日以上の欠席は「不登校」の目安とされます。</li>
    <li><b>高校</b>……多くの学校で、各科目の「出席時数が規定の3分の2以上（欠席が3分の1を超えない）」などの要件があり、満たさないと単位が認定されず進級・卒業に影響することがあります。</li>
    <li><b>大学</b>……科目ごとに「全授業回数の3分の2以上の出席」を単位認定の条件とすることが一般的です。</li>
    </ul>
    <h2>関連する出席の計算ツール</h2>
    <p>目的に合わせて、次のツールもあわせてご利用ください。</p>
    <ul>
    <li><a href="/sims/hisho-nissu/">必要出席日数 計算</a>……目標の出席率まで「あと何日出席が必要か」を計算</li>
    <li><a href="/sims/kaikin-hantei/">皆勤・精勤 判定</a>……欠席・遅刻の数から皆勤／精勤を判定</li>
    <li><a href="/sims/shinkyu-hantei/">進級・卒業の出席条件 判定</a>……「3分の2以上」などの出席要件を満たしているかチェック</li>
    <li><a href="/sims/chiko-soutai/">遅刻・早退→欠席換算</a>……遅刻・早退を欠席に換算して実質出席率を計算</li>
    </ul>
    <h2>よくある質問</h2>'''+faq([
    ('出席率は何％あればいい？','学校段階や学校の規定によって異なります。高校・大学では「3分の2以上（約66.7％以上）」を単位・進級の要件とすることが多いですが、必ず在籍校の規定をご確認ください。'),
    ('遅刻・早退はどう数える？','本ツールは欠席日数のみで計算します。遅刻・早退を欠席に換算したい場合は、'+'<a href="/sims/chiko-soutai/">遅刻・早退→欠席換算</a>ツールをご利用ください。換算ルールは校則に従ってください。'),
    ('欠席が何日まで大丈夫か知りたい','年間授業日数を入れると「9割維持まであと何日休めるか」の目安を表示します。目標出席率で細かく計算したい場合は'+'<a href="/sims/kaikin-hantei/">皆勤・精勤 判定</a>や'+'<a href="/sims/hisho-nissu/">必要出席日数 計算</a>もどうぞ。'),
    ('出席停止（インフルエンザ等）は欠席になる？','学校保健安全法に基づく出席停止や忌引きは「欠席日数」に含めない扱いが一般的ですが、記録の仕方は学校によります。詳しくは学校にご確認ください。'),
    ('データは送信されますか？','いいえ。計算はすべてあなたのブラウザ内で完結します。')]),
  js='''  function calc(){
    const t=Math.max(1,+$('total').value||1),a=Math.max(0,+$('abs').value||0),y=Math.max(1,+$('year').value||1);
    const rate=(t-a)/t*100, canAbs=Math.floor(y*0.1)-a;
    $('sub').textContent=`${t}日中 ${a}日欠席`;
    $('att').textContent=(t-a)+'日'; $('keep').textContent='あと'+Math.max(0,canAbs)+'日まで'; $('absv').textContent=a+'日';
    SHARE=`出席率シミュ、現在の出席率は${rate.toFixed(1)}%でした📅`;
    show(); anim($('big'),0,rate,800,1);
  }''')

add(id='print-cost', cat=T, emoji='🖨️',
  title='プリント印刷枚数・コストシミュレーター｜年間で何枚刷ってる？｜シミュラボ',
  desc='クラス人数・1日のプリント枚数・年間授業日数から、年間の印刷枚数・紙の費用・積み上げた高さを計算する先生向け無料ツール。',
  ogtitle='プリント印刷枚数・コスト｜年間で何枚？', ogdesc='人数・1日の枚数・授業日数から年間の印刷枚数を計算。',
  h1='プリント印刷枚数・コストシミュレーター',
  lead='毎日のプリント、年間で何枚刷っている？人数・1日の枚数・授業日数から、年間の印刷枚数とコスト、積み上げた高さを出します。ペーパーレス検討の参考に。',
  inputs='''    <h2>🖨️ 条件を入れる</h2>
    <div class="row"><div class="field"><label>クラス人数 <span class="hint">（人）</span></label><input type="number" id="n" value="35" min="1" inputmode="numeric"></div>
    <div class="field"><label>1日のプリント枚数 <span class="hint">（枚/人）</span></label><input type="number" id="d" value="3" min="0" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>年間授業日数 <span class="hint">（日）</span></label><input type="number" id="days" value="200" min="1" inputmode="numeric"></div>
    <div class="field"><label>1枚あたりコスト <span class="hint">（円・紙+トナー）</span></label><input type="number" id="cost" value="1.5" min="0" step="0.1" inputmode="decimal"></div></div>
    <button class="btn btn-primary" id="calcBtn">年間の印刷量を見る</button>''',
  result='''      <div class="label">年間の印刷枚数</div>
      <div class="big"><span id="big">0</span><span class="unit">枚</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">年間コスト</div><div class="v accent" id="costv">—</div></div>
      <div class="stat"><div class="k">積むと高さ</div><div class="v" id="height">—</div></div>
      <div class="stat"><div class="k">1日あたり</div><div class="v" id="day">—</div></div></div>''',
  article='''    <h2>計算式</h2>
    <div class="note"><strong>計算式</strong><br>年間枚数 ＝ 人数 × 1日の枚数 × 年間授業日数<br>高さ ＝ 枚数 × 0.1mm（コピー用紙1枚）</div>
    <p>意外と膨大な印刷量。タブレット配信やデジタル教材に一部を置き換えると、コストも準備時間も削減できます。環境にもやさしい選択です。</p>
    <h2>よくある質問</h2>'''+faq([('両面印刷なら？','枚数（用紙数）で入れれば、両面でもそのままの枚数で計算されます。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const n=Math.max(0,+$('n').value||0),d=Math.max(0,+$('d').value||0),days=Math.max(0,+$('days').value||0),c=Math.max(0,+$('cost').value||0);
    const sheets=n*d*days, cost=sheets*c, hcm=sheets*0.1/10;
    $('sub').textContent=`${n}人 × ${d}枚 × ${days}日`;
    $('costv').textContent=yen(cost); $('height').textContent=(hcm/100).toFixed(1)+'m'; $('day').textContent=num(n*d)+'枚';
    SHARE=`プリント印刷シミュ、年間で約${num(sheets)}枚・${yen(cost)}・積むと${(hcm/100).toFixed(1)}mの高さでした🖨️`;
    show(); anim($('big'),0,sheets,800);
  }''')

add(id='wasure-kyokusen', cat=T, emoji='🧠',
  title='忘却曲線シミュレーター｜復習しないとどれだけ忘れる？｜シミュラボ',
  desc='エビングハウスの忘却曲線をもとに、復習なし／適切な復習ありで1ヶ月後にどれだけ記憶が残るかを比較する先生・学習者向け無料ツール。',
  ogtitle='忘却曲線シミュレーター｜復習でどれだけ残る？', ogdesc='復習なし／ありで1ヶ月後の定着率を比較。',
  h1='忘却曲線シミュレーター',
  lead='覚えたことは、復習しないとどんどん忘れていきます。エビングハウスの忘却曲線をもとに、復習なし／復習ありで1ヶ月後にどれだけ残るかを比較します。',
  inputs='''    <h2>🧠 条件を入れる</h2>
    <div class="field"><label>覚えた項目数 <span class="hint">（個・単語や用語など）</span></label><input type="number" id="items" value="50" min="1" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">1ヶ月後を見る</button>''',
  result='''      <div class="label">復習ありで1ヶ月後に残る数</div>
      <div class="big"><span id="big">0</span><span class="unit">個</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">復習なしだと</div><div class="v accent" id="no">—</div></div>
      <div class="stat"><div class="k">その差</div><div class="v" id="diff">—</div></div>
      <div class="stat"><div class="k">おすすめ復習日</div><div class="v" id="when">—</div></div></div>''',
  article='''    <h2>忘却曲線と分散学習</h2>
    <div class="note"><strong>目安</strong><br>復習しないと1ヶ月後の定着は約2割。翌日・1週間後・1ヶ月後など間隔をあけて復習（分散学習）すると、約9割を保てると言われます。</div>
    <p>「忘れる前に復習」より「忘れかけた頃に復習」が効果的。授業の最後の振り返り、翌日の小テスト、週末のまとめ——タイミングを設計すると定着がぐっと上がります。</p>
    <h2>よくある質問</h2>'''+faq([('正確な数値？','研究にもとづく目安です。個人差や内容で変わります。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const it=Math.max(0,+$('items').value||0);
    const no=Math.round(it*0.21), yes=Math.round(it*0.9);
    $('sub').textContent=`${it}個 覚えた場合`;
    $('no').textContent=no+'個'; $('diff').textContent='+'+(yes-no)+'個'; $('when').textContent='翌日・1週間・1ヶ月後';
    SHARE=`忘却曲線シミュ、${it}個覚えても復習なしだと1ヶ月後は約${no}個だけ…復習ありなら${yes}個🧠`;
    show(); anim($('big'),0,yes,800);
  }''')

add(id='hensachi', cat=T, emoji='📐',
  title='偏差値計算シミュレーター｜点数・平均・標準偏差から偏差値を｜シミュラボ',
  desc='自分の点数とクラスの平均点・標準偏差から、偏差値と上位何％かの目安を計算する先生・生徒向け無料ツール。',
  ogtitle='偏差値計算シミュレーター｜偏差値を計算', ogdesc='点数・平均・標準偏差から偏差値と上位％を計算。',
  h1='偏差値計算シミュレーター',
  lead='点数・平均点・標準偏差から、偏差値と「上位およそ何％か」を計算します。進路指導や、テスト結果の説明に。',
  inputs='''    <h2>📐 条件を入れる</h2>
    <div class="row"><div class="field"><label>あなたの点数</label><input type="number" id="score" value="70" min="0" inputmode="numeric"></div>
    <div class="field"><label>平均点</label><input type="number" id="mean" value="60" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>標準偏差 <span class="hint">（分からなければ15）</span></label><input type="number" id="sd" value="15" min="1" step="0.1" inputmode="decimal"></div>
    <button class="btn btn-primary" id="calcBtn">偏差値を計算する</button>''',
  result='''      <div class="label">あなたの偏差値</div>
      <div class="big"><span id="big">0</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">上位およそ</div><div class="v accent" id="top">—</div></div>
      <div class="stat"><div class="k">平均との差</div><div class="v" id="diff">—</div></div>
      <div class="stat"><div class="k">100人なら順位</div><div class="v" id="rank">—</div></div></div>''',
  article='''    <h2>偏差値の計算</h2>
    <div class="note"><strong>計算式</strong><br>偏差値 ＝ 50 ＋ 10 ×（点数 − 平均）÷ 標準偏差</div>
    <p>偏差値50が平均、60で上位約16％、70で上位約2％が目安。点数の分布が正規分布に近いほど精度が上がります。標準偏差が分からないときは15前後で概算を。</p>
    <h2>よくある質問</h2>'''+faq([('上位％はどう出す？','正規分布を仮定した近似で算出しています。実際の分布で多少ずれます。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const x=+$('score').value||0,m=+$('mean').value||0,sd=Math.max(0.1,+$('sd').value||1);
    const hensa=50+10*(x-m)/sd, z=(hensa-50)/10;
    // 正規分布の上側確率（近似）
    const cdf=0.5*(1+erf(z/Math.SQRT2)); const top=(1-cdf)*100;
    function erf(t){const s=t<0?-1:1;t=Math.abs(t);const a1=0.254829592,a2=-0.284496736,a3=1.421413741,a4=-1.453152027,a5=1.061405429,p=0.3275911;const u=1/(1+p*t);const y=1-(((((a5*u+a4)*u)+a3)*u+a2)*u+a1)*u*Math.exp(-t*t);return s*y;}
    $('sub').textContent=`点数${x}・平均${m}・標準偏差${sd}`;
    $('top').textContent=top.toFixed(1)+'%'; $('diff').textContent=(x-m>=0?'+':'')+(x-m)+'点'; $('rank').textContent=Math.max(1,Math.round(top))+'位くらい';
    SHARE=`偏差値計算シミュ、私の偏差値は${hensa.toFixed(1)}・上位約${top.toFixed(1)}%でした📐`;
    show(); anim($('big'),0,hensa,800,1);
  }''')

add(id='zangyo-kyoin', cat=T, emoji='⏰',
  title='教員の残業時間シミュレーター｜月の残業、何時間？｜シミュラボ',
  desc='出勤・退勤時刻と持ち帰り仕事の時間から、教員の1日・1ヶ月の時間外労働の目安を計算するツール。働き方を見つめ直すきっかけに。',
  ogtitle='教員の残業時間シミュレーター｜月何時間？', ogdesc='出退勤と持ち帰りから教員の残業時間を試算。',
  h1='教員の残業時間シミュレーター',
  lead='出勤・退勤時刻と持ち帰り仕事から、1日・1ヶ月の時間外労働の目安を出します。働き方を見直すきっかけに（所定労働は7時間45分で計算）。',
  inputs='''    <h2>⏰ 条件を入れる</h2>
    <div class="row"><div class="field"><label>出勤時刻</label><input type="time" id="in" value="07:45"></div>
    <div class="field"><label>退勤時刻</label><input type="time" id="out" value="19:00"></div></div>
    <div class="row"><div class="field"><label>休憩時間 <span class="hint">（分）</span></label><input type="number" id="rest" value="45" min="0" inputmode="numeric"></div>
    <div class="field"><label>持ち帰り仕事 <span class="hint">（分/日）</span></label><input type="number" id="home" value="30" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">残業時間を見る</button>''',
  result='''      <div class="label">1ヶ月の時間外労働</div>
      <div class="big"><span id="big">0</span><span class="unit">時間</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1日あたり</div><div class="v" id="day">—</div></div>
      <div class="stat"><div class="k">過労死ライン(月80h)</div><div class="v accent" id="line">—</div></div>
      <div class="stat"><div class="k">年間</div><div class="v" id="year">—</div></div></div>''',
  article='''    <h2>教員の働き方</h2>
    <div class="note"><strong>計算式</strong><br>1日の時間外 ＝（退勤 − 出勤 − 休憩）− 7時間45分 ＋ 持ち帰り<br>月 ＝ 1日 × 20日</div>
    <p>「過労死ライン」は月80時間が一つの目安とされます。本ツールで現状を可視化し、業務の見直し・分担・ICT活用（採点や所見の時短など）で負担軽減を。先生の健康が一番です。</p>
    <h2>よくある質問</h2>'''+faq([('部活動は？','退勤時刻に部活指導後の時間を含めて入れてください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const pin=($('in').value||'07:45').split(':').map(Number), pout=($('out').value||'19:00').split(':').map(Number);
    const inM=pin[0]*60+pin[1], outM=pout[0]*60+pout[1], rest=Math.max(0,+$('rest').value||0), home=Math.max(0,+$('home').value||0);
    let work=outM-inM-rest; if(work<0)work+=1440;
    const over=Math.max(0,work-465)+home; const monthH=over*20/60;
    $('sub').textContent=`実働${(work/60).toFixed(1)}h・所定7h45m`;
    $('day').textContent=(over/60).toFixed(1)+'時間'; $('line').textContent=monthH>=80?'超えています…':'あと'+(80-monthH).toFixed(0)+'h'; $('year').textContent=num(monthH*12)+'時間';
    SHARE=`教員の残業時間シミュ、月の時間外は約${monthH.toFixed(0)}時間でした⏰ 働き方、見直そう…`;
    show(); anim($('big'),0,monthH,800);
  }''')

add(id='tairyoku-hyouka', cat=T, emoji='🏃',
  title='体力テスト評価シミュレーター｜記録から評価の目安を｜シミュラボ',
  desc='シャトルラン・50m走・反復横跳びなどの記録から、体力テストの評価段階（A〜E）の目安を表示する先生・保護者向けツール。',
  ogtitle='体力テスト評価シミュレーター｜記録から評価', ogdesc='種目と記録から体力テストの評価段階の目安を表示。',
  h1='体力テスト評価シミュレーター',
  lead='シャトルラン・50m走・反復横跳びの記録から、評価段階の目安（A〜E）を表示します（中学生の一般的な目安。学年・性別で基準は異なります）。',
  inputs='''    <h2>🏃 条件を入れる</h2>
    <div class="field"><label>種目</label><select id="event"><option value="shuttle">20mシャトルラン（回）</option><option value="run50">50m走（秒）</option><option value="yoko">反復横跳び（点）</option></select></div>
    <div class="field"><label>記録</label><input type="number" id="rec" value="60" min="0" step="0.1" inputmode="decimal"></div>
    <button class="btn btn-primary" id="calcBtn">評価の目安を見る</button>''',
  result='''      <div class="label">評価の目安</div>
      <div class="big" style="font-size:48px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="adv" style="text-align:left;margin-top:18px;">—</div>''',
  article='''    <h2>体力テストの評価</h2>
    <div class="note"><strong>目安</strong><br>記録を5段階（A〜E）でざっくり評価します。本ツールは中学生の一般的な目安で、正式な評価は学年・性別ごとの基準表に従ってください。</div>
    <p>体力テストは、子どもの体力の現状を知り、運動の習慣づけにつなげるためのもの。評価そのものより、前回からの伸びや得意・苦手を見てあげるのが大切です。</p>
    <h2>よくある質問</h2>'''+faq([('学年・性別で違う？','はい。正式には基準表が分かれます。本ツールは大まかな目安です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const ev=$('event').value, r=+$('rec').value||0;
    let rank, higherBetter=true, th;
    if(ev==='shuttle'){th=[80,60,40,20];}
    else if(ev==='run50'){th=[7.5,8.3,9.1,10.0];higherBetter=false;}
    else {th=[55,48,41,34];}
    function grade(){ if(higherBetter){ if(r>=th[0])return'A'; if(r>=th[1])return'B'; if(r>=th[2])return'C'; if(r>=th[3])return'D'; return'E'; } else { if(r<=th[0])return'A'; if(r<=th[1])return'B'; if(r<=th[2])return'C'; if(r<=th[3])return'D'; return'E'; } }
    rank=grade();
    const msg={A:'すばらしい！得意分野ですね。',B:'良い記録。あと一歩でトップ層。',C:'平均的。コツコツ続けて伸ばそう。',D:'これから。少しずつ運動習慣を。',E:'まずは体を動かす楽しさから。'}[rank];
    $('big').textContent=rank;
    $('sub').textContent=`${sel('event').text}：${r}`;
    $('adv').textContent='🏃 '+msg;
    SHARE=`体力テスト評価シミュ、${sel('event').text}は評価「${rank}」でした🏃`;
    show();
  }''')

add(id='kyushoku-shukin', cat=T, emoji='💴',
  title='集金計算シミュレーター｜給食費・教材費の集金、合計いくら？｜シミュラボ',
  desc='1人あたりの月額と人数・集金月数から、クラスの集金総額・1人あたりの年額・未納時の不足額を計算する先生向け無料ツール。',
  ogtitle='集金計算シミュレーター｜集金の合計は？', ogdesc='月額と人数・月数からクラスの集金総額を計算。',
  h1='集金計算シミュレーター',
  lead='給食費・教材費などの集金、クラス合計でいくら？1人あたりの月額と人数・集金月数から、総額や1人の年額、未納が出たときの不足額を出します。',
  inputs='''    <h2>💴 条件を入れる</h2>
    <div class="row"><div class="field"><label>1人あたりの月額 <span class="hint">（円）</span></label><input type="number" id="m" value="4500" min="0" inputmode="numeric"></div>
    <div class="field"><label>人数 <span class="hint">（人）</span></label><input type="number" id="n" value="35" min="1" inputmode="numeric"></div></div>
    <div class="field"><label>集金する月数 <span class="hint">（ヶ月）</span></label><input type="number" id="months" value="11" min="1" max="12" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">集金額を見る</button>''',
  result='''      <div class="label">年間の集金総額（クラス）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">毎月の集金額</div><div class="v accent" id="mo">—</div></div>
      <div class="stat"><div class="k">1人の年額</div><div class="v" id="per">—</div></div>
      <div class="stat"><div class="k">未納1人で不足</div><div class="v" id="miss">—</div></div></div>''',
  article='''    <h2>計算式</h2>
    <div class="note"><strong>計算式</strong><br>年間総額 ＝ 1人の月額 × 人数 × 集金月数</div>
    <p>集金は金額が大きく、ミスが許されない業務。総額や1人あたりを事前に把握しておくと、徴収・管理がスムーズです。未納が出たときの不足額の確認にも。口座振替・キャッシュレス化の検討材料にも。</p>
    <h2>よくある質問</h2>'''+faq([('項目が複数ある','給食費・教材費など項目ごとに計算して合算してください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const m=Math.max(0,+$('m').value||0),n=Math.max(1,+$('n').value||1),mo=Math.max(1,+$('months').value||1);
    const total=m*n*mo, perYear=m*mo, monthly=m*n;
    $('sub').textContent=`月${num(m)}円 × ${n}人 × ${mo}ヶ月`;
    $('mo').textContent=yen(monthly); $('per').textContent=yen(perYear); $('miss').textContent=yen(perYear);
    SHARE=`集金計算シミュ、年間のクラス集金総額は${yen(total)}でした💴`;
    show(); anim($('big'),0,total,800);
  }''')

# ===== SEO穴場キーワード狙いの追加7本 =====
add(id='hyoutei-heikin', cat=T, emoji='🎓',
  title='評定平均値 計算シミュレーター｜推薦・指定校の評定平均をすぐ計算｜シミュラボ',
  desc='全科目の評定（5段階）を入力するだけで、大学推薦・指定校推薦の出願基準に使う「評定平均値（学習成績の状況）」を自動計算。基準クリアの目安も表示する無料ツール。',
  ogtitle='評定平均値 計算｜推薦・指定校の評定平均をすぐ計算', ogdesc='全科目の評定から評定平均値を自動計算。推薦基準の目安も。',
  h1='評定平均値 計算シミュレーター',
  lead='大学の指定校推薦・公募推薦で使う「評定平均値（学習成績の状況）」を、全科目の評定を貼り付けるだけで計算します。志望校の基準に届くかの目安もチェック。先生の進路指導・生徒の自己確認に。',
  inputs='''    <h2>🎓 評定を入力</h2>
    <div class="field"><label>全科目の評定（5・4・3…をカンマや改行で）</label><textarea id="hyotei" rows="4" style="width:100%;padding:12px;border:1.5px solid var(--line);border-radius:12px;font-size:15px;">5,4,4,5,3,4,4,5,4,3,4,4</textarea></div>
    <button class="btn btn-primary" id="calcBtn">評定平均値を計算する</button>''',
  result='''      <div class="label">評定平均値</div>
      <div class="big"><span id="big">0</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">科目数</div><div class="v" id="n">—</div></div>
      <div class="stat"><div class="k">評定の合計</div><div class="v" id="sum">—</div></div>
      <div class="stat"><div class="k">推薦の目安</div><div class="v accent" id="rank">—</div></div></div>''',
  article='''    <h2>評定平均値とは</h2>
    <div class="note"><strong>計算式</strong><br>評定平均値 ＝ 全科目の評定の合計 ÷ 科目数（小数第1位まで）</div>
    <p>高校3年間（または出願時まで）の全科目の評定を平均した数値で、大学の推薦入試で重視されます。指定校推薦は3.5〜4.3以上を基準にする大学が多く、評定平均値はA〜Eの段階にも区分されます（4.3以上=A、3.5以上=B…）。本ツールは目安です。正確な値は学校の調査書でご確認ください。</p>
    <h2>よくある質問</h2>'''+faq([('何年分を入れる？','一般に高1〜出願時までの全科目です。学校の指示に従ってください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const arr=($('hyotei').value.match(/[1-5](?:\\.\\d)?/g)||[]).map(Number);
    if(!arr.length){alert('評定を入力してね');return;}
    const n=arr.length, sum=arr.reduce((a,b)=>a+b,0), avg=sum/n;
    let r; if(avg>=4.3)r='A（4.3以上）'; else if(avg>=3.5)r='B（3.5以上）'; else if(avg>=2.7)r='C'; else if(avg>=1.9)r='D'; else r='E';
    $('sub').textContent=`${n}科目の評定から`;
    $('n').textContent=n+'科目'; $('sum').textContent=sum+'点'; $('rank').textContent=r;
    SHARE=`評定平均値 計算シミュ、評定平均は${avg.toFixed(1)}（区分${r.charAt(0)}）でした🎓`;
    show(); anim($('big'),0,avg,800,1);
  }''')

add(id='gpa', cat=T, emoji='📗',
  title='GPA計算ツール｜大学・高校のGPAを成績から自動計算｜シミュラボ',
  desc='秀・優・良・可（A・B・C・D）など成績の科目数を入れるだけで、GPA（評価平均）を自動計算する無料ツール。大学生・高校生・先生の成績管理に。',
  ogtitle='GPA計算ツール｜成績からGPAを自動計算', ogdesc='成績の科目数を入れるだけでGPAを自動計算。',
  h1='GPA計算ツール',
  lead='大学・高校の成績評価から「GPA」を計算します。秀＝4・優＝3・良＝2・可＝1として、それぞれの科目数を入れるだけ。奨学金・留学・院進の出願準備や成績管理に。',
  inputs='''    <h2>📗 成績の科目数を入れる</h2>
    <div class="row"><div class="field"><label>秀／S／A（4点）</label><input type="number" id="a" value="6" min="0" inputmode="numeric"></div>
    <div class="field"><label>優／B（3点）</label><input type="number" id="b" value="8" min="0" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>良／C（2点）</label><input type="number" id="c" value="4" min="0" inputmode="numeric"></div>
    <div class="field"><label>可／D（1点）</label><input type="number" id="d" value="2" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">GPAを計算する</button>''',
  result='''      <div class="label">あなたのGPA</div>
      <div class="big"><span id="big">0</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">総科目数</div><div class="v" id="n">—</div></div>
      <div class="stat"><div class="k">獲得ポイント計</div><div class="v" id="pt">—</div></div>
      <div class="stat"><div class="k">評価の目安</div><div class="v accent" id="rank">—</div></div></div>''',
  article='''    <h2>GPAの計算方法</h2>
    <div class="note"><strong>計算式</strong><br>GPA ＝（各評価のポイント × 科目数）の合計 ÷ 総科目数<br>一般的に 秀/S/A=4・優/B=3・良/C=2・可/D=1・不可=0</div>
    <p>GPA（Grade Point Average）は成績の平均値。奨学金・交換留学・大学院進学などで重視されます。4.0満点で、3.0以上あると評価されやすい目安。大学により単位数で重み付けする「単位加重GPA」を使う場合もあります（本ツールは科目数ベースの簡易版）。</p>
    <h2>よくある質問</h2>'''+faq([('単位数で重み付けは？','本ツールは科目数ベースの簡易計算です。厳密には単位数加重で計算する大学が多いです。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const a=Math.max(0,+$('a').value||0),b=Math.max(0,+$('b').value||0),c=Math.max(0,+$('c').value||0),d=Math.max(0,+$('d').value||0);
    const n=a+b+c+d, pt=a*4+b*3+c*2+d*1, gpa=n>0?pt/n:0;
    let r; if(gpa>=3.5)r='非常に優秀'; else if(gpa>=3.0)r='優秀'; else if(gpa>=2.0)r='標準'; else r='要努力';
    $('sub').textContent=`${n}科目の成績から`;
    $('n').textContent=n+'科目'; $('pt').textContent=pt+'pt'; $('rank').textContent=r;
    SHARE=`GPA計算ツール、私のGPAは${gpa.toFixed(2)}（${r}）でした📗`;
    show(); anim($('big'),0,gpa,800,2);
  }''')

add(id='jugyou-jisuu', cat=T, emoji='🗓️',
  title='年間授業時数シミュレーター｜標準授業時数を満たしてる？｜シミュラボ',
  desc='週の授業時数と実施週数から年間の授業時数を計算し、学年ごとの標準授業時数を満たしているか・過不足を確認できる先生向け無料ツール。',
  ogtitle='年間授業時数シミュレーター｜標準時数を満たしてる？', ogdesc='週時数と実施週数から年間授業時数と標準との過不足を計算。',
  h1='年間授業時数シミュレーター',
  lead='週の授業コマ数と実施週数から、年間の授業時数を計算。学年ごとの「標準授業時数」と比べて、足りているか・どれくらい余裕があるかを確認できます。年間指導計画づくりに。',
  inputs='''    <h2>🗓️ 条件を入れる</h2>
    <div class="field"><label>学年（標準授業時数）</label><select id="grade"><option value="850">小1（850）</option><option value="910">小2（910）</option><option value="980">小3（980）</option><option value="1015" selected>小4〜6（1015）</option><option value="1015">中学（1015）</option></select></div>
    <div class="row"><div class="field"><label>週の授業時数 <span class="hint">（コマ）</span></label><input type="number" id="week" value="29" min="1" inputmode="numeric"></div>
    <div class="field"><label>年間の実施週数 <span class="hint">（週）</span></label><input type="number" id="weeks" value="35" min="1" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">年間授業時数を見る</button>''',
  result='''      <div class="label">年間の実施授業時数</div>
      <div class="big"><span id="big">0</span><span class="unit">コマ</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">標準授業時数</div><div class="v" id="std">—</div></div>
      <div class="stat"><div class="k">過不足</div><div class="v accent" id="diff">—</div></div>
      <div class="stat"><div class="k">判定</div><div class="v" id="judge">—</div></div></div>''',
  article='''    <h2>標準授業時数とは</h2>
    <div class="note"><strong>計算式</strong><br>年間授業時数 ＝ 週の授業時数 × 実施週数<br>学習指導要領の標準授業時数：小4〜6・中学＝1015コマ（1コマ＝小45分・中50分）</div>
    <p>各学校は学習指導要領が定める「標準授業時数」を確保する必要があります。行事や休校で時数が不足しないよう、年間指導計画で管理します。本ツールは概算で、正確には教科ごとの時数管理が必要です。</p>
    <h2>よくある質問</h2>'''+faq([('教科ごとに見たい？','教科ごとの週コマ数で計算すると各教科の年間時数が出ます。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const std=+$('grade').value||1015, week=Math.max(1,+$('week').value||1), weeks=Math.max(1,+$('weeks').value||1);
    const total=week*weeks, diff=total-std;
    $('sub').textContent=`週${week}コマ × ${weeks}週`;
    $('std').textContent=std+'コマ'; $('diff').textContent=(diff>=0?'+':'')+diff+'コマ'; $('judge').textContent= diff>=0?'確保できる見込み✓':'不足の可能性';
    SHARE=`年間授業時数シミュ、年間${total}コマ（標準${std}に対し${diff>=0?'+':''}${diff}）でした🗓️`;
    show(); anim($('big'),0,total,800);
  }''')

add(id='kekka-tani', cat=T, emoji='⚠️',
  title='欠課時数・単位シミュレーター｜あと何回休むと単位が危ない？｜シミュラボ',
  desc='科目の年間授業時数と現在の欠課時数、欠課上限の割合から、単位修得のためにあと何回まで休めるかを計算する高校生・先生向け無料ツール。',
  ogtitle='欠課時数・単位シミュレーター｜あと何回休める？', ogdesc='年間時数と欠課数から、単位を落とさず休める残り回数を計算。',
  h1='欠課時数・単位シミュレーター',
  lead='高校で「欠時オーバー」して単位を落とすのが心配な人へ。科目の年間授業時数と今の欠課時数から、あと何回まで休めるか（単位修得ライン）を計算します。',
  inputs='''    <h2>⚠️ 条件を入れる</h2>
    <div class="row"><div class="field"><label>その科目の年間授業時数 <span class="hint">（コマ）</span></label><input type="number" id="total" value="70" min="1" inputmode="numeric"></div>
    <div class="field"><label>これまでの欠課時数 <span class="hint">（コマ）</span></label><input type="number" id="abs" value="10" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>欠課できる上限の割合 <span class="hint">（％・校則。一般に1/3＝33%）</span></label><input type="number" id="limit" value="33" min="1" max="100" inputmode="numeric"></div>
    <button class="btn btn-primary" id="calcBtn">あと何回休めるか見る</button>''',
  result='''      <div class="label">あと休める回数</div>
      <div class="big"><span id="big">0</span><span class="unit">コマ</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">欠課の上限</div><div class="v" id="max">—</div></div>
      <div class="stat"><div class="k">現在の欠課</div><div class="v" id="now">—</div></div>
      <div class="stat"><div class="k">状態</div><div class="v accent" id="judge">—</div></div></div>''',
  article='''    <h2>欠課と単位修得</h2>
    <div class="note"><strong>計算式</strong><br>欠課の上限 ＝ 年間授業時数 × 上限の割合<br>あと休める ＝ 上限 − これまでの欠課</div>
    <p>高校は科目ごとに出席時数が単位修得の条件になっており、欠課が一定（多くは総時数の3分の1）を超えると単位を落とす（原級留置の原因に）ことがあります。基準は学校で異なるので、必ず校則・担任に確認を。本ツールは目安です。</p>
    <h2>よくある質問</h2>'''+faq([('遅刻・早退は？','学校により「3回で1欠課」など換算があります。校則に従ってください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const total=Math.max(1,+$('total').value||1), abs=Math.max(0,+$('abs').value||0), lim=Math.max(1,Math.min(100,+$('limit').value||33))/100;
    const max=Math.floor(total*lim), left=max-abs;
    let j; if(left<0)j='上限超過の可能性…要相談'; else if(left<=2)j='危険ライン！注意'; else if(left<=5)j='余裕少なめ'; else j='まだ余裕あり';
    $('sub').textContent=`年間${total}コマ・上限${Math.round(lim*100)}%`;
    $('max').textContent=max+'コマ'; $('now').textContent=abs+'コマ'; $('judge').textContent=j;
    SHARE=`欠課時数・単位シミュ、あと${Math.max(0,left)}回まで休める計算でした⚠️（${j}）`;
    show(); anim($('big'),0,Math.max(0,left),800);
  }''')

add(id='kyoin-kyuryo', cat=T, emoji='💴',
  title='教員の給料シミュレーター｜号俸・経験年数から月給の目安｜シミュラボ',
  desc='経験年数と学歴・地域手当から、公立学校教員の月給・年収の目安を試算する無料ツール。教職調整額・地域手当も加味。これから教員を目指す人にも。',
  ogtitle='教員の給料シミュレーター｜月給・年収の目安', ogdesc='経験年数と学歴・地域手当から教員の給料の目安を試算。',
  h1='教員の給料シミュレーター',
  lead='公立学校の教員の給料、経験を積むとどれくらい？経験年数・学歴・地域手当から、月給と年収の目安を試算します（教職調整額4%込み）。教員志望の方の参考にも。',
  inputs='''    <h2>💴 条件を入れる</h2>
    <div class="row"><div class="field"><label>経験年数 <span class="hint">（年）</span></label><input type="number" id="years" value="5" min="0" max="40" inputmode="numeric"></div>
    <div class="field"><label>学歴</label><select id="edu"><option value="202000" selected>大卒</option><option value="228000">大学院卒</option><option value="184000">短大卒</option></select></div></div>
    <div class="field"><label>地域手当</label><select id="chiiki"><option value="0">なし（地方）</option><option value="0.1" selected>10%（都市部）</option><option value="0.2">20%（東京特別区など）</option></select></div>
    <button class="btn btn-primary" id="calcBtn">給料の目安を見る</button>''',
  result='''      <div class="label">月給の目安（総支給）</div>
      <div class="big"><span id="big">0</span><span class="unit">円</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">年収の目安</div><div class="v accent" id="year">—</div></div>
      <div class="stat"><div class="k">基本給</div><div class="v" id="base">—</div></div>
      <div class="stat"><div class="k">教職調整額(4%)</div><div class="v" id="cho">—</div></div></div>''',
  article='''    <h2>教員の給料のしくみ</h2>
    <div class="note"><strong>概算の内訳</strong><br>基本給 ＝ 初任給 ＋ 経験年数 × 約4,500円（昇給の目安）<br>月給 ＝ 基本給 ＋ 教職調整額（基本給×4%）＋ 地域手当<br>年収 ＝ 月給 × 12 ＋ ボーナス（約4.5ヶ月）</div>
    <p>教員には残業代の代わりに「教職調整額（基本給の4%）」が一律支給されます（給特法）。実際の給料は自治体の給料表・号俸・各種手当（扶養・住居・部活など）で大きく変わるため、本ツールはあくまで目安です。</p>
    <h2>よくある質問</h2>'''+faq([('正確な額は？','自治体の給料表で号俸ごとに決まります。本ツールは概算の目安です。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const y=Math.max(0,+$('years').value||0), init=+$('edu').value||202000, ch=+$('chiiki').value||0;
    const base=init+y*4500, cho=base*0.04, region=base*ch, month=base+cho+region;
    const yearInc=month*12+base*4.5;
    $('sub').textContent=`経験${y}年・${sel('edu').text}・地域手当${Math.round(ch*100)}%`;
    $('year').textContent=yen(yearInc); $('base').textContent=yen(base); $('cho').textContent=yen(cho);
    SHARE=`教員の給料シミュ、月給の目安は約${yen(month)}・年収約${yen(yearInc)}でした💴（経験${y}年）`;
    show(); anim($('big'),0,month,800);
  }''')

add(id='kyosai-bairitsu', cat=T, emoji='📋',
  title='教員採用試験 倍率シミュレーター｜受験者数と採用数から倍率を計算｜シミュラボ',
  desc='教員採用試験の受験者数と採用者数（合格者数）から、競争倍率と合格率を計算する無料ツール。自治体・校種別の倍率比較や受験校選びの参考に。',
  ogtitle='教員採用試験 倍率シミュレーター｜倍率を計算', ogdesc='受験者数と採用数から教採の倍率と合格率を計算。',
  h1='教員採用試験 倍率シミュレーター',
  lead='教員採用試験（教採）の倍率を、受験者数と採用者数から計算します。合格率もわかるので、自治体・校種ごとの比較や、出願先選びの目安に。',
  inputs='''    <h2>📋 条件を入れる</h2>
    <div class="row"><div class="field"><label>受験者数 <span class="hint">（人）</span></label><input type="number" id="apply" value="1200" min="1" inputmode="numeric"></div>
    <div class="field"><label>採用者数（合格者数） <span class="hint">（人）</span></label><input type="number" id="pass" value="300" min="1" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">倍率を計算する</button>''',
  result='''      <div class="label">競争倍率</div>
      <div class="big"><span id="big">0</span><span class="unit">倍</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">合格率</div><div class="v accent" id="rate">—</div></div>
      <div class="stat"><div class="k">不合格者の目安</div><div class="v" id="fail">—</div></div>
      <div class="stat"><div class="k">全国平均(約3〜4倍)と</div><div class="v" id="vs">—</div></div></div>''',
  article='''    <h2>教採の倍率</h2>
    <div class="note"><strong>計算式</strong><br>倍率 ＝ 受験者数 ÷ 採用者数／合格率 ＝ 採用者数 ÷ 受験者数 ×100</div>
    <p>近年は教員不足を背景に倍率が下がる自治体も増えています（全国平均は小学校で2倍台、中高でやや高め）。校種・教科・自治体で大きく差があるため、志望先の最新データと合わせて確認しましょう。</p>
    <h2>よくある質問</h2>'''+faq([('倍率が低い＝受かりやすい？','傾向としてはそうですが、合否は試験の出来しだいです。対策が大切。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const a=Math.max(1,+$('apply').value||1), p=Math.max(1,+$('pass').value||1);
    const b=a/p, rate=p/a*100;
    $('sub').textContent=`受験${num(a)}人 ÷ 採用${num(p)}人`;
    $('rate').textContent=rate.toFixed(1)+'%'; $('fail').textContent=num(Math.max(0,a-p))+'人'; $('vs').textContent= b<3?'低め（受かりやすい傾向）':b>4?'高め（難関）':'平均的';
    SHARE=`教員採用試験 倍率シミュ、倍率は${b.toFixed(1)}倍・合格率${rate.toFixed(1)}%でした📋`;
    show(); anim($('big'),0,b,800,1);
  }''')

add(id='gakkyu-hensei', cat=T, emoji='🏫',
  title='学級編成シミュレーター｜児童生徒数から何クラス？（35人学級）｜シミュラボ',
  desc='学年の児童生徒数と1クラスの上限人数（35人・40人）から、何クラスに編成されるか・1クラスの平均人数・あと何人で1クラス増えるかを計算する先生向け無料ツール。',
  ogtitle='学級編成シミュレーター｜何クラスになる？35人学級', ogdesc='児童生徒数と上限人数からクラス数・平均人数を計算。',
  h1='学級編成シミュレーター',
  lead='学年の人数から、何クラスに分かれるかを計算します。35人学級・40人学級の上限に対応。1クラスの平均人数や、「あと何人で1クラス増える（減る）」のボーダーも分かります。',
  inputs='''    <h2>🏫 条件を入れる</h2>
    <div class="row"><div class="field"><label>学年の児童生徒数 <span class="hint">（人）</span></label><input type="number" id="n" value="72" min="1" inputmode="numeric"></div>
    <div class="field"><label>1クラスの上限</label><select id="cap"><option value="35" selected>35人（小学校・中学）</option><option value="40">40人</option><option value="30">30人</option></select></div></div>
    <button class="btn btn-primary" id="calcBtn">クラス数を見る</button>''',
  result='''      <div class="label">編成されるクラス数</div>
      <div class="big"><span id="big">0</span><span class="unit">クラス</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">1クラス平均</div><div class="v accent" id="avg">—</div></div>
      <div class="stat"><div class="k">あと何人で+1クラス</div><div class="v" id="next">—</div></div>
      <div class="stat"><div class="k">上限</div><div class="v" id="cap">—</div></div></div>''',
  article='''    <h2>学級編制の標準</h2>
    <div class="note"><strong>計算式</strong><br>クラス数 ＝ 児童生徒数 ÷ 1クラスの上限（端数は切り上げ）<br>1クラス平均 ＝ 児童生徒数 ÷ クラス数</div>
    <p>公立小中学校の1学級の人数は「学級編制の標準」で定められ、小学校は段階的に35人学級へ。1人増えるだけでクラス数が変わり、教員配置にも影響します。実際は特別支援学級なども含めた配置になります。</p>
    <h2>よくある質問</h2>'''+faq([('1人の差でクラスが変わる？','はい。上限を1人超えると1クラス増えます。本ツールでボーダーを確認できます。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const n=Math.max(1,+$('n').value||1), cap=+$('cap').value||35;
    const classes=Math.ceil(n/cap), avg=n/classes, toNext=(classes*cap)-n+1;
    $('sub').textContent=`${n}人・上限${cap}人`;
    $('avg').textContent=avg.toFixed(1)+'人'; $('next').textContent='あと'+toNext+'人'; $('cap').textContent=cap+'人';
    SHARE=`学級編成シミュ、${n}人なら${classes}クラス（1クラス平均${avg.toFixed(1)}人）でした🏫`;
    show(); anim($('big'),0,classes,800);
  }''')

# ============================================================
# 出席率クラスタ（shusseki-ritsu の関連ツール）
# ============================================================
add(id='hisho-nissu', cat=T, emoji='🎯',
  title='必要出席日数 計算｜目標の出席率まであと何日出席が必要？｜シミュラボ',
  desc='今までの授業日数・欠席日数と、目標の出席率から「年間であと何日出席が必要か」「あと何日休めるか」を計算する先生・生徒・保護者向け無料ツール。',
  ogtitle='必要出席日数 計算｜あと何日出席が必要？', ogdesc='目標出席率まで、あと何日出席が必要か・あと何日休めるかを計算。',
  h1='必要出席日数 計算',
  lead='目標の出席率を保つには、年間であと何日出席が必要か・あと何日まで休めるかを計算します。進級や単位の出席要件の逆算に。',
  inputs='''    <h2>🎯 条件を入れる</h2>
    <div class="row"><div class="field"><label>年間の授業日数 <span class="hint">（日）</span></label><input type="number" id="year" value="200" min="1" inputmode="numeric"></div>
    <div class="field"><label>目標の出席率 <span class="hint">（％）</span></label><input type="number" id="goal" value="90" min="1" max="100" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>これまでの授業日数 <span class="hint">（日）</span></label><input type="number" id="total" value="120" min="0" inputmode="numeric"></div>
    <div class="field"><label>これまでの欠席日数 <span class="hint">（日）</span></label><input type="number" id="abs" value="10" min="0" inputmode="numeric"></div></div>
    <button class="btn btn-primary" id="calcBtn">必要な出席日数を見る</button>''',
  result='''      <div class="label">あと何日 出席が必要</div>
      <div class="big"><span id="big">0</span><span class="unit">日</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">年間で許される欠席</div><div class="v accent" id="allow">—</div></div>
      <div class="stat"><div class="k">あと休める日数</div><div class="v" id="left">—</div></div>
      <div class="stat"><div class="k">残りの授業日数</div><div class="v" id="rem">—</div></div></div>''',
  article='''    <h2>必要出席日数の計算方法</h2>
    <div class="note"><strong>計算式</strong><br>年間で必要な出席日数 ＝ 年間授業日数 × 目標出席率<br>年間で許される欠席日数 ＝ 年間授業日数 −（年間で必要な出席日数）<br>あと休める日数 ＝ 許される欠席日数 − これまでの欠席日数</div>
    <p>「目標の出席率を保つには、残りをどれだけ出席すればいいか」を逆算するツールです。高校・大学では出席率が単位・進級の要件になることが多いため、早めに逆算しておくと安心です。まず<a href="/sims/shusseki-ritsu/">出席率シミュレーター</a>で現在の出席率を確認し、こちらで必要日数を計算するのがおすすめです。</p>
    <h2>関連ツール</h2>
    <ul>
    <li><a href="/sims/shusseki-ritsu/">出席率シミュレーター</a>……現在の出席率を計算</li>
    <li><a href="/sims/shinkyu-hantei/">進級・卒業の出席条件 判定</a>……「3分の2以上」などの要件チェック</li>
    <li><a href="/sims/kaikin-hantei/">皆勤・精勤 判定</a></li>
    </ul>
    <h2>よくある質問</h2>'''+faq([
    ('目標出席率は何％にすべき？','高校・大学では「3分の2以上（約66.7％）」や「4分の3以上（75％）」を要件とすることが多いです。正確な数値は在籍校の規定をご確認ください。'),
    ('「あと休める日数」がマイナスになった','すでに目標の出席率を保てない欠席数に達している可能性があります。学校・大学の窓口に早めに相談してください。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const year=Math.max(1,+$('year').value||1), goal=Math.min(100,Math.max(1,+$('goal').value||90));
    const total=Math.max(0,+$('total').value||0), abs=Math.max(0,+$('abs').value||0);
    const needAtt=Math.ceil(year*goal/100);
    const allowAbs=year-needAtt;
    const att=Math.max(0,total-abs);
    const remainDays=Math.max(0,year-total);
    const needMore=Math.max(0,needAtt-att);
    const leftAbs=allowAbs-abs;
    $('sub').textContent=`目標 出席率${goal}%（年間${year}日）`;
    $('allow').textContent=allowAbs+'日まで';
    $('left').textContent=(leftAbs>=0?'あと'+leftAbs+'日':'超過'+(-leftAbs)+'日');
    $('rem').textContent=remainDays+'日';
    SHARE=`必要出席日数 計算、目標${goal}%まであと${needMore}日の出席が必要でした🎯`;
    show(); anim($('big'),0,needMore,800);
  }''')

add(id='kaikin-hantei', cat=T, emoji='🏅',
  title='皆勤・精勤 判定｜欠席・遅刻から皆勤賞・精勤賞をチェック｜シミュラボ',
  desc='欠席日数と遅刻・早退の回数から、皆勤・精勤に当てはまるかを判定する先生・生徒・保護者向け無料ツール。精勤の基準（欠席の許容日数）も選べます。',
  ogtitle='皆勤・精勤 判定｜皆勤賞・精勤賞をチェック', ogdesc='欠席・遅刻の回数から皆勤・精勤に当てはまるか判定。',
  h1='皆勤・精勤 判定',
  lead='欠席日数と遅刻・早退の回数から、皆勤・精勤に当てはまるかを判定します。精勤の許容日数も選べます（基準は学校により異なります）。',
  inputs='''    <h2>🏅 条件を入れる</h2>
    <div class="row"><div class="field"><label>欠席日数 <span class="hint">（日）</span></label><input type="number" id="abs" value="0" min="0" inputmode="numeric"></div>
    <div class="field"><label>遅刻・早退の合計 <span class="hint">（回）</span></label><input type="number" id="late" value="0" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>精勤とみなす欠席の上限</label><select id="rule"><option value="1">欠席1日まで精勤</option><option value="3" selected>欠席3日まで精勤</option><option value="5">欠席5日まで精勤</option></select></div>
    <button class="btn btn-primary" id="calcBtn">判定する</button>''',
  result='''      <div class="label">判定</div>
      <div class="big" style="font-size:30px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">欠席</div><div class="v" id="av">—</div></div>
      <div class="stat"><div class="k">遅刻・早退</div><div class="v" id="lv">—</div></div>
      <div class="stat"><div class="k">精勤の基準</div><div class="v accent" id="rv">—</div></div></div>''',
  article='''    <h2>皆勤・精勤の考え方</h2>
    <div class="note"><strong>判定の目安</strong><br>皆勤＝欠席0日・遅刻早退0回<br>精勤＝欠席が「精勤とみなす上限」以内（遅刻・早退の扱いは学校による）</div>
    <p>「皆勤（かいきん）」は一年間まったく休まなかったこと、「精勤（せいきん）」はごくわずかな欠席にとどまったことを指すのが一般的です。ただし、遅刻・早退を欠席として数えるか、精勤の許容日数を何日にするかは学校によって大きく異なります。本ツールはあくまで目安です。</p>
    <p>出席率そのものを知りたい場合は<a href="/sims/shusseki-ritsu/">出席率シミュレーター</a>、遅刻・早退を欠席に換算したい場合は<a href="/sims/chiko-soutai/">遅刻・早退→欠席換算</a>もご利用ください。</p>
    <h2>よくある質問</h2>'''+faq([
    ('遅刻は皆勤に影響する？','学校によります。遅刻・早退があっても皆勤とする学校もあれば、精勤扱いにする学校もあります。本ツールは遅刻・早退が1回でもあれば皆勤にはしない設定です。'),
    ('精勤の日数は正しい？','精勤の基準は学校ごとに異なります。選択式の目安ですので、正確な基準は在籍校にご確認ください。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const abs=Math.max(0,+$('abs').value||0), late=Math.max(0,+$('late').value||0), rule=+$('rule').value||3;
    let res,detail;
    if(abs===0&&late===0){res='🏅 皆勤';detail='一度も休まず、遅刻・早退もありません。';}
    else if(abs===0&&late>0){res='✨ 精勤（皆勤惜しい）';detail='欠席はありませんが、遅刻・早退があります。';}
    else if(abs<=rule){res='✨ 精勤';detail=`欠席${abs}日は精勤の目安（${rule}日以内）です。`;}
    else{res='該当なし';detail=`欠席${abs}日は精勤の目安（${rule}日以内）を超えています。`;}
    $('big').textContent=res;
    $('sub').textContent=detail;
    $('av').textContent=abs+'日'; $('lv').textContent=late+'回'; $('rv').textContent='欠席'+rule+'日まで';
    SHARE=`皆勤・精勤 判定、結果は「${res}」でした🏅`;
    show();
  }''')

add(id='shinkyu-hantei', cat=T, emoji='✅',
  title='進級・卒業の出席条件 判定｜出席率が3分の2以上あるかチェック｜シミュラボ',
  desc='全授業回数と欠席回数から出席率を計算し、「3分の2以上」「4分の3以上」などの出席要件を満たしているか、あと何回休めるかを判定する高校生・大学生向け無料ツール。',
  ogtitle='進級・卒業の出席条件 判定｜出席要件チェック', ogdesc='出席率が3分の2以上あるか・あと何回休めるかを判定。',
  h1='進級・卒業の出席条件 判定',
  lead='全授業回数と欠席回数から、「3分の2以上」などの出席要件を満たしているかを判定します。単位・進級・卒業の出席条件の確認に。',
  inputs='''    <h2>✅ 条件を入れる</h2>
    <div class="row"><div class="field"><label>全授業回数 <span class="hint">（回・予定含む）</span></label><input type="number" id="total" value="30" min="1" inputmode="numeric"></div>
    <div class="field"><label>これまでの欠席回数 <span class="hint">（回）</span></label><input type="number" id="abs" value="6" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>必要な出席の基準</label><select id="req"><option value="0.6667" selected>3分の2以上（約66.7%）</option><option value="0.75">4分の3以上（75%）</option><option value="0.8">80%以上</option><option value="0.9">90%以上</option></select></div>
    <button class="btn btn-primary" id="calcBtn">判定する</button>''',
  result='''      <div class="label">現時点の出席率</div>
      <div class="big"><span id="big">0</span><span class="unit">%</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">判定</div><div class="v accent" id="ok">—</div></div>
      <div class="stat"><div class="k">あと休める回数</div><div class="v" id="left">—</div></div>
      <div class="stat"><div class="k">必要な最低出席</div><div class="v" id="need">—</div></div></div>''',
  article='''    <h2>出席条件の判定方法</h2>
    <div class="note"><strong>計算式</strong><br>出席率 ＝（全授業回数 − 欠席回数）÷ 全授業回数 × 100<br>許される欠席回数 ＝ 全授業回数 ×（1 − 必要な出席の基準）<br>あと休める回数 ＝ 許される欠席回数 − これまでの欠席回数</div>
    <p>高校・大学では、科目ごとに「全授業回数の3分の2以上の出席」を単位認定・進級・卒業の条件とすることが一般的です。本ツールは、いまの欠席回数で要件を満たしているか、あと何回まで休めるかの目安を示します。正確な基準は在籍校のシラバス・学則をご確認ください。</p>
    <p>出席率の基本計算は<a href="/sims/shusseki-ritsu/">出席率シミュレーター</a>、目標からの逆算は<a href="/sims/hisho-nissu/">必要出席日数 計算</a>もどうぞ。</p>
    <h2>よくある質問</h2>'''+faq([
    ('「3分の2以上」ってどういう意味？','全授業回数の3分の2以上に出席するという意味で、言い換えると欠席が全体の3分の1を超えるとアウト、ということです。30回なら欠席10回まで（＝出席20回以上）が目安になります。'),
    ('遅刻は欠席になる？','学校・科目によります。遅刻数回で1欠席とみなす場合は、'+'<a href="/sims/chiko-soutai/">遅刻・早退→欠席換算</a>で実質の欠席回数を出してから入力してください。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const total=Math.max(1,+$('total').value||1), abs=Math.max(0,+$('abs').value||0), req=+$('req').value||0.6667;
    const att=Math.max(0,total-abs), rate=att/total*100;
    const needAtt=Math.ceil(total*req);
    const allowAbs=total-needAtt;
    const left=allowAbs-abs;
    const ok=att>=needAtt;
    $('sub').textContent=`全${total}回中 ${abs}回欠席`;
    $('ok').textContent=ok?'✅ 満たしている':'⚠️ 要注意';
    $('left').textContent=(left>=0?'あと'+left+'回':'超過'+(-left)+'回');
    $('need').textContent=needAtt+'回以上';
    SHARE=`進級・卒業の出席条件 判定、出席率${rate.toFixed(1)}%で${ok?'要件クリア✅':'要注意⚠️'}でした`;
    show(); anim($('big'),0,rate,800,1);
  }''')

add(id='chiko-soutai', cat=T, emoji='⏰',
  title='遅刻・早退→欠席換算｜遅刻早退を欠席に直して実質出席率を計算｜シミュラボ',
  desc='遅刻・早退の回数を「○回で欠席1回」の換算ルールで欠席に直し、実質の欠席数と実質出席率を計算する高校生・大学生・先生向け無料ツール。',
  ogtitle='遅刻・早退→欠席換算｜実質出席率を計算', ogdesc='遅刻・早退を欠席に換算して実質の出席率を計算。',
  h1='遅刻・早退→欠席換算',
  lead='遅刻・早退を「○回で欠席1回」のルールで欠席に換算し、実質の欠席数と実質出席率を計算します。出席要件の確認に（換算ルールは校則に従ってください）。',
  inputs='''    <h2>⏰ 条件を入れる</h2>
    <div class="row"><div class="field"><label>全授業日数（回） <span class="hint">（日・回）</span></label><input type="number" id="total" value="120" min="1" inputmode="numeric"></div>
    <div class="field"><label>欠席日数 <span class="hint">（日）</span></label><input type="number" id="abs" value="3" min="0" inputmode="numeric"></div></div>
    <div class="row"><div class="field"><label>遅刻の回数 <span class="hint">（回）</span></label><input type="number" id="late" value="6" min="0" inputmode="numeric"></div>
    <div class="field"><label>早退の回数 <span class="hint">（回）</span></label><input type="number" id="early" value="2" min="0" inputmode="numeric"></div></div>
    <div class="field"><label>換算ルール</label><select id="ratio"><option value="3" selected>遅刻・早退3回で欠席1回</option><option value="2">2回で欠席1回</option><option value="4">4回で欠席1回</option></select></div>
    <button class="btn btn-primary" id="calcBtn">実質出席率を見る</button>''',
  result='''      <div class="label">実質の出席率</div>
      <div class="big"><span id="big">0</span><span class="unit">%</span></div>
      <div class="sub" id="sub">—</div>
      <div class="statline"><div class="stat"><div class="k">換算された欠席</div><div class="v accent" id="conv">—</div></div>
      <div class="stat"><div class="k">実質の欠席合計</div><div class="v" id="tot">—</div></div>
      <div class="stat"><div class="k">見かけの出席率</div><div class="v" id="raw">—</div></div></div>''',
  article='''    <h2>遅刻・早退の欠席換算とは</h2>
    <div class="note"><strong>計算式</strong><br>換算欠席 ＝（遅刻＋早退）÷ 換算ルール（切り捨て）<br>実質欠席 ＝ 欠席日数 ＋ 換算欠席<br>実質出席率 ＝（全授業日数 − 実質欠席）÷ 全授業日数 × 100</div>
    <p>多くの学校・大学では、遅刻や早退が一定回数たまると欠席1回分として扱われます（例：遅刻3回で欠席1回）。このツールは、そのルールで遅刻・早退を欠席に換算し、「見かけの出席率」ではなく「実質の出席率」を計算します。出席要件ギリギリの人ほど、換算後の数字で確認しておくと安心です。</p>
    <p>換算後の欠席回数が出たら、<a href="/sims/shinkyu-hantei/">進級・卒業の出席条件 判定</a>で要件を満たすかチェックしてみてください。基本の出席率は<a href="/sims/shusseki-ritsu/">出席率シミュレーター</a>で確認できます。</p>
    <h2>よくある質問</h2>'''+faq([
    ('換算ルールは学校で違う？','はい。遅刻3回で欠席1回、2回で1回など学校・科目でさまざまです。本ツールは代表的な例を選べますが、正確なルールは校則・シラバスをご確認ください。'),
    ('遅刻と早退は同じ扱い？','本ツールは遅刻と早退を合算して換算します。別ルールの場合は、合計回数を調整して入力してください。'),
    ('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
  js='''  function calc(){
    const total=Math.max(1,+$('total').value||1), abs=Math.max(0,+$('abs').value||0);
    const late=Math.max(0,+$('late').value||0), early=Math.max(0,+$('early').value||0), ratio=Math.max(1,+$('ratio').value||3);
    const conv=Math.floor((late+early)/ratio);
    const realAbs=abs+conv;
    const rawRate=Math.max(0,(total-abs)/total*100);
    const realRate=Math.max(0,(total-realAbs)/total*100);
    $('sub').textContent=`遅刻${late}・早退${early}回を${ratio}回=欠席1で換算`;
    $('conv').textContent='＋'+conv+'日'; $('tot').textContent=realAbs+'日'; $('raw').textContent=rawRate.toFixed(1)+'%';
    SHARE=`遅刻・早退→欠席換算、実質の出席率は${realRate.toFixed(1)}%でした⏰`;
    show(); anim($('big'),0,realRate,800,1);
  }''')

def render():
    for s in SIMS:
        d=os.path.join(ROOT,'sims',s['id']); os.makedirs(d,exist_ok=True)
        html=(TPL.replace('__TITLE__',s['title']).replace('__DESC__',s['desc'])
              .replace('__OGTITLE__',s['ogtitle']).replace('__OGDESC__',s['ogdesc'])
              .replace('__CAT__',s['cat']).replace('__H1__',s['h1']).replace('__LEAD__',s['lead'])
              .replace('__INPUTS__',s['inputs']).replace('__RESULT__',s['result'])
              .replace('__ARTICLE__',s['article']).replace('__JS__',s['js']).replace('__ID__',s['id']))
        with open(os.path.join(d,'index.html'),'w',encoding='utf-8') as f: f.write(html)
        print('created sims/'+s['id'])

if __name__=='__main__':
    render()
    print(f'teacher done. {len(SIMS)} sims.')
