"""楽天アフィリエイトの枠を、結果と文脈が合うページだけに1枠入れる（2026-10-18）。何度実行しても同じ結果。
  - アフィリエイトID は scripts/rakuten_affiliate_id.txt の1行目（楽天アフィリエイトの「リンク作成」で出るリンクの hgc/ の後ろ）。
    空のときは枠を入れない（入っていれば外す）。
  - リンク先は楽天市場の検索結果（商品の売り切れでリンク切れにならないように）。
  - 理科の授業向け（/rika/ のパンくずのページ）には入れない。
使い方: python scripts/rakuten_slots.py
"""
import io, os, re, sys
from urllib.parse import quote

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
START, END = "<!-- rakuten-slot:start -->", "<!-- rakuten-slot:end -->"

# slug → (見出し, [(表示名, 検索語)])
SLOTS = {
    "kaibatsu-check": ("この場所で備えておきたいもの", [
        ("防災セット・防災リュック", "防災セット"), ("保存水・長期保存の非常食", "非常食 長期保存"),
        ("ポータブル電源", "ポータブル電源"), ("簡易トイレ", "簡易トイレ 防災"), ("ライフジャケット・救命胴衣", "ライフジャケット 大人")]),
    "jishin-live": ("揺れに備えて、今のうちに", [
        ("家具の転倒防止グッズ", "家具 転倒防止"), ("防災セット・防災リュック", "防災セット"),
        ("保存水・長期保存の非常食", "非常食 長期保存"), ("ポータブル電源", "ポータブル電源"), ("ヘッドライト・懐中電灯", "LEDヘッドライト 防災")]),
    "hoshizora-shisu": ("星空観察に持っていくと便利なもの", [
        ("双眼鏡（星空・天体向け）", "双眼鏡 星空"), ("初心者向けの天体望遠鏡", "天体望遠鏡 初心者"),
        ("星座早見盤", "星座早見盤"), ("赤色ライト（目が暗さに慣れたまま使える）", "赤色ライト 天体観測"), ("レジャーシート・アウトドアチェア", "アウトドアチェア 軽量")]),
    "shio-live": ("潮に合わせて海へ行くなら", [
        ("ライフジャケット・救命胴衣", "ライフジャケット 大人"), ("潮干狩りセット", "潮干狩り セット"),
        ("釣り竿セット（初心者向け）", "釣り竿 セット 初心者"), ("クーラーボックス", "クーラーボックス"), ("マリンシューズ", "マリンシューズ")]),
}


def aff_id():
    p = os.path.join(HERE, "rakuten_affiliate_id.txt")
    if not os.path.exists(p): return ""
    v = io.open(p, encoding="utf-8").read().strip().splitlines()[0].strip() if io.open(p, encoding="utf-8").read().strip() else ""
    assert v == "" or re.fullmatch(r"[0-9a-f]{8}(\.[0-9a-f]{8}){3}", v), f"アフィリエイトIDの形が違います: {v}"
    return v


def link(aid, word):
    pc = "https://search.rakuten.co.jp/search/mall/" + quote(word) + "/"
    return f"https://hb.afl.rakuten.co.jp/hgc/{aid}/?pc={quote(pc, safe='')}&m={quote(pc, safe='')}"


def slot(aid, title, items):
    lis = "".join(f'<li><a href="{link(aid, w)}" target="_blank" rel="sponsored nofollow noopener">{n}</a></li>' for n, w in items)
    return f'''{START}
  <aside class="rakuten-slot" aria-label="広告" style="margin:22px 0;padding:14px 18px;border:1px dashed var(--line,#d9d3c7);border-radius:12px;">
    <p style="margin:0 0 6px;font-size:13.5px;font-weight:700;">🛒 {title}（楽天市場で探す）</p>
    <ul style="margin:0;padding-left:1.2em;line-height:1.9;font-size:14px;">{lis}</ul>
    <p style="margin:6px 0 0;font-size:11.5px;opacity:.65;">※広告（楽天アフィリエイト）。リンク先は楽天市場の検索結果です。</p>
  </aside>
{END}
'''


def main():
    aid = aff_id()
    for slug, (title, items) in SLOTS.items():
        p = os.path.join(ROOT, "sims", slug, "index.html")
        h = io.open(p, encoding="utf-8").read(); h0 = h
        assert 'href="../../rika/"' not in h, f"{slug} は理科の授業向けページなので入れない"
        h = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n", "", h, flags=re.S)
        if aid:
            anchor = '  <article class="article">'
            assert h.count(anchor) == 1, slug
            h = h.replace(anchor, slot(aid, title, items) + anchor)
        if h != h0:
            io.open(p, "w", encoding="utf-8", newline="").write(h)
    print(f"楽天の枠: {'入れた' if aid else 'IDが未設定なので入れていない'}（{len(SLOTS)}ページ）")


if __name__ == "__main__":
    main()
