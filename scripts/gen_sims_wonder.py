# -*- coding: utf-8 -*-
"""シミュラボ：ふしぎ・現象カテゴリ canvas系10本を生成。"""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGO = '''<span class="mark">
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M9 3h6M10 3v5.2L5.4 16.4A2.4 2.4 0 0 0 7.5 20h9a2.4 2.4 0 0 0 2.1-3.6L14 8.2V3" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M7.7 14.5h8.6" stroke="#fff" stroke-width="1.8" stroke-linecap="round"/>
          <circle cx="10.3" cy="16.7" r="1" fill="#fff"/>
          <circle cx="13.4" cy="17.4" r=".7" fill="#fff"/>
        </svg>
      </span>'''

CV = '<canvas id="cv" width="__W__" height="__H__" style="width:100%;max-width:__MX__px;height:auto;background:#fff;border:1px solid var(--line);border-radius:12px;__XTRA__"></canvas>'

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
    <div class="cat">ふしぎ・現象</div>
    <h1>__H1__</h1>
    <p class="lead">__LEAD__</p>
  </div>

  <section class="panel">
    <div style="display:grid;place-items:center;gap:16px;">
      __CANVAS__
      <div style="width:100%;max-width:560px;">__CONTROLS__</div>
    </div>
    <p style="text-align:center;color:var(--ink-2);font-size:13px;margin-top:14px;">__LEGEND__</p>
    <div style="text-align:center;"><span id="shareCount" class="share-count" style="display:none"></span></div>
    <div class="share-row"><button class="btn btn-x" id="shareBtn">𝕏 でシェア</button></div>
  </section>

  <article class="article">
__ARTICLE__
  </article>

  <section class="req-banner">
    <h2>💡 こんなシミュも見てみたい？</h2>
    <p>あなたの「これ見てみたい」を送ってください。投票で人気の案から実際に作ります。</p>
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
  const SHARE = '__SHARE__';
  try {
__JS__
  } catch(e) { console.error(e); }
  const sb=$('shareBtn'); if(sb) sb.addEventListener('click',()=>window.open('https://twitter.com/intent/tweet?text='+encodeURIComponent(SHARE)+'&url='+encodeURIComponent(location.href)+'&hashtags='+encodeURIComponent('シミュラボ'),'_blank','noopener'));
})();
</script>
<script src="../../assets/share-counter.js"></script>
<script>ShareCounter.initSim({ simId:'__ID__', badgeEl:document.getElementById('shareCount'), shareBtnIds:['shareBtn'] });</script>
</body>
</html>
'''

def faq(qa):
    return '<dl class="faq">' + ''.join(f'<dt>{q}</dt><dd>{a}</dd>' for q,a in qa) + '</dl>'

def canvas(w,h,mx,xtra=''):
    return CV.replace('__W__',str(w)).replace('__H__',str(h)).replace('__MX__',str(mx)).replace('__XTRA__',xtra)

def btn(id,label,primary=False):
    cls='btn btn-primary' if primary else 'btn btn-ghost'
    return f'<button class="{cls}" id="{id}" style="padding:11px 18px;font-size:14px;">{label}</button>'

def row(*items):
    return '<div class="share-row" style="margin-top:0;">'+''.join(items)+'</div>'

def slider(id,label,mn,mx,val,step='1'):
    return (f'<div class="field" style="margin-bottom:10px;"><div class="slider-head"><label style="margin:0;">{label}</label>'
            f'<span class="val" id="{id}L">{val}</span></div>'
            f'<input type="range" id="{id}" min="{mn}" max="{mx}" value="{val}" step="{step}" style="width:100%;"></div>')

SIMS=[]

# 1. ライフゲーム
SIMS.append(dict(id='life', emoji='🦠',
  title='ライフゲーム｜3つのルールで生命が生まれるシミュレーター｜シミュラボ',
  desc='生きる・死ぬのたった3つのルールだけで、まるで生命のようなパターンが生まれて動き続ける「ライフゲーム」をブラウザで体感できる無料シミュレーター。',
  ogtitle='ライフゲーム｜3つのルールで生命が生まれる', ogdesc='たった3つのルールで生命のようなパターンが動き出すライフゲーム。',
  h1='ライフゲーム',
  lead='「生きる・死ぬ」のたった3つのルールだけ。それなのに、まるで生命のようなパターンが生まれ、動き、増えていきます。クリックで命を置いてみてください。',
  canvas=canvas(480,360,520,'cursor:crosshair;'),
  controls=row(btn('play','⏸ 一時停止',True),btn('rand','ランダム'),btn('clear','クリア')),
  legend='マスをクリックで命を配置／🟦＝生きているセル。3つのルールだけで動き続けます。',
  article='''    <h2>3つのルール</h2>
    <ul><li>生きているセルの周りに2〜3個の仲間 → 生存</li><li>死んでいるセルの周りにちょうど3個 → 誕生</li><li>それ以外 → 死</li></ul>
    <p>1970年に数学者コンウェイが考案。単純なルールから、移動する「グライダー」や永遠に動く構造など、驚くほど複雑なパターンが生まれます。これは「単純なルールから複雑さが生まれる（創発）」の代表例です。</p>
    <h2>よくある質問</h2>'''+faq([('何の役に立つの？','創発・複雑系を直感的に理解できる教材として有名です。眺めるだけでも面白いですよ。'),('データは送信されますか？','いいえ。すべてブラウザ内で動作します。')]),
  share='たった3つのルールで"生命"が生まれて動き出す…ライフゲーム、見てると止まらない🦠',
  js='''  const c=$('cv'),x=c.getContext('2d'),CELL=8,COLS=c.width/CELL|0,ROWS=c.height/CELL|0;
  let g,run=true,f=0;
  const mk=(fn)=>Array.from({length:ROWS},()=>Array.from({length:COLS},fn));
  const rnd=()=>g=mk(()=>Math.random()<0.3?1:0);
  const clr=()=>g=mk(()=>0);
  function step(){const n=mk(()=>0);for(let i=0;i<ROWS;i++)for(let j=0;j<COLS;j++){let s=0;for(let di=-1;di<=1;di++)for(let dj=-1;dj<=1;dj++){if(di||dj)s+=g[(i+di+ROWS)%ROWS][(j+dj+COLS)%COLS];}n[i][j]=(g[i][j]&&(s===2||s===3))||(!g[i][j]&&s===3)?1:0;}g=n;}
  function draw(){x.clearRect(0,0,c.width,c.height);x.fillStyle='#0fb5c4';for(let i=0;i<ROWS;i++)for(let j=0;j<COLS;j++)if(g[i][j])x.fillRect(j*CELL,i*CELL,CELL-1,CELL-1);}
  function loop(){if(run){f++;if(f%4===0)step();}draw();requestAnimationFrame(loop);}
  $('play').addEventListener('click',()=>{run=!run;$('play').textContent=run?'⏸ 一時停止':'▶ 再生';});
  $('rand').addEventListener('click',rnd);$('clear').addEventListener('click',clr);
  c.addEventListener('click',e=>{const r=c.getBoundingClientRect();const j=(e.clientX-r.left)/r.width*COLS|0,i=(e.clientY-r.top)/r.height*ROWS|0;if(g[i]&&g[i][j]!=null)g[i][j]^=1;});
  rnd();loop();'''))

# 2. 森林火災（浸透）
SIMS.append(dict(id='forest-fire', emoji='🔥',
  title='森林火災シミュレーター｜木の密度と燃え広がりの臨界｜シミュラボ',
  desc='木の密度をスライダーで変えて火をつけると、ある密度を超えた瞬間に火が端から端まで燃え広がる「浸透（パーコレーション）の臨界」を体感できる無料シミュレーター。',
  ogtitle='森林火災シミュレーター｜燃え広がりの臨界', ogdesc='木がちょっと増えただけで火が全体に広がる、浸透の臨界を体感。',
  h1='森林火災シミュレーター',
  lead='木がまばらだと火はすぐ消えるのに、ある密度を超えた瞬間、端から端まで一気に燃え広がる。この「臨界」のふしぎを体感してください。',
  canvas=canvas(480,360,520),
  controls=slider('dens','木の密度','10','90','60')+row(btn('fire','🔥 左から着火',True),btn('reset','リセット')),
  legend='🟩 木／🟥 燃焼中／⬜ 燃えた跡。密度を上げて着火すると、ある所から一気に燃え広がります。',
  article='''    <h2>燃え広がりの「臨界」</h2>
    <p>木の密度が低いと、火は隣の木に飛び移れずすぐ消えます。ところが密度が約59%を超えたあたりで、突然「端から端まで一本につながった道」ができ、火が全体に到達するようになります。これを<strong>パーコレーション（浸透）の臨界</strong>と呼びます。</p>
    <p>感染症の広がり、ネットワークの分断、山火事対策など、いろいろな現象に共通する考え方です。</p>
    <h2>よくある質問</h2>'''+faq([('59%って何？','格子上で隣同士がつながり全体を貫通し始める密度の目安（浸透閾値）です。'),('データは送信されますか？','いいえ。すべてブラウザ内で動作します。')]),
  share='木がちょっと増えただけで、火が端から端まで燃え広がる。"臨界"の不思議🔥🌲',
  js='''  const c=$('cv'),x=c.getContext('2d'),CELL=6,COLS=c.width/CELL|0,ROWS=c.height/CELL|0;
  let g,run=false;
  function init(){const d=(+$('dens').value)/100;g=Array.from({length:ROWS},()=>Array.from({length:COLS},()=>Math.random()<d?1:0));run=false;$('densL').textContent=$('dens').value+'%';draw();}
  function ignite(){for(let i=0;i<ROWS;i++)if(g[i][0]===1)g[i][0]=2;run=true;}
  function step(){let any=false;const n=g.map(r=>r.slice());for(let i=0;i<ROWS;i++)for(let j=0;j<COLS;j++)if(g[i][j]===2){n[i][j]=3;[[1,0],[-1,0],[0,1],[0,-1]].forEach(([di,dj])=>{const a=i+di,b=j+dj;if(a>=0&&a<ROWS&&b>=0&&b<COLS&&g[a][b]===1){n[a][b]=2;any=true;}});}g=n;if(!any)run=false;}
  const COL=['#eef2f6','#16a34a','#f43f5e','#cbd5e1'];
  function draw(){for(let i=0;i<ROWS;i++)for(let j=0;j<COLS;j++){x.fillStyle=COL[g[i][j]];x.fillRect(j*CELL,i*CELL,CELL,CELL);}}
  let f=0;function loop(){if(run){f++;if(f%2===0)step();}draw();requestAnimationFrame(loop);}
  $('dens').addEventListener('input',init);$('fire').addEventListener('click',ignite);$('reset').addEventListener('click',init);
  init();loop();'''))

# 3. 街の分断（シェリング）
SIMS.append(dict(id='schelling', emoji='🏘️',
  title='街の分断シミュレーター｜悪意ゼロでも分かれる（シェリング）｜シミュラボ',
  desc='「少しだけ同じ人が近くにいたい」という弱い好みだけで、街がくっきり2つに分断されていく様子を再現したシェリングの分居モデル。差別意識ゼロでも分離が起きる不思議を体感できます。',
  ogtitle='街の分断シミュレーター｜悪意ゼロでも分かれる', ogdesc='弱い好みだけで街が分断される、シェリングの分居モデル。',
  h1='街の分断シミュレーター',
  lead='「ご近所にちょっとだけ同じ人がいると安心」。たったそれだけの弱い好みでも、街は放っておくとくっきり2つに分かれます。悪意ゼロでも起きる「分断」を見てください。',
  canvas=canvas(400,400,420),
  controls=slider('tol','満足する同類の割合','10','70','35')+row(btn('reset','リセット'),btn('toggle','⏸ 一時停止')),
  legend='🔵🟠＝2つのグループ／白＝空き地。不満な人が空き地へ引っ越すだけで、街は分かれていきます。',
  article='''    <h2>シェリングの分居モデル</h2>
    <p>経済学者シェリングが示した有名なモデルです。各住人は「近所の◯％以上が同じ仲間なら満足、足りなければ引っ越す」というルールだけで動きます。<strong>「相手を排除したい」という気持ちはゼロ</strong>。それでも、わずかな好みが積み重なると、街全体は強く分断されてしまいます。</p>
    <p>社会の分断やフィルターバブルを考えるうえで示唆に富んだモデルです。</p>
    <h2>よくある質問</h2>'''+faq([('差別の話ですか？','むしろ逆で、強い差別意識がなくても分離が起きうることを示すモデルです。'),('データは送信されますか？','いいえ。すべてブラウザ内で動作します。')]),
  share='「少しだけ同じ人が近くにいたい」だけで、街はくっきり分断される。悪意ゼロでも…🏘️',
  js='''  const c=$('cv'),x=c.getContext('2d'),CELL=10,COLS=c.width/CELL|0,ROWS=c.height/CELL|0;
  let g,run=true;
  function init(){g=Array.from({length:ROWS},()=>Array.from({length:COLS},()=>{const r=Math.random();return r<0.45?1:r<0.9?2:0;}));$('tolL').textContent=$('tol').value+'%';draw();}
  function happy(i,j){const t=g[i][j];if(!t)return true;let same=0,tot=0;for(let di=-1;di<=1;di++)for(let dj=-1;dj<=1;dj++){if(di||dj){const a=i+di,b=j+dj;if(a>=0&&a<ROWS&&b>=0&&b<COLS&&g[a][b]){tot++;if(g[a][b]===t)same++;}}}return tot===0?true:(same/tot)>=(+$('tol').value)/100;}
  function step(){const empties=[];for(let i=0;i<ROWS;i++)for(let j=0;j<COLS;j++)if(!g[i][j])empties.push([i,j]);for(let i=0;i<ROWS;i++)for(let j=0;j<COLS;j++){if(g[i][j]&&!happy(i,j)&&empties.length){const k=Math.random()*empties.length|0,[a,b]=empties[k];g[a][b]=g[i][j];g[i][j]=0;empties[k]=[i,j];}}}
  const COL=['#ffffff','#3b82f6','#f59e0b'];
  function draw(){for(let i=0;i<ROWS;i++)for(let j=0;j<COLS;j++){x.fillStyle=COL[g[i][j]];x.fillRect(j*CELL,i*CELL,CELL-1,CELL-1);}}
  let f=0;function loop(){if(run){f++;if(f%6===0)step();}draw();requestAnimationFrame(loop);}
  $('tol').addEventListener('input',()=>$('tolL').textContent=$('tol').value+'%');
  $('reset').addEventListener('click',init);$('toggle').addEventListener('click',()=>{run=!run;$('toggle').textContent=run?'⏸ 一時停止':'▶ 再生';});
  init();loop();'''))

# 4. 砂山崩し
SIMS.append(dict(id='sandpile', emoji='⛰️',
  title='砂山崩しシミュレーター｜大崩壊はいつ来るか分からない｜シミュラボ',
  desc='砂を一粒ずつ積んでいくと、ある時 突然 連鎖的な大崩壊が起きる「自己組織化臨界」をブラウザで再現。地震や株価暴落にも通じる仕組みを体感できる無料シミュレーターです。',
  ogtitle='砂山崩しシミュレーター｜大崩壊はいつ来るか分からない', ogdesc='砂を積むとある時 突然 大崩壊。自己組織化臨界を体感。',
  h1='砂山崩しシミュレーター',
  lead='砂を一粒ずつ積むだけ。小さな崩れが続くなか、ある瞬間、予測できない「大崩壊」が突然やってきます。地震や株価暴落にも通じる不思議な仕組みです。',
  canvas=canvas(360,360,400,'image-rendering:pixelated;'),
  controls=row(btn('reset','リセット')),
  legend='中央に砂を積み続けています。色は砂の高さ。4つ積もると四方へ崩れ、それが連鎖します。',
  article='''    <h2>自己組織化臨界</h2>
    <p>1つのマスに砂が4粒たまると、周囲4マスへ1粒ずつ崩れます。崩れた先がまた4粒になれば、さらに崩れる…と連鎖します。たいていは小さな崩れですが、ときどき<strong>とてつもない大崩壊</strong>が起こります。しかも、いつ大崩壊が来るかは事前に分かりません。</p>
    <p>この「ふだんは静かで、ときどき大事件」という性質は、地震・山火事・株価暴落など多くの現象に共通します。</p>
    <h2>よくある質問</h2>'''+faq([('美しい模様になるのはなぜ？','崩れのルールが生む数学的なパターンです。完成形はフラクタル的な構造になります。'),('データは送信されますか？','いいえ。すべてブラウザ内で動作します。')]),
  share='砂を一粒ずつ積むだけ。ある時"大崩壊"が突然くる。地震や株価と同じ仕組み…⛰️',
  js='''  const c=$('cv'),x=c.getContext('2d'),N=c.width,img=x.createImageData(N,N);
  let g,cx=N>>1,cy=N>>1;
  const COL=[[245,247,250],[159,225,203],[29,158,117],[10,135,150]];
  function init(){g=new Uint8Array(N*N);}
  function add(n){for(let k=0;k<n;k++)g[cy*N+cx]++;}
  function topple(){let again=true,c2=0;while(again&&c2<4){again=false;c2++;for(let i=1;i<N-1;i++)for(let j=1;j<N-1;j++){const id=i*N+j;if(g[id]>=4){const q=g[id]>>2;g[id]-=q*4;g[id-1]+=q;g[id+1]+=q;g[id-N]+=q;g[id+N]+=q;again=true;}}}}
  function draw(){const d=img.data;for(let i=0;i<N*N;i++){const v=Math.min(3,g[i]),col=COL[v];d[i*4]=col[0];d[i*4+1]=col[1];d[i*4+2]=col[2];d[i*4+3]=255;}x.putImageData(img,0,0);}
  function loop(){add(40);topple();draw();requestAnimationFrame(loop);}
  $('reset').addEventListener('click',init);
  init();loop();'''))

# 5. 鳥の群れ（ボイド）
SIMS.append(dict(id='boids', emoji='🐦',
  title='鳥の群れシミュレーター（ボイド）｜群れはどう生まれる？｜シミュラボ',
  desc='一羽一羽は「近くに合わせる」だけの3つのルールで動いているのに、全体としては鳥の群れのような動きが生まれるボイドモデルをブラウザで体感できる無料シミュレーター。',
  ogtitle='鳥の群れシミュレーター（ボイド）', ogdesc='3つのルールだけで群れが生まれるボイドモデル。',
  h1='鳥の群れシミュレーター（ボイド）',
  lead='一羽一羽は「ぶつからない・向きを合わせる・近づく」の3つだけ。リーダーもいないのに、全体としては生きた群れのような動きが生まれます。',
  canvas=canvas(520,360,540,'background:#0b1220;'),
  controls=slider('n','群れの数','20','200','90')+row(btn('reset','リセット')),
  legend='中央のルールだけで動く「ボイド」たち。だれも全体を指揮していないのに群れになります。',
  article='''    <h2>3つのルール</h2>
    <ul><li><strong>分離</strong>：近づきすぎたら離れる</li><li><strong>整列</strong>：周りと進む向きを合わせる</li><li><strong>結合</strong>：群れの中心へ寄っていく</li></ul>
    <p>1986年にレイノルズが考案。中央の指揮者なしに、局所的なルールだけで群れの動きが生まれます（創発）。映画やゲームの群衆表現にも使われています。</p>
    <h2>よくある質問</h2>'''+faq([('本物の鳥もこれ？','完全に同じではありませんが、群れの動きをよく再現できることで知られています。'),('データは送信されますか？','いいえ。すべてブラウザ内で動作します。')]),
  share='一羽一羽はただ"近くに合わせてる"だけ。なのに群れになる。ボイドの不思議🐦',
  js='''  const c=$('cv'),x=c.getContext('2d'),W=c.width,H=c.height;
  let b=[];
  function init(){const n=+$('n').value;$('nL').textContent=n;b=Array.from({length:n},()=>({x:Math.random()*W,y:Math.random()*H,vx:Math.random()*2-1,vy:Math.random()*2-1}));}
  function step(){const R=40,R2=R*R;for(const p of b){let ax=0,ay=0,cx=0,cy=0,sx=0,sy=0,cnt=0;for(const q of b){if(q===p)continue;const dx=q.x-p.x,dy=q.y-p.y,d2=dx*dx+dy*dy;if(d2<R2&&d2>0){ax+=q.vx;ay+=q.vy;cx+=q.x;cy+=q.y;cnt++;if(d2<260){sx-=dx;sy-=dy;}}}if(cnt){ax/=cnt;ay/=cnt;cx/=cnt;cy/=cnt;p.vx+=(ax-p.vx)*0.05+(cx-p.x)*0.0008+sx*0.02;p.vy+=(ay-p.vy)*0.05+(cy-p.y)*0.0008+sy*0.02;}p.vx+=(Math.random()-.5)*0.1;p.vy+=(Math.random()-.5)*0.1;const sp=Math.hypot(p.vx,p.vy),mx=2.6;if(sp>mx){p.vx=p.vx/sp*mx;p.vy=p.vy/sp*mx;}p.x=(p.x+p.vx+W)%W;p.y=(p.y+p.vy+H)%H;}}
  function draw(){x.fillStyle='rgba(11,18,32,0.35)';x.fillRect(0,0,W,H);for(const p of b){const a=Math.atan2(p.vy,p.vx);x.save();x.translate(p.x,p.y);x.rotate(a);x.fillStyle='#5dcaa5';x.beginPath();x.moveTo(6,0);x.lineTo(-4,3);x.lineTo(-4,-3);x.closePath();x.fill();x.restore();}}
  function loop(){step();draw();requestAnimationFrame(loop);}
  $('n').addEventListener('input',init);$('reset').addEventListener('click',init);
  init();x.fillStyle='#0b1220';x.fillRect(0,0,W,H);loop();'''))

# 6. 二重振り子（カオス）
SIMS.append(dict(id='double-pendulum', emoji='🌀',
  title='二重振り子シミュレーター｜カオスを体感する｜シミュラボ',
  desc='ほんのわずかに初期条件が違うだけで、数秒後にはまったく違う動きになる「二重振り子」のカオスを、2本同時に並べて体感できる無料シミュレーター。',
  ogtitle='二重振り子シミュレーター｜カオスを体感', ogdesc='わずかな差が大きな違いに。二重振り子のカオスを2本並べて体感。',
  h1='二重振り子シミュレーター',
  lead='ほぼ同じスタートに見える2本の振り子。でも数秒後にはまったく違う動きに。これが「カオス」。小さな差が大きな違いを生む様子を見てください。',
  canvas=canvas(420,400,440,'background:#0b1220;'),
  controls=row(btn('reset','リセット（少しズラして再開）',True)),
  legend='2本の振り子は、ほんのわずかだけ初期角度が違うだけ。やがて完全にバラバラになります。',
  article='''    <h2>カオスとは</h2>
    <p>二重振り子は「決まった物理法則」で動く（ランダムではない）のに、初期条件のごくわずかな差が、時間とともに指数関数的に拡大します。これを<strong>カオス（バタフライ効果）</strong>と呼びます。天気予報が長期では当たりにくいのも、これが理由のひとつです。</p>
    <h2>よくある質問</h2>'''+faq([('ランダムなの？','いいえ。完全に決まった法則で動きます。それでも予測が難しいのがカオスの面白さです。'),('データは送信されますか？','いいえ。すべてブラウザ内で動作します。')]),
  share='まったく同じに見える初期条件が、数秒で全然違う動きに。これがカオス🌀',
  js='''  const c=$('cv'),x=c.getContext('2d'),W=c.width,H=c.height,ox=W/2,oy=H*0.4;
  const L1=90,L2=90,m1=10,m2=10,g=1.0;
  let P=[];
  function mk(a1){return {a1:a1,a2:Math.PI/2,p1:0,p2:0,tr:[],col:''};}
  function init(){P=[mk(Math.PI/2),mk(Math.PI/2+0.01)];P[0].col='#0fb5c4';P[1].col='#f43f5e';}
  function deriv(s){const {a1,a2,p1,p2}=s;const d=a1-a2;const den=(2*m1+m2-m2*Math.cos(2*d));
    const da1=(6/(m1*L1*L1))*(2*p1-3*Math.cos(d)*p2)/(16-9*Math.cos(d)*Math.cos(d));
    const da2=(6/(m2*L2*L2))*(8*p2-3*Math.cos(d)*p1)/(16-9*Math.cos(d)*Math.cos(d));
    const dp1=-0.5*m1*L1*L1*(da1*da2*Math.sin(d)+3*(g/L1)*Math.sin(a1));
    const dp2=-0.5*m2*L2*L2*(-da1*da2*Math.sin(d)+(g/L2)*Math.sin(a2));
    return {a1:da1,a2:da2,p1:dp1,p2:dp2};}
  function stepOne(s){const dt=0.18;const k=deriv(s);s.a1+=k.a1*dt;s.a2+=k.a2*dt;s.p1+=k.p1*dt;s.p2+=k.p2*dt;}
  function draw(){x.fillStyle='rgba(11,18,32,0.25)';x.fillRect(0,0,W,H);for(const s of P){const x1=ox+L1*Math.sin(s.a1),y1=oy+L1*Math.cos(s.a1),x2=x1+L2*Math.sin(s.a2),y2=y1+L2*Math.cos(s.a2);s.tr.push([x2,y2]);if(s.tr.length>120)s.tr.shift();x.strokeStyle=s.col;x.globalAlpha=0.5;x.beginPath();s.tr.forEach((p,i)=>i?x.lineTo(p[0],p[1]):x.moveTo(p[0],p[1]));x.stroke();x.globalAlpha=1;x.strokeStyle=s.col;x.lineWidth=2;x.beginPath();x.moveTo(ox,oy);x.lineTo(x1,y1);x.lineTo(x2,y2);x.stroke();x.fillStyle=s.col;x.beginPath();x.arc(x2,y2,5,0,7);x.fill();}}
  function loop(){for(let k=0;k<3;k++)for(const s of P)stepOne(s);draw();requestAnimationFrame(loop);}
  $('reset').addEventListener('click',()=>{init();x.fillStyle='#0b1220';x.fillRect(0,0,W,H);});
  init();x.fillStyle='#0b1220';x.fillRect(0,0,W,H);loop();'''))

# 7. 波の干渉
SIMS.append(dict(id='wave', emoji='🌊',
  title='波の干渉シミュレーター｜2つの波が作るしま模様｜シミュラボ',
  desc='2つの波源から広がる波が重なり、強め合う場所と打ち消し合う場所が「しま模様」になる干渉を、波源の間隔を変えながら体感できる無料シミュレーター。',
  ogtitle='波の干渉シミュレーター｜2つの波が作るしま模様', ogdesc='2つの波が重なると現れる干渉のしま模様を体感。',
  h1='波の干渉シミュレーター',
  lead='水面に2つの波源。広がる波が重なると、強め合う線と打ち消し合う線が現れ、美しい「しま模様」になります。波源の間隔を変えてみてください。',
  canvas=canvas(480,320,520),
  controls=slider('gap','2つの波源の間隔','40','300','140')+row(btn('toggle','⏸ 一時停止')),
  legend='明るい所＝波が強め合う／暗い所＝打ち消し合う。これが「干渉」です。',
  article='''    <h2>干渉とは</h2>
    <p>2つの波が重なると、山と山が合うところは強め合い（明るい）、山と谷が合うところは打ち消し合います（暗い）。この結果あらわれるしま模様が<strong>干渉縞</strong>です。光・音・水面など、波であれば共通して起こる現象で、ヤングの実験（光が波であることの証明）でも有名です。</p>
    <h2>よくある質問</h2>'''+faq([('波源を近づけると？','しま模様の間隔が広がります。逆に離すと細かくなります。'),('データは送信されますか？','いいえ。すべてブラウザ内で動作します。')]),
  share='2つの波が重なると、強め合う線と消し合う線が現れる。干渉のしま模様🌊',
  js='''  const c=$('cv'),x=c.getContext('2d'),W=c.width,H=c.height,S=4;
  const gw=Math.ceil(W/S),gh=Math.ceil(H/S),img=x.createImageData(gw,gh);
  let t=0,run=true;
  function frame(){const gap=+$('gap').value;$('gapL').textContent=gap+'px';const ax=W/2-gap/2,bx=W/2+gap/2,cy=H/2,k=0.18,d=img.data;
    for(let gy=0;gy<gh;gy++)for(let gx=0;gx<gw;gx++){const px=gx*S,py=gy*S;const d1=Math.hypot(px-ax,py-cy),d2=Math.hypot(px-bx,py-cy);const v=Math.sin(k*d1-t)+Math.sin(k*d2-t);const b=Math.round((v+2)/4*255);const i=(gy*gw+gx)*4;d[i]=b*0.2;d[i+1]=b*0.7;d[i+2]=b;d[i+3]=255;}
    x.putImageData(img,0,0);x.imageSmoothingEnabled=false;x.drawImage(c,0,0,gw,gh,0,0,W,H);}
  function loop(){if(run){t+=0.25;frame();}requestAnimationFrame(loop);}
  $('gap').addEventListener('input',()=>{$('gapL').textContent=$('gap').value+'px';if(!run)frame();});
  $('toggle').addEventListener('click',()=>{run=!run;$('toggle').textContent=run?'⏸ 一時停止':'▶ 再生';});
  loop();'''))

# 8. 拡散（混ざると戻らない）
SIMS.append(dict(id='diffusion', emoji='🫧',
  title='拡散シミュレーター｜なぜ混ざると元に戻らない？｜シミュラボ',
  desc='左右に分かれた2色の粒子がランダムに動くだけで、だんだん混ざり合い、二度と勝手には分かれない「不可逆性（エントロピー）」を体感できる無料シミュレーター。',
  ogtitle='拡散シミュレーター｜なぜ混ざると元に戻らない？', ogdesc='2色の粒子が混ざって戻らない、エントロピーと時間の向き。',
  h1='拡散シミュレーター',
  lead='左に赤、右に青の粒子。それぞれがランダムに動くだけなのに、放っておくと必ず混ざり合い、二度と勝手には分かれません。「時間に向きがある」理由です。',
  canvas=canvas(480,320,520,'background:#0b1220;'),
  controls=row(btn('reset','リセット（左右に分ける）',True)),
  legend='粒子はランダムに動くだけ。なのに混ざる一方で、自然に元の左右には戻りません。',
  article='''    <h2>なぜ戻らないのか</h2>
    <p>一粒一粒の動きはランダムで、向きの好みはありません。それでも全体は必ず「混ざった状態」に向かいます。理由は、混ざった状態のほうが圧倒的に「場合の数が多い」から。これが<strong>エントロピー増大</strong>であり、私たちが感じる「時間の向き（過去→未来）」の正体ともいわれます。</p>
    <h2>よくある質問</h2>'''+faq([('絶対に戻らない？','理論上はゼロではありませんが、確率が天文学的に低く、現実には起こりません。'),('データは送信されますか？','いいえ。すべてブラウザ内で動作します。')]),
  share='インクは水に広がるけど、勝手に元には戻らない。"時間に向き"がある理由🫧',
  js='''  const c=$('cv'),x=c.getContext('2d'),W=c.width,H=c.height,N=600;
  let p=[];
  function init(){p=Array.from({length:N},(_,i)=>({x:i<N/2?Math.random()*W/2:W/2+Math.random()*W/2,y:Math.random()*H,r:i<N/2}));}
  function step(){for(const q of p){q.x+=(Math.random()-.5)*4;q.y+=(Math.random()-.5)*4;if(q.x<0)q.x=0;if(q.x>W)q.x=W;if(q.y<0)q.y=0;if(q.y>H)q.y=H;}}
  function draw(){x.fillStyle='#0b1220';x.fillRect(0,0,W,H);for(const q of p){x.fillStyle=q.r?'#f43f5e':'#3b82f6';x.beginPath();x.arc(q.x,q.y,2.4,0,7);x.fill();}}
  function loop(){step();draw();requestAnimationFrame(loop);}
  $('reset').addEventListener('click',init);
  init();loop();'''))

# 9. 反応拡散（模様が生まれる）
SIMS.append(dict(id='turing', emoji='🐆',
  title='模様が生まれるシミュレーター｜反応拡散で生き物の模様｜シミュラボ',
  desc='ただの2種類の物質が反応して広がるだけで、ヒョウ柄やシマ模様、迷路のような模様がひとりでに生まれる反応拡散（チューリングパターン）を体感できる無料シミュレーター。',
  ogtitle='模様が生まれるシミュレーター｜反応拡散', ogdesc='2つの物質が反応するだけでヒョウ柄やシマ模様が生まれる。',
  h1='模様が生まれるシミュレーター',
  lead='たった2種類の物質が反応して広がるだけ。それなのに、ヒョウ柄やシマ模様、迷路のような模様がひとりでに生まれます。生き物の模様の起源とも言われる現象です。',
  canvas=canvas(120,120,360,'image-rendering:pixelated;'),
  controls=('<div class="field" style="margin-bottom:10px;"><label>模様のタイプ</label>'
            '<select id="pat"><option value="spots">水玉・ヒョウ柄</option><option value="stripes">しま模様</option><option value="maze">迷路</option></select></div>'
            +row(btn('reset','リセット'))),
  legend='2つの物質の濃さを色で表示。種類を変えると、生まれる模様が変わります。',
  article='''    <h2>チューリングパターン</h2>
    <p>計算機科学の父アラン・チューリングが提唱した理論です。「広がる速さの違う2つの物質が反応し合う」だけで、自然に規則的な模様が生まれることを示しました。シマウマ・ヒョウ・熱帯魚・貝殻など、生き物の模様の説明に使われています。</p>
    <h2>よくある質問</h2>'''+faq([('ランダムに描いてるの？','いいえ。物質の反応と拡散の数式から、模様が自然に立ち上がります。'),('データは送信されますか？','いいえ。すべてブラウザ内で動作します。')]),
  share='ただの2つの物質が反応するだけで、ヒョウ柄やシマ模様が生まれる。生き物の模様の起源🐆',
  js='''  const c=$('cv'),x=c.getContext('2d'),N=c.width,img=x.createImageData(N,N);
  const Du=0.16,Dv=0.08,dt=1;let f=0.035,k=0.065,U,V;
  function init(){U=new Float32Array(N*N).fill(1);V=new Float32Array(N*N).fill(0);for(let i=N/2-8;i<N/2+8;i++)for(let j=N/2-8;j<N/2+8;j++){V[i*N+j]=1;}const p=$('pat').value;if(p==='spots'){f=0.035;k=0.065;}else if(p==='stripes'){f=0.055;k=0.062;}else{f=0.029;k=0.057;}}
  function step(){const u2=U.slice(),v2=V.slice();for(let i=1;i<N-1;i++)for(let j=1;j<N-1;j++){const id=i*N+j;const lu=U[id-1]+U[id+1]+U[id-N]+U[id+N]-4*U[id];const lv=V[id-1]+V[id+1]+V[id-N]+V[id+N]-4*V[id];const uvv=U[id]*V[id]*V[id];u2[id]=U[id]+(Du*lu-uvv+f*(1-U[id]))*dt;v2[id]=V[id]+(Dv*lv+uvv-(k+f)*V[id])*dt;}U=u2;V=v2;}
  function draw(){const d=img.data;for(let i=0;i<N*N;i++){const v=Math.max(0,Math.min(1,V[i]));const cc=Math.round((1-v)*255);d[i*4]=Math.round(15+v*100);d[i*4+1]=cc*0.6+v*60;d[i*4+2]=Math.round(cc*0.8);d[i*4+3]=255;}x.putImageData(img,0,0);}
  function loop(){for(let s=0;s<8;s++)step();draw();requestAnimationFrame(loop);}
  $('pat').addEventListener('change',init);$('reset').addEventListener('click',init);
  init();loop();'''))

# 10. 同期現象
SIMS.append(dict(id='sync', emoji='✨',
  title='同期現象シミュレーター｜ホタルやメトロノームが勝手に揃う｜シミュラボ',
  desc='バラバラに光っていた多数のホタル（振動子）が、弱く影響し合うだけで、放っておくとひとりでに点滅を揃えていく「同期現象」を体感できる無料シミュレーター。',
  ogtitle='同期現象シミュレーター｜勝手に揃うふしぎ', ogdesc='バラバラのホタルが放っておくと点滅を揃える、同期現象。',
  h1='同期現象シミュレーター',
  lead='最初はバラバラに光るホタルたち。お互いに少し影響し合うだけで、放っておくと点滅がだんだん揃っていきます。拍手・メトロノーム・コオロギの合唱にも見られる不思議です。',
  canvas=canvas(420,360,440,'background:#0b1220;'),
  controls=slider('k','影響し合う強さ','0','100','35')+row(btn('reset','リセット（バラバラに戻す）')),
  legend='点が明るいほど「今光っている」状態。強さを上げるほど、早く一斉に光るようになります。',
  article='''    <h2>同期はなぜ起きる？</h2>
    <p>それぞれのホタルは自分のリズムで光りますが、まわりが光ると自分のリズムを少しだけ合わせます。この弱い引き込みが積み重なると、全体がひとつのリズムに揃います。これを<strong>蔵本モデル（同期現象）</strong>といいます。心臓のペースメーカー細胞や、橋を渡る歩行者の歩調が揃う現象などにも見られます。</p>
    <h2>よくある質問</h2>'''+faq([('強さを0にすると？','お互いに影響しなくなり、いつまでもバラバラのままになります。'),('データは送信されますか？','いいえ。すべてブラウザ内で動作します。')]),
  share='バラバラに光ってたホタルが、放っておくと勝手に揃う。同期現象の不思議✨',
  js='''  const c=$('cv'),x=c.getContext('2d'),W=c.width,H=c.height,N=160;
  let o=[];
  function init(){o=Array.from({length:N},()=>({x:20+Math.random()*(W-40),y:20+Math.random()*(H-40),th:Math.random()*6.283,w:0.9+Math.random()*0.2}));}
  function step(){const K=(+$('k').value)/100*0.08;$('kL').textContent=$('k').value;let sx=0,sy=0;for(const p of o){sx+=Math.cos(p.th);sy+=Math.sin(p.th);}const psi=Math.atan2(sy,sx),r=Math.hypot(sx,sy)/N;for(const p of o){p.th+=0.05*p.w+K*r*Math.sin(psi-p.th)*N*0.02;}}
  function draw(){x.fillStyle='#0b1220';x.fillRect(0,0,W,H);for(const p of o){const b=(1+Math.sin(p.th))/2;x.fillStyle='rgba('+Math.round(80+b*175)+','+Math.round(200+b*55)+','+Math.round(120+b*80)+','+(0.2+b*0.8).toFixed(2)+')';x.beginPath();x.arc(p.x,p.y,4+b*4,0,7);x.fill();}}
  function loop(){step();draw();requestAnimationFrame(loop);}
  $('k').addEventListener('input',()=>$('kL').textContent=$('k').value);$('reset').addEventListener('click',init);
  init();loop();'''))

for s in SIMS:
    d=os.path.join(ROOT,'sims',s['id']); os.makedirs(d,exist_ok=True)
    body=s['canvas']
    html=(TPL.replace('__TITLE__',s['title']).replace('__DESC__',s['desc'])
          .replace('__OGTITLE__',s['ogtitle']).replace('__OGDESC__',s['ogdesc'])
          .replace('__H1__',s['h1']).replace('__LEAD__',s['lead'])
          .replace('__CANVAS__',s['canvas']).replace('__CONTROLS__',s['controls'])
          .replace('__LEGEND__',s['legend']).replace('__ARTICLE__',s['article'])
          .replace('__SHARE__',s['share']).replace('__JS__',s['js']).replace('__ID__',s['id']))
    with open(os.path.join(d,'index.html'),'w',encoding='utf-8') as f: f.write(html)
    print('created sims/'+s['id'])
print(f'done. {len(SIMS)} sims.')
