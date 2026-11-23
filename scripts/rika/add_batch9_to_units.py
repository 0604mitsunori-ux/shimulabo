# -*- coding: utf-8 -*-
"""リクエスト（2026-11-23 受付・高校生物のセッケン・シャボン玉・細胞膜）1本を units.json（/rika/ の単元表）に入れる（冪等）。グループの先頭に置く。
   使い方: python scripts/rika/add_batch9_to_units.py  → その後 python scripts/rika/build.py"""
import io, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "units.json")
U = json.load(io.open(P, encoding="utf-8"))

NEW = [
    ("ko", "生物基礎・生物", "sekken-shabondama", "生物 細胞と分子（生体物質と細胞：親水部・疎水部と生体膜）", "セッケンの油汚れ落とし・シャボン玉の膜・リン脂質二重層を見比べ、「親水部は水の側、疎水部は水のない側」という決まりから細胞膜の構造を予想させる。分子をかくして予想→答え合わせができる。"),
    ("ko", "化学基礎・化学", "sekken-shabondama", "化学 有機化合物（油脂とセッケン：界面活性剤・ミセル・乳化）", "セッケン分子が水面に並び、濃度が高くなるとミセルをつくる様子、油汚れを取り囲んで油滴にする乳化のしくみを見る。"),
]
added = 0
for sec_id, gtitle, sid, unit, use in reversed(NEW):
    sec = next(s for s in U["sections"] if s["id"] == sec_id)
    g = next(g for g in sec["groups"] if g["title"] == gtitle)
    if any(it["id"] == sid and it["unit"] == unit for it in g["items"]): continue
    g["items"].insert(0, {"id": sid, "unit": unit, "use": use}); added += 1
json.dump(U, io.open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"追加 {added}か所")
