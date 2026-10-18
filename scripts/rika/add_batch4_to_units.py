# -*- coding: utf-8 -*-
"""第4弾（高校）6本（2026-10-18）を units.json（/rika/ の単元表）に入れる（冪等）。各グループの先頭に置く。
   使い方: python scripts/rika/add_batch4_to_units.py  → その後 python scripts/rika/build.py"""
import io, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "units.json")
U = json.load(io.open(P, encoding="utf-8"))

# (セクションid, グループ名, id, 単元ラベル, 授業での使いどころ)
NEW = [
    ("ko", "物理基礎・物理", "tan-shindou", "物理 円運動と単振動（ばね振り子・単振り子）", "ばね定数・質量・振幅を変えて、単振動が等速円運動の正射影であること、周期 T=2π√(m/k) が振幅によらないことを、x・v・a のグラフとエネルギーの棒グラフで確かめる。"),
    ("ko", "物理基礎・物理", "unari-teijouha", "物理基礎 波（音と振動：うなり・定常波・弦と気柱の固有振動）", "2つの音を重ねてうなり（|f1−f2| 回/秒）を実際に聞く。逆向きの2つの波から定常波の腹と節ができる様子と、弦・閉管・開管の固有振動数。"),
    ("ko", "化学基礎・化学", "denshi-haichi", "化学基礎 物質の構成粒子（原子の構造・電子配置）", "原子番号を選ぶと電子殻（K・L・M・N）に電子が入り、価電子の数と周期表の族の関係、イオンになって貴ガスと同じ配置になる様子を見る。"),
    ("ko", "生物基礎・生物", "iden-fudou", "生物 遺伝子の変化と進化の仕組み（遺伝的浮動・ハーディー・ワインベルグの法則）", "集団の大きさと選択の強さを変えて、対立遺伝子頻度が世代ごとにゆらぎ、小さい集団ほど早く固定・消失する様子を複数の集団で比べる。平衡の確かめも。"),
    ("ko", "地学基礎・地学", "coriolis-henseifu", "地学基礎・地学 大気と海洋（コリオリの力・大気の大循環）", "回る円盤の上で投げた玉が右へそれる様子（回転系と静止系）から、緯度とコリオリの力、低気圧のまわりの風、貿易風・偏西風・極偏東風の向きまでをつなげる。"),
    ("ko", "地学基礎・地学", "eratosthenes", "地学基礎 地球のすがた（地球の大きさ）", "エラトステネスの方法（夏至の正午の影の角度と2地点の距離）で地球一周の長さを計算する。日本の2地点でも試せる。"),
]
added = 0
for sec_id, gtitle, sid, unit, use in reversed(NEW):
    sec = next(s for s in U["sections"] if s["id"] == sec_id)
    g = next(g for g in sec["groups"] if g["title"] == gtitle)
    if any(it["id"] == sid and it["unit"] == unit for it in g["items"]): continue
    g["items"].insert(0, {"id": sid, "unit": unit, "use": use}); added += 1
json.dump(U, io.open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"追加 {added}か所")
