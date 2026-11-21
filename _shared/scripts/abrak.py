#!/usr/bin/env python3
"""Ábrák fordítása a sorozat könyveihez.

Használat:  python3 _shared/scripts/abrak.py <könyvmappa> [--mind]

Minden `<könyv>/abrak/tikz/*.tex` fájlt xelatex-hel (PE_TEX_ENGINE=lualatex is lehet) PDF-be fordít, majd
pdftocairo-val (ennek hiányában PyMuPDF-fel) SVG-t készít belőle. Az
`<könyv>/abrak/py/*.py` szkriptek (matplotlib) közvetlenül írnak SVG-t és
PDF-et. Az eredmény az `<könyv>/abrak/gen/` mappába kerül. Csak az elavult
ábrák fordulnak újra (vagy mind, ha `--mind`).
"""
import os
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

gyoker = Path(__file__).resolve().parents[2]
konyv = gyoker / sys.argv[1]
mind = "--mind" in sys.argv
tikz_dir = konyv / "abrak" / "tikz"
py_dir = konyv / "abrak" / "py"
gen = konyv / "abrak" / "gen"
gen.mkdir(parents=True, exist_ok=True)
sty = gyoker / "_shared" / "tikz" / "peabra.sty"
MOTOR = os.environ.get("PE_TEX_ENGINE", "xelatex")  # xelatex vagy lualatex
env = dict(os.environ)
# saját stílus elöl, a rendszer könyvtárai középen, a pótlékok (compat) a végén
env["TEXINPUTS"] = f".:{gyoker/'_shared'/'tikz'}:{tikz_dir}//::{gyoker/'_shared'/'tikz'/'compat'}"
env["OSFONTDIR"] = str(gyoker / "_shared" / "fonts" / "ttf") + ":" + env.get("OSFONTDIR", "")


def svg_from_pdf(pdf: Path, svg: Path):
    if shutil.which("pdftocairo"):
        subprocess.run(["pdftocairo", "-svg", str(pdf), str(svg)], check=True)
    else:
        import pymupdf
        d = pymupdf.open(str(pdf))
        svg.write_text(d[0].get_svg_image(text_as_path=True), encoding="utf-8")


def elavult(forras: Path, cel: Path, extra=()):
    if mind or not cel.exists():
        return True
    t = cel.stat().st_mtime
    return any(p.stat().st_mtime > t for p in (forras, *extra) if p.exists())


def tikz(tex: Path):
    pdf = gen / (tex.stem + ".pdf")
    svg = gen / (tex.stem + ".svg")
    if not elavult(tex, svg, (sty, *sorted(tikz_dir.glob("_*")))):
        return None
    with tempfile.TemporaryDirectory() as tmp:
        r = subprocess.run([MOTOR, "-interaction=nonstopmode", "-halt-on-error",
                            f"-output-directory={tmp}", str(tex)],
                           cwd=tex.parent, env=env, capture_output=True, text=True)
        out = Path(tmp) / (tex.stem + ".pdf")
        if r.returncode != 0 or not out.exists():
            log = (Path(tmp) / (tex.stem + ".log"))
            hiba = [l for l in (log.read_text(errors="ignore").splitlines() if log.exists() else [])
                    if l.startswith("!")][:3]
            return f"HIBA {tex.name}: {' | '.join(hiba) or r.stdout[-400:]}"
        shutil.copy2(out, pdf)
    svg_from_pdf(pdf, svg)
    return f"ok   {tex.name}"


def python(py: Path):
    svg = gen / (py.stem + ".svg")
    if not elavult(py, svg):
        return None
    r = subprocess.run([sys.executable, str(py), str(gen)], capture_output=True, text=True)
    return f"ok   {py.name}" if r.returncode == 0 else f"HIBA {py.name}: {r.stderr[-600:]}"


feladat = []
if tikz_dir.exists():
    feladat += [(tikz, t) for t in sorted(tikz_dir.glob("*.tex")) if not t.name.startswith("_")]
if py_dir.exists():
    feladat += [(python, p) for p in sorted(py_dir.glob("*.py")) if not p.name.startswith("_")]
with ThreadPoolExecutor(max_workers=os.cpu_count() or 2) as ex:
    eredmeny = list(ex.map(lambda fa: fa[0](fa[1]), feladat))
hibak = [e for e in eredmeny if e and e.startswith("HIBA")]
for e in eredmeny:
    if e:
        print("abrak:", e)
print(f"abrak: {konyv.name}: {len([e for e in eredmeny if e])} ábra frissítve, {len(hibak)} hiba")
sys.exit(1 if hibak else 0)
