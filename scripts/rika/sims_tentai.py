# -*- coding: utf-8 -*-
"""理科の授業向け（天体の動き）：太陽の1日の動きと季節／星の1日・1年の動き
   照合メモ（2026-10-04）
   - taiyou-ugoki：太陽の赤緯は、地軸の傾きを教科書どおり23.4°とし、2026年の春分3/20・夏至6/21・秋分9/23・冬至12/22の
     正午にちょうど 0°・＋23.4°・0°・−23.4° になるよう黄経を区間ごとに直線でつないだもの。均時差は USNO の近似式。
     Meeus『Astronomical Algorithms』25章の式（国立天文台の表と丸めの範囲で一致を確認）と比べ、2026年の1年間で
     赤緯の差 0.20°以内・南中高度 0.24°以内・南中時刻 0.5分以内・日の出入り 1.6分以内（東京・札幌・那覇）。
     国立天文台 暦計算室「日の出入り」2026年：東京 3/20 5:45・11:49・17:52、6/21 4:25・11:43(77.8°)・19:00、
     9/23 5:29・11:34・17:37、12/22 6:47・11:39(30.9°)・16:32、10/4 5:38・11:30(50.0°)・17:21／
     札幌 6/21 3:55・11:36(70.4°)・19:18／那覇 12/22 7:13・12:28(40.4°)・17:43。
   - hoshi-ugoki：星の赤経・赤緯・V等級は SIMBAD（CDS）の値（ICRS, J2000）を 2026.5年へ歳差補正（Meeus 21章）。
     恒星時は Meeus 12.4（平均恒星時）。東京は国立天文台の暦計算室と同じ 北緯35.6581°・東経139.7414°。
     Python で別の方法（回転行列による歳差＋ベクトルの回転）で計算した高度・方位と、10例で差 0.006°以内。
     各月15日21時の南の空（子午線から2.2時間以内・天頂より南で南中）：1〜2月 オリオン・おうし・おおいぬ・こいぬ・ふたご／
     4〜5月 しし・おとめ・うしかい／7〜8月 さそり・いて・わし／10〜11月 ペガスス・アンドロメダ・みなみのうお。
     0時に南中する日：ベテルギウス12/16・アンタレス5/26。南中は1日に3.93分早くなる（30日で118分）。北極星の高度35.03〜36.28°。
"""
import json, math
from common import canvas, slider, select, btn, stats, T, N, P

SIMS = []
def sim(**kw): SIMS.append(kw)

A = lambda url, text=None: '<a href="%s" rel="noopener" target="_blank">%s</a>' % (url, text or url)
NW = lambda t: '<span style="white-space:nowrap">%s</span>' % t   # 表の短いセルを折り返さない
MEXT_SHO = "https://www.mext.go.jp/component/a_menu/education/micro_detail/__icsFiles/afieldfile/2019/03/18/1387017_005_1.pdf"
MEXT_CHU = "https://www.mext.go.jp/component/a_menu/education/micro_detail/__icsFiles/afieldfile/2019/03/18/1387018_005.pdf"

# ============================================================ 星のデータ（SIMBAD・J2000）
# key, 赤経(°), 赤緯(°), V等級, 色(r赤 o橙 y黄 w白 b青白), 名前, 図に名前を出すか
STAR_DATA = [
    ("aOri", 88.79293899, 7.40706400, 0.42, "r", "ベテルギウス", 1), ("bOri", 78.63446707, -8.20163836, 0.13, "b", "リゲル", 1),
    ("gOri", 81.28276356, 6.34970326, 1.64, "b", "", 0), ("dOri", 83.00166706, -0.29909511, 2.41, "b", "", 0),
    ("eOri", 84.05338894, -1.20191914, 1.69, "b", "", 0), ("zOri", 85.18969443, -1.94257359, 1.77, "b", "", 0),
    ("kOri", 86.93912017, -9.66960492, 2.06, "b", "", 0), ("lOri", 83.78449002, 9.93415587, 3.66, "b", "", 0),
    ("aCMa", 101.28715533, -16.71611586, -1.46, "b", "シリウス", 1), ("bCMa", 95.67493897, -17.95591871, 1.97, "b", "", 0),
    ("dCMa", 107.09785021, -26.39319958, 1.84, "y", "", 0), ("eCMa", 104.65645315, -28.97208616, 1.50, "b", "", 0),
    ("hCMa", 111.02375950, -29.30310551, 2.45, "b", "", 0),
    ("aCMi", 114.82549791, 5.22498756, 0.37, "y", "プロキオン", 1), ("bCMi", 111.78767391, 8.28931576, 2.89, "b", "", 0),
    ("aTau", 68.98016279, 16.50930235, 0.86, "o", "アルデバラン", 1), ("bTau", 81.57297133, 28.60745172, 1.65, "b", "", 0),
    ("zTau", 84.41118926, 21.14254411, 3.03, "b", "", 0), ("gTau", 64.94834968, 15.62764205, 3.65, "o", "", 0),
    ("dTau", 65.73372983, 17.54251383, 3.76, "o", "", 0), ("eTau", 67.15416773, 19.18043421, 3.53, "o", "", 0),
    ("tTau", 67.16559005, 15.87087465, 3.41, "w", "", 0), ("hTau", 56.87115230, 24.10513565, 2.87, "b", "すばる", 1),
    ("aGem", 113.64947164, 31.88828222, 1.58, "w", "カストル", 0), ("bGem", 116.32895777, 28.02619889, 1.14, "o", "ポルックス", 1),
    ("gGem", 99.42796043, 16.39928043, 1.92, "w", "", 0), ("dGem", 110.03072736, 21.98230405, 3.53, "w", "", 0),
    ("eGem", 100.98302980, 25.13112719, 2.98, "y", "", 0), ("mGem", 95.74011193, 22.51358275, 2.87, "r", "", 0),
    ("aAur", 79.17232794, 45.99799147, 0.08, "y", "カペラ", 1), ("bAur", 89.88217887, 44.94743257, 1.90, "w", "", 0),
    ("tAur", 89.93029218, 37.21258463, 2.62, "w", "", 0), ("iAur", 74.24841676, 33.16609377, 2.69, "o", "", 0),
    ("aLeo", 152.09296244, 11.96720878, 1.40, "b", "レグルス", 1), ("bLeo", 177.26490976, 14.57205806, 2.13, "w", "デネボラ", 0),
    ("gLeo", 154.99314359, 19.84148867, 2.23, "o", "", 0), ("dLeo", 168.52708927, 20.52371814, 2.53, "w", "", 0),
    ("tLeo", 168.56002363, 15.42957109, 3.35, "w", "", 0), ("hLeo", 151.83313496, 16.76266332, 3.41, "w", "", 0),
    ("eLeo", 146.46280674, 23.77425378, 2.98, "y", "", 0), ("mLeo", 148.19090422, 26.00695119, 3.88, "o", "", 0),
    ("zLeo", 154.17256318, 23.41731699, 3.41, "w", "", 0),
    ("aVir", 201.29824736, -11.16131949, 0.97, "b", "スピカ", 1),
    ("aBoo", 213.91530029, 19.18240916, -0.05, "o", "アークトゥルス", 1), ("eBoo", 221.24673983, 27.07422232, 2.45, "o", "", 0),
    ("dBoo", 228.87567842, 33.31483124, 3.49, "y", "", 0), ("bBoo", 225.48650960, 40.39056857, 3.52, "y", "", 0),
    ("gBoo", 218.01946533, 38.30824808, 3.02, "w", "", 0), ("rBoo", 217.95745554, 30.37143657, 3.59, "o", "", 0),
    ("aSco", 247.35191542, -26.43200261, 0.91, "r", "アンタレス", 1), ("bSco", 241.35929993, -19.80545278, 2.62, "b", "", 0),
    ("dSco", 240.08335535, -22.62170643, 2.32, "b", "", 0), ("pSco", 239.71297182, -26.11410795, 2.91, "b", "", 0),
    ("sSco", 245.29714881, -25.59279208, 2.89, "b", "", 0), ("tSco", 248.97063689, -28.21601709, 2.81, "b", "", 0),
    ("eSco", 252.54087839, -34.29323159, 2.29, "o", "", 0), ("mSco", 252.96761815, -38.04739946, 2.98, "b", "", 0),
    ("zSco", 253.64585430, -42.36131584, 3.62, "o", "", 0), ("hSco", 258.03830873, -43.23918953, 3.33, "w", "", 0),
    ("thSco", 264.32970772, -42.99782799, 1.85, "w", "", 0), ("iSco", 266.89616446, -40.12699736, 2.99, "w", "", 0),
    ("kSco", 265.62198000, -39.02998308, 2.39, "b", "", 0), ("lSco", 263.40216718, -37.10382355, 1.63, "b", "", 0),
    ("uSco", 262.69098801, -37.29581348, 2.65, "b", "", 0),
    ("mSgr", 273.44087017, -21.05883169, 3.85, "b", "", 0), ("lSgr", 276.99266966, -25.42169850, 2.81, "o", "", 0),
    ("pSgr", 281.41412309, -26.99078265, 3.14, "b", "", 0), ("sSgr", 283.81636041, -26.29672411, 2.07, "b", "", 0),
    ("tSgr", 286.73501297, -27.67041564, 3.31, "o", "", 0), ("zSgr", 285.65304266, -29.88006330, 2.59, "w", "", 0),
    ("aLyr", 279.23473479, 38.78368896, 0.03, "b", "ベガ", 1), ("eLyr", 281.08477455, 39.67012591, 4.6, "w", "", 0),
    ("zLyr", 281.19315451, 37.60512165, 4.36, "w", "", 0), ("dLyr", 283.62617787, 36.89861991, 4.30, "r", "", 0),
    ("gLyr", 284.73592734, 32.68955574, 3.25, "b", "", 0), ("bLyr", 282.51997977, 33.36266677, 3.42, "b", "", 0),
    ("aAql", 297.69582730, 8.86832120, 0.76, "w", "アルタイル", 1), ("bAql", 298.82830351, 6.40676423, 3.71, "y", "", 0),
    ("gAql", 296.56491231, 10.61325872, 2.72, "o", "", 0),
    ("aCyg", 310.35797975, 45.28033881, 1.25, "w", "デネブ", 1), ("gCyg", 305.55709098, 40.25667916, 2.23, "y", "", 0),
    ("hCyg", 299.07654932, 35.08342289, 3.88, "o", "", 0), ("bCyg", 292.68031501, 27.95967363, 3.08, "o", "アルビレオ", 0),
    ("dCyg", 296.24365384, 45.13081463, 2.87, "b", "", 0), ("eCyg", 311.55280115, 33.97032834, 2.48, "o", "", 0),
    ("zCyg", 318.23410829, 30.22689868, 3.21, "y", "", 0),
    ("aPeg", 346.19022269, 15.20526715, 2.48, "b", "", 0), ("bPeg", 345.94357275, 28.08278712, 2.42, "r", "", 0),
    ("gPeg", 3.30896812, 15.18359843, 2.84, "b", "", 0), ("ePeg", 326.04648391, 9.87500865, 2.39, "o", "", 0),
    ("zPeg", 340.36550299, 10.83136331, 3.41, "b", "", 0), ("thPeg", 332.54995255, 6.19792159, 3.55, "w", "", 0),
    ("aAnd", 2.09691619, 29.09043112, 2.06, "b", "", 0), ("dAnd", 9.83167964, 30.86098358, 3.28, "o", "", 0),
    ("bAnd", 17.43301617, 35.62055765, 2.05, "r", "", 0), ("gAnd", 30.97480121, 42.32972842, 2.10, "o", "", 0),
    ("bCas", 2.29452158, 59.14978110, 2.27, "w", "", 0), ("aCas", 10.12684601, 56.53732922, 2.23, "o", "シェダル", 0),
    ("gCas", 14.17721289, 60.71674002, 2.39, "b", "", 0), ("dCas", 21.45396446, 60.23528403, 2.68, "w", "", 0),
    ("eCas", 28.59889203, 63.67010007, 3.37, "b", "", 0),
    ("aUMa", 165.93196467, 61.75103469, 1.79, "o", "ドゥーベ", 0), ("bUMa", 165.46033230, 56.38243365, 2.37, "w", "", 0),
    ("gUMa", 178.45769715, 53.69475973, 2.44, "w", "", 0), ("dUMa", 183.85649936, 57.03261698, 3.32, "w", "", 0),
    ("eUMa", 193.50728997, 55.95982296, 1.77, "w", "", 0), ("zUMa", 200.98141867, 54.92535197, 2.23, "w", "", 0),
    ("hUMa", 206.88515734, 49.31326673, 1.86, "b", "", 0),
    ("aUMi", 37.95456067, 89.26410897, 2.02, "y", "北極星", 1), ("dUMi", 263.05415922, 86.58645961, 4.34, "w", "", 0),
    ("eUMi", 251.49268168, 82.03725828, 4.21, "y", "", 0), ("zUMi", 236.01466071, 77.79449312, 4.27, "w", "", 0),
    ("hUMi", 244.37612605, 75.75534308, 4.95, "w", "", 0), ("gUMi", 230.18209805, 71.83402545, 3.00, "w", "", 0),
    ("bUMi", 222.67635750, 74.15550394, 2.08, "o", "", 0),
    ("aPsA", 344.41269272, -29.62223703, 1.16, "w", "フォーマルハウト", 1),
]
# 星座：名前, 線（星のkeyの列）, 代表の星
CONS_DATA = [
    ("オリオン座", [["lOri", "aOri"], ["lOri", "gOri"], ["aOri", "zOri", "kOri"], ["gOri", "dOri", "bOri"], ["dOri", "eOri", "zOri"]], "aOri"),
    ("おおいぬ座", [["bCMa", "aCMa", "dCMa", "hCMa"], ["dCMa", "eCMa"]], "aCMa"),
    ("こいぬ座", [["aCMi", "bCMi"]], "aCMi"),
    ("おうし座", [["bTau", "eTau", "dTau", "gTau", "tTau", "aTau", "zTau"]], "aTau"),
    ("ふたご座", [["aGem", "bGem"], ["aGem", "eGem", "mGem"], ["bGem", "dGem", "gGem"]], "bGem"),
    ("ぎょしゃ座", [["aAur", "bAur", "tAur", "bTau", "iAur", "aAur"]], "aAur"),
    ("しし座", [["aLeo", "hLeo", "gLeo", "zLeo", "mLeo", "eLeo"], ["gLeo", "dLeo", "bLeo", "tLeo", "aLeo"], ["dLeo", "tLeo"]], "aLeo"),
    ("おとめ座", [], "aVir"),
    ("うしかい座", [["aBoo", "eBoo", "dBoo", "bBoo", "gBoo", "rBoo", "aBoo"]], "aBoo"),
    ("さそり座", [["bSco", "dSco", "pSco"], ["dSco", "sSco", "aSco", "tSco", "eSco", "mSco", "zSco", "hSco", "thSco", "iSco", "kSco", "lSco", "uSco"]], "aSco"),
    ("いて座", [["mSgr", "lSgr", "pSgr", "sSgr", "tSgr", "zSgr", "pSgr"]], "sSgr"),
    ("こと座", [["aLyr", "eLyr", "zLyr", "aLyr"], ["zLyr", "dLyr", "gLyr", "bLyr", "zLyr"]], "aLyr"),
    ("わし座", [["gAql", "aAql", "bAql"]], "aAql"),
    ("はくちょう座", [["aCyg", "gCyg", "hCyg", "bCyg"], ["dCyg", "gCyg", "eCyg", "zCyg"]], "aCyg"),
    ("ペガスス座", [["aPeg", "bPeg", "aAnd", "gPeg", "aPeg"], ["aPeg", "zPeg", "thPeg", "ePeg"]], "aPeg"),
    ("アンドロメダ座", [["aAnd", "dAnd", "bAnd", "gAnd"]], "aAnd"),
    ("カシオペヤ座", [["bCas", "aCas", "gCas", "dCas", "eCas"]], "aCas"),
    ("北斗七星（おおぐま座）", [["aUMa", "bUMa", "gUMa", "dUMa", "aUMa"], ["dUMa", "eUMa", "zUMa", "hUMa"]], "aUMa"),
    ("こぐま座", [["aUMi", "dUMi", "eUMi", "zUMi", "bUMi", "gUMi", "hUMi", "zUMi"]], "aUMi"),
    ("みなみのうお座", [], "aPsA"),
]
# 星の並び（点線）：名前, 星, 色
ASTER_DATA = [("夏の大三角", ["aLyr", "aAql", "aCyg", "aLyr"], "#fde047", ["aLyr", "aAql", "aCyg"]),
              ("冬の大三角", ["aOri", "aCMa", "aCMi", "aOri"], "#f9a8d4", ["aOri", "aCMa", "aCMi"]),
              ("春の大曲線", ["eUMa", "zUMa", "hUMa", "aBoo", "aVir"], "#86efac", ["hUMa", "aBoo"])]
# 公転の図に置く季節の星座
ORB_DATA = [("オリオン座", "冬"), ("しし座", "春"), ("さそり座", "夏"), ("ペガスス座", "秋")]
# 「注目する星」の選択肢
SEL_DATA = ["aUMi", "aLeo", "aVir", "aBoo", "aUMa", "aSco", "aLyr", "aAql", "aCyg", "aPsA", "aCas", "aTau", "aAur", "aOri", "bOri", "aCMa", "aCMi", "bGem"]


def precess(ra, dec, year=2026.5):
    """J2000 → year の赤経・赤緯（Meeus 21.2〜21.4）"""
    t = (year - 2000.0) / 100.0
    r = math.radians
    zeta = r((2306.2181 * t + 0.30188 * t * t + 0.017998 * t ** 3) / 3600)
    z = (2306.2181 * t + 1.09468 * t * t + 0.018203 * t ** 3) / 3600
    th = r((2004.3109 * t - 0.42665 * t * t - 0.041833 * t ** 3) / 3600)
    a0, d0 = r(ra), r(dec)
    Aa = math.cos(d0) * math.sin(a0 + zeta)
    Bb = math.cos(th) * math.cos(d0) * math.cos(a0 + zeta) - math.sin(th) * math.sin(d0)
    Cc = math.sin(th) * math.cos(d0) * math.cos(a0 + zeta) + math.cos(th) * math.sin(d0)
    d = math.degrees(math.asin(Cc)) if abs(Cc) < 0.9 else math.copysign(math.degrees(math.acos(math.hypot(Aa, Bb))), Cc)
    return (math.degrees(math.atan2(Aa, Bb)) + z) % 360, d


def ecl_lon(ra, dec, eps=23.4366):
    r = math.radians
    return math.degrees(math.atan2(math.sin(r(ra)) * math.cos(r(eps)) + math.tan(r(dec)) * math.sin(r(eps)), math.cos(r(ra)))) % 360


KEY = {s[0]: i for i, s in enumerate(STAR_DATA)}
STARS26 = [precess(s[1], s[2]) for s in STAR_DATA]


def centroid(keys):
    vx = vy = vz = 0.0
    for k in keys:
        ra, dec = STARS26[KEY[k]]
        vx += math.cos(math.radians(dec)) * math.cos(math.radians(ra)); vy += math.cos(math.radians(dec)) * math.sin(math.radians(ra)); vz += math.sin(math.radians(dec))
    return math.degrees(math.atan2(vy, vx)) % 360, math.degrees(math.atan2(vz, math.hypot(vx, vy)))


def star_js():
    st = [[round(STARS26[i][0], 4), round(STARS26[i][1], 4), s[3], s[4], s[5], s[6]] for i, s in enumerate(STAR_DATA)]
    co = [[c[0], [[KEY[k] for k in ln] for ln in c[1]], KEY[c[2]]] for c in CONS_DATA]
    asr = [[a[0], [KEY[k] for k in a[1]], a[2], [KEY[k] for k in a[3]]] for a in ASTER_DATA]
    orb = []
    for nm, sea in ORB_DATA:
        c = next(cc for cc in CONS_DATA if cc[0] == nm)
        keys = sorted({k for ln in c[1] for k in ln})
        ra, dec = centroid(keys)
        orb.append([[cc[0] for cc in CONS_DATA].index(nm), sea, round(ecl_lon(ra, dec), 1)])
    dump = lambda v: json.dumps(v, ensure_ascii=False, separators=(",", ":"))
    return dump(st), dump(co), dump(asr), dump(orb)


ST_JS, CO_JS, AS_JS, ORB_JS = star_js()
SEL_OPTS = [(str(KEY[k]), STAR_DATA[KEY[k]][5] + "（" + next(c[0] for c in CONS_DATA if any(k in ln for ln in c[1]) or c[2] == k).replace("（おおぐま座）", "") + "）") for k in SEL_DATA]

# ============================================================ 共通（描画の小道具）
UI_COMMON = r'''
  const F=(s,b)=>(b?'bold ':'')+s+'px system-ui,-apple-system,"Hiragino Sans","Noto Sans JP",sans-serif';
  function lerp(c1,c2,f){ const q=(s)=>[1,3,5].map(i=>parseInt(s.slice(i,i+2),16)); const a=q(c1), b=q(c2); return 'rgb('+a.map((v,i)=>Math.round(v+(b[i]-v)*f)).join(',')+')'; }
  function skyCols(s){ if(s>=8) return ['#5aa7e6','#d6ecfa']; if(s<=-12) return ['#060b1c','#17213b'];
    if(s>=0){ const f=s/8; return [lerp('#3a64a0','#5aa7e6',f), lerp('#f0b27c','#d6ecfa',f)]; }
    const f=(s+12)/12; return [lerp('#060b1c','#3a64a0',f), lerp('#17213b','#f0b27c',f)]; }
  function rr(a,b,w,h,r){ x.beginPath(); x.moveTo(a+r,b); x.arcTo(a+w,b,a+w,b+h,r); x.arcTo(a+w,b+h,a,b+h,r); x.arcTo(a,b+h,a,b,r); x.arcTo(a,b,a+w,b,r); x.closePath(); }
  function halo(t,px,py,col,dark,al){ x.textAlign=al||'center'; x.textBaseline='middle'; x.lineJoin='round'; x.lineWidth=3; x.strokeStyle=dark?'rgba(8,12,26,.88)':'rgba(255,255,255,.92)'; x.strokeText(t,px,py); x.fillStyle=col; x.fillText(t,px,py); }
  function hm(h){ let m=Math.round(wrap(h,24)*60); if(m>=1440) m-=1440; return Math.floor(m/60)+':'+String(m%60).padStart(2,'0'); }
  function arrowHead(px,py,ang,sz){ x.beginPath(); x.moveTo(px+Math.cos(ang)*sz,py+Math.sin(ang)*sz); x.lineTo(px+Math.cos(ang+2.5)*sz,py+Math.sin(ang+2.5)*sz); x.lineTo(px+Math.cos(ang-2.5)*sz,py+Math.sin(ang-2.5)*sz); x.closePath(); x.fill(); }
  function setBtn(id,on){ const b=$(id); if(!b) return; b.style.background=on?'var(--teal-l)':''; b.style.borderColor=on?'var(--teal)':''; b.style.color=on?'var(--teal-d)':''; b.style.fontWeight=on?'800':''; }
  function fit(id,v){ setStat(id,v); const e=$(id); if(e) e.style.fontSize=v.length>9?'14px':v.length>6?'16px':''; }
'''

# ============================================================ 1 太陽の1日の動きと季節
CORE1 = r'''
  const R=Math.PI/180, EPS=23.4, H0=-0.8333, ML=[31,28,31,30,31,30,31,31,30,31,30,31];
  const LOC={tokyo:{n:'東京',lat:35.6581,lon:139.7414}, sapporo:{n:'札幌',lat:43.0667,lon:141.35}, naha:{n:'那覇',lat:26.2167,lon:127.6667},
             equator:{n:'赤道',lat:0,lon:135}, pole:{n:'北極',lat:89.999,lon:135}};
  const SEAS=[[79,'春分'],[172,'夏至'],[266,'秋分'],[356,'冬至']], ANC=[[79.5,0],[172.5,90],[266.5,180],[356.5,270],[444.5,360]];
  const wrap=(v,m)=>((v%m)+m)%m;
  function md(n){ let m=0; while(m<11&&n>ML[m]){ n-=ML[m]; m++; } return [m+1,n]; }
  function lamOf(t){ if(t<ANC[0][0]) t+=365; for(let i=0;i<4;i++){ const a=ANC[i], b=ANC[i+1]; if(t<=b[0]) return a[1]+(b[1]-a[1])*(t-a[0])/(b[0]-a[0]); } return 0; }
  function decOf(n){ return Math.asin(Math.sin(EPS*R)*Math.sin(lamOf(n+0.5)*R))/R; }   // その日の太陽の赤緯（正午）
  function eotOf(n){ const d=Date.UTC(2026,0,n,3)/864e5+2440587.5-2451545, g=(357.529+0.98560028*d)*R, q=280.459+0.98564736*d;   // 均時差（度）
    const L=(q+1.915*Math.sin(g)+0.020*Math.sin(2*g))*R, e=(23.439-0.00000036*d)*R;
    return wrap(q-Math.atan2(Math.cos(e)*Math.sin(L),Math.cos(L))/R+180,360)-180; }
  function sunDay(n,p){ const d=decOf(n), E=eotOf(n), noon=12-(p.lon-135)/15-E/15, sl=Math.sin(p.lat*R), cl=Math.cos(p.lat*R), sd=Math.sin(d*R), cd=Math.cos(d*R);
    const c=(Math.sin(H0*R)-sl*sd)/(cl*cd), h0=c<=-1?180:c>=1?0:Math.acos(c)/R;
    let top=90-p.lat+d, north=false; if(top>90){ top=180-top; north=true; }
    const s=sd/cl;
    return {d:d, noon:noon, len:2*h0/15, rise:noon-h0/15, set:noon+h0/15, kind:c<=-1?'白夜':c>=1?'極夜':'', top:top, north:north, shift:Math.abs(s)<1?Math.asin(s)/R:null}; }
  function sunAt(n,p,t){ const d=decOf(n)*R, Hd=15*(t-12)+(p.lon-135)+eotOf(n), Hr=Hd*R, la=p.lat*R;   // 高度・方位（南から西回り）・時角
    const h=Math.asin(Math.sin(la)*Math.sin(d)+Math.cos(la)*Math.cos(d)*Math.cos(Hr));
    return [h/R, Math.atan2(Math.sin(Hr),Math.cos(Hr)*Math.sin(la)-Math.tan(d)*Math.cos(la))/R, Hd]; }
'''

JS1 = r'''
  const cv=$('cv'); const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const x=cv.getContext('2d'); x.setTransform(dpr,0,0,dpr,0,0);
  cv.style.cursor='pointer';
%%CORE%%
%%UI%%
  const LW=392, CX=194, CY=222, RD=152, CP=Math.cos(28*R), SP=Math.sin(28*R), SL=Math.sin(24*R), CL=Math.cos(24*R), STK=0.2;
  const EX=518, EY=118, ER=52, GX0=414, GX1=628, GA0=250, GA1=294, GB0=322, GB1=366;
  const P3=(e,n,z)=>[CX+(e*CP+n*SP)*RD, CY-((n*CP-e*SP)*SL+z*CL)*RD];   // ななめ上（南南東）から見た図：東が右手前
  function V(h,A,k){ const c=Math.cos(h*R)*k; return [-Math.sin(A*R)*c,-Math.cos(A*R)*c,Math.sin(h*R)*k]; }   // 東・北・上
  const PS=(h,A,k)=>{ const v=V(h,A,k||1); return P3(v[0],v[1],v[2]); };
  const td=new Date();
  let n0=clamp(Math.round((Date.UTC(2026,td.getMonth(),td.getDate())-Date.UTC(2026,0,1))/864e5)+1,1,365);
  let hour=+$('hour').value, p=LOC[$('loc').value]||LOC.tokyo, play=false, last=0, need=true, drag=null, d0=null, yd=null;
  function dur(h){ const m=Math.round(h*60); return Math.floor(m/60)+'時間'+String(m%60).padStart(2,'0')+'分'; }
  const D8=['南','南西','西','北西','北','北東','東','南東'], dir8=(A)=>D8[Math.round(wrap(A,360)/45)%8];
  const seasonOf=(n)=>{ const s=SEAS.find(q=>q[0]===n); return s?s[1]:''; };
  const dateTxt=(n)=>{ const q=md(n), s=seasonOf(n); return q[0]+'月'+q[1]+'日'+(s?'（'+s+'）':''); };
  const latTxt=()=>{ const v=Math.round(Math.min(90,p.lat)*10)/10; return v===0?'0':v===90?'90':v.toFixed(1); };
  function yearData(){ const a=[], b=[]; for(let i=1;i<=365;i++){ const s=sunDay(i,p); a.push(s.top); b.push(s.len); } yd=[a,b]; }
  function segs(n){ const out=[]; let cur=null, pv=null;   // 地平線より上の通り道（5分ごと）
    for(let i=0;i<=288;i++){ const t=i/12, sv=sunAt(n,p,t);
      if(sv[0]>=0){ if(!cur){ cur=[]; if(pv){ const f=pv[0]/(pv[0]-sv[0]), q=sunAt(n,p,t-(1-f)/12); cur.push(PS(0,q[1])); } } cur.push(PS(sv[0],sv[1])); }
      else if(cur){ const f=pv[0]/(pv[0]-sv[0]), q=sunAt(n,p,t-(1-f)/12); cur.push(PS(0,q[1])); out.push(cur); cur=null; }
      pv=sv; }
    if(cur) out.push(cur); return out; }
  function strokeSegs(ss){ ss.forEach(sg=>{ x.beginPath(); sg.forEach((q,i)=>i?x.lineTo(q[0],q[1]):x.moveTo(q[0],q[1])); x.stroke(); }); }
  function shiftTxt(s){ if(s.shift===null) return s.kind==='極夜'?'のぼらない':'しずまない'; const a=Math.round(Math.abs(s.shift)); return a===0?'真東・真西':(s.shift>0?'北':'南')+'寄り'+a+'°'; }
  function topTxt(s){ return s.top<=0.05?'のぼらない':s.top.toFixed(1)+'°'+(s.north?'（北）':''); }
  function formula(s){ const sea=seasonOf(n0), L=latTxt()+'°'; let f='90° − '+L;
    if(sea==='夏至') f+=' ＋ 23.4°'; else if(sea==='冬至') f+=' − 23.4°'; else if(!sea) f+=(s.d>=0?' ＋ ':' − ')+Math.abs(s.d).toFixed(1)+'°';
    return f; }
  function infoLines(s,now){ const L=[], sea=seasonOf(n0), f=formula(s);
    if(p.lat>89) L.push(s.top<=0.05?'太陽は1日中のぼらない（極夜）：'+f+' ＝ '+s.top.toFixed(1)+'°':'太陽の高さ '+s.top.toFixed(1)+'°（1日中ほぼ同じ）＝ '+f);
    else if(s.north) L.push('南中高度 '+s.top.toFixed(1)+'°（北の空）'+(sea?'＝':'≒')+' 180° −（'+f+'）');
    else L.push('南中高度 '+s.top.toFixed(1)+'° '+(sea?'＝':'≒')+' '+f+(sea?'':'（この日のずれ）'));
    L.push(s.kind?('1日中'+(s.kind==='白夜'?'しずまない（白夜）':'のぼらない（極夜）')+'　昼の長さ '+dur(s.len)):('南中 '+hm(s.noon)+'　日の出 '+hm(s.rise)+'　日の入り '+hm(s.set)+'　昼 '+dur(s.len)));
    if(s.shift!==null){ const a=Math.round(Math.abs(s.shift)); L.push('日の出・日の入りの方位：'+(a===0?'真東・真西':'真東・真西から'+(s.shift>0?'北':'南')+'へ'+a+'°')); }
    else L.push('日の出・日の入り：なし（太陽は地平線と平行に1日1周）');
    if(now[0]>0.3){ const k=1/Math.tan(now[0]*R), kt='影は棒の'+(k<10?k.toFixed(2)+'倍':'10倍以上');
      L.push('いま '+hm(hour)+'：高度 '+Math.round(now[0])+'°'+(p.lat>89?'　'+kt+'（北極ではどの向きも南）':'（'+dir8(now[1])+'）　'+kt+'（'+dir8(now[1]+180)+'向き）')); }
    else L.push('いま '+hm(hour)+'：太陽は地平線の下（影はできない）');
    return L; }
  function drawDome(s,now){
    const sAlt=now[0], dk=sAlt<-3, ink=dk?'226,232,240':'30,41,59';
    const cols=skyCols(sAlt), g=x.createLinearGradient(0,0,0,H); g.addColorStop(0,cols[0]); g.addColorStop(1,cols[1]); x.fillStyle=g; x.fillRect(0,0,LW,H);
    // 台紙（地平面）と東西・南北の線
    x.fillStyle=dk?'#2a3247':'#f2eee2'; x.beginPath(); x.ellipse(CX,CY,RD,RD*SL,0,0,2*Math.PI); x.fill(); x.strokeStyle='rgba('+ink+',.55)'; x.lineWidth=1.2; x.stroke();
    x.setLineDash([4,4]); x.strokeStyle='rgba('+ink+',.35)'; x.beginPath();
    let a=P3(1,0,0), b=P3(-1,0,0); x.moveTo(a[0],a[1]); x.lineTo(b[0],b[1]); a=P3(0,1,0); b=P3(0,-1,0); x.moveTo(a[0],a[1]); x.lineTo(b[0],b[1]); x.stroke(); x.setLineDash([]);
    // 透明半球と子午線（北—天頂—南）
    x.fillStyle=dk?'rgba(255,255,255,.05)':'rgba(255,255,255,.3)'; x.beginPath(); x.arc(CX,CY,RD,Math.PI,2*Math.PI); x.closePath(); x.fill();
    x.setLineDash([2,5]); x.strokeStyle='rgba('+ink+',.3)'; x.lineWidth=1; x.beginPath();
    for(let i=0;i<=36;i++){ const t=i*5, q=t<=90?PS(t,0):PS(180-t,180); i?x.lineTo(q[0],q[1]):x.moveTo(q[0],q[1]); } x.stroke(); x.setLineDash([]);
    x.strokeStyle=dk?'rgba(255,255,255,.6)':'rgba(30,64,110,.6)'; x.lineWidth=1.6; x.beginPath(); x.arc(CX,CY,RD,Math.PI,2*Math.PI); x.stroke();
    // 夏至・春分秋分・冬至の通り道（比べる用）
    x.setLineDash([5,4]); x.lineWidth=1.4; x.font=F(10.5,1);
    [[172,'夏至'],[79,'春分・秋分'],[356,'冬至']].forEach(r=>{ if(Math.abs(decOf(r[0])-s.d)<0.05) return; const sd=sunDay(r[0],p);
      x.strokeStyle='rgba('+ink+',.45)'; strokeSegs(segs(r[0]));
      if(sd.top>2){ const q=PS(sd.top,sd.north?180:0); x.setLineDash([]); halo(r[1],q[0]+6,q[1]-8,'rgba('+ink+',.95)',dk,'left'); x.setLineDash([5,4]); } });
    x.setLineDash([]);
    // 選んだ日の通り道と1時間ごとの印
    const ss=segs(n0); x.lineCap='round'; x.strokeStyle=dk?'rgba(0,0,0,.35)':'rgba(255,255,255,.8)'; x.lineWidth=6.5; strokeSegs(ss); x.strokeStyle='#f97316'; x.lineWidth=3.2; strokeSegs(ss); x.lineCap='butt';
    x.font=F(10.5,1); const DP=[[1,0],[-1,0],[0,-1],[0,1]].map(d=>P3(d[0]*1.13,d[1]*1.13,0));
    for(let k=0;k<24;k++){ const sv=sunAt(n0,p,k); if(sv[0]<0.5) continue; const q=PS(sv[0],sv[1]);
      x.fillStyle='#fff'; x.strokeStyle='#c2410c'; x.lineWidth=1.5; x.beginPath(); x.arc(q[0],q[1],3.4,0,2*Math.PI); x.fill(); x.stroke();
      if(k%3===0){ const dx=q[0]-CX, dy=q[1]-(CY-30), l=Math.hypot(dx,dy)||1, lx=q[0]+dx/l*16, ly=q[1]+dy/l*13;
        if(DP.every(d=>Math.hypot(d[0]-lx,d[1]-ly)>24)) halo(k+'時',lx,ly,dk?'#fed7aa':'#9a3412',dk); } }
    // 日の出・日の入りの位置（ふちの三角）
    if(s.shift!==null){ x.fillStyle='#ea580c'; [-90-s.shift,90+s.shift].forEach(A=>{ const q=PS(0,A), o=PS(0,A,1.07); arrowHead(q[0],q[1],Math.atan2(q[1]-o[1],q[0]-o[0]),6); }); }
    // 南中高度（中心Oから見た角度）
    const O=P3(0,0,0), Tp=P3(0,0,STK);
    if(s.top>0.5){ const A0=s.north?180:0, C=PS(s.top,A0), B=PS(0,A0);
      x.strokeStyle='#dc2626'; x.lineWidth=1.6; x.setLineDash([5,3]); x.beginPath(); x.moveTo(O[0],O[1]); x.lineTo(B[0],B[1]); x.moveTo(O[0],O[1]); x.lineTo(C[0],C[1]); x.stroke(); x.setLineDash([]);
      x.lineWidth=2.4; x.beginPath(); for(let i=0;i<=24;i++){ const q=PS(s.top*i/24,A0,0.3); i?x.lineTo(q[0],q[1]):x.moveTo(q[0],q[1]); } x.stroke();
      const q=PS(s.top*0.55,A0,0.3); x.font=F(11.5,1); const t=(p.lat>89?'太陽の高さ ':'南中高度 ')+s.top.toFixed(1)+'°', w=x.measureText(t).width;
      x.fillStyle=dk?'rgba(8,12,26,.8)':'rgba(255,255,255,.9)'; rr(q[0]-w-16,q[1]-9,w+8,18,5); x.fill(); x.fillStyle='#dc2626'; x.textAlign='left'; x.textBaseline='middle'; x.fillText(t,q[0]-w-12,q[1]+0.5); }
    // 棒と影
    if(sAlt>0.3){ const L=STK/Math.tan(sAlt*R), Lc=Math.min(L,1), sp=P3(Math.sin(now[1]*R)*Lc,Math.cos(now[1]*R)*Lc,0);
      x.strokeStyle=dk?'rgba(0,0,0,.55)':'rgba(30,41,59,.72)'; x.lineWidth=5; x.lineCap='round'; x.beginPath(); x.moveTo(O[0],O[1]); x.lineTo(sp[0],sp[1]); x.stroke(); x.lineCap='butt';
    }
    x.strokeStyle='#92400e'; x.lineWidth=4; x.beginPath(); x.moveTo(O[0],O[1]); x.lineTo(Tp[0],Tp[1]); x.stroke();
    x.fillStyle='#ef4444'; x.beginPath(); x.arc(O[0],O[1],3,0,2*Math.PI); x.fill();
    // 太陽（中心Oへの光の線）
    if(sAlt>-0.5){ const q=PS(Math.max(0,sAlt),now[1]);
      x.setLineDash([3,4]); x.strokeStyle='rgba(234,179,8,.95)'; x.lineWidth=1.6; x.beginPath(); x.moveTo(q[0],q[1]); x.lineTo(O[0],O[1]); x.stroke(); x.setLineDash([]);
      const gl=x.createRadialGradient(q[0],q[1],4,q[0],q[1],26); gl.addColorStop(0,'rgba(255,236,150,.95)'); gl.addColorStop(1,'rgba(255,236,150,0)'); x.fillStyle=gl; x.beginPath(); x.arc(q[0],q[1],26,0,2*Math.PI); x.fill();
      x.fillStyle='#fde047'; x.strokeStyle='#f59e0b'; x.lineWidth=2; x.beginPath(); x.arc(q[0],q[1],10,0,2*Math.PI); x.fill(); x.stroke(); }
    drawShadowTop(now,dk);
    // 方位
    x.font=F(14,1); [['東',1,0],['西',-1,0],['南',0,-1],['北',0,1]].forEach(d=>{ const q=P3(d[1]*1.13,d[2]*1.13,0); halo(d[0],q[0],q[1]+(d[2]<0?6:0),dk?'#fff':'#0f172a',dk); });
    // 見出し
    x.fillStyle='rgba(6,11,28,.66)'; rr(6,6,272,42,8); x.fill();
    x.textAlign='left'; x.textBaseline='alphabetic'; x.fillStyle='#fff'; x.font=F(13,1); x.fillText('透明半球（ななめ上から見た図）',14,23);
    x.fillStyle='#fde68a'; x.font=F(12,1); x.fillText(p.n+'（北緯'+latTxt()+'°）　'+dateTxt(n0)+'　'+hm(hour),14,40);
    // 数値
    const ls=infoLines(s,now); x.fillStyle='rgba(6,11,28,.74)'; rr(6,H-98,LW-12,92,8); x.fill();
    ls.forEach((l,i)=>{ x.font=F(i===0?12:11.5,i===0); x.fillStyle=i===0?'#fde68a':'#e2e8f0'; x.textAlign='left'; x.textBaseline='alphabetic'; x.fillText(l,14,H-78+i*20); });
  }
  function drawShadowTop(now,dk){   // 上から見た影（北が上）
    const bx=290, by=6, ICX=339, ICY=66, IR=31, SH=9;
    x.fillStyle='rgba(6,11,28,.66)'; rr(bx,by,98,108,8); x.fill();
    x.textAlign='center'; x.textBaseline='alphabetic'; x.fillStyle='#fff'; x.font=F(11,1); x.fillText('上から見た影',bx+49,by+15);
    x.fillStyle=dk?'#2a3247':'#f2eee2'; x.beginPath(); x.arc(ICX,ICY,IR,0,2*Math.PI); x.fill();
    x.strokeStyle='rgba(30,41,59,.35)'; x.lineWidth=1; x.setLineDash([2,3]); x.beginPath(); x.moveTo(ICX-IR,ICY); x.lineTo(ICX+IR,ICY); x.moveTo(ICX,ICY-IR); x.lineTo(ICX,ICY+IR); x.stroke(); x.setLineDash([]);
    x.font=F(10,1); x.fillStyle='#e2e8f0'; x.textBaseline='middle'; x.fillText('北',ICX,ICY-IR-6); x.fillText('南',ICX,ICY+IR+7); x.fillText('東',ICX+IR+7,ICY); x.fillText('西',ICX-IR-7,ICY);
    const tip=(h,A)=>{ const L=Math.min(SH/Math.tan(h*R),IR); return [ICX+Math.sin(A*R)*L, ICY-Math.cos(A*R)*L]; };
    const pts=[]; for(let k=0;k<24;k++){ const sv=sunAt(n0,p,k); if(sv[0]>4) pts.push([k,tip(sv[0],sv[1])]); }
    x.strokeStyle='rgba(100,116,139,.8)'; x.lineWidth=1; x.beginPath(); pts.forEach((q,i)=>i?x.lineTo(q[1][0],q[1][1]):x.moveTo(q[1][0],q[1][1])); x.stroke();
    pts.forEach(q=>{ x.fillStyle='#64748b'; x.beginPath(); x.arc(q[1][0],q[1][1],1.8,0,2*Math.PI); x.fill(); });
    if(now[0]>0.3){ const t=tip(now[0],now[1]); x.strokeStyle='#1e293b'; x.lineWidth=3.5; x.lineCap='round'; x.beginPath(); x.moveTo(ICX,ICY); x.lineTo(t[0],t[1]); x.stroke(); x.lineCap='butt';
      const sx=ICX-Math.sin(now[1]*R)*IR, sy=ICY+Math.cos(now[1]*R)*IR; x.fillStyle='#fde047'; x.strokeStyle='#f59e0b'; x.lineWidth=1.5; x.beginPath(); x.arc(sx,sy,5,0,2*Math.PI); x.fill(); x.stroke(); }
    x.fillStyle='#92400e'; x.beginPath(); x.arc(ICX,ICY,2.6,0,2*Math.PI); x.fill();
  }
  function drawEarth(s,now){
    x.fillStyle='#0b1020'; x.fillRect(LW+2,0,W-LW-2,H);
    const lam=lamOf(n0+0.5)*R, e=EPS*R, kp=40*R, cl=Math.cos(lam), sl=Math.sin(lam);
    const S3=[cl,sl,0], T3=[-sl,cl,0], rv=[-cl,-sl,0], uv=[-Math.sin(kp)*T3[0],-Math.sin(kp)*T3[1],Math.cos(kp)], vv=[Math.cos(kp)*T3[0],Math.cos(kp)*T3[1],Math.sin(kp)];
    const dot=(a,b)=>a[0]*b[0]+a[1]*b[1]+a[2]*b[2];
    const pr=(q,r)=>[EX+(r||ER)*dot(q,rv), EY-(r||ER)*dot(q,uv)];
    const ec=(a,b,c)=>[a, b*Math.cos(e)+c*Math.sin(e), -b*Math.sin(e)+c*Math.cos(e)];
    const ra=Math.atan2(Math.cos(e)*sl,cl);
    const site=(la,Hd)=>{ const t=ra+Hd*R, c=Math.cos(la*R); return ec(c*Math.cos(t),c*Math.sin(t),Math.sin(la*R)); };
    x.textAlign='left'; x.textBaseline='alphabetic'; x.fillStyle='#fff'; x.font=F(13,1); x.fillText('宇宙から見た地球',LW+12,20);
    x.font=F(10.5); x.fillStyle='rgba(203,213,225,.85)'; x.fillText('地軸は公転面に垂直な向きから23.4°',LW+12,36);
    // 太陽の光
    x.strokeStyle='rgba(253,224,71,.75)'; x.fillStyle='rgba(253,224,71,.75)'; x.lineWidth=1.5;
    [-34,-11,12,35].forEach(dy=>{ const y=EY+dy; x.beginPath(); x.moveTo(LW+10,y); x.lineTo(EX-ER-14,y); x.stroke(); arrowHead(EX-ER-12,y,0,5); });
    x.font=F(10.5,1); x.fillStyle='#fde68a'; x.fillText('太陽の光',LW+10,EY-44);
    // 地球（左半分が昼）
    x.fillStyle='#173153'; x.beginPath(); x.arc(EX,EY,ER,0,2*Math.PI); x.fill();
    x.fillStyle='#3d8bd0'; x.beginPath(); x.arc(EX,EY,ER,Math.PI/2,3*Math.PI/2); x.closePath(); x.fill();
    x.strokeStyle='rgba(255,255,255,.35)'; x.lineWidth=1; x.beginPath(); x.arc(EX,EY,ER,0,2*Math.PI); x.stroke();
    // 赤道（点線）と、選んだ地点の緯線（昼の側は黄色）
    const ringPts=(la)=>{ const o=[]; for(let i=0;i<=120;i++){ const h=-180+i*3, q=site(la,h); o.push([pr(q),dot(q,vv)>=0,dot(q,S3)>Math.sin(H0*R)]); } return o; };
    const eqp=ringPts(0); x.lineWidth=1; for(let i=0;i<120;i++){ const a=eqp[i], b=eqp[i+1]; if(!a[1]) continue; x.strokeStyle='rgba(255,255,255,.45)'; x.setLineDash([3,3]); x.beginPath(); x.moveTo(a[0][0],a[0][1]); x.lineTo(b[0][0],b[0][1]); x.stroke(); } x.setLineDash([]);
    if(p.lat<89){ const rp=ringPts(p.lat);
      for(let i=0;i<120;i++){ const a=rp[i], b=rp[i+1]; x.strokeStyle=a[2]?'#facc15':'#64748b'; x.lineWidth=a[1]?2.6:1.2; x.globalAlpha=a[1]?1:0.45; x.beginPath(); x.moveTo(a[0][0],a[0][1]); x.lineTo(b[0][0],b[0][1]); x.stroke(); }
      x.globalAlpha=1;
      for(let h=0;h<360;h+=15){ const q=site(p.lat,h), P=pr(q), fr=dot(q,vv)>=0, dy=dot(q,S3)>Math.sin(H0*R); x.fillStyle=dy?'#fef08a':'#94a3b8'; x.globalAlpha=fr?1:0.4; x.beginPath(); x.arc(P[0],P[1],fr?2.3:1.6,0,2*Math.PI); x.fill(); }
      x.globalAlpha=1; }
    // 地軸
    const N3=ec(0,0,1), nb=pr(N3), nt=pr(N3,ER*1.36), sb=pr([-N3[0],-N3[1],-N3[2]]), st=pr([-N3[0],-N3[1],-N3[2]],ER*1.3);
    x.strokeStyle='#e2e8f0'; x.lineWidth=2; x.beginPath(); x.moveTo(nb[0],nb[1]); x.lineTo(nt[0],nt[1]); x.moveTo(sb[0],sb[1]); x.lineTo(st[0],st[1]); x.stroke();
    x.setLineDash([3,3]); x.strokeStyle='rgba(203,213,225,.5)'; x.lineWidth=1; x.beginPath(); x.moveTo(EX,EY-ER-2); x.lineTo(EX,EY-ER*1.42); x.stroke(); x.setLineDash([]);
    x.font=F(11,1); x.fillStyle='#fff'; x.textAlign=nt[0]<EX?'right':'left'; x.fillText('北極',nt[0]+(nt[0]<EX?-4:4),nt[1]+2);
    x.font=F(10.5); x.fillStyle='#fde68a'; x.textAlign=st[0]<EX?'right':'left'; x.fillText('地軸',st[0]+(st[0]<EX?-5:5),st[1]+2);
    // 地点（いま）
    if(p.lat<89){ const q=site(p.lat,now[2]), P=pr(q), fr=dot(q,vv)>=0;
      x.fillStyle=fr?'#ef4444':'rgba(239,68,68,.45)'; x.strokeStyle='#fff'; x.lineWidth=1.5; x.beginPath(); x.arc(P[0],P[1],4.6,0,2*Math.PI); x.fill(); if(fr) x.stroke();
      x.font=F(10.5,1); halo(p.n,P[0],P[1]-11,'#fff',true); }
    else { x.fillStyle='#ef4444'; x.beginPath(); x.arc(nb[0],nb[1],4.6,0,2*Math.PI); x.fill(); }
    x.font=F(12,1); x.fillStyle='#bfdbfe'; x.textAlign='center'; x.fillText('昼',EX-24,EY+38); x.fillStyle='#94a3b8'; x.fillText('夜',EX+24,EY+38);
    x.font=F(10); x.fillStyle='rgba(203,213,225,.85)'; x.textAlign='left'; x.fillText('黄色の点＝昼の側の1時間ごとの位置',LW+12,EY+ER+40);
  }
  const gx=(n)=>GX0+(n-1)/364*(GX1-GX0);
  function drawGraph(s){
    x.strokeStyle='rgba(255,255,255,.14)'; x.lineWidth=1; x.beginPath(); x.moveTo(LW+8,EY+ER+50); x.lineTo(W-8,EY+ER+50); x.stroke();
    x.textAlign='left'; x.textBaseline='alphabetic'; x.fillStyle='#fff'; x.font=F(12.5,1); x.fillText('1年の変化（'+p.n+'）',LW+12,GA0-26);
    const strip=(y0,y1,arr,max,col,lab,val,mid)=>{
      x.fillStyle='rgba(255,255,255,.05)'; x.fillRect(GX0,y0,GX1-GX0,y1-y0);
      if(mid!==undefined){ const ym=y1-(mid/max)*(y1-y0); x.setLineDash([2,3]); x.strokeStyle='rgba(255,255,255,.25)'; x.beginPath(); x.moveTo(GX0,ym); x.lineTo(GX1,ym); x.stroke(); x.setLineDash([]); }
      SEAS.forEach(q=>{ x.strokeStyle='rgba(255,255,255,.12)'; x.beginPath(); x.moveTo(gx(q[0]),y0); x.lineTo(gx(q[0]),y1); x.stroke(); });
      x.strokeStyle=col; x.lineWidth=2; x.beginPath(); arr.forEach((v,i)=>{ const yy=y1-clamp(v,0,max)/max*(y1-y0), xx=gx(i+1); i?x.lineTo(xx,yy):x.moveTo(xx,yy); }); x.stroke();
      x.font=F(11,1); x.fillStyle=col; x.fillText(lab,GX0,y0-6); x.fillStyle='#fff'; x.textAlign='right'; x.fillText(val,GX1,y0-6); x.textAlign='left';
      const yy=y1-clamp(arr[n0-1],0,max)/max*(y1-y0); x.fillStyle='#fff'; x.beginPath(); x.arc(gx(n0),yy,3.6,0,2*Math.PI); x.fill(); };
    strip(GA0,GA1,yd[0],90,'#fb923c','南中高度（0〜90°）',topTxt(s));
    strip(GB0,GB1,yd[1],24,'#60a5fa','昼の長さ（0〜24時間）',dur(s.len),12);
    x.strokeStyle='rgba(255,255,255,.8)'; x.lineWidth=1.2; x.beginPath(); x.moveTo(gx(n0),GA0); x.lineTo(gx(n0),GB1); x.stroke();
    x.font=F(10.5,1); x.textAlign='center'; SEAS.forEach(q=>{ x.fillStyle=q[0]===n0?'#fde68a':'rgba(203,213,225,.85)'; x.fillText(q[1],gx(q[0]),GB1+15); });
    x.font=F(10); x.fillStyle='rgba(203,213,225,.75)'; x.textAlign='left'; x.fillText('グラフをなぞると日付が変わります',LW+12,H-10);
  }
  function draw(){
    if(!yd) yearData();
    const s=sunDay(n0,p), now=sunAt(n0,p,hour);
    x.clearRect(0,0,W,H); drawDome(s,now); drawEarth(s,now); drawGraph(s);
    x.strokeStyle='rgba(255,255,255,.2)'; x.lineWidth=1; x.beginPath(); x.moveTo(LW+1,0); x.lineTo(LW+1,H); x.stroke();
    fit('sAlt',topTxt(s)); fit('sLen',dur(s.len)); fit('sDir',shiftTxt(s));
    if(now[0]>0.3){ const k=1/Math.tan(now[0]*R); fit('sNow',Math.round(now[0])+'°（影'+(k<10?k.toFixed(2)+'倍':'10倍超')+'）'); } else fit('sNow','地平線の下');
    SEAS.forEach((q,i)=>setBtn('s'+i,q[0]===n0));
    setShare('【太陽の動き】'+p.n+'・'+dateTxt(n0)+'の南中高度は'+topTxt(s)+'、昼の長さは'+dur(s.len)+'。日の出・日の入りの方位は'+shiftTxt(s)+'☀️｜シミュラボ');
  }
  function syncUI(){ $('day').value=String(n0); $('dayL').textContent=dateTxt(n0); $('hour').value=String(Math.round(hour*4)/4); $('hourL').textContent=hm(hour); }
  function stopPlay(){ play=false; $('play').textContent='▶ 1日を再生'; }
  function frame(ts){ const dt=last?Math.min(0.1,(ts-last)/1000):0; last=ts;
    if(play){ hour+=dt*1.2; const s=sunDay(n0,p); if(!s.kind&&hour>s.set+0.6){ hour=Math.min(24,s.set+0.6); stopPlay(); } if(hour>=24) hour-=24; syncUI(); need=true; }
    if(need){ need=false; draw(); }
    requestAnimationFrame(frame); }
  function pos(e){ const q=cpos(cv,e); return [q[0]/dpr,q[1]/dpr]; }
  function nearT(q){ let best=1e9, bt=null; for(let i=0;i<=288;i++){ const t=i/12, sv=sunAt(n0,p,t); if(sv[0]<0) continue; const P=PS(sv[0],sv[1]), d=Math.hypot(P[0]-q[0],P[1]-q[1]); if(d<best){ best=d; bt=t; } } return best<70?bt:null; }
  function mv(q){
    if(drag==='dome'){ const t=nearT(q); if(t!==null) hour=t; }
    else if(drag==='earth'){ hour=wrap(d0[1]+(q[0]-d0[0])/9,24); }
    else if(drag==='graph'){ n0=clamp(Math.round((q[0]-GX0)/(GX1-GX0)*364)+1,1,365); }
    syncUI(); draw(); }
  cv.addEventListener('pointerdown',e=>{ const q=pos(e); drag=q[0]<LW?'dome':q[1]<EY+ER+50?'earth':'graph'; d0=[q[0],hour]; stopPlay(); try{ cv.setPointerCapture(e.pointerId); }catch(_){ } mv(q); });
  cv.addEventListener('pointermove',e=>{ if(drag) mv(pos(e)); });
  ['pointerup','pointercancel'].forEach(nm=>cv.addEventListener(nm,()=>{ drag=null; }));
  $('day').addEventListener('input',()=>{ n0=+$('day').value; syncUI(); draw(); });
  $('hour').addEventListener('input',()=>{ hour=+$('hour').value; if(hour>=24) hour=23.99; stopPlay(); syncUI(); draw(); });
  $('loc').addEventListener('change',()=>{ p=LOC[$('loc').value]||LOC.tokyo; yearData(); draw(); });
  SEAS.forEach((q,i)=>$('s'+i).addEventListener('click',()=>{ n0=q[0]; syncUI(); draw(); }));
  $('play').addEventListener('click',()=>{ if(play){ stopPlay(); return; } const s=sunDay(n0,p); if(!s.kind&&(hour<s.rise-0.6||hour>s.set+0.3)) hour=Math.max(0,s.rise-0.5); play=true; $('play').textContent='⏸ 止める'; });
  syncUI(); draw(); need=false; requestAnimationFrame(frame);
'''

T1_TABLE = T([[NW("札幌（北緯43.1°）"), "46.9°", "70.3°", "23.5°", NW("15時間22分"), NW("9時間00分")],
              [NW("東京（北緯35.7°）"), "54.3°", "77.7°", "30.9°", NW("14時間34分"), NW("9時間45分")],
              [NW("那覇（北緯26.2°）"), "63.8°", "87.2°", "40.4°", NW("13時間47分"), NW("10時間30分")],
              [NW("赤道（北緯0°）"), "90°（真上）", "66.6°（北の空）", "66.6°", NW("12時間07分"), NW("12時間07分")],
              [NW("北極（北緯90°）"), "0°（地平線すれすれ）", "23.4°", "のぼらない", "24時間（白夜）", "0時間（極夜）"]],
             ["地点", "春分・秋分の南中高度", "夏至の南中高度", "冬至の南中高度", "夏至の昼の長さ", "冬至の昼の長さ"])

sim(slug="taiyou-ugoki", cat="rika", emoji="🌞", score=81,
    title="太陽の1日の動きと季節（透明半球・南中高度・昼の長さ）",
    title_tag="南中高度・太陽の動きのシミュレーター｜透明半球で見る季節の変化と南中高度の求め方",
    meta_desc="南中高度の求め方と太陽の1日の動きを、透明半球の図で確かめる無料シミュレーター。日付・時刻・地点を変えると、太陽の通り道・棒の影・南中高度・昼の長さ・日の出の方位が連動し、宇宙から見た地軸の傾きも表示します。小3・中3の理科の授業に。",
    og_title="太陽の1日の動きと季節シミュレーター（透明半球・南中高度・昼の長さ）",
    og_desc="日付と時刻を動かすと、透明半球の太陽の通り道・棒の影・南中高度・昼の長さが連動。夏至と冬至のちがいを地軸の傾きから確かめよう。",
    card_desc="透明半球に太陽の通り道と棒の影。夏至・冬至のボタンで南中高度・昼の長さ・日の出の方位のちがいを比べられる。",
    lead="日付・時刻・地点を変えると、透明半球の太陽の通り道、棒の影、南中高度、昼の長さが連動します。季節による変化が地軸の傾きから起こることも、右の図とグラフで確かめられます。",
    model="小3 太陽と地面の様子／中3 日周運動と自転・年周運動と公転",
    level="小学3年、中学3年",
    unit="小学校 第3学年 B(2)「太陽と地面の様子」／中学校 第2分野（6）地球と宇宙（ア）天体の動きと地球の自転・公転",
    canvas=canvas(640, 420),
    controls=slider("day", "日付", 1, 365, 172, 1) + slider("hour", "時刻（日本時間）", 0, 24, 10, 0.25)
           + select("loc", "地点", [("tokyo", "東京（北緯35.7°）"), ("sapporo", "札幌（北緯43.1°）"), ("naha", "那覇（北緯26.2°）"),
                                    ("equator", "赤道（北緯0°）"), ("pole", "北極（北緯90°）")]),
    buttons=btn("s0", "🌸 春分") + btn("s1", "☀️ 夏至") + btn("s2", "🍁 秋分") + btn("s3", "⛄ 冬至") + btn("play", "▶ 1日を再生", True),
    stats=stats([("sAlt", "南中高度", True), ("sLen", "昼の長さ", False), ("sDir", "日の出・日の入りの方位", False), ("sNow", "いまの高度（影の長さ）", False)]),
    legend="左：透明半球をななめ上（南南東）から見た図。オレンジの線が選んだ日の太陽の通り道、白い点が1時間ごとの位置、点線は夏至・春分秋分・冬至の通り道です。赤い線の角度が南中高度、中心の棒の影は太陽の反対側にできます。右上の小さな図は、真上から見た棒の影（北が上、灰色の点は1時間ごとの影の先）です。右：宇宙から見た地球と、1年の南中高度・昼の長さのグラフ。左の図の通り道、右の地球、グラフを指でなぞっても動かせます。",
    article='''
<h2>このシミュレーションでわかること</h2>
<p>太陽は、東の地平線からのぼり、南の空でいちばん高くなって（南中）、西にしずみます。この1日の動き（日周運動）は、地球が1日に1回、西から東へ自転しているために起こる見かけの動きです。透明半球に1時間ごとに記録すると、印の間隔はどれも同じになり、太陽は1時間に約15°（360°÷24時間）の同じ速さで動いていることがわかります。</p>
<p>また、太陽の通り道は季節によって南北に平行に移り、<b>南中高度・昼の長さ・日の出と日の入りの方位</b>が変わります。これは、地球が地軸を公転面に垂直な方向から23.4°かたむけたまま、太陽のまわりを公転しているためです。</p>
''' + T([[NW("小学校3年"), NW("B(2) 太陽と地面の様子"), "日陰は太陽の光を遮るとでき、日陰の位置は太陽の位置の変化によって変わること（太陽の位置は東から南、西へと変化する）"],
          [NW("中学校3年"), "第2分野（6）地球と宇宙「日周運動と自転」", "天体の日周運動の観察を行い、その観察記録を地球の自転と関連付けて理解すること"],
          [NW("中学校3年"), "第2分野（6）地球と宇宙「年周運動と公転」", "太陽の南中高度の変化などの観察記録を、地球の公転や地軸の傾きと関連付けて理解すること（季節による昼夜の長さや気温の変化にも触れる）"]],
         ["学年", "単元", "学習指導要領（平成29年告示）の内容"]) + '''
<p>中学校の解説（理科編 p.105〜106）は、透明半球を使った太陽の日周運動の観察とあわせて、観察者の視点を地球の外に移して考えるために、コンピュータシミュレーションを用いて視覚的に捉えさせる工夫を例にあげています。学年は一般的な配当です。小学校3年では方位は東・西・南・北を扱い、地球から見た太陽の位置の変化として学習します。</p>

<h2>授業での使い方</h2>
<p><b>導入（小3）</b>：時刻のスライダーを朝から夕方へ動かし、太陽が東→南→西と動くことを確かめます。図の右上の「上から見た影」で、棒の影がいつも太陽の反対側にでき、西→北→東へ動くこと、太陽が高い昼ごろは影が短くなることにも気づかせます。</p>
<p><b>展開（中3・日周運動）</b>：「▶ 1日を再生」で太陽を動かし、透明半球の1時間ごとの印の間隔が同じことから、太陽が一定の速さで動くことを確かめます。右の「宇宙から見た地球」で、観測地点（赤い点）が自転によって昼の側に入ったり出たりすることと、空の太陽の動きを対応させます。</p>
<p><b>展開（中3・年周運動）</b>：「夏至」「冬至」「春分」「秋分」のボタンで通り道を比べ、南中高度・昼の長さ・日の出の方位を表にまとめます。地点を札幌・那覇に変えると、緯度による違いも確かめられます。</p>
<p><b>まとめ</b>：下の「南中高度の求め方」で計算し、シミュレーターの値と照らし合わせます。季節によって気温が変わる理由（太陽の光の当たる角度と昼の長さ）にもふれます。</p>
<p>児童・生徒への問いの例です。</p>
<ul>
<li>（小3）午前10時ごろ、棒の影は東・西・南・北のどちらの側にできるでしょう。（太陽が南東の空にあるので、反対の北西の側）</li>
<li>（中3）夏至の日の昼が冬至の日より長いのはなぜでしょう。右の図で、選んだ地点の緯線のうち昼の側（黄色）にある部分の長さに注目して説明しましょう。</li>
<li>（中3）赤道では、1年中、昼の長さがほぼ12時間なのはなぜでしょう。</li>
</ul>

<h2>しくみ・解説</h2>
<h3>透明半球への記録のしかた</h3>
<p>透明半球は、観測する人を中心にして、空を半球の形で表したもの（天球のモデル）です。台紙に透明半球のふちと同じ大きさの円をかき、中心Oと東西南北の線をかいて、方位を合わせて日の当たる水平な場所に置きます。ペン先の影が中心Oにくる位置に、1時間ごとに印をつけます。印をなめらかな線で結んで透明半球のふちまでのばすと、日の出と日の入りの位置がわかります。</p>
''' + N("太陽を直接見てはいけません。小学校での観察では、しゃ光板（JIS規格のもの）を必ず使います。") + '''
<p>1時間ごとの印の間隔は、どれも同じ長さになります。地球が一定の速さで自転しているからです。</p>
<h3>南中高度の求め方</h3>
<p>南中高度は、太陽が真南にきたとき（南中）の、地平線からの角度です。透明半球では、中心Oから見た「真南の点」と「南中したときの印」の間の角度で、図の赤い線で示しています。北緯◯°の地点では、次の式で求められます。</p>
''' + N("春分・秋分の日：南中高度 ＝ 90° − 緯度<br>夏至の日：南中高度 ＝ 90° − 緯度 ＋ 23.4°<br>冬至の日：南中高度 ＝ 90° − 緯度 − 23.4°") + '''
<p>春分・夏至・秋分・冬至以外の日は、その日の太陽の通り道が、春分・秋分の日の通り道から北や南へずれている角度を足したり引いたりします（図の下の数値の「この日のずれ」。高校では太陽の赤緯といいます）。たとえば東京の10月4日は、通り道が南へ約4.3°ずれているので、90° − 35.7° − 4.3° ≒ 50.0°です。</p>
<p><b>例題1</b>：東京（北緯35.7°）の夏至の日の南中高度は何度ですか。<br>答え：90° − 35.7° ＋ 23.4° ＝ <b>77.7°</b></p>
<p><b>例題2</b>：北緯34.0°の地点の、冬至の日の南中高度は何度ですか。<br>答え：90° − 34.0° − 23.4° ＝ <b>32.6°</b></p>
<p><b>例題3</b>：ある地点で、春分の日の南中高度が50.0°でした。この地点の緯度は何度ですか。<br>答え：90° − 緯度 ＝ 50.0° より、<b>北緯40.0°</b></p>
<p>式の意味：春分・秋分の日には、太陽の光が赤道に真上から当たります。北緯◯°の地点では地面が赤道の地面より◯°かたむいているので、太陽は真上から◯°ずれた高さ（90°−緯度）に見えます。夏至の日は、地軸の北極側が太陽の方へ23.4°かたむいているので、その分だけ高くなります。冬至の日はその反対です。計算した値が90°をこえたら、太陽は北の空で「180° − その値」の高さに南中します（例：赤道の夏至は 90° − 0° ＋ 23.4° ＝ 113.4° → 北の空で66.6°）。</p>
<h3>地点ごとの早見表</h3>
''' + T1_TABLE + '''
<p>南中高度は、地軸の傾き23.4°を使った計算値です。地軸の傾きは正確には23.44°で、国立天文台の暦では、2026年の夏至の日の南中高度は東京77.8°・札幌70.4°です。昼の長さは日の出から日の入りまでの時間で、このシミュレーターの計算値です（2026年）。</p>
<h3>透明半球の記録から時刻を求める</h3>
<p><b>例題4</b>：透明半球で、1時間ごとの印の間隔は2.4cmでした。日の出の位置（透明半球のふち）から午前9時の印までの長さが7.2cmのとき、日の出の時刻は何時ですか。<br>答え：7.2 ÷ 2.4 ＝ 3（時間）なので、9時の3時間前の<b>午前6時</b></p>
<p>日の出から南中までの時間と、南中から日の入りまでの時間はほぼ等しいので、南中時刻は日の出と日の入りのちょうど真ん中の時刻になります。日本の南中時刻が12時ちょうどにならないのは、日本の時刻が東経135°の地点を基準にしているためと、地球の公転の速さが季節で少し変わるためです（2026年の東京では11時25分〜11時55分ごろ）。</p>
<h3>影の向きと長さ</h3>
<p>影は、太陽と反対の側にできます。太陽が東→南→西と動くので、棒の影は西→北→東と動き、南中したとき（正午ごろ）に真北を向いて、いちばん短くなります。太陽が高いほど影は短くなります。</p>
''' + T([["15°", "3.73倍"], ["30°", "1.73倍"], ["45°", "1.00倍"], ["60°", "0.58倍"], ["77.7°（東京の夏至の南中）", "0.22倍"], ["30.9°（東京の冬至の南中）", "1.67倍"]],
        ["太陽の高度", "影の長さ（棒の長さの何倍か）"]) + '''
<p>影の長さは「棒の長さ ÷ tan（太陽の高度）」で求められます（tanは高校の数学で学びます。中学校では、表のように高度が低いほど影が長くなる関係をつかめば十分です）。</p>
<h3>昼の長さと気温が季節で変わるわけ</h3>
<p>右の「宇宙から見た地球」の黄色と灰色の線は、選んだ地点が自転で1日に回る道すじ（緯線）で、点は1時間ごとの位置です。黄色の点（昼の側にある点）の数が、ほぼ昼の長さになります。夏至のころは地軸の北極側が太陽の方へかたむくため、北半球の緯線は昼の側に長く入り、昼が長くなります。冬至のころはその反対です。赤道は、いつも半分が昼の側にあるので、1年中ほぼ12時間です。</p>
<p>太陽の高度が高いほど、同じ面積の地面が受ける光の量が多くなり、昼が長いほど長い時間あたためられます。これが、夏に気温が高くなる主な理由です。</p>
<h3>このシミュレーションで単純化していること</h3>
<ul>
<li>地軸の傾きを教科書と同じ23.4°とし、太陽の通り道は、2026年の春分（3月20日）・夏至（6月21日）・秋分（9月23日）・冬至（12月22日）にちょうど春分の通り道から0°・北へ23.4°・0°・南へ23.4°となるように、その間をなめらかにつないでいます。精密な計算（J. Meeusの式）と比べた2026年1年間の差は、南中高度で0.3°以内です。</li>
<li>1日のあいだは、太陽の通り道は変わらないものとしています。</li>
<li>日の出・日の入りの時刻と昼の長さは、国立天文台と同じく「太陽の上のふちが地平線に接する時刻（大気で光が曲がって浮き上がって見える分を含む）」で計算しています。そのため春分・秋分の日でも、昼の長さは12時間より7〜9分ほど長くなります。透明半球の図と日の出・日の入りの方位は、太陽の中心が地平線にくる位置で表しています。</li>
<li>地点の緯度・経度は国立天文台の暦計算室と同じ値（東京：北緯35.6581°・東経139.7414°、札幌：北緯43.0667°・東経141.35°、那覇：北緯26.2167°・東経127.6667°）です。赤道と北極は東経135°として、時刻は日本時間で表しています。</li>
<li>国立天文台の2026年の暦と比べると、日の出・日の入り・南中の時刻の差は2分以内でした（例：東京の夏至の日は、このシミュレーターで日の出4:26・日の入り19:00、国立天文台は4:25・19:00）。</li>
<li>右の地球の図は、大きさを誇張しています。</li>
</ul>

<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「小学校学習指導要領（平成29年告示）解説 理科編」（''' + A(MEXT_SHO) + '''）</li>
<li>文部科学省「中学校学習指導要領（平成29年告示）解説 理科編」p.104〜106（''' + A(MEXT_CHU) + '''）</li>
<li>国立天文台 暦計算室「日の出入り 東京（2026年6月）」（''' + A("https://eco.mtk.nao.ac.jp/koyomi/dni/2026/s1306.html") + '''）…日の出・日の入り・南中の時刻と南中高度の照合に使用（札幌・那覇、ほかの月も同じページから）</li>
<li>国立天文台「春分の日・秋分の日には、昼と夜の長さは同じになるの？」（''' + A("https://www.nao.ac.jp/faq/a0303.html") + '''）</li>
<li>Jean Meeus『Astronomical Algorithms』第2版（Willmann-Bell, 1998）</li>
</ul>
''',
    faqs=[("南中高度はどうやって求めますか？", "北緯◯°の地点では、春分・秋分の日は「90° − 緯度」、夏至の日は「90° − 緯度 ＋ 23.4°」、冬至の日は「90° − 緯度 − 23.4°」で求められます。東京（北緯35.7°）では、春分・秋分54.3°、夏至77.7°、冬至30.9°です。"),
          ("夏は昼が長く、冬は短いのはなぜですか？", "地球が地軸を23.4°かたむけたまま公転しているからです。夏至のころは北半球が太陽の方へかたむくので、自転で1日に回る道すじのうち昼の側にある部分が長くなり、太陽も高くのぼります。冬至のころはその反対になります。"),
          ("春分の日は、昼と夜の長さが同じですか？", "ほぼ同じですが、昼のほうが少し長くなります。日の出・日の入りは太陽の上のふちが地平線に接する時刻で決めることと、大気で光が曲がって太陽が浮き上がって見えるためです。国立天文台によると、2026年3月20日の東京は日の出5時45分・日の入り17時52分で、昼の長さは12時間7分です。"),
          ("夏至の日、太陽は真東からのぼりますか？", "いいえ。夏至の日は真東より北寄り（東京で約30°）からのぼり、真西より北寄りにしずみます。冬至の日は南寄りです。真東からのぼって真西にしずむのは、春分・秋分の日です。"),
          ("透明半球の1時間ごとの印の間隔が同じになるのはなぜですか？", "地球が一定の速さで自転しているので、太陽も1時間に約15°の同じ速さで動いて見えるからです。印の間隔を使うと、日の出や日の入りの時刻を求めることができます。"),
          ("棒の影の向きは、1日でどう変わりますか？", "影は太陽の反対側にできるので、朝は西側、正午ごろは北側、夕方は東側にでき、西→北→東と動きます。正午ごろ（南中したとき）がいちばん短くなります。")],
    rel=[("hiruma-nagasa", "🌅", "昼の長さメーター"), ("hoshi-ugoki", "⭐", "星の1日・1年の動き（日周運動・年周運動）"),
         ("tsuki-michikake", "🌓", "月の満ち欠けの仕組みシミュレーター"), ("solar-system", "🪐", "太陽系シミュレーター"), ("solar-hatsuden", "🔋", "今日のソーラー発電シミュ")],
    js=JS1.replace("%%CORE%%", CORE1).replace("%%UI%%", UI_COMMON))

# ============================================================ 2 星の1日・1年の動き
CORE2 = r'''
  const R=Math.PI/180, LAT=35.6581, LON=139.7414, SLA=Math.sin(LAT*R), CLA=Math.cos(LAT*R), EPS=23.4366*R;
  const ML=[31,28,31,30,31,30,31,31,30,31,30,31], JD0=Date.UTC(2026,0,1)/864e5+2440587.5;
  const wrap=(v,m)=>((v%m)+m)%m;
  function md(n){ let m=0; while(m<11&&n>ML[m]){ n-=ML[m]; m++; } return [m+1,n]; }
  const jdOf=(n,h)=>JD0+(n-1)+(h-9)/24;   // 2026年の通し日 n・日本時間 h
  const lstOf=(jd)=>wrap(280.46061837+360.98564736629*(jd-2451545)+LON,360);   // 地方恒星時（度）
  function hor(ra,dec,L){ const Hr=(L-ra)*R, d=dec*R, sh=SLA*Math.sin(d)+CLA*Math.cos(d)*Math.cos(Hr);   // 高度・方位（北から東回り）
    return [Math.asin(sh)/R, wrap(Math.atan2(-Math.cos(d)*Math.sin(Hr), Math.sin(d)*CLA-Math.cos(d)*Math.cos(Hr)*SLA)/R,360)]; }
  function sunOf(jd){ const n=jd-2451545, g=(357.529+0.98560028*n)*R, q=280.459+0.98564736*n, L=wrap(q+1.915*Math.sin(g)+0.020*Math.sin(2*g),360), e=(23.439-0.00000036*n)*R;
    return {lam:L, ra:wrap(Math.atan2(Math.cos(e)*Math.sin(L*R),Math.cos(L*R))/R,360), dec:Math.asin(Math.sin(e)*Math.sin(L*R))/R}; }
  const ST=%%ST%%;   // 赤経, 赤緯（2026.5年）, 等級, 色, 名前, 図に名前
  const CO=%%CO%%;   // 星座名, 線, 代表の星
'''

JS2 = r'''
  const cv=$('cv'); const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const x=cv.getContext('2d'); x.setTransform(dpr,0,0,dpr,0,0);
  cv.style.cursor='pointer';
%%CORE%%
%%UI%%
  const AS=%%AS%%, ORB=%%ORB%%;
  const SX=199, SY=235, FL=210, HC=35.66, PW=398, HZ=SY+FL*Math.tan(HC*R);
  const OX=518, OY=210, OR=46, CR=96, TH0=186;
  const VAZ={E:90,S:180,W:270,N:0}, VJ={E:'東',S:'南',W:'西',N:'北'};
  const HINT={E:'星は地平線から右ななめ上へのぼる', S:'星は左（東）から右（西）へ動く', W:'星は右ななめ下へしずむ', N:'北極星を中心に反時計回り'};
  const COL={r:'#ff9a76',o:'#ffc56e',y:'#fff1b8',w:'#ffffff',b:'#cfe1ff'};
  const N8=['北','北東','東','南東','南','南西','西','北西'], dir8=(a)=>N8[Math.round(wrap(a,360)/45)%8];
  const SID=15.0410686;   // 1時間に恒星時が進む角度（度）
  const td=new Date();
  let n0=clamp(Math.round((Date.UTC(2026,td.getMonth(),td.getDate())-Date.UTC(2026,0,1))/864e5)+1,1,365);
  let hour=+$('hour').value, view='S', cam=null, sel=+$('star').value, play=false, last=0, need=true, drag=null, d0=null, trail=null, ghost=0;
  const tAbs=()=>(n0-1)*24+hour, jdT=(T)=>JD0+(T-9)/24;
  function mkCam(az){ const a=az*R, h=HC*R; return {F:[Math.sin(a)*Math.cos(h),Math.cos(a)*Math.cos(h),Math.sin(h)], Rt:[Math.cos(a),-Math.sin(a),0], U:[-Math.sin(h)*Math.sin(a),-Math.sin(h)*Math.cos(a),Math.cos(h)]}; }
  cam=mkCam(VAZ[view]);
  function pj(alt,az){ const ca=Math.cos(alt*R), d0x=ca*Math.sin(az*R), d1=ca*Math.cos(az*R), d2=Math.sin(alt*R), z=d0x*cam.F[0]+d1*cam.F[1]+d2*cam.F[2];   // 透視図（カメラで写した見え方）
    if(z<0.12) return null; return [SX+FL*(d0x*cam.Rt[0]+d1*cam.Rt[1])/z, SY-FL*(d0x*cam.U[0]+d1*cam.U[1]+d2*cam.U[2])/z]; }
  const dateTxt=(n)=>{ const q=md(n); return q[0]+'月'+q[1]+'日'; };
  const word=(h)=>h<4?'真夜中':h<6?'明け方':h<10?'朝':h<14?'昼':h<17?'午後':h<19?'夕方':'夜';
  const ecl=(a)=>wrap(Math.atan2(Math.sin(a*R)*Math.cos(EPS),Math.cos(a*R))/R,360);   // 天の赤道上の点の黄経
  function southCons(L){ const c=[]; CO.forEach(k=>{ const s=ST[k[2]], ha=Math.abs(wrap(L-s[0]+180,360)-180)/15; if(s[1]<LAT-2&&ha<2.2&&hor(s[0],s[1],L)[0]>10) c.push([ha,k[0]]); });   // 天頂より南で南中し、子午線から2.2時間以内
    c.sort((a,b)=>a[0]-b[0]); return c.slice(0,2).map(v=>v[1]); }
  function autoSel(){ const L=lstOf(jdT(tAbs())); let best=-1, bm=99; [...$('star').options].forEach(o=>{ const i=+o.value, s=ST[i], h=hor(s[0],s[1],L); if(h[0]>12&&Math.abs(h[1]-180)<50&&s[2]<bm){ bm=s[2]; best=i; } }); return best>=0?best:+$('star').options[0].value; }
  function nextMonth(n){ const q=md(n), m2=q[0]%12+1; let d=Math.min(q[1],ML[m2-1]), k=d; for(let i=0;i<m2-1;i++) k+=ML[i]; return k; }
  // 公転の図の星座の形（南の空で見た向き・東が左）
  const ICON=ORB.map(o=>{ const c=CO[o[0]], ids=[...new Set(c[1].flat())]; let vx=0,vy=0,vz=0; ids.forEach(i=>{ const s=ST[i]; vx+=Math.cos(s[1]*R)*Math.cos(s[0]*R); vy+=Math.cos(s[1]*R)*Math.sin(s[0]*R); vz+=Math.sin(s[1]*R); });
    const ra=Math.atan2(vy,vx)/R, de=Math.atan2(vz,Math.hypot(vx,vy))/R, pt={}; let mx=1;
    ids.forEach(i=>{ const s=ST[i], u=-(wrap(s[0]-ra+180,360)-180)*Math.cos(de*R), v=s[1]-de; pt[i]=[u,v]; mx=Math.max(mx,Math.abs(u),Math.abs(v)); });
    Object.keys(pt).forEach(i=>{ pt[i]=[pt[i][0]/mx*17,-pt[i][1]/mx*17]; }); return pt; });
  function drawSky(){
    const T=tAbs(), jd=jdT(T), L=lstOf(jd), sn=sunOf(jd), sAlt=hor(sn.ra,sn.dec,L)[0];
    const vis=sAlt<-12?1:sAlt<-6?0.8:sAlt<0?0.5:0.22, dark=sAlt<-3;
    const cols=skyCols(sAlt), g=x.createLinearGradient(0,0,0,HZ); g.addColorStop(0,cols[0]); g.addColorStop(1,cols[1]);
    x.save(); x.beginPath(); x.rect(0,0,PW,HZ); x.clip(); x.fillStyle=g; x.fillRect(0,0,PW,HZ);
    // 高度30°・60°の目安
    x.setLineDash([2,6]); x.strokeStyle=dark?'rgba(148,163,184,.3)':'rgba(30,58,95,.3)'; x.lineWidth=1; x.font=F(10); x.fillStyle=dark?'rgba(148,163,184,.75)':'rgba(30,58,95,.7)';
    [30,60].forEach(a=>{ x.beginPath(); let pen=false, lp=null; for(let k=-70;k<=70;k+=2){ const q=pj(a,VAZ[view]+k); if(q){ pen?x.lineTo(q[0],q[1]):x.moveTo(q[0],q[1]); pen=true; if(q[0]>4&&!lp) lp=q; } else pen=false; } x.stroke(); if(lp){ x.textAlign='left'; x.textBaseline='bottom'; x.fillText('高度'+a+'°',Math.max(4,lp[0]),lp[1]-2); } });
    x.setLineDash([]);
    const P=ST.map(s=>{ const h=hor(s[0],s[1],L); return {h:h, q:h[0]>-3?pj(h[0],h[1]):null}; });
    const line=(ids,PP)=>{ x.beginPath(); let pen=false; ids.forEach(i=>{ const q=PP[i].q; if(q){ pen?x.lineTo(q[0],q[1]):x.moveTo(q[0],q[1]); pen=true; } else pen=false; }); x.stroke(); };
    // 再生中の光跡
    if(trail&&T-trail>0.05){ const t0=Math.max(trail,T-12); x.strokeStyle='rgba(255,255,255,'+(0.35*vis+0.1).toFixed(2)+')'; x.lineWidth=1.2;
      const ts=[]; for(let t=t0;t<T;t+=0.25) ts.push(t); ts.push(T); const Ls=ts.map(t=>lstOf(jdT(t)));
      ST.forEach(s=>{ if(s[2]>3.6) return; x.beginPath(); let pen=false; Ls.forEach(Lt=>{ const h=hor(s[0],s[1],Lt), q=h[0]>-1?pj(h[0],h[1]):null; if(q){ pen?x.lineTo(q[0],q[1]):x.moveTo(q[0],q[1]); pen=true; } else pen=false; }); x.stroke(); }); }
    // 1か月前の同じ時刻（＋1か月を押したとき）
    let GP=null;
    if(ghost){ const Lg=lstOf(jd-ghost); GP=ST.map(s=>{ const h=hor(s[0],s[1],Lg); return {h:h, q:h[0]>-3?pj(h[0],h[1]):null}; });
      x.setLineDash([4,3]); x.strokeStyle='rgba(251,146,60,.8)'; x.lineWidth=1.4; CO.forEach(c=>c[1].forEach(ln=>line(ln,GP))); x.setLineDash([]); }
    // 星の並び（大三角など）
    x.setLineDash([5,5]); x.lineWidth=1.3; x.font=F(11,1);
    AS.forEach(a=>{ x.strokeStyle=a[2]; x.globalAlpha=0.55*vis+0.15; line(a[1],P); x.globalAlpha=1;
      const v=a[3].map(i=>P[i]).filter(o=>o.q&&o.h[0]>0); if(v.length===a[3].length){ const cx=v.reduce((m,o)=>m+o.q[0],0)/v.length, cy=v.reduce((m,o)=>m+o.q[1],0)/v.length; if(cx>30&&cx<PW-30&&cy>70&&cy<HZ-12) halo(a[0],cx,cy,a[2],true); } });
    x.setLineDash([]);
    // 星座線
    x.strokeStyle='rgba(147,197,253,'+(0.5*vis+0.12).toFixed(2)+')'; x.lineWidth=1.2; CO.forEach(c=>c[1].forEach(ln=>line(ln,P)));
    // 選んだ星の1日の道すじ（1時間ごとの点）と、1時間で15°
    const sp=P[sel], ss=ST[sel];
    if(sel!==SELP){ x.setLineDash([3,4]); x.strokeStyle='rgba(250,204,21,.75)'; x.lineWidth=1.4; x.beginPath(); let pen=false;
      for(let k=-72;k<=72;k++){ const h=hor(ss[0],ss[1],L+SID*k/6), q=h[0]>0?pj(h[0],h[1]):null; if(q){ pen?x.lineTo(q[0],q[1]):x.moveTo(q[0],q[1]); pen=true; } else pen=false; } x.stroke(); x.setLineDash([]);
      x.font=F(10,1);
      for(let k=-12;k<=12;k++){ if(!k) continue; const h=hor(ss[0],ss[1],L+SID*k), q=h[0]>0?pj(h[0],h[1]):null; if(!q) continue; x.fillStyle='rgba(250,204,21,.9)'; x.beginPath(); x.arc(q[0],q[1],2.4,0,2*Math.PI); x.fill();
        if(k%2===0) halo(Math.floor(wrap(hour+k,24))+'時',q[0],q[1]+11,'#fde68a',true); }
      const h1=hor(ss[0],ss[1],L-SID), q1=h1[0]>0?pj(h1[0],h1[1]):null;
      if(q1&&sp.q&&sp.h[0]>0){ x.strokeStyle='#facc15'; x.lineWidth=3; x.beginPath(); for(let k=0;k<=12;k++){ const h=hor(ss[0],ss[1],L-SID+SID*k/12), q=pj(h[0],h[1]); if(q) k?x.lineTo(q[0],q[1]):x.moveTo(q[0],q[1]); } x.stroke();
        if(view==='N'&&ss[1]>90-LAT){ const pc=pj(LAT,0); if(pc){ x.setLineDash([2,3]); x.strokeStyle='rgba(250,204,21,.8)'; x.lineWidth=1.2; x.beginPath(); x.moveTo(pc[0],pc[1]); x.lineTo(q1[0],q1[1]); x.moveTo(pc[0],pc[1]); x.lineTo(sp.q[0],sp.q[1]); x.stroke(); x.setLineDash([]); } }
        const hm2=hor(ss[0],ss[1],L-SID/2), qm=pj(hm2[0],hm2[1]); if(qm){ x.font=F(11,1); halo('1時間で15°',qm[0],qm[1]-14,'#fde047',true); } } }
    // 1か月前の位置から矢印
    if(GP&&GP[sel].q&&sp.q&&GP[sel].h[0]>0&&sp.h[0]>0){ const a=GP[sel].q, b=sp.q; x.strokeStyle='#fb923c'; x.fillStyle='#fb923c'; x.lineWidth=2; x.beginPath(); x.moveTo(a[0],a[1]); x.lineTo(b[0],b[1]); x.stroke(); arrowHead(b[0],b[1],Math.atan2(b[1]-a[1],b[0]-a[0]),7);
      x.beginPath(); x.arc(a[0],a[1],4,0,2*Math.PI); x.fill(); x.font=F(11,1); halo('1か月前の同じ時刻',a[0],a[1]+14,'#fdba74',true); }
    // 星
    ST.forEach((s,i)=>{ const o=P[i]; if(!o.q||o.h[0]<0) return; const r=clamp(3.7-0.62*s[2],0.9,4.8); x.globalAlpha=vis; x.fillStyle=COL[s[3]];
      if(r>2.6){ const gl=x.createRadialGradient(o.q[0],o.q[1],r*0.4,o.q[0],o.q[1],r*2.6); gl.addColorStop(0,COL[s[3]]); gl.addColorStop(1,'rgba(255,255,255,0)'); x.fillStyle=gl; x.beginPath(); x.arc(o.q[0],o.q[1],r*2.6,0,2*Math.PI); x.fill(); x.fillStyle=COL[s[3]]; }
      x.beginPath(); x.arc(o.q[0],o.q[1],r,0,2*Math.PI); x.fill(); x.globalAlpha=1; });
    // 名前
    x.font=F(11); CO.forEach(c=>{ const ids=[...new Set(c[1].flat())]; if(!ids.length) return; const v=ids.map(i=>P[i]).filter(o=>o.q&&o.h[0]>2&&o.q[0]>0&&o.q[0]<PW&&o.q[1]>0); if(v.length<2) return;
      const cx=v.reduce((a,o)=>a+o.q[0],0)/v.length, my=Math.max(...v.map(o=>o.q[1])); halo(c[0],clamp(cx,40,PW-40),Math.min(HZ-10,my+15),'rgba(191,219,254,.95)',true); });
    x.font=F(10.5,1); ST.forEach((s,i)=>{ const o=P[i]; if(!s[5]||i===sel||!o.q||o.h[0]<0) return; const rt=o.q[0]+9+x.measureText(s[4]).width>PW-2; halo(s[4],o.q[0]+(rt?-7:7),o.q[1]-8,COL[s[3]],true,rt?'right':'left'); });
    if(sp.q&&sp.h[0]>-0.5){ x.strokeStyle='#facc15'; x.lineWidth=2; x.beginPath(); x.arc(sp.q[0],sp.q[1],9,0,2*Math.PI); x.stroke(); x.font=F(12,1); const rt=sp.q[0]+14+x.measureText(ss[4]).width>PW-2; halo(ss[4],sp.q[0]+(rt?-12:12),sp.q[1]-11,'#fde047',true,rt?'right':'left'); }
    x.restore();
    // 地面と方位
    x.fillStyle=dark?'#0e1712':'#3f5a35'; x.fillRect(0,HZ,PW,H-HZ); x.strokeStyle='rgba(255,255,255,.5)'; x.lineWidth=1.2; x.beginPath(); x.moveTo(0,HZ); x.lineTo(PW,HZ); x.stroke();
    x.font=F(13,1); halo(VJ[view],SX,HZ+17,'#fff',true);
    x.font=F(12,1); halo('← '+dir8(VAZ[view]-90),8,HZ+17,'#cbd5e1',true,'left'); halo(dir8(VAZ[view]+90)+' →',PW-8,HZ+17,'#cbd5e1',true,'right');
    [-45,45].forEach(k=>{ const q=pj(0.01,VAZ[view]+k); if(q&&q[0]>70&&q[0]<PW-70) halo(dir8(VAZ[view]+k),q[0],HZ+17,'#fff',true); });
    // 見えない方向にある選んだ星
    if(!(sp.q&&sp.h[0]>0&&sp.q[0]>0&&sp.q[0]<PW&&sp.q[1]>0&&sp.q[1]<HZ)){ x.font=F(11,1); const t=sp.h[0]>0?ss[4]+'は'+dir8(sp.h[1])+'の空（高度'+Math.round(sp.h[0])+'°）':ss[4]+'はいま地平線の下'; const w=x.measureText(t).width;
      x.fillStyle='rgba(6,11,28,.7)'; rr(PW-w-18,HZ-30,w+12,22,6); x.fill(); x.fillStyle='#fde68a'; x.textAlign='left'; x.textBaseline='middle'; x.fillText(t,PW-w-12,HZ-19); }
    // 見出し
    const cul=(()=>{ if(sel===SELP) return '北極星：ほとんど動かない（高度約'+LAT.toFixed(1)+'°）'; const dh=(wrap(ss[0]-L+180,360)-180)/SID, tc=wrap(hour+dh,24), ha=Math.min(90-LAT+ss[1],90+LAT-ss[1]);
      return ss[4]+'：'+(ss[1]>LAT?'北の空でいちばん高くなる ':'南中 ')+hm(tc)+'（高度'+Math.round(ha)+'°）'; })();
    x.fillStyle='rgba(6,11,28,.66)'; rr(6,6,292,62,8); x.fill();
    x.textAlign='left'; x.textBaseline='alphabetic'; x.fillStyle='#fff'; x.font=F(13,1); x.fillText(VJ[view]+'の空（東京）　'+dateTxt(n0)+' '+hm(hour),14,23);
    x.font=F(11.5,1); x.fillStyle='#93c5fd'; x.fillText(HINT[view]+(sAlt>-3?'（いまは空が明るく見えない）':''),14,41);
    x.fillStyle='#fde68a'; x.fillText(cul,14,59);
    return L; }
  function oxy(lam,r){ const t=(lam+TH0)*R; return [OX+r*Math.cos(t), OY-r*Math.sin(t)]; }
  function drawOrbit(L){
    const jd=jdT(tAbs()), sn=sunOf(jd), sAlt=hor(sn.ra,sn.dec,L)[0], night=sAlt<-6;
    x.fillStyle='#0b1020'; x.fillRect(PW+2,0,W-PW-2,H);
    x.textAlign='left'; x.textBaseline='alphabetic'; x.fillStyle='#fff'; x.font=F(13,1); x.fillText('宇宙から見た公転（北極側から）',PW+12,20);
    x.font=F(10.5); x.fillStyle='rgba(203,213,225,.85)'; x.fillText(night?'黄色の矢印＝いま南に見える方向':'灰色の矢印＝いま南の方向（昼）',PW+12,36);
    const am=ecl(L), le=sn.lam+180;
    // 季節の星座（外側）
    ORB.forEach((o,k)=>{ const c=CO[o[0]], q=oxy(o[2],CR), d=Math.abs(wrap(o[2]-am+180,360)-180), hit=night&&d<40, pt=ICON[k];
      if(hit){ x.fillStyle='rgba(250,204,21,.16)'; x.beginPath(); x.arc(q[0],q[1],25,0,2*Math.PI); x.fill(); }
      x.strokeStyle=hit?'#fde047':'rgba(147,197,253,.7)'; x.lineWidth=hit?1.6:1.1; c[1].forEach(ln=>{ x.beginPath(); ln.forEach((i,j)=>{ const v=pt[i]; j?x.lineTo(q[0]+v[0],q[1]+v[1]):x.moveTo(q[0]+v[0],q[1]+v[1]); }); x.stroke(); });
      x.fillStyle=hit?'#fff':'rgba(226,232,240,.85)'; Object.keys(pt).forEach(i=>{ const v=pt[i]; x.beginPath(); x.arc(q[0]+v[0],q[1]+v[1],ST[i][2]<1.5?2:1.2,0,2*Math.PI); x.fill(); });
      x.font=F(10.5,hit); const ty=q[1]+(q[1]>OY+30?33:q[1]<OY-30?-27:31); halo(c[0]+'（'+o[1]+'）',clamp(q[0],PW+44,W-44),ty,hit?'#fde047':'#bfdbfe',true); });
    // 公転軌道と月
    x.setLineDash([3,4]); x.strokeStyle='rgba(203,213,225,.45)'; x.lineWidth=1; x.beginPath(); x.arc(OX,OY,OR,0,2*Math.PI); x.stroke(); x.setLineDash([]);
    x.font=F(9.5); x.fillStyle='rgba(203,213,225,.75)';
    [1,4,7,10].forEach(m=>{ let k=1; for(let i=0;i<m-1;i++) k+=ML[i]; const lm=sunOf(jdOf(k,0)).lam+180, q=oxy(lm,OR), t=oxy(lm,OR-13); x.beginPath(); x.arc(q[0],q[1],1.8,0,2*Math.PI); x.fill(); halo(m+'月',t[0],t[1],'rgba(203,213,225,.9)',true); });
    const ga=oxy(le+50,OR), gb=oxy(le+62,OR); x.strokeStyle='rgba(203,213,225,.7)'; x.fillStyle='rgba(203,213,225,.7)'; x.lineWidth=1.3; x.beginPath(); x.arc(OX,OY,OR,-(le+50+TH0)*R,-(le+62+TH0)*R,true); x.stroke(); arrowHead(gb[0],gb[1],Math.atan2(gb[1]-ga[1],gb[0]-ga[0]),5);
    // 太陽
    const sg=x.createRadialGradient(OX,OY,3,OX,OY,22); sg.addColorStop(0,'rgba(255,240,170,1)'); sg.addColorStop(1,'rgba(255,200,60,0)'); x.fillStyle=sg; x.beginPath(); x.arc(OX,OY,22,0,2*Math.PI); x.fill();
    x.fillStyle='#fde047'; x.beginPath(); x.arc(OX,OY,9,0,2*Math.PI); x.fill(); x.font=F(10,1); halo('太陽',OX,OY+19,'#fde68a',true);
    // 地球（太陽の側が昼）と、南の向き
    const ep=oxy(le,OR), ts=Math.atan2(OY-ep[1],OX-ep[0]);
    x.fillStyle='#173153'; x.beginPath(); x.arc(ep[0],ep[1],8,0,2*Math.PI); x.fill(); x.fillStyle='#4f9fdc'; x.beginPath(); x.arc(ep[0],ep[1],8,ts-Math.PI/2,ts+Math.PI/2); x.closePath(); x.fill();
    const ta=-(am+TH0)*R, ex=ep[0]+Math.cos(ta)*30, ey=ep[1]+Math.sin(ta)*30;
    x.setLineDash([2,4]); x.strokeStyle=night?'rgba(250,204,21,.45)':'rgba(148,163,184,.35)'; x.lineWidth=1; x.beginPath(); x.moveTo(ep[0],ep[1]); x.lineTo(ep[0]+Math.cos(ta)*(CR+30),ep[1]+Math.sin(ta)*(CR+30)); x.stroke(); x.setLineDash([]);
    x.strokeStyle=night?'#facc15':'#94a3b8'; x.fillStyle=x.strokeStyle; x.lineWidth=2.4; x.beginPath(); x.moveTo(ep[0]+Math.cos(ta)*9,ep[1]+Math.sin(ta)*9); x.lineTo(ex,ey); x.stroke(); arrowHead(ex,ey,ta,6);
    x.fillStyle='#ef4444'; x.beginPath(); x.arc(ep[0]+Math.cos(ta)*8,ep[1]+Math.sin(ta)*8,2.6,0,2*Math.PI); x.fill();
    // 説明
    x.textAlign='left'; x.textBaseline='alphabetic'; x.font=F(10.5); x.fillStyle='rgba(226,232,240,.9)';
    ['真夜中は、太陽と反対側の星座が南に見える','地球は1日に約1°公転 → 同じ時刻の星は','1か月に約30°ずつ西へずれる（大きさは誇張）'].forEach((t,i)=>x.fillText(t,PW+12,H-46+i*16));
  }
  const SELP=ST.findIndex(s=>s[4]==='北極星');
  function draw(){
    cam=mkCam(VAZ[view]); x.clearRect(0,0,W,H);
    const L=drawSky(); drawOrbit(L);
    x.strokeStyle='rgba(255,255,255,.2)'; x.lineWidth=1; x.beginPath(); x.moveTo(PW+1,0); x.lineTo(PW+1,H); x.stroke();
    const jd=jdT(tAbs()), sn=sunOf(jd), sAlt=hor(sn.ra,sn.dec,L)[0], sc=southCons(L), h=hor(ST[sel][0],ST[sel][1],L);
    fit('sDate',dateTxt(n0)); fit('sTime',hm(hour)+'（'+word(hour)+'）');
    $('sSouth').style.whiteSpace='pre-line'; fit('sSouth',sAlt>-3?'昼（見えない）':sc.length?sc.join('\n'):'めだつ星座なし');
    fit('sStar',h[0]>0?dir8(h[1])+'・高度'+Math.round(h[0])+'°':'地平線の下');
    ['E','S','W','N'].forEach(k=>setBtn('v'+k,k===view));
    setShare('【星の動き】'+dateTxt(n0)+' '+hm(hour)+'、東京の南の空には'+(sc.length&&sAlt<=-3?sc.join('・'):'（昼で星は見えない）')+'。星は1時間に15°、同じ時刻なら1か月に30°西へ動いて見えます⭐｜シミュラボ');
  }
  function syncUI(){ $('day').value=String(n0); $('dayL').textContent=dateTxt(n0); $('hour').value=String(Math.round(hour*4)/4); $('hourL').textContent=hm(hour)+'（'+word(hour)+'）'; }
  function stopPlay(){ play=false; $('play').textContent='▶ 時間を進める'; }
  function step(dh){ hour+=dh; while(hour>=24){ hour-=24; n0=n0%365+1; } while(hour<0){ hour+=24; n0=n0===1?365:n0-1; } }
  function frame(ts){ const dt=last?Math.min(0.1,(ts-last)/1000):0; last=ts;
    if(play){ step(dt*1.0); syncUI(); need=true; }
    if(need){ need=false; draw(); }
    requestAnimationFrame(frame); }
  function pos(e){ const q=cpos(cv,e); return [q[0]/dpr,q[1]/dpr]; }
  function pickStar(q){ const L=lstOf(jdT(tAbs())); let best=-1, bd=20; [...$('star').options].forEach(o=>{ const i=+o.value, h=hor(ST[i][0],ST[i][1],L); if(h[0]<0) return; const pq=pj(h[0],h[1]); if(!pq) return; const d=Math.hypot(pq[0]-q[0],pq[1]-q[1]); if(d<bd){ bd=d; best=i; } }); return best; }
  function angAt(q){ const pc=pj(LAT,0)||[SX,SY]; return Math.atan2(-(q[1]-pc[1]),q[0]-pc[0])/R; }
  function mv(q){
    if(drag==='sky'){ const dx=q[0]-d0.q[0]; if(Math.abs(dx)+Math.abs(q[1]-d0.q[1])>5) d0.moved=true; if(!d0.moved) return;
      let dh=dx/12; if(view==='N'){ const a=angAt(q); d0.acc+=wrap(a-d0.a+180,360)-180; d0.a=a; dh=d0.acc/SID; } n0=d0.n; hour=d0.h; step(dh); }
    else if(drag==='orbit'){ const a=Math.atan2(-(q[1]-OY),q[0]-OX)/R, le=wrap(a-TH0,360), ls=wrap(le-180,360); let best=n0, bd=1e9; for(let k=1;k<=365;k++){ const d=Math.abs(wrap(sunOf(jdOf(k,hour)).lam-ls+180,360)-180); if(d<bd){ bd=d; best=k; } } n0=best; }
    trail=null; ghost=0; syncUI(); draw(); }
  cv.addEventListener('pointerdown',e=>{ const q=pos(e); stopPlay(); drag=q[0]<PW?'sky':'orbit'; d0={q:q,h:hour,n:n0,moved:false,a:angAt(q),acc:0}; try{ cv.setPointerCapture(e.pointerId); }catch(_){ } if(drag==='orbit') mv(q); });
  cv.addEventListener('pointermove',e=>{ if(drag) mv(pos(e)); });
  cv.addEventListener('pointerup',e=>{ if(drag==='sky'&&d0&&!d0.moved){ const i=pickStar(pos(e)); if(i>=0){ sel=i; $('star').value=String(i); draw(); } } drag=null; });
  cv.addEventListener('pointercancel',()=>{ drag=null; });
  $('day').addEventListener('input',()=>{ n0=+$('day').value; trail=null; ghost=0; syncUI(); draw(); });
  $('hour').addEventListener('input',()=>{ hour=+$('hour').value; if(hour>=24) hour=23.99; trail=null; ghost=0; stopPlay(); syncUI(); draw(); });
  $('star').addEventListener('change',()=>{ sel=+$('star').value; const h=hor(ST[sel][0],ST[sel][1],lstOf(jdT(tAbs()))); if(h[0]>3){ view=['N','E','S','W'][Math.round(wrap(h[1],360)/90)%4]; } draw(); });
  ['E','S','W','N'].forEach(k=>$('v'+k).addEventListener('click',()=>{ view=k; draw(); }));
  $('play').addEventListener('click',()=>{ if(play){ stopPlay(); return; } play=true; ghost=0; trail=tAbs(); $('play').textContent='⏸ 止める'; });
  $('month').addEventListener('click',()=>{ stopPlay(); const n2=nextMonth(n0); ghost=wrap(n2-n0,365)||30; n0=n2; trail=null; syncUI(); draw(); });
  sel=autoSel(); $('star').value=String(sel);
  syncUI(); draw(); need=false; requestAnimationFrame(frame);
'''

sim(slug="hoshi-ugoki", cat="rika", emoji="⭐", score=79,
    title="星の1日・1年の動き（日周運動・年周運動・季節の星座）",
    title_tag="星の日周運動・年周運動シミュレーター｜季節の星座が変わる理由と北極星のまわりの動き",
    meta_desc="星の日周運動（1時間に15°）と年周運動（1か月に30°）を、東・南・西・北の空で確かめる無料シミュレーター。オリオン座・さそり座・カシオペヤ座・北斗七星など実際の星の位置を東京の空で計算し、公転と季節の星座の関係も表示します。小4・中3の理科の授業に。",
    og_title="星の1日・1年の動きシミュレーター（日周運動・年周運動・季節の星座）",
    og_desc="東・南・西・北の空で星の動きを再生。北の空は北極星を中心に反時計回り。同じ時刻の星が1か月に30°西へずれる理由を、公転の図と並べて確かめよう。",
    card_desc="東・南・西・北の空で星の動きを再生。1時間に15°の日周運動、1か月に30°の年周運動と季節の星座がわかる。",
    lead="星は1時間に約15°ずつ東から西へ動き、北の空では北極星を中心に反時計回りに回ります。同じ時刻に見える星は1か月に約30°西へずれ、季節によって見える星座が変わります。",
    model="小4 月と星／中3 日周運動と自転・年周運動と公転",
    level="小学4年、中学3年",
    unit="小学校 第4学年 B(5)「月と星」／中学校 第2分野（6）地球と宇宙（ア）天体の動きと地球の自転・公転",
    canvas=canvas(640, 420),
    controls=slider("day", "日付", 1, 365, 15, 1) + slider("hour", "時刻（日本時間）", 0, 24, 21, 0.25) + select("star", "注目する星", SEL_OPTS),
    buttons=btn("vE", "東の空") + btn("vS", "南の空") + btn("vW", "西の空") + btn("vN", "北の空") + btn("play", "▶ 時間を進める", True) + btn("month", "＋1か月（同じ時刻）"),
    stats=stats([("sDate", "日付", False), ("sTime", "時刻", False), ("sSouth", "南の空の主な星座", True), ("sStar", "注目する星の高度・方位", False)]),
    legend="左：東京で東・南・西・北のどれかを向いて見た空（カメラで写した見え方）。黄色の点線は注目する星の1日の道すじで、点は1時間ごとの位置です。「▶ 時間を進める」で星が動いた跡（光跡）が残り、「＋1か月」で1か月前の同じ時刻の位置（オレンジの点線）と比べられます。空を左右に（北の空では北極星のまわりに）なぞると時刻が、星をタップすると注目する星が変わります。右：北極の上から見た地球の公転と季節の星座。地球をなぞると日付が変わります。",
    article='''
<h2>このシミュレーションでわかること</h2>
<p>星も太陽と同じように、東からのぼり、南の空を通って西へしずみます。空の星全体が、北極星の近くを中心にして、1時間に約15°（360°÷24時間）ずつ東から西へ回って見えます。これは地球が西から東へ自転しているために起こる見かけの動き（日周運動）です。北の空では、星は北極星を中心に反時計回りに回ります。</p>
<p>また、同じ時刻に見える星の位置は、1か月に約30°ずつ東から西へずれていき、1年でもとにもどります（年周運動）。これは地球が太陽のまわりを1年で1周（公転）しているからです。そのため季節によって見える星座が変わり、真夜中に南の空に見えるのは、地球から見て太陽と反対側にある星座です。</p>
''' + T([[NW("小学校4年"), NW("B(5) 月と星"), "空には、明るさや色の違う星があること。星の集まりは、1日のうちでも時刻によって、並び方は変わらないが、位置が変わること"],
          [NW("中学校3年"), "第2分野（6）地球と宇宙「日周運動と自転」", "天体の日周運動の観察を行い、その観察記録を地球の自転と関連付けて理解すること"],
          [NW("中学校3年"), "第2分野（6）地球と宇宙「年周運動と公転」", "星座の年周運動などの観察を行い、その観察記録を地球の公転と関連付けて理解すること"]],
         ["学年", "単元", "学習指導要領（平成29年告示）の内容"]) + '''
<p>中学校の解説（理科編 p.105〜106）は、天球の各方位の星座の見かけの動きを観察すること、太陽を中心に公転する地球とその外側に季節の代表的な星座を配したモデルを使うことをあげ、どちらでも観察者の視点を地球の外に移して考えさせるために、コンピュータシミュレーションを用いて視覚的に捉えさせる工夫を例にあげています。小学校4年の解説は、学校で観察できない時間帯の月や星の位置の変化について、映像や模型、プラネタリウムなどの活用をあげています。学年は一般的な配当です。</p>

<h2>授業での使い方</h2>
<p><b>導入（小4）</b>：「南の空」で時刻のスライダーを動かし、星座の形（星の並び方）は変わらないまま、位置が東から西へ変わることを確かめます。ベテルギウスやアンタレス（赤い星）、リゲルやシリウス（青白い星）など、星の色の違いにも注目させます。</p>
<p><b>展開（中3・日周運動）</b>：東・南・西・北の空を切り替えて「▶ 時間を進める」を押し、星の動き方が方位によって違うこと（東の空は右ななめ上へ、南の空は東から西へ、西の空は右ななめ下へ、北の空は北極星を中心に反時計回り）を記録させます。注目する星の「1時間で15°」の表示で、動く速さを確かめます。</p>
<p><b>展開（中3・年周運動）</b>：時刻を同じにしたまま「＋1か月（同じ時刻）」を押し、星の位置が約30°西へずれることを確かめます。右の公転の図で、地球の位置と、真夜中に南の空に見える星座の関係を説明させます。</p>
<p><b>まとめ</b>：下の季節の星座の表と計算問題で、星が南中する時刻が1か月で約2時間早くなることを確かめます。</p>
<p>児童・生徒への問いの例です。</p>
<ul>
<li>（小4）夜8時にオリオン座を見ました。夜10時には、オリオン座の形と位置はどうなっているでしょう。（形は同じで、西の方へ動いている）</li>
<li>（中3）北の空のカシオペヤ座は、3時間後に、北極星を中心にどちら回りに何度回って見えるでしょう。（反時計回りに約45°）</li>
<li>（中3）夏の夜にオリオン座が見えないのはなぜでしょう。右の公転の図を使って説明しましょう。（夏の地球から見ると、オリオン座は太陽と同じ方向にあり、昼の空にあるから）</li>
</ul>

<h2>しくみ・解説</h2>
<h3>日周運動：1時間に15°</h3>
<p>地球は1日（約24時間）で1回自転するので、星は1時間に 360° ÷ 24 ＝ 15° 動いて見えます。星が回る中心は、地軸を北へのばした方向（天の北極）で、そのすぐ近くに北極星があります。そのため北極星はほとんど動かず、その高度は観測地点の緯度とほぼ同じです（東京で約35.7°）。</p>
''' + T([["東の空", "地平線から右ななめ上へのぼる"], ["南の空", "東（左）から西（右）へ、弧をえがいて動く。真南にきたとき（南中）がいちばん高い"],
          ["西の空", "右ななめ下へしずむ"], ["北の空", "北極星を中心に、反時計回りに回る（1時間に15°）"]], ["見る方角", "星の動き方（東京）"]) + '''
<h3>年周運動：1か月に30°</h3>
<p>地球は1年（12か月）で太陽のまわりを1周するので、同じ時刻に見える星の位置は、1か月に 360° ÷ 12 ＝ 30° ずつ東から西へずれます。1日では約1°で、時間にすると約4分です。つまり、星が南中する時刻は1日に約4分、1か月で約2時間ずつ早くなります。</p>
<p><b>例題1</b>：ある日の午後8時に、オリオン座が南中しました。同じ日の午後10時には、オリオン座は南中した位置からどちらへ何度動いていますか。<br>答え：15° × 2時間 ＝ <b>西へ30°</b></p>
<p><b>例題2</b>：1月15日の午後10時に、オリオン座が南中しました。午後8時に南中するのは、いつごろですか。<br>答え：南中する時刻は1か月に約2時間早くなるので、<b>約1か月後の2月15日ごろ</b></p>
<p><b>例題3</b>：ある日の午後9時に、北の空でカシオペヤ座が北極星の真上に見えました。同じ日の何時に、北極星の左側（西側）に見えますか。<br>答え：反時計回りに90°回るのにかかる時間は 90° ÷ 15° ＝ 6時間なので、<b>翌日の午前3時</b></p>
<p><b>例題4</b>：7月10日ごろの午後9時に、さそり座のアンタレスが南中しました。2か月後の午後9時には、アンタレスは南中した位置からどちらへ何度動いた位置にありますか。<br>答え：30° × 2か月 ＝ <b>西へ60°</b>（南西の地平線近く。このシミュレーターでは、9月10日21時に高度約5°）</p>
<h3>季節の星座（夜9時ごろの南の空）</h3>
''' + T([[NW("春（4〜5月ごろ）"), "しし座、おとめ座、うしかい座", "レグルス、スピカ（青白い星）、アークトゥルス（だいだい色の星）。北斗七星の柄のカーブをのばすと春の大曲線"],
          [NW("夏（7〜8月ごろ）"), "さそり座、いて座、わし座。頭の上近くに こと座・はくちょう座", "アンタレス（赤い星）、ベガ・アルタイル・デネブ（夏の大三角）"],
          [NW("秋（10〜11月ごろ）"), "ペガスス座、アンドロメダ座、みなみのうお座", "秋の四辺形、フォーマルハウト。北の空にカシオペヤ座"],
          [NW("冬（1〜2月ごろ）"), "オリオン座、おうし座、おおいぬ座、こいぬ座、ふたご座", "ベテルギウス（赤い星）、リゲル（青白い星）、シリウス、プロキオン（冬の大三角）、すばる"]],
         ["季節", "南の空の主な星座", "明るい星・目じるし"]) + '''
<p>月は目安です。このシミュレーターで各月15日の21時の東京の空を計算し、南中の前後2時間ほど（子午線から約30°以内）にある星座を確かめました。3月・6月・9月・12月ごろは、となりの季節の星座が入れかわる時期です。</p>
<h3>公転と、真夜中に南に見える星座</h3>
<p>真夜中に南の空に見えるのは、地球から見て太陽と反対の方向にある星座です。右の図のように、12月中ごろの地球から見て太陽と反対側にあるのはオリオン座（ベテルギウスが0時に南中するのは12月16日ごろ）、5月の終わりごろはさそり座（アンタレスは5月26日ごろ）です。季節が進むと地球の位置が変わるので、真夜中に南に見える星座も変わります。太陽と同じ方向にある星座は、昼の空にあるため見えません。</p>
''' + P("星座の星はとても遠くにあるので、地球が公転して位置が変わっても、星座の形や星座のある方向は変わりません。変わるのは「いつ、どの方角に見えるか」です。") + '''
<h3>星の位置の計算（このシミュレーションのしくみ）</h3>
<p>星の位置は、それぞれの星の赤経・赤緯（天球の上の経度・緯度にあたる値）と、日付・時刻から求めた恒星時をもとに、東京（北緯35.7°）で見た高度と方位を計算しています。星の赤経・赤緯と明るさ（等級）は SIMBAD（ストラスブール天文データセンター）の値で、2026年までの歳差（地軸の向きのゆっくりした変化）を補正しています。たとえば、東京でベテルギウスが南中するときの高度は約62°、アンタレスは約28°、シリウスは約38°です。南中する時刻は、ベテルギウスが1月15日21時58分・2月15日19時56分、アンタレスが7月15日20時39分（2026年）です。</p>
<h3>このシミュレーションで単純化していること</h3>
<ul>
<li>地上から見た空の図は、カメラで写したときと同じ見え方（透視図）で、左右の端ほど引きのばされて見えます。</li>
<li>大気による浮き上がり（地平線近くで約0.5°）は入れていません。高度は計算上の値です。</li>
<li>星座は、明るい星だけを線で結んでいます。結び方は本によって少しずつ違います。</li>
<li>右の公転の図は、大きさと距離を誇張しています。黄色の矢印は、いまの時刻に東京で真南の空の方向を、公転の面に写したものです。</li>
<li>日付は2026年の暦で計算しています（ほかの年でも、星の位置のずれは1°ほどです）。</li>
</ul>

<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「小学校学習指導要領（平成29年告示）解説 理科編」（''' + A(MEXT_SHO) + '''）</li>
<li>文部科学省「中学校学習指導要領（平成29年告示）解説 理科編」p.104〜106（''' + A(MEXT_CHU) + '''）</li>
<li>国立天文台 暦計算室「暦Wiki 天文航法/緯度の決定」（''' + A("https://eco.mtk.nao.ac.jp/koyomi/wiki/C5B7CAB8B9D2CBA12FB0DEC5D9A4CEB7E8C4EA.html") + '''）…北極星の高度と緯度</li>
<li>国立天文台「歳差ってなに？」（''' + A("https://www.nao.ac.jp/faq/a1007.html") + '''）</li>
<li>SIMBAD Astronomical Database（CDS, Strasbourg）（''' + A("https://simbad.cds.unistra.fr/simbad/") + '''）…星の赤経・赤緯・等級</li>
<li>Jean Meeus『Astronomical Algorithms』第2版（Willmann-Bell, 1998）</li>
</ul>
''',
    faqs=[("星が東から西へ動いて見えるのはなぜですか？", "地球が西から東へ自転しているからです。地球は1日に1回自転するので、星は1時間に約15°（360°÷24時間）ずつ、東から西へ動いて見えます。これを日周運動といいます。"),
          ("北極星がほとんど動かないのはなぜですか？", "地軸を北へのばした方向（天の北極）のすぐ近くにあるからです。ほかの星は北極星のまわりを反時計回りに回って見えます。北極星の高度は、観測する場所の緯度とほぼ同じで、東京では約35.7°です。"),
          ("同じ時刻に見える星座が、季節によって変わるのはなぜですか？", "地球が太陽のまわりを1年で1周（公転）しているからです。同じ時刻に見える星の位置は1か月に約30°ずつ西へずれ、1年でもとにもどります。これを年周運動といいます。"),
          ("星が南中する時刻は、1日に何分早くなりますか？", "約4分です。1か月では約2時間、1年で24時間早くなって、もとの時刻にもどります。地球が公転して、1日に約1°ずつ太陽に対する向きが変わるためです。"),
          ("星座の形は、時間がたつと変わりますか？", "星の並び方（星座の形）は変わりません。位置が変わるのと同時に、地平線に対する向き（かたむき）は変わって見えます。たとえばオリオン座は、東の空からのぼるときは横だおしのような向きに見えます。"),
          ("夏の大三角・冬の大三角は、どの星ですか？", "夏の大三角は、こと座のベガ、わし座のアルタイル、はくちょう座のデネブです。冬の大三角は、オリオン座のベテルギウス、おおいぬ座のシリウス、こいぬ座のプロキオンです。")],
    rel=[("hoshizora-shisu", "🔭", "今夜の星空指数"), ("taiyou-ugoki", "🌞", "太陽の1日の動きと季節（透明半球・南中高度）"),
         ("tsuki-michikake", "🌓", "月の満ち欠けの仕組みシミュレーター"), ("kyou-no-tsuki", "🌙", "今日の月（月齢・満ち欠け・次の満月はいつ？）"), ("solar-system", "🪐", "太陽系シミュレーター")],
    js=JS2.replace("%%CORE%%", CORE2.replace("%%ST%%", ST_JS).replace("%%CO%%", CO_JS)).replace("%%UI%%", UI_COMMON).replace("%%AS%%", AS_JS).replace("%%ORB%%", ORB_JS))

assert all("@@" not in s["js"] and "%%" not in s["js"] for s in SIMS)
