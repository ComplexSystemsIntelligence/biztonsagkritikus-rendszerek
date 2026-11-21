#!/usr/bin/env python3
"""A böngészős alkalmazások összeállítása: a src/ mappa sablonjaiba beilleszti a közös CSS-t és JS-t,
így minden alkalmazás egyetlen, önálló HTML-fájl lesz (internetkapcsolat nélkül is fut)."""
from pathlib import Path
src = Path(__file__).parent / "src"
css = (src / "_kozos.css").read_text(encoding="utf-8")
js = (src / "_kozos.js").read_text(encoding="utf-8")
for f in sorted(src.glob("*.html")):
    t = f.read_text(encoding="utf-8").replace("/*KOZOS_CSS*/", css).replace("/*KOZOS_JS*/", js)
    (src.parent / f.name).write_text(t, encoding="utf-8")
    print("alkalmazás:", f.name)
