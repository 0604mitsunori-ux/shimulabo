# -*- coding: utf-8 -*-
"""シミュラボ：診断クイズ共通エンジン（複数generatorで再利用）。
make_engines(SIMS, CAT, TPL, viz) → (tally_quiz, num_quiz, band_quiz, add, q_article, render)
 - tally_quiz: 集計式タイプ診断（最多keyの結果）
 - num_quiz : スコア→VMIN..VMAXの数値＋バンド（偏差値/％表示）
 - band_quiz: スコア→バンドのラベル
 - add      : 計算シミュ等のdictを追加（calc系）
"""
import os, json

QIN = '''    <h2>__QHEAD__</h2>
    <p style="color:var(--ink-2);font-size:13px;margin:-4px 0 6px;">直感で選んでOK。<span id="prog" style="font-weight:800;color:var(--teal-d);">0 / __QN__ 問</span></p>
    <div id="quiz" class="quiz"></div>
    <button class="btn btn-primary" id="calcBtn" style="margin-top:8px;">結果を見る</button>'''
RES_TYPE = '''      <div class="label">__RLABEL__</div>
      <div id="emoji" style="font-size:62px;line-height:1.1;">🔎</div>
      <div class="big" style="font-size:25px;"><span id="big">—</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="desc" style="text-align:left;margin-top:14px;">—</div>'''

_BUILD = r'''  const wrap=$('quiz');
  Q.forEach((qq,i)=>{const d=document.createElement('div');d.className='q';
    let h='<p class="qt"><b>Q'+(i+1)+'.</b> '+qq[0]+'</p><div class="opts" style="grid-template-columns:1fr;">';
    qq[1].forEach(o=>{h+='<button type="button" class="opt" data-q="'+i+'" data-k="'+o[1]+'">'+o[0]+'</button>';});
    d.innerHTML=h+'</div>';wrap.appendChild(d);});
  wrap.addEventListener('click',e=>{const b=e.target.closest('.opt');if(!b)return;const qi=b.dataset.q;
    wrap.querySelectorAll('.opt[data-q="'+qi+'"]').forEach(o=>o.classList.toggle('on',o===b));
    const p=$('prog');if(p)p.textContent=document.querySelectorAll('#quiz .opt.on').length+' / '+Q.length+' 問';});
  function _need(){const on=document.querySelectorAll('#quiz .opt.on');
    if(on.length<Q.length){alert('あと'+(Q.length-on.length)+'問！全部答えてね');const qs=document.querySelectorAll('#quiz .q');for(let j=0;j<qs.length;j++){if(!qs[j].querySelector('.opt.on')){qs[j].scrollIntoView({behavior:'smooth',block:'center'});break;}}return null;}return on;}
'''

def make_engines(SIMS, CAT, TPL, viz):
    def q_article(intro, title, text, faqs, note='※エンタメ診断です。気軽に楽しんでください。'):
        from gen_sims11 import faq
        return ('    <div class="note"><strong>これは何？</strong>：'+intro+'<br><b>'+note+'</b></div>\n'
                '    <h2>'+title+'</h2>\n    <p>'+text+'</p>\n    <h2>よくある質問</h2>'+faq(faqs))

    def _append(id, emoji, title, desc, ogtitle, ogdesc, h1, lead, inputs, result, visual, article, js):
        SIMS.append(dict(id=id, emoji=emoji, cat=CAT, title=title, desc=desc, ogtitle=ogtitle, ogdesc=ogdesc,
            h1=h1, lead=lead, inputs=inputs, result=result, visual=visual, article=article, js=js))

    def tally_quiz(id, emoji, title, desc, ogtitle, ogdesc, h1, lead, qhead, questions, results, rlabel, sharetpl, article):
        js=('  const Q='+json.dumps(questions,ensure_ascii=False)+';\n  const RES='+json.dumps(results,ensure_ascii=False)+';\n'
            '  const SHARETPL='+json.dumps(sharetpl,ensure_ascii=False)+';\n'+_BUILD
            + r'''  function calc(){const on=_need();if(!on)return;
    const t={};on.forEach(b=>{t[b.dataset.k]=(t[b.dataset.k]||0)+1;});
    let best=Object.keys(RES)[0],bv=-1;for(const k in RES){const v=t[k]||0;if(v>bv){bv=v;best=k;}}
    const r=RES[best];$('emoji').textContent=r[0];$('big').textContent=r[1];$('sub').textContent='あなたの結果';$('desc').textContent='✨ '+r[2];
    SHARE=SHARETPL.replace('{name}',r[1]);show();}
''')
        _append(id,emoji,title,desc,ogtitle,ogdesc,h1,lead,
            QIN.replace('__QHEAD__',qhead).replace('__QN__',str(len(questions))),RES_TYPE.replace('__RLABEL__',rlabel),'',article,js)

    def num_quiz(id, emoji, title, desc, ogtitle, ogdesc, h1, lead, qhead, questions, unit, vmin, vmax, bands, rlabel, sharetpl, article):
        maxs=sum(max(int(p) for _,p in opts) for _,opts in questions)
        # data-k に点数を入れる（_BUILDはdata-k参照）
        js=('  const Q='+json.dumps(questions,ensure_ascii=False)+';\n  const BANDS='+json.dumps(bands,ensure_ascii=False)+';\n'
            '  const MAXS='+str(maxs)+',VMIN='+str(vmin)+',VMAX='+str(vmax)+',UNIT='+json.dumps(unit,ensure_ascii=False)+',SHARETPL='+json.dumps(sharetpl,ensure_ascii=False)+';\n'+_BUILD
            + r'''  function calc(){const on=_need();if(!on)return;
    let s=0;on.forEach(b=>s+=(+b.dataset.k||0));const val=Math.round(VMIN+(s/MAXS)*(VMAX-VMIN));
    let band=BANDS[BANDS.length-1];for(const bd of BANDS){if(val<=bd[0]){band=bd;break;}}
    $('emoji').textContent=band[1];$('big').textContent=val;$('sub').textContent=band[2];$('desc').textContent='✨ '+band[3];
    SHARE=SHARETPL.replace('{val}',val).replace('{label}',band[2]);show();drawBar(val,VMAX);}
  function drawBar(v,mx){const c=$('viz');if(!c)return;const x=c.getContext('2d'),W=c.width,H=c.height,bx=20,bw=W-40,by=H/2-11;cancelAnimationFrame(raf);
    const t0=performance.now();function f(n){const p=Math.min(1,(n-t0)/800);x.fillStyle='#0b1530';x.fillRect(0,0,W,H);
      x.fillStyle='rgba(255,255,255,.1)';x.fillRect(bx,by,bw,22);const g=x.createLinearGradient(bx,0,bx+bw,0);g.addColorStop(0,'#f59e0b');g.addColorStop(1,'#ec4899');
      x.save();x.beginPath();x.rect(bx,by,bw*Math.min(1,v/mx)*p,22);x.clip();x.fillStyle=g;x.fillRect(bx,by,bw,22);x.restore();
      x.fillStyle='#fff';x.font='bold 13px sans-serif';x.textAlign='center';x.fillText(Math.round(v*p)+UNIT,W/2,by+40);
      if(p<1)raf=requestAnimationFrame(f);}raf=requestAnimationFrame(f);}
''')
        res='''      <div class="label">__RLABEL__</div>
      <div id="emoji" style="font-size:56px;line-height:1.1;">📊</div>
      <div class="big"><span id="big">—</span><span class="unit">__UNIT__</span></div>
      <div class="sub" id="sub">—</div>
      <div class="alert good" id="desc" style="text-align:left;margin-top:14px;">—</div>'''.replace('__RLABEL__',rlabel).replace('__UNIT__',unit)
        _append(id,emoji,title,desc,ogtitle,ogdesc,h1,lead,
            QIN.replace('__QHEAD__',qhead).replace('__QN__',str(len(questions))),res,viz(480,80,500),article,js)

    def band_quiz(id, emoji, title, desc, ogtitle, ogdesc, h1, lead, qhead, questions, bands, rlabel, sharetpl, article):
        maxs=sum(max(int(p) for _,p in opts) for _,opts in questions)
        js=('  const Q='+json.dumps(questions,ensure_ascii=False)+';\n  const BANDS='+json.dumps(bands,ensure_ascii=False)+';\n'
            '  const MAXS='+str(maxs)+',SHARETPL='+json.dumps(sharetpl,ensure_ascii=False)+';\n'+_BUILD
            + r'''  function calc(){const on=_need();if(!on)return;
    let s=0;on.forEach(b=>s+=(+b.dataset.k||0));
    let band=BANDS[BANDS.length-1];for(const bd of BANDS){if(s<=bd[0]){band=bd;break;}}
    $('emoji').textContent=band[1];$('big').textContent=band[2];$('sub').textContent='あなたの結果';$('desc').textContent='✨ '+band[3];
    SHARE=SHARETPL.replace('{label}',band[2]);show();}
''')
        _append(id,emoji,title,desc,ogtitle,ogdesc,h1,lead,
            QIN.replace('__QHEAD__',qhead).replace('__QN__',str(len(questions))),RES_TYPE.replace('__RLABEL__',rlabel),'',article,js)

    def add(**k):
        k.setdefault('visual','')
        k.setdefault('cat', CAT)  # cat=... をkで渡せばsimごとに上書き可
        SIMS.append(dict(**k))

    def render():
        ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        for s in SIMS:
            d=os.path.join(ROOT,'sims',s['id']); os.makedirs(d,exist_ok=True)
            html=(TPL.replace('__TITLE__',s['title']).replace('__DESC__',s['desc'])
                  .replace('__OGTITLE__',s['ogtitle']).replace('__OGDESC__',s['ogdesc'])
                  .replace('__CAT__',s['cat']).replace('__H1__',s['h1']).replace('__LEAD__',s['lead'])
                  .replace('__INPUTS__',s['inputs']).replace('__RESULT__',s['result'])
                  .replace('__VISUAL__',s.get('visual','')).replace('__ARTICLE__',s['article'])
                  .replace('__JS__',s['js']).replace('__ID__',s['id']))
            with open(os.path.join(d,'index.html'),'w',encoding='utf-8') as f: f.write(html)
            print('created sims/'+s['id'])
    return tally_quiz, num_quiz, band_quiz, add, q_article, render
