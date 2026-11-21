"""ReaktorVéd esettanulmány -- a könyvben használt számértékek egyetlen forrása.
Futtatás: python3 reaktorved.py  (a kimenet a fejezetek számpéldáival egyezik)."""
import math, itertools
T1 = 8760.0      # proof teszt intervallum [h]
MTTR = 8.0       # javítási idő [h]
# --- LOPA ---
f_IE = 0.1       # hűtővíz-kiesés gyakorisága [1/év]
P_en = 0.5       # feltételt teremtő tényező: exoterm fázis aránya
PFD_alarm = 0.1  # riasztás + operátori beavatkozás
f_mitig = f_IE*P_en*PFD_alarm
f_tol = 1e-5     # tolerálható gyakoriság egy haláleset-szcenárióra [1/év]
PFD_req = f_tol/f_mitig
print(f"LOPA: f(SIF nélkül) = {f_mitig:.1e}/év, szükséges PFD <= {PFD_req:.1e}, RRF >= {1/PFD_req:.0f}")
# --- SIF elemek ---
def pfd_1oo1(lDU, lDD=0.0):
    return lDU*(T1/2+MTTR) + lDD*MTTR
def pfd_1oo2(lDU, lDD, beta, betaD):
    lD = lDU+lDD
    tCE = lDU/lD*(T1/2+MTTR) + lDD/lD*MTTR
    tGE = lDU/lD*(T1/3+MTTR) + lDD/lD*MTTR
    ind = 2*((1-betaD)*lDD+(1-beta)*lDU)**2*tCE*tGE
    ccf = betaD*lDD*MTTR + beta*lDU*(T1/2+MTTR)
    return ind+ccf, ind, ccf
TT_lD, TT_DC = 1.0e-6, 0.6
TT_lDD, TT_lDU = TT_lD*TT_DC, TT_lD*(1-TT_DC)
V_lDU = 2.5e-6
PFD_LS = 5e-5
s, s_ind, s_ccf = pfd_1oo2(TT_lDU, TT_lDD, 0.05, 0.025)
v, v_ind, v_ccf = pfd_1oo2(V_lDU, 0.0, 0.10, 0.05)
print(f"TT 1oo1 PFD = {pfd_1oo1(TT_lDU, TT_lDD):.3e}")
print(f"TT 1oo2: PFD = {s:.3e} (független {s_ind:.3e}, közös ok {s_ccf:.3e})")
print(f"Szelep 1oo1 PFD = {pfd_1oo1(V_lDU):.3e}")
print(f"Szelep 1oo2: PFD = {v:.3e} (független {v_ind:.3e}, közös ok {v_ccf:.3e})")
tot = s+PFD_LS+v
print(f"SIF PFDavg = {tot:.3e}  (érzékelők {s/tot:.0%}, logika {PFD_LS/tot:.0%}, szelepek {v/tot:.0%}) RRF = {1/tot:.0f}")
# részleges löketvizsgálat (PST): DC_PST = 0.6, PST havonta
DC_pst, T_pst = 0.6, 730.0
def pfd_valve_pst(beta):
    lDU1 = V_lDU*(1-DC_pst); lDU2 = V_lDU*DC_pst
    # egycsatornás közelítés a közös okú részre (a domináns tag)
    return beta*(lDU1*(T1/2+MTTR) + lDU2*(T_pst/2+MTTR))
v_pst_ccf = pfd_valve_pst(0.10)
print(f"Szelep közös okú tag PST-vel: {v_pst_ccf:.3e} (PST nélkül {v_ccf:.3e})")
# --- Hibafa (energiával működtetett kialakítás) ---
q = {'BE1': pfd_1oo1(V_lDU), 'BE2': pfd_1oo1(V_lDU), 'BE3': 1e-3, 'BE4': PFD_LS,
     'BE5': TT_lDU*(T1/2), 'BE6': 1e-3, 'BE7': TT_lDU*(T1/2)}
mcs = [{'BE3'}, {'BE4'}, {'BE6'}, {'BE1','BE2'}, {'BE5','BE7'}]
def prod(c): return math.prod(q[e] for e in c)
rea = sum(prod(c) for c in mcs)
# pontos (inkluzió-exklúzió)
ex = 0.0
for k in range(1, len(mcs)+1):
    for comb in itertools.combinations(mcs, k):
        ex += (-1)**(k+1)*prod(set().union(*comb))
mcub = 1-math.prod(1-prod(c) for c in mcs)
print("q:", {k: f"{v:.3e}" for k,v in q.items()})
print(f"FT csúcs: ritka esemény {rea:.4e}, MCUB {mcub:.4e}, pontos {ex:.4e}")
for c in mcs: print("  MCS", sorted(c), f"{prod(c):.3e}", f"{prod(c)/rea:.1%}")
# fontossági mértékek (pontos struktúrafüggvénnyel)
def top(qq):
    tot=0.0
    for k in range(1, len(mcs)+1):
        for comb in itertools.combinations(mcs, k):
            tot += (-1)**(k+1)*math.prod(qq[e] for e in set().union(*comb))
    return tot
Q0 = top(q)
print(f"{'esemény':8s} {'Birnbaum':>10s} {'FV':>8s} {'RAW':>9s} {'RRW':>9s}")
for e in sorted(q):
    q1 = dict(q); q1[e] = 1.0; Q1 = top(q1)
    q0 = dict(q); q0[e] = 0.0; Qz = top(q0)
    IB = Q1-Qz; FV = (Q0-Qz)/Q0; RAW = Q1/Q0; RRW = Q0/Qz if Qz>0 else float('inf')
    print(f"{e:8s} {IB:10.3e} {FV:8.3f} {RAW:9.1f} {RRW:9.3f}")
# energiamentesítéssel működtetett (de-energize-to-trip) kialakítás: BE3, BE6 nem veszélyes
mcs2 = [{'BE4'}, {'BE1','BE2'}, {'BE5','BE7'}]
rea2 = sum(prod(c) for c in mcs2)
print(f"FT de-energize: {rea2:.3e}")
# 1oo2 időátlag-korrekció: átlagok szorzata vs szorzat átlaga
lam=V_lDU; avg_prod = (lam*T1)**2/3; prod_avg=(lam*T1/2)**2
print(f"1oo2 szelep: szorzat átlaga {avg_prod:.3e}, átlagok szorzata {prod_avg:.3e}, arány {avg_prod/prod_avg:.3f}")
