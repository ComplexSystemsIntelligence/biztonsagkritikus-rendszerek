#!/usr/bin/env python3
"""Renderelés utáni magyar tipográfiai javítások (Quarto post-render).

A Quarto angol mintájú feliratsorrendjét ("ábra 2.1: ...") a magyar szokásra
("2.1. ábra. ...") cseréli, és a fejezet- és szakaszszámok után kiteszi a pontot.
HTML-fájlokon és az EPUB-csomagon belül is elvégzi a cserét.
"""
import os
import re
import shutil
import tempfile
import zipfile
from pathlib import Path

FELIRAT = re.compile(r"(ábra|táblázat|kódrészlet)(?:&nbsp;| |\s)(\d+(?:\.\d+)*)(?::|&nbsp;:)\s*")
FEJSZAM = re.compile(r'(<span class="chapter-number">)([0-9A-Z]+)(</span>)')
XREFCIM = re.compile(r'(class="quarto-xref"><span>)([0-9A-Z]+(?:\.[0-9]+)*)&nbsp;[^<]*(</span>)')
SZAKSZAM = re.compile(r'(<span class="header-section-number">)([0-9A-Z]+(?:\.[0-9]+)*)(</span>)')


def javit(s: str) -> str:
    s = FELIRAT.sub(lambda m: f'<span class="abraszam">{m.group(2)}. {m.group(1)}.</span> ', s)
    s = XREFCIM.sub(lambda m: m.group(1) + m.group(2) + m.group(3), s)
    s = FEJSZAM.sub(lambda m: m.group(1) + m.group(2) + "." + m.group(3), s)
    s = SZAKSZAM.sub(lambda m: m.group(1) + m.group(2) + "." + m.group(3), s)
    return s


def epub_javit(path: Path):
    tmp = Path(tempfile.mkdtemp())
    with zipfile.ZipFile(path) as z:
        z.extractall(tmp)
        nevek = z.namelist()
    for n in nevek:
        f = tmp / n
        if f.suffix in (".xhtml", ".html"):
            s = f.read_text(encoding="utf-8")
            j = javit(s)
            if j != s:
                f.write_text(j, encoding="utf-8")
    uj = path.with_suffix(".tmp")
    with zipfile.ZipFile(uj, "w") as z:
        z.write(tmp / "mimetype", "mimetype", compress_type=zipfile.ZIP_STORED)
        for n in nevek:
            if n != "mimetype" and (tmp / n).is_file():
                z.write(tmp / n, n, compress_type=zipfile.ZIP_DEFLATED)
    uj.replace(path)
    shutil.rmtree(tmp)


kimenet = os.environ.get("QUARTO_PROJECT_OUTPUT_DIR")
if kimenet:
    kimenet = Path(os.environ.get("QUARTO_PROJECT_DIR", ".")) / kimenet
    for f in kimenet.rglob("*.html"):
        s = f.read_text(encoding="utf-8")
        j = javit(s)
        if j != s:
            f.write_text(j, encoding="utf-8")
    for e in kimenet.rglob("*.epub"):
        epub_javit(e)
