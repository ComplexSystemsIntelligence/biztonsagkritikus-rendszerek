# Colab-notebookok

A gyakorlati útmutató hét Python-notebookja. A „Colab” hivatkozás a Google Colabban nyitja meg a jegyzetfüzetet, ahol telepítés nélkül futtatható; a kód csak a Colab alapcsomagjait (NumPy, SciPy, pandas, Matplotlib) használja. A notebookok lefuttatott kimenettel szerepelnek a tárolóban, így futtatás nélkül is olvashatók.

| Notebook | Megnyitás | Gyakorlat |
|:--|:--|:--|
| [Egyéni és társadalmi kockázat (IRPA, F–N görbe)](02_kockazat_irpa_fn.ipynb) | [Colab](https://colab.research.google.com/github/ComplexSystemsIntelligence/biztonsagkritikus-rendszerek/blob/main/gyakorlat/notebookok/02_kockazat_irpa_fn.ipynb) | [2.](https://complexsystemsintelligence.github.io/biztonsagkritikus-rendszerek/gyakorlat/laborok/02-kockazati-matrix.html) |
| [FMEDA: diagnosztikai lefedettség és biztonságos meghibásodási hányad](04_fmeda.ipynb) | [Colab](https://colab.research.google.com/github/ComplexSystemsIntelligence/biztonsagkritikus-rendszerek/blob/main/gyakorlat/notebookok/04_fmeda.ipynb) | [4.](https://complexsystemsintelligence.github.io/biztonsagkritikus-rendszerek/gyakorlat/laborok/04-fmea.html) |
| [Meghibásodási ráta becslése és Weibull-elemzés cenzúrázott adatokra](06_megbizhatosag_weibull.ipynb) | [Colab](https://colab.research.google.com/github/ComplexSystemsIntelligence/biztonsagkritikus-rendszerek/blob/main/gyakorlat/notebookok/06_megbizhatosag_weibull.ipynb) | [6.](https://complexsystemsintelligence.github.io/biztonsagkritikus-rendszerek/gyakorlat/laborok/06-megbizhatosag.html) |
| [Blokkdiagramok: hídkapcsolás, Monte Carlo, közös okú meghibásodás](07_rbd_hid_mc.ipynb) | [Colab](https://colab.research.google.com/github/ComplexSystemsIntelligence/biztonsagkritikus-rendszerek/blob/main/gyakorlat/notebookok/07_rbd_hid_mc.ipynb) | [7.](https://complexsystemsintelligence.github.io/biztonsagkritikus-rendszerek/gyakorlat/laborok/07-rbd.html) |
| [Hibafa: MOCUS, bináris döntési diagram, fontosság és bizonytalanság](08_hibafa.ipynb) | [Colab](https://colab.research.google.com/github/ComplexSystemsIntelligence/biztonsagkritikus-rendszerek/blob/main/gyakorlat/notebookok/08_hibafa.ipynb) | [8.](https://complexsystemsintelligence.github.io/biztonsagkritikus-rendszerek/gyakorlat/laborok/08-hibafa.html) |
| [Markov-modellek: javítható rendszerek, hideg tartalék, többfázisú PFD](10_markov.ipynb) | [Colab](https://colab.research.google.com/github/ComplexSystemsIntelligence/biztonsagkritikus-rendszerek/blob/main/gyakorlat/notebookok/10_markov.ipynb) | [10.](https://complexsystemsintelligence.github.io/biztonsagkritikus-rendszerek/gyakorlat/laborok/10-markov.html) |
| [PFD és SIL-igazolás: képletek, érzékenység, Monte Carlo](11_sil.ipynb) | [Colab](https://colab.research.google.com/github/ComplexSystemsIntelligence/biztonsagkritikus-rendszerek/blob/main/gyakorlat/notebookok/11_sil.ipynb) | [11.](https://complexsystemsintelligence.github.io/biztonsagkritikus-rendszerek/gyakorlat/laborok/11-sil.html) |

## Újragenerálás

A notebookokat a [`_keszit.py`](_keszit.py) állítja elő és futtatja le (`pip install -r requirements.txt`, majd `python gyakorlat/notebookok/_keszit.py` a tároló gyökeréből). A számok a kézikönyv eseteivel és a `_shared/esetek/` szkriptjeivel egyeznek.
