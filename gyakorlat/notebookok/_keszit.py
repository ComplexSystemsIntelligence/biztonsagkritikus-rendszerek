#!/usr/bin/env python3
"""A gyakorlati útmutató Colab-notebookjainak előállítása és ellenőrző futtatása.
Futtatás: python3 _keszit.py  (nbformat, nbclient szükséges). A notebookok kimenettel együtt kerülnek a tárolóba."""
import nbformat as nbf
from nbclient import NotebookClient
from pathlib import Path
import sys

REPO = "ComplexSystemsIntelligence/biztonsagkritikus-rendszerek"
HERE = Path(__file__).parent

LOGO = ('<img src="https://complexsystemsintelligence.github.io/biztonsagkritikus-rendszerek/gyakorlat/assets/logo/pe-cimer-nevjel-fekvo-kek.png" '
        'alt="Pannon Egyetem – University of Pannonia" height="56">\n\n')

def colab(nev):
    return LOGO + (f"[Megnyitás a Google Colabban](https://colab.research.google.com/github/{REPO}/blob/main/gyakorlat/notebookok/{nev}) · "
            "*Biztonságkritikus rendszerek – gyakorlati útmutató* · © 2026 Abonyi János, Pannon Egyetem · kód: MIT, szöveg: CC BY-NC-SA 4.0")

STILUS = '''import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
PE = {"kek": "#285780", "sotet": "#1B3A57", "kiemel": "#E07B39", "zold": "#3E8E63", "piros": "#B83A3A", "lila": "#7A5C99", "szurke": "#6B7280"}
plt.rcParams.update({"figure.figsize": (7.5, 4.2), "axes.grid": True, "grid.color": "#e6e9ee", "axes.spines.top": False,
                     "axes.spines.right": False, "axes.prop_cycle": plt.cycler(color=list(PE.values())), "axes.formatter.use_locale": False})
def hu(x, sig=3):
    """Szám magyar formátumban (tizedesvessző, normálalak)."""
    if x == 0: return "0"
    e = int(np.floor(np.log10(abs(x))))
    if -2 <= e < 5: return f"{x:.{max(0, sig-1-e)}f}".replace(".", ",")
    return f"{x/10**e:.{sig-1}f}".replace(".", ",") + f"·10^{e}"
'''

NB = {}

NB["02_kockazat_irpa_fn.ipynb"] = [
("md", """# 2. gyakorlat – egyéni és társadalmi kockázat

Ez a notebook a könyv 3. fejezetének két kvantitatív eszközét számolja végig: az **egyéni kockázatot** (IRPA) egy kezelőre, és a **társadalmi kockázatot** egy kis létesítmény **F–N görbéjével**.

**Tanulási eredmények:** a notebook végére képes leszel IRPA-t számolni forgatókönyvekből, F–N görbét szerkeszteni és kritériumvonallal összevetni, valamint megállapítani, melyik forgatókönyv a kockázat domináns forrása."""),
("code", STILUS),
("md", """## 1. Egyéni kockázat

$\\text{IRPA} = \\sum_i F_i \\, P_{\\mathrm{h},i} \\, P_{\\mathrm{j},i}$, ahol $F_i$ a forgatókönyv gyakorisága, $P_{\\mathrm{h},i}$ a halálos kimenetel, $P_{\\mathrm{j},i}$ a jelenlét valószínűsége. Az adatok a könyv 3. fejezetének példájából valók (a reaktorfelhasadás gyakorisága a 11. fejezet eseményfájából)."""),
("code", '''forgatokonyvek = [  # név, F [1/év], P_halálos, P_jelenlét
    ("reaktor felhasadása megfutó reakció miatt", 6.8e-6, 0.9, 0.25),
    ("mérgező gőz kis szivárgása",                 1e-2,  1e-4, 0.25),
    ("tűz a betöltőnyílásnál",                     1e-4,  0.1, 0.25),
]
irpa = 0
for nev, F, Ph, Pj in forgatokonyvek:
    h = F * Ph * Pj; irpa += h
    print(f"{nev:45s} {hu(h)} /év")
print(f"{'összesen':45s} {hu(irpa)} /év")
for nev, F, Ph, Pj in forgatokonyvek:
    print(f"  {nev}: {100*F*Ph*Pj/irpa:.0f} %")'''),
("md", """**Értelmezés.** Az eredmény ($4{,}3\\cdot10^{-6}$/év) a brit HSE-kritériumok szerint a tolerálható tartomány alsó részébe esik, ezért ALARP-igazolás kell. A legnagyobb hozzájárulás a tűzé, nem a látványosabb reaktorfelhasadásé.

**1. feladat.** Mennyivel csökken az IRPA, ha zárt betöltéssel a tűz gyakoriságát tizedére csökkentjük? Melyik forgatókönyv lesz ezután a domináns?"""),
("code", '''# 1. feladat – írd ide a megoldást
'''),
("md", """## 2. F–N görbe

Az F–N görbe azt mutatja, mekkora gyakorisággal fordul elő $N$ vagy több áldozatot követelő baleset. A kritériumvonal $F = C/N^{a}$ alakú; itt a könyv ábrájának megfelelően $C = 10^{-3}$, $a = 2$ (kockázatkerülő), az elhanyagolható szint $10^{-5}/N^2$. A létesítmény forgatókönyvei (szemléltető adatok):"""),
("code", '''esemenyek = np.array([  # áldozatok száma, gyakoriság [1/év]
    [1, 1.4e-5], [3, 4.8e-6], [10, 1.0e-6], [40, 1.9e-7], [120, 1.0e-8]])
N = np.sort(np.unique(esemenyek[:, 0]))
F_N = np.array([esemenyek[esemenyek[:, 0] >= n, 1].sum() for n in N])
for n, f in zip(N, F_N):
    print(f"F(N ≥ {int(n):4d}) = {hu(f)} /év   kritérium: {hu(1e-3/n**2)}   {'megfelel' if f <= 1e-3/n**2 else 'NEM felel meg'}")
fig, ax = plt.subplots()
xs = np.logspace(0, 3, 50)
ax.loglog(xs, 1e-3/xs**2, color=PE["piros"], lw=2, label="kritérium: $10^{-3}/N^2$")
ax.loglog(xs, 1e-5/xs**2, color=PE["zold"], ls="--", label="elhanyagolható: $10^{-5}/N^2$")
ax.step(np.append(N, 1000), np.append(F_N, F_N[-1]), where="post", color=PE["kek"], lw=2, label="a létesítmény F–N görbéje")
ax.set_xlabel("áldozatok száma, N"); ax.set_ylabel("F(N vagy több áldozat) [1/év]"); ax.legend(); plt.show()'''),
("md", """**2. feladat.** Egy új forgatókönyv (például egy gáztartály felrobbanása) $5\\cdot10^{-8}$/év gyakorisággal 200 áldozatot követelhet. Add hozzá, és vizsgáld meg, átlépi-e a görbe a kritériumvonalat! Mit jelent a kockázatkerülés ($a = 2$) ebben az esetben?

**3. feladat.** Hasonlítsd össze az $a = 1$ (kockázatsemleges) és az $a = 2$ kritériumot: mely forgatókönyvekre szigorúbb az egyik, és melyekre a másik?

## Mintapromptok

- *„Magyarázd el, miért használnak egyes országok kockázatkerülő (a = 2) F–N kritériumot! Milyen etikai és gyakorlati érvek szólnak mellette és ellene? Hivatkozz konkrét szabályozásokra, és jelöld, ha bizonytalan vagy.”*
- *„Ellenőrizd a fenti Python-kód logikáját: helyesen számolja-e a kumulált F(N ≥ n) gyakoriságot? Ne írd át a kódot, csak a hibákat jelezd.”*"""),
]

NB["04_fmeda.ipynb"] = [
("md", """# 4. gyakorlat – FMEDA: diagnosztikai lefedettség és biztonságos meghibásodási hányad

A notebook a könyv 6. fejezetének TT-101 hőmérséklet-távadójára számolja ki az FMEDA-mérőszámokat, majd megmutatja, hogyan változik a DC és az SFF a diagnosztika fejlesztésével.

**Tanulási eredmények:** FMEDA-táblázatból $\\lambda_S$, $\\lambda_{DD}$, $\\lambda_{DU}$, DC és SFF számolása; a diagnosztikai fejlesztések hatásának értékelése; a mérőszámok kapcsolata az architekturális korlátokkal."""),
("code", STILUS + '''import pandas as pd'''),
("code", '''# blokk, meghibásodási mód, λ [FIT], kategória (S / D), diagnosztikai lefedettség a veszélyes részre
fmeda = pd.DataFrame([
    ("RTD érzékelőelem", "szakadás", 150, "S", 0.0),
    ("RTD érzékelőelem", "rövidzár", 100, "D", 1.0),
    ("RTD érzékelőelem", "lassú drift lefelé", 250, "D", 0.0),
    ("A/D átalakító", "befagyott vagy hibás érték", 200, "D", 0.7),
    ("mikrovezérlő", "programfutási hiba", 300, "D", 0.9),
    ("kimeneti fokozat", "áram a felső határon", 200, "S", 0.0),
    ("kimeneti fokozat", "áram beragad közbenső értéken", 150, "D", 0.6),
    ("tápegység", "kiesés", 150, "S", 0.0)],
    columns=["blokk", "mód", "lambda_FIT", "kat", "dc"])
def merok(df):
    lS = df.loc[df.kat == "S", "lambda_FIT"].sum()
    D = df[df.kat == "D"]
    lDD = (D.lambda_FIT * D.dc).sum(); lDU = (D.lambda_FIT * (1 - D.dc)).sum()
    return dict(lS=lS, lDD=lDD, lDU=lDU, DC=lDD/(lDD+lDU), SFF=(lS+lDD)/(lS+lDD+lDU))
m = merok(fmeda)
print(f"λS = {m['lS']:.0f} FIT, λDD = {m['lDD']:.0f} FIT, λDU = {m['lDU']:.0f} FIT")
print(f"DC = {100*m['DC']:.1f} %, SFF = {100*m['SFF']:.1f} %")'''),
("md", """Az eredmény egyezik a könyv 6.x táblázatával: $\\lambda_D = 1000$ FIT, DC = 60%, SFF = 73,3%. A legnagyobb rejtett veszélyes hozzájárulás az érzékelőelem driftje.

## Diagnosztikai fejlesztések

Vizsgáljunk három lehetséges fejlesztést: (a) a két távadó jelének eltérésfigyelése a logikában, amely a drift 90%-át felfedi; (b) jobb A/D-referenciaellenőrzés (95%); (c) mindkettő."""),
("code", '''valtozatok = {"alap": {}, "(a) eltérésfigyelés": {2: 0.9}, "(b) A/D-referencia": {3: 0.95}, "(c) mindkettő": {2: 0.9, 3: 0.95}}
eredm = {}
for nev, mod in valtozatok.items():
    df = fmeda.copy()
    for i, dc in mod.items(): df.loc[i, "dc"] = dc
    eredm[nev] = merok(df)
tab = pd.DataFrame(eredm).T
tab["DC_%"] = 100*tab.DC; tab["SFF_%"] = 100*tab.SFF
print(tab[["lDD", "lDU", "DC_%", "SFF_%"]].round(1))
fig, ax = plt.subplots(figsize=(7.5, 3.4))
ax.barh(list(tab.index), tab.lDU, color=PE["piros"]); ax.set_xlabel("λDU [FIT]"); ax.invert_yaxis(); plt.show()'''),
("md", """**Értelmezés.** Az eltérésfigyelés a rejtett veszélyes rátát 400 FIT-ről 175 FIT-re csökkenti (SFF = 88,3%); a két fejlesztés együtt az SFF-et 90% fölé emeli (91,7%). Az IEC 61508 1H útja szerint egy B típusú elem HFT = 0 mellett 90–99% közötti SFF-fel már SIL 2-ig alkalmazható (60–90% között csak SIL 1-ig). A diagnosztika tehát nemcsak a PFD-t javítja, hanem az architekturális korlátot is.

**1. feladat.** Számold ki a TT-101 egycsatornás PFD-jét ($T_1 = 8760$ h, MTTR = 8 h) az alapváltozatra és a (c) változatra!

**2. feladat.** Egy gyártó a „nincs hatás” kategóriájú meghibásodásokat is a biztonságosak közé számolná, és így az SFF 80% fölé kerülne. Miért nem fogadható ez el az IEC 61508 2010-es kiadása szerint?"""),
("code", '''# 1. feladat
T1, MTTR = 8760, 8
for nev in ["alap", "(c) mindkettő"]:
    lDU, lDD = eredm[nev]["lDU"]*1e-9, eredm[nev]["lDD"]*1e-9
    print(nev, hu(lDU*(T1/2+MTTR) + lDD*MTTR))'''),
]

NB["06_megbizhatosag_weibull.ipynb"] = [
("md", """# 6. gyakorlat – meghibásodási ráta és Weibull-elemzés

A notebook a könyv 8. fejezetének két esetét számolja végig: (1) állandó meghibásodási ráta becslése terepi adatokból konfidenciakorlátokkal, (2) Weibull-illesztés cenzúrázott csapágyadatokra maximum likelihood és rangregresszió módszerrel, bootstrap-konfidenciaintervallummal.

**Tanulási eredmények:** pont- és intervallumbecslés exponenciális modellre; Weibull-paraméterek becslése jobbról cenzúrázott adatokból; a becslési bizonytalanság számszerűsítése."""),
("code", STILUS + '''from scipy import optimize, special'''),
("md", """## 1. Állandó ráta terepi adatokból

250 távadó 4 éven át: $T = 250 \\cdot 4 \\cdot 8760 = 8{,}76\\cdot10^6$ óra, $r = 3$ veszélyes meghibásodás. A pontbecslés $\\hat\\lambda = r/T$, az egyoldali $1-\\alpha$ felső korlát $\\chi^2_{1-\\alpha}(2r+2)/(2T)$."""),
("code", '''T, r = 250*4*8760, 3
print("pontbecslés:", hu(r/T), "1/h")
for c in (0.7, 0.9, 0.95):
    print(f"{int(c*100)} %-os felső korlát: {hu(stats.chi2.ppf(c, 2*r+2)/(2*T))} 1/h")'''),
("md", """A 70%-os felső korlát ($5{,}44\\cdot10^{-7}$) az IEC 61508 2H útjának adatkövetelménye. **1. feladat:** mennyi üzemóra kellene ahhoz, hogy hibamentes működés esetén a 90%-os felső korlát $10^{-7}$/h legyen?

## 2. Weibull-illesztés cenzúrázott adatokra

A KoboCella robothajtásainak csapágyai: kilenc meghibásodás és három, 12 000 óránál még működő (jobbról cenzúrázott) csapágy."""),
("code", '''t = np.array([4100, 5200, 5900, 6600, 7300, 7900, 8500, 9800, 10500, 12000, 12000, 12000], float)
d = np.array([1]*9 + [0]*3)          # 1 = meghibásodott, 0 = cenzúrázott
def negll(p):
    b, e = np.exp(p)
    z = (t/e)**b
    return -(np.sum(d*(np.log(b) - np.log(e) + (b-1)*np.log(t/e))) - np.sum(z))
res = optimize.minimize(negll, x0=np.log([2, 10000]), method="Nelder-Mead", options={"xatol": 1e-9, "fatol": 1e-12, "maxiter": 5000})
beta, eta = np.exp(res.x)
mttf = eta*special.gamma(1 + 1/beta)
print(f"ML-becslés: β = {beta:.3f}, η = {eta:.0f} h, MTTF = {mttf:.0f} h")
print(f"B10 = {eta*(-np.log(0.9))**(1/beta):.0f} h, R(5000) = {np.exp(-(5000/eta)**beta):.3f}")
print(f"R(8000 | 6000) = {np.exp(-(8000/eta)**beta + (6000/eta)**beta):.3f}")'''),
("md", """Az eredmény egyezik a könyvvel: $\\hat\\beta = 2{,}73$, $\\hat\\eta \\approx 10\\,170$ h. A $\\beta > 1$ elhasználódásra utal: a megelőző csere értelmes stratégia.

### Rangregresszió (Weibull-papír)

A rangregresszió a medián rangokat ($F_i \\approx (i - 0{,}3)/(n + 0{,}4)$, cenzúrázott adatoknál Johnson-féle korrigált rangokkal) illeszti egyenesre a $\\ln(-\\ln(1-F))$ – $\\ln t$ síkon."""),
("code", '''# Johnson-féle korrigált rangok
n = len(t); rang_elozo = 0.0; pontok = []
for i, (ti, di) in enumerate(zip(t, d)):
    if di:
        novekmeny = (n + 1 - rang_elozo)/(1 + (n - i))
        rang_elozo += novekmeny
        pontok.append((ti, (rang_elozo - 0.3)/(n + 0.4)))
x = np.log([p[0] for p in pontok]); y = np.log(-np.log(1 - np.array([p[1] for p in pontok])))
b_rr, a_rr = np.polyfit(x, y, 1)
print(f"rangregresszió: β = {b_rr:.3f}, η = {np.exp(-a_rr/b_rr):.0f} h")
fig, ax = plt.subplots()
ax.plot(x, y, "o", color=PE["kek"], label="meghibásodások (medián rang)")
xs = np.linspace(x.min()-0.2, np.log(14000), 50)
ax.plot(xs, b_rr*xs + a_rr, "--", color=PE["szurke"], label="rangregresszió")
ax.plot(xs, beta*(xs - np.log(eta)), color=PE["piros"], label="ML-becslés")
ax.set_xlabel("ln t"); ax.set_ylabel("ln(−ln(1−F))"); ax.legend(); plt.show()'''),
("md", """## 3. Bootstrap-konfidenciaintervallum

Kevés adatnál a becslés bizonytalansága nagy. A parametrikus bootstrap az illesztett modellből új mintákat szimulál (ugyanazzal a cenzúrázási idővel), mindegyikre újra illeszt, és a becslések eloszlásából ad intervallumot."""),
("code", '''rng = np.random.default_rng(42)
B = 1000; becslesek = []
for _ in range(B):
    ts = eta*rng.weibull(beta, n)
    ds = (ts < 12000).astype(int); ts = np.minimum(ts, 12000)
    if ds.sum() < 3: continue
    def nll(p, ts=ts, ds=ds):
        b, e = np.exp(p); z = (ts/e)**b
        return -(np.sum(ds*(np.log(b) - np.log(e) + (b-1)*np.log(ts/e))) - np.sum(z))
    r_ = optimize.minimize(nll, x0=np.log([beta, eta]), method="Nelder-Mead")
    becslesek.append(np.exp(r_.x))
becslesek = np.array(becslesek)
for j, nev in enumerate(["β", "η"]):
    lo, hi = np.percentile(becslesek[:, j], [5, 95])
    print(f"{nev}: 90 %-os bootstrap-intervallum {lo:.2f} – {hi:.2f}")'''),
("md", """**2. feladat.** Hogyan változik az intervallum szélessége, ha a 12 helyett 36 csapágy adata állna rendelkezésre (ugyanazzal az arányú cenzúrázással)? Módosítsd a szimulációt!

**3. feladat.** Milyen megelőző csereidőköz mellett lesz a csapágy meghibásodási valószínűsége a csere előtt legfeljebb 5%?

## Mintaprompt

*„Az alábbi csapágyadatokra Weibull-eloszlást illesztettem (β = 2,73, η = 10 170 h). Magyarázd el lépésenként, mit jelent a β > 1 a karbantartási stratégia szempontjából, és milyen feltevései vannak a megelőző csere optimalizálásának! Ne számolj helyettem; kérdezz rá, ha valamelyik adat hiányzik.”*"""),
]

NB["07_rbd_hid_mc.ipynb"] = [
("md", """# 7. gyakorlat – blokkdiagramok: hídkapcsolás, Monte Carlo, közös okú meghibásodás

A notebook a könyv 9. fejezetének számításait reprodukálja: a hídkapcsolás megbízhatóságát háromféleképpen (állapotfelsorolás, dekompozíció, minimális utak), a bizonytalan komponensadatok hatását Monte Carlo-szimulációval, végül a közös okú meghibásodás hatását az 1oo2 struktúrára."""),
("code", STILUS + '''import itertools'''),
("code", '''# Hídkapcsolás: A–D és C–B a két ág, E a híd; minimális utak
utak = [{"A", "D"}, {"C", "B"}, {"A", "E", "B"}, {"C", "E", "D"}]
elemek = ["A", "B", "C", "D", "E"]
def R_felsorolas(p):
    ossz = 0
    for allapot in itertools.product([0, 1], repeat=5):
        mukodik = {e for e, s in zip(elemek, allapot) if s}
        if any(u <= mukodik for u in utak):
            ossz += np.prod([p[e] if s else 1-p[e] for e, s in zip(elemek, allapot)])
    return ossz
def R_dekompozicio(p):
    # E működik: (A||C) soros (D||B); E hibás: (A–D) || (C–B)
    Rjo = (1-(1-p["A"])*(1-p["C"])) * (1-(1-p["D"])*(1-p["B"]))
    Rrossz = 1 - (1 - p["A"]*p["D"])*(1 - p["C"]*p["B"])
    return p["E"]*Rjo + (1-p["E"])*Rrossz
p = {e: 0.9 for e in elemek}
print("állapotfelsorolás:", round(R_felsorolas(p), 5), " dekompozíció:", round(R_dekompozicio(p), 5))'''),
("md", """Mindkét módszer $R = 0{,}97848$-at ad, egyezésben a könyvvel. **1. feladat:** számold ki a megbízhatóságot a minimális utak szita-formulájával is!

## Bizonytalan komponensadatok

Tegyük fel, hogy minden elem megbízhatósága bizonytalan: béta-eloszlású, várható értéke 0,9, és a 90%-os tartománya nagyjából 0,85–0,95. Az intervallumbecslés (mindegyik a korlátján) és a Monte Carlo-szimuláció összevetése:"""),
("code", '''rng = np.random.default_rng(1)
a, b = 90, 10          # Béta(90, 10): várható érték 0,9
minta = rng.beta(a, b, size=(20000, 5))
Rmc = np.array([R_dekompozicio(dict(zip(elemek, s))) for s in minta])
lo, hi = stats.beta.ppf([0.05, 0.95], a, b)
print(f"elemszintű 90 %-os tartomány: {lo:.3f} – {hi:.3f}")
print(f"intervallumbecslés: {R_dekompozicio(dict.fromkeys(elemek, lo)):.5f} – {R_dekompozicio(dict.fromkeys(elemek, hi)):.5f}")
print(f"Monte Carlo: átlag {Rmc.mean():.5f}, 5–95 %: {np.percentile(Rmc, 5):.5f} – {np.percentile(Rmc, 95):.5f}")
plt.hist(Rmc, bins=60, color=PE["kek"]); plt.xlabel("a hídkapcsolás megbízhatósága"); plt.ylabel("gyakoriság"); plt.show()'''),
("md", """A Monte Carlo-intervallum szűkebb, mert nem feltételezi, hogy minden elem egyszerre a legrosszabb értékén van.

## Közös okú meghibásodás az 1oo2 struktúrában

Két szelep, $\\lambda = 2{,}5\\cdot10^{-6}$/h, egy év küldetési idő, javítás nélkül. A β-tényezős modellben a ráta $\\beta$ hányada mindkét elemet egyszerre éri."""),
("code", '''lam, t = 2.5e-6, 8760
for beta_ in (0, 0.02, 0.05, 0.10, 0.20):
    Rf = np.exp(-(1-beta_)*lam*t); Rc = np.exp(-beta_*lam*t)
    F = 1 - Rc*(1 - (1-Rf)**2)
    print(f"β = {beta_:4.2f}: a két szelep együttes meghibásodásának valószínűsége {hu(F)}")'''),
("md", """**2. feladat.** Mekkora β mellett lesz az 1oo2 struktúra rosszabb, mint a független feltevéssel számolt érték tízszerese? Mit jelent ez a redundancia értékére?

## Mintaprompt

*„Egy hídkapcsolású rendszer megbízhatóságát dekompozícióval számoltam. Kérlek, ellenőrizd a gondolatmenetet lépésenként, és mutasd meg, hogyan kapnám ugyanezt a minimális utakból a szita-formulával! Ne adj meg végeredményt, amíg nem kérem.”*"""),
]

NB["08_hibafa.ipynb"] = [
("md", """# 8. gyakorlat – hibafa: MOCUS, bináris döntési diagram, fontosság és bizonytalanság

A notebook a könyv 10. fejezetének ReaktorVéd-hibafáját elemzi: minimális vágatok a MOCUS-eljárással, pontos valószínűség Shannon-kifejtéssel (a bináris döntési diagram elvén), fontossági mértékek, végül Monte Carlo-bizonytalanságelemzés.

**Tanulási eredmények:** hibafa programozott elemzése; a ritkaesemény-közelítés és a pontos érték összevetése; a fontossági mértékek kiszámolása és értelmezése; a paraméterbizonytalanság terjedésének becslése."""),
("code", STILUS),
("code", '''# A hibafa: kapuk (típus, bemenetek) és alapesemények (valószínűség). HEN: házesemény (1 = energiával működtetett szelepek)
def fa(HEN=1):
    G = {"TOP": ("AND", ["G2", "G3"]), "G2": ("OR", ["BE1", "E1TAP", "G4"]), "G3": ("OR", ["BE2", "E1TAP", "G4"]),
         "G4": ("OR", ["BE4", "E1TAP", "G5"]), "G5": ("AND", ["G6", "G7"]), "G6": ("OR", ["BE5", "E2TAP"]), "G7": ("OR", ["BE7", "E2TAP"])}
    if HEN: G["E1TAP"] = ("OR", ["BE3"]); G["E2TAP"] = ("OR", ["BE6"])
    else:   G["E1TAP"] = ("OR", []);      G["E2TAP"] = ("OR", [])      # üres VAGY = sosem következik be
    return G
q = {"BE1": 1.097e-2, "BE2": 1.097e-2, "BE3": 1e-3, "BE4": 5e-5, "BE5": 1.752e-3, "BE6": 1e-3, "BE7": 1.752e-3}

def minimalis(L):
    L = sorted({frozenset(c) for c in L}, key=len); ki = []
    for c in L:
        if not any(m <= c for m in ki): ki.append(c)
    return ki
def mocus(G, n="TOP"):
    if n not in G: return [frozenset([n])]
    tip, be = G[n]
    if tip == "OR":
        return minimalis([c for b in be for c in mocus(G, b)])
    vag = [frozenset()]
    for b in be:
        vag = minimalis([a | c for a in vag for c in mocus(G, b)])
    return vag
mcs = mocus(fa(1))
for c in sorted(mcs, key=lambda c: (len(c), sorted(c))):
    print(sorted(c), hu(np.prod([q[x] for x in c])))'''),
("code", '''def pontos(cuts, q, memo=None):
    """A csúcsesemény pontos valószínűsége Shannon-kifejtéssel (a BDD elve)."""
    memo = {} if memo is None else memo
    if any(len(c) == 0 for c in cuts): return 1.0
    if not cuts: return 0.0
    kulcs = frozenset(cuts)
    if kulcs in memo: return memo[kulcs]
    gyak = {}
    for c in cuts:
        for v in c: gyak[v] = gyak.get(v, 0) + 1
    x = max(gyak, key=gyak.get)
    egy = minimalis([c - {x} for c in cuts]); nulla = [c for c in cuts if x not in c]
    p = q[x]*pontos(egy, q, memo) + (1-q[x])*pontos(nulla, q, memo)
    memo[kulcs] = p; return p
Qk = [np.prod([q[x] for x in c]) for c in mcs]
print("ritkaesemény-közelítés:", hu(sum(Qk), 5))
print("felső korlát (MCUB):   ", hu(1 - np.prod([1-v for v in Qk]), 5))
print("pontos:                ", hu(pontos(mcs, q), 5))
print("energiamentesítéssel (HEN = 0):", hu(pontos(mocus(fa(0)), q), 4))'''),
("md", """## Fontossági mértékek"""),
("code", '''Q = pontos(mcs, q); rare = sum(Qk)
print(f"{'esemény':8s} {'Birnbaum':>10s} {'FV':>7s} {'RAW':>8s} {'RRW':>7s}")
for v in sorted(q):
    Q1 = pontos(mcs, {**q, v: 1.0}); Q0 = pontos(mcs, {**q, v: 0.0})
    fv = sum(Qc for c, Qc in zip(mcs, Qk) if v in c)/rare
    print(f"{v:8s} {Q1-Q0:10.3e} {fv:7.3f} {Q1/Q:8.1f} {Q/Q0:7.3f}")'''),
("md", """## Monte Carlo-bizonytalanság

Minden alapesemény valószínűsége lognormális, mediánja a pontbecslés, hibatényezője EF = 3 ($\\sigma = \\ln 3/1{,}645$)."""),
("code", '''rng = np.random.default_rng(7); Nmc = 200000; sig = np.log(3)/1.645
minta = {v: q[v]*np.exp(sig*rng.standard_normal(Nmc)) for v in q}
top = np.zeros(Nmc)
for c in mcs:                 # ritkaesemény-közelítés mintánként (kis valószínűségeknél pontos)
    top += np.prod([minta[x] for x in c], axis=0)
print("pontbecslés:", hu(rare), " átlag:", hu(top.mean()), " medián:", hu(np.median(top)))
print("90 %-os intervallum:", hu(np.percentile(top, 5)), "–", hu(np.percentile(top, 95)))
plt.hist(np.log10(top), bins=80, color=PE["kek"]); plt.axvline(np.log10(2e-3), color=PE["piros"], ls="--", label="LOPA-követelmény")
plt.xlabel("log10(PFD)"); plt.legend(); plt.show()'''),
("md", """**1. feladat.** Építsd be a közös okú meghibásodást (szelepek: β = 10%, távadók: β = 5%) az energiamentesítéses változatba, és ellenőrizd, hogy $1{,}335\\cdot10^{-3}$ jön ki!

**2. feladat.** A fontossági mértékek alapján melyik egyetlen tervezési változtatás csökkentené leginkább a kockázatot az energiával működtetett változatban? Indokold a Fussell–Vesely- és az RRW-értékkel!

## Mintaprompt

*„Az alábbi hibafa minimális vágatait MOCUS-eljárással határoztam meg: … Ellenőrizd, hogy a vágatok valóban minimálisak-e, és hogy nem hiányzik-e közülük egy sem! Indokold lépésenként a Boole-algebrai átalakításokkal.”*"""),
]

NB["10_markov.ipynb"] = [
("md", """# 10. gyakorlat – Markov-modellek

A notebook a könyv 12. fejezetének modelljeit valósítja meg: javítható elem, javítható 1oo2 rendszer közös okú meghibásodással, hideg tartalék indulási és rejtett hibával, végül a gyorszáró szelepek többfázisú modellje és a nem tökéletes proof teszt.

**Tanulási eredmények:** intenzitásmátrix felírása; tranziens, tartós és elnyelő állapotos megoldás; többfázisú modell periodikus tesztelésre."""),
("code", STILUS + '''from scipy.linalg import expm
def tartos(Q):
    n = len(Q); A = np.vstack([Q.T, np.ones(n)]); b = np.zeros(n+1); b[-1] = 1
    return np.linalg.lstsq(A, b, rcond=None)[0]
def mttf(Q, start, elnyelo):
    tr = [i for i in range(len(Q)) if i not in elnyelo]
    N = -np.linalg.inv(Q[np.ix_(tr, tr)]); return N[tr.index(start)].sum()'''),
("code", '''lam, mu = 1e-4, 1/8
Q = np.array([[-lam, lam], [mu, -mu]])
p = tartos(Q); print("javítható elem: A =", round(p[0], 6), " U =", hu(p[1]), " állásidő:", round(p[1]*8760, 1), "h/év")
for beta in (0.0, 0.05):
    Q = np.array([[-(2*(1-beta)*lam + beta*lam), 2*(1-beta)*lam, beta*lam], [mu, -(mu+lam), lam], [0, mu, -mu]])
    Qa = Q.copy(); Qa[2] = 0
    print(f"1oo2, β = {beta}: U = {hu(tartos(Q)[2])}, MTTF = {hu(mttf(Qa, 0, [2]))} h")'''),
("code", '''# hideg tartalék: 0 = A üzemel, B tartalék; 1 = A üzemel, B rejtett hiba; 2 = B üzemel; 3 = rendszerhiba
for ps, ld in [(0, 0), (0.02, 0), (0.02, 0.1*lam), (0.05, 0.2*lam)]:
    Q = np.array([[-(lam+ld), ld, lam*(1-ps), lam*ps], [0, -lam, 0, lam], [0, 0, -lam, lam], [0, 0, 0, 0]])
    print(f"p_s = {ps}, λ_d = {ld/lam:.1f}λ: MTTF = {mttf(Q, 0, [3])*lam:.3f}/λ")'''),
("md", """## Többfázisú modell: gyorszáró szelepek, 1oo2

Állapotok: mindkét szelep jó; egy rejtett hibás; mindkettő hibás. A próbák között nincs javítás; a próba (évente) mindent visszaállít. A PFD(t) fűrészfog alakú."""),
("code", '''T1, lDU, b = 8760.0, 2.5e-6, 0.10
li, lc = (1-b)*lDU, b*lDU
Q = np.array([[-(2*li+lc), 2*li, lc], [0, -(li+lc), li+lc], [0, 0, 0]])
dt = 10.0; P = expm(Q*dt); x = np.array([1.0, 0, 0]); pfd = []
for k in range(int(3*T1/dt)):
    if k and k % int(T1/dt) == 0: x = np.array([1.0, 0, 0])     # proof teszt
    pfd.append(x[2]); x = x @ P
pfd = np.array(pfd); tt = np.arange(len(pfd))*dt/8760
print("PFDavg (Markov):", hu(pfd.mean(), 4), " – IEC 61508-6 képlet: 1,227·10^-3")
plt.plot(tt, pfd, color=PE["kek"]); plt.xlabel("idő [év]"); plt.ylabel("PFD(t)"); plt.show()'''),
("code", '''# Nem tökéletes proof teszt: egycsatornás szelep, PTC, nagyjavítás 10 évente
TM = 10*8760; t = np.linspace(0, TM, 200001)
for ptc in (1.0, 0.9, 0.7):
    pf = 1 - np.exp(-ptc*lDU*np.mod(t, T1))*np.exp(-(1-ptc)*lDU*t)
    plt.plot(t/8760, pf, label=f"PTC = {int(ptc*100)} %, átlag {hu(np.trapezoid(pf, t)/TM)}")
plt.xlabel("üzemidő [év]"); plt.ylabel("PFD(t)"); plt.legend(); plt.show()'''),
("md", """**1. feladat.** Egészítsd ki a javítható 1oo2 modellt két javítócsapattal (a 2 → 1 átmenet rátája 2μ)! Hogyan változik a tartós rendelkezésre nem állás és az MTTF?

**2. feladat.** Módosítsd a többfázisú modellt úgy, hogy a két szelepet fél év eltolással teszteljék! Csökken-e a PFD<sub>avg</sub>?

## Mintaprompt

*„Írj fel egy Markov-modellt egy 2oo3 szavazású, javítható rendszerre egy javítócsapattal! Add meg az állapotokat és az intenzitásmátrixot, de a megoldást ne számold ki; azt én végzem el Pythonban.”*"""),
]

NB["11_sil.ipynb"] = [
("md", """# 11. gyakorlat – PFD és SIL-igazolás

A notebook a könyv 13. fejezetének ReaktorVéd-igazolását végzi el: az IEC 61508-6 egyszerűsített képletei, részleges löketpróba, nem tökéletes proof teszt, érzékenységvizsgálat (tornádó), végül Monte Carlo-bizonytalanság a PFD-re.

**Tanulási eredmények:** PFD<sub>avg</sub> számítása 1oo1, 1oo2 és 2oo3 alrendszerekre; a tesztelési stratégia hatásának értékelése; az eredmény bizonytalanságának becslése."""),
("code", STILUS),
("code", '''T1, MTTR, TM = 8760.0, 8.0, 87600.0
def ido(lDU, lDD, ptc=1.0, Tp=None, dcp=0.0, T1=T1):
    lD = lDU + lDD
    if Tp is None:
        a1 = ptc*(T1/2+MTTR) + (1-ptc)*TM/2; a2 = ptc*(T1/3+MTTR) + (1-ptc)*TM/3
    else:
        a1 = (1-dcp)*(T1/2+MTTR) + dcp*(Tp/2+MTTR); a2 = (1-dcp)*(T1/3+MTTR) + dcp*(Tp/3+MTTR)
    return lDU/lD*a1 + lDD/lD*MTTR, lDU/lD*a2 + lDD/lD*MTTR, a1
def pfd(arch, lDU, lDD, beta=0.0, betaD=0.0, **kw):
    tCE, tGE, a1 = ido(lDU, lDD, **kw); lf = (1-betaD)*lDD + (1-beta)*lDU
    ccf = betaD*lDD*MTTR + beta*lDU*a1
    if arch == "1oo1": return (lDU+lDD)*tCE
    if arch == "1oo2": return 2*lf**2*tCE*tGE + ccf
    if arch == "2oo3": return 6*lf**2*tCE*tGE + ccf
def sif(**kw):
    s = pfd("1oo2", 4e-7, 6e-7, 0.05, 0.025, T1=kw.get("T1", T1))
    v = pfd("1oo2", 2.5e-6*kw.get("vfak", 1), 0.0, kw.get("vbeta", 0.10), 0.05,
            ptc=kw.get("ptc", 1.0), Tp=kw.get("Tp"), dcp=kw.get("dcp", 0.0), T1=kw.get("T1", T1))
    return s + 5e-5 + v, s, v
tot, s, v = sif()
print(f"távadók {hu(s)}, logika 5,0·10^-5, szelepek {hu(v)}  ->  PFD = {hu(tot, 4)}, RRF = {1/tot:.0f}")
print("PST havonta (DC 60 %):", hu(sif(Tp=730, dcp=0.6)[0], 4))
print("PTC 90 %:             ", hu(sif(ptc=0.9)[0], 4))'''),
("md", """## Tornádódiagram"""),
("code", '''esetek = [("T1 fél / két év", sif(T1=4380)[0], sif(T1=17520)[0]),
          ("szelep λDU fele / kétszerese", sif(vfak=0.5)[0], sif(vfak=2)[0]),
          ("PTC 100 % / 90 %", tot, sif(ptc=0.9)[0]),
          ("szelep β 5 % / 15 %", sif(vbeta=0.05)[0], sif(vbeta=0.15)[0]),
          ("PST van / nincs", sif(Tp=730, dcp=0.6)[0], tot)]
esetek.sort(key=lambda e: e[2]/e[1])
fig, ax = plt.subplots(figsize=(7.5, 3.6))
for i, (n, lo, hi) in enumerate(esetek):
    ax.barh(i, np.log10(tot) - np.log10(lo), left=np.log10(lo), color=PE["kek"])
    ax.barh(i, np.log10(hi) - np.log10(tot), left=np.log10(tot), color=PE["kiemel"])
ax.axvline(np.log10(2e-3), color=PE["piros"], ls="--", label="követelmény")
ax.set_yticks(range(len(esetek))); ax.set_yticklabels([e[0] for e in esetek]); ax.set_xlabel("log10(PFD)"); ax.legend(); plt.show()'''),
("md", """## Monte Carlo: mennyire biztos a SIL 2?

A meghibásodási ráták és a β-tényezők bizonytalanok. Lognormális eloszlást feltételezünk (EF = 3 a rátákra, EF = 2 a β-kra), mediánként a pontbecsléssel."""),
("code", '''rng = np.random.default_rng(3); N = 50000
def ln(m, ef, n): return m*np.exp(np.log(ef)/1.645*rng.standard_normal(n))
eredm = []
for lt, lv, bt, bv in zip(ln(4e-7, 3, N), ln(2.5e-6, 3, N), np.minimum(ln(0.05, 2, N), 0.5), np.minimum(ln(0.10, 2, N), 0.5)):
    s_ = pfd("1oo2", lt, 1.5*lt, bt, bt/2); v_ = pfd("1oo2", lv, 0.0, bv, bv/2)
    eredm.append(s_ + 5e-5 + v_)
eredm = np.array(eredm)
print("medián:", hu(np.median(eredm)), " 90 %-os intervallum:", hu(np.percentile(eredm, 5)), "–", hu(np.percentile(eredm, 95)))
print("P(PFD > 2·10^-3) =", round((eredm > 2e-3).mean(), 3))'''),
("md", """**Értelmezés.** A pontbecslés teljesíti a követelményt, de a bizonytalanság figyelembevételével jelentős (az eredmény szerint nagyjából egyharmad) annak a valószínűsége, hogy a valódi PFD a határ fölött van. Ez erős érv a részleges löketpróba mellett, és az IEC 61508 2H útjának bizonytalanságkezelési követelményét is szemlélteti.

**1. feladat.** Ismételd meg a Monte Carlo-elemzést havi részleges löketpróbával! Hogyan változik a túllépés valószínűsége?

**2. feladat.** Számold ki a 2oo3 távadó-architektúra PFD-jét és téves leállási gyakoriságát, és hasonlítsd össze az 1oo2-vel!

## Mintaprompt

*„Az alábbi biztonsági funkció PFD-jét az IEC 61508-6 egyszerűsített képleteivel számoltam: … Ellenőrizd, hogy a képletek feltevései (λT ≪ 1, egyidejű tesztelés, tökéletes próba) teljesülnek-e, és sorold fel, melyik feltevés sérülése rontaná leginkább az eredményt! Szabványpontra csak akkor hivatkozz, ha biztos vagy benne.”*"""),
]

def keszit(nev, cellak, futtat=True):
    nb = nbf.v4.new_notebook()
    nb.metadata = {"kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"},
                   "language_info": {"name": "python"}, "colab": {"provenance": []}}
    cells = [nbf.v4.new_markdown_cell(colab(nev))]
    for tip, src in cellak:
        cells.append(nbf.v4.new_markdown_cell(src) if tip == "md" else nbf.v4.new_code_cell(src))
    nb.cells = cells
    if futtat:
        NotebookClient(nb, timeout=600, kernel_name="python3", resources={"metadata": {"path": str(HERE)}}).execute()
    nbf.write(nb, HERE / nev)
    print("notebook:", nev)

if __name__ == "__main__":
    csak = sys.argv[1:]
    for nev, cellak in NB.items():
        if not csak or any(c in nev for c in csak):
            keszit(nev, cellak)
