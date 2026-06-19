# -*- coding: utf-8 -*-
"""プレースホルダのドメインを実ドメインへ一括置換。
   使い方: python scripts/set_domain.py shimulabo.com
"""
import os, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD = "shimulabo.com"
NEW = sys.argv[1] if len(sys.argv) > 1 else "shimulabo.com"

EXTS = (".html", ".xml", ".txt", ".js", ".py")
changed = 0
for path in glob.glob(os.path.join(ROOT, "**", "*"), recursive=True):
    if not path.lower().endswith(EXTS):
        continue
    try:
        with open(path, "r", encoding="utf-8") as f:
            s = f.read()
    except (UnicodeDecodeError, IsADirectoryError):
        continue
    if OLD in s:
        with open(path, "w", encoding="utf-8") as f:
            f.write(s.replace(OLD, NEW))
        changed += 1
        print("updated:", os.path.relpath(path, ROOT))

print(f"done. {changed} files. {OLD} -> {NEW}")
