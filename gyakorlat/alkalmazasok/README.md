# Böngészős alkalmazások

A gyakorlati útmutató kilenc interaktív alkalmazása. Mindegyik egyetlen, önálló HTML-fájl: telepítés és internetkapcsolat nélkül fut, a munkát a böngésző helyi tárolójában megőrzi, az eredmények CSV- vagy Markdown-fájlként letölthetők.

| Alkalmazás | Mire való | Gyakorlat |
|:--|:--|:--|
| [Kockázati mátrix tervező](https://complexsystemsintelligence.github.io/biztonsagkritikus-rendszerek/gyakorlat/alkalmazasok/kockazati-matrix.html) | kategóriák, kritériumok, forgatókönyvek; a mátrix rangsorhibáinak (Cox) kimutatása | [2.](https://complexsystemsintelligence.github.io/biztonsagkritikus-rendszerek/gyakorlat/laborok/02-kockazati-matrix.html) |
| [FMEA-munkalap](https://complexsystemsintelligence.github.io/biztonsagkritikus-rendszerek/gyakorlat/alkalmazasok/fmea.html) | RPN és cselekvési prioritás párhuzamosan, az ellentmondó sorok jelölése | [4.](https://complexsystemsintelligence.github.io/biztonsagkritikus-rendszerek/gyakorlat/laborok/04-fmea.html) |
| [STPA-munkalap](https://complexsystemsintelligence.github.io/biztonsagkritikus-rendszerek/gyakorlat/alkalmazasok/stpa.html) | veszteségek, veszélyek, irányítási struktúra, UCA-táblázat, forgatókönyvek, követelmények; Markdown-export | [5.](https://complexsystemsintelligence.github.io/biztonsagkritikus-rendszerek/gyakorlat/laborok/05-stpa.html) |
| [Élettartam-eloszlások](https://complexsystemsintelligence.github.io/biztonsagkritikus-rendszerek/gyakorlat/alkalmazasok/eloszlasok.html) | exponenciális, Weibull- és lognormális eloszlás, kádgörbe | [6.](https://complexsystemsintelligence.github.io/biztonsagkritikus-rendszerek/gyakorlat/laborok/06-megbizhatosag.html) |
| [Megbízhatósági blokkdiagram](https://complexsystemsintelligence.github.io/biztonsagkritikus-rendszerek/gyakorlat/alkalmazasok/rbd.html) | soros, párhuzamos, k-ból-n és hídkapcsolás; R(t), MTTF, fontosság | [7.](https://complexsystemsintelligence.github.io/biztonsagkritikus-rendszerek/gyakorlat/laborok/07-rbd.html) |
| [Hibafa-elemző](https://complexsystemsintelligence.github.io/biztonsagkritikus-rendszerek/gyakorlat/alkalmazasok/hibafa.html) | szöveges hibafa, minimális vágatok, csúcsesemény-valószínűség, fontossági mértékek, házesemények | [8.](https://complexsystemsintelligence.github.io/biztonsagkritikus-rendszerek/gyakorlat/laborok/08-hibafa.html) |
| [LOPA és eseményfa](https://complexsystemsintelligence.github.io/biztonsagkritikus-rendszerek/gyakorlat/alkalmazasok/lopa.html) | kezdő esemény, feltételek, független védelmi rétegek, szükséges SIL | [9.](https://complexsystemsintelligence.github.io/biztonsagkritikus-rendszerek/gyakorlat/laborok/09-lopa.html) |
| [Markov-modell szerkesztő](https://complexsystemsintelligence.github.io/biztonsagkritikus-rendszerek/gyakorlat/alkalmazasok/markov.html) | állapotok és átmenetek, pillanatnyi és tartós rendelkezésre állás, MTTF | [10.](https://complexsystemsintelligence.github.io/biztonsagkritikus-rendszerek/gyakorlat/laborok/10-markov.html) |
| [PFD- és SIL-kalkulátor](https://complexsystemsintelligence.github.io/biztonsagkritikus-rendszerek/gyakorlat/alkalmazasok/sil.html) | IEC 61508-6 képletek, architekturális korlátok, részleges löketpróba, téves leállások, érzékenység | [11.](https://complexsystemsintelligence.github.io/biztonsagkritikus-rendszerek/gyakorlat/laborok/11-sil.html) |

## Szerkesztés

A forrás a [`src/`](src/) mappában van; a közös stílus a `src/_kozos.css`, a közös segédfüggvények (számformázás, diagramok, mentés) a `src/_kozos.js` fájlban. Az `epit.py` ezeket minden alkalmazásba beilleszti, és a kész fájlokat ebbe a mappába írja; a könyv fordításakor ez automatikusan lefut.
