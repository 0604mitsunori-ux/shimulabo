# -*- coding: utf-8 -*-
"""リクエスト（2026-11-14 受付・高校生物の細胞膜）2本を units.json（/rika/ の単元表）に入れる（冪等）。各グループの先頭に置く。
   使い方: python scripts/rika/add_batch6_to_units.py  → その後 python scripts/rika/build.py"""
import io, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "units.json")
U = json.load(io.open(P, encoding="utf-8"))

# (セクションid, グループ名, id, 単元ラベル, 授業での使いどころ)
NEW = [
    ("ko", "生物基礎・生物", "rinshishitsu-maku", "生物 細胞と分子（生体物質と細胞：リン脂質と生体膜）", "親水性の頭と疎水性の尾をもつ分子が、水面に並び、水中でミセルや脂質二重層に集まっていく過程を観察する。尾が1本と2本、分子の数（濃度）で比べ、小胞の安定性も確かめる。"),
    ("ko", "生物基礎・生物", "maku-yuso", "生物 細胞と分子（生命現象とタンパク質：膜輸送タンパク質）", "単純拡散・チャネル・担体・ナトリウムポンプを切り替え、受動輸送では濃度差がなくなり、能動輸送（ATPを使う）では濃度差ができることをグラフで比べる。"),
    ("ko", "化学基礎・化学", "rinshishitsu-maku", "化学 有機化合物（油脂とセッケン：界面活性剤・ミセル）", "セッケンのような尾が1本の分子が、水面に並んで単分子膜をつくり、水面が埋まると水中でミセルをつくる様子を見る。"),
]
added = 0
for sec_id, gtitle, sid, unit, use in reversed(NEW):
    sec = next(s for s in U["sections"] if s["id"] == sec_id)
    g = next(g for g in sec["groups"] if g["title"] == gtitle)
    if any(it["id"] == sid and it["unit"] == unit for it in g["items"]): continue
    g["items"].insert(0, {"id": sid, "unit": unit, "use": use}); added += 1
json.dump(U, io.open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"追加 {added}か所")
