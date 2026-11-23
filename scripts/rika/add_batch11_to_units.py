# -*- coding: utf-8 -*-
"""リクエスト（2026-11-23 受付・高校生物・化学の脂肪酸と融点）1本を units.json（/rika/ の単元表）に入れる（冪等）。グループの先頭に置く。
   使い方: python scripts/rika/add_batch11_to_units.py  → その後 python scripts/rika/build.py"""
import io, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "units.json")
U = json.load(io.open(P, encoding="utf-8"))

NEW = [
    ("ko", "生物基礎・生物", "shibousan-yuuten", "生物 細胞と分子（生体物質と細胞：脂質・脂肪酸の構造と性質）", "炭素数18のステアリン酸・オレイン酸・エライジン酸を比べ、シス型の二重結合による鎖の折れ曲がりが、分子の並び方と融点のちがいにつながることを見る。生体膜の流動性を考える基礎になる。"),
    ("ko", "化学基礎・化学", "shibousan-yuuten", "化学 有機化合物（油脂：飽和脂肪酸と不飽和脂肪酸・シス-トランス異性体と融点）", "飽和脂肪酸と不飽和脂肪酸、シス型とトランス型で、鎖の形・分子どうしの接し方・融点がどう変わるかを、温度を変えながら比べる。単結合の回転と二重結合の回転できない性質も見られる。"),
]
added = 0
for sec_id, gtitle, sid, unit, use in reversed(NEW):
    sec = next(s for s in U["sections"] if s["id"] == sec_id)
    g = next(g for g in sec["groups"] if g["title"] == gtitle)
    if any(it["id"] == sid and it["unit"] == unit for it in g["items"]): continue
    g["items"].insert(0, {"id": sid, "unit": unit, "use": use}); added += 1
json.dump(U, io.open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"追加 {added}か所")
