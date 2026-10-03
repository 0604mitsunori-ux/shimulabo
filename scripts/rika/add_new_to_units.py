# -*- coding: utf-8 -*-
"""第1弾の新規10本を units.json（/rika/ の単元表）に入れる（冪等）。各グループの先頭に置く。
   使い方: python scripts/rika/add_new_to_units.py  → その後 python scripts/rika/build.py"""
import io, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "units.json")
U = json.load(io.open(P, encoding="utf-8"))

# (セクションid, グループ名, id, 単元ラベル, 授業での使いどころ)
NEW = [
    ("sho", "4年", "tsuki-michikake", "小4 月と星", "日付と時刻を動かすと、月の形・見える方角・時刻が変わる。宇宙から見た位置と、地上から見た形を並べて確かめる。"),
    ("sho", "4年", "denki-kairo", "小4 電流の働き", "乾電池の数とつなぎ方（直列・並列）で、豆電球の明るさやモーターの回り方がどう変わるか。"),
    ("sho", "4年", "joutai-henka", "小4 金属，水，空気と温度", "水を温めたり冷やしたりしたときの、すがたと体積の変わり方を粒のモデルとグラフで。"),
    ("sho", "5年", "furiko-jikken", "小5 振り子の運動", "糸の長さ・おもりの重さ・振れ幅を1つずつ変えて、10往復の時間を測って表にまとめる。"),
    ("sho", "6年", "teko-tsuriai", "小6 てこの規則性", "左右の目盛りにおもりを置いて、つり合うきまり（おもりの重さ×支点からの距離）を見つける。"),
    ("sho", "6年", "tsuki-michikake", "小6 月と太陽", "月の輝いている側に太陽がある。太陽と月の位置関係で月の形が変わることを確かめる。"),
    ("sho", "6年", "gesshoku-nisshoku", "小6 月と太陽（発展）", "太陽・地球・月が一直線に並ぶと月食・日食になる。毎月は起きない理由も。"),
    ("chu", "第1分野（物理・化学）", "totsu-lens", "中1 光と音（凸レンズのはたらき）", "物体の位置を動かすと、実像・虚像と大きさが変わる。3本の光で作図を確かめる。"),
    ("chu", "第1分野（物理・化学）", "joutai-henka", "中1 状態変化", "温度で粒子の動きと間隔が変わり、状態と体積が変わる。融点・沸点で温度が一定になるグラフも。"),
    ("chu", "第1分野（物理・化学）", "denki-kairo", "中2 電流（回路と電流・電圧、オームの法則）", "抵抗の直列・並列で電流と電圧がどう分かれるか。電圧と電流のグラフでオームの法則を確かめる。"),
    ("chu", "第2分野（生物・地学）", "jishin-ha", "中1 火山と地震（地震の伝わり方）", "P波とS波が広がる様子と、各地の地震計の記録。初期微動継続時間が震源からの距離に比例することを確かめる。"),
    ("chu", "第2分野（生物・地学）", "shitsudo-roten", "中2 気象観測・天気の変化（霧や雲の発生）", "飽和水蒸気量のグラフ上で空気を冷やすと、露点で水滴ができる。湿度の計算と、雲ができ始める高さ。"),
    ("chu", "第2分野（生物・地学）", "mendel-iden", "中3 遺伝の規則性と遺伝子", "丸い種子としわの種子のかけ合わせを数千回試すと、孫の代で 3：1 に近づく。"),
    ("chu", "第2分野（生物・地学）", "tsuki-michikake", "中3 月や金星の運動と見え方", "上弦の月は夕方に南の空、真夜中に西に沈む——宇宙から見た位置と見え方を連動させて確かめる。"),
    ("chu", "第2分野（生物・地学）", "gesshoku-nisshoku", "中3 月や金星の運動と見え方（発展）", "日食・月食が起きる位置関係と、月の通り道の傾き。"),
    ("ko", "物理基礎・物理", "denki-kairo", "物理基礎 電気（電気抵抗）", "直列・並列の合成抵抗と、各部分の電流・電圧・電力。"),
    ("ko", "物理基礎・物理", "totsu-lens", "物理 光（レンズ）", "レンズの式 1/a＋1/b＝1/f と倍率を、物体の位置を動かして確かめる。"),
    ("ko", "地学基礎・地学", "jishin-ha", "地学基礎 活動する地球（地震）", "P波・S波の速さと震源距離・初期微動継続時間の関係（大森公式）。"),
]
added = 0
for sec_id, gtitle, sid, unit, use in reversed(NEW):
    sec = next(s for s in U["sections"] if s["id"] == sec_id)
    g = next(g for g in sec["groups"] if g["title"] == gtitle)
    if any(it["id"] == sid and it["unit"] == unit for it in g["items"]): continue
    g["items"].insert(0, {"id": sid, "unit": unit, "use": use}); added += 1
U["shelf"] = ["tsuki-michikake", "denki-kairo", "shitsudo-roten", "jishin-ha", "teko-tsuriai", "totsu-lens", "mendel-iden", "gears"]
json.dump(U, io.open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"追加 {added}か所")
