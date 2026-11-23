# -*- coding: utf-8 -*-
"""リクエスト（2026-11-23 受付・高校生物の酵素）2本を units.json（/rika/ の単元表）に入れる（冪等）。グループの先頭に置く。
   使い方: python scripts/rika/add_batch7_to_units.py  → その後 python scripts/rika/build.py"""
import io, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "units.json")
U = json.load(io.open(P, encoding="utf-8"))

NEW = [
    ("ko", "生物基礎・生物", "kouso-hannou-sokudo", "生物 細胞と分子（生命現象とタンパク質：酵素の反応速度）", "酵素と基質の数を変え、時間と生成物量のグラフ、酵素濃度・基質濃度と反応開始直後の反応速度のグラフを、粒子の動きと同時に見る。酵素を増やしても最終量は同じ、基質を増やすと反応速度が頭打ちになることを確かめる。"),
    ("ko", "生物基礎・生物", "kouso-sogai", "生物 細胞と分子（生命現象とタンパク質：競争的阻害・非競争的阻害）", "阻害剤なし・競争的阻害・非競争的阻害の3条件で、阻害剤の結合する場所と、基質濃度―反応速度の曲線のちがいを比べる。基質を増やすと競争的阻害では最大反応速度に近づき、非競争的阻害では届かない。"),
]
added = 0
for sec_id, gtitle, sid, unit, use in reversed(NEW):
    sec = next(s for s in U["sections"] if s["id"] == sec_id)
    g = next(g for g in sec["groups"] if g["title"] == gtitle)
    if any(it["id"] == sid and it["unit"] == unit for it in g["items"]): continue
    g["items"].insert(0, {"id": sid, "unit": unit, "use": use}); added += 1
json.dump(U, io.open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"追加 {added}か所")
