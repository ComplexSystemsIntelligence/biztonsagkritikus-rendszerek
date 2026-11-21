"""SIL-igazolás (13. fejezet) -- a könyv számértékeinek forrása.
Az IEC 61508-6 egyszerűsített képletei (B.3.2.2, B.3.3.2) és azok kiterjesztése
részleges löketpróbára (PST) és nem tökéletes proof tesztre (PTC). Futtatás: python3 sil_peldak.py"""
import numpy as np

T1, MTTR = 8760.0, 8.0
TM = 10*8760.0
def tce_tge(lDU, lDD, T1=T1, MTTR=MTTR, ptc=1.0, Tp=None, dcp=0.0):
    """Ekvivalens leállási idők. ptc: proof teszt lefedettség (a maradék TM-nél derül ki);
    Tp, dcp: részleges löketpróba időköze és lefedettsége (a DU-hibák dcp hányadát fedi fel)."""
    lD = lDU+lDD
    if Tp is None:
        a1 = ptc*(T1/2+MTTR) + (1-ptc)*(TM/2)
        a2 = ptc*(T1/3+MTTR) + (1-ptc)*(TM/3)
    else:
        a1 = (1-dcp)*(T1/2+MTTR) + dcp*(Tp/2+MTTR)
        a2 = (1-dcp)*(T1/3+MTTR) + dcp*(Tp/3+MTTR)
    tCE = lDU/lD*a1 + lDD/lD*MTTR
    tGE = lDU/lD*a2 + lDD/lD*MTTR
    return tCE, tGE, a1
def pfd_1oo1(lDU, lDD=0.0, **kw):
    tCE, tGE, a1 = tce_tge(lDU, lDD, **kw)
    return (lDU+lDD)*tCE
def pfd_1oo2(lDU, lDD, beta, betaD, **kw):
    tCE, tGE, a1 = tce_tge(lDU, lDD, **kw)
    ind = 2*((1-betaD)*lDD + (1-beta)*lDU)**2*tCE*tGE
    ccf = betaD*lDD*MTTR + beta*lDU*a1
    return ind+ccf, ind, ccf
def pfd_2oo3(lDU, lDD, beta, betaD, **kw):
    tCE, tGE, a1 = tce_tge(lDU, lDD, **kw)
    ind = 6*((1-betaD)*lDD + (1-beta)*lDU)**2*tCE*tGE
    ccf = betaD*lDD*MTTR + beta*lDU*a1
    return ind+ccf, ind, ccf
def pfh_1oo2(lDU, lDD, beta, betaD, T1, MRT=8.0):
    lD = lDU+lDD
    tCE = lDU/lD*(T1/2+MRT) + lDD/lD*MRT
    return 2*((1-betaD)*lDD+(1-beta)*lDU)*(1-beta)*lDU*tCE + betaD*lDD + beta*lDU

# --- ReaktorVéd adatok ---
TT = dict(lDU=4e-7, lDD=6e-7, beta=0.05, betaD=0.025); TT_lS = 5e-7
V  = dict(lDU=2.5e-6, lDD=0.0, beta=0.10, betaD=0.05)
LS = 5e-5
def sif(T1=T1, MTTR=MTTR, vbeta=0.10, vfak=1.0, ptc=1.0, Tp=None, dcp=0.0, sens='1oo2'):
    kw = dict(T1=T1, MTTR=MTTR)
    s = (pfd_1oo2 if sens=='1oo2' else pfd_2oo3)(TT['lDU'], TT['lDD'], TT['beta'], TT['betaD'], **kw)[0]
    v = pfd_1oo2(V['lDU']*vfak, 0.0, vbeta, 0.05, ptc=ptc, Tp=Tp, dcp=dcp, **kw)
    return s + LS + v[0], s, v
base, s, v = sif()
print(f"[A] alapeset: érzékelők {s:.3e}, logika {LS:.1e}, szelepek {v[0]:.3e} (független {v[1]:.3e}, közös ok {v[2]:.3e}); SIF {base:.3e}, RRF {1/base:.0f}")
pst, s_p, v_p = sif(Tp=730.0, dcp=0.6)
print(f"[B] PST (DC 60%, havonta): szelepek {v_p[0]:.3e} (független {v_p[1]:.3e}, közös ok {v_p[2]:.3e}); SIF {pst:.3e}, RRF {1/pst:.0f}")
ptc9, _, v_c = sif(ptc=0.9)
print(f"[C] PTC 90% (TM 10 év): szelepek {v_c[0]:.3e}; SIF {ptc9:.3e}, RRF {1/ptc9:.0f}")
# numerikus ellenőrzés (pontos időátlag, egyidejű tesztek, MTTR nélkül)
def num_valves(Tp=None, dcp=0.0, ptc=1.0, beta=0.10, lDU=2.5e-6, horizon=TM, n=400001):
    t = np.linspace(0, horizon, n)
    if Tp is None:
        cats = [(lDU*ptc, T1), (lDU*(1-ptc), TM)]
    else:
        cats = [(lDU*(1-dcp), T1), (lDU*dcp, Tp)]
    Si = np.exp(-sum((1-beta)*l*np.mod(t, T) for l, T in cats))
    Sc = np.exp(-sum(beta*l*np.mod(t, T) for l, T in cats))
    pfd = 1 - Sc*(1 - (1-Si)**2)
    return np.trapezoid(pfd, t)/horizon
print(f"[D] numerikus ellenőrzés szelepek: alap {num_valves():.3e}, PST {num_valves(Tp=730.0, dcp=0.6):.3e}, PTC90 {num_valves(ptc=0.9):.3e}")
# érzékenység (tornádó)
cases = [("T1 = 0,5 év / 2 év", sif(T1=4380.0)[0], sif(T1=17520.0)[0]),
         ("szelep béta = 5% / 15%", sif(vbeta=0.05)[0], sif(vbeta=0.15)[0]),
         ("szelep lambda_DU x0,5 / x2", sif(vfak=0.5)[0], sif(vfak=2.0)[0]),
         ("MTTR = 8 h / 72 h", base, sif(MTTR=72.0)[0]),
         ("részleges löketpróba (havonta)", sif(Tp=730.0, dcp=0.6)[0], base),
         ("proof teszt lefedettség 100% / 90%", base, sif(ptc=0.9)[0])]
print("[E] érzékenység (alacsony / magas):")
for n_, lo, hi in cases: print(f"     {n_:38s} {lo:.3e}  {hi:.3e}")
# 2oo3 érzékelők
s23 = pfd_2oo3(TT['lDU'], TT['lDD'], TT['beta'], TT['betaD'])
print(f"[F] érzékelők 2oo3: {s23[0]:.3e} (független {s23[1]:.3e}, közös ok {s23[2]:.3e}) vs 1oo2 {s:.3e}")
# architekturális korlátok
lS, lDD, lDU = TT_lS, TT['lDD'], TT['lDU']
sff = (lS+lDD)/(lS+lDD+lDU)
print(f"[G] távadó SFF = {sff:.1%}, DC = {lDD/(lDD+lDU):.0%}")
# téves leállások (feltevések): TT lS 5e-7, DD->kioldás; szelep téves zárás 1e-6/szelep; logika 1e-6; tápegység 5e-6/db (2 db)
str_tt_1oo2 = 2*(TT_lS+lDD)
str_tt_2oo3 = 6*(TT_lS+lDD)**2*MTTR
str_v, str_l, lam_psu = 2*1e-6, 1e-6, 5e-6
for nev, sens, psu in [("1oo2 távadó, egyszeres táp", str_tt_1oo2, 2*lam_psu),
                       ("1oo2 távadó, redundáns táp", str_tt_1oo2, 2*(2*lam_psu**2*MTTR)),
                       ("2oo3 távadó, redundáns táp", str_tt_2oo3, 2*(2*lam_psu**2*MTTR))]:
    tot = sens+str_v+str_l+psu
    print(f"[H] STR {nev:28s}: {tot:.3e}/h = {tot*8760:.3f}/év, MTTFS = {1/(tot*8760):.1f} év (érzékelők {sens:.2e}, táp {psu:.2e})")
# KoboCella: kétcsatornás biztonságos megállítás PFH (nagy igénybevétel)
for T in (20*8760.0,):
    pfh = pfh_1oo2(1e-8, 9.9e-7, 0.02, 0.01, T)
    print(f"[I] KoboCella 1oo2 PFH (lD=1e-6, DC 99%, béta 2%, béta_D 1%, T1=20 év): {pfh:.3e}/h")
    pfh_b = pfh_1oo2(5e-8, 9.5e-7, 0.02, 0.01, T)
    print(f"[I] ugyanez DC 95%: {pfh_b:.3e}/h; 1oo1 DC 99%: PFH ~ lambda_DU = 1.0e-08 + DD reakció")
