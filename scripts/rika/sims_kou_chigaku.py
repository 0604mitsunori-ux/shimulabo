# -*- coding: utf-8 -*-
"""理科の授業向け（第4弾・高校地学）：コリオリの力と大気の大循環／エラトステネスの方法で地球の大きさを測る
   照合メモ（2026-10-18）
   - coriolis-henseifu：Ω＝7.29×10⁻⁵ rad/s（2π÷1恒星日 86,164 s ＝ 7.292×10⁻⁵）。f＝2Ω sinφ：北緯30° 7.29×10⁻⁵、
     35° 8.36×10⁻⁵、45° 1.03×10⁻⁴、90° 1.458×10⁻⁴ /s（Python で別計算）。地衡風の例：Δp/Δn＝4 hPa/400 km、ρ＝1.2 kg/m³、
     北緯35° → V＝1.0×10⁻³ ÷（1.2×8.36×10⁻⁵）＝9.96 m/s。回る円盤：半径1 m・1分間に10回転・秒速1 m → ふちまで1.00秒で60°。
   - eratosthenes：925 km×360÷7.2＝46,250 km。tan7.2°＝0.1263。都道府県庁の緯度経度（世界測地系。地理院地図で読める値と同じ）から、
     GRS80楕円体の子午線弧長（数値積分）と Vincenty の式で2地点間の距離を計算し、球面（半径6,371 km）の haversine と 0.5%以内で一致を確認。
     子午線の全周 40,007.9 km・赤道の全周 40,075.0 km・緯度1°の子午線の長さ 赤道110.57／35° 110.94／45° 111.13／極 111.69 km。
     シエネ（アスワン 北緯24.09°・東経32.90°）—アレクサンドリア（北緯31.20°・東経29.92°）：緯度差7.11°・南北788 km・2地点間841 km。
"""
import json, math
from common import canvas, slider, select, btn, stats, T, N, P

SIMS = []
def sim(**kw): SIMS.append(kw)

def A(url, text=None): return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (url, text or url)
def NW(t): return '<span style="white-space:nowrap">%s</span>' % t
MEXT_KOU = "https://www.mext.go.jp/a_menu/shotou/new-cs/1407074.htm"

# ============================================================ 数値（記事の表と JS のデータを同じ計算から作る）
OM = 7.29e-5
def fpar(p): return 2 * OM * math.sin(math.radians(p))

GA, GF = 6378137.0, 1 / 298.257222101          # GRS80
GB, GE2 = GA * (1 - GF), GF * (2 - GF)
def merid(p, n=4000):
    """赤道から緯度 p までの子午線弧長 [m]（シンプソン則）"""
    h = math.radians(p) / n; s = 0.0
    for i in range(n + 1):
        q = h * i; w = 1 if i in (0, n) else (4 if i % 2 else 2)
        s += w * GA * (1 - GE2) / (1 - GE2 * math.sin(q) ** 2) ** 1.5
    return s * h / 3
def vincenty(l1, o1, l2, o2):
    L = math.radians(o2 - o1); U1 = math.atan((1 - GF) * math.tan(math.radians(l1))); U2 = math.atan((1 - GF) * math.tan(math.radians(l2)))
    lam = L
    for _ in range(200):
        sl, cl = math.sin(lam), math.cos(lam)
        ss = math.hypot(math.cos(U2) * sl, math.cos(U1) * math.sin(U2) - math.sin(U1) * math.cos(U2) * cl)
        cs = math.sin(U1) * math.sin(U2) + math.cos(U1) * math.cos(U2) * cl
        sg = math.atan2(ss, cs); sa = math.cos(U1) * math.cos(U2) * sl / ss; c2a = 1 - sa * sa
        c2m = cs - 2 * math.sin(U1) * math.sin(U2) / c2a
        C = GF / 16 * c2a * (4 + GF * (4 - 3 * c2a)); lp = lam
        lam = L + (1 - C) * GF * sa * (sg + C * ss * (c2m + C * cs * (-1 + 2 * c2m * c2m)))
        if abs(lam - lp) < 1e-13: break
    u2 = c2a * (GA * GA - GB * GB) / (GB * GB)
    Aa = 1 + u2 / 16384 * (4096 + u2 * (-768 + u2 * (320 - 175 * u2))); Bb = u2 / 1024 * (256 + u2 * (-128 + u2 * (74 - 47 * u2)))
    ds = Bb * ss * (c2m + Bb / 4 * (cs * (-1 + 2 * c2m * c2m) - Bb / 6 * c2m * (-3 + 4 * ss * ss) * (-3 + 4 * c2m * c2m)))
    return GB * Aa * (sg - ds)

MERID_CIRC = 4 * merid(90) / 1000      # 40,007.9 km
# 都道府県庁の位置（世界測地系・小数第4位）
CITY = {"札幌": (43.0643, 141.3469), "青森": (40.8246, 140.7405), "仙台": (38.2686, 140.8721), "水戸": (36.3417, 140.4468),
        "新潟": (37.9025, 139.0232), "前橋": (36.3907, 139.0605), "福岡": (33.6064, 130.4180), "鹿児島": (31.5602, 130.5580),
        "松江": (35.4723, 133.0505), "高知": (33.5597, 133.5311), "那覇": (26.2124, 127.6809)}
PAIR_KEYS = [("青森", "仙台"), ("青森", "水戸"), ("札幌", "水戸"), ("新潟", "前橋"), ("福岡", "鹿児島"), ("松江", "高知"), ("札幌", "那覇")]
PAIRS = []
for a_, b_ in PAIR_KEYS:
    (l1, o1), (l2, o2) = CITY[a_], CITY[b_]
    ns = abs(merid(l1) - merid(l2)) / 1000; geo = vincenty(l1, o1, l2, o2) / 1000
    PAIRS.append([a_, l1, o1, b_, l2, o2, round(ns, 1), round(geo, 1)])
assert abs(PAIRS[0][6] - 283.8) < 0.2 and abs(MERID_CIRC - 40007.9) < 0.2
PAIRS_JS = json.dumps(PAIRS, ensure_ascii=False, separators=(",", ":"))
PAIR_OPTS = [(str(i), "%s—%s（緯度差%.2f°）%s" % (q[0], q[3], q[1] - q[4], "※経度差大" if abs(q[2] - q[5]) > 5 else ""))
             for i, q in enumerate(PAIRS)]

def f3(v): return ("%.1f" % v)
def comma(v): return "{:,}".format(int(round(v)))
PAIR_TABLE = T([[NW(q[0] + "—" + q[3]), "%.3f°" % (q[1] - q[4]), "%.2f°" % abs(q[2] - q[5]), f3(q[6]) + " km", f3(q[7]) + " km",
                 NW(comma(q[6] * 360 / (q[1] - q[4])) + " km"), NW(comma(q[7] * 360 / (q[1] - q[4])) + " km")] for q in PAIRS],
               ["2地点（都道府県庁）", "緯度の差", "経度の差", "南北の距離", "2地点間の距離", "一周（南北の距離で）", "一周（2地点間の距離で）"])
F_TABLE = T([[NW("%d°" % p), "%.3f" % math.sin(math.radians(p)), NW("%.2f×10⁻⁵" % (fpar(p) / 1e-5)), NW("%.2f×10⁻⁴ N" % (fpar(p) * 10 / 1e-4))]
             for p in (0, 10, 20, 30, 35, 40, 45, 60, 90)],
            ["緯度φ", "sinφ", "f＝2Ω sinφ［/s］", "風速10 m/sの空気1 kgにはたらくコリオリの力"])
TAN_TABLE = T([[NW("%s°" % (("%.1f" % d) if d != int(d) else "%d" % d)), "%.3f" % math.tan(math.radians(d)), "%.1f cm" % (100 * math.tan(math.radians(d)))]
               for d in (5, 7.2, 10, 20, 30, 35, 40, 45)],
              ["太陽の光と棒のなす角（天頂からの角度）", "tan", "高さ1 mの棒の影の長さ"])

# ============================================================ 共通（描画の小道具）
UI_COMMON = r'''
  const F=(s,b)=>(b?'bold ':'')+s+'px system-ui,-apple-system,"Hiragino Sans","Noto Sans JP",sans-serif';
  function rr(a,b,w,h,r){ x.beginPath(); x.moveTo(a+r,b); x.arcTo(a+w,b,a+w,b+h,r); x.arcTo(a+w,b+h,a,b+h,r); x.arcTo(a,b+h,a,b,r); x.arcTo(a,b,a+w,b,r); x.closePath(); }
  function txt(t,px,py,col,sz,b,al,bl,maxw){ let s=sz; x.font=F(s,b); if(maxw){ while(s>8&&x.measureText(t).width>maxw){ s-=0.5; x.font=F(s,b); } } x.fillStyle=col; x.textAlign=al||'left'; x.textBaseline=bl||'alphabetic'; x.fillText(t,px,py); }
  function halo(t,px,py,col,sz,b,al,bg){ x.font=F(sz,b); x.textAlign=al||'center'; x.textBaseline='middle'; x.lineJoin='round'; x.lineWidth=3.5; x.strokeStyle=bg||'rgba(255,255,255,.92)'; x.strokeText(t,px,py); x.fillStyle=col; x.fillText(t,px,py); }
  function head(px,py,a,sz,col){ x.fillStyle=col; x.beginPath(); x.moveTo(px,py); x.lineTo(px-sz*Math.cos(a-0.45),py-sz*Math.sin(a-0.45)); x.lineTo(px-sz*Math.cos(a+0.45),py-sz*Math.sin(a+0.45)); x.closePath(); x.fill(); }
  function arrow(x1,y1,x2,y2,col,lw,hs){ const a=Math.atan2(y2-y1,x2-x1), L=Math.hypot(x2-x1,y2-y1); if(L<1) return; hs=Math.min(hs||8,L*0.8); x.strokeStyle=col; x.lineWidth=lw||2; x.beginPath(); x.moveTo(x1,y1); x.lineTo(x2-Math.cos(a)*hs*0.6,y2-Math.sin(a)*hs*0.6); x.stroke(); head(x2,y2,a,hs,col); }
  function tabs(list,cur){ const w=(W-12)/list.length; list.forEach((t,i)=>{ const on=i===cur; x.fillStyle=on?'#0e7490':'#e2e8f0'; rr(6+i*w+2,5,w-4,32,8); x.fill(); txt(t,6+i*w+w/2,21.5,on?'#fff':'#334155',14,1,'center','middle',w-12); }); }
  function showField(id,on){ const e=$(id); if(!e) return; const f=e.closest('.field'); if(f) f.style.display=on?'':'none'; }
  function showBtn(id,on){ const e=$(id); if(e) e.style.display=on?'':'none'; }
  function setK(id,t){ const e=$(id); if(e&&e.previousElementSibling) e.previousElementSibling.textContent=t; }
  function fit(id,v){ setStat(id,v); const e=$(id); if(e) e.style.fontSize=v.length>11?'13px':v.length>8?'15px':v.length>6?'17px':''; }
'''

# ============================================================ 1 コリオリの力と大気の大循環
JS1 = r'''
  const cv=$('cv'); const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; let x=cv.getContext('2d'); x.setTransform(dpr,0,0,dpr,0,0);
%%UI%%
  const R=Math.PI/180, OM=7.29e-5, SLOW=0.5;
  let lastKey=''; function upd(k,fn){ if(k!==lastKey){ lastKey=k; fn(); } }
  const MODES=['① 回る円盤','② 緯度と風の曲がり方','③ 大気の大循環'], MV=['disk','earth','gc'];
  const hm=MV.indexOf((location.hash||'').slice(1));
  let mode=hm>=0?hm:Math.max(0,MV.indexOf($('mode').value)), lat=+$('lat').value, ang=0, throws=[], last=0, drag=false;
  if(hm>=0) $('mode').value=MV[hm];
  const latName=(p)=>p===0?'赤道（緯度0°）':(p>0?'北緯':'南緯')+Math.abs(p)+'°';
  const fval=(p)=>2*OM*Math.sin(p*R);
  const SUP={'-':'⁻','0':'⁰','1':'¹','2':'²','3':'³','4':'⁴','5':'⁵','6':'⁶','7':'⁷','8':'⁸','9':'⁹'};
  function sci(v,d){ if(Math.abs(v)<1e-12) return '0'; let e=Math.floor(Math.log10(Math.abs(v))), m=v/Math.pow(10,e); if(Math.abs(+m.toFixed(d))>=10){ e++; m/=10; } return m.toFixed(d).replace('-','−')+'×10'+String(e).split('').map(c=>SUP[c]).join(''); }
  function latLabel(){ setStat('latL',latName(lat)); const l=$('latL'); if(l) l.textContent=latName(lat); }

  // ---------------- ① 回る円盤（半径1 m）
  const DK=[[165,246],[475,246]], DR=128;
  const om=()=>(+$('rpm').value)*2*Math.PI/60*($('dir').value==='cw'?-1:1), vb=()=>+$('vb').value;
  const rot=(px,py,a)=>[px*Math.cos(a)-py*Math.sin(a), px*Math.sin(a)+py*Math.cos(a)];
  function newThrow(){ const th={b0:Math.PI/2+ang, s:0, pts:[[0,0,0,0]], done:false}; throws.push(th); if(throws.length>3) throws.shift(); return th; }
  function stepThrow(th,dt){ if(th.done) return; th.s+=dt; let d=vb()*th.s; if(d>=1){ d=1; th.done=true; }
    const xi=d*Math.cos(th.b0), yi=d*Math.sin(th.b0), r=rot(xi,yi,-ang); th.pts.push([xi,yi,r[0],r[1]]); }
  function instantThrow(){ throws=[]; ang=0; const th=newThrow(), dt=0.004; let n=0; while(!th.done&&n<5000){ ang+=om()*dt; stepThrow(th,dt); n++; } }
  function arcArrow(cx,cy,r,a1,a2,col){ x.strokeStyle=col; x.lineWidth=2.5; x.beginPath(); for(let i=0;i<=20;i++){ const a=a1+(a2-a1)*i/20; i?x.lineTo(cx+r*Math.cos(a),cy-r*Math.sin(a)):x.moveTo(cx+r*Math.cos(a),cy-r*Math.sin(a)); } x.stroke();
    const s=Math.sign(a2-a1), tx=-Math.sin(a2)*s, ty=-Math.cos(a2)*s; head(cx+r*Math.cos(a2)+tx*4,cy-r*Math.sin(a2)+ty*4,Math.atan2(ty,tx),10,col); }
  function drawDisk(k){ const cx=DK[k][0], cy=DK[k][1], r0=k===0?ang:0, w=om();
    x.fillStyle='#fef3c7'; x.beginPath(); x.arc(cx,cy,DR,0,2*Math.PI); x.fill();
    const sa=-(Math.PI/2+r0); x.fillStyle='rgba(251,191,36,.38)'; x.beginPath(); x.moveTo(cx,cy); x.arc(cx,cy,DR,sa-Math.PI/9,sa+Math.PI/9); x.closePath(); x.fill();
    x.strokeStyle='rgba(180,83,9,.28)'; x.lineWidth=1; for(let i=0;i<8;i++){ const a=r0+i*Math.PI/4; x.beginPath(); x.moveTo(cx,cy); x.lineTo(cx+DR*Math.cos(a),cy-DR*Math.sin(a)); x.stroke(); }
    x.beginPath(); x.arc(cx,cy,DR/2,0,2*Math.PI); x.stroke(); x.strokeStyle='#b45309'; x.lineWidth=2; x.beginPath(); x.arc(cx,cy,DR,0,2*Math.PI); x.stroke();
    if(k===0&&Math.abs(w)>1e-6){ const a0=w>0?200*R:250*R, a1=w>0?250*R:200*R; arcArrow(cx,cy,DR+11,a0,a1,'#b45309'); arcArrow(cx,cy,DR+11,a0+Math.PI,a1+Math.PI,'#b45309'); }
    if(k===1){ x.setLineDash([5,4]); x.strokeStyle='rgba(30,41,59,.45)'; x.lineWidth=1.5; x.beginPath(); x.moveTo(cx,cy); x.lineTo(cx,cy-DR); x.stroke(); x.setLineDash([]); }
    // 軌跡
    throws.forEach((th,j)=>{ const newest=j===throws.length-1, ix=k===0?0:2; x.strokeStyle=newest?'#dc2626':'rgba(220,38,38,.3)'; x.lineWidth=newest?3:2; x.lineCap='round';
      x.beginPath(); th.pts.forEach((q,i)=>{ const px=cx+q[ix]*DR, py=cy-q[ix+1]*DR; i?x.lineTo(px,py):x.moveTo(px,py); }); x.stroke(); x.lineCap='butt'; });
    const th=throws[throws.length-1];
    if(th){ const ix=k===0?0:2, q=th.pts[th.pts.length-1], px=cx+q[ix]*DR, py=cy-q[ix+1]*DR;
      if(k===1&&th.done){ const dv=om()/vb(), la=Math.PI/2-dv; if(Math.abs(dv)>0.02){ x.strokeStyle='#7c3aed'; x.lineWidth=2.2; x.beginPath(); for(let i=0;i<=24;i++){ const a=Math.PI/2+(la-Math.PI/2)*i/24; const rr2=DR*0.66; i?x.lineTo(cx+rr2*Math.cos(a),cy-rr2*Math.sin(a)):x.moveTo(cx+rr2*Math.cos(a),cy-rr2*Math.sin(a)); } x.stroke();
          const am=Math.PI/2+(la-Math.PI/2)/2; halo(Math.round(Math.abs(dv)/R)+'°',cx+DR*0.8*Math.cos(am),cy-DR*0.8*Math.sin(am),'#6d28d9',14,1); } }
      if(k===1&&!th.done&&th.pts.length>2){ const p0=th.pts[th.pts.length-3], vx=q[2]-p0[2], vy=q[3]-p0[3], l=Math.hypot(vx,vy)||1, s=Math.sign(om());
        if(s) arrow(px,py,px+vy/l*30*s,py+vx/l*30*s,'#7c3aed',2.5,9); }
      x.fillStyle='#fff'; x.strokeStyle='#111827'; x.lineWidth=2; x.beginPath(); x.arc(px,py,7,0,2*Math.PI); x.fill(); x.stroke(); }
    // 人
    const ca=Math.PI/2+r0, qx=cx+DR*Math.cos(ca), qy=cy-DR*Math.sin(ca);
    x.fillStyle='#2563eb'; x.beginPath(); x.arc(qx,qy,8,0,2*Math.PI); x.fill(); x.strokeStyle='#fff'; x.lineWidth=2; x.stroke();
    halo('受ける人',qx+Math.cos(ca)*20+(Math.abs(Math.cos(ca))>0.5?Math.sign(Math.cos(ca))*14:0),qy-Math.sin(ca)*20,'#1d4ed8',12,1);
    x.fillStyle='#16a34a'; x.beginPath(); x.arc(cx,cy,7,0,2*Math.PI); x.fill(); x.strokeStyle='#fff'; x.lineWidth=2; x.stroke();
    halo('投げる人',cx,cy+19,'#15803d',12,1);
  }
  function drawM0(){ const w=om(), v=vb(), T=1/v, dv=Math.abs(w)*T/R, rpm=+$('rpm').value, ccw=$('dir').value!=='cw';
    x.fillStyle='#fff'; x.fillRect(0,0,W,H);
    txt('外（止まっている所）から見る',DK[0][0],60,'#0f172a',15,1,'center','alphabetic',300); txt('玉はまっすぐ進む',DK[0][0],79,'#475569',13,0,'center');
    txt('円盤の上（いっしょに回る人）から見る',DK[1][0],60,'#0f172a',15,1,'center','alphabetic',300);
    txt(rpm===0?'回っていないのでまっすぐ':(ccw?'玉は進む向きの右へ曲がって見える':'玉は進む向きの左へ曲がって見える'),DK[1][0],79,'#7c3aed',13,1,'center','alphabetic',300);
    x.strokeStyle='#e2e8f0'; x.lineWidth=1; x.beginPath(); x.moveTo(W/2,48); x.lineTo(W/2,388); x.stroke();
    drawDisk(0); drawDisk(1);
    x.fillStyle='#f1f5f9'; rr(6,394,W-12,120,10); x.fill();
    txt((rpm===0?'円盤は止まっている':'1分間に'+rpm+'回転（1周'+(60/rpm).toFixed(1)+'秒）・'+(ccw?'反時計回り（北半球と同じ）':'時計回り（南半球と同じ）')),18,418,'#0f172a',14,1,'left','alphabetic',W-36);
    txt('秒速'+v.toFixed(1)+' mの玉が、半径1 mの円盤のふちに届くまで '+T.toFixed(2)+'秒'+(rpm?' → その間に円盤は '+Math.round(dv)+'° 回る':''),18,442,'#334155',13,0,'left','alphabetic',W-36);
    txt(rpm===0?'円盤が回っていなければ、どちらから見ても玉はまっすぐ進みます':'円盤の上から見ると、玉は進む向きの'+(ccw?'右':'左')+'へ曲がり、'+Math.round(dv)+'° それて届く',18,468,'#6d28d9',15,1,'left','alphabetic',W-36);
    txt('紫の矢印＝コリオリの力（回る円盤の上で見える見かけの力）。動きはスロー再生（実際の1/2の速さ）',18,494,'#64748b',11.5,0,'left','alphabetic',W-36);
    tabs(MODES,mode);
    upd('0|'+rpm+'|'+v+'|'+ccw,()=>{ setK('s1','円盤の1周'); setK('s2','ふちに届くまで'); setK('s3','曲がって見える角度'); setK('s4','曲がる向き');
    fit('s1',rpm?(60/rpm).toFixed(1)+'秒':'回転なし'); fit('s2',T.toFixed(2)+'秒'); fit('s3',Math.round(dv)+'°'); fit('s4',rpm===0?'曲がらない':(ccw?'右へ（北半球）':'左へ（南半球）'));
    setShare('【コリオリの力】1分間に'+rpm+'回転する円盤の中心から秒速'+v.toFixed(1)+'mで玉を投げると、円盤の上からは'+(rpm===0?'まっすぐ進む':(ccw?'右':'左')+'へ'+Math.round(dv)+'°曲がって見える')+'｜シミュラボ'); });
  }

  // ---------------- ② 地球：緯度とコリオリパラメータ、低気圧・高気圧
  const GX=125, GY=160, GR=86, E=18*R, F0=2.2, KF=0.55, GG=55, ROUT=94, LC=[446,162], HC=[446,398];
  let parts=[];
  function gp(la,lo){ const cl=Math.cos(la*R); return [GX+GR*cl*Math.sin(lo*R), GY-GR*(Math.sin(la*R)*Math.cos(E)-cl*Math.cos(lo*R)*Math.sin(E)), cl*Math.cos(lo*R)*Math.cos(E)+Math.sin(la*R)*Math.sin(E)]; }
  function newP(k,fill){ const a=Math.random()*2*Math.PI, r=k===0?(fill?12+(ROUT-12)*Math.random():ROUT*(0.86+0.14*Math.random())):(fill?3+(ROUT-6)*Math.random():3+12*Math.random()); return {k:k,x:r*Math.cos(a),y:r*Math.sin(a),vx:0,vy:0,tr:[],age:0}; }
  function initParts(){ parts=[]; for(let i=0;i<64;i++){ parts.push(newP(0,true)); parts.push(newP(1,true)); } for(let i=0;i<260;i++) stepParts(1/60); }
  function stepParts(dt){ const f=F0*Math.sin(lat*R), n=2, h=dt/n;
    for(const p of parts){ for(let i=0;i<n;i++){ const r=Math.hypot(p.x,p.y)||1, s=p.k===0?-1:1; let gx=s*GG*p.x/r, gy=s*GG*p.y/r; if(p.k===0&&r<6){ gx=0; gy=0; }
        p.vx+=gx*h; p.vy+=gy*h; const a=-f*h, c=Math.cos(a), sn=Math.sin(a), vx=p.vx*c-p.vy*sn, vy=p.vx*sn+p.vy*c; p.vx=vx*(1-KF*h); p.vy=vy*(1-KF*h); p.x+=p.vx*h; p.y+=p.vy*h; }
      p.age+=dt; p.tr.push([p.x,p.y]); if(p.tr.length>34) p.tr.shift();
      const r=Math.hypot(p.x,p.y); if((p.k===0&&r<9)||(p.k===1&&r>ROUT)||p.age>16) Object.assign(p,newP(p.k,false)); } }
  function drawGlobe(){ const f=fval(lat);
    const g=x.createRadialGradient(GX-30,GY-30,10,GX,GY,GR); g.addColorStop(0,'#7dd3fc'); g.addColorStop(1,'#1d4ed8'); x.fillStyle=g; x.beginPath(); x.arc(GX,GY,GR,0,2*Math.PI); x.fill();
    [-60,-30,0,30,60].forEach(la=>{ x.strokeStyle=la===0?'rgba(255,255,255,.85)':'rgba(255,255,255,.35)'; x.lineWidth=la===0?1.6:1; x.beginPath(); let on=false; for(let lo=-180;lo<=180;lo+=5){ const q=gp(la,lo); if(q[2]>0){ on?x.lineTo(q[0],q[1]):x.moveTo(q[0],q[1]); on=true; } else on=false; } x.stroke(); });
    x.strokeStyle='#dc2626'; x.lineWidth=2.6; x.beginPath(); let on=false; for(let lo=-180;lo<=180;lo+=4){ const q=gp(lat,lo); if(q[2]>-0.02){ on?x.lineTo(q[0],q[1]):x.moveTo(q[0],q[1]); on=true; } else on=false; } x.stroke();
    const tp=[GX,GY-(GR+26)*Math.cos(E)], bt=[GX,GY+(GR+18)*Math.cos(E)]; x.strokeStyle='#0f172a'; x.lineWidth=2; x.beginPath(); x.moveTo(bt[0],bt[1]); x.lineTo(tp[0],tp[1]); x.stroke();
    x.strokeStyle='#ea580c'; x.lineWidth=2.2; x.beginPath(); x.ellipse(tp[0],tp[1]+6,16,5,0,0.15*Math.PI,0.95*Math.PI,true); x.stroke(); head(tp[0]-15,tp[1]+8.5,Math.PI*0.97,8,'#ea580c');
    txt('北極',tp[0]+20,tp[1]+4,'#0f172a',11.5,1,'left'); txt('自転の角速度',8,56,'#9a3412',11.5,0,'left'); txt('Ω＝7.29×10⁻⁵ rad/s',8,71,'#9a3412',11.5,0,'left');
    const P=gp(lat,-28); if(P[2]>0){ const dx=P[0]-GX, dy=P[1]-GY, l=Math.hypot(dx,dy)||1; arrow(P[0],P[1],P[0]+dx/l*24,P[1]+dy/l*24,'#facc15',2.5,8);
      x.fillStyle='#dc2626'; x.strokeStyle='#fff'; x.lineWidth=2; x.beginPath(); x.arc(P[0],P[1],5,0,2*Math.PI); x.fill(); x.stroke(); }
    halo(latName(lat),GX+GR*0.55,Math.min(GY+GR+8,Math.max(70,gp(lat,40)[1]-12)),'#b91c1c',12,1);
    // f のグラフ
    const gx0=22, gx1=238, gy0=330, A=42, sx=(p)=>gx0+(p+90)/180*(gx1-gx0), sy=(v)=>gy0-v/1.458e-4*A;
    x.fillStyle='#f8fafc'; rr(4,262,246,128,8); x.fill(); txt('f＝2Ω sinφ（コリオリパラメータ）',10,278,'#0f172a',12,0,'left','alphabetic',236);
    x.strokeStyle='#cbd5e1'; x.lineWidth=1; x.beginPath(); x.moveTo(gx0,gy0); x.lineTo(gx1,gy0); x.moveTo(sx(0),gy0-A-4); x.lineTo(sx(0),gy0+A+4); x.stroke();
    [-90,-45,0,45,90].forEach(p=>txt((p===0?'0°':(p>0?'北':'南')+Math.abs(p)+'°'),sx(p),gy0+A+12,'#64748b',9.5,0,'center'));
    txt('+1.46',sx(0)-3,gy0-A+3,'#64748b',9,0,'right'); txt('−1.46',sx(0)-3,gy0+A+3,'#64748b',9,0,'right'); txt('×10⁻⁴',gx1,gy0-A+3,'#64748b',9,0,'right');
    x.strokeStyle='#0891b2'; x.lineWidth=2.2; x.beginPath(); for(let p=-90;p<=90;p+=2){ const X=sx(p), Y=sy(fval(p)); p>-90?x.lineTo(X,Y):x.moveTo(X,Y); } x.stroke();
    x.fillStyle='#dc2626'; x.beginPath(); x.arc(sx(lat),sy(f),5.5,0,2*Math.PI); x.fill();
    // 式
    x.fillStyle='#ecfeff'; rr(4,396,246,118,8); x.fill();
    txt('f ＝ 2Ω sinφ ＝ 2 × 7.29×10⁻⁵ × sin'+(lat<0?'(−'+(-lat)+'°)':lat+'°'),12,418,'#0f172a',12.5,0,'left','alphabetic',230);
    txt('＝ '+sci(f,2)+' /s',12,446,'#0e7490',19,1,'left','alphabetic',230);
    txt('赤道で0、極で最大（1.46×10⁻⁴ /s）',12,468,'#334155',11.5,0,'left','alphabetic',230);
    const ws=+$('ws').value; txt('風速'+ws+' m/sの空気1 kgにはたらく力',12,488,'#334155',11.5,0,'left','alphabetic',230);
    txt('2Ωv sinφ ＝ '+sci(Math.abs(f*ws),2)+' N',12,506,'#7c3aed',12.5,0,'left','alphabetic',230);
  }
  function drawSys(k){ const c=k===0?LC:HC, cx=c[0], cy=c[1], y0=cy-116, f=fval(lat), hemi=lat>0?'北半球':lat<0?'南半球':'赤道';
    x.fillStyle=k===0?'#eff6ff':'#fff7ed'; rr(256,y0,378,230,10); x.fill();
    let t; if(lat===0) t=(k===0?'低気圧（赤道）：渦にならず、まっすぐ吹きこむ':'高気圧（赤道）：渦にならず、まっすぐ吹き出す');
    else { const ccw=(lat>0)===(k===0); t=(k===0?'低気圧':'高気圧')+'（'+hemi+'）：'+(ccw?'反時計回り':'時計回り')+'に'+(k===0?'吹きこむ':'吹き出す'); }
    txt(t,264,y0+19,k===0?'#1e3a8a':'#9a3412',14,1,'left','alphabetic',362);
    x.strokeStyle=k===0?'rgba(30,64,175,.35)':'rgba(194,65,12,.35)'; x.lineWidth=1.2; [32,63,94].forEach(r=>{ x.beginPath(); x.arc(cx,cy,r,0,2*Math.PI); x.stroke(); });
    const isob=k===0?['996','1000','1004']:['1024','1020','1016']; isob.forEach((s,i)=>txt(s,cx+[32,63,94][i]*0.71+2,cy-[32,63,94][i]*0.71-2,k===0?'#1e40af':'#c2410c',9.5,0,'left'));
    halo(k===0?'L':'H',cx,cy,k===0?'#1d4ed8':'#c2410c',26,1); halo(k===0?'低':'高',cx,cy+22,k===0?'#1d4ed8':'#c2410c',11,1);
    x.lineCap='round'; parts.forEach(p=>{ if(p.k!==k||p.tr.length<2) return; x.strokeStyle=k===0?'rgba(37,99,235,.55)':'rgba(234,88,12,.55)'; x.lineWidth=1.6; x.beginPath(); p.tr.forEach((q,i)=>{ const X=cx+q[0], Y=cy-q[1]; i?x.lineTo(X,Y):x.moveTo(X,Y); }); x.stroke(); }); x.lineCap='butt';
    if(k===0){ // 力のつり合い（地上の風）
      const f2=F0*Math.sin(lat*R), gx=GG, den=f2*f2+KF*KF, vx=gx*KF/den, vy=-f2*gx/den, vl=Math.hypot(vx,vy), S=44/GG, px=cx-62, py=cy;
      arrow(px,py,px+gx*S,py,'#475569',3,9); arrow(px,py,px+vx/vl*40,py-vy/vl*40,'#1d4ed8',4,11);
      const cx2=f2*vy, cy2=-f2*vx; arrow(px,py,px+cx2*S,py-cy2*S,'#7c3aed',3,9); arrow(px,py,px-KF*vx*S,py+KF*vy*S,'#16a34a',3,9);
      x.fillStyle='#111827'; x.beginPath(); x.arc(px,py,3.5,0,2*Math.PI); x.fill();
      [['━ 風（地上）','#1d4ed8'],['━ 気圧傾度力','#475569'],['━ コリオリの力','#7c3aed'],['━ 摩擦力','#16a34a']].forEach((q,i)=>txt(q[0],262,y0+170+i*15,q[1],11,1)); }
  }
  function drawM1(){ x.fillStyle='#fff'; x.fillRect(0,0,W,H); drawGlobe(); drawSys(0); drawSys(1); tabs(MODES,mode);
    const f=fval(lat), ws=+$('ws').value, low=lat===0?'まっすぐ吹きこむ':(lat>0?'反時計回りに吹きこむ':'時計回りに吹きこむ');
    upd('1|'+lat+'|'+ws,()=>{ setK('s1','緯度'); setK('s2','f＝2Ω sinφ'); setK('s3','コリオリの力（1kgあたり）'); setK('s4','低気圧のまわりの風');
    fit('s1',latName(lat)); fit('s2',sci(f,2)+' /s'); fit('s3',sci(Math.abs(f*ws),2)+' N'); fit('s4',low);
    setShare('【コリオリの力】'+latName(lat)+'のコリオリパラメータ f=2Ωsinφ='+sci(f,2)+'/s。低気圧のまわりでは風が'+low+'｜シミュラボ'); }); }

  // ---------------- ③ 大気の大循環
  const C3=[36,290], R3=170, HA=56, MX0=380, MX1=630, MY=(la)=>290-la*2.4;
  const CELLS=[[15,12,-1,'ハドレー循環'],[45,12,1,'フェレル循環'],[75,12,-1,'極循環']], COLS3=['#f97316','#16a34a','#0ea5e9'];
  const WN3=[[75,'極偏東風'],[45,'偏西風'],[15,'北東貿易風'],[-15,'南東貿易風'],[-45,'偏西風'],[-75,'極偏東風']];
  let phase=0, mparts=[];
  const cs=(la,h)=>[C3[0]+(R3+h)*Math.cos(la*R), C3[1]-(R3+h)*Math.sin(la*R)];
  const uvw=(la)=>[-Math.sin(6*Math.abs(la)*R), -0.45*Math.sin(6*la*R)];
  function newM(){ return {lx:Math.random(), la:-87+174*Math.random(), age:0, life:2+3*Math.random()}; }
  function initM(){ mparts=[]; for(let i=0;i<170;i++){ const p=newM(); p.age=Math.random()*p.life; mparts.push(p); } }
  function stepMap(dt){ phase+=dt*0.22; mparts.forEach(p=>{ const w=uvw(p.la); p.lx+=w[0]*0.06*dt; p.la+=w[1]*7*dt; if(p.lx<0) p.lx+=1; if(p.lx>1) p.lx-=1; p.age+=dt; if(p.age>p.life||Math.abs(p.la)>89) Object.assign(p,newM()); }); }
  function band(p){ const a=Math.abs(p), Nh=p>0;
    const w=a<5?'弱い風（熱帯収束帯）':a<28?(Nh?'北東貿易風':'南東貿易風'):a<=32?'弱い風（亜熱帯高圧帯）':a<58?(Nh?'偏西風（南西の風）':'偏西風（北西の風）'):a<=62?'偏西風と極偏東風の境':(Nh?'極偏東風（北東の風）':'極偏東風（南東の風）');
    const c=a===30?'ハドレー／フェレルの境':a===60?'フェレル／極循環の境':a<30?'ハドレー循環':a<60?'フェレル循環':'極循環';
    const b=a<15?'赤道低圧帯（熱帯収束帯）':a<45?'亜熱帯高圧帯（30°付近）':a<75?'亜寒帯低圧帯（60°付近）':'極高圧帯';
    return [w,c,b]; }
  let bg3=null;
  function staticM2(){ x.fillStyle='#fff'; x.fillRect(0,0,W,H);
    x.fillStyle='#e0f2fe'; x.beginPath(); x.arc(C3[0],C3[1],R3+HA,-Math.PI/2,Math.PI/2); x.lineTo(C3[0],C3[1]); x.fill();
    const g=x.createRadialGradient(C3[0],C3[1],20,C3[0],C3[1],R3); g.addColorStop(0,'#60a5fa'); g.addColorStop(1,'#1e40af'); x.fillStyle=g; x.beginPath(); x.arc(C3[0],C3[1],R3,-Math.PI/2,Math.PI/2); x.lineTo(C3[0],C3[1]); x.fill();
    [-60,-30,0,30,60].forEach(la=>{ const a=cs(la,0), b=cs(la,HA+4); x.strokeStyle='rgba(15,23,42,.25)'; x.lineWidth=1; x.setLineDash([3,3]); x.beginPath(); x.moveTo(a[0],a[1]); x.lineTo(b[0],b[1]); x.stroke(); x.setLineDash([]); });
    [1,-1].forEach(hs=>CELLS.forEach((c,ci)=>{ const pt=(t)=>cs(hs*(c[0]+c[1]*Math.cos(t)),28+19*Math.sin(t));
      x.strokeStyle=COLS3[ci]; x.lineWidth=2.2; x.beginPath(); for(let i=0;i<=48;i++){ const q=pt(i/48*2*Math.PI); i?x.lineTo(q[0],q[1]):x.moveTo(q[0],q[1]); } x.stroke();
      [Math.PI/2,3*Math.PI/2,0,Math.PI].forEach(t=>{ const q=pt(t), q2=pt(t+c[2]*0.2); head(q2[0],q2[1],Math.atan2(q2[1]-q[1],q2[0]-q[0]),8,COLS3[ci]); });
      const lq=cs(hs*c[0],-[58,52,40][ci]); txt(c[3],lq[0],lq[1]+4,'#fff',12.5,1,'center','middle'); }));
    [[0,['赤道低圧帯','（上昇気流）']],[30,['北緯30° 亜熱帯','高圧帯（下降）']],[60,['北緯60° 亜寒帯','低圧帯（上昇）']],[-30,['南緯30° 亜熱帯','高圧帯（下降）']],[-60,['南緯60° 亜寒帯','低圧帯（上昇）']]].forEach(q=>{
      const p=cs(q[0],HA+8); q[1].forEach((s,i)=>txt(s,p[0]+3,p[1]-6+i*13+(q[0]<0?8:0),'#334155',10.5,i===0,'left','alphabetic',MX0-p[0]-8)); });
    txt('大気の大循環（地球の断面）',8,56,'#0f172a',13,1,'left','alphabetic',260); txt('※大気の厚さは誇張',42,294,'#e0f2fe',10.5,0,'left');
    const MW=MX1-MX0; [[90,60,'#e0f2fe'],[60,30,'#dcfce7'],[30,0,'#ffedd5'],[0,-30,'#ffedd5'],[-30,-60,'#dcfce7'],[-60,-90,'#e0f2fe']].forEach(b=>{ x.fillStyle=b[2]; x.fillRect(MX0,MY(b[0]),MW,MY(b[1])-MY(b[0])); });
    x.strokeStyle='#94a3b8'; x.lineWidth=1; x.strokeRect(MX0,MY(90),MW,MY(-90)-MY(90));
    [60,30,0,-30,-60].forEach(la=>{ x.strokeStyle=la===0?'#64748b':'#cbd5e1'; x.beginPath(); x.moveTo(MX0,MY(la)); x.lineTo(MX1,MY(la)); x.stroke(); txt(la===0?'赤道':(la>0?'北':'南')+Math.abs(la)+'°',MX0+3,MY(la)-3,'#475569',10,1); });
    WN3.forEach(q=>{ const w=uvw(q[0]), l=Math.hypot(w[0],w[1]), y=MY(q[0])+8; [MX0+44,MX0+MW/2,MX1-40].forEach(cx=>arrow(cx-w[0]/l*15,y+w[1]/l*15,cx+w[0]/l*15,y-w[1]/l*15,'#0f172a',2.6,9)); });
    txt('地上の風（年平均のモデル）',MX0,56,'#0f172a',13,1,'left','alphabetic',MW); txt('上が北・右が東',MX0,72,'#64748b',10.5,0,'left'); }
  function drawM2(){ const MW=MX1-MX0;
    if(!bg3){ bg3=document.createElement('canvas'); bg3.width=W*dpr; bg3.height=H*dpr; const sv=x; x=bg3.getContext('2d'); x.setTransform(dpr,0,0,dpr,0,0); staticM2(); x=sv; }
    x.drawImage(bg3,0,0,W,H);
    const L2=cs(lat,HA+6); x.strokeStyle='rgba(220,38,38,.85)'; x.lineWidth=2; x.beginPath(); x.moveTo(C3[0],C3[1]); x.lineTo(L2[0],L2[1]); x.stroke();
    x.fillStyle='#fff'; x.lineWidth=1.5; [1,-1].forEach(hs=>CELLS.forEach((c,ci)=>{ x.strokeStyle=COLS3[ci]; for(let k=0;k<4;k++){ const t=c[2]*(phase*2*Math.PI)+k*Math.PI/2, q=cs(hs*(c[0]+c[1]*Math.cos(t)),28+19*Math.sin(t)); x.beginPath(); x.arc(q[0],q[1],3,0,2*Math.PI); x.fill(); x.stroke(); } }));
    x.save(); x.beginPath(); x.rect(MX0,MY(90),MW,MY(-90)-MY(90)); x.clip(); x.lineCap='round'; x.lineWidth=1.4; x.strokeStyle='rgba(30,41,59,.32)'; x.beginPath(); mparts.forEach(p=>{ const w=uvw(p.la), X=MX0+p.lx*MW, Y=MY(p.la); x.moveTo(X-w[0]*9,Y+w[1]*7); x.lineTo(X,Y); }); x.stroke(); x.lineCap='butt'; x.restore();
    WN3.forEach(q=>halo(q[1],MX0+MW/2,MY(q[0])-14,'#0f172a',13,1,'center','rgba(255,255,255,.95)'));
    x.strokeStyle='#dc2626'; x.lineWidth=2.4; x.beginPath(); x.moveTo(MX0,MY(lat)); x.lineTo(MX1,MY(lat)); x.stroke();
    tabs(MODES,mode);
    upd('2|'+lat,()=>{ const b=band(lat); setK('s1','緯度'); setK('s2','地上の風'); setK('s3','循環'); setK('s4','近くの気圧帯');
    fit('s1',latName(lat)); fit('s2',b[0]); fit('s3',b[1]); fit('s4',b[2]);
    setShare('【大気の大循環】'+latName(lat)+'は'+b[1]+'の範囲で、地上の風は'+b[0]+'｜シミュラボ'); }); }

  function draw(){ [mode===0?drawM0:mode===1?drawM1:drawM2][0](); }
  function setMode(m){ mode=m; $('mode').value=MV[m]; ['dir','rpm','vb'].forEach(id=>showField(id,m===0)); showField('lat',m>0); showField('ws',m===1); showBtn('throw',m===0); showBtn('clr',m===0);
    if(m===1&&!parts.length) initParts(); if(m===2&&!mparts.length) initM(); draw(); }
  function setLat(v){ v=clamp(Math.round(v),-90,90); if(v===lat) return; lat=v; $('lat').value=v; latLabel(); if(mode===1) for(let i=0;i<90;i++) stepParts(1/60); draw(); }
  function hit(px,py,first){ if(mode===0){ if(first) { newThrow(); } return; }
    if(mode===1){ if(px<252){ if(py>262&&py<392) setLat((px-22)/216*180-90); else if(py<262){ setLat(Math.asin(clamp((GY-py)/(GR*Math.cos(E)),-1,1))/R); } } return; }
    if(px>=MX0) setLat((290-py)/2.4); else setLat(Math.atan2(C3[1]-py,px-C3[0])/R); }
  cv.addEventListener('pointerdown',e=>{ const p=cpos(cv,e), px=p[0]/dpr, py=p[1]/dpr; if(py<40){ const i=Math.floor((px-6)/((W-12)/3)); if(i>=0&&i<3) setMode(i); return; }
    drag=true; if(cv.setPointerCapture) try{ cv.setPointerCapture(e.pointerId); }catch(_){} hit(px,py,true); });
  cv.addEventListener('pointermove',e=>{ if(!drag) return; const p=cpos(cv,e); hit(p[0]/dpr,p[1]/dpr,false); });
  window.addEventListener('pointerup',()=>{ drag=false; });
  $('mode').addEventListener('change',()=>setMode(Math.max(0,MV.indexOf($('mode').value))));
  ['dir','rpm','vb'].forEach(id=>$(id).addEventListener('input',()=>{ instantThrow(); draw(); }));
  $('lat').addEventListener('input',()=>{ const v=+$('lat').value; lat=v-1000; setLat(v); });
  $('ws').addEventListener('input',draw);
  $('throw').addEventListener('click',()=>{ if(mode!==0) setMode(0); newThrow(); });
  $('clr').addEventListener('click',()=>{ throws=[]; draw(); });
  latLabel(); instantThrow(); setMode(mode);
  function loop(ts){ const dt=Math.min(0.05,(ts-(last||ts))/1000); last=ts;
    if(mode===0){ const sd=dt*SLOW; ang=(ang+om()*sd)%(2*Math.PI*1000); throws.forEach(t=>stepThrow(t,sd)); } else if(mode===1) stepParts(dt); else stepMap(dt);
    draw(); requestAnimationFrame(loop); }
  requestAnimationFrame(loop);
'''

sim(slug="coriolis-henseifu", cat="rika", emoji="🌀", score=80,
    title="コリオリの力と大気の大循環シミュレーター（偏西風・貿易風）",
    title_tag="コリオリの力のシミュレーター｜回る円盤・f＝2Ωsinφ・偏西風と大気の大循環（高校地学）",
    meta_desc="コリオリの力（転向力）を、回る円盤の上で玉を投げる実験で確かめる無料シミュレーター。緯度を変えるとコリオリパラメータ f＝2Ωsinφ と低気圧・高気圧のまわりの風の向き（北半球と南半球の違い）が変わり、ハドレー循環・フェレル循環・極循環と貿易風・偏西風・極偏東風も表示します。地学基礎・地学の授業に。",
    og_title="コリオリの力と大気の大循環シミュレーター（偏西風・貿易風）",
    og_desc="回る円盤で玉が右へ曲がって見えるわけから、f＝2Ωsinφ、低気圧の渦の向き、ハドレー循環・偏西風までを1つの画面で確かめる高校地学の教材です。",
    card_desc="回る円盤で玉が右へ曲がる理由から、f＝2Ωsinφ、低気圧の渦の向き、偏西風・貿易風の大循環まで。",
    lead="回る円盤の中心から玉を投げると、外から見るとまっすぐなのに、円盤の上から見ると右へ曲がります。この見かけの力がコリオリの力です。緯度を変えて、コリオリパラメータ f＝2Ωsinφ、低気圧・高気圧のまわりの風、大気の大循環と貿易風・偏西風の向きを確かめられます。",
    model="地学基礎 大気と海水の運動／地学 大気の運動と気象",
    level="高校（地学基礎・地学）",
    unit="高等学校 地学基礎（1）ア（ｳ）㋑ 大気と海水の運動／地学（3）ア（ｱ）㋑ 大気の運動と気象",
    canvas=canvas(640, 520, light=True),
    controls=select("mode", "見るもの", [("disk", "① 回る円盤"), ("earth", "② 緯度と低気圧・高気圧"), ("gc", "③ 大気の大循環")])
           + select("dir", "回転の向き", [("ccw", "反時計回り（北半球）"), ("cw", "時計回り（南半球）")])
           + slider("rpm", "円盤の回転", 0, 20, 10, 1, "1分間に{v}回転")
           + slider("vb", "玉の速さ", 0.5, 3, 1, 0.1, "秒速{v} m")
           + slider("lat", "緯度", -90, 90, 35, 1)
           + slider("ws", "風速", 1, 50, 10, 1, "{v} m/s"),
    buttons=btn("throw", "▶ 玉を投げる", True) + btn("clr", "軌跡を消す"),
    stats=stats([("s1", "円盤の1周", False), ("s2", "ふちに届くまで", False), ("s3", "曲がって見える角度", True), ("s4", "曲がる向き", False)]),
    legend="図の上のタブ（または「見るもの」）で3つの図を切りかえます。①左は外から見た円盤、右は円盤といっしょに回る人から見た円盤で、赤い線が玉の通り道、紫の矢印がコリオリの力です。円盤をタップしても玉を投げられます。②左は地球と緯度（赤い線）、f＝2Ωsinφ のグラフ、右は低気圧（L）と高気圧（H）のまわりの空気の動き（線は空気の通った跡）。地球やグラフをなぞると緯度が変わります。③左は地球の断面の3つの循環、右は地上の風の向き（年平均のモデル）。どちらもなぞると緯度が変わります。②③の空気の動きと速さは向きを示すためのモデルで、実際の値ではありません。",
    article='''
<h2>このシミュレーションでわかること</h2>
''' + P("<b>コリオリの力（転向力）は、自転している地球の上で運動する物体にはたらいて見える見かけの力で、北半球では進む向きの右向き、南半球では左向きにはたらきます。</b>大きさは 2mΩv sinφ（m：質量、Ω：地球の自転の角速度 7.29×10⁻⁵ rad/s、v：速さ、φ：緯度）で、赤道で0、極で最大です。") + '''
<p>このシミュレーターでは、①回る円盤の上で玉を投げる実験でコリオリの力の正体（回転する座標から見た見かけの動き）を確かめ、②緯度によるコリオリパラメータ f＝2Ωsinφ の違いと、低気圧・高気圧のまわりの風の吹き方（北半球と南半球で反対）を見て、③ハドレー循環・フェレル循環・極循環と、貿易風・偏西風・極偏東風の向きを地球の断面と地図で確かめます。</p>
''' + T([[NW("地学基礎"), "（1）地球のすがた ア（ｳ）大気と海洋 ㋑ 大気と海水の運動", "大気と海水の運動に関する資料に基づいて、大気と海洋の大循環について理解するとともに、地球規模で熱が輸送されていることを見いだして理解すること"],
          [NW("地学"), "（3）地球の大気と海洋 ア（ｱ）大気の構造と運動 ㋑ 大気の運動と気象", "大循環と対流による現象及び日本や世界の気象の特徴を理解すること（「大循環」による現象では、偏西風波動と地上の高気圧や低気圧との関係も扱う）"]],
         ["科目", "単元", "学習指導要領（平成30年告示）の内容"]) + '''
<p>高等学校学習指導要領解説 理科編は、地学基礎（p.155）で年平均の風の分布などの資料から偏西風・貿易風・ハドレー循環などを理解させること、地学（p.172）で地衡風が気圧傾度力とコリオリの力のつり合ったときの風であること、中緯度で偏西風が吹いていることを取り上げることを示しています。</p>

<h2>授業での使い方</h2>
<p><b>導入（①回る円盤）</b>：円盤を反時計回りに回し、中心から「受ける人」に向けて玉を投げます。外から見ると玉はまっすぐ進むのに、円盤の上の人には右へそれて見えることを確かめます。回転を時計回りにすると左へそれることから、北半球と南半球の違いにつなげます。</p>
<p><b>展開（②緯度と風）</b>：緯度のスライダーを北緯90°から0°、南緯90°へ動かし、f＝2Ωsinφ のグラフと、低気圧のまわりの風の向きの変化を観察します。赤道では渦ができず、南半球では向きが反対になることを確かめます。左の低気圧の図の矢印で、地上の風が気圧傾度力・コリオリの力・摩擦力のつり合いで等圧線を斜めに横切ることも説明できます。</p>
<p><b>まとめ（③大気の大循環）</b>：緯度ごとの循環と地上の風の名前を表にまとめます。貿易風が「北東」から、偏西風が「南西」から吹く理由を、南北の流れがコリオリの力で曲げられることから説明させます。</p>
<p>生徒への問いの例です。</p>
<ul>
<li>回る円盤で、玉の速さを2倍にすると、曲がって見える角度はどうなるでしょう。（ふちに届くまでの時間が半分になるので、角度も半分になる）</li>
<li>北緯30°と北緯90°では、同じ風速の風にはたらくコリオリの力は何倍ちがうでしょう。（sin30°＝0.5、sin90°＝1 なので2倍）</li>
<li>ハドレー循環で赤道へ向かう地上の風は、なぜ「北東貿易風」になるのでしょう。（北から南へ向かう空気が、コリオリの力で進む向きの右＝西へ曲げられるから）</li>
</ul>

<h2>しくみ・解説</h2>
<h3>用語の意味</h3>
<ul>
<li><b>コリオリの力（転向力）</b>とは、回転する座標系（地球の上）から運動を見たときに現れる見かけの力で、運動の向きに垂直にはたらき、物体の速さは変えずに向きだけを変えます。</li>
<li><b>コリオリパラメータ</b>とは、f＝2Ωsinφ で表される量で、緯度φでの地面の回転の強さを表します（単位は /s）。</li>
<li><b>気圧傾度力</b>とは、気圧の高い方から低い方へ空気を押す力で、等圧線に垂直にはたらきます。</li>
<li><b>地衡風</b>とは、上空で気圧傾度力とコリオリの力がつり合って、等圧線に平行に吹く風です（北半球では低圧側を左に見て吹きます）。</li>
<li><b>大気の大循環</b>とは、緯度によって太陽放射の受熱量が違うことで起こる、地球規模の大気の流れで、低緯度から高緯度へ熱を運んでいます。</li>
</ul>
<h3>コリオリの力の式</h3>
''' + N("コリオリの力 C ＝ 2mΩv sinφ ＝ m f v　（北半球では進む向きの右向き、南半球では左向き）<br>コリオリパラメータ f ＝ 2Ω sinφ<br>地球の自転の角速度 Ω ＝ 2π ÷ 86,164 s（1恒星日）≒ 7.29×10⁻⁵ rad/s") + '''
<p>sinφ がつくのは、その場所の地面が鉛直な軸のまわりに回る速さが Ω sinφ になるからです。北極では地面は円盤と同じように Ω で回り、赤道では鉛直な軸のまわりには回っていない（地軸と地面が平行）ので、水平に動く物体にはたらくコリオリの力は0になります。南半球では sinφ が負になり、向きが反対になります。</p>
<h3>緯度ごとの早見表</h3>
''' + F_TABLE + '''
<p><b>計算例1</b>：北緯35°で風速10 m/sの風が吹いているとき、空気1 kgにはたらくコリオリの力の大きさは何Nですか。<br>答え：f＝2×7.29×10⁻⁵×sin35°＝2×7.29×10⁻⁵×0.574≒8.36×10⁻⁵ /s。C＝m f v＝1×8.36×10⁻⁵×10≒<b>8.4×10⁻⁴ N</b></p>
<p><b>計算例2（地衡風）</b>：北緯35°で、400 km 離れた等圧線の間で気圧が4 hPa（400 Pa）違うとき、地衡風の速さは何 m/s ですか（空気の密度 1.2 kg/m³、摩擦は考えない）。<br>答え：気圧傾度力（1 kgあたり）＝(1/ρ)×(Δp/Δn)＝(1/1.2)×(400/400,000)≒8.3×10⁻⁴ N。これがコリオリの力 f v とつり合うので、v＝(Δp/Δn)÷(ρ f)＝1.0×10⁻³÷(1.2×8.36×10⁻⁵)≒<b>10 m/s</b></p>
<p><b>計算例3（回る円盤）</b>：半径1 mの円盤が1分間に10回転しています。中心から秒速1 mで玉を転がすと、円盤の上から見て何度それて見えますか。<br>答え：ふちに届くまで 1 m÷1 m/s＝1秒。その間に円盤は 360°×10÷60＝60° 回るので、<b>60°</b>（反時計回りなら右へ）。</p>
<h3>低気圧・高気圧のまわりの風</h3>
''' + T([["北半球", "反時計回りに吹きこむ", "時計回りに吹き出す"], ["南半球", "時計回りに吹きこむ", "反時計回りに吹き出す"], ["赤道付近", "渦になりにくい（台風は緯度5°以内ではほとんど発生しない）", "—"]],
        ["", "低気圧", "高気圧"]) + '''
<p>地上の風は、気圧傾度力・コリオリの力・摩擦力の3つがつり合って吹くため、等圧線を斜めに横切って低気圧側へ向かいます（横切る角度は海上で小さく、陸上で大きくなります）。上空では摩擦がほとんどないので、等圧線に平行な地衡風になります。</p>
<h3>大気の大循環と地上の風</h3>
''' + T([[NW("0〜30°"), "ハドレー循環（赤道で上昇し、緯度30°付近で下降）", "貿易風（北半球は北東の風、南半球は南東の風）", "赤道低圧帯（熱帯収束帯）／亜熱帯高圧帯"],
          [NW("30〜60°"), "フェレル循環（緯度30°付近で下降し、60°付近で上昇）", "偏西風（北半球は南西の風、南半球は北西の風）", "亜熱帯高圧帯／亜寒帯低圧帯"],
          [NW("60〜90°"), "極循環（緯度60°付近で上昇し、極で下降）", "極偏東風（北半球は北東の風、南半球は南東の風）", "亜寒帯低圧帯／極高圧帯"]],
         ["緯度", "循環", "地上の風", "気圧帯"]) + '''
<p>赤道付近であたためられた空気は上昇し、上空を高緯度へ向かって緯度30°付近で下降します（ハドレー循環）。下降した空気が地上を赤道へもどるとき、コリオリの力で西へ曲げられて貿易風になります。緯度30°付近から高緯度へ向かう地上の空気は東へ曲げられて偏西風になります。中緯度の上空には、南北の温度差によって強い偏西風（ジェット気流）が吹き、南北に蛇行しながら（偏西風波動）低緯度と高緯度の間で熱を運んでいます。日本付近の天気が西から東へ変わるのは、この偏西風のためです。</p>
<h3>このシミュレーションで単純化していること</h3>
<ul>
<li>①の円盤は半径1 mとし、玉と円盤の摩擦は考えていません。外から見て等速直線運動する玉を、円盤とともに回る座標に直して描いています（遠心力も含めた見かけの動きになります）。</li>
<li>②の低気圧・高気圧の空気の動きは、気圧傾度力・コリオリの力（f を緯度に合わせて sinφ 倍）・摩擦力を時間・長さの単位をそろえずに計算したモデルで、向きと曲がり方の違いを示すためのものです。実際の風速・大きさではありません。</li>
<li>③の循環と地上の風は年平均の理想化したモデルです。実際には、気圧帯は季節によって南北に動き、海と陸の分布によって季節風なども生じます。フェレル循環は、ハドレー循環と極循環にはさまれて生じる見かけの循環です。</li>
<li>図の大気の厚さは誇張しています（対流圏の厚さは約11 km で、地球の半径約6,400 km に比べてとても薄い）。</li>
</ul>

<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「高等学校学習指導要領（平成30年告示）解説 理科編 理数編」地学基礎 p.155、地学 p.172（''' + A(MEXT_KOU) + '''）</li>
<li>国立天文台 編『理科年表』（丸善出版）…地球の自転の角速度・地球の大きさ</li>
<li>高等学校「地学基礎」「地学」の教科書（大気の大循環・コリオリの力・地衡風の単元）</li>
</ul>
''',
    faqs=[("コリオリの力とは何ですか？", "自転している地球の上で運動する物体にはたらいて見える見かけの力で、転向力ともいいます。北半球では進む向きの右向き、南半球では左向きにはたらき、大きさは 2mΩv sinφ です（Ω＝7.29×10⁻⁵ rad/s、φ＝緯度）。"),
          ("コリオリパラメータ f＝2Ωsinφ は赤道と極でいくつですか？", "赤道（φ＝0°）では sin0°＝0 なので f＝0、極（φ＝90°）では最大の f＝2×7.29×10⁻⁵＝1.46×10⁻⁴ /s です。北緯35°では約8.36×10⁻⁵ /s です。"),
          ("北半球の低気圧のまわりで、風が反時計回りに吹きこむのはなぜですか？", "空気は気圧傾度力で低気圧の中心へ向かいますが、北半球ではコリオリの力で進む向きの右へ曲げられるため、中心のまわりを反時計回りに回りながら吹きこみます。南半球では左へ曲げられるので時計回りになります。"),
          ("偏西風と貿易風は、なぜ吹く向きが反対なのですか？", "どちらも南北に流れる地上の空気がコリオリの力で曲げられたものです。ハドレー循環で赤道へ向かう空気は西へ曲げられて東寄りの貿易風に、緯度30°付近から高緯度へ向かう空気は東へ曲げられて西寄りの偏西風になります。"),
          ("お風呂の栓をぬいたときの渦の向きは、コリオリの力で決まりますか？", "ほとんど決まりません。浴槽のような小さく短い時間の流れでは、コリオリの力は他の力（水の最初の動きや浴槽の形の影響）に比べてとても小さいためです。コリオリの力が効くのは、低気圧や大気の大循環のような数百km以上・数時間以上の大きな運動です。"),
          ("地衡風とは何ですか？", "上空で、気圧傾度力とコリオリの力がつり合って等圧線に平行に吹く風です。北半球では低圧側を左に見て吹きます。地上では摩擦力がはたらくので、風は等圧線を斜めに横切って低圧側へ吹きこみます。")],
    rel=[("kiatsu-jet", "🎢", "気圧ジェットコースター指数"), ("zensen-tenki", "🌦️", "前線と天気の変化シミュレーター"),
         ("taiyou-ugoki", "🌞", "太陽の1日の動きと季節"), ("eratosthenes", "🌍", "エラトステネスの方法で地球の大きさを測る"), ("gravity", "🌌", "重力シミュレーター")],
    js=JS1.replace("%%UI%%", UI_COMMON))


# ============================================================ 2 エラトステネスの方法
JS2 = r'''
  const cv=$('cv'); const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const x=cv.getContext('2d'); x.setTransform(dpr,0,0,dpr,0,0);
%%UI%%
  const R=Math.PI/180, PAIRS=%%PAIRS%%, REAL=40008, MV=['erato','japan'], MODES=['① エラトステネスの測定','② 日本の2都市で測る'];
  const hm=MV.indexOf((location.hash||'').slice(1));
  let mode=hm>=0?hm:Math.max(0,MV.indexOf($('mode').value)), drag=false;
  if(hm>=0) $('mode').value=MV[hm];
  const CX=58, CY=332, ER=250, PX0=352, PX1=632;
  const P=(a,r)=>[CX+(r||ER)*Math.cos(a*R), CY-(r||ER)*Math.sin(a*R)];
  const fx=(v,d)=>v.toFixed(d);
  function cur(){ if(mode===0){ const th=+$('th').value, d=+$('dk').value; return {n1:'アレクサンドリア', n2:'シエネ', a1:th, a2:0, dphi:th, d:d, eq:-23.4, dlab:'2地点の距離'}; }
    const q=PAIRS[+$('pair').value], ns=$('dist').value==='ns'; return {n1:q[0], n2:q[3], a1:q[1], a2:q[4], dphi:q[1]-q[4], d:ns?q[6]:q[7], eq:0, q:q, ns:ns, dlab:ns?'南北の距離':'2地点間の距離'}; }
  const dstr=(d)=>mode===0?num(d):d.toLocaleString('ja-JP',{minimumFractionDigits:1,maximumFractionDigits:1});
  function rod(a,len,col,name,up){ const b=P(a), t=P(a,ER+len), sh=len*Math.tan(Math.abs(a)*R);
    // 影（地面に沿って、太陽と反対側＝極の側）
    if(Math.abs(a)>0.05){ const tx=-Math.sin(a*R), ty=-Math.cos(a*R), L=Math.min(sh,70); x.strokeStyle='rgba(15,23,42,.8)'; x.lineWidth=4; x.lineCap='round'; x.beginPath(); x.moveTo(b[0],b[1]); x.lineTo(b[0]+tx*L,b[1]+ty*L); x.stroke(); x.lineCap='butt';
      x.strokeStyle='rgba(234,179,8,.95)'; x.lineWidth=1.6; x.beginPath(); x.moveTo(PX0-6,t[1]); x.lineTo(b[0]+tx*L,b[1]+ty*L); x.stroke(); }
    else { x.strokeStyle='rgba(234,179,8,.95)'; x.lineWidth=1.6; x.beginPath(); x.moveTo(PX0-6,b[1]); x.lineTo(b[0],b[1]); x.stroke(); }
    x.strokeStyle=col; x.lineWidth=3.2; x.beginPath(); x.moveTo(b[0],b[1]); x.lineTo(t[0],t[1]); x.stroke();
    x.fillStyle=col; x.beginPath(); x.arc(b[0],b[1],3.6,0,2*Math.PI); x.fill();
    halo(name,t[0]+6,t[1]+(up?-14:16),col,13,1,'right','rgba(255,253,245,.95)'); }
  function zoom(y0,h,name,z,col,well){ x.fillStyle='#f8fafc'; rr(PX0,y0,PX1-PX0,h,10); x.fill(); x.strokeStyle='#e2e8f0'; x.lineWidth=1; x.stroke();
    x.save(); rr(PX0,y0,PX1-PX0,h,10); x.clip();
    const gy=y0+h-16, rx=566, Hr=h-62, sh=Hr*Math.tan(z*R), d=[-Math.sin(z*R),Math.cos(z*R)];
    x.fillStyle='#d6d3d1'; x.fillRect(PX0+8,gy,PX1-PX0-16,7); x.strokeStyle='#78716c'; x.lineWidth=1.5; x.beginPath(); x.moveTo(PX0+8,gy); x.lineTo(PX1-8,gy); x.stroke();
    if(well){ x.fillStyle='#1e3a8a'; x.fillRect(470,gy-2,18,9); x.strokeStyle='#57534e'; x.lineWidth=2; x.strokeRect(468,gy-12,22,12); }
    x.strokeStyle='rgba(234,179,8,.9)'; x.lineWidth=1.5; [-1,1,2].forEach(k=>{ const ex=rx+k*26, ey=gy, L=(gy-(y0+30))/Math.cos(z*R); x.beginPath(); x.moveTo(ex-d[0]*L,ey-d[1]*L); x.lineTo(ex,ey); x.stroke(); head(ex,ey,Math.atan2(d[1],d[0]),7,'rgba(234,179,8,.95)'); });
    if(well){ const L=(gy-(y0+30)); x.beginPath(); x.moveTo(479,gy-L); x.lineTo(479,gy+4); x.stroke(); }
    { const L=(gy-Hr-(y0+30))/Math.cos(z*R)+4; x.strokeStyle='#ca8a04'; x.lineWidth=1.8; x.beginPath(); x.moveTo(rx-d[0]*L,gy-Hr-d[1]*L); x.lineTo(rx-sh,gy); x.stroke(); }
    if(sh>0.5){ x.strokeStyle='#0f172a'; x.lineWidth=5; x.lineCap='round'; x.beginPath(); x.moveTo(rx,gy); x.lineTo(rx-sh,gy); x.stroke(); x.lineCap='butt'; }
    x.strokeStyle=col; x.lineWidth=4; x.beginPath(); x.moveTo(rx,gy); x.lineTo(rx,gy-Hr); x.stroke();
    if(z>0.3){ x.strokeStyle='#dc2626'; x.lineWidth=2; x.beginPath(); x.arc(rx,gy-Hr,22,-Math.PI/2,-Math.PI/2+z*R); x.stroke(); x.setLineDash([3,3]); x.strokeStyle='rgba(220,38,38,.6)'; x.beginPath(); x.moveTo(rx,gy-Hr); x.lineTo(rx,gy-Hr-26); x.stroke(); x.setLineDash([]);
      halo(fx(z,z<10?1:2)+'°',rx+16+12*Math.sin(z*R/2),gy-Hr-30,'#b91c1c',12.5,1,'left'); }
    x.restore();
    txt(name,PX0+10,y0+20,col,14,1,'left','alphabetic',190);
    if(z>0.3){ txt('棒 1 m → 影 '+fx(100*Math.tan(z*R),1)+' cm',PX0+10,y0+40,'#0f172a',12.5,0,'left','alphabetic',150); txt('tan θ ＝ 影 ÷ 棒 ＝ '+fx(Math.tan(z*R),3),PX0+10,y0+57,'#334155',11.5,0,'left','alphabetic',150);
      txt('θ ＝ '+fx(z,z<10?1:2)+'°（太陽の高度 '+fx(90-z,1)+'°）',PX0+10,y0+74,'#b91c1c',11.5,1,'left','alphabetic',150); }
    else { txt('太陽が真上：影ができない',PX0+10,y0+40,'#0f172a',12.5,0,'left','alphabetic',160); txt(well?'井戸の底まで光が届く':'θ ＝ 0°',PX0+10,y0+57,'#334155',11.5,0,'left','alphabetic',160); } }
  function draw(){ const c=cur(), Lc=c.d*360/c.dphi, err=(Lc/REAL-1)*100, len=mode===0?30:16;
    x.fillStyle='#fffdf5'; x.fillRect(0,0,W,H);
    // 光線（平行）
    for(let y=92;y<=H;y+=24){ const dy=y-CY; if(Math.abs(dy)>=ER) continue; const sx=CX+Math.sqrt(ER*ER-dy*dy); x.strokeStyle='rgba(250,204,21,.45)'; x.lineWidth=1.2; x.beginPath(); x.moveTo(PX0-6,y); x.lineTo(sx,y); x.stroke(); head(sx,y,Math.PI,6,'rgba(234,179,8,.55)'); }
    txt('← 太陽の光（平行な光線）',PX0-8,90,'#a16207',11.5,1,'right');
    // 地球
    const g=x.createRadialGradient(CX+60,CY-60,30,CX,CY,ER); g.addColorStop(0,'#bfdbfe'); g.addColorStop(1,'#60a5fa'); x.fillStyle=g; x.beginPath(); x.arc(CX,CY,ER,0,2*Math.PI); x.fill(); x.strokeStyle='#1d4ed8'; x.lineWidth=2; x.stroke();
    // 赤道・地軸
    x.setLineDash([6,4]); x.strokeStyle='rgba(30,58,138,.55)'; x.lineWidth=1.4; let q=P(c.eq); x.beginPath(); x.moveTo(CX,CY); x.lineTo(q[0],q[1]); x.stroke(); q=P(c.eq+90,ER+16); x.beginPath(); x.moveTo(CX,CY); x.lineTo(q[0],q[1]); x.stroke(); x.setLineDash([]);
    q=P(c.eq,ER-46); halo('赤道',q[0],q[1]+(mode===0?14:12),'#1e3a8a',11.5,1,'center','rgba(219,234,254,.9)'); q=P(c.eq+90,ER-16); halo('北極',q[0]+20,q[1],'#1e3a8a',11.5,1,'center','rgba(219,234,254,.9)');
    // 中心から2地点へ
    x.setLineDash([4,4]); x.strokeStyle='rgba(15,23,42,.6)'; x.lineWidth=1.3; [c.a1,c.a2].forEach(a=>{ const t=P(a,ER+len); x.beginPath(); x.moveTo(CX,CY); x.lineTo(t[0],t[1]); x.stroke(); }); x.setLineDash([]);
    if(mode===1){ x.setLineDash([2,4]); x.strokeStyle='rgba(15,23,42,.35)'; x.beginPath(); x.moveTo(CX,CY); x.lineTo(CX+ER,CY); x.stroke(); x.setLineDash([]); }
    // 中心角
    x.fillStyle='rgba(249,115,22,.35)'; x.beginPath(); x.moveTo(CX,CY); x.arc(CX,CY,78,-c.a1*R,-c.a2*R); x.closePath(); x.fill(); x.strokeStyle='#ea580c'; x.lineWidth=2; x.beginPath(); x.arc(CX,CY,78,-c.a1*R,-c.a2*R); x.stroke();
    const am=(c.a1+c.a2)/2, lp=P(am,78); x.strokeStyle='#ea580c'; x.lineWidth=1.2; x.beginPath(); x.moveTo(lp[0],lp[1]); x.lineTo(lp[0]+34,lp[1]+30); x.stroke();
    halo((mode===0?'θ ＝ ':'Δφ ＝ ')+fx(c.dphi,mode===0?1:3)+'°',lp[0]+36,lp[1]+38,'#c2410c',14,1,'left','rgba(219,234,254,.92)');
    // 2地点間の弧
    x.strokeStyle='#dc2626'; x.lineWidth=5; x.beginPath(); x.arc(CX,CY,ER,-c.a1*R,-c.a2*R); x.stroke();
    const dp=P(am,ER-30); halo(dstr(c.d)+' km',dp[0]-6,dp[1]+(mode===0?0:2),'#b91c1c',14,1,'right','rgba(219,234,254,.92)');
    rod(c.a1,len,'#dc2626',c.n1,true); rod(c.a2,len,'#2563eb',c.n2,false);
    // 錯角の印（地点1）
    if(c.a1>0.5&&mode===0){ const t=P(c.a1,ER+len); x.strokeStyle='#dc2626'; x.lineWidth=1.6; x.beginPath(); x.arc(t[0],t[1],14,-c.a1*R,0); x.stroke(); }
    txt(mode===0?'地球の断面（夏至の日の正午）':'地球の断面（春分・秋分の日の正午）',8,58,'#0f172a',14,1,'left','alphabetic',330);
    txt('角度は実際の大きさ・棒の長さは誇張',8,75,'#64748b',11,0,'left','alphabetic',330);
    // 拡大図
    zoom(46,142,c.n1+'（拡大）',mode===0?c.a1:c.a1,'#dc2626',false); zoom(194,142,c.n2+'（拡大）',mode===0?0:c.a2,'#2563eb',mode===0);
    // 式
    x.fillStyle='#ecfeff'; rr(PX0,342,PX1-PX0,172,10); x.fill(); x.strokeStyle='#a5f3fc'; x.lineWidth=1; x.stroke();
    txt('360° : '+(mode===0?'θ':'Δφ')+' ＝ 地球一周 : 距離',PX0+12,364,'#0f172a',13,1,'left','alphabetic',256);
    txt('地球一周 ＝ '+dstr(c.d)+' km × 360° ÷ '+fx(c.dphi,mode===0?1:3)+'°',PX0+12,388,'#334155',13,0,'left','alphabetic',256);
    txt('＝ '+num(Lc)+' km',PX0+12,422,'#0e7490',26,1,'left','alphabetic',256);
    txt('実際（子午線の一周）40,008 km との差 '+(err>=0?'+':'−')+fx(Math.abs(err),1)+'%',PX0+12,446,'#334155',12,0,'left','alphabetic',256);
    txt('地球の半径 ＝ 一周 ÷ 2π ＝ '+num(Lc/2/Math.PI)+' km',PX0+12,466,'#334155',12,0,'left','alphabetic',256);
    if(mode===0) txt('925 kmは5,000スタディア（1スタディオン185 m）',PX0+12,488,'#64748b',11,0,'left','alphabetic',256);
    else { txt(c.ns?'南北の距離（子午線にそった長さ）を使用':'2地点間の距離を使用（経度差 '+fx(Math.abs(c.q[2]-c.q[5]),2)+'°の分だけ長い）',PX0+12,488,'#64748b',11,0,'left','alphabetic',256);
      txt('南北 '+fx(c.q[6],1)+' km ／ 2地点間 '+fx(c.q[7],1)+' km',PX0+12,505,'#64748b',11,0,'left','alphabetic',256); }
    if(mode===0) txt('シエネとアレクサンドリアはほぼ南北に並ぶ',PX0+12,505,'#64748b',11,0,'left','alphabetic',256);
    tabs(MODES,mode);
    setK('s1',mode===0?'中心角 θ（影の角度）':'緯度の差 Δφ'); setK('s2',c.dlab); setK('s3','計算した地球一周'); setK('s4','実際の一周との差');
    fit('s1',fx(c.dphi,mode===0?1:3)+'°'); fit('s2',dstr(c.d)+' km'); fit('s3',num(Lc)+' km'); fit('s4',(err>=0?'+':'−')+fx(Math.abs(err),1)+'%');
    setShare(mode===0?'【エラトステネスの方法】影の角度'+fx(c.dphi,1)+'°・距離'+num(c.d)+'kmから地球一周は'+num(Lc)+'km（実際は約40,000km）｜シミュラボ'
      :'【エラトステネスの方法】'+c.n1+'と'+c.n2+'（緯度の差'+fx(c.dphi,3)+'°・'+c.dlab+fx(c.d,1)+'km）から地球一周は'+num(Lc)+'km｜シミュラボ'); }
  function setMode(m){ mode=m; $('mode').value=MV[m]; showField('th',m===0); showField('dk',m===0); showField('pair',m===1); showField('dist',m===1); showBtn('reset',m===0); draw(); }
  cv.addEventListener('pointerdown',e=>{ const p=cpos(cv,e), px=p[0]/dpr, py=p[1]/dpr; if(py<40){ const i=Math.floor((px-6)/((W-12)/2)); if(i>=0&&i<2) setMode(i); return; }
    if(mode===0&&px<PX0){ drag=true; if(cv.setPointerCapture) try{ cv.setPointerCapture(e.pointerId); }catch(_){} mv(px,py); } });
  function mv(px,py){ const a=Math.atan2(CY-py,px-CX)/R; $('th').value=clamp(Math.round(a*10)/10,1,20); $('th').dispatchEvent(new Event('input')); }
  cv.addEventListener('pointermove',e=>{ if(!drag) return; const p=cpos(cv,e); mv(p[0]/dpr,p[1]/dpr); });
  window.addEventListener('pointerup',()=>{ drag=false; });
  $('mode').addEventListener('change',()=>setMode(Math.max(0,MV.indexOf($('mode').value))));
  ['th','dk','pair','dist'].forEach(id=>{ $(id).addEventListener('input',draw); $(id).addEventListener('change',draw); });
  $('reset').addEventListener('click',()=>{ $('th').value=7.2; $('dk').value=925; ['th','dk'].forEach(id=>$(id).dispatchEvent(new Event('input'))); });
  setMode(mode);
'''

sim(slug="eratosthenes", cat="rika", emoji="🌍", score=79,
    title="エラトステネスの方法で地球の大きさを測るシミュレーター（地球の全周の求め方）",
    title_tag="エラトステネスの方法のシミュレーター｜地球の大きさの求め方（360°:θ＝全周:距離）と日本の2都市で計算",
    meta_desc="エラトステネスが地球の大きさを測った方法を、地球の断面図・平行な太陽光線・棒の影で再現する無料シミュレーター。影の角度7.2°と距離925 kmから地球一周約46,000 kmを求め、日本の2都市の緯度の差と南北の距離で計算し直すと約40,000 kmになることも確かめられます。tanの計算・扁平な地球の話つき。地学基礎の授業に。",
    og_title="エラトステネスの方法で地球の大きさを測るシミュレーター",
    og_desc="平行な太陽光線と棒の影から中心角を求め、360°:θ＝全周:距離 で地球一周を計算。シエネとアレクサンドリア、日本の2都市で比べられる地学基礎の教材です。",
    card_desc="棒の影の角度と2地点の距離から地球一周を計算。シエネとアレクサンドリア、日本の2都市で比べる。",
    lead="夏至の正午、シエネでは影ができず、アレクサンドリアでは棒の影の角度が7.2°でした。太陽の光は平行なので、この角度は地球の中心角に等しく、360°:7.2°＝地球一周:925 km から地球の大きさが求められます。日本の2都市の緯度の差と南北の距離でも計算してみましょう。",
    model="地学基礎 地球の形と大きさ",
    level="高校（地学基礎）",
    unit="高等学校 地学基礎（1）地球のすがた ア（ｱ）㋐ 地球の形と大きさ",
    canvas=canvas(640, 520, light=True),
    controls=select("mode", "測り方", [("erato", "① エラトステネスの測定"), ("japan", "② 日本の2都市で測る")])
           + slider("th", "影の角度（中心角）θ", 1, 20, 7.2, 0.1, "{v}°")
           + slider("dk", "2地点の距離", 100, 3000, 925, 5, "{v} km")
           + select("pair", "2つの都市", PAIR_OPTS)
           + select("dist", "使う距離", [("ns", "南北の距離（子午線にそう）"), ("geo", "2地点間の直線距離")]),
    buttons=btn("reset", "↺ エラトステネスの値（7.2°・925 km）"),
    stats=stats([("s1", "中心角 θ（影の角度）", False), ("s2", "2地点の距離", False), ("s3", "計算した地球一周", True), ("s4", "実際の一周との差", False)]),
    legend="左：地球の断面。黄色の線が太陽の光（平行な光線）、赤と青の棒が2地点に立てた棒、黒い線が影、オレンジの角が中心角です。角度は実際の大きさで描き、棒の長さは誇張しています。①では地球の断面をなぞると影の角度が変わります。右：2地点の棒と影の拡大図（棒の高さ1 m）と、地球一周を求める比例式。②の都市の緯度経度は都道府県庁の位置（世界測地系）、距離は地球を回転楕円体として計算した値です。",
    article='''
<h2>このシミュレーションでわかること</h2>
''' + P("<b>エラトステネスの方法とは、南北に離れた2地点で同時に測った太陽の光の角度の差（＝地球の中心角θ）と2地点間の距離から、比例式 360° : θ ＝ 地球一周 : 距離 によって地球の大きさを求める方法です。</b>紀元前3世紀に、エラトステネスはシエネとアレクサンドリアの間の中心角7.2°（円の1/50）と距離から、地球一周を求めました。") + '''
<p>このシミュレーターでは、地球の断面図に平行な太陽の光・2地点の棒と影・中心角を描き、影の長さと棒の高さから角度を求める計算（tan）と、地球一周の比例式を確かめます。日本の2都市（都道府県庁）の緯度の差と南北の距離で計算すると約40,000 kmになること、南北に並んでいない2地点の直線距離を使うと大きめに出ることもわかります。</p>
''' + T([[NW("地学基礎"), "（1）地球のすがた ア（ｱ）惑星としての地球 ㋐ 地球の形と大きさ", "地球の形や大きさに関する観察、実験などを行い、地球の形の特徴と大きさを見いだして理解すること（測定の歴史や方法にも触れる）"]],
         ["科目", "単元", "学習指導要領（平成30年告示）の内容"]) + '''
<p>高等学校学習指導要領解説 理科編（地学基礎 p.152）は、エラトステネスの方法を取り上げて測定の歴史や方法に触れること、地球を球と仮定して子午線方向に離れた2地点の緯度の差と距離を地形図や情報通信ネットワークで閲覧できる地図などで調べ、地球の大きさを求めさせることを例にあげています。</p>

<h2>授業での使い方</h2>
<p><b>導入</b>：「地球の大きさを、2本の棒と影だけで測れるだろうか」と問いかけ、①の図でシエネ（影なし）とアレクサンドリア（影の角度7.2°）を見せます。太陽の光が平行であることから、影の角度と中心角が等しいこと（平行線の錯角）を確認します。</p>
<p><b>展開</b>：比例式 360°:7.2°＝地球一周:925 km を立てて計算させ、シミュレーターの値（46,250 km）と照らし合わせます。影の角度や距離のスライダーを動かして、角度を少しまちがえるだけで結果が大きく変わることも確かめます。</p>
<p><b>まとめ</b>：②に切りかえ、日本の2都市の緯度の差と南北の距離から地球一周を計算します。「使う距離」を2地点間の距離に変え、経度の差が大きい組み合わせほど結果が大きくなる理由を考えさせます。地球が極方向に少しつぶれていることにもふれます。</p>
<p>生徒への問いの例です。</p>
<ul>
<li>アレクサンドリアで高さ1 mの棒の影が12.6 cmだったとき、太陽の光と棒のなす角は何度でしょう。（tanθ＝0.126 より θ≒7.2°）</li>
<li>緯度の差が1°で、南北の距離が111 kmの2地点から、地球一周は何kmと求められるでしょう。（111 km×360＝39,960 km）</li>
<li>札幌と那覇の「2地点間の距離」を使うと、地球一周が約48,000 kmと大きく出てしまうのはなぜでしょう。（2地点は南北に並んでおらず、距離に東西方向の分がふくまれるから）</li>
</ul>

<h2>しくみ・解説</h2>
<h3>用語の意味</h3>
<ul>
<li><b>中心角</b>とは、地球の中心から2地点を見たときに2本の半径がつくる角度で、南北に並ぶ2地点では緯度の差に等しくなります。</li>
<li><b>子午線</b>とは、北極と南極を結ぶ経線のことで、子午線にそって測った2地点の長さが「南北の距離」です。</li>
<li><b>扁平率</b>とは、地球（回転楕円体）のつぶれ具合を表す値で、（赤道半径−極半径）÷赤道半径 ≒ 1/298 です。</li>
</ul>
<h3>地球一周を求める式</h3>
''' + N("360° : θ ＝ 地球一周 L : 2地点間の距離 d　より　L ＝ d × 360° ÷ θ<br>地球の半径 r ＝ L ÷ 2π<br>影の角度：tan θ ＝ 影の長さ ÷ 棒の高さ　→　θ ＝ tan⁻¹（影の長さ ÷ 棒の高さ）") + '''
<p>太陽はとても遠いので、地球に届く太陽の光は平行と考えられます。シエネの棒を地球の中心までのばした直線と、アレクサンドリアの棒を中心までのばした直線は、中心でθの角をつくります。アレクサンドリアに届く光は、シエネの棒の延長線（光の向き）と平行なので、棒と光のなす角も錯角でθになります。だから、影から測った角度がそのまま地球の中心角になります。</p>
<h3>影の長さから角度を求める（tan の早見表）</h3>
''' + TAN_TABLE + '''
<p><b>計算例1（エラトステネス）</b>：夏至の日の正午、シエネでは影ができず、アレクサンドリアでは太陽の光と棒のなす角が7.2°でした。2地点間の距離を925 kmとすると、地球一周は何kmですか。<br>答え：L＝925 km×360°÷7.2°＝925×50＝<b>46,250 km</b>（実際の子午線の一周 40,008 km より約16%大きい）</p>
<p>エラトステネスは2地点間の距離を5,000スタディアとし、地球一周を250,000スタディア（のちに252,000スタディア）としました。1スタディオンの長さは時代や地域で異なり、185 mとすると約46,000 km、157.5 mとすると約39,700 kmになるため、どれだけ正確だったかについては複数の説があります。実際のシエネ（現在のアスワン、北緯24.09°）とアレクサンドリア（北緯31.20°）の緯度の差は7.11°、南北の距離は約788 kmで、これを使うと 788×360÷7.11≒39,900 km になります。2つの都市は経度が約3°ずれていて、ちょうど南北には並んでいません。</p>
<p><b>計算例2（影の長さから）</b>：春分の日の正午、青森で高さ1 mの棒の影が86.4 cm、仙台で78.9 cmでした。2地点の南北の距離を283.8 kmとして地球一周を求めなさい。<br>答え：tan⁻¹0.864≒40.82°、tan⁻¹0.789≒38.27°。緯度の差は約2.55°なので、L＝283.8×360÷2.55≒<b>約40,000 km</b>（緯度の差を2.556°とすると39,972 km）。春分・秋分の日の正午には、太陽の光と棒のなす角がその地点の緯度に等しくなります。</p>
<h3>日本の2都市で計算した結果</h3>
''' + PAIR_TABLE + '''
<p>南北の距離（子午線にそった長さ）を使うと、どの組み合わせでも約39,900〜40,000 kmになります。2地点間の距離（地図上でまっすぐ測った距離）を使うと、2地点が真南・真北に並んでいない分だけ距離が長くなり、地球一周が大きく出ます。経度の差が0.04°の新潟—前橋ではほとんど差がなく、経度の差が13.7°ある札幌—那覇では約20%大きくなります。2地点間の距離を使うときは、経度の差ができるだけ小さい（南北にほぼ並ぶ）組み合わせを選ぶことが大切です。</p>
<h3>地球は少しつぶれている（測定でわかる地球の形）</h3>
''' + T([["赤道付近", "110.57 km"], ["緯度35°（日本付近）", "110.94 km"], ["緯度45°", "111.13 km"], ["極付近", "111.69 km"]],
        ["場所", "緯度1°あたりの子午線の長さ"]) + '''
<p>緯度1°あたりの子午線の長さは、高緯度ほど長くなります。これは、地球が赤道方向にふくらみ、極方向に少しつぶれた回転楕円体だからです（赤道半径6,378 km、極半径6,357 km、扁平率約1/298）。日本付近（緯度30〜40°台）のデータでは、1°あたりの長さが平均より少し短いため、地球一周も40,008 kmより少し小さく（約39,950 km）求まります。地学基礎の解説も、低緯度と高緯度のデータで求めた地球の大きさが異なることから、地球が厳密には球でないことに気付かせることを例にあげています。</p>
<h3>このシミュレーションで単純化していること</h3>
<ul>
<li>断面図は地球を球として描いています。中心角などの角度は実際の大きさですが、棒の長さは見やすいように誇張しています。①では、シエネを夏至の日の正午に太陽が真上にくる地点として描いています。</li>
<li>②の都市の位置は都道府県庁の緯度・経度（世界測地系、小数第4位まで）です。南北の距離は地球を回転楕円体（GRS80）とした子午線の長さ、2地点間の距離は同じ楕円体の上の最短距離（Vincentyの式）で計算しました。地球を半径6,371 kmの球として計算した距離との差は0.5%以内です。</li>
<li>②の影の長さは、春分・秋分の日のそれぞれの地点の南中時（太陽が真南にきたとき）の値で、大気による光の屈折は考えていません。経度が違う2地点では南中の時刻がずれますが、同じ日の南中時に測れば、角度の差は緯度の差になります。</li>
</ul>

<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「高等学校学習指導要領（平成30年告示）解説 理科編 理数編」地学基礎 p.152（''' + A(MEXT_KOU) + '''）</li>
<li>国土地理院「地理院地図」（''' + A("https://maps.gsi.go.jp/") + '''）…2地点の緯度・経度と距離を調べるのに使えます</li>
<li>国立天文台 編『理科年表』（丸善出版）…地球の赤道半径・極半径・扁平率（GRS80）</li>
<li>高等学校「地学基礎」の教科書（地球の形と大きさの単元）</li>
</ul>
''',
    faqs=[("エラトステネスはどうやって地球の大きさを測ったのですか？", "夏至の日の正午、シエネでは太陽が真上にきて井戸の底まで光が届き、北にあるアレクサンドリアでは太陽の光が棒と7.2°（円の1/50）の角をつくることを使いました。太陽の光は平行なので7.2°は地球の中心角に等しく、2地点間の距離の50倍が地球一周になります。"),
          ("地球の全周を求める式は何ですか？", "360° : θ ＝ 地球一周 : 2地点間の距離 です。地球一周 ＝ 距離 × 360° ÷ θ で、たとえば θ＝7.2°、距離925 kmなら 925×360÷7.2＝46,250 km になります。"),
          ("影の長さと棒の高さから角度を求めるには？", "tan θ ＝ 影の長さ ÷ 棒の高さ の関係を使い、θ ＝ tan⁻¹（影の長さ ÷ 棒の高さ）で求めます。高さ1 mの棒の影が12.6 cmなら tanθ＝0.126 で、θ≒7.2°です。"),
          ("エラトステネスの値（約46,000 km）が実際の約40,000 kmとずれたのはなぜですか？", "距離（5,000スタディア）をkmに直すときの1スタディオンの長さがはっきりしないこと、シエネとアレクサンドリアが真南・真北に並んでいないこと、距離の測定のあらさなどが理由と考えられています。1スタディオンを157.5 mとすると約39,700 kmになります。"),
          ("日本の2都市で地球の大きさを測るときの注意点は？", "経度の差ができるだけ小さく、南北にほぼ並ぶ2地点を選び、緯度の差と南北の距離（子午線にそった長さ）を使うことです。2地点間の直線距離を使うと東西方向の分だけ長くなり、地球一周が大きく出ます。"),
          ("地球は完全な球ですか？", "いいえ。赤道方向にふくらんだ回転楕円体で、赤道半径は約6,378 km、極半径は約6,357 kmです。緯度1°あたりの子午線の長さが赤道付近（110.57 km）より極付近（111.69 km）で長いことからわかります。")],
    rel=[("taiyou-ugoki", "🌞", "太陽の1日の動きと季節"), ("hiruma-nagasa", "🌅", "昼の長さメーター"), ("coriolis-henseifu", "🌀", "コリオリの力と大気の大循環"),
         ("solar-system", "🪐", "太陽系シミュレーター"), ("kaibatsu-check", "⛰️", "うちの海抜チェッカー")],
    js=JS2.replace("%%UI%%", UI_COMMON).replace("%%PAIRS%%", PAIRS_JS))
