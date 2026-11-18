# -*- coding: utf-8 -*-
"""人口ピラミッド用データを公的統計の原表（xlsx）から作る（2026-11-18）。
  実績 1950〜2020年: 総務省統計局 国勢調査 時系列データ 第2表「年齢（5歳階級），男女別人口及び人口性比－全国（大正9年～令和2年）」
     e-Stat statInfId=000001085926（jinko_src/kokusei_jikei_da02.xlsx）。2015・2020年は不詳補完値（※）、それ以前は原数値（年齢不詳を除く）
  推計 2025〜2070年: 国立社会保障・人口問題研究所「日本の将来推計人口（令和5年推計）」表1-9A 出生中位（死亡中位）（jinko_src/ipss_r5_1-9a.xlsx）
  年齢は 0〜4 … 80〜84, 85歳以上 の18階級にそろえる（2000年以前の国勢調査が85歳以上までのため）。単位は千人。"""
import json, os, re, sys, openpyxl
sys.stdout.reconfigure(encoding="utf-8")
D = os.path.dirname(os.path.abspath(__file__))
AG = [f"{a}〜{a+4}" for a in range(0, 85, 5)] + ["85〜"]
out = {}
# 国勢調査
ws = openpyxl.load_workbook(os.path.join(D, "jinko_src", "kokusei_jikei_da02.xlsx"), data_only=True).active
rows = {}
for r in ws.iter_rows(min_row=15, values_only=True):
    if not r[0]: continue
    y = int(str(r[0])[:4]); rows.setdefault((y, r[3]), []).append(r)
for y in range(1950, 2021, 5):
    rs = rows.get((y, "※")) or rows[(y, None)]
    m = [0.0] * 18; f = [0.0] * 18; tot = None
    for r in rs:
        lab = str(r[2])
        if lab == "総数" and tot is None: tot = r[4]
        mm = re.match(r"^(\d+)～(\d+)歳$", lab); mo = re.match(r"^(\d+)歳以上$", lab)
        if mm: a = int(mm.group(1))
        elif mo: a = int(mo.group(1))
        else: continue
        i = min(a // 5, 17)
        if mo and a < 85: raise SystemExit(f"{y}: unexpected {lab}")
        m[i] += r[5] or 0; f[i] += r[6] or 0
    if tot is None: tot = next(r[4] for r in rows[(y, None)] if str(r[2]) == "総数")
    out[y] = {"src": "census", "total": round(tot / 1000, 1), "m": [round(v / 1000, 1) for v in m], "f": [round(v / 1000, 1) for v in f]}
# 社人研 推計
wb = openpyxl.load_workbook(os.path.join(D, "jinko_src", "ipss_r5_1-9a.xlsx"), data_only=True)
for ws in wb:
    y = None; acc = None
    for r in ws.iter_rows(values_only=True):
        h = str(r[0] or "")
        my = re.search(r"\((\d{4})\)年", h)
        if my: y = int(my.group(1)); acc = {"m": [0.0] * 18, "f": [0.0] * 18}; continue
        if y is None or y <= 2020 or y > 2070: continue
        lab = h.strip().replace(" ", "")
        if lab.startswith("総"): acc["total"] = r[1]; continue
        mm = re.match(r"^(\d+)～(\d+)$", lab); mo = re.match(r"^(\d+)\+$", lab)
        if mm and int(mm.group(2)) - int(mm.group(1)) == 4: a = int(mm.group(1))
        elif mo and int(mo.group(1)) >= 95: a = int(mo.group(1))
        else: continue
        i = min(a // 5, 17); acc["m"][i] += r[2]; acc["f"][i] += r[3]
        if lab == "100+":
            out[y] = {"src": "ipss", "total": round(acc["total"], 1), "m": [round(v, 1) for v in acc["m"]], "f": [round(v, 1) for v in acc["f"]]}
for y in sorted(out):
    o = out[y]; s = sum(o["m"]) + sum(o["f"])
    print(y, o["src"], o["total"], round(s, 1), "65+%", round((sum(o["m"][13:]) + sum(o["f"][13:])) / s * 100, 1), "0-14%", round((sum(o["m"][:3]) + sum(o["f"][:3])) / s * 100, 1))
json.dump({"ages": AG, "years": {str(y): out[y] for y in sorted(out)}}, open(os.path.join(D, "jinko_pyramid.json"), "w", encoding="utf-8"), ensure_ascii=False)
