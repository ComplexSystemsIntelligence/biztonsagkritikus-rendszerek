#!/usr/bin/env python3
"""A böngészős alkalmazások összeállítása: a src/ mappa sablonjaiba beilleszti a közös CSS-t és JS-t,
valamint a fejlécbe a Pannon Egyetem logóját, így minden alkalmazás egyetlen, önálló HTML-fájl lesz
(internetkapcsolat nélkül is fut)."""
from pathlib import Path
src = Path(__file__).parent / "src"
css = (src / "_kozos.css").read_text(encoding="utf-8")
js = (src / "_kozos.js").read_text(encoding="utf-8")
import base64
logo_svg = src.parents[2] / "_shared" / "logo" / "pe-cimer-nevjel-fekvo-feher.svg"
logo = ""
if logo_svg.exists():
    b64 = base64.b64encode(logo_svg.read_bytes()).decode("ascii")
    logo = (f'<a class="pe-logo" href="https://uni-pannon.hu/" target="_blank" rel="noopener" title="Pannon Egyetem">'
            f'<img src="data:image/svg+xml;base64,{b64}" alt="Pannon Egyetem"></a><div class="szoveg">')
for f in sorted(src.glob("*.html")):
    t = f.read_text(encoding="utf-8").replace("/*KOZOS_CSS*/", css).replace("/*KOZOS_JS*/", js)
    if logo and '<header class="app">' in t:
        # a Pannon Egyetem logója a fejléc elején, a cím és a leírás mellett
        t = t.replace('<header class="app">', '<header class="app">' + logo, 1)
        t = t.replace("</header>", "</div></header>", 1)
    (src.parent / f.name).write_text(t, encoding="utf-8")
    print("alkalmazás:", f.name)
