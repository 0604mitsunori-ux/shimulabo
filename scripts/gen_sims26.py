# -*- coding: utf-8 -*-
"""シミュラボ：canvas系 補充（ふしぎ3＋あそぶ3）。gen_sims17のテンプレ/ヘルパー再利用。"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_sims17 import TPL, canvas, btn, row, slider, resbox, faq

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIMS=[]
def add(**k): SIMS.append(k)

W='ふしぎ・現象'; P='あそぶ・実験'

# ===== ふしぎ・現象 =====
add(id='galton', cat=W, emoji='🎲',
  title='ガルトンボード｜ランダムから正規分布が生まれるシミュレーター｜シミュラボ',
  desc='たくさんのボールが釘にぶつかって左右にランダムに落ちるだけで、きれいな釣り鐘型（正規分布）が現れる「ガルトンボード」を体感できる無料シミュレーター。',
  ogtitle='ガルトンボード｜ランダムから正規分布が生まれる', ogdesc='ボールが左右にランダムに落ちるだけで釣り鐘型が出現。',
  h1='ガルトンボード',
  lead='ボールは釘にぶつかるたび、左右にランダムに転がるだけ。なのに、たまっていくと美しい釣り鐘型（正規分布）が現れます。ランダムの中の秩序を眺めてください。',
  canvas=canvas(520,440,560),
  controls=row(btn('reset','リセット',True)),
  legend='偶然の積み重ねが「正規分布（ベルカーブ）」を生みます。身長やテストの点の分布もこの形。',
  article='''    <h2>なぜ釣り鐘型に？</h2>
    <p>1個のボールがどこに落ちるかは完全にランダム。でも何千個も落とすと、中央が高く両端が低い「正規分布」になります。これは「たくさんの偶然が重なると安定した形が現れる（中心極限定理）」の visual な実例。自然界やデータの多くがこの形をしています。</p>
    <h2>よくある質問</h2>'''+faq([('毎回同じ形？','細部は違いますが、釣り鐘型に収束します。それが確率の不思議。'),('データは送信されますか？','いいえ。すべてブラウザ内で動きます。')]),
  share='ボールが左右にランダムに落ちるだけで、きれいな釣り鐘型が生まれる…ガルトンボード🎲 確率って美しい。',
  js='''
    const cv=$('cv'),x=cv.getContext('2d');const W=cv.width,H=cv.height;
    const rows=11,bins=rows+1,topY=24,botY=H-120,colW=W/(bins);
    let counts=new Array(bins).fill(0),balls=[],f=0;
    $('reset').addEventListener('click',()=>{counts.fill(0);balls=[];});
    function loop(){f++;if(f%5===0)balls.push({x:W/2,y:topY,row:-1,bin:0});
      x.fillStyle='#0b1020';x.fillRect(0,0,W,H);
      x.fillStyle='rgba(255,255,255,.22)';
      for(let r=0;r<rows;r++){const py=topY+(r+1)*(botY-topY)/(rows+1);const n=r+1;for(let c=0;c<n;c++){const px=W/2+(c-r/2)*colW*0.62;x.beginPath();x.arc(px,py,2,0,7);x.fill();}}
      for(const b of balls){b.y+=3.2;const r=Math.floor((b.y-topY)/((botY-topY)/(rows+1)));
        if(r>b.row&&r<rows){b.row=r;const d=Math.random()<0.5?-1:1;b.x+=d*colW*0.31;if(d>0)b.bin++;}
        if(b.y>=botY){counts[Math.max(0,Math.min(bins-1,b.bin))]++;b.dead=1;}
        x.fillStyle='#5eead4';x.beginPath();x.arc(b.x,b.y,3.4,0,7);x.fill();}
      balls=balls.filter(b=>!b.dead);
      const max=Math.max(1,...counts);
      for(let i=0;i<bins;i++){const h=counts[i]/max*96;x.fillStyle='hsl('+(190+i*9)+',82%,62%)';x.fillRect(i*colW+2,H-18-h,colW-4,h);}
      requestAnimationFrame(loop);
    } loop();
''')

add(id='lissajous', cat=W, emoji='🌀',
  title='リサージュ図形｜2つの波が描く幾何学模様シミュレーター｜シミュラボ',
  desc='縦と横、2つの単純な波（サインカーブ）を組み合わせるだけで、8の字やリボン、複雑な網目模様が生まれる「リサージュ図形」を描ける無料シミュレーター。',
  ogtitle='リサージュ図形｜2つの波が描く幾何学模様', ogdesc='縦横2つの波の周波数比で無限の幾何学模様を描く。',
  h1='リサージュ図形',
  lead='縦と横、2つのサインカーブを組み合わせるだけ。周波数の比を変えると、8の字・リボン・網目…無限の幾何学模様が現れます。理科の実験でも有名な美しい曲線です。',
  canvas=canvas(520,520,520),
  controls=slider('a','横の周波数',1,8,3)+slider('b','縦の周波数',1,8,2)+slider('delta','位相差（度）',0,180,30),
  legend='周波数の比が整数だと模様が閉じます。オシロスコープでも見られる物理の名場面。',
  article='''    <h2>リサージュ図形とは</h2>
    <p>x方向とy方向に、それぞれ単純なサイン波で動く点の軌跡です。横と縦の周波数の比（例：3対2）で模様の形が決まります。音の周波数の比較や、電気信号の解析（オシロスコープ）でも使われる、科学と美が交わる図形です。</p>
    <h2>よくある質問</h2>'''+faq([('比を変えると？','整数比ほどシンプルで閉じた形に。比が複雑だと網目状になります。'),('データは送信されますか？','いいえ。すべてブラウザ内で動きます。')]),
  share='縦横2つの波を組み合わせるだけで無限の模様…リサージュ図形🌀 周波数比を変えるのが楽しい。',
  js='''
    const cv=$('cv'),x=cv.getContext('2d');const W=cv.width,H=cv.height,cx=W/2,cy=H/2;let ph=0;
    function loop(){const a=+$('a').value,b=+$('b').value,delta=(+$('delta').value)*Math.PI/180;
      x.fillStyle='#0b1020';x.fillRect(0,0,W,H);
      const A=W*0.42,B=H*0.42;x.lineWidth=2;
      for(let t=0;t<=Math.PI*2;t+=0.008){const px=cx+A*Math.sin(a*t+delta+ph),py=cy+B*Math.sin(b*t);
        x.strokeStyle='hsl('+((t/(Math.PI*2)*300+ph*50)%360)+',85%,63%)';
        if(t===0){x.beginPath();x.moveTo(px,py);}else{x.lineTo(px,py);}}
      x.stroke();ph+=0.006;requestAnimationFrame(loop);
    } loop();
''')

add(id='magnet', cat=W, emoji='🧲',
  title='磁力線シミュレーター｜方位磁針で見る磁石の周りの力｜シミュラボ',
  desc='棒磁石の周りに並べた方位磁針が、磁力の向きにそろう様子を可視化する無料シミュレーター。磁石を回すと針も向きを変えます。',
  ogtitle='磁力線シミュレーター｜磁石の周りの力を見る', ogdesc='方位磁針が磁力の向きにそろう様子を可視化。',
  h1='磁力線シミュレーター',
  lead='棒磁石の周りに、たくさんの方位磁針を置いてみました。針はそれぞれの場所の磁力の向きにそろい、目に見えない「磁力線」が浮かび上がります。磁石を回してみてください。',
  canvas=canvas(540,440,560),
  controls=slider('rot','磁石の向き（度）',0,180,0),
  legend='N極から出てS極へ入るのが磁力線。針の赤い先がN極を指します。理科の砂鉄実験と同じ。',
  article='''    <h2>磁力線とは</h2>
    <p>磁石の周りには、目に見えない磁力の場（磁場）が広がっています。方位磁針を置くと、その場所の磁力の向きに針がそろい、N極からS極へと流れる「磁力線」が見えてきます。砂鉄を撒く理科の実験と同じ現象を、ブラウザで再現しています。</p>
    <h2>よくある質問</h2>'''+faq([('地球も磁石？','はい。地球も巨大な磁石で、だから方位磁針は北を指します。'),('データは送信されますか？','いいえ。すべてブラウザ内で動きます。')]),
  share='方位磁針が磁力の向きにそろって磁力線が見える…磁力シミュレーター🧲 砂鉄実験みたい！',
  js='''
    const cv=$('cv'),x=cv.getContext('2d');const W=cv.width,H=cv.height,cx=W/2,cy=H/2;
    function loop(){const ang=(+$('rot').value)*Math.PI/180,d=64;
      x.fillStyle='#0b1020';x.fillRect(0,0,W,H);
      const nx=cx-Math.cos(ang)*d,ny=cy-Math.sin(ang)*d,sx=cx+Math.cos(ang)*d,sy=cy+Math.sin(ang)*d;
      const step=34;
      for(let gx=step/2;gx<W;gx+=step)for(let gy=step/2;gy<H;gy+=step){
        let fx=0,fy=0;
        const ps=[[nx,ny,1],[sx,sy,-1]];
        for(let k=0;k<2;k++){const dx=gx-ps[k][0],dy=gy-ps[k][1],r=Math.hypot(dx,dy)+10,f=ps[k][2]/(r*r);fx+=dx/r*f;fy+=dy/r*f;}
        const a=Math.atan2(fy,fx),mag=Math.min(1,Math.hypot(fx,fy)*5000);
        x.save();x.translate(gx,gy);x.rotate(a);
        x.strokeStyle='rgba(130,200,255,'+(0.25+mag*0.6)+')';x.lineWidth=2;x.beginPath();x.moveTo(-9,0);x.lineTo(9,0);x.stroke();
        x.fillStyle='#f43f5e';x.beginPath();x.arc(9,0,2.4,0,7);x.fill();x.restore();
      }
      x.save();x.translate(cx,cy);x.rotate(ang);
      x.fillStyle='#3b82f6';x.fillRect(-d,-11,d,22);x.fillStyle='#ef4444';x.fillRect(0,-11,d,22);
      x.fillStyle='#fff';x.font='bold 13px sans-serif';x.textAlign='center';x.textBaseline='middle';x.fillText('N',-d/2,1);x.fillText('S',d/2,1);x.restore();
      requestAnimationFrame(loop);
    } loop();
''')

# ===== あそぶ・実験 =====
add(id='kaleido', cat=P, emoji='🔮',
  title='万華鏡シミュレーター｜マウスで描く対称模様｜シミュラボ',
  desc='マウスやタッチでなぞるだけで、左右対称・回転対称の美しい万華鏡模様が描ける無料のお絵かきシミュレーター。',
  ogtitle='万華鏡シミュレーター｜マウスで描く対称模様', ogdesc='なぞるだけで万華鏡のような対称模様が描ける。',
  h1='万華鏡シミュレーター',
  lead='画面をマウスでなぞる（タッチでもOK）と、対称にコピーされて万華鏡のような模様が生まれます。何も考えず動かすだけで、自分だけのアート作品に。',
  canvas=canvas(500,500,500,'cursor:crosshair;background:#0b1020;'),
  controls=slider('sym','対称の数',4,16,8,'2')+row(btn('clear','クリア',True)),
  legend='なぞった線が対称にコピーされます。色は動かすほど変化。スクショで保存できます。',
  article='''    <h2>対称の美しさ</h2>
    <p>本物の万華鏡は、鏡の反射で1つの模様が何重にもコピーされて見えます。このシミュレーターも同じ原理で、なぞった線を回転・反転コピー。左右対称・回転対称が生む整った美しさを、自分の手で作り出せます。気に入った模様はスクリーンショットで保存を。</p>
    <h2>よくある質問</h2>'''+faq([('保存できる？','スクリーンショットで保存できます。'),('データは送信されますか？','いいえ。すべてブラウザ内で動きます。')]),
  share='なぞるだけで万華鏡みたいな対称模様が描ける…万華鏡シミュレーター🔮 無心になれる。',
  js='''
    const cv=$('cv'),x=cv.getContext('2d');const W=cv.width,H=cv.height,cx=W/2,cy=H/2;
    x.fillStyle='#0b1020';x.fillRect(0,0,W,H);let last=null,hue=0;
    function seg(x0,y0,x1,y1){const n=+$('sym').value;hue=(hue+5)%360;x.strokeStyle='hsl('+hue+',85%,62%)';x.lineWidth=3;x.lineCap='round';
      for(let i=0;i<n;i++){const a=i/n*Math.PI*2;for(let m=-1;m<=1;m+=2){x.save();x.translate(cx,cy);x.rotate(a);x.scale(1,m);x.beginPath();x.moveTo(x0-cx,y0-cy);x.lineTo(x1-cx,y1-cy);x.stroke();x.restore();}}}
    cv.addEventListener('pointerdown',e=>{const p=cpos(cv,e);last=p;});
    cv.addEventListener('pointermove',e=>{if(e.buttons===0&&!(e.pointerType==='touch'))return;const p=cpos(cv,e);if(last)seg(last[0],last[1],p[0],p[1]);last=p;});
    cv.addEventListener('pointerup',()=>last=null);cv.addEventListener('pointerleave',()=>last=null);
    cv.addEventListener('touchmove',e=>{e.preventDefault();const p=cpos(cv,e);if(last)seg(last[0],last[1],p[0],p[1]);last=p;},{passive:false});
    cv.addEventListener('touchstart',e=>{const p=cpos(cv,e);last=p;},{passive:true});
    $('clear').addEventListener('click',()=>{x.fillStyle='#0b1020';x.fillRect(0,0,W,H);});
''')

add(id='aim-trainer', cat=P, emoji='🎯',
  title='エイム的当てゲーム｜30秒で何個タップできる？｜シミュラボ',
  desc='次々に現れる的を30秒でできるだけ多くタップ（クリック）する、反射神経と正確さを鍛えるエイム練習ゲーム型シミュレーター。',
  ogtitle='エイム的当てゲーム｜30秒で何個？', ogdesc='30秒で的を何個タップできるか挑戦。スコアをシェア。',
  h1='エイム的当てゲーム',
  lead='次々に現れる的を、30秒でできるだけ多くタップ（クリック）！反射神経と正確さの勝負です。FPSのエイム練習にも。スコアを友達と競おう。',
  canvas=canvas(520,400,560,'cursor:crosshair;'),
  controls=row(btn('start','スタート',True))+resbox(),
  legend='的をタップすると次が出現。30秒で何個当てられるか挑戦！',
  article='''    <h2>反射神経と正確さ</h2>
    <p>動く目標を素早く正確に狙う力は、ゲームだけでなくスポーツや運転にも通じます。焦って外すとタイムロス。落ち着いて、でも素早く——のバランスが高スコアのコツ。繰り返すと上達するので、記録更新を目指してみてください。</p>
    <h2>よくある質問</h2>'''+faq([('スマホでもできる？','はい。タップで遊べます。'),('データは送信されますか？','いいえ。すべてブラウザ内で動きます。')]),
  share='エイム的当てゲーム🎯 30秒で何個タップできるか挑戦！君のスコアは？',
  js='''
    const cv=$('cv'),x=cv.getContext('2d');const W=cv.width,H=cv.height;
    let target=null,score=0,playing=false,tEnd=0;
    function spawn(){const r=16+Math.random()*16;target={x:r+Math.random()*(W-2*r),y:r+Math.random()*(H-2*r),r:r};}
    function draw(){x.fillStyle='#0b1020';x.fillRect(0,0,W,H);
      if(playing){const left=Math.max(0,(tEnd-performance.now())/1000);
        if(target){x.fillStyle='#f43f5e';x.beginPath();x.arc(target.x,target.y,target.r,0,7);x.fill();x.fillStyle='#fff';x.beginPath();x.arc(target.x,target.y,target.r*0.4,0,7);x.fill();}
        x.fillStyle='#fff';x.font='bold 16px sans-serif';x.textAlign='left';x.fillText('スコア '+score,12,24);x.textAlign='right';x.fillText('残り '+left.toFixed(1)+'s',W-12,24);
        if(left<=0){playing=false;target=null;$('res').style.display='';$('res').innerHTML='30秒で <span style="font-size:26px;color:var(--accent-d)">'+score+'</span> 個命中！';SHARE='エイム的当てゲーム、30秒で'+score+'個命中したよ🎯 君は？';}}
      else if(!target){x.fillStyle='#fff';x.textAlign='center';x.font='bold 19px sans-serif';x.fillText('スタートを押して的をタップ！',W/2,H/2);}
      requestAnimationFrame(draw);}
    cv.addEventListener('pointerdown',e=>{if(!playing||!target)return;const p=cpos(cv,e);if(Math.hypot(p[0]-target.x,p[1]-target.y)<=target.r){score++;spawn();}});
    $('start').addEventListener('click',()=>{score=0;playing=true;tEnd=performance.now()+30000;spawn();$('res').style.display='none';});
    draw();
''')

add(id='color-test', cat=P, emoji='👁️',
  title='色当てゲーム｜1つだけ違う色、どこまで見分けられる？｜シミュラボ',
  desc='並んだタイルの中から、1つだけ微妙に色が違うタイルを見つけるゲーム。レベルが上がるほど色の差が小さく難しくなる、色覚チャレンジ型シミュレーター。',
  ogtitle='色当てゲーム｜違う色、どこまで見分けられる？', ogdesc='1つだけ違う色を探すゲーム。何レベルまでいける？',
  h1='色当てゲーム',
  lead='並んだタイルの中に、1つだけ微妙に色が違うものが。それを見つけてタップ！正解するほど色の差は小さく、マスは増えて難しくなります。あなたの色を見分ける力は？',
  canvas=canvas(440,440,440,'cursor:pointer;'),
  controls='<div id="lv" style="text-align:center;font-weight:800;margin-bottom:8px;">スタートを押してね</div>'+row(btn('start','スタート',True))+resbox(),
  legend='1つだけ違う色のタイルをタップ。レベルが上がると差が小さくなります。',
  article='''    <h2>色を見分ける力</h2>
    <p>人の目はわずかな色の違いも見分けられますが、その精度には個人差があります。このゲームはレベルが上がるほど色差が小さくなり、マスも増えていきます。どこまで見分けられるか挑戦してみてください。明るい画面・適度な距離で見るのがコツ。</p>
    <h2>よくある質問</h2>'''+faq([('色覚検査になる？','いいえ。あくまでゲームです。医学的な検査ではありません。'),('データは送信されますか？','いいえ。すべてブラウザ内で動きます。')]),
  share='色当てゲーム👁️ 1つだけ違う色、どこまで見分けられる？君は何レベル？',
  js='''
    const cv=$('cv'),x=cv.getContext('2d');const W=cv.width,H=cv.height;
    let level=1,grid=2,oddIdx=0,baseCol='',oddCol='',playing=false;
    function rr(px,py,w,h,r){x.beginPath();x.moveTo(px+r,py);x.arcTo(px+w,py,px+w,py+h,r);x.arcTo(px+w,py+h,px,py+h,r);x.arcTo(px,py+h,px,py,r);x.arcTo(px,py,px+w,py,r);x.closePath();}
    function next(){grid=Math.min(7,1+Math.ceil((level+1)/2));const diff=Math.max(4,40-level*2.4);
      const bh=Math.random()*360,bs=55+Math.random()*20,bl=45+Math.random()*15;
      baseCol='hsl('+bh+','+bs+'%,'+bl+'%)';oddCol='hsl('+bh+','+bs+'%,'+(bl+diff*(Math.random()<0.5?-1:1))+'%)';
      oddIdx=Math.floor(Math.random()*grid*grid);draw();}
    function draw(){x.fillStyle='#0b1020';x.fillRect(0,0,W,H);const gap=6,cell=(W-gap*(grid+1))/grid;
      for(let i=0;i<grid*grid;i++){const r=Math.floor(i/grid),c=i%grid,px=gap+c*(cell+gap),py=gap+r*(cell+gap);
        x.fillStyle=(i===oddIdx)?oddCol:baseCol;rr(px,py,cell,cell,8);x.fill();}}
    cv.addEventListener('pointerdown',e=>{if(!playing)return;const p=cpos(cv,e);const gap=6,cell=(W-gap*(grid+1))/grid;
      const c=Math.floor((p[0]-gap)/(cell+gap)),r=Math.floor((p[1]-gap)/(cell+gap));if(c<0||c>=grid||r<0||r>=grid)return;const idx=r*grid+c;
      if(idx===oddIdx){level++;$('lv').textContent='レベル '+level;next();}
      else{playing=false;$('res').style.display='';$('res').innerHTML='ゲームオーバー！レベル <span style="font-size:24px;color:var(--accent-d)">'+level+'</span> まで到達👁️';SHARE='色当てゲーム、レベル'+level+'まで到達できた👁️ 君は？';}});
    $('start').addEventListener('click',()=>{level=1;playing=true;$('res').style.display='none';$('lv').textContent='レベル 1';next();});
    x.fillStyle='#0b1020';x.fillRect(0,0,W,H);
''')

def render():
    for s in SIMS:
        d=os.path.join(ROOT,'sims',s['id']); os.makedirs(d,exist_ok=True)
        html=(TPL.replace('__TITLE__',s['title']).replace('__DESC__',s['desc'])
              .replace('__OGTITLE__',s['ogtitle']).replace('__OGDESC__',s['ogdesc'])
              .replace('__CAT__',s['cat']).replace('__H1__',s['h1']).replace('__LEAD__',s['lead'])
              .replace('__CANVAS__',s.get('canvas','')).replace('__CONTROLS__',s['controls'])
              .replace('__LEGEND__',s['legend']).replace('__ARTICLE__',s['article'])
              .replace('__SHARE__',s['share']).replace('__JS__',s['js']).replace('__ID__',s['id']))
        with open(os.path.join(d,'index.html'),'w',encoding='utf-8') as f: f.write(html)
        print('created sims/'+s['id'])

if __name__=='__main__':
    render()
    print(f'canvas batch done. {len(SIMS)} sims.')
