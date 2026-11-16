"""style.css の人気ランキング部分を GA4 実データ版のUIに差し替え（2026-11-16）"""
from pathlib import Path

p = Path(__file__).resolve().parent.parent / "assets" / "style.css"
s = p.read_text(encoding="utf-8")
a = s.index(".rank-bar { flex: 0 0 76px; }")
b = s.index("@media (max-width: 520px){ .rank-bar { display: none; } }")
b = b + len("@media (max-width: 520px){ .rank-bar { display: none; } }")
new = '''.rank-main .t, .rank-main .c { display: block; }
/* 棒は題名の下に細く（スマホでも見える） */
.rank-bar { display: block; height: 3px; margin-top: 6px; background: var(--line-2); max-width: 260px; }
.rank-bar .fill { display: block; height: 100%; background: var(--teal); }
.rank-row.top1 .rank-bar .fill { background: var(--accent); }
.rank-stat { flex: 0 0 auto; display: flex; align-items: center; gap: 8px; text-align: right; }
.rank-num { font-size: 12px; color: var(--ink-3); white-space: nowrap; font-variant-numeric: tabular-nums; }
.rank-num b { font-size: 16px; color: var(--ink); font-weight: 700; margin-right: 1px; }
.rank-mv { min-width: 36px; font-size: 11.5px; font-weight: 700; white-space: nowrap; font-variant-numeric: tabular-nums; text-align: center; }
.rank-mv.up { color: var(--accent); }
.rank-mv.down { color: var(--ink-3); }
.rank-mv.same { color: var(--ink-3); }
.rank-mv.new { color: #fff; background: var(--accent); padding: 2px 6px; border-radius: 3px; min-width: 0; font-size: 10.5px; letter-spacing: .04em; }
.rank-arrow { flex: 0 0 auto; color: var(--ink-2); font-weight: 900; }

/* シミュレーション回数カウンター（実験ノートの「計数器」） */
.play-counter {
  display: flex; align-items: flex-end; justify-content: space-between; gap: 10px 24px; flex-wrap: wrap;
  margin: 14px 0 6px; padding: 16px 18px; background: var(--card); border: 1px solid var(--line); border-left: 3px solid var(--accent);
}
.pc-main { display: flex; align-items: baseline; gap: 8px; flex-wrap: wrap; }
.pc-label, .pc-unit { font-size: 13px; color: var(--ink-2); font-weight: 600; }
.pc-num { font-family: var(--serif); font-size: clamp(30px, 6vw, 42px); line-height: 1; color: var(--accent); font-weight: 700; font-variant-numeric: tabular-nums; letter-spacing: .01em; }
.pc-sub { display: flex; gap: 14px; flex-wrap: wrap; font-size: 12.5px; color: var(--ink-3); }
.pc-sub b { color: var(--ink); font-variant-numeric: tabular-nums; }
.pc-trend.up { color: var(--accent); font-weight: 700; }
.pc-trend.down { color: var(--ink-3); }

/* 期間タブ */
.rank-tabs { display: flex; gap: 0; margin: 12px 0 2px; border-bottom: 1px solid var(--line); overflow-x: auto; }
.rank-tabs button {
  appearance: none; background: none; border: 0; border-bottom: 2px solid transparent; margin-bottom: -1px;
  padding: 9px 14px; font: inherit; font-size: 13.5px; font-weight: 600; color: var(--ink-3); cursor: pointer; white-space: nowrap;
}
.rank-tabs button:hover { color: var(--ink); }
.rank-tabs button[aria-selected="true"] { color: var(--ink); border-bottom-color: var(--accent); }
.rank-tabs button:focus-visible { outline: 2px solid var(--teal); outline-offset: -2px; }
.rank-more {
  display: block; width: 100%; margin-top: 8px; padding: 10px; background: none; border: 1px dashed var(--line);
  font: inherit; font-size: 13px; font-weight: 600; color: var(--teal-d); cursor: pointer;
}
.rank-more:hover { background: var(--teal-l); }
.rank-src { margin: 8px 0 0; font-size: 11px; color: var(--ink-3); }
.rank-empty { padding: 18px 6px; color: var(--ink-3); font-size: 13px; }
@media (max-width: 520px){
  .rank-row { gap: 10px; padding: 12px 2px; }
  .rank-arrow { display: none; }
  .rank-mv { min-width: 30px; }
  .play-counter { padding: 14px; }
}

/* 各シミュページの回数表示 */
.play-pill { display: inline-flex; align-items: center; gap: 6px; margin: 4px 0 2px; padding: 4px 10px; font-size: 12.5px; color: var(--ink-2); background: var(--card); border: 1px solid var(--line); border-radius: 999px; }
.play-pill b { color: var(--accent); font-variant-numeric: tabular-nums; }
.play-pill .rk { color: var(--teal-d); font-weight: 700; }'''
s = s[:a] + new + s[b:]
p.write_text(s, encoding="utf-8")
print("ok")
