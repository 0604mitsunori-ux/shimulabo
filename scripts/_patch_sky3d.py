# -*- coding: utf-8 -*-
"""既存の天体ページに「3Dで見る」を足す（2026-11-08）。2Dの図と操作はそのまま、同じスライダーで動く3Dを下に置く
   使い方: python scripts/_patch_sky3d.py [slug ...]   … 何度実行しても同じ結果（前に入れた3Dの部分は入れ直す）
   3Dの中身は sims/<slug>/view3d.js。three.js は見える位置までスクロールしてから読み込む
"""
import io, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = {
    "tsuki-michikake": ([("top", "宇宙（北極の上）から"), ("side", "ななめから"), ("earth", "地球から月を見る")],
                        "太陽・地球・月を3Dで回して見られます（大きさと距離は誇張）。「地球から月を見る」にすると、地球のそばから見た月の形になります。月齢と時刻は上のスライダーで動かしてください。", None),
    "gesshoku-nisshoku": ([("moon", "月のそば（地球から見る向き）"), ("side", "横から全体"), ("earth", "地球のそば")],
                          "太陽・地球・月の大きさと距離を実際の比率で並べ、地球の影（本影・半影）と月の影を3Dで表示しています。上の「見るとき」「月齢」「通り道のずれ」と連動します。", None),
    "taiyou-ugoki": ([("persp", "ななめ上（南南東）から"), ("top", "真上から"), ("east", "東から")],
                     "透明半球を3Dで回して見られます。オレンジが選んだ日の太陽の通り道、点線が夏至・春分秋分・冬至です。中心の棒の影も、太陽の位置に合わせて動きます。",
                     None),
    "hoshi-ugoki": ([("south", "南を見る"), ("north", "北を見る"), ("east", "東を見る"), ("west", "西を見る"), ("out", "天球を外から")],
                    "東京で見上げた星空を3Dにしています。「天球を外から」にすると、星が北極星の近くを軸にして回っている様子（天球の回転）が分かります。上の日付・時刻・注目する星と連動します。",
                    ("  const AS=", "  window.__hoshi={ST:ST,CO:CO,LAT:LAT,LON:LON};\n  const AS=")),
    "kinsei-michikake": ([("top", "北極の上から"), ("side", "ななめから"), ("earth", "地球から金星を見る")],
                         "太陽・金星・地球の位置を3Dで表示しています（大きさは誇張）。「地球から金星を見る」で、望遠鏡で見たときの金星の形と向きになります。上の日付と連動します。",
                         ("  function visOf(st){", "  { const __st0=state; state=function(){ const s=__st0(); window.__sim2d={lv:s.lv, le:s.le}; return s; }; }\n  function visOf(st){")),
    # ---- 地学（2026-11-08 追加）。4つ目の値 False＝明るい背景 ----
    "chisou": ([("persp", "ななめ上（南東）から"), ("south", "南から（上の断面図と同じ向き）"), ("top", "真上から（地表の地層）"), ("nw", "北西から")],
               "上の断面図を手前の面にして、奥（北）へ160m分を立体にしています。A〜Dの柱はボーリングで取り出した地層（深さ35m）です。上の「積もらせる」「噴火」「断層」「しゅう曲」と連動します。高さは横の約2.5倍に強調し、奥の地形の起伏は説明のための模式です。",
               ("  loadExample(); draw(); requestAnimationFrame(loop);",
                "  window.__chisou={G:G,base:base,blocks:blocks,hasF:hasF,zc:zc,topMat:topMat,Hx:Hx,ashIdx:ashIdx,seaY:seaY,TY:TY,st:()=>({L:L,BOT:BOT,phase:phase,B:B,sel:sel,fA:fA,fS:fS,k:k,U:U,lift:lift,ero:ero,drill:drill,erupt:erupt,tm:tm,depositing:depositing})};\n  loadExample(); draw(); requestAnimationFrame(loop);"),
               False),
    "kazan-kaseigan": ([("persp", "ななめ上から（切り口を見る）"), ("south", "南から（断面）"), ("top", "真上から")],
                       "上の図の火山の形を回して立体にし、手前の4分の1を切り取って、マグマだまり・火道（マグマの通り道）と、ア（地表付近）・イ（地下深く）の場所を見せています。上の「マグマのねばりけ」「例の火山」「冷え方」「噴火を止める」と連動します。大きさは実際の比率ではありません。",
                       ("  viscLabel(); draw(); requestAnimationFrame(loop);",
                        "  window.__kazan={vh:vh,reach:reach,shW:shW,rockC:rockC,cls:cls,st:()=>({p:p,erupting:erupting,tm:tm})};\n  viscLabel(); draw(); requestAnimationFrame(loop);"),
                       False),
    "jishin-ha": ([("persp", "ななめ上から"), ("south", "南から（地下の断面）"), ("top", "真上から（上の地図と同じ）")],
                  "上の地図を地表にして、地下110kmまでを箱にしています。赤い点が震源、×が震央です。青い球がP波、赤い球がS波の先頭で、地表では円に、震源を通る断面（東西）では同心円に見えます。オレンジの点線は、選んだ観測点までの震源距離です。上の「地震を起こす」「震源の深さ」「観測点を選ぶ」「時間」と連動します。たてと横は同じ縮尺で、地図と観測点は上の図と同じ架空のものです。",
                  ("  tog(); vlab(); draw(model()); requestAnimationFrame(frame);",
                   "  window.__jishin={model:model,ST:ST,COAST:COAST,surfR:surfR,st:()=>({ex:ex,ey:ey,t:t,sel:sel,playing:playing})};\n  tog(); vlab(); draw(model()); requestAnimationFrame(frame);"),
                  False),
    # ---- 宇宙・生き物（2026-11-08 追加）。5つ目の値＝入れる場所（lab-legend が無いページ） ----
    "dna": ([("persp", "ななめから"), ("side", "横から"), ("top", "らせんの軸の方向から")],
            "2本の鎖（糖とリン酸）を、塩基のペア（A–T、G–C）がはしごのようにつないだ右巻きのらせんです。直径約2nm、塩基対10個で1回転（約3.4nm）にしています。上の「回転スピード」と連動します。「ほどいてコピーする」を押すと、ほどけた鎖それぞれに相手の塩基が組み、同じ並びのDNAが2つできる様子を見られます（ほどけた所ははしごの形にのばした模式。原子の細かい形は省いています）。",
            ("    function loop(){", "    window.__dna={st:()=>({p:p})};\n    function loop(){"),
            True, r'<p style="text-align:center;color:var\(--ink-2\);font-size:13px;margin-top:14px;">.*?</p>'),
    "solar-system": ([("persp", "ななめ上から"), ("top", "北の上から（上の図と同じ向き）"), ("side", "横から（軌道の面）")],
                     "上の図と同じ8つの惑星を、同じ角度・同じ速さ（実際の公転周期の比）で回しています。北の上から見て反時計回りが、実際の回る向きです。「本当の距離の比率」にすると、ページの表の距離（天文単位）どおりに並びかえます。惑星と太陽の大きさは見やすく誇張しています。上の「スピード」「軌道を表示」「一時停止」と連動します。",
                     ("const x0=cx+Math.cos(ang[i])*p[0],y0=cy+Math.sin(ang[i])*p[0];",
                      "const x0=cx+Math.cos(ang[i])*p[0],y0=cy-Math.sin(ang[i])*p[0];if(!window.__solar||window.__solar.P!==P)window.__solar={P:P,st:()=>({ang:ang,playing:playing})};"),
                     True, r'<p style="text-align:center;color:var\(--ink-2\);font-size:13px;margin-top:14px;">.*?</p>'),
    "iss-doko": ([("whole", "地球全体（ISSの上から）"), ("iss", "ISSのそばから"), ("japan", "日本の上から")],
                 "地球とISSの高さを同じ縮尺にした地球儀です。黄色い線がこれから45分の通り道、点線がこれまでの通り道で、ISSは今の時刻に合わせて動きます（位置は公開API wheretheiss.at から取得）。赤いピンは上で選んだ地域です。昼と夜の境目も、そのときの太陽の位置で描いています。ISSの大きさは見やすく誇張しています。",
                 ("  const R = 6371;", "  window.__iss={PREFS:PREFS};\n  const R = 6371;"),
                 True, r'<div class="hint" id="state"[^>]*></div>'),
    # ---- 理科（2026-11-08 追加） ----
    "saibou-bunretsu": ([("persp", "ななめから"), ("front", "正面から（上の図と同じ向き）"), ("side", "横から（中央の面を見る）")],
                        "上の図の細胞を立体にして、染色体（4本・色は上の図と同じ）の動きを見せています。「横から」にすると、③で染色体が中央の面に広がって並ぶようすが分かります。「顕微鏡で見た根の先端」では、根を縦に半分に切った模型で、A・B・Cの場所の細胞の大きさと分裂中の細胞を見られます。上の「表示する内容」「段階」「再生」と連動します。形と大きさは簡単にした模式図です。",
                        ("  function frame(ts){ const dt=last?", "  window.__cell={LOCS:LOCS,CELLS:CELLS,TAI:TAI,GEN:GEN,st:()=>({mode:mode,p:p,loc:loc})};\n  function frame(ts){ const dt=last?"),
                        False),
    "denryu-jikai": ([("persp", "ななめから"), ("front", "正面から"), ("top", "真上から")],
                     "上の図の4つの実験（導線・コイルのまわりの磁界／電磁石／ぶらんこ・モーター／電磁誘導・発電機）を立体の模型にしています。オレンジの粒＝電流、青＝磁力線（磁界の向き）、緑の矢印＝力です。上の「実験」「表示」「電流の大きさ」などのボタンやスライダーと連動し、方位磁針・コイル・磁石も上の図と同じように動きます。大きさや形は簡単にした模式図です。",
                     ("  function frame(t){ const dt=last?", "  window.__denki={BX:BX,BY:BY,CN:CN,CL:CL,CA:CA,CPW:CPW,CPC:CPC,coilList:coilList,Bsum:Bsum,st:()=>({m:$('mode').value,v:$('view').value,I:Iof(),dirI:dirI,earth:earth,probe:probe,nd:nd,wo:wo,so:so,core:core,swOn:swOn,shown:shown,N:+$('turns').value,nb:nbat(),magUp:magUp,phi:phi,comm:comm,pSide:pSide,alpha:alpha,omega:omega,magN:magN,mX:mX,iNow:iNow,ndl:ndl,vS:vS,theta:theta,playing:playing})};\n  function frame(t){ const dt=last?"),
                     False),
    "hito-karada": ([("persp", "ななめから"), ("front", "正面から（上の図と同じ向き）"), ("side", "横から")],
                    "上の図の3つの画面を、体の中の立体の模式図にしています。①血液の循環では、心臓の4つの部屋と血管を立体にし、上の図と同じ100粒の血液が肺と全身をめぐります（赤＝酸素が多い血液、青＝二酸化炭素が多い血液）。②呼吸では、ろっ骨と横隔膜の動きで肺がふくらむようすと、肺胞の拡大を、③消化と吸収では、口からこう門までの通り道と柔毛の拡大を見られます。上のボタンやスライダーと連動します。形と大きさは簡単にした模式図です。",
                    ("  function draw(){ ctx.fillStyle='#ffffff';", "  window.__body={H1:H1,H2:H2,parts:parts,oxy:oxy,air:air,AWL:AWL,AWR:AWR,o2:o2,co2:co2,rbc:rbc,CAP:CAP,CAP0:CAP0,CAP1:CAP1,AC:AC,at:at,SP:SP,stg:stg,lvls:lvls,PLACE:PLACE,JUICE_S:JUICE_S,DESC:DESC,st:()=>({mode:mode,run:run,T:T,cph:cph,rph:rph,dp:dp,s6:S6(),hr:+$('hr').value,sv:+$('sv').value,br:+$('br').value,tv:+$('tv').value,B:breath(),amp:ampK(),R:curR()})};\n  function draw(){ ctx.fillStyle='#ffffff';"),
                    False),
}
CSS = '<link rel="stylesheet" href="../../assets/three/sim3d.css?v=1">'
LOADER = """<script>(()=>{const el=document.getElementById('view3d');if(!el)return;const go=()=>import('./view3d.js?v=1').catch(()=>{const l=el.querySelector('.load');if(l)l.textContent='3D表示を読み込めませんでした';});if('IntersectionObserver' in window){const io=new IntersectionObserver(es=>{if(es[0].isIntersecting){io.disconnect();go();}},{rootMargin:'300px'});io.observe(el);}else go();})();</script>"""

for slug in (sys.argv[1:] or PAGES):
    cams, legend, hook = PAGES[slug][:3]
    dark = PAGES[slug][3] if len(PAGES[slug]) > 3 else True
    anchor = PAGES[slug][4] if len(PAGES[slug]) > 4 else None   # lab-legend が無いページは、入れる場所（正規表現）を指定
    lstyle = "margin-top:6px;" if anchor is None else "margin-top:6px;text-align:center;color:var(--ink-2);font-size:13px;line-height:1.7;"
    p = os.path.join(ROOT, "sims", slug, "index.html")
    h = io.open(p, encoding="utf-8").read()
    assert os.path.isfile(os.path.join(ROOT, "sims", slug, "view3d.js")), slug
    h = re.sub(r"\n?<!-- sky3d:start -->.*?<!-- sky3d:end -->", "", h, flags=re.S)
    h = re.sub(r"\n?<!-- sky3d-loader:start -->.*?<!-- sky3d-loader:end -->", "", h, flags=re.S)
    if CSS not in h:
        h = h.replace('<link rel="stylesheet" href="../../assets/style.css?v=4">', '<link rel="stylesheet" href="../../assets/style.css?v=4">\n' + CSS, 1)
    btns = "".join('<button data-v="%s"%s>%s</button>' % (k, ' class="on"' if i == 0 else "", t) for i, (k, t) in enumerate(cams))
    block = """
<!-- sky3d:start -->
    <div class="v3d-block" style="width:100%%;margin-top:18px;">
      <h3 style="margin:0 0 8px;font-size:15px;">🧊 3Dで見る（ドラッグで回転・上の操作と連動）</h3>
      <div class="view3d%s" id="view3d"><div class="load">3D模型を読み込み中…</div><div class="hud" id="hud3d" style="display:none"></div></div>
      <div class="cam-row" id="camRow3d">%s</div>
      <p class="lab-legend" style="%s">%s</p>
    </div>
<!-- sky3d:end -->""" % (" dark" if dark else "", btns, lstyle, legend)
    m = re.search(anchor or r'<p class="lab-legend">.*?</p>', h, flags=re.S)
    assert m, slug
    h = h[:m.end()] + block + h[m.end():]
    h = h.replace('<script src="../../assets/share-counter.js', "<!-- sky3d-loader:start -->\n" + LOADER + "\n<!-- sky3d-loader:end -->\n" + '<script src="../../assets/share-counter.js', 1)
    if hook and hook[1] not in h:
        assert hook[0] in h, (slug, "hook")
        h = h.replace(hook[0], hook[1], 1)
    io.open(p, "w", encoding="utf-8").write(h)
    print("patched", slug)
