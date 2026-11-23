# -*- coding: utf-8 -*-
"""リクエスト（2026-11-23 受付・高校生物のウイルスと洗剤・エタノール）1本を units.json（/rika/ の単元表）に入れる（冪等）。グループの先頭に置く。
   使い方: python scripts/rika/add_batch10_to_units.py  → その後 python scripts/rika/build.py"""
import io, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "units.json")
U = json.load(io.open(P, encoding="utf-8"))

NEW = [
    ("ko", "生物基礎・生物", "virus-sekken-alcohol", "生物 細胞と分子（生体膜・タンパク質の変性の応用：ウイルスと手洗い・消毒）", "エンベロープをもつ・もたないウイルスを並べ、洗剤の界面活性剤やエタノールが、脂質二重層と膜のタンパク質にどう作用して感染性を失わせるかを見る。リン脂質の親水性・疎水性、タンパク質の変性の学習を、手洗い・消毒のしくみと結び付ける。"),
]
added = 0
for sec_id, gtitle, sid, unit, use in reversed(NEW):
    sec = next(s for s in U["sections"] if s["id"] == sec_id)
    g = next(g for g in sec["groups"] if g["title"] == gtitle)
    if any(it["id"] == sid and it["unit"] == unit for it in g["items"]): continue
    g["items"].insert(0, {"id": sid, "unit": unit, "use": use}); added += 1
json.dump(U, io.open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"追加 {added}か所")
