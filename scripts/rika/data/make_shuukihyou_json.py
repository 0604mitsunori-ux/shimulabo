# -*- coding: utf-8 -*-
"""周期表ページ用の元素データを作る（1回だけ実行・結果の shuukihyou.json をコミット）。
   元データ：PubChem Periodic Table（https://pubchem.ncbi.nlm.nih.gov/periodic-table/）の CSV
   使い方：python -I make_shuukihyou_json.py <pubchem.csv のパス>"""
import csv, json, re, sys, io, os
JA = ("水素 ヘリウム リチウム ベリリウム ホウ素 炭素 窒素 酸素 フッ素 ネオン ナトリウム マグネシウム アルミニウム ケイ素 リン 硫黄 塩素 アルゴン "
      "カリウム カルシウム スカンジウム チタン バナジウム クロム マンガン 鉄 コバルト ニッケル 銅 亜鉛 ガリウム ゲルマニウム ヒ素 セレン 臭素 クリプトン "
      "ルビジウム ストロンチウム イットリウム ジルコニウム ニオブ モリブデン テクネチウム ルテニウム ロジウム パラジウム 銀 カドミウム インジウム スズ アンチモン テルル ヨウ素 キセノン "
      "セシウム バリウム ランタン セリウム プラセオジム ネオジム プロメチウム サマリウム ユウロピウム ガドリニウム テルビウム ジスプロシウム ホルミウム エルビウム ツリウム イッテルビウム ルテチウム "
      "ハフニウム タンタル タングステン レニウム オスミウム イリジウム 白金 金 水銀 タリウム 鉛 ビスマス ポロニウム アスタチン ラドン "
      "フランシウム ラジウム アクチニウム トリウム プロトアクチニウム ウラン ネプツニウム プルトニウム アメリシウム キュリウム バークリウム カリホルニウム アインスタイニウム フェルミウム メンデレビウム ノーベリウム ローレンシウム "
      "ラザホージウム ドブニウム シーボーギウム ボーリウム ハッシウム マイトネリウム ダームスタチウム レントゲニウム コペルニシウム ニホニウム フレロビウム モスコビウム リバモリウム テネシン オガネソン").split()
assert len(JA) == 118, len(JA)
CORE = {"He": "1s2", "Ne": "[He]2s2 2p6", "Ar": "[Ne]3s2 3p6", "Kr": "[Ar]3d10 4s2 4p6", "Xe": "[Kr]4d10 5s2 5p6", "Rn": "[Xe]4f14 5d10 6s2 6p6"}
def expand(c):
    c = re.sub(r"\(.*?\)", "", c).strip()
    while "[" in c:
        c = re.sub(r"\[(\w+)\]", lambda m: CORE[m.group(1)] + " ", c)
    return re.findall(r"(\d)([spdf])(\d+)", c)
def pos(z):
    """(族, 周期, 表の行) 表の行 8=ランタノイド 9=アクチノイド"""
    if z == 1: return 1, 1, 1
    if z == 2: return 18, 1, 1
    starts = [(3, 2), (11, 3), (19, 4), (37, 5), (55, 6), (87, 7)]
    for zs, p in reversed(starts):
        if z >= zs: break
    i = z - zs
    if p in (2, 3):
        return (i + 1 if i < 2 else i + 11), p, p
    if p in (4, 5):
        return i + 1, p, p
    # 6・7周期：i=2〜16 が f ブロック（57〜71 / 89〜103）
    if i < 2: return i + 1, p, p
    if i <= 16: return 3, p, 8 if p == 6 else 9
    return i - 13, p, p
NONMETAL = {1, 2, 6, 7, 8, 9, 10, 15, 16, 17, 18, 34, 35, 36, 53, 54, 86}
HALF = {5, 14, 32, 33, 51, 52}   # 半金属（教科書で扱いが分かれる）
def kind(z, g, row):
    if z == 1: return "h"
    if g == 18: return "noble"
    if g == 17 and z != 117: return "halogen"
    if g == 1: return "alkali"
    if g == 2: return "alkaline"
    if row in (8, 9): return "lan" if row == 8 else "act"
    if 3 <= g <= 12: return "trans"
    if z in NONMETAL: return "nonmetal"
    if z in HALF: return "half"
    return "metal"
def f(x):
    try: return float(x)
    except: return None
out = []
for r in csv.DictReader(io.open(sys.argv[1], encoding="utf-8")):
    z = int(r["AtomicNumber"]); g, p, row = pos(z)
    sh = [0] * 7
    for n, l, k in expand(r["ElectronConfiguration"]): sh[int(n) - 1] += int(k)
    while sh and sh[-1] == 0: sh.pop()
    assert sum(sh) == z, (z, r["ElectronConfiguration"], sh)
    y = r["YearDiscovered"]
    out.append(dict(z=z, s=r["Symbol"], ja=JA[z - 1], en=r["Name"], m=f(r["AtomicWeight"]), g=g, p=p, row=row, k=kind(z, g, row),
                    sh=sh, ec=r["ElectronConfiguration"], en_=f(r["Electronegativity"]), ie=f(r["IonizationEnergy"]),
                    rad=f(r["AtomicRadius"]), mp=f(r["MeltingPoint"]), bp=f(r["BoilingPoint"]), d=f(r["Density"]),
                    st=r["StandardState"], y=(0 if y == "Ancient" else int(y)) if y else None))
assert len(out) == 118
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shuukihyou.json")
io.open(p, "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
print("ok", p, len(out))
