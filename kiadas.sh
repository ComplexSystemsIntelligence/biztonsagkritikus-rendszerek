#!/usr/bin/env bash
# Kiadás előkészítése: a teljes webhely fordítása, majd a PDF- és EPUB-fájlok bemásolása a kiadas/ mappába,
# hogy a GitHub-kiadás forráscsomagjával a Zenodo az olvasható könyvet is archiválja.
# Előtte frissítendő: a CITATION.cff (version, date-released) és a _shared/latex/preamble.tex \peverzio sora.
set -euo pipefail
cd "$(dirname "$0")"
./build.sh
mkdir -p kiadas
cp _site/kezikonyv/biztonsagkritikus-rendszerek.pdf kiadas/biztonsagkritikus-rendszerek-kezikonyv.pdf
cp _site/kezikonyv/biztonsagkritikus-rendszerek.epub kiadas/biztonsagkritikus-rendszerek-kezikonyv.epub
cp _site/gyakorlat/biztonsagkritikus-rendszerek-gyakorlat.pdf kiadas/biztonsagkritikus-rendszerek-gyakorlat.pdf
ls -la kiadas
