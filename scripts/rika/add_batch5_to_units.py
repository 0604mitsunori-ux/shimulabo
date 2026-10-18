# -*- coding: utf-8 -*-
"""第5弾（小3・小4）10本（2026-10-18）を units.json（/rika/ の単元表）に入れる（冪等）。各グループの先頭に置く。
   使い方: python scripts/rika/add_batch5_to_units.py  → その後 python scripts/rika/build.py"""
import io, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "units.json")
U = json.load(io.open(P, encoding="utf-8"))

# (セクションid, グループ名, id, 単元ラベル, 授業での使いどころ)
NEW = [
    ("sho", "3年", "mono-omosa", "小3 物と重さ", "ねん土の形を変えても重さは変わらないこと、同じ大きさでも物によって重さがちがうことを、はかりとてんびんで確かめる。"),
    ("sho", "3年", "kaze-gomu", "小3 風とゴムの力の働き", "風の強さやゴムをのばす長さを変えて車を走らせ、進んだきょりを表とグラフにして比べる。"),
    ("sho", "3年", "hikari-oto", "小3 光と音の性質", "かがみではね返した日光を重ねると明るく暖かくなる、虫めがねで光を集める、音が出るとき物はふるえている、を確かめる。"),
    ("sho", "3年", "denki-toorimichi", "小3 電気の通り道", "かん電池・豆電球・どう線を「わ」につなぐと明かりがつく。身の回りの物が電気を通すか調べて仲間分けする（金属は電気を通す）。"),
    ("sho", "3年", "konchu-sodachi", "小3 身の回りの生物（こん虫・植物の育ち方と体のつくり）", "モンシロチョウとバッタの育ち方（さなぎになる・ならない）を比べ、こん虫の体が頭・むね・はらに分かれ、あしが6本あることを確かめる。"),
    ("sho", "4年", "hone-kinniku", "小4 人の体のつくりと運動", "うでを曲げのばしすると、ちぢむ筋肉とゆるむ筋肉が入れかわり、関節で曲がることを確かめる。体の骨のはたらきも。"),
    ("sho", "4年", "kisetsu-seibutsu", "小4 季節と生物", "月を動かすと気温と動物・植物の様子が変わる。暖かい季節と寒い季節の活動や成長、冬ごしのちがいを1年分くらべる。"),
    ("sho", "4年", "amamizu-yukue", "小4 雨水の行方と地面の様子", "雨水が高い所から低い所へ流れて集まる様子と、土のつぶの大きさで水のしみこみ方がちがうことを確かめる。"),
    ("sho", "4年", "tenki-kion", "小4 天気の様子", "晴れ・くもり・雨の日の1日の気温の変わり方をグラフで比べ、気温の正しいはかり方を知る。水の蒸発と結露も。"),
    ("sho", "4年", "atatamarikata", "小4 金属，水，空気と温度（温まり方）", "金属は熱した所から順に、水と空気は動きながら全体が温まる様子を色と矢印で比べる。"),
]
added = 0
for sec_id, gtitle, sid, unit, use in reversed(NEW):
    sec = next(s for s in U["sections"] if s["id"] == sec_id)
    g = next(g for g in sec["groups"] if g["title"] == gtitle)
    if any(it["id"] == sid and it["unit"] == unit for it in g["items"]): continue
    g["items"].insert(0, {"id": sid, "unit": unit, "use": use}); added += 1
json.dump(U, io.open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"追加 {added}か所")
