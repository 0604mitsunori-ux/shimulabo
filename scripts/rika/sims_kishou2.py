# -*- coding: utf-8 -*-
"""理科の授業向け（第2弾）：前線の通過と天気の変化（中2）／流れる水の働きと土地の変化（小5）"""
import math
from common import canvas, slider, select, btn, stats, T, N, P

SIMS = []
def sim(**kw): SIMS.append(kw)

MEXT_CHU = "https://www.mext.go.jp/a_menu/shotou/new-cs/1387016.htm"
MEXT_SHO = "https://www.mext.go.jp/a_menu/shotou/new-cs/1387014.htm"
def A(url, text): return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (url, text)
def NW(t): return '<span style="white-space:nowrap">%s</span>' % t

# 飽和水蒸気量［g/m³］（0〜40℃・1℃ごと。shitsudo-roten と同じ表。25℃＝23.1）
SAT = [4.8, 5.2, 5.6, 6.0, 6.4, 6.8, 7.3, 7.8, 8.3, 8.8, 9.4, 10.0, 10.7, 11.4, 12.1, 12.8, 13.6, 14.5, 15.4, 16.3,
       17.3, 18.3, 19.4, 20.6, 21.8, 23.1, 24.4, 25.8, 27.2, 28.8, 30.4, 32.1, 33.8, 35.7, 37.6, 39.6, 41.7, 43.9,
       46.2, 48.6, 51.1]
assert len(SAT) == 41 and abs(SAT[25] - 23.1) < 1e-9
SAT_JS = ",".join("%.1f" % v for v in SAT)


# ============================================================ 前線モデル（JS と同じ式。記事の観測記録の表を作る）
def _cl(v, a, b): return max(a, min(b, v))
def _jr(v): return math.floor(v + 0.5)                    # JS の Math.round
def _f1(v): return "%.1f" % (math.floor(v * 10 + 0.5) / 10)  # JS の (Math.round(v*10)/10).toFixed(1)
def _sat(t):
    t = _cl(t, 0, 40); i = min(39, int(math.floor(t))); return SAT[i] + (SAT[i + 1] - SAT[i]) * (t - i)
def _ss(a, b, v):
    u = _cl((v - a) / (b - a), 0, 1); return u * u * (3 - 2 * u)
def _lg(v): return 0.0 if v < -50 else 1 / (1 + math.exp(-v))
def _xwf(s): return s * (1.6 - 0.0006 * s)
def _xcf(s): return -s * (0.6 - 0.0003 * s)
def _g2(dx, dy, sg): return math.exp(-(dx * dx + dy * dy) / (2 * sg * sg))
def _pres(x, y):
    s = -y
    p = 1013 - 17 * _g2(x, y, 520) + 8 * _g2(x - 1600, y + 150, 560) + 8 * _g2(x + 1550, y + 250, 560)
    if s > 0:
        dW = x - _xwf(s); dC = x - _xcf(s)
        p -= (5.5 * _ss(0, 140, s) * (1 - _ss(620, 820, s)) * math.exp(-math.sqrt(dW * dW + 2025) / 240)
              + 7 * _ss(0, 140, s) * (1 - _ss(820, 1020, s)) * math.exp(-math.sqrt(dC * dC + 100) / 230))
    return p
DIRS = ["北", "北北東", "北東", "東北東", "東", "東南東", "南東", "南南東", "南", "南南西", "南西", "西南西", "西", "西北西", "北西", "北北西"]
WXN = ["快晴", "晴れ", "くもり", "雨", "強い雨"]
_BFT = [0.3, 1.6, 3.4, 5.5, 8.0, 10.8, 13.9, 17.2, 20.8, 24.5, 28.5, 32.7]
def _wind(x, y):
    gx = (_pres(x + 1, y) - _pres(x - 1, y)) / 2; gy = (_pres(x, y + 1) - _pres(x, y - 1)) / 2
    g = math.hypot(gx, gy) or 1e-9; ca = math.cos(2 * math.pi / 3); sa = math.sin(2 * math.pi / 3)
    vx = (gx * ca - gy * sa) / g; vy = (gx * sa + gy * ca) / g
    b = (math.degrees(math.atan2(-vx, -vy)) + 360) % 360; ms = g * 0.1 / (1.2 * 8.4e-5) * 0.22
    bf = 0
    while bf < 12 and ms >= _BFT[bf]: bf += 1
    return DIRS[_jr(b / 22.5) % 16], bf
def _rain(x, y):
    s = -y; r = 0.0
    if s > -20:
        sp = max(s, 0); dW = x - _xwf(sp); Rw = 320 - 0.25 * sp
        r = (1 + 3 * (1 - _cl(dW / Rw, 0, 1))) * _lg(dW / 12 + 1) * _lg((Rw - dW) / 15) * (1 - _ss(560, 760, s))
        if s > 0:
            dC = x - _xcf(s); r = max(r, 25 * _lg((dC + 55) / 6) * _lg((12 - dC) / 5) * _ss(30, 140, s) * (1 - _ss(850, 1020, s)))
    bb = 3.2 * math.exp(-((x - 80) ** 2 / 115200 + (y - 60) ** 2 / 45000)) * _ss(-120, 0, y)
    if bb > 0.5: r = max(r, bb)
    return r
def _cloud(x, y, r):
    s = -y; dW = x - _xwf(s); dC = x - _xcf(s); Rw = 320 - 0.25 * s; c = 2.0
    if dW > 0: c = max(c, 2 + 8 * _cl((Rw + 300 - dW) / 150, 0, 1))
    if dW <= 0 and dC >= 0:
        c = 4.0
        if dW > -70: c = max(c, 4 + 5 * (1 + dW / 70))
        if dC < 90: c = max(c, 4 + 6 * min(1, (90 - dC) / 78))
    if dC < 0: c = max(2, 2 + 8 * _cl((dC + 170) / 110, 0, 1))
    return min(10, max(c, 10 * _cl(r / 0.5, 0, 1)))
def _diur(h):
    h = ((h % 24) + 24) % 24
    if 6 <= h <= 14: return -math.cos(math.pi * (h - 6) / 8)
    return math.cos(math.pi * ((((h - 14) % 24) + 24) % 24) / 16)
_XSKM = 400 * 4.5
def _zrun(ys=300, U=40, twf=16.0):
    x0 = _XSKM - _xwf(ys) - U * twf; tcf = (_XSKM - x0 - _xcf(ys)) / U
    def obs(t):
        x = _XSKM - (x0 + U * t); y = -ys
        Sw = _lg(-(x - _xwf(ys)) / 25); Sc = _lg(-(x - _xcf(ys)) / 6); r = _rain(x, y); c = _cloud(x, y, r)
        Tm = 12 + 7 * Sw - 9 * Sc + 3 * (1 - 0.08 * c) * _diur(t)
        Td = 6 + 9 * Sw - 13 * Sc; Td = min(Tm, Td + (Tm - Td) * min(1, r / 1.5))
        d, bf = _wind(x, y)
        wx = (3 if r >= 10 else 2) if r >= 0.5 else (1 if c >= 9 else (0 if c >= 2 else -1))
        return dict(T=Tm, RH=min(100, _sat(Td) / _sat(Tm) * 100), P=_pres(x, y), d=d, bf=bf, r=r, wx=wx)
    return obs, twf, tcf

def _hm(t):
    m = _jr(t * 4) * 15; d = m // 1440; r = m - d * 1440
    return "%d日目 %d:%02d" % (d + 1, r // 60, r % 60)

_ZO, _ZTWF, _ZTCF = _zrun()
_ZROWS = [_ZO(3 * k) for k in range(17)]
ZTABLE = T([["%d日目 %d時" % (3 * k // 24 + 1, 3 * k % 24), WXN[o["wx"] + 1], o["d"], str(o["bf"]), _f1(o["T"]), str(_jr(o["RH"])), _f1(o["P"])]
            for k, o in enumerate(_ZROWS)], ["日時", "天気", "風向", "風力", "気温［℃］", "湿度［％］", "気圧［hPa］"])
_HR = []
for _h in range(48):
    _a = sum(_ZO(_h + q / 4)["r"] * (0.5 if q in (0, 4) else 1) for q in range(5)); _HR.append(_a / 4)
_WR = [h for h in range(0, 24) if _HR[h] >= 0.5]
_CR = [h for h in range(24, 48) if _HR[h] >= 0.5]
_WSUM = sum(_HR[h] for h in _WR); _CSUM = sum(_HR[h] for h in _CR); _CMAX = max(_HR[h] for h in _CR); _WMAX = max(_HR[h] for h in _WR)
_R = {k: _ZROWS[k] for k in range(17)}
# 例題で使う値（初期設定）：温暖前線 15時→18時、寒冷前線 2日目6時→9時
assert _R[5]["wx"] >= 2 and _R[6]["wx"] <= 1 and _R[10]["wx"] >= 2 and _R[11]["wx"] <= 1
assert 15 < _ZTWF < 18 and 30 < _ZTCF < 33
assert _R[10]["d"] in ("南南西", "南西") and _R[11]["d"] in ("北西", "北北西")


# ============================================================ 1 前線と天気の変化
sim(slug="zensen-tenki", cat="rika", emoji="🌦️", score=82,
    title="前線と天気の変化シミュレーター（寒冷前線・温暖前線）",
    title_tag="寒冷前線・温暖前線のシミュレーター｜前線の通過と天気の変化・断面図（中2理科）",
    meta_desc="寒冷前線と温暖前線をともなう低気圧が西から東へ進み、観測地点の気温・湿度・気圧・風向・天気がどう変わるかを、天気図・断面図・観測記録のグラフで同時に確かめられる無料シミュレーター。積乱雲と乱層雲、雨の降り方のちがい、通過時刻の読み取り練習つき。",
    og_title="前線と天気の変化シミュレーター（寒冷前線・温暖前線）",
    og_desc="低気圧と前線が通過するときの気温・気圧・風向・天気の変化を、天気図・断面図・観測記録のグラフで確かめる中2理科の教材です。",
    card_desc="寒冷前線・温暖前線が通過すると気温・風向・雨はどう変わる？天気図・断面図・観測グラフで確かめる。",
    lead="温帯低気圧と前線が西から東へ進むと、観測地点の気温・湿度・気圧・風向・天気がグラフに記録されていきます。寒冷前線が通ると気温が急に下がって北寄りの風になり、短時間の強い雨。温暖前線は長くおだやかな雨のあと気温が上がります。断面図で寒気と暖気の動きと雲のちがいも確かめられます。",
    model="中2 天気の変化（前線の通過と天気の変化）",
    level="中学2年",
    unit="中学校 第2分野（4）気象とその変化",
    canvas=canvas(640, 656, light=True),
    controls=select("mode", "使い方", [("play", "ふつう（前線を表示）"), ("quiz", "読み取り練習（前線をかくす）")])
           + slider("tt", "時刻", 0, 48, 0, 0.25)
           + slider("ys", "観測地点の位置", 200, 500, 300, 10, "中心の南{v}km")
           + slider("uu", "低気圧の進む速さ", 30, 60, 40, 5, "時速{v}km")
           + select("diu", "気温の日変化", [("on", "入れる（実際の観測に近い）"), ("off", "入れない（前線の影響だけ）")])
           + slider("sp", "再生の速さ", 1, 6, 2, 1, "1秒で{v}時間"),
    buttons=btn("play", "⏸ 一時停止", True) + btn("rew", "↺ 最初から") + btn("rand", "🎲 別の天気で") + btn("ans", "✔ 答えを見る", True),
    stats=stats([("sTime", "時刻", False), ("sT", "気温", True), ("sRH", "湿度", False), ("sP", "気圧", False),
                 ("sW", "風向（風力）", False), ("sWx", "天気", False), ("sWf", "温暖前線の通過", False), ("sCf", "寒冷前線の通過", True)]),
    legend="上の図：赤い線と半円＝温暖前線、青い線と三角＝寒冷前線、黒い線＝等圧線（4hPaごと）、青くぬった所＝雨の範囲、灰色の矢印＝地上の風（空気が流れる向き）。地図を指でなぞると観測地点を南北に動かせます。下のグラフをなぞると時刻を動かせます。天気記号：○快晴、○に縦線＝晴れ、◎くもり、●雨（大きい●は強い雨）。記号からのびる棒は風がふいてくる方位、羽根の数は風力です。前線・気温・雨の量は説明のためのモデルで、実際の観測値ではありません。",
    article='''
<h2>このシミュレーションでわかること</h2>
''' + P("寒冷前線が通過すると、<b>気温が急に下がり、風向が南寄りから北寄りに変わり、せまい範囲に短時間の強い雨</b>が降ります。温暖前線が通過すると、<b>広い範囲で長く続いたおだやかな雨がやみ、気温が上がり、風向が東寄り（南東）から南寄り（南西）に変わります</b>。") + '''
<p>温帯低気圧にともなう前線が西から東へ進むようすを、天気図ふうの図・断面図・観測地点の記録グラフの3つで同時に見られます。断面図では、寒冷前線では寒気が暖気の下にもぐりこんで暖気を急におし上げること（積乱雲）、温暖前線では暖気が寒気の上をゆるやかにはい上がること（乱層雲など）を確かめられます。</p>
<p>対応する単元は、中学校学習指導要領 理科 第2分野（4）「気象とその変化」の（イ）天気の変化「前線の通過と天気の変化」で、主に<b>中学2年</b>で学習します。学習指導要領解説は、前線の通過にともなう気温・湿度・気圧・風向・天気の変化を暖気・寒気と関連付けて理解させること、暖気と寒気のぶつかり合いを表すモデル実験などで前線の構造の理解を深めることを例示しています。</p>

<h2>授業での使い方</h2>
<ul>
<li><b>導入</b>：「にわか雨のあと急に寒くなった」「北風に変わった」などの経験を聞き、そのまま再生して、観測地点の記録グラフがかかれていくようすを見せます。何がいつ変わったかを予想させます。</li>
<li><b>展開</b>：前線が通過した時刻の前後で、気温・湿度・気圧・風向・天気がどう変わったかをグラフから読み取り、断面図の寒気・暖気の動きと結びつけます。観測地点を南北に動かすと、2つの前線が通過する時刻の間かくが変わることも確かめられます。校庭での継続的な気象観測の記録や教科書のグラフと見くらべるのも効果的です。</li>
<li><b>まとめ</b>：「使い方」を「読み取り練習」にすると、前線がかくれ、記録グラフだけが表示されます。寒冷前線が通過した時刻をグラフをタップして答え、「答えを見る」で確かめます。「別の天気で」を押すと、観測地点・低気圧の速さ・時刻を変えた別の記録で何度も練習できます。</li>
</ul>
<p>生徒への問いの例：</p>
<ol>
<li>寒冷前線が通過するとき、気温・風向・雨の降り方はどう変わるでしょうか。それはなぜでしょうか。</li>
<li>温暖前線による雨と寒冷前線による雨では、降る時間や強さにどんなちがいがあるでしょうか。断面図の雲の形と結びつけて説明しましょう。</li>
<li>夜に気温が下がったのか、寒冷前線が通過して気温が下がったのかは、グラフのどこを見れば区別できるでしょうか。</li>
</ol>

<h2>しくみ・解説</h2>
<h3>気団と前線</h3>
<p>気温や湿度がほぼ一様な大きな空気のかたまりを<b>気団</b>といいます。性質のちがう気団（寒気と暖気）が接すると、すぐには混じり合わずに境の面ができます。この面を<b>前線面</b>、前線面が地表と交わる線を<b>前線</b>といいます。暖気は寒気より密度が小さい（軽い）ので、前線面では暖気が寒気の上にのり上げる形になります。</p>
<h3>寒冷前線と温暖前線のちがい</h3>
''' + T([["空気の動き", "寒気が暖気の下にもぐりこみ、暖気をおし上げる", "暖気が寒気の上をはい上がる"],
          ["前線面の傾き", "急", "ゆるやか"],
          ["できる雲", "積乱雲（縦に発達する雲）", "乱層雲・高層雲・巻層雲・巻雲（横に広がる雲）"],
          ["雨の降り方", "せまい範囲に、短時間の強い雨（雷や突風をともなうことも）", "広い範囲に、長時間のおだやかな雨"],
          ["通過後の気温", "急に下がる", "上がる"],
          ["通過時の風向の変化", "南寄り（南西など）→ 北寄り（北西など）", "東寄り（南東など）→ 南寄り（南西など）"],
          ["天気図の記号", "三角（▲）を進む向きにつけた線（青）", "半円を進む向きにつけた線（赤）"]],
         ["", "寒冷前線", "温暖前線"]) + '''
<p>気圧は、前線（低気圧）が近づくと下がり、寒冷前線が通過するころに最も低くなり、通過後は上がっていきます。</p>
<h3>温帯低気圧と天気の移り変わり</h3>
<p>日本付近の温帯低気圧は、中心から南東に温暖前線、南西に寒冷前線をのばしていることが多く、上空の偏西風に流されて西から東へ進みます。そのため天気は西から東へ移り変わり、ある地点では、温暖前線の通過 → 2つの前線の間（暖域） → 寒冷前線の通過、の順に天気が変わります。断面図は、時間がたつと右（東）へ動いていくので、観測地点の天気の変化は、断面図を東（右）から西（左）へ読んだ順番になります。</p>
<p>低気圧のまわりでは、北半球では風が<b>反時計回りに中心に向かってふきこみ</b>、中心付近で上昇気流が起こるため雲ができやすくなります。高気圧からは<b>時計回りにふき出し</b>、下降気流が起こるため晴れることが多くなります。天気図ふうの図の灰色の矢印で確かめられます。</p>
<h3>観測記録から前線の通過を読み取る（例題）</h3>
<p>次の表は、このシミュレーターを初期設定のまま（観測地点は低気圧の中心の南300km、時速40km、気温の日変化あり）で再生したときの、3時間ごとの記録です。ページを開いた直後の設定で再生すると、同じ記録になります。</p>
''' + ZTABLE + '''
<p><b>例題1</b>　寒冷前線が観測地点を通過したのは、何日目の何時から何時の間ですか。また、そう考えた理由を2つ答えなさい。<br>
→ 2日目6時から9時の間に、気温が''' + _f1(_R[10]["T"]) + '''℃から''' + _f1(_R[11]["T"]) + '''℃に急に下がり、風向が''' + _R[10]["d"] + '''から''' + _R[11]["d"] + '''（北寄り）に変わっています。　答え <b>2日目6時から9時の間</b>（理由：気温が急に下がった。風向が南寄りから北寄りに変わった。）</p>
<p><b>例題2</b>　温暖前線が通過したのは、何日目の何時から何時の間ですか。<br>
→ 1日目15時から18時の間に、雨がやみ、気温が''' + _f1(_R[5]["T"]) + '''℃から''' + _f1(_R[6]["T"]) + '''℃に上がり、風向が''' + _R[5]["d"] + '''から''' + _R[6]["d"] + '''に変わっています。　答え <b>1日目15時から18時の間</b></p>
<p><b>例題3</b>　シミュレーターの「降水量」のグラフ（1時間ごと）を見て、温暖前線による雨と寒冷前線による雨のちがいを説明しなさい。<br>
→ 温暖前線による雨は1日目''' + str(_WR[0]) + '''時ごろから''' + str(_WR[-1] + 1) + '''時ごろまで約''' + str(len(_WR)) + '''時間続き、1時間あたり最大約''' + "%d" % _jr(_WMAX) + '''mmのおだやかな雨でした（合計約''' + "%d" % _jr(_WSUM) + '''mm）。寒冷前線による雨は2日目''' + str(_CR[0] - 24) + '''時ごろから''' + str(_CR[-1] + 1 - 24) + '''時ごろまでの約''' + str(len(_CR)) + '''時間で、強い時間は1時間に約''' + "%d" % _jr(_CMAX) + '''mmでした（合計約''' + "%d" % _jr(_CSUM) + '''mm）。　答え <b>温暖前線の雨は長時間おだやかに降り、寒冷前線の雨は短時間に強く降った。</b></p>
<p><b>例題4</b>　寒冷前線が通過したあと、気圧と湿度はどう変わりましたか。<br>
→ 気圧は2日目6時の''' + _f1(_R[10]["P"]) + '''hPaが最も低く、その後は上がっています（2日目15時に''' + _f1(_R[13]["P"]) + '''hPa）。湿度は2日目9時に''' + str(_jr(_R[11]["RH"])) + '''％、15時に''' + str(_jr(_R[13]["RH"])) + '''％と、2つの前線の間（暖域）にいたときより低くなっています（乾いた寒気に入ったため）。</p>
''' + P("寒冷前線の通過は、<b>気温の急な低下・風向の北寄りへの変化・短時間の強い雨・気圧の上昇へのきりかわり</b>の4つがそろう時刻をさがします。夜は前線と関係なく気温が下がる（気温の日変化）ので、気温だけでなく風向も合わせて判断します。「気温の日変化」を「入れない」にすると、前線による変化だけを見られます。") + '''
<h3>閉塞前線と停滞前線</h3>
<p>寒冷前線は温暖前線より速く進むことが多く、やがて温暖前線に追いつきます。寒冷前線が温暖前線に追いついた前線を<b>閉塞前線</b>といい、天気図では半円と三角を同じ側に交互につけた線（色つきの図では紫色）で表します。閉塞前線ができると、暖気は上空におし上げられ、低気圧はやがておとろえていくことが多くなります。</p>
<p>寒気と暖気の勢力がほぼ同じで、ほとんど同じ位置にとどまっている前線を<b>停滞前線</b>といい、半円と三角を反対側に交互につけた線（赤と青）で表します。初夏の梅雨前線や、夏から秋に移るころの秋雨前線は停滞前線で、長い期間、雨やくもりの日が続きます。</p>
<p>このシミュレーターでは、前線は形を変えずに低気圧と同じ速さで進むものとしているので、閉塞前線や停滞前線は表示されません。</p>
<h3>天気図記号の読み方</h3>
<p>グラフの上の段は、3時間ごとの天気図記号です。○の中のようすで天気（○快晴、○の中に縦線が晴れ、◎くもり、●雨）を表し、○からのびる棒（矢）は<b>風がふいてくる方位</b>（風向）、棒の先の羽根の数は<b>風力</b>を表します。たとえば棒が北西にのびていれば「北西の風」です。雲量が0〜1なら快晴、2〜8なら晴れ、9〜10ならくもりです。</p>
''' + N("<b>このシミュレーターで単純にしていること</b><br>"
     "・低気圧・前線・高気圧の形と強さ、気温（寒気約10〜12℃、暖気約19℃）、雨の範囲と強さは、教科書の説明に合わせて作ったモデルの値です。実際の前線の天気は、季節や場所によって大きく変わります。<br>"
     "・前線は形を変えずに、低気圧と同じ速さで西から東へ進むものとしています。<br>"
     "・地上の風は、等圧線に対して約30°低気圧側にかたむいてふくとして、気圧の分布から向きを計算しています。風力はモデルによる目安です。<br>"
     "・気温の日変化は、晴れの日は約6℃、雨の日は約1℃の幅（最低は朝6時、最高は14時）としています。湿度は、湿度と雲のでき方シミュレーターと同じ飽和水蒸気量の表を使って計算しています。<br>"
     "・断面図は、高さを横の長さの約50倍に引きのばして表示しています。実際の前線面の傾きはとてもゆるやかで、寒冷前線でおよそ50〜100分の1、温暖前線でおよそ100〜300分の1程度とされます。") + '''
<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「中学校学習指導要領（平成29年告示）解説 理科編」第2分野（4）気象とその変化（''' + A(MEXT_CHU, "中学校学習指導要領解説") + '''）</li>
<li>気象庁「予報用語」気団・前線・気圧配置に関する用語（''' + A("https://www.jma.go.jp/jma/kishou/know/yougo_hp/haichi3.html", "気象庁ホームページ") + '''）</li>
<li>気象庁「天気図」（''' + A("https://www.jma.go.jp/bosai/weather_map/", "気象庁 天気図") + '''）</li>
<li>中学校理科の教科書（東京書籍「新しい科学」、啓林館「未来へひろがるサイエンス」、大日本図書「理科の世界」、学校図書「中学校科学」、教育出版「自然の探究 中学理科」）の第2学年「気象とその変化」の単元</li>
</ul>
''',
    faqs=[("寒冷前線と温暖前線のちがいは何ですか？", "寒冷前線は、寒気が暖気の下にもぐりこみ、暖気をおし上げながら進む前線です。前線面の傾きが急で積乱雲が発達し、せまい範囲に短時間の強い雨が降り、通過後は気温が下がります。温暖前線は、暖気が寒気の上をはい上がりながら進む前線です。前線面の傾きがゆるやかで乱層雲などが広がり、広い範囲に長時間おだやかな雨が降り、通過後は気温が上がります。"),
          ("寒冷前線が通過すると、天気はどう変わりますか？", "短い時間に強い雨が降り（雷や突風をともなうこともあります）、通過後は気温が急に下がり、風向が南寄りから北寄り（北西など）に変わります。気圧は通過するころに最も低くなり、通過後は上がっていきます。"),
          ("温暖前線が通過すると、天気はどう変わりますか？", "前線が近づくと雲がふえ、広い範囲で長い時間おだやかな雨が降ります。通過すると雨がやみ、気温が上がり、風向が東寄り（南東など）から南寄り（南西など）に変わります。"),
          ("気象観測のグラフから、前線が通過した時刻はどう読み取りますか？", "寒冷前線は「気温が急に下がった」「風向が南寄りから北寄りに変わった」「短時間に強い雨が降った」時刻をさがします。気温の変化だけでは、夜に気温が下がる日変化と区別しにくいので、風向や気圧の変化と合わせて判断します。3時間ごとの記録なら「○時から○時の間」と答えます。"),
          ("閉塞前線と停滞前線とは何ですか？", "閉塞前線は、寒冷前線が温暖前線に追いついてできる前線です。停滞前線は、寒気と暖気の勢力がほぼ同じで、ほとんど同じ位置にとどまっている前線で、初夏の梅雨前線や、夏から秋に移るころの秋雨前線がその例です。"),
          ("低気圧のまわりでは、風はどのようにふきますか？", "北半球では、低気圧の中心に向かって反時計回りにふきこみ、中心付近では上昇気流が起こるため雲ができやすくなります。高気圧からは時計回りにふき出し、下降気流が起こるため晴れることが多くなります。")],
    rel=[("kiatsu-jet", "🎢", "気圧ジェットコースター指数"), ("amagumo-now", "🌧️", "いまの雨雲マップ"),
         ("shitsudo-roten", "☁️", "湿度と雲のでき方（露点）"), ("kaminari-alert", "⚡", "今日の雷ゴロゴロ度")],
    js=r'''
  const cv=$('cv'); const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const ctx=cv.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0);
  cv.setAttribute('role','img'); cv.setAttribute('aria-label','温帯低気圧と前線の天気図ふうの図、観測地点を通る西から東への断面図、観測地点の天気・風向・降水量・気温・湿度・気圧の記録グラフ');
  cv.style.cursor='pointer';
  // ---------- モデル（km。x＝東、y＝北、低気圧の中心が原点。式は記事の表を作った Python と同じ）
  const SAT=[@SAT@];
  const sat=(v)=>{ v=clamp(v,0,40); const i=Math.min(39,Math.floor(v)); return SAT[i]+(SAT[i+1]-SAT[i])*(v-i); };
  const ss=(a,b,v)=>{ const u=clamp((v-a)/(b-a),0,1); return u*u*(3-2*u); };
  const lg=(v)=>v<-50?0:1/(1+Math.exp(-v));
  const xwf=(s)=>s*(1.6-0.0006*s), xcf=(s)=>-s*(0.6-0.0003*s);
  const g2=(dx,dy,sg)=>Math.exp(-(dx*dx+dy*dy)/(2*sg*sg));
  function pres(x,y){ const s=-y; let p=1013-17*g2(x,y,520)+8*g2(x-1600,y+150,560)+8*g2(x+1550,y+250,560);
    if(s>0){ const dW=x-xwf(s), dC=x-xcf(s); p-=5.5*ss(0,140,s)*(1-ss(620,820,s))*Math.exp(-Math.sqrt(dW*dW+2025)/240)+7*ss(0,140,s)*(1-ss(820,1020,s))*Math.exp(-Math.sqrt(dC*dC+100)/230); }
    return p; }
  const DIRS=['北','北北東','北東','東北東','東','東南東','南東','南南東','南','南南西','南西','西南西','西','西北西','北西','北北西'];
  const BFT=[0.3,1.6,3.4,5.5,8.0,10.8,13.9,17.2,20.8,24.5,28.5,32.7], CA=Math.cos(2*Math.PI/3), SA=Math.sin(2*Math.PI/3);
  function wind(x,y){ const gx=(pres(x+1,y)-pres(x-1,y))/2, gy=(pres(x,y+1)-pres(x,y-1))/2, g=Math.hypot(gx,gy)||1e-9;
    const vx=(gx*CA-gy*SA)/g, vy=(gx*SA+gy*CA)/g, b=(Math.atan2(-vx,-vy)*180/Math.PI+360)%360, ms=g*0.1/(1.2*8.4e-5)*0.22;
    let bf=0; while(bf<12 && ms>=BFT[bf]) bf++;
    return {vx:vx,vy:vy,b:b,d:DIRS[Math.round(b/22.5)%16],bf:bf}; }
  function rain(x,y){ const s=-y; let r=0;
    if(s>-20){ const sp=Math.max(s,0), dW=x-xwf(sp), Rw=320-0.25*sp; r=(1+3*(1-clamp(dW/Rw,0,1)))*lg(dW/12+1)*lg((Rw-dW)/15)*(1-ss(560,760,s));
      if(s>0){ const dC=x-xcf(s); r=Math.max(r,25*lg((dC+55)/6)*lg((12-dC)/5)*ss(30,140,s)*(1-ss(850,1020,s))); } }
    const bb=3.2*Math.exp(-((x-80)*(x-80)/115200+(y-60)*(y-60)/45000))*ss(-120,0,y); if(bb>0.5) r=Math.max(r,bb);
    return r; }
  function cloud(x,y,r){ const s=-y, dW=x-xwf(s), dC=x-xcf(s), Rw=320-0.25*s; let c=2;
    if(dW>0) c=Math.max(c,2+8*clamp((Rw+300-dW)/150,0,1));
    if(dW<=0 && dC>=0){ c=4; if(dW>-70) c=Math.max(c,4+5*(1+dW/70)); if(dC<90) c=Math.max(c,4+6*Math.min(1,(90-dC)/78)); }
    if(dC<0) c=Math.max(2,2+8*clamp((dC+170)/110,0,1));
    return Math.min(10,Math.max(c,10*clamp(r/0.5,0,1))); }
  function diur(h){ h=((h%24)+24)%24; if(h>=6 && h<=14) return -Math.cos(Math.PI*(h-6)/8); return Math.cos(Math.PI*((((h-14)%24)+24)%24)/16); }
  // ---------- レイアウト（px）
  const KM=4.5, XS=400, XSKM=XS*KM, HB=28, MT=56, MB=232, TRK=MT+50, S0=258, SG=382, ZK=11.4,
        GL=60, GR=598, GW=GR-GL, GTY=408, WY=434, RT=468, RB=496, TT=502, TB=570, PT=578, PB=622;
  const gx=(v)=>GL+v/48*GW, Zs=(z)=>SG-z*ZK;
  const WXN=['快晴','晴れ','くもり','雨','強い雨'];
  // ---------- 状態
  let ys=300, U=40, twf=16, toff=0, diu=true, x0=0, tcf=0, t=0, playing=true, quiz=false, rev=false, guess=null, drag=null, dirty=true, hintT=0, last=performance.now();
  let SER=[], RH1=[], TR=[5,25], PR=[992,1016], WPI=null, CPI=null;
  function geo(){ x0=XSKM-xwf(ys)-U*twf; tcf=(XSKM-x0-xcf(ys))/U; }
  function obs(v){ const x=XSKM-(x0+U*v), y=-ys, Sw=lg(-(x-xwf(ys))/25), Sc=lg(-(x-xcf(ys))/6), r=rain(x,y), c=cloud(x,y,r);
    const Tm=12+toff+7*Sw-9*Sc+(diu?3*(1-0.08*c)*diur(v):0); let Td=6+toff+9*Sw-13*Sc; Td=Math.min(Tm,Td+(Tm-Td)*Math.min(1,r/1.5));
    return {t:v,T:Tm,RH:Math.min(100,sat(Td)/sat(Tm)*100),P:pres(x,y),w:wind(x,y),r:r,c:c,wx:r>=0.5?(r>=10?3:2):(c>=9?1:(c>=2?0:-1))}; }
  function compute(){ geo(); SER=[]; for(let k=0;k<=192;k++) SER.push(obs(k/4));
    RH1=[]; for(let h=0;h<48;h++){ let a=0; for(let q=0;q<=4;q++) a+=SER[h*4+q].r*(q===0||q===4?0.5:1); RH1.push(a/4); }
    let tn=1e9,tx=-1e9,pn=1e9,px=-1e9; SER.forEach((o)=>{ tn=Math.min(tn,o.T); tx=Math.max(tx,o.T); pn=Math.min(pn,o.P); px=Math.max(px,o.P); });
    TR=[Math.floor(tn/5)*5,Math.ceil(tx/5)*5]; if(TR[1]-TR[0]<15) TR[1]=TR[0]+15;
    PR=[Math.floor(pn/4)*4,Math.ceil(px/4)*4]; if(PR[1]-PR[0]<12) PR[1]=PR[0]+12;
    WPI={a:obs(twf-1.5),b:obs(twf+2)}; CPI={a:obs(tcf-1),b:obs(tcf+1.5)}; dirty=true; }
  // ---------- 等圧線と雨の範囲（低気圧といっしょに動くので最初に1回だけ計算）
  const GX0=-3400, GY0=-650, GS=25, NX=257, NY=38, PG=new Float32Array(NX*NY), RG=new Float32Array(NX*NY);
  for(let j=0;j<NY;j++) for(let i=0;i<NX;i++){ PG[j*NX+i]=pres(GX0+i*GS,GY0+j*GS); RG[j*NX+i]=rain(GX0+i*GS,GY0+j*GS); }
  const ISO=[];
  for(let lv=984;lv<=1024;lv+=4){ const sg=[]; let lb=null, bd=1e9;
    for(let j=0;j<NY-1;j++) for(let i=0;i<NX-1;i++){ const a=PG[j*NX+i], b=PG[j*NX+i+1], c=PG[(j+1)*NX+i+1], d=PG[(j+1)*NX+i], x=GX0+i*GS, y=GY0+j*GS, q=[];
      if((a<lv)!==(b<lv)) q.push(x+GS*(lv-a)/(b-a),y);
      if((b<lv)!==(c<lv)) q.push(x+GS,y+GS*(lv-b)/(c-b));
      if((c<lv)!==(d<lv)) q.push(x+GS*(1-(lv-c)/(d-c)),y+GS);
      if((d<lv)!==(a<lv)) q.push(x,y+GS*(1-(lv-d)/(a-d)));
      for(let k=0;k+3<q.length;k+=4){ sg.push(q[k],q[k+1],q[k+2],q[k+3]); const mx=(q[k]+q[k+2])/2, my=(q[k+1]+q[k+3])/2;
        if(mx>-1300 && mx<-60 && my>60 && my<220 && Math.abs(my-140)<bd){ bd=Math.abs(my-140); lb=[mx,my]; } } }
    if(sg.length) ISO.push({lv:lv,sg:sg,lb:lb}); }
  const RC=document.createElement('canvas'); RC.width=NX; RC.height=NY;
  function mkRain(){ const c2=RC.getContext('2d'), im=c2.createImageData(NX,NY);
    for(let j=0;j<NY;j++) for(let i=0;i<NX;i++){ const r=RG[j*NX+i]; if(r<0.3) continue; const o=((NY-1-j)*NX+i)*4, k=clamp((r-3)/9,0,1);
      im.data[o]=Math.round(120-85*k); im.data[o+1]=Math.round(180-90*k); im.data[o+2]=Math.round(250-15*k); im.data[o+3]=Math.round(255*clamp((r-0.3)/0.5,0,1)*(0.45+0.3*k)); }
    c2.putImageData(im,0,0); }
  mkRain();
  const WFL=[], CFL=[]; for(let s=0;s<=740;s+=10) WFL.push([xwf(s),-s]); for(let s=0;s<=940;s+=10) CFL.push([xcf(s),-s]);
  const LOWP=pres(0,0), HIGHS=[[1600,-150,pres(1600,-150)],[-1550,-250,pres(-1550,-250)]];
  // ---------- 描画の道具
  const f1=(v)=>(Math.round(v*10)/10).toFixed(1);
  const line=(a,b,c,d)=>{ ctx.beginPath(); ctx.moveTo(a,b); ctx.lineTo(c,d); ctx.stroke(); };
  function txt(s,x,y,font,col,al,halo){ ctx.font=font; ctx.textAlign=al||'left'; if(halo){ ctx.lineJoin='round'; ctx.lineWidth=3.5; ctx.strokeStyle='rgba(255,255,255,.95)'; ctx.strokeText(s,x,y); } ctx.fillStyle=col; ctx.fillText(s,x,y); }
  function tw(s,font){ ctx.font=font; return ctx.measureText(s).width; }
  function rr(x,y,w,h,r){ ctx.beginPath(); ctx.moveTo(x+r,y); ctx.lineTo(x+w-r,y); ctx.quadraticCurveTo(x+w,y,x+w,y+r); ctx.lineTo(x+w,y+h-r); ctx.quadraticCurveTo(x+w,y+h,x+w-r,y+h); ctx.lineTo(x+r,y+h); ctx.quadraticCurveTo(x,y+h,x,y+h-r); ctx.lineTo(x,y+r); ctx.quadraticCurveTo(x,y,x+r,y); ctx.closePath(); }
  function arrow(x1,y1,x2,y2,hs){ line(x1,y1,x2,y2); const a=Math.atan2(y2-y1,x2-x1), h=hs||6; ctx.beginPath(); ctx.moveTo(x2,y2); ctx.lineTo(x2-h*Math.cos(a-0.45),y2-h*Math.sin(a-0.45)); ctx.lineTo(x2-h*Math.cos(a+0.45),y2-h*Math.sin(a+0.45)); ctx.closePath(); ctx.fill(); }
  function lab(id){ const s=$(id), l=$(id+'L'); if(l) l.textContent = s.dataset.fmt ? s.dataset.fmt.replace('{v}', s.value) : s.value; }
  function tfmt(v){ const m=Math.round(v*4)*15, d=Math.floor(m/1440), r=m-d*1440, mi=r%60; return (d+1)+'日目 '+Math.floor(r/60)+':'+(mi<10?'0':'')+mi; }
  // ---------- 上：いまの観測値
  function drawHead(o){ ctx.fillStyle='#f1f5f9'; rr(1,1,W-2,HB-2,8); ctx.fill();
    const L=[[tfmt(o.t),'#0f172a'],['気温 '+f1(o.T)+'℃','#dc2626'],['湿度 '+Math.round(o.RH)+'%','#15803d'],['気圧 '+f1(o.P)+'hPa','#1d4ed8'],[o.w.d+'の風 風力'+o.w.bf,'#334155'],[WXN[o.wx+1],'#0f172a']];
    let font='bold 13px sans-serif', tot=0; L.forEach((p)=>{ tot+=tw(p[0],font); }); if(tot>W-70){ font='bold 12px sans-serif'; tot=0; L.forEach((p)=>{ tot+=tw(p[0],font); }); }
    const gap=(W-20-tot)/(L.length-1); let x=10; L.forEach((p)=>{ txt(p[0],x,19,font,p[1]); x+=tw(p[0],font)+gap; }); }
  // ---------- 天気図ふうの図
  function front(L,col,cold,X,Y){ const Pp=L.map((p)=>[X(p[0]),Y(p[1])]);
    ctx.strokeStyle=col; ctx.lineWidth=2.6; ctx.lineJoin='round'; ctx.beginPath(); Pp.forEach((p,i)=>{ if(i) ctx.lineTo(p[0],p[1]); else ctx.moveTo(p[0],p[1]); }); ctx.stroke();
    ctx.fillStyle=col; let dist=0, next=14;
    for(let k=1;k<Pp.length;k++){ const ax=Pp[k-1][0], ay=Pp[k-1][1], bx=Pp[k][0], by=Pp[k][1], L2=Math.hypot(bx-ax,by-ay); if(L2<1e-6) continue; const tx=(bx-ax)/L2, ty=(by-ay)/L2, nx=ty, ny=-tx;
      while(next<=dist+L2){ const u=next-dist, px=ax+tx*u, py=ay+ty*u;
        if(px>-10 && px<W+10 && py>MT-10 && py<MB+10){ ctx.beginPath(); if(cold){ ctx.moveTo(px-tx*5.5,py-ty*5.5); ctx.lineTo(px+nx*8.5,py+ny*8.5); ctx.lineTo(px+tx*5.5,py+ty*5.5); } else { const a=Math.atan2(ty,tx); ctx.moveTo(px+tx*5.5,py+ty*5.5); ctx.arc(px,py,5.5,a,a-Math.PI,true); } ctx.closePath(); ctx.fill(); }
        next+=24; }
      dist+=L2; } }
  function drawMap(t){ const xc=x0+U*t, X=(x)=>(xc+x)/KM, Y=(y)=>TRK-y/KM, hide=quiz&&!rev;
    txt('天気図ふうの図（上が北）',6,MT-7,'bold 13px sans-serif','#0f172a');
    let lx=W-6; [['ins','等圧線（4hPaごと）'],['rain','雨の範囲'],['cf','寒冷前線'],['wf','温暖前線']].forEach((g)=>{ const w=tw(g[1],'11px sans-serif'); txt(g[1],lx-w,MT-8,'11px sans-serif','#334155'); lx-=w+4;
      if(g[0]==='ins'){ ctx.strokeStyle='#475569'; ctx.lineWidth=1.2; line(lx-16,MT-12,lx,MT-12); lx-=16; }
      else if(g[0]==='rain'){ ctx.fillStyle='rgba(96,165,250,.6)'; ctx.fillRect(lx-14,MT-17,14,10); lx-=14; }
      else if(g[0]==='cf'){ ctx.strokeStyle='#2563eb'; ctx.lineWidth=2.2; line(lx-18,MT-11,lx,MT-11); ctx.fillStyle='#2563eb'; ctx.beginPath(); ctx.moveTo(lx-14,MT-11); ctx.lineTo(lx-9,MT-19); ctx.lineTo(lx-4,MT-11); ctx.closePath(); ctx.fill(); lx-=18; }
      else { ctx.strokeStyle='#dc2626'; ctx.lineWidth=2.2; line(lx-18,MT-11,lx,MT-11); ctx.fillStyle='#dc2626'; ctx.beginPath(); ctx.arc(lx-9,MT-11,4.5,Math.PI,0); ctx.closePath(); ctx.fill(); lx-=18; }
      lx-=12; });
    ctx.save(); ctx.beginPath(); ctx.rect(0,MT,W,MB-MT); ctx.clip();
    ctx.fillStyle='#f8fafc'; ctx.fillRect(0,MT,W,MB-MT);
    if(!hide){
      ctx.imageSmoothingEnabled=true; ctx.drawImage(RC,X(GX0-GS/2),Y(GY0+(NY-0.5)*GS),NX*GS/KM,NY*GS/KM);
      ISO.forEach((Lv)=>{ const s=Lv.sg; ctx.beginPath(); for(let k=0;k<s.length;k+=4){ ctx.moveTo(X(s[k]),Y(s[k+1])); ctx.lineTo(X(s[k+2]),Y(s[k+3])); } ctx.strokeStyle=Lv.lv%20===0?'#334155':'#64748b'; ctx.lineWidth=Lv.lv%20===0?1.5:0.9; ctx.stroke(); });
      ctx.strokeStyle='rgba(71,85,105,.5)'; ctx.fillStyle='rgba(71,85,105,.5)'; ctx.lineWidth=1.3;
      for(let ax=40; ax<W; ax+=80) for(let ay=MT+24; ay<MB-6; ay+=50){ const w=wind(ax*KM-xc,(TRK-ay)*KM); arrow(ax-w.vx*8,ay+w.vy*8,ax+w.vx*8,ay-w.vy*8,5); }
      front(WFL,'#dc2626',false,X,Y); front(CFL,'#2563eb',true,X,Y);
      ISO.forEach((Lv)=>{ if(Lv.lb){ const a=X(Lv.lb[0]), b=Y(Lv.lb[1]); if(a>14 && a<W-14 && b>MT+8 && b<MB-6) txt(String(Lv.lv),a,b+4,'bold 10px sans-serif','#334155','center',true); } });
      const lcx=X(0), lcy=Y(0); ctx.strokeStyle='#dc2626'; ctx.lineWidth=2.4; line(lcx-5,lcy-5,lcx+5,lcy+5); line(lcx-5,lcy+5,lcx+5,lcy-5);
      txt('低',lcx,lcy-9,'bold 18px sans-serif','#dc2626','center',true); txt(String(Math.round(LOWP)),lcx+9,lcy+15,'bold 11px sans-serif','#b91c1c','left',true);
      HIGHS.forEach((h)=>{ const a=X(h[0]), b=Y(h[1]); if(a>-20 && a<W+20){ txt('高',a,b+6,'bold 18px sans-serif','#2563eb','center',true); txt(String(Math.round(h[2])),a,b+21,'bold 11px sans-serif','#1d4ed8','center',true); } });
    } else {
      ctx.fillStyle='#e2e8f0'; ctx.fillRect(0,MT,W,MB-MT);
      txt('読み取り練習中：前線と雨の範囲はかくしています',W/2,(MT+MB)/2-34,'bold 14px sans-serif','#475569','center');
      txt('下のグラフをタップして答えを選び、「✔ 答えを見る」をおしてください',W/2,(MT+MB)/2-14,'12px sans-serif','#475569','center'); }
    const sy=Y(-ys); ctx.setLineDash([6,4]); ctx.strokeStyle='#0f766e'; ctx.lineWidth=1.4; line(0,sy,W,sy); ctx.setLineDash([]);
    txt('断面図の線',6,sy-5,'bold 11px sans-serif','#0f766e','left',true);
    ctx.fillStyle='#fff'; ctx.strokeStyle='#0f172a'; ctx.lineWidth=2.4; ctx.beginPath(); ctx.arc(XS,sy,7,0,Math.PI*2); ctx.fill(); ctx.stroke(); ctx.fillStyle='#0f172a'; ctx.beginPath(); ctx.arc(XS,sy,2.6,0,Math.PI*2); ctx.fill();
    txt('観測地点',XS+11,sy-8,'bold 12px sans-serif','#0f172a','left',true);
    if(!quiz) txt('地図を上下になぞると、観測地点を南北に動かせます',6,MB-8,'10.5px sans-serif','#475569','left',true);
    const sbx=W-128, sby=MB-9; ctx.strokeStyle='#0f172a'; ctx.lineWidth=2; line(sbx,sby,sbx+500/KM,sby); line(sbx,sby-4,sbx,sby+2); line(sbx+500/KM,sby-4,sbx+500/KM,sby+2); txt('500 km',sbx+250/KM,sby-5,'10px sans-serif','#0f172a','center',true);
    ctx.restore(); ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1; ctx.strokeRect(0.5,MT+0.5,W-1,MB-MT-1); }
  // ---------- 断面図
  function blob(L,fill,stroke,lw){ ctx.beginPath(); L.forEach((c)=>{ ctx.moveTo(c[0]+c[2],c[1]); if(c.length>3) ctx.ellipse(c[0],c[1],c[2],c[3],0,0,Math.PI*2); else ctx.arc(c[0],c[1],c[2],0,Math.PI*2); }); ctx.lineWidth=lw; ctx.strokeStyle=stroke; ctx.stroke(); ctx.fillStyle=fill; ctx.fill(); }
  function streaks(x1,x2,step,zf,col,len,ph){ if(x2<-5 || x1>W+5) return; ctx.strokeStyle=col; ctx.lineWidth=1.3; ctx.beginPath();
    for(let p=Math.max(x1,-4);p<=Math.min(x2,W+4);p+=step){ const top=Zs(zf(p)), h=SG-top; if(h<6) continue; for(let k=0;k<3;k++){ const y=top+((k*h/3+p*7.3+ph)%h); ctx.moveTo(p,y); ctx.lineTo(p-1.6,Math.min(SG,y+len)); } }
    ctx.stroke(); }
  function drawSec(t,ph){ const xc=x0+U*t, X=(x)=>(xc+x)/KM, Xw=X(xwf(ys)), Xc=X(xcf(ys)), Rw=320-0.25*ys, hide=quiz&&!rev;
    const zw=(p)=>clamp((p-Xw)*KM/180,0,10.6), zc=(p)=>clamp((Xc-p)*KM/60,0,10.6);
    txt('断面図（観測地点を通る西→東の線・高さは約50倍）',6,S0-7,'bold 13px sans-serif','#0f172a');
    { let lx=W-6; [['温暖前線の前線面','#dc2626'],['寒冷前線の前線面','#2563eb']].forEach((g)=>{ const w=tw(g[0],'11px sans-serif'); txt(g[0],lx-w,S0-8,'11px sans-serif','#334155'); lx-=w+4; ctx.strokeStyle=g[1]; ctx.lineWidth=2.4; line(lx-16,S0-7,lx-2,S0-15); lx-=30; }); }
    ctx.save(); ctx.beginPath(); ctx.rect(0,S0,W,SG-S0+6); ctx.clip();
    ctx.fillStyle='#fff7ed'; ctx.fillRect(0,S0,W,SG-S0);
    if(!hide){
      ctx.fillStyle='#dbeafe';
      if(Xw<W+10){ const a=Math.max(Xw,-30); ctx.beginPath(); ctx.moveTo(a,SG); for(let p=a;p<=W+12;p+=6) ctx.lineTo(p,Zs(zw(p))); ctx.lineTo(W+12,SG); ctx.closePath(); ctx.fill(); }
      if(Xc>-10){ const a=Math.min(Xc,W+30); ctx.beginPath(); ctx.moveTo(a,SG); for(let p=a;p>=-12;p-=4) ctx.lineTo(p,Zs(zc(p))); ctx.lineTo(-12,SG); ctx.closePath(); ctx.fill(); }
      ctx.lineWidth=2.4; ctx.strokeStyle='#dc2626'; line(Xw,SG,Xw+10.6*180/KM,Zs(10.6)); ctx.strokeStyle='#2563eb'; line(Xc,SG,Xc-10.6*60/KM,Zs(10.6));
      const b1=X(xwf(ys)+Rw), a2=X(xwf(ys)+Rw*0.55), b2=X(xwf(ys)+Rw+200), a3=X(xwf(ys)+Rw+110), b3=X(xwf(ys)+Rw+330);
      if(b3>-10 && a3<W+10){ ctx.lineCap='round'; for(let k=0;k<3;k++){ const yy=Zs(7.7+k*0.45), xa=a3+k*14, xb=b3-k*18; ctx.beginPath(); ctx.moveTo(xa,yy); ctx.quadraticCurveTo((xa+xb)/2,yy-6,xb,yy+2); ctx.strokeStyle='#cbd5e1'; ctx.lineWidth=5; ctx.stroke(); ctx.strokeStyle='#fff'; ctx.lineWidth=3; ctx.stroke(); } ctx.lineCap='butt';
        txt('巻層雲・巻雲',clamp((a3+b3)/2,40,W-70),Zs(9.3),'bold 11px sans-serif','#475569','center',true); }
      if(b2>-10 && a2<W+10){ ctx.beginPath(); ctx.moveTo(a2,Zs(6.1)); for(let p=a2;p<=b2;p+=6) ctx.lineTo(p,Zs(6.1-0.5*(p-a2)/(b2-a2))+2*Math.sin(p*0.3)); for(let p=b2;p>=a2;p-=6) ctx.lineTo(p,Zs(Math.max(zw(p)+0.9,3.4))); ctx.closePath();
        ctx.fillStyle='#e2e8f0'; ctx.fill(); ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1; ctx.stroke(); txt('高層雲',clamp((a2+b2)/2+14,40,W-30),Zs(4.9),'bold 11px sans-serif','#475569','center',true); }
      const a1=Xw-8;
      if(b1+8>-10 && a1<W+10){ ctx.beginPath(); ctx.moveTo(a1,Zs(0.5)); ctx.quadraticCurveTo(a1-6,Zs(3.4),a1+6,Zs(5.2)); for(let p=a1+6;p<=b1+8;p+=4) ctx.lineTo(p,Zs(5.3-0.9*(p-a1)/Math.max(1,b1+8-a1))-2.2*Math.abs(Math.sin(p*0.12))); for(let p=b1+8;p>=a1;p-=5) ctx.lineTo(p,Zs(zw(p)+0.45)); ctx.closePath();
        ctx.fillStyle='#94a3b8'; ctx.fill(); ctx.strokeStyle='#64748b'; ctx.lineWidth=1.2; ctx.stroke();
        streaks(Xw-2,b1,5,(p)=>zw(p)+0.45,'rgba(37,99,235,.6)',6,ph);
        if(b1-a1>44) txt('乱層雲',clamp((a1+b1)/2,a1+26,W-30),Zs(3.1),'bold 12px sans-serif','#ffffff','center'); }
      const wsec=Xw-Xc; if(wsec>90){ [0.3,0.62].forEach((f,i)=>{ const px=Xc+wsec*f; if(px>-20 && px<W+20) blob([[px-6,Zs(1.5),6],[px+5,Zs(1.55),6.5],[px,Zs(2.0),7]],'#ffffff','#cbd5e1',2); }); }
      if(Xc-40>-20 && Xc-40<W+20) blob([[Xc-46,Zs(1.4),5.5],[Xc-36,Zs(1.45),6],[Xc-41,Zs(1.85),6.5]],'#ffffff','#cbd5e1',2);
      const cx=Xc-4;
      if(cx>-90 && cx<W+40){ streaks(X(xcf(ys)-55),X(xcf(ys)+12),2.2,()=>1.2,'rgba(30,64,175,.85)',8,ph*1.6);
        const L=[[cx-7,Zs(1.6),11],[cx+7,Zs(1.8),10],[cx-2,Zs(3.1),13.5],[cx+3,Zs(4.6),14],[cx-3,Zs(6.1),14],[cx+2,Zs(7.5),13],[cx,Zs(8.7),12]];
        L.push([cx+24,Zs(9.75),50,7.5]); for(let k=0;k<5;k++) L.push([cx-14+k*16,Zs(10.0),6.5]);
        blob(L,'#ffffff','#94a3b8',3); txt('積乱雲',cx+36,Zs(6.4),'bold 12px sans-serif','#334155','center',true); }
      if(Xc>40){ const lx=Math.max(28,Xc-110); txt('寒気',lx,Zs(Math.min(2,zc(lx)*0.45))+5,'bold 13px sans-serif','#1d4ed8','center',true); }
      if(Xw<W-40){ let lx=Math.min(W-28,Xw+150); if(Math.abs(lx-XS)<75) lx=(XS+85<W-24)?XS+85:XS-70; if(lx>Xw+20) txt('寒気',lx,Zs(Math.min(1.2,zw(lx)*0.4))+5,'bold 13px sans-serif','#1d4ed8','center',true); }
      const wa=Math.max(Xc,0), wb=Math.min(Xw,W); if(wb-wa>70) txt('暖気',(wa+wb)/2,Zs(3.0),'bold 13px sans-serif','#c2410c','center',true); else txt('暖気',clamp((Xc+Xw)/2,40,W-40),Zs(8.4),'bold 13px sans-serif','#c2410c','center',true);
      ctx.lineWidth=2.4;
      if(Xc>20 && Xc<W+40){ ctx.strokeStyle='#1d4ed8'; ctx.fillStyle='#1d4ed8'; arrow(Xc-60,Zs(0.6),Xc-16,Zs(0.6)); ctx.strokeStyle='#ea580c'; ctx.fillStyle='#ea580c'; arrow(Xc+18,Zs(0.5),Xc-2,Zs(4.4)); }
      if(Xw>-60 && Xw<W-20){ ctx.strokeStyle='#ea580c'; ctx.fillStyle='#ea580c'; arrow(Xw-34,Zs(1.0),Xw+62,Zs(zw(Xw+62)+1.1)); }
    } else { ctx.fillStyle='#e2e8f0'; ctx.fillRect(0,S0,W,SG-S0); txt('読み取り練習中：断面図はかくしています',W/2,(S0+SG)/2,'bold 13px sans-serif','#475569','center'); }
    ctx.fillStyle='#a8a29e'; ctx.fillRect(0,SG,W,6);
    ctx.strokeStyle='#0f172a'; ctx.lineWidth=2; line(XS,SG,XS,SG-17); ctx.fillStyle='#0f766e'; ctx.beginPath(); ctx.moveTo(XS,SG-17); ctx.lineTo(XS+11,SG-13.5); ctx.lineTo(XS,SG-10); ctx.closePath(); ctx.fill();
    txt('観測地点',XS+13,SG-4,'bold 11px sans-serif','#0f172a','left',true);
    ctx.strokeStyle='#64748b'; ctx.lineWidth=1; [0,5,10].forEach((z)=>{ line(0,Zs(z),5,Zs(z)); if(z) txt(z+'km',7,Zs(z)+4,'10px sans-serif','#475569','left',true); });
    txt('西',46,S0+15,'bold 12px sans-serif','#334155','left',true); txt('東',W-8,S0+15,'bold 12px sans-serif','#334155','right',true);
    ctx.restore(); ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1; ctx.strokeRect(0.5,S0+0.5,W-1,SG-S0+5); }
  // ---------- 観測記録のグラフ
  function wsym(x,y,o){ const r=6.2, b=o.w.b*Math.PI/180, ux=Math.sin(b), uy=-Math.cos(b), L=13;
    ctx.strokeStyle='#0f172a'; ctx.lineWidth=1.5;
    if(o.w.bf>0){ line(x+ux*r,y+uy*r,x+ux*(r+L),y+uy*(r+L)); const px=-uy, py=ux;
      for(let k=0;k<Math.min(12,o.w.bf);k++){ const sd=k<6?1:-1, d=r+L-(k%6)*2.7, qx=x+ux*d, qy=y+uy*d; line(qx,qy,qx+px*5.2*sd-ux*2.2,qy+py*5.2*sd-uy*2.2); } }
    const rad=o.wx===3?7.6:r; ctx.beginPath(); ctx.arc(x,y,rad,0,Math.PI*2); ctx.fillStyle=o.wx>=2?'#0f172a':'#fff'; ctx.fill(); ctx.stroke();
    if(o.wx===0) line(x,y-r,x,y+r); else if(o.wx===1){ ctx.beginPath(); ctx.arc(x,y,r*0.48,0,Math.PI*2); ctx.stroke(); } }
  function drawGraph(t,o){ const tm=quiz?48:t, hid=quiz&&!rev;
    if(!quiz){ let msg=null, col=null;
      if(t>=tcf && t<tcf+3){ msg='寒冷前線が通過：強い雨のあと気温が'+f1(CPI.a.T)+'℃→'+f1(CPI.b.T)+'℃、風向は'+CPI.a.w.d+'→'+CPI.b.w.d; col='#1d4ed8'; }
      else if(t>=twf && t<twf+3){ msg='温暖前線が通過：雨がやみ、気温が'+f1(WPI.a.T)+'℃→'+f1(WPI.b.T)+'℃、風向は'+WPI.a.w.d+'→'+WPI.b.w.d; col='#b91c1c'; }
      if(msg){ const font='bold 12.5px sans-serif', w=tw(msg,font)+20; ctx.fillStyle=col; rr(2,GTY-15,Math.min(W-4,w),21,7); ctx.fill(); txt(msg,12,GTY,font,'#fff'); }
      else txt('観測地点の記録（3時間ごとの天気記号・1時間ごとの降水量・気温・湿度・気圧）',6,GTY,'bold 12.5px sans-serif','#0f172a'); }
    else if(hintT && performance.now()-hintT<2000) txt('先にグラフをタップして、答えの時刻を選んでください',6,GTY,'bold 12.5px sans-serif','#b91c1c');
    else if(!rev) txt(guess===null?'練習：寒冷前線が通過したのはいつ？　グラフをタップして答えよう':'あなたの答え：'+tfmt(guess)+'ごろ　→「✔ 答えを見る」で確かめよう',6,GTY,'bold 12.5px sans-serif','#c2410c');
    else { const d=Math.abs(guess-tcf); txt((d<=1?'正解！ ':(d<=3?'おしい！ ':'もう一度グラフを見てみよう。'))+'寒冷前線の通過は '+tfmt(tcf)+'ごろ（あなたの答えとの差 '+f1(d)+'時間）',6,GTY,'bold 12.5px sans-serif',d<=1?'#15803d':'#c2410c'); }
    for(let h=0;h<=48;h+=3){ const x=gx(h); ctx.strokeStyle=h%24===0?'rgba(15,23,42,.35)':(h%6===0?'rgba(15,23,42,.13)':'rgba(15,23,42,.06)'); ctx.lineWidth=1; line(x,RT-4,x,PB); }
    ctx.strokeStyle='#cbd5e1'; ctx.lineWidth=1; ctx.strokeRect(GL+0.5,RT+0.5,GW,RB-RT); ctx.strokeRect(GL+0.5,TT+0.5,GW,TB-TT); ctx.strokeRect(GL+0.5,PT+0.5,GW,PB-PT);
    txt('天気',4,WY-1,'bold 11px sans-serif','#0f172a'); txt('風向',4,WY+13,'bold 11px sans-serif','#0f172a');
    txt('降水量',4,RT+10,'bold 11px sans-serif','#1d4ed8'); txt('（mm）',2,RT+21,'9.5px sans-serif','#475569');
    txt('気温',4,TT+12,'bold 11px sans-serif','#dc2626'); txt('（℃）',2,TT+24,'9.5px sans-serif','#dc2626');
    txt('湿度',4,TT+46,'bold 11px sans-serif','#15803d'); txt('（％）',2,TT+58,'9.5px sans-serif','#15803d');
    txt('気圧',4,PT+14,'bold 11px sans-serif','#1d4ed8'); txt('（hPa）',2,PT+26,'9.5px sans-serif','#1d4ed8');
    const TY=(v)=>TB-3-(v-TR[0])/(TR[1]-TR[0])*(TB-TT-6), HY=(v)=>TB-3-v/100*(TB-TT-6), PY=(v)=>PB-3-(v-PR[0])/(PR[1]-PR[0])*(PB-PT-6);
    ctx.strokeStyle='rgba(15,23,42,.06)'; for(let v=TR[0];v<=TR[1];v+=5){ line(GL,TY(v),GR,TY(v)); txt(String(v),GL-4,TY(v)+4,'10px sans-serif','#b91c1c','right'); }
    [0,50,100].forEach((v)=>txt(v+'%',GR+4,HY(v)+4,'10px sans-serif','#15803d','left'));
    const pst=Math.max(4,Math.ceil((PR[1]-PR[0])/8)*4); for(let v=PR[0];v<=PR[1];v+=pst) txt(String(v),GR+4,PY(v)+4,'10px sans-serif','#1d4ed8','left');
    txt('25',GR+4,RT+9,'10px sans-serif','#1d4ed8','left'); txt('0',GR+4,RB+3,'10px sans-serif','#1d4ed8','left');
    for(let h=0;h<48;h++){ if(h+1>tm+1e-6) break; const v=RH1[h]; if(v<0.1) continue; const bh=Math.max(2,Math.min(1,v/25)*(RB-RT-2)); ctx.fillStyle=v>=10?'#1d4ed8':'#60a5fa'; ctx.fillRect(gx(h)+1,RB-bh,GW/48-2,bh); }
    function plot(fn,Yf,col,lw){ ctx.strokeStyle=col; ctx.lineWidth=lw; ctx.lineJoin='round'; ctx.beginPath(); let n=0; for(let k=0;k<=192;k++){ if(k/4>tm+1e-9) break; const x=gx(k/4), y=Yf(fn(SER[k])); if(n++) ctx.lineTo(x,y); else ctx.moveTo(x,y); } if(!quiz && n && tm<48) ctx.lineTo(gx(tm),Yf(fn(o))); ctx.stroke(); }
    plot((q)=>q.RH,HY,'#22c55e',1.6); plot((q)=>q.T,TY,'#dc2626',2.4); plot((q)=>q.P,PY,'#2563eb',2.2);
    for(let k=0;k<=16;k++){ const v=k*3; if(v>tm+1e-9) break; const q=SER[k*12]; wsym(gx(v),WY,q); txt(q.w.d,gx(v),WY+28,'9.5px sans-serif','#334155','center'); }
    if(!quiz || rev){ [[twf,'#dc2626','温暖前線の通過'],[tcf,'#2563eb','寒冷前線の通過']].forEach((q)=>{ if(!quiz && t<q[0]) return; const x=gx(q[0]), rt=x>GR-90; ctx.setLineDash([5,4]); ctx.strokeStyle=q[1]; ctx.lineWidth=1.8; line(x,RT-6,x,PB); ctx.setLineDash([]); txt(q[2],x+(rt?-4:4),RT+12,'bold 11px sans-serif',q[1],rt?'right':'left',true); }); }
    if(quiz && guess!==null){ const x=gx(guess), rt=x>GR-90; ctx.strokeStyle='#ea580c'; ctx.lineWidth=2.6; line(x,RT-6,x,PB); txt('あなたの答え',x+(rt?-4:4),PT+12,'bold 11px sans-serif','#c2410c',rt?'right':'left',true); }
    if(!quiz || rev){ const x=gx(t); ctx.strokeStyle='rgba(15,23,42,.6)'; ctx.lineWidth=1.2; line(x,WY-18,x,PB);
      if(!quiz && t>0.4){ const rt=x>GR-60; let yT=TY(o.T)-5, yH=HY(o.RH)+12; if(Math.abs(yT-yH)<13){ if(yT<yH) yH=yT+13; else yH=yT-13; } txt(f1(o.T)+'℃',x+(rt?-5:5),yT,'bold 11px sans-serif','#dc2626',rt?'right':'left',true); txt(Math.round(o.RH)+'%',x+(rt?-5:5),yH,'bold 10px sans-serif','#15803d',rt?'right':'left',true); txt(f1(o.P),x+(rt?-5:5),PY(o.P)-4,'bold 10px sans-serif','#1d4ed8',rt?'right':'left',true); } }
    if(!quiz && t<0.3) txt('▶ 再生すると、観測地点の記録がここにかかれていきます',GL+GW/2,(TT+TB)/2+4,'bold 13px sans-serif','#64748b','center');
    for(let h=0;h<=48;h+=6) txt((h%24)+'時',gx(h),PB+14,'10px sans-serif','#475569','center');
    ['1日目','2日目'].forEach((s,i)=>{ const a=gx(i*24), b=gx(i*24+24); ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1; line(a+3,PB+24,b-3,PB+24); line(a+3,PB+20,a+3,PB+28); line(b-3,PB+20,b-3,PB+28); txt(s,(a+b)/2,PB+28,'bold 11px sans-serif','#334155','center',true); }); }
  // ---------- まとめて描く
  function draw(ph){ const o=obs(t); ctx.clearRect(0,0,W,H); ctx.fillStyle='#fff'; ctx.fillRect(0,0,W,H);
    drawHead(o); drawMap(t); drawSec(t,ph); drawGraph(t,o);
    setStat('sTime',tfmt(t)); setStat('sT',f1(o.T)+'℃'); setStat('sRH',Math.round(o.RH)+'%'); setStat('sP',f1(o.P)+' hPa'); setStat('sW',o.w.d+'（'+o.w.bf+'）'); setStat('sWx',WXN[o.wx+1]);
    const hid=quiz&&!rev; setStat('sWf',hid?'？':tfmt(twf)); setStat('sCf',hid?'？':tfmt(tcf));
    setShare(hid?'【前線の読み取り練習】気象観測の記録グラフから、寒冷前線が通過した時刻を当てよう｜シミュラボ'
      :'【前線と天気】寒冷前線が'+tfmt(tcf)+'ごろ通過し、気温'+f1(CPI.a.T)+'℃→'+f1(CPI.b.T)+'℃、風向'+CPI.a.w.d+'→'+CPI.b.w.d+'に。温暖前線の通過（'+tfmt(twf)+'ごろ）では雨がやんで気温が上がった｜シミュラボ'); }
  // ---------- 操作
  function tog(){ $('play').textContent=playing?'⏸ 一時停止':'▶ 再生'; }
  function syncT(){ $('tt').value=t; $('ttL').textContent=tfmt(t); }
  function btnVis(){ $('play').style.display=quiz?'none':''; $('rew').style.display=quiz?'none':''; $('ans').style.display=quiz?'':'none'; }
  function resetQuiz(){ rev=false; guess=null; if(quiz){ playing=false; t=48; } }
  function setYs(py){ const v=clamp(Math.round((py-TRK)*KM/10)*10,200,500); if(v!==ys){ ys=v; $('ys').value=ys; lab('ys'); compute(); } }
  function setT(px){ const v=Math.round(clamp((px-GL)/GW*48,0,48)*4)/4; if(quiz && !rev) guess=v; else { playing=false; tog(); } t=v; syncT(); dirty=true; }
  function pxy(e){ const p=cpos(cv,e); return [p[0]/dpr,p[1]/dpr]; }
  cv.addEventListener('pointerdown',(e)=>{ const q=pxy(e);
    if(q[1]>=MT && q[1]<=MB){ if(quiz) return; drag='map'; setYs(q[1]); }
    else if(q[1]>=WY-20 && q[1]<=PB+8 && q[0]>=GL-12 && q[0]<=GR+12){ drag='graph'; setT(q[0]); }
    else return;
    try{ cv.setPointerCapture(e.pointerId); }catch(err){ } e.preventDefault(); });
  cv.addEventListener('pointermove',(e)=>{ if(!drag) return; const q=pxy(e); if(drag==='map') setYs(q[1]); else setT(q[0]); });
  ['pointerup','pointercancel'].forEach((n)=>cv.addEventListener(n,()=>{ drag=null; }));
  $('tt').addEventListener('input',()=>{ t=+$('tt').value; if(quiz && !rev) guess=t; else { playing=false; tog(); } $('ttL').textContent=tfmt(t); dirty=true; });
  $('ys').addEventListener('input',()=>{ ys=+$('ys').value; compute(); resetQuiz(); syncT(); });
  $('uu').addEventListener('input',()=>{ U=+$('uu').value; compute(); resetQuiz(); syncT(); });
  $('diu').addEventListener('change',()=>{ diu=$('diu').value==='on'; compute(); });
  $('mode').addEventListener('change',()=>{ quiz=$('mode').value==='quiz'; rev=false; guess=null; if(quiz){ playing=false; t=48; } else { t=0; playing=true; } btnVis(); tog(); syncT(); dirty=true; });
  $('play').addEventListener('click',()=>{ if(!playing && t>=48-1e-6) t=0; playing=!playing; tog(); dirty=true; });
  $('rew').addEventListener('click',()=>{ t=0; playing=true; tog(); syncT(); dirty=true; });
  $('rand').addEventListener('click',()=>{ ys=Math.round(rnd(20,48))*10; U=Math.round(rnd(6,12))*5; toff=Math.round(rnd(-2,3)); twf=Math.round(rnd(8,19)*4)/4;
    twf=Math.max(5,Math.min(twf,Math.floor((44-(xwf(ys)-xcf(ys))/U)*4)/4));
    $('ys').value=ys; lab('ys'); $('uu').value=U; lab('uu'); compute(); rev=false; guess=null; if(quiz){ t=48; playing=false; } else { t=0; playing=true; } tog(); syncT(); });
  $('ans').addEventListener('click',()=>{ if(guess===null){ hintT=performance.now(); dirty=true; return; } rev=true; t=tcf; syncT(); dirty=true; });
  function frame(now){ const dt=Math.min(0.05,Math.max(0,(now-last)/1000)); last=now;
    if(playing){ t+=dt*(+$('sp').value); if(t>=48){ t=48; playing=false; tog(); } syncT(); dirty=true; }
    if(hintT && now-hintT<2300) dirty=true;
    if(dirty){ dirty=false; draw(playing?now*0.06:0); }
    requestAnimationFrame(frame); }
  btnVis(); compute(); tog(); syncT(); draw(0); requestAnimationFrame(frame);
'''.replace("@SAT@", SAT_JS))


# ============================================================ 流れる水モデル（JS と同じ式。記事の早見表を作る）
_CPT = [[-6, 96], [28, 106], [60, 90], [92, 108], [122, 98], [150, 120], [176, 150], [198, 186], [224, 214], [260, 230], [298, 222],
        [326, 196], [342, 162], [360, 130], [388, 108], [426, 102], [460, 118], [482, 150], [498, 190], [522, 224], [556, 244], [592, 250], [614, 250]]
CPT_JS = ",".join("[%d,%d]" % (a, b) for a, b in _CPT)
def _ub(u): return (0.5 + 1.2 * (1 - u) ** 1.3) * (1 - 0.6 * _ss(0.93, 1, u))
def _dmm(u): return 450 * math.exp(-4.2 * u) * (1 - 0.8 * _ss(0.8, 1, u))
def _rnd(u): return _cl((u - 0.08) / 0.75, 0, 1) ** 0.9
def _river():
    def crp(a, b, c, d, u):
        u2 = u * u; u3 = u2 * u
        return [0.5 * (2 * b[k] + (-a[k] + c[k]) * u + (2 * a[k] - 5 * b[k] + 4 * c[k] - d[k]) * u2 + (-a[k] + 3 * b[k] - 3 * c[k] + d[k]) * u3) for k in (0, 1)]
    dn = []
    for k in range(len(_CPT) - 1):
        a = _CPT[max(0, k - 1)]; b = _CPT[k]; c = _CPT[k + 1]; d = _CPT[min(len(_CPT) - 1, k + 2)]
        for j in range(16): dn.append(crp(a, b, c, d, j / 16))
    dn.append(_CPT[-1])
    cum = [0.0]
    for k in range(1, len(dn)): cum.append(cum[-1] + math.hypot(dn[k][0] - dn[k - 1][0], dn[k][1] - dn[k - 1][1]))
    L = cum[-1]; DS = 2.5; ns = int(math.floor(L / DS)) + 1; pts = []; j = 0
    for i in range(ns):
        s = min(L, i * DS)
        while j < len(dn) - 2 and cum[j + 1] < s: j += 1
        q = (s - cum[j]) / ((cum[j + 1] - cum[j]) or 1)
        pts.append((dn[j][0] + (dn[j + 1][0] - dn[j][0]) * q, dn[j][1] + (dn[j + 1][1] - dn[j][1]) * q))
    th = []
    for i in range(ns):
        a = pts[max(0, i - 1)]; b = pts[min(ns - 1, i + 1)]; th.append(math.atan2(b[1] - a[1], b[0] - a[0]))
    for i in range(1, ns):
        while th[i] - th[i - 1] > math.pi: th[i] -= 2 * math.pi
        while th[i] - th[i - 1] < -math.pi: th[i] += 2 * math.pi
    K = []
    for i in range(ns):
        a = max(0, i - 6); b = min(ns - 1, i + 6); K.append(_cl(-(th[b] - th[a]) / ((b - a) * DS) * 55, -1, 1))
    return ns, K
_NS, _K = _river()
_IB = max(range(_NS), key=lambda i: abs(_K[i]) if 0.38 <= i / (_NS - 1) <= 0.62 else -1)
_UB = _IB / (_NS - 1); _SG = 1 if _K[_IB] >= 0 else -1
def _vel(u, k, nw): return _ub(u) * (1 - 0.45 * nw * nw) * (1 - 0.55 * k * nw)
_V_OUT = _vel(_UB, _K[_IB], -0.72 * _SG); _V_IN = _vel(_UB, _K[_IB], 0.72 * _SG)
def _iu(u): return _jr(u * (_NS - 1))                      # JS の Math.round
def _straight(a, b):
    best = _iu(a); bk = 9
    for i in range(_iu(a), _iu(b) + 1):
        if abs(_K[i]) < bk: bk = abs(_K[i]); best = i
    return best
_PL = [("上流（山の中）", _straight(0.1, 0.2)), ("中流・曲がった所の外側", _IB), ("中流・曲がった所の内側", _IB), ("下流（平地）", _straight(0.78, 0.9)), ("河口の近く", _iu(0.965))]
def _size(mm):
    if mm >= 100: return "約%dcm" % _jr(mm / 10)
    if mm >= 10: return "約%scm" % _f1(mm / 10)
    return "約%dmm" % _jr(mm)
def _sizew(mm):
    return ("ひとかかえほど" if mm >= 400 else "人の頭より大きい" if mm >= 200 else "人の頭くらい" if mm >= 130 else "にぎりこぶしくらい" if mm >= 70 else
            "たまごくらい" if mm >= 30 else "ビー玉くらい" if mm >= 10 else "大豆くらいの小石" if mm >= 3 else "すなつぶ")
def _shapew(r): return "角ばっている" if r < 0.3 else ("角がとれて少し丸い" if r < 0.65 else "丸い")
def _vrow(name, i, v):
    u = i / (_NS - 1); d = _dmm(u)
    return [name, "秒速%sm" % _f1(v), "%s（%s）" % (_size(d), _sizew(d)), _shapew(_rnd(u))]
NTABLE = T([_vrow(_PL[0][0], _PL[0][1], _vel(_PL[0][1] / (_NS - 1), _K[_PL[0][1]], 0)),
            _vrow(_PL[1][0], _IB, _V_OUT), _vrow(_PL[2][0], _IB, _V_IN),
            _vrow(_PL[3][0], _PL[3][1], _vel(_PL[3][1] / (_NS - 1), _K[_PL[3][1]], 0)),
            _vrow(_PL[4][0], _PL[4][1], _vel(_PL[4][1] / (_NS - 1), _K[_PL[4][1]], 0))],
           ["場所", "流れの速さ（ふつうの水の量）", "川原の石の大きさ", "石の形"])
assert abs(_K[_IB]) > 0.6 and _V_OUT > 2 * _V_IN


# ============================================================ 2 流れる水の働き
sim(slug="nagareru-mizu", cat="rika", emoji="🏞️", score=80,
    title="流れる水の働きシミュレーター（しん食・運ぱん・たい積）",
    title_tag="流れる水の働きシミュレーター｜しん食・運ぱん・たい積と川原の石（小5理科）",
    meta_desc="土地のかたむきと水の量を変えて川に水を流すと、土がけずられ（しん食）、運ばれ（運ぱん）、積もる（たい積）ようすが土のつぶの動きで見られる無料シミュレーター。曲がった所の外側と内側、上流と下流の石のちがい、大雨で増水したときの変化も確かめられます。",
    og_title="流れる水の働きシミュレーター（しん食・運ぱん・たい積）",
    og_desc="川を流れる水が土をけずり、運び、積もらせるようすを土のつぶで見る小5理科の教材。曲がった所の外側・内側、上流と下流の石、大雨の増水も。",
    card_desc="川の水が土をけずり、運び、積もらせるようすを見る。曲がった所の外側・内側や、上流と下流の石もくらべられる。",
    lead="山から海へ流れる川に水を流すと、土のつぶがけずられ（しん食）、運ばれ（運ぱん）、流れがおそい所に積もる（たい積）ようすが見られます。土地のかたむきや水の量を変えたり、「大雨」をふらせたりして、流れの速さと土地の変わり方をくらべましょう。地図をタップすると、その場所の流れの速さ・川の断面・川原の石が分かります。",
    model="小5 流れる水の働きと土地の変化",
    level="小学5年",
    unit="小学校 第5学年 B（3）流れる水の働きと土地の変化",
    canvas=canvas(640, 580, light=True),
    controls=select("place", "観察する場所", [("out", "中流：曲がった所の外側"), ("in", "中流：曲がった所の内側"), ("up", "上流（山の中）"),
                                         ("down", "下流（平地）"), ("mouth", "河口の近く"), ("tap", "地図をタップしてえらんだ場所")])
           + slider("slope", "土地のかたむき", 1, 5, 3, 1)
           + slider("qq", "水の量", 1, 5, 2, 1)
           + slider("early", "早送り（土地の変わる速さ）", 1, 5, 1, 1, "×{v}"),
    buttons=btn("play", "⏸ 一時停止") + btn("rain", "☔ 大雨をふらせる", True) + btn("reset", "↺ はじめにもどす"),
    stats=stats([("sV", "えらんだ所の流れ", True), ("sE", "けずられた土（しん食）", False),
                 ("sD", "積もった土（たい積）", False), ("sS", "えらんだ所の石", False)]),
    legend="青い所＝川の水（こい青ほど深い）、うすい茶色＝川原（川底のすなや石）、こい茶色の線＝けずられてできたがけ、茶色の点＝運ばれている土や石、白い線＝水の流れ（長いほど速い）。地図をタップすると、その場所の流れの速さ・川の断面・川原の石が下に出ます。「けずられた土＝運ばれている土＋積もった土」の数は、シミュレーションの中の土のつぶの数です。川の形・速さ・石の大きさは、しくみがわかるように作ったモデルです。",
    article='''
<h2>このシミュレーションでわかること</h2>
''' + P("川を流れる水には、<b>地面をけずるはたらき（しん食）</b>、<b>けずった土や石を運ぶはたらき（運ぱん）</b>、<b>運んだ土や石を積もらせるはたらき（たい積）</b>があります。土地のかたむきが大きい所や、大雨で水の量がふえたときは、流れが速くなり、けずるはたらきと運ぶはたらきが大きくなります。") + '''
<p>曲がって流れている所では、<b>外側</b>は流れが速く、川岸がけずられてがけになり、川底も深くなります。<b>内側</b>は流れがおそく、石やすなが積もって川原ができます。また、<b>上流</b>には大きくて角ばった石が多く、<b>下流</b>には小さくて丸い石やすなが多く見られます。</p>
<p>小学校5年の理科「流れる水の働きと土地の変化」（学習指導要領 第5学年 B（3））で学ぶ内容です。学習指導要領の解説では、野外での観察のほか、人工の流れをつくったモデル実験で水の速さや量を変えて調べることや、大雨で増水した川のようすを映像などで調べることが例にあげられています。</p>

<h2>授業での使い方</h2>
<ul>
<li><b>導入</b>：大雨のあとの川のようす（水がにごって茶色い、水の量が多い、流れが速い）を思い出させ、「流れる水には、どんなはたらきがあるのだろう」と問いかけます。シミュレーションを動かして、土がけずられ、運ばれ、積もっていくようすを見せます。</li>
<li><b>展開</b>：校庭の土の山や、土を入れたといなどに水を流すモデル実験の前に、予想を立てるときに使えます。「土地のかたむき」と「水の量」は、<b>変える条件を1つだけ</b>にしてくらべます。「観察する場所」で曲がった所の外側と内側を切りかえて、流れの速さをくらべます。実験のあとは、実験の結果と見くらべて、実際の川のようすにつなげます。</li>
<li><b>まとめ</b>：場所を「上流」「下流」に切りかえて、川原の石の大きさや形のちがいを確かめます。「☔ 大雨をふらせる」で、増水すると土地のようすが大きく変わることや、川の水があふれるきけんがあることを話し合い、川の災害にそなえるくふうにつなげます。</li>
</ul>
<p>児童への問いの例：</p>
<ol>
<li>曲がって流れている所で、外側と内側では、流れの速さや川の深さはどうちがうでしょうか。</li>
<li>水の量を多くすると、けずられる土や運ばれる土の量はどう変わるでしょうか。</li>
<li>上流と下流で、川原の石の大きさや形がちがうのはなぜでしょうか。</li>
</ol>

<h2>しくみ・解説</h2>
<h3>流れる水の3つのはたらき</h3>
''' + T([["しん食（けずる）", "地面や川岸、川底をけずる", "流れが速い所（上流、曲がった所の外側）"],
          ["運ぱん（運ぶ）", "けずった土や石を下流へ運ぶ", "流れが速いほど、大きな石まで運ばれる"],
          ["たい積（積もらせる）", "運んできた土や石を積もらせる", "流れがおそい所（下流、曲がった所の内側、河口）"]],
         ["はたらき", "どんなはたらきか", "よく見られる場所"]) + '''
<p>流れが速いほど、けずるはたらきと運ぶはたらきは大きくなります。流れがおそくなると、運ばれていた石や土が、大きい（重い）ものから先に積もります。</p>
<p>シミュレーションの上に出る「けずられた土 ＝ 運ばれている土 ＋ 積もった土」は、けずられた土が運ばれて、やがてどこかに積もることを表しています（数は、シミュレーションの中の土のつぶの数です）。水の量を「多い」や「大雨」にしたり、「早送り」にしたりすると、数のふえ方が速くなります。</p>
<h3>曲がって流れている所（外側と内側）</h3>
<p>川が曲がっている所では、水が外側におしつけられるように流れるので、<b>外側の流れが速く</b>なります。そのため外側では、川岸や川底がけずられて、がけになったり深くなったりします。<b>内側は流れがおそい</b>ので、運ばれてきた石やすなが積もって、川原ができます。シミュレーションでも、外側の岸が少しずつけずられてこい茶色の「がけ」の線がのび、内側に土のつぶが積もっていきます。長い年月のあいだに、これがくり返されて、川の曲がり方は少しずつ大きくなっていきます。</p>
<h3>上流・中流・下流のちがい</h3>
''' + T([[NW("上流"), "大きい（急）", "速い", "せまい", "大きくて角ばった石が多い", "深い谷（V字のような谷）"],
          [NW("中流"), "中くらい", "中くらい", "広くなる", "角がとれて丸みのある石", "曲がって流れる所、川原"],
          [NW("下流"), "小さい（ゆるやか）", "おそい", "広い", "小さくて丸い石、すな、どろ", "平地、河口（すなやどろが積もる）"]],
         ["場所", "土地のかたむき", "流れの速さ", "川はば", "川原の石", "土地のようす"]) + '''
<p>上流の石が大きくて角ばっているのは、山の岩がくずれてできたばかりの石だからです。石は、流れる水に運ばれるあいだに、ほかの石や川底とぶつかったりこすれたりして、角がとれて丸くなり、小さくなっていきます。また、大きくて重い石は、流れが速くないと運ばれないので、上流に多く残ります。</p>
<p>このシミュレーションの初期設定（土地のかたむき「ふつう」・水の量「ふつう」）では、それぞれの場所は次のようになります。</p>
''' + NTABLE + P("同じ中流の曲がった所でも、外側は内側の約%d倍の速さで流れます。水の量を「とても多い（大雨）」にすると、どの場所も流れが速くなり、ふだんは動かない大きな石まで運ばれるようになります。" % _jr(_V_OUT / _V_IN)) + '''
<h3>大雨と増水</h3>
<p>雨が短い時間にたくさん降ったり、長い時間降り続いたりすると、川の水の量がふえ（増水）、流れも速くなります。すると、しん食や運ぱんのはたらきが大きくなり、川岸が大きくけずられたり、たくさんの土や石が運ばれたりして、短い時間で土地のようすが大きく変わることがあります。水が川からあふれると、こう水になります。</p>
<p>シミュレーションで「☔ 大雨をふらせる」をおすと、約20秒のあいだ水の量がふえます。水が茶色くにごるのは、けずられた土をたくさん運んでいるからです。水の量を「あふれるほど多い」にして大雨をふらせると、下流で川の水があふれ、家のまわりまで水が来ることがあります。</p>
<h3>川の災害にそなえる</h3>
<ul>
<li>大雨のときや大雨のあとは、川に近づかない（上流で降った雨で、急に水がふえることもあります）。</li>
<li>住んでいる地いきのハザードマップで、水につかるおそれのある場所や、ひなんする場所を、家の人といっしょに確かめておく。</li>
<li>気象庁の「キキクル（危険度分布）」や、市町村から出されるひなんの情報に気をつける。</li>
<li>川には、水があふれないようにする「てい防」、水の量を調節する「ダム」、土や石が一度に流れ出るのを防ぐ「砂防（さぼう）ダム」、川岸がけずられないように守る「護岸（ごがん）ブロック」など、災害を防ぐくふうがあります。</li>
</ul>
<h3>川原の石を観察するとき</h3>
<ul>
<li>石の大きさ（ものさしで長さをはかる）、形（角ばっているか、丸いか）、色をくらべ、記録します。</li>
<li>上流・中流・下流の石の写真や標本と見くらべます。</li>
<li>川原での観察は、天気や川の水の量に気をつけて、かならず大人といっしょに行います。</li>
</ul>
''' + N("<b>このシミュレーションで単純にしていること</b><br>"
     "・川の形、流れの速さ、石の大きさは、しくみがわかるように作ったモデルの値で、実際の川の値ではありません（目安です）。<br>"
     "・流れの速さは、土地のかたむきと水の量から計算し、曲がった所では外側が速く、内側がおそくなるようにしています。水の中でも、岸に近い所ほどおそくなります。<br>"
     "・土のつぶは、流れが速いほど大きなつぶまで動き、流れがおそくなると止まって積もります。曲がった所では、つぶが内側へよせられるようにしています。<br>"
     "・川原の石の大きさと形は、場所ごとの代表的な大きさ（上流ほど大きく、下流ほど小さい）と丸さを表しています。<br>"
     "・地いきや川によって、石の大きさや流れの速さは大きくちがいます。") + '''
<h2>参考</h2>
<ul class="seo-refs">
<li>文部科学省「小学校学習指導要領（平成29年告示）解説 理科編」第5学年 B（3）流れる水の働きと土地の変化（''' + A(MEXT_SHO, "文部科学省 学習指導要領解説のページ") + '''）</li>
<li>小学校理科の教科書（東京書籍「新しい理科」、啓林館「わくわく理科」、大日本図書「たのしい理科」など）5年の「流れる水のはたらき」の単元</li>
<li>国土交通省・国土地理院「ハザードマップポータルサイト」（''' + A("https://disaportal.gsi.go.jp/", "ハザードマップポータルサイト") + '''）</li>
<li>気象庁「キキクル（危険度分布）」（''' + A("https://www.jma.go.jp/bosai/risk/", "気象庁 キキクル") + '''）</li>
</ul>
''',
    faqs=[("流れる水のはたらきには、どんなものがありますか？", "地面をけずる「しん食」、けずった土や石を運ぶ「運ぱん」、運んだ土や石を積もらせる「たい積」の3つがあります。流れが速い所ではけずるはたらきと運ぶはたらきが大きく、流れがおそい所では積もらせるはたらきが大きくなります。"),
          ("川が曲がって流れている所では、外側と内側で何がちがいますか？", "外側は流れが速く、川岸や川底がけずられて、がけになったり深くなったりします。内側は流れがおそく、石やすなが積もって川原になります。"),
          ("上流と下流で、川原の石の大きさや形がちがうのはなぜですか？", "上流の石は、山の岩がくずれてできたばかりなので、大きくて角ばっています。流れる水に運ばれるあいだに、石どうしや川底とぶつかったりこすれたりして、角がとれて丸く、小さくなっていきます。また、大きくて重い石は流れが速くないと運ばれないので、上流に残りやすくなります。"),
          ("大雨で川の水がふえると、どうなりますか？", "流れが速くなり、けずるはたらきと運ぶはたらきが大きくなります。川岸が大きくけずられたり、ふだんは動かない大きな石まで運ばれたりして、短い時間で土地のようすが大きく変わることがあります。水が川からあふれると、こう水になります。大雨のときは、川に近づかないようにしましょう。"),
          ("土地のかたむきが大きいと、流れはどうなりますか？", "かたむきが大きい（急な）所ほど、水の流れは速くなります。山の中の上流はかたむきが大きいので流れが速く、平地の下流はかたむきが小さいので流れがおそくなります。"),
          ("川の災害を防ぐために、どんなくふうがありますか？", "川の水があふれないようにする「てい防」、水の量を調節する「ダム」、土や石が一度に流れ出るのを防ぐ「砂防（さぼう）ダム」、川岸がけずられないように守る「護岸（ごがん）ブロック」などがあります。住んでいる地いきのハザードマップで、ひなんする場所を確かめておくことも大切です。")],
    rel=[("kaibatsu-check", "⛰️", "うちの海抜チェッカー"), ("chisou", "⛏️", "地層のでき方と柱状図"),
         ("amagumo-now", "🌧️", "いまの雨雲マップ"), ("tsunami-kishi", "🌊", "津波はなぜ岸で高くなる？")],
    js=r'''
  const cv=$('cv'); const dpr=Math.min(2,window.devicePixelRatio||1); const W=cv.width,H=cv.height; cv.width=W*dpr; cv.height=H*dpr; const ctx=cv.getContext('2d'); ctx.setTransform(dpr,0,0,dpr,0,0);
  cv.setAttribute('role','img'); cv.setAttribute('aria-label','山から海へ流れる川を上から見た図、川の高さのようす、えらんだ場所の川の断面と川原の石');
  cv.style.cursor='pointer';
  const HB=40, MT=44, MB=298, PT=318, PB=362, IT=388, IB=H-4, PXS=30;
  const ss=(a,b,v)=>{ const u=clamp((v-a)/(b-a),0,1); return u*u*(3-2*u); };
  const f1=(v)=>(Math.round(v*10)/10).toFixed(1);
  const line=(a,b,c,d)=>{ ctx.beginPath(); ctx.moveTo(a,b); ctx.lineTo(c,d); ctx.stroke(); };
  function txt(s,x,y,font,col,al,halo){ ctx.font=font; ctx.textAlign=al||'left'; if(halo){ ctx.lineJoin='round'; ctx.lineWidth=3.5; ctx.strokeStyle='rgba(255,255,255,.95)'; ctx.strokeText(s,x,y); } ctx.fillStyle=col; ctx.fillText(s,x,y); }
  function tw(s,font){ ctx.font=font; return ctx.measureText(s).width; }
  function rr(x,y,w,h,r){ ctx.beginPath(); ctx.moveTo(x+r,y); ctx.lineTo(x+w-r,y); ctx.quadraticCurveTo(x+w,y,x+w,y+r); ctx.lineTo(x+w,y+h-r); ctx.quadraticCurveTo(x+w,y+h,x+w-r,y+h); ctx.lineTo(x+r,y+h); ctx.quadraticCurveTo(x,y+h,x,y+h-r); ctx.lineTo(x,y+r); ctx.quadraticCurveTo(x,y,x+r,y); ctx.closePath(); }
  function rng(seed){ let a=seed>>>0; return function(){ a=(a+0x6D2B79F5)|0; let q=Math.imul(a^(a>>>15),1|a); q=(q+Math.imul(q^(q>>>7),61|q))^q; return ((q^(q>>>14))>>>0)/4294967296; }; }
  // ---------- 川の中心線（左＝上流の山、右＝下流の海）を長さ2.5pxごとの点にする
  const CPT=[@CPT@];
  function crp(a,b,c,d,u){ const u2=u*u, u3=u2*u, o=[]; for(let k=0;k<2;k++) o.push(0.5*(2*b[k]+(-a[k]+c[k])*u+(2*a[k]-5*b[k]+4*c[k]-d[k])*u2+(-a[k]+3*b[k]-3*c[k]+d[k])*u3)); return o; }
  const DN=[]; for(let k=0;k<CPT.length-1;k++){ const a=CPT[Math.max(0,k-1)], b=CPT[k], c=CPT[k+1], d=CPT[Math.min(CPT.length-1,k+2)]; for(let j=0;j<16;j++) DN.push(crp(a,b,c,d,j/16)); } DN.push(CPT[CPT.length-1]);
  const CUM=[0]; for(let k=1;k<DN.length;k++) CUM.push(CUM[k-1]+Math.hypot(DN[k][0]-DN[k-1][0],DN[k][1]-DN[k-1][1]));
  const LEN=CUM[CUM.length-1], DS=2.5, NS=Math.floor(LEN/DS)+1, R=[];
  for(let i=0,j=0;i<NS;i++){ const s=Math.min(LEN,i*DS); while(j<DN.length-2 && CUM[j+1]<s) j++; const q=(s-CUM[j])/((CUM[j+1]-CUM[j])||1); R.push({x:DN[j][0]+(DN[j+1][0]-DN[j][0])*q, y:DN[j][1]+(DN[j+1][1]-DN[j][1])*q}); }
  const TH=[]; R.forEach((p,i)=>{ const a=R[Math.max(0,i-1)], b=R[Math.min(NS-1,i+1)], L=Math.hypot(b.x-a.x,b.y-a.y)||1; p.tx=(b.x-a.x)/L; p.ty=(b.y-a.y)/L; p.nx=p.ty; p.ny=-p.tx; TH.push(Math.atan2(b.y-a.y,b.x-a.x)); });
  for(let i=1;i<NS;i++){ while(TH[i]-TH[i-1]>Math.PI) TH[i]-=2*Math.PI; while(TH[i]-TH[i-1]<-Math.PI) TH[i]+=2*Math.PI; }
  R.forEach((p,i)=>{ const a=Math.max(0,i-6), b=Math.min(NS-1,i+6); p.K=clamp(-(TH[b]-TH[a])/((b-a)*DS)*55,-1,1); p.u=i/(NS-1); p.w0=3.6+12*p.u; });
  // K>0：左に曲がる（外側は右岸）。n は中心線からの距離で、左岸側が＋。
  // ---------- モデル
  const SLW=['とてもゆるやか','ゆるやか','ふつう','急','とても急'], QW=['少ない','ふつう','多い','とても多い（大雨）','あふれるほど多い'], QV=[0.5,1,1.7,2.6,3.6];
  const Ub=(u)=>(0.5+1.2*Math.pow(1-u,1.3))*(1-0.6*ss(0.93,1,u));
  const Dmm=(u)=>450*Math.exp(-4.2*u)*(1-0.8*ss(0.8,1,u));
  const RNDu=(u)=>Math.pow(clamp((u-0.08)/0.75,0,1),0.9);
  const ucB=(u)=>0.6+0.9*(1-u)*(1-u), ovf=(u)=>ss(0.3,0.7,u);
  let slope=3, qs=2, flood=0, fT=-1, early=1, playing=true, eroded=0, restOld=0, upAcc=0, GR=[], dirty=true, last=performance.now(), sel=null, drag=false;
  const Kf=()=>Math.sqrt(slope/3), Qnow=()=>QV[qs-1]+flood, Qf=()=>Math.pow(Qnow(),0.4);
  const fW=()=>Math.min(1.8,0.6+0.4*(Qf()-0.758)/(1.466-0.758));
  function velAt(p,nw){ return Math.abs(nw)>1?0:Ub(p.u)*Kf()*Qf()*(1-0.45*nw*nw)*(1-0.55*p.K*nw); }
  function geomAll(){ const f=fW(); R.forEach((p)=>{ const Wc=p.bl+p.br;
    if(f<=1){ const kk=Math.min(1,Math.abs(p.K)), dry=Math.min(0.62,(1-f)*(1+0.9*kk))*Wc, a=0.5+0.5*Math.min(1,kk*1.3), di=dry*a, dout=dry-di; if(p.K>=0){ p.eL=p.bl-di; p.eR=-(p.br-dout); } else { p.eL=p.bl-dout; p.eR=-(p.br-di); } }
    else { const ov=(f-1)*Wc*2.4*ovf(p.u); p.eL=p.bl+ov; p.eR=-(p.br+ov); } }); }
  const nwOf=(p,n)=>(n-(p.eL+p.eR)/2)/(((p.eL-p.eR)/2)||1);
  function gsize(u){ return Math.random()<0.4?rnd(0.4,2.0):Dmm(u)*Math.exp(0.5*randn()); }
  function addGrain(s,n,d){ GR.push({s:s,n:n,d:d,mv:true,sea:false,x:0,y:0}); eroded++; }
  function erodeAll(dt){ const kq=Kf()*Qf();
    for(let i=3;i<NS-4;i++){ const p=R[i], base=Ub(p.u)*kq*0.675, uc=ucB(p.u), rL=clamp(1-(p.bl-p.eL)/3,0,1), rR=clamp(1-(p.br+p.eR)/3,0,1);
      const eL=0.35*Math.max(0,base*(1-0.47*p.K)-uc)*rL, eR=0.35*Math.max(0,base*(1+0.47*p.K)-uc)*rR;
      if(eL>0 && p.bl<p.w0+16){ const d=eL*dt; p.bl+=d; p.EL+=d; p.aL+=d*DS/1.1; while(p.aL>=1){ p.aL-=1; addGrain(i*DS+rnd(-1,1),Math.min(p.bl,p.eL)-0.5,gsize(p.u)); } }
      if(eR>0 && p.br<p.w0+16){ const d=eR*dt; p.br+=d; p.ER+=d; p.aR+=d*DS/1.1; while(p.aR>=1){ p.aR-=1; addGrain(i*DS+rnd(-1,1),Math.max(-p.br,p.eR)+0.5,gsize(p.u)); } } } }
  function supply(dt){ upAcc+=dt*1.6*Kf()*Kf()*Math.pow(Qf(),3); while(upAcc>=1){ upAcc-=1; const i=Math.floor(rnd(2,9)), p=R[i]; addGrain(i*DS,(p.eL+p.eR)/2+rnd(-0.8,0.8)*(p.eL-p.eR)/2,gsize(0.03)); } }
  function settle(g,i,nw){ const p=R[i]; if(Math.abs(p.K)>0.2 && nw*p.K>0){ for(let j=-3;j<=3;j++){ const q=R[clamp(i+j,0,NS-1)], w=(4-Math.abs(j))/16*0.05*Math.min(1,g.d/3+0.3); if(p.K>0) q.bl=Math.max(q.w0*0.5,q.bl-w); else q.br=Math.max(q.w0*0.5,q.br-w); } } }
  function moveGrains(dt){ const kq=Kf()*Qf(), m=R[NS-1];
    for(let k=0;k<GR.length;k++){ const g=GR[k]; if(g.sea) continue;
      const i=clamp(Math.floor(g.s/DS),0,NS-1), p=R[i], hw=(p.eL-p.eR)/2, nw=(g.n-(p.eL+p.eR)/2)/(hw||1), uc=0.18*Math.pow(g.d,0.45);
      const u=Math.abs(nw)<=1?Ub(p.u)*kq*(1-0.45*nw*nw)*(1-0.55*p.K*nw):0;
      if(g.mv){ if(u<uc){ g.mv=false; settle(g,i,nw); continue; }
        const v=u*Math.min(1,(u-uc)/(0.6*uc))*0.85*PXS; g.s+=v*dt; g.n+=(p.K*0.32*hw+randn()*1.2)*dt; g.d*=Math.exp(-v*dt*0.0006);
        if(g.s>=LEN-3){ g.sea=true; g.mv=false; const a=Math.atan2(m.ty,m.tx)+randn()*0.7, r=5+Math.abs(randn())*12; g.x=m.x+Math.cos(a)*r; g.y=m.y+Math.sin(a)*r; } }
      else if(u>uc*1.25 && Math.random()<dt*3) g.mv=true; } }
  const WPS=[]; for(let k=0;k<230;k++) WPS.push({s:Math.random()*LEN,nw:rnd(-0.95,0.95),v:0});
  function moveWater(dt){ const kq=Kf()*Qf(); WPS.forEach((w)=>{ const p=R[clamp(Math.floor(w.s/DS),0,NS-1)]; w.v=Ub(p.u)*kq*(1-0.45*w.nw*w.nw)*(1-0.55*p.K*w.nw)*PXS; w.s+=w.v*dt; if(w.s>=LEN-2){ w.s=rnd(0,6); w.nw=rnd(-0.95,0.95); } }); }
  function cleanup(){ if(GR.length<=2600) return; let rm=GR.length-2300; const keep=[]; GR.forEach((g)=>{ if(rm>0 && !g.mv){ rm--; restOld++; } else keep.push(g); }); GR=keep; }
  function step(dtr){ if(fT>=0){ fT+=dtr; flood=3*(fT<3?ss(0,3,fT):(fT<10?1:1-ss(10,20,fT))); if(fT>=20){ fT=-1; flood=0; $('rain').disabled=false; $('rain').textContent='☔ 大雨をふらせる'; } }
    geomAll(); const dt=dtr*early; erodeAll(dt); supply(dt); moveGrains(dtr); moveWater(dtr); cleanup(); }
  // ---------- 場所
  let IBd=0; for(let i=0;i<NS;i++){ if(R[i].u>=0.38 && R[i].u<=0.62 && Math.abs(R[i].K)>Math.abs(R[IBd].K)) IBd=i; }
  const SGN=R[IBd].K>=0?1:-1, iu=(u)=>Math.round(u*(NS-1));
  function straightIn(a,b){ let best=iu(a), bk=9; for(let i=iu(a);i<=iu(b);i++){ if(Math.abs(R[i].K)<bk){ bk=Math.abs(R[i].K); best=i; } } return best; }
  const IUP=straightIn(0.1,0.2), IDN=straightIn(0.78,0.9);
  function preset(v){ if(v==='out') sel={i:IBd,rel:-0.72*SGN}; else if(v==='in') sel={i:IBd,rel:0.72*SGN}; else if(v==='up') sel={i:IUP,rel:0}; else if(v==='down') sel={i:IDN,rel:0}; else if(v==='mouth') sel={i:iu(0.965),rel:0}; dirty=true; }
  function place(){ const p=R[sel.i]; let n, nw; if(sel.rel!==undefined && sel.rel!==null){ nw=sel.rel; n=(p.eL+p.eR)/2+nw*(p.eL-p.eR)/2; } else { n=sel.n; nw=nwOf(p,n); }
    const v=velAt(p,nw); let name=p.u<0.3?'上流':(p.u<0.7?'中流':(p.u<0.95?'下流':'河口の近く'));
    if(n>p.bl+0.5 || n<-p.br-0.5) name+=(Math.abs(nw)<=1?'・岸の上（水があふれている）':'・岸の上（陸地）');
    else if(Math.abs(nw)>1) name+='・川原（水の外）';
    else if(Math.abs(nw)<0.3) name+='・川のまん中';
    else if(Math.abs(p.K)>0.3) name+='・曲がった所の'+(nw*p.K<0?'外側':'内側');
    else name+='・岸の近く';
    return {i:sel.i,p:p,n:n,nw:nw,v:v,name:name,D:Dmm(p.u),r:RNDu(p.u)}; }
  function fmtSize(mm){ return mm>=100?'約'+Math.round(mm/10)+'cm':(mm>=10?'約'+f1(mm/10)+'cm':'約'+Math.round(mm)+'mm'); }
  function sizeWord(mm){ return mm>=400?'ひとかかえほど':(mm>=200?'人の頭より大きい':(mm>=130?'人の頭くらい':(mm>=70?'にぎりこぶしくらい':(mm>=30?'たまごくらい':(mm>=10?'ビー玉くらい':(mm>=3?'大豆くらいの小石':'すなつぶ')))))); }
  function shapeWord(r){ return r<0.3?'角ばっている':(r<0.65?'角がとれて少し丸い':'丸い'); }
  // ---------- 背景（山・田畑・海）は最初に1回だけかく
  const BG=document.createElement('canvas'); BG.width=Math.round(W*dpr); BG.height=Math.round((MB-MT)*dpr);
  function distR(x,y){ let m=1e9; for(let i=0;i<NS;i+=2){ const d=Math.hypot(R[i].x-x,R[i].y-y); if(d<m) m=d; } return m; }
  const coastX=(y)=>606+5*Math.sin(y*0.06);
  const HOUSES=[], ROCKS=[];
  function mkBG(){ const b=BG.getContext('2d'); b.setTransform(dpr,0,0,dpr,0,-MT*dpr);
    const g=b.createLinearGradient(0,0,W,0); g.addColorStop(0,'#b7cd94'); g.addColorStop(0.3,'#cadda8'); g.addColorStop(0.45,'#e1edcc'); g.addColorStop(1,'#e9f3da'); b.fillStyle=g; b.fillRect(0,MT,W,MB-MT);
    b.lineJoin='round'; b.lineCap='round'; const i1=Math.floor(NS*0.36);
    b.beginPath(); for(let i=0;i<=i1;i++){ if(i) b.lineTo(R[i].x,R[i].y); else b.moveTo(R[i].x,R[i].y); } b.strokeStyle='rgba(92,112,62,.30)'; b.lineWidth=44; b.stroke(); b.strokeStyle='rgba(120,104,76,.28)'; b.lineWidth=22; b.stroke();
    const r1=rng(11);
    for(let x=258;x<596;x+=27) for(let y=MT+6;y<MB-8;y+=19){ const xx=x+(Math.floor((y-MT)/19)%2)*9; if(distR(xx+12,y+8)<34 || xx+24>coastX(y)-6) continue; b.fillStyle=r1()<0.5?'#d9eabf':'#e4f0d0'; b.fillRect(xx,y,24,16); b.strokeStyle='rgba(120,150,90,.35)'; b.lineWidth=1; b.strokeRect(xx+0.5,y+0.5,23,15); }
    for(let k=0;k<140;k++){ const x=r1()*250-6, y=MT+4+r1()*(MB-MT-8); if(x>215+(y-MT)*0.15 || distR(x,y)<26) continue; const s=11+r1()*12*(1-Math.max(0,x)/320);
      b.beginPath(); b.moveTo(x-s,y+s*0.5); b.lineTo(x,y-s*0.62); b.lineTo(x+s,y+s*0.5); b.closePath(); b.fillStyle='#8fa96d'; b.fill();
      b.beginPath(); b.moveTo(x,y-s*0.62); b.lineTo(x+s,y+s*0.5); b.lineTo(x+s*0.15,y+s*0.5); b.closePath(); b.fillStyle='#738d56'; b.fill();
      b.beginPath(); b.moveTo(x-s,y+s*0.5); b.lineTo(x,y-s*0.62); b.lineTo(x+s,y+s*0.5); b.strokeStyle='#5f7646'; b.lineWidth=1; b.stroke(); }
    b.beginPath(); b.moveTo(coastX(MT),MT); for(let y=MT;y<=MB;y+=4) b.lineTo(coastX(y),y); b.lineTo(W,MB); b.lineTo(W,MT); b.closePath();
    const sg=b.createLinearGradient(600,0,W,0); sg.addColorStop(0,'#9cc9f5'); sg.addColorStop(1,'#5b9be6'); b.fillStyle=sg; b.fill();
    b.strokeStyle='rgba(255,255,255,.7)'; b.lineWidth=1.2; for(let y=MT+14;y<MB;y+=22){ const x=coastX(y)+12; b.beginPath(); b.arc(x,y,5,Math.PI*1.1,Math.PI*1.9); b.stroke(); b.beginPath(); b.arc(x+11,y+8,5,Math.PI*1.1,Math.PI*1.9); b.stroke(); } }
  function mkDecor(){ const r2=rng(23);
    for(let i=4;i<NS-4;i+=5){ const p=R[i]; for(const sd of [1,-1]){ if(r2()<0.35) continue; const big=p.u<0.4; const d=Dmm(p.u)*Math.exp(0.4*(r2()-0.5)); const rad=clamp(0.9+0.85*Math.log10(d),1,4.6);
      const off=sd*(p.w0*(big?0.55:0.75)+r2()*1.5), pts=[], m=big?6:9; for(let k=0;k<m;k++){ const a=(k+(r2()-0.5)*0.5)/m*Math.PI*2; pts.push([Math.cos(a)*rad*(big?0.7+0.3*r2():1), Math.sin(a)*rad*(big?0.6+0.3*r2():0.8)]); }
      ROCKS.push({i:i,n:off,pts:pts,big:big}); } }
    [[0.74,1,22],[0.77,-1,18],[0.8,1,26],[0.83,-1,20],[0.87,1,24],[0.9,-1,30],[0.93,1,21]].forEach((h)=>{ const i=iu(h[0]), p=R[i], n=h[1]*(p.w0+h[2]), x=p.x+p.nx*n, y=p.y+p.ny*n; if(y>MT+10 && y<MB-8 && x<coastX(y)-12) HOUSES.push({i:i,sd:h[1],off:h[2],x:x,y:y}); }); }
  // ---------- 描画
  function pos(i,n){ const p=R[i]; return [p.x+p.nx*n,p.y+p.ny*n]; }
  function band(fa,fb){ ctx.beginPath(); for(let i=0;i<NS;i++){ const p=R[i], o=fa(p); if(i) ctx.lineTo(p.x+p.nx*o,p.y+p.ny*o); else ctx.moveTo(p.x+p.nx*o,p.y+p.ny*o); } for(let i=NS-1;i>=0;i--){ const p=R[i], o=fb(p); ctx.lineTo(p.x+p.nx*o,p.y+p.ny*o); } ctx.closePath(); }
  function grR(d){ return clamp(0.6+0.75*Math.log10(Math.max(d,0.1)),0.7,2.8); }
  function mixc(a,b,k){ return 'rgb('+Math.round(a[0]+(b[0]-a[0])*k)+','+Math.round(a[1]+(b[1]-a[1])*k)+','+Math.round(a[2]+(b[2]-a[2])*k)+')'; }
  function drawMap(pl){ const f=fW(), mud=clamp((Qnow()-1.6)/3.4,0,1);
    ctx.save(); ctx.beginPath(); ctx.rect(0,MT,W,MB-MT); ctx.clip();
    ctx.drawImage(BG,0,MT,W,MB-MT);
    band((p)=>p.bl,(p)=>-p.br); ctx.fillStyle='#e8dab8'; ctx.fill(); ctx.strokeStyle='rgba(120,98,60,.55)'; ctx.lineWidth=1; ctx.stroke();
    ROCKS.forEach((r)=>{ const a=pos(r.i,r.n); ctx.beginPath(); r.pts.forEach((q,k)=>{ if(k) ctx.lineTo(a[0]+q[0],a[1]+q[1]); else ctx.moveTo(a[0]+q[0],a[1]+q[1]); }); ctx.closePath(); ctx.fillStyle=r.big?'#8b8680':'#b5aea4'; ctx.fill(); if(r.big){ ctx.strokeStyle='#57534e'; ctx.lineWidth=0.8; ctx.stroke(); } });
    for(const sd of [1,-1]){ ctx.strokeStyle='#7c4a1e'; ctx.lineWidth=2.8; ctx.lineCap='round'; ctx.beginPath(); let on=false;
      for(let i=0;i<NS;i++){ const p=R[i], E=sd>0?p.EL:p.ER; if(E>1.2){ const a=pos(i,sd>0?p.bl:-p.br); if(on) ctx.lineTo(a[0],a[1]); else ctx.moveTo(a[0],a[1]); on=true; } else on=false; } ctx.stroke(); }
    GR.forEach((g)=>{ if(g.mv) return; let x, y; if(g.sea){ x=g.x; y=g.y; } else { const a=pos(clamp(Math.floor(g.s/DS),0,NS-1),g.n); x=a[0]; y=a[1]; } const r=grR(g.d)+0.45; ctx.fillStyle=g.d<2.5?'#b07d3c':(g.d<40?'#8f7a5c':'#625548'); ctx.fillRect(x-r,y-r,2*r,2*r); });
    band((p)=>p.eL,(p)=>p.eR); ctx.fillStyle=mixc([66,140,235],[150,112,70],mud); ctx.globalAlpha=0.86; ctx.fill(); ctx.globalAlpha=1;
    band((p)=>{ const k=clamp((Math.abs(p.K)-0.15)*1.4,0,1), w=0.42*(p.eL-p.eR)*k; return p.K>=0?p.eR+w:p.eL-w; },(p)=>p.K>=0?p.eR:p.eL);
    ctx.fillStyle=mixc([30,64,175],[110,72,40],mud); ctx.globalAlpha=0.45; ctx.fill(); ctx.globalAlpha=1;
    ctx.strokeStyle='rgba(255,255,255,.85)'; ctx.lineWidth=1.3; ctx.lineCap='round'; ctx.beginPath();
    WPS.forEach((w)=>{ const i=clamp(Math.floor(w.s/DS),0,NS-1), p=R[i], n=(p.eL+p.eR)/2+w.nw*(p.eL-p.eR)/2, j=clamp(Math.floor((w.s-w.v*0.13)/DS),0,NS-1), q=R[j], m=(q.eL+q.eR)/2+w.nw*(q.eL-q.eR)/2; ctx.moveTo(q.x+q.nx*m,q.y+q.ny*m); ctx.lineTo(p.x+p.nx*n,p.y+p.ny*n); }); ctx.stroke();
    GR.forEach((g)=>{ if(!g.mv) return; const a=pos(clamp(Math.floor(g.s/DS),0,NS-1),g.n), r=grR(g.d)+0.2; ctx.fillStyle=g.d<2.5?'#b7791f':(g.d<40?'#8a5a2b':'#5c4330'); ctx.beginPath(); ctx.arc(a[0],a[1],r,0,Math.PI*2); ctx.fill(); });
    let wet=0; HOUSES.forEach((h)=>{ const p=R[h.i], ov=f>1?(f-1)*(p.bl+p.br)*2.4*ovf(p.u):0, inw=ov>h.off-((h.sd>0?p.bl:p.br)-p.w0)-5;
      if(inw){ wet++; ctx.fillStyle='rgba(150,112,70,.55)'; ctx.beginPath(); ctx.ellipse(h.x,h.y+2,11,7,0,0,Math.PI*2); ctx.fill(); }
      ctx.fillStyle='#f8fafc'; ctx.fillRect(h.x-5,h.y-2,10,7); ctx.strokeStyle='#64748b'; ctx.lineWidth=1; ctx.strokeRect(h.x-5,h.y-2,10,7); ctx.fillStyle='#b45309'; ctx.beginPath(); ctx.moveTo(h.x-7,h.y-1); ctx.lineTo(h.x,h.y-7); ctx.lineTo(h.x+7,h.y-1); ctx.closePath(); ctx.fill(); });
    const ib=R[IBd], so=SGN>0?-1:1, oo=so>0?ib.bl:-ib.br, io=so>0?-ib.br:ib.bl, a1=pos(IBd,oo+so*24), a2=pos(IBd,io-so*26);
    txt('がけ（けずられる）',a1[0],a1[1]+4,'bold 11px sans-serif','#7c2d12','center',true); txt('川原（積もる）',a2[0],a2[1]+4,'bold 11px sans-serif','#854d0e','center',true);
    txt('山',36,MT+18,'bold 14px sans-serif','#3f6212','center',true); txt('上流',R[iu(0.1)].x,R[iu(0.1)].y+30,'bold 13px sans-serif','#1e3a8a','center',true);
    txt('中流',R[iu(0.5)].x+30,R[iu(0.5)].y+4,'bold 13px sans-serif','#1e3a8a','center',true); txt('下流',R[iu(0.8)].x-34,R[iu(0.8)].y-18,'bold 13px sans-serif','#1e3a8a','center',true);
    txt('平地',430,MB-12,'bold 12px sans-serif','#4d7c0f','center',true); txt('海',coastX(120)+18,MT+60,'bold 14px sans-serif','#1e3a8a','center',true);
    const sp=pos(pl.i,pl.n); ctx.strokeStyle='#ea580c'; ctx.lineWidth=2.6; ctx.beginPath(); ctx.arc(sp[0],sp[1],8,0,Math.PI*2); ctx.stroke(); ctx.strokeStyle='#fff'; ctx.lineWidth=1.2; ctx.beginPath(); ctx.arc(sp[0],sp[1],10,0,Math.PI*2); ctx.stroke();
    if(sp[0]<W-110) txt('◀ えらんだ場所',sp[0]+13,sp[1]+4,'bold 11px sans-serif','#c2410c','left',true); else txt('えらんだ場所 ▶',sp[0]-13,sp[1]+4,'bold 11px sans-serif','#c2410c','right',true);
    if(f>1.02){ const m='⚠ 川の水があふれています'+(wet?'（家のまわりまで水が来ています）':'')+'。大雨のときは川に近づかないようにしましょう'; txt(m,W/2,MB-30,'bold 12px sans-serif','#b91c1c','center',true); }
    ctx.restore(); ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1; ctx.strokeRect(0.5,MT+0.5,W-1,MB-MT-1); }
  function drawHead(pl,cnt){ ctx.fillStyle=fT>=0?'#dbeafe':'#f1f5f9'; rr(1,1,W-2,HB-2,8); ctx.fill();
    const s1=(fT>=0?'☔ 大雨で増水中！　':'')+'えらんだ場所：'+pl.name+'　流れの速さ：'+(pl.v>0?'秒速'+f1(pl.v)+'m':'0（水の外）')+'　石：'+fmtSize(pl.D);
    let font='bold 12.5px sans-serif'; if(tw(s1,font)>W-20) font='bold 11.5px sans-serif'; txt(s1,10,16,font,fT>=0?'#1d4ed8':'#0f172a');
    const L=[['けずられた土 '+num(eroded),'#b45309'],[' ＝ ','#475569'],['運ばれている土 '+num(cnt.mv),'#ea580c'],[' ＋ ','#475569'],['積もった土 '+num(cnt.rest),'#a16207'],['（つぶの数）','#64748b']];
    let x=10; L.forEach((p,k)=>{ const fo=k===5?'11px sans-serif':'bold 12.5px sans-serif'; txt(p[0],x,33,fo,p[1]); x+=tw(p[0],fo); }); }
  function drawProf(pl){ const xa=6, xb=W-40, base=PB-3, Hk=8+5.5*slope, zx=(u)=>base-4-Hk*Math.pow(1-u,2.2), X=(u)=>xa+(xb-xa)*u;
    txt('川の高さのようす（横から見た図）',6,PT-6,'bold 12px sans-serif','#0f172a'); txt('土地のかたむき：'+SLW[slope-1],W-6,PT-6,'11px sans-serif','#475569','right');
    ctx.fillStyle='#f8fafc'; ctx.fillRect(0,PT,W,PB-PT);
    ctx.beginPath(); ctx.moveTo(xa,PB); for(let k=0;k<=80;k++) ctx.lineTo(X(k/80),zx(k/80)); ctx.lineTo(xb,PB); ctx.closePath(); ctx.fillStyle='#d4bf95'; ctx.fill();
    ctx.strokeStyle=fT>=0?'#1d4ed8':'#3b82f6'; ctx.lineWidth=fT>=0?3.4:2.4; ctx.beginPath(); for(let k=0;k<=80;k++){ const u=k/80; if(k) ctx.lineTo(X(u),zx(u)-1.5); else ctx.moveTo(X(u),zx(u)-1.5); } ctx.stroke();
    ctx.fillStyle='#93c5fd'; ctx.fillRect(xb,base-4,W-xb,PB-base+4); txt('海',W-20,PB-8,'bold 11px sans-serif','#1e3a8a','center');
    txt('上流：かたむきが大きい',xa+4,PB-6,'bold 10.5px sans-serif','#713f12','left'); txt('中流',X(0.5),PB-6,'bold 10.5px sans-serif','#713f12','center'); txt('下流：ゆるやか',X(0.86),PB-6,'bold 10.5px sans-serif','#713f12','center');
    const us=pl.p.u, sx=X(us); ctx.setLineDash([3,3]); ctx.strokeStyle='#ea580c'; ctx.lineWidth=1.5; line(sx,PT+2,sx,PB); ctx.setLineDash([]); ctx.fillStyle='#ea580c'; ctx.beginPath(); ctx.arc(sx,zx(us)-1.5,4,0,Math.PI*2); ctx.fill();
    ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1; ctx.strokeRect(0.5,PT+0.5,W-1,PB-PT-1); }
  function drawXsec(pl){ const L0=4, R0=316, T0=IT, B0=IB, p=pl.p, u=p.u, sc=46/Math.sqrt(p.bl+p.br), f=fW(), cx=(L0+R0)/2, gy=T0+66, Dp=30+22*(1-u);
    txt('川の断面（下流の方を向いて見た図）',L0+2,T0-6,'bold 12px sans-serif','#0f172a');
    ctx.save(); ctx.beginPath(); ctx.rect(L0,T0,R0-L0,B0-T0); ctx.clip(); ctx.fillStyle='#f0f9ff'; ctx.fillRect(L0,T0,R0-L0,B0-T0);
    const xl=cx-p.bl*sc, xr=cx+p.br*sc, a=clamp((Math.abs(p.K)-0.12)*1.4,0,1), outR=p.K>0;
    const al=outR?0.8+0.6*a:0.8-0.45*a, be=outR?0.8-0.45*a:0.8+0.6*a, qm=al/(al+be), gm=Math.pow(qm,al)*Math.pow(1-qm,be), mx=Dp*(1+0.3*a);
    const dep=(q)=>mx*Math.pow(clamp(q,0,1),al)*Math.pow(clamp(1-q,0,1),be)/gm, vall=1.6*(1-ss(0.1,0.45,u));
    const ys=f<=1?gy+mx*(1-clamp((f-0.4)/0.6,0,1)):gy-(f-1)*(18+30*(1-ovf(u)));
    const kq=Kf()*Qf(), sp=(q)=>{ const nw=1-2*q; return Ub(u)*kq*(1-0.45*nw*nw)*(1-0.55*p.K*nw); };
    const wg=ctx.createLinearGradient(xl,0,xr,0); for(let k=0;k<=4;k++){ const q=k/4, v=clamp(sp(q)/2.6,0,1); wg.addColorStop(q,mixc([186,220,253],[29,78,216],v)); }
    const mud=clamp((Qnow()-1.6)/3.4,0,1); ctx.fillStyle=wg; ctx.fillRect(L0,ys,R0-L0,B0-ys); if(mud>0){ ctx.fillStyle='rgba(150,112,70,'+(0.55*mud).toFixed(2)+')'; ctx.fillRect(L0,ys,R0-L0,B0-ys); } ctx.strokeStyle='#1d4ed8'; ctx.lineWidth=1.6; line(L0,ys,R0,ys);
    ctx.beginPath(); ctx.moveTo(L0-2,gy-(xl-L0+2)*vall); ctx.lineTo(xl,gy); for(let k=1;k<40;k++){ const q=k/40; ctx.lineTo(xl+(xr-xl)*q,gy+dep(q)); } ctx.lineTo(xr,gy); ctx.lineTo(R0+2,gy-(R0+2-xr)*vall); ctx.lineTo(R0+2,B0+2); ctx.lineTo(L0-2,B0+2); ctx.closePath();
    ctx.fillStyle='#b08d5b'; ctx.fill(); ctx.strokeStyle='#6b4f2a'; ctx.lineWidth=1.5; ctx.stroke();
    ctx.strokeStyle='#65a30d'; ctx.lineWidth=3; line(L0,gy-(xl-L0)*vall-1.5,xl-2,gy-1.5); line(xr+2,gy-1.5,R0,gy-(R0-xr)*vall-1.5);
    const rg=rng(500+pl.i), D=pl.D, rad=clamp(1.2+1.6*Math.log10(D),1.2,7);
    for(let k=0;k<26;k++){ const q=0.04+0.92*rg(), x=xl+(xr-xl)*q, y=gy+dep(q)-rad*0.7; ctx.fillStyle=k%3?'#78716c':'#a8a29e'; ctx.beginPath(); ctx.ellipse(x,y,rad*(0.8+0.5*rg()),rad*0.7,0,0,Math.PI*2); ctx.fill(); }
    const px=cx-pl.n*sc; ctx.fillStyle='#ea580c'; ctx.beginPath(); ctx.moveTo(px,Math.min(ys,gy)-4); ctx.lineTo(px-6,Math.min(ys,gy)-14); ctx.lineTo(px+6,Math.min(ys,gy)-14); ctx.closePath(); ctx.fill();
    if(a>0.3){ const oL=!outR; const xo=oL?L0+6:R0-6, xi=oL?R0-6:L0+6, ao=oL?'left':'right', ai=oL?'right':'left';
      txt('外側（がけ）',xo,T0+16,'bold 12px sans-serif','#7c2d12',ao,true); txt('流れが速く、深い',xo,T0+31,'11px sans-serif','#1e3a8a',ao,true);
      txt('内側（川原）',xi,T0+16,'bold 12px sans-serif','#854d0e',ai,true); txt('流れがおそく、浅い',xi,T0+31,'11px sans-serif','#1e3a8a',ai,true); }
    else txt(u<0.3?'上流：川はばがせまく、谷が深い':(u>0.8?'下流：川はばが広く、浅い':'まっすぐな所：まん中が深く、流れが速い'),cx,T0+16,'bold 12px sans-serif','#334155','center',true);
    if(f>1.02) txt('水が岸をこえてあふれる！',cx,Math.max(T0+48,ys-6),'bold 13px sans-serif','#b91c1c','center',true);
    txt('こい青ほど流れが速い',R0-6,B0-6,'10px sans-serif','#1e3a8a','right',true);
    ctx.restore(); ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1; ctx.strokeRect(L0+0.5,T0+0.5,R0-L0-1,B0-T0-1); }
  function stone(cx,cy,rad,rd,rg){ const m=rd>0.6?11:(rd>0.3?8:6), pts=[];
    for(let k=0;k<m;k++){ const a=(k+(rg()-0.5)*0.6*(1-rd))/m*Math.PI*2, q=rad*(1-0.4*(1-rd)*rg()); pts.push([cx+Math.cos(a)*q*1.12,cy+Math.sin(a)*q*0.86]); }
    ctx.beginPath();
    if(rd>0.35){ const md=(a,b)=>[(a[0]+b[0])/2,(a[1]+b[1])/2]; const s0=md(pts[m-1],pts[0]); ctx.moveTo(s0[0],s0[1]); for(let k=0;k<m;k++){ const q=md(pts[k],pts[(k+1)%m]); ctx.quadraticCurveTo(pts[k][0],pts[k][1],q[0],q[1]); } }
    else { ctx.moveTo(pts[0][0],pts[0][1]); for(let k=1;k<m;k++) ctx.lineTo(pts[k][0],pts[k][1]); }
    ctx.closePath(); const cs=[['#e7e5e4','#78716c'],['#e2e8f0','#64748b'],['#f5f5f4','#a8a29e']][Math.floor(rg()*3)], gr=ctx.createRadialGradient(cx-rad*0.35,cy-rad*0.4,rad*0.1,cx,cy,rad*1.25);
    gr.addColorStop(0,cs[0]); gr.addColorStop(1,cs[1]); ctx.fillStyle=gr; ctx.fill(); ctx.strokeStyle='rgba(41,37,36,.6)'; ctx.lineWidth=1.2; ctx.stroke(); }
  function drawStones(pl){ const L0=324, R0=W-4, T0=IT, B0=IB, D=pl.D, rd=pl.r, rg=rng(1000+pl.i*7);
    txt('えらんだ場所の川原の石（ズーム）',L0+2,T0-6,'bold 12px sans-serif','#0f172a');
    ctx.save(); ctx.beginPath(); ctx.rect(L0,T0,R0-L0,B0-T0); ctx.clip(); ctx.fillStyle='#efe5cc'; ctx.fillRect(L0,T0,R0-L0,B0-T0);
    ctx.fillStyle='#d8c79f'; for(let k=0;k<260;k++){ ctx.fillRect(L0+rg()*(R0-L0),T0+rg()*(B0-T0),1.4,1.4); }
    const pxmm=46/D, cw=(R0-L0-16)/4, top=T0+40, ch=(B0-28-top)/2;
    for(let r2=0;r2<2;r2++) for(let c=0;c<4;c++){ const z=Math.sqrt(-2*Math.log(rg()+1e-9))*Math.cos(2*Math.PI*rg()), sz=clamp(D*Math.exp(0.3*z)*pxmm,16,Math.min(cw,ch)-4);
      stone(L0+8+cw*(c+0.5)+(rg()-0.5)*8,top+ch*(r2+0.5)+(rg()-0.5)*6,sz/2,rd,rg); }
    ctx.fillStyle='rgba(255,255,255,.88)'; rr(L0+4,T0+4,R0-L0-8,32,6); ctx.fill();
    txt('大きさ：'+fmtSize(D)+'（'+sizeWord(D)+'）',L0+10,T0+18,'bold 12px sans-serif','#0f172a'); txt('形：'+shapeWord(rd),L0+10,T0+32,'bold 12px sans-serif','#7c2d12');
    const NL=[1,2,5,10,20,50,100,200,500]; let Lm=1; NL.forEach((v)=>{ if(v*pxmm<=110) Lm=v; }); const bx=L0+10, by=B0-12, bw=Lm*pxmm;
    ctx.strokeStyle='#0f172a'; ctx.lineWidth=2.4; line(bx,by,bx+bw,by); line(bx,by-5,bx,by+3); line(bx+bw,by-5,bx+bw,by+3);
    txt(Lm>=10?(Lm/10)+'cm':Lm+'mm',bx+bw+6,by+4,'bold 11px sans-serif','#0f172a','left',true);
    ctx.restore(); ctx.strokeStyle='#94a3b8'; ctx.lineWidth=1; ctx.strokeRect(L0+0.5,T0+0.5,R0-L0-1,B0-T0-1); }
  function draw(){ const pl=place(); let mv=0; GR.forEach((g)=>{ if(g.mv) mv++; }); const cnt={mv:mv,rest:GR.length-mv+restOld};
    ctx.clearRect(0,0,W,H); ctx.fillStyle='#fff'; ctx.fillRect(0,0,W,H);
    drawHead(pl,cnt); drawMap(pl); drawProf(pl); drawXsec(pl); drawStones(pl);
    setStat('sV',pl.v>0?'秒速'+f1(pl.v)+'m':'0（水の外）'); setStat('sE',num(eroded)+'つぶ'); setStat('sD',num(cnt.rest)+'つぶ'); setStat('sS',fmtSize(pl.D));
    setShare('【流れる水のはたらき】土地のかたむき「'+SLW[slope-1]+'」・水の量「'+QW[qs-1]+'」のとき、'+pl.name+'の流れは秒速'+f1(pl.v)+'m。けずられた土'+num(eroded)+'つぶのうち'+num(cnt.rest)+'つぶが積もった｜シミュラボ'); }
  // ---------- 操作
  function labs(){ $('slopeL').textContent=SLW[slope-1]; $('qqL').textContent=QW[qs-1]; }
  function resetAll(){ R.forEach((p)=>{ p.bl=p.w0; p.br=p.w0; p.EL=0; p.ER=0; p.aL=0; p.aR=0; }); GR=[]; eroded=0; restOld=0; upAcc=0; fT=-1; flood=0; $('rain').disabled=false; $('rain').textContent='☔ 大雨をふらせる'; geomAll(); dirty=true; }
  function pxy(e){ const p=cpos(cv,e); return [p[0]/dpr,p[1]/dpr]; }
  function pick(x,y){ if(y>=MT && y<=MB){ let best=-1, bd=1e9; for(let i=0;i<NS;i++){ const d=(R[i].x-x)*(R[i].x-x)+(R[i].y-y)*(R[i].y-y); if(d<bd){ bd=d; best=i; } } if(bd>48*48) return false; const p=R[best], n=(x-p.x)*p.nx+(y-p.y)*p.ny; sel={i:best,n:clamp(n,-(p.br+40),p.bl+40),rel:null}; }
    else if(y>=PT && y<=PB){ sel={i:clamp(Math.round((x-6)/(W-46)*(NS-1)),0,NS-1),rel:0}; } else return false;
    $('place').value='tap'; dirty=true; return true; }
  cv.addEventListener('pointerdown',(e)=>{ const q=pxy(e); if(!pick(q[0],q[1])) return; drag=true; try{ cv.setPointerCapture(e.pointerId); }catch(err){ } e.preventDefault(); });
  cv.addEventListener('pointermove',(e)=>{ if(!drag) return; const q=pxy(e); pick(q[0],q[1]); });
  ['pointerup','pointercancel'].forEach((n)=>cv.addEventListener(n,()=>{ drag=false; }));
  $('place').addEventListener('change',()=>preset($('place').value));
  $('slope').addEventListener('input',()=>{ slope=+$('slope').value; labs(); dirty=true; });
  $('qq').addEventListener('input',()=>{ qs=+$('qq').value; labs(); dirty=true; });
  $('early').addEventListener('input',()=>{ early=+$('early').value; });
  $('play').addEventListener('click',()=>{ playing=!playing; $('play').textContent=playing?'⏸ 一時停止':'▶ 再生'; });
  $('rain').addEventListener('click',()=>{ if(fT>=0) return; fT=0; playing=true; $('play').textContent='⏸ 一時停止'; $('rain').disabled=true; $('rain').textContent='☔ 大雨（増水中…）'; });
  $('reset').addEventListener('click',resetAll);
  function frame(now){ const dt=Math.min(0.05,Math.max(0,(now-last)/1000)); last=now;
    if(playing){ step(dt); dirty=true; }
    if(dirty){ dirty=false; draw(); }
    requestAnimationFrame(frame); }
  mkBG(); mkDecor(); resetAll(); preset('out'); labs(); draw(); requestAnimationFrame(frame);
'''.replace("@CPT@", CPT_JS))
