#!/usr/bin/env bash
# A teljes webhely összeállítása: kézikönyv (HTML, PDF, EPUB) + gyakorlati útmutató (HTML, PDF)
# + nyitóoldal. Az eredmény a _site/ mappába kerül, amelyet a GitHub Pages szolgál ki.
#
# Használat:  ./build.sh            minden formátum
#             ./build.sh html       csak a webes változat (gyors előnézet)
#
# Előfeltételek: Quarto 1.11+, XeLaTeX (TeX Live), poppler-utils (pdftocairo),
# Python 3.10+, valamint a _shared/fonts/ttf betűk telepítve (lásd README).
set -euo pipefail
cd "$(dirname "$0")"

formatumok="${1:-all}"
rm -rf _site
mkdir -p _site

for konyv in kezikonyv gyakorlat; do
  echo "== ${konyv}"
  if [[ "$formatumok" == "html" ]]; then
    (cd "$konyv" && quarto render --to html)
  else
    (cd "$konyv" && quarto render)
  fi
done

cp landing/index.html _site/index.html
touch _site/.nojekyll

# ellenőrzés: feloldatlan kereszthivatkozások
if grep -rl 'class="quarto-unresolved-ref"' _site --include=*.html >/dev/null 2>&1; then
  echo "FIGYELEM: feloldatlan kereszthivatkozás:" >&2
  grep -rl 'class="quarto-unresolved-ref"' _site --include=*.html >&2
  exit 1
fi
echo "Kész: _site/"
