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
  article='''    <h2>出席率の計算</h2>
    <div class="note"><strong>計算式</strong><br>出席率 ＝（授業日数 − 欠席日数）÷ 授業日数 ×100</div>
    <p>進級・進学・皆勤の基準は学校により異なります。本ツールは目安です。気になる場合は学校の規定をご確認ください。遅刻・早退の扱いも学校ごとに異なります。</p>
    <h2>よくある質問</h2>'''+faq([('遅刻は？','本ツールは欠席日数のみで計算します。遅刻・早退の換算は校則に従ってください。'),('データは送信されますか？','いいえ。計算はすべてブラウザ内で完結します。')]),
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
