#!/usr/bin/env python3
"""Renderelés előtti előkészítés (Quarto pre-render).

- a közös webes betűket a könyv `assets/fonts`, a logókat az `assets/logo` mappájába másolja;
- lefordítja az elavult ábrákat (TikZ -> PDF + SVG, Python -> SVG + PDF), ha van LaTeX.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

konyv = Path(os.environ.get("QUARTO_PROJECT_DIR", Path.cwd())).resolve()
gyoker = konyv.parent
cel = konyv / "assets" / "fonts"
cel.mkdir(parents=True, exist_ok=True)
for f in (gyoker / "_shared" / "fonts" / "web").glob("*.woff2"):
    t = cel / f.name
    if not t.exists() or t.stat().st_mtime < f.stat().st_mtime:
        shutil.copy2(f, t)

# a Pannon Egyetem logói (webes kimenet: oldalsáv, favicon)
logo_cel = konyv / "assets" / "logo"
logo_cel.mkdir(parents=True, exist_ok=True)
for f in (gyoker / "_shared" / "logo").iterdir():
    if f.suffix in (".svg", ".png"):
        t = logo_cel / f.name
        if not t.exists() or t.stat().st_mtime < f.stat().st_mtime:
            shutil.copy2(f, t)

# a böngészős alkalmazások összeállítása (ha a könyvnek vannak ilyenek)
epit = konyv / "alkalmazasok" / "epit.py"
if epit.exists():
    subprocess.run([sys.executable, str(epit)], check=True)

if shutil.which("xelatex") or shutil.which("lualatex"):
    subprocess.run([sys.executable, str(gyoker / "_shared" / "scripts" / "abrak.py"), konyv.name],
                   check=True)
else:
    print("prepare: nincs LaTeX, a meglévő ábrákat használom")
