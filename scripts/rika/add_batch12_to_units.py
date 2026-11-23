# -*- coding: utf-8 -*-
"""リクエスト（2026-11-23 受付・高校生物のPCR法）1本を units.json（/rika/ の単元表）に入れる（冪等）。グループの先頭に置く。
   使い方: python scripts/rika/add_batch12_to_units.py  → その後 python scripts/rika/build.py"""
import io, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "units.json")
U = json.load(io.open(P, encoding="utf-8"))

NEW = [
    ("ko", "生物基礎・生物", "pcr-hou", "生物 遺伝情報の発現と発生（遺伝子を扱う技術：PCR法）", "熱変性・アニーリング・伸長の3段階を1段階ずつ止めて、DNA・プライマー・DNAポリメラーゼの動きと鎖の向き（5′→3′）を確かめる。1〜3サイクル目で目的の長さのDNAができる過程と、サイクルごとに2倍に増えることを、鎖の色分けとグラフで追う。"),
]
added = 0
for sec_id, gtitle, sid, unit, use in reversed(NEW):
    sec = next(s for s in U["sections"] if s["id"] == sec_id)
    g = next(g for g in sec["groups"] if g["title"] == gtitle)
    if any(it["id"] == sid and it["unit"] == unit for it in g["items"]): continue
    g["items"].insert(0, {"id": sid, "unit": unit, "use": use}); added += 1
json.dump(U, io.open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"追加 {added}か所")
