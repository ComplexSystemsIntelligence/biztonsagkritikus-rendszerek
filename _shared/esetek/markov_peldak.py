"""Markov-modellek a 12. fejezethez -- a könyvben szereplő számértékek forrása.
Futtatás: python3 markov_peldak.py"""
import numpy as np
from scipy.linalg import expm

def stac(Q):
    n = Q.shape[0]
    A = np.vstack([Q.T, np.ones(n)])
    b = np.zeros(n+1); b[-1] = 1
    return np.linalg.lstsq(A, b, rcond=None)[0]

def mttf(Q, start, absorbing):
    tr = [i for i in range(Q.shape[0]) if i not in absorbing]
    Qt = Q[np.ix_(tr, tr)]
    N = -np.linalg.inv(Qt)
    return N[tr.index(start)].sum()

lam, mttr = 1e-4, 8.0
mu = 1/mttr
# 1) egyetlen javítható elem
Q = np.array([[-lam, lam], [mu, -mu]])
p = stac(Q)
print(f"[1] A = {p[0]:.6f}, U = {p[1]:.3e}, lambda*MTTR = {lam*mttr:.3e}, állásidő {p[1]*8760:.2f} h/év, időállandó 1/(l+m) = {1/(lam+mu):.2f} h")
# 2) 1oo2, egy javítócsapat, közös ok nélkül és béta=5%-kal
for beta in (0.0, 0.05):
    # állapotok: 0 = mindkettő jó, 1 = egy jó, 2 = rendszerhiba
    Q = np.array([[-(2*(1-beta)*lam + beta*lam), 2*(1-beta)*lam, beta*lam],
                  [mu, -(mu+lam), lam],
                  [0, mu, -mu]])
    p = stac(Q)
    Qa = Q.copy(); Qa[2] = 0
    m = mttf(Qa, 0, [2])
    print(f"[2] béta={beta:.2f}: U_rendszer = {p[2]:.3e}, MTTF_rendszer = {m:.4e} h ({m/8760:.0f} év)")
print(f"[2] javítás nélkül: MTTF = 1.5/lambda = {1.5/lam:.0f} h; képlet (3l+m)/(2l^2) = {(3*lam+mu)/(2*lam**2):.4e} h")
# 3) hideg tartalék: indulási hiba p_s, alvó meghibásodás lambda_d, javítás nélkül
for ps, ld in [(0.0, 0.0), (0.02, 0.0), (0.02, 0.1*lam), (0.05, 0.2*lam)]:
    # 0: A üzemel, B tartalékban jó; 1: A üzemel, B tartalékban hibás; 2: B üzemel; 3: rendszerhiba
    Q = np.array([[-(lam+ld), ld, lam*(1-ps), lam*ps],
                  [0, -lam, 0, lam],
                  [0, 0, -lam, lam],
                  [0, 0, 0, 0]], dtype=float)
    m = mttf(Q, 0, [3])
    print(f"[3] p_s={ps:.2f}, lambda_d={ld/lam:.1f}*lambda: MTTF = {m*lam:.3f}/lambda")
print("[3] meleg tartalék (1oo2 aktív): 1.500/lambda")
# 4) többfázisú Markov: 1oo2 szelep, béta=10%, T1=8760, MTTR=8 -- PFDavg
T1, MTTR = 8760.0, 8.0
lDU, beta = 2.5e-6, 0.10
li, lc = (1-beta)*lDU, beta*lDU
# állapotok: 0 OK-OK, 1 egy DU, 2 mindkettő DU (veszélyes)
Q = np.array([[-(2*li+lc), 2*li, lc],
              [0, -(li+lc), li+lc],
              [0, 0, 0]])
dt = 1.0; n = int(T1/dt)
P = expm(Q*dt)
x = np.array([1.0, 0, 0]); s = 0.0
for k in range(n):
    xn = x @ P
    s += 0.5*(x[2]+xn[2])*dt
    x = xn
pfd_markov = s/T1
# javítási idő hozzájárulás: proof teszt után a hibás szelepek MTTR-ig nem állnak rendelkezésre
pfd_markov_mttr = pfd_markov + x[2]*MTTR/T1 + x[1]*0  # egy hibás szelep javítás alatt a másik véd
print(f"[4] 1oo2 szelep, többfázisú Markov: PFDavg (a periódus alatt) = {pfd_markov:.4e}, javítással ~ {pfd_markov_mttr:.4e}")
print(f"[4] IEC 61508-6 képlet (reaktorved.py): 1.227e-03; közös ok {lc*(T1/2+MTTR):.4e}, független 2(li)^2 tCE tGE = {2*li**2*(T1/2+MTTR)*(T1/3+MTTR):.4e}")
print(f"[4] PFD(T1-) a próba előtt = {x[2]:.4e}")
# 5) nem tökéletes proof teszt: 1oo1 szelep, PTC=0.9, T_M = 10 év
TM = 10*8760.0
for ptc in (1.0, 0.9, 0.7):
    approx = ptc*lDU*(T1/2+MTTR) + (1-ptc)*lDU*(TM/2)
    # numerikus időátlag
    t = np.linspace(0, TM, 200001)
    pfd_t = 1-np.exp(-ptc*lDU*np.mod(t, T1))*np.exp(-(1-ptc)*lDU*t)
    print(f"[5] PTC={ptc:.1f}: PFDavg közelítés = {approx:.3e}, numerikus (MTTR nélkül) = {np.trapezoid(pfd_t, t)/TM:.3e}, PFD a 10. év végén {pfd_t[-1]:.3e}")
