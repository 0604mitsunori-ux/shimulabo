# -*- coding: utf-8 -*-
"""リクエスト（2026-11-23 受付・高校生物の酵素の失活）1本を units.json（/rika/ の単元表）に入れる（冪等）。グループの先頭に置く。
   使い方: python scripts/rika/add_batch8_to_units.py  → その後 python scripts/rika/build.py"""
import io, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "units.json")
U = json.load(io.open(P, encoding="utf-8"))

NEW = [
    ("ko", "生物基礎・生物", "kouso-shikkatsu", "生物 細胞と分子（生命現象とタンパク質：酵素の働きと立体構造・変性と失活）", "温度とpHを変えて、立体構造を支える水素結合・イオン結合・疎水性相互作用・ジスルフィド結合と活性部位の変化を見る。低温でおそい状態、高温で変性した状態、pHで活性部位の電荷が変わった状態を比べ、温度・pHと酵素活性のグラフと結び付ける。"),
]
added = 0
for sec_id, gtitle, sid, unit, use in reversed(NEW):
    sec = next(s for s in U["sections"] if s["id"] == sec_id)
    g = next(g for g in sec["groups"] if g["title"] == gtitle)
    if any(it["id"] == sid and it["unit"] == unit for it in g["items"]): continue
    g["items"].insert(0, {"id": sid, "unit": unit, "use": use}); added += 1
json.dump(U, io.open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"追加 {added}か所")
