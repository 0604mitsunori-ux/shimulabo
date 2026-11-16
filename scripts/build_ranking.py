"""シミュラボ 人気ランキング＆シミュレーション回数カウンターのデータを作る。

GA4（プロパティ 542391428・shimulabo.com のみ）の閲覧数から
  assets/ranking.json    … トップページ用（累計・今週・きのう・ランキング4種）
  assets/sim-counts.json … 各シミュページ用（id → 累計回数・今週の順位）
を書き出す。数える対象は /sims/<id>/ と /en/sims/<id>/ の閲覧（＝シミュが開かれた回数）。

使い方:  python scripts/build_ranking.py
毎朝1回まわして git push すれば、サイトのランキングとカウンターが更新される。
"""
import os, re, sys, json, datetime as dt
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent
SA = os.environ.get("GA4_SA_JSON", r"C:\Users\社員\.config\gcloud_sa\ga4-sa.json")
os.environ.setdefault("GOOGLE_APPLICATION_CREDENTIALS", SA)
PROPERTY = "properties/542391428"
HOST = "shimulabo.com"
SINCE = "2026-06-01"          # 公開（6/20）より前から＝全期間

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (RunReportRequest, DateRange, Dimension, Metric,
                                                FilterExpression, Filter)

ga = BetaAnalyticsDataClient()
SIM_RE = re.compile(r"^/(?:en/)?sims/([a-z0-9][a-z0-9-]*)/")


def views(start, end, by_date=False):
    """{sim_id: 閲覧数}（by_date=True なら {日付: 閲覧数}）"""
    dims = [Dimension(name="pagePath")] + ([Dimension(name="date")] if by_date else [])
    r = ga.run_report(RunReportRequest(
        property=PROPERTY, date_ranges=[DateRange(start_date=start, end_date=end)],
        dimensions=dims, metrics=[Metric(name="screenPageViews")], limit=250000,
        dimension_filter=FilterExpression(filter=Filter(
            field_name="hostName", string_filter=Filter.StringFilter(value=HOST)))))
    out = {}
    for row in r.rows:
        m = SIM_RE.match(row.dimension_values[0].value)
        if not m:
            continue
        key = row.dimension_values[1].value if by_date else m.group(1)
        out[key] = out.get(key, 0) + int(row.metric_values[0].value)
    return out


# ---- シミュのタイトル・絵文字・カテゴリ（トップのギャラリーカードから） ----
html = (ROOT / "index.html").read_text(encoding="utf-8")
META = {}
for m in re.finditer(r'<a class="sim-card"[^>]*href="sims/([^/"]+)/[^"]*">(.*?)</a>', html, re.S):
    sid, body = m.group(1), m.group(2)
    if sid in META:
        continue
    t = re.search(r"<h3>(.*?)</h3>", body, re.S)
    e = re.search(r'class="emoji">(.*?)</span>', body, re.S)
    c = re.search(r'class="cat">(.*?)</div>', body, re.S)
    if t:
        META[sid] = {"title": re.sub(r"<[^>]+>", "", t.group(1)).strip(),
                     "emoji": e.group(1).strip() if e else "🧪",
                     "cat": c.group(1).strip() if c else ""}
print(f"シミュ {len(META)} 本のタイトルを取得")

# ---- 期間（JST） ----
today = dt.date.today()
d = lambda n: (today - dt.timedelta(days=n)).isoformat()

all_time = views(SINCE, "today")
week = views(d(7), d(1))            # 直近7日（きのうまで）
prev_week = views(d(14), d(8))      # その前の7日
month = views(d(30), d(1))          # 直近30日
daily = views(d(1), "today", by_date=True)
yesterday = daily.get(d(1).replace("-", ""), 0)
today_so_far = daily.get(today.isoformat().replace("-", ""), 0)


def ranked(counts, n=10):
    items = [(k, v) for k, v in counts.items() if k in META and v > 0]
    items.sort(key=lambda kv: (-kv[1], kv[0]))
    return items[:n]


prev_rank = {k: i + 1 for i, (k, _) in enumerate(ranked(prev_week, 10**6))}


def row(sid, v, **extra):
    r = {"id": sid, "views": v, **META[sid], **extra}
    return r


week_rows = []
for i, (sid, v) in enumerate(ranked(week)):
    pr = prev_rank.get(sid)
    week_rows.append(row(sid, v, prev=pr))          # prev=None → NEW

# 急上昇：今週10回以上・先週の2倍以上に伸びたものを「増えた回数」の多い順
rising = []
for sid, v in week.items():
    p = prev_week.get(sid, 0)
    if sid in META and v >= 10 and v >= 2 * p:
        rising.append((v - p, v, sid, p))
rising.sort(key=lambda x: (-x[0], -x[1], x[2]))
rising_rows = [row(sid, v, prevViews=p, up=inc) for inc, v, sid, p in rising[:10]]

total = sum(all_time.values())
out = {
    "updated": dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S+09:00"),
    "source": "Googleアナリティクス（シミュのページが開かれた回数）",
    "total": total,
    "week": sum(week.values()),
    "prevWeek": sum(prev_week.values()),
    "yesterday": yesterday,
    "today": today_so_far,
    "simsPlayed": sum(1 for k, v in all_time.items() if k in META and v > 0),
    "rankings": {
        "week": week_rows,
        "month": [row(s, v) for s, v in ranked(month)],
        "rising": rising_rows,
        "all": [row(s, v) for s, v in ranked(all_time)],
    },
}
(ROOT / "assets" / "ranking.json").write_text(
    json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

week_rank = {k: i + 1 for i, (k, _) in enumerate(ranked(week, 10**6))}
counts = {"updated": out["updated"],
          "c": {k: [v, week_rank.get(k, 0)] for k, v in sorted(all_time.items()) if k in META}}
(ROOT / "assets" / "sim-counts.json").write_text(
    json.dumps(counts, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")

print(f"累計 {total:,} 回／今週 {out['week']:,}（先週 {out['prevWeek']:,}）／きのう {yesterday:,}")
for i, r in enumerate(week_rows[:5], 1):
    print(f"  今週{i}位 {r['views']:>4}回  {r['title']}  (先週 {r['prev'] or 'NEW'})")
