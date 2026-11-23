# -*- coding: utf-8 -*-
"""リクエスト（2026-11-23 受付・高校生物の原核生物の転写と翻訳）1本を units.json（/rika/ の単元表）に入れる（冪等）。グループの先頭に置く。
   使い方: python scripts/rika/add_batch13_to_units.py  → その後 python scripts/rika/build.py"""
import io, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "units.json")
U = json.load(io.open(P, encoding="utf-8"))

NEW = [
    ("ko", "生物基礎・生物", "tensha-honyaku-genkaku", "生物 遺伝情報の発現と発生（遺伝情報とその発現：原核生物の転写と翻訳）", "RNAポリメラーゼがmRNAを合成している途中で、リボソームが結合して翻訳が始まる様子を見る。mRNAの5′・3′端、転写と翻訳の進む向き、ポリソーム、コドンとtRNA、終止コドンと転写終結部位のちがいを、途中で止めて予想させながら確かめる。"),
]
added = 0
for sec_id, gtitle, sid, unit, use in reversed(NEW):
    sec = next(s for s in U["sections"] if s["id"] == sec_id)
    g = next(g for g in sec["groups"] if g["title"] == gtitle)
    if any(it["id"] == sid and it["unit"] == unit for it in g["items"]): continue
    g["items"].insert(0, {"id": sid, "unit": unit, "use": use}); added += 1
json.dump(U, io.open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"追加 {added}か所")
