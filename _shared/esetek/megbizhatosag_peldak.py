"""A 8. fejezet számpéldái (terepi adatok, Weibull-illesztés)."""
import numpy as np
from scipy import stats, optimize, special
# --- terepi adat, exponenciális, időre csonkított vizsgálat ---
n_eszkoz, evek, r = 250, 4, 3
T = n_eszkoz*evek*8760
lam = r/T
for conf in (0.70, 0.90, 0.95):
    up = stats.chi2.ppf(conf, 2*r+2)/(2*T)
    print(f"terep: T={T:.3e} h, r={r}, lam_hat={lam:.3e}, {conf:.0%} felső korlát={up:.3e}")
print("nulla hiba 95%: ", -np.log(0.05)/T, " (3/T =", 3/T, ")")
# --- Weibull: KoboCella hajtómű-csapágy élettartamok (üzemóra), + = cenzúrázott ---
t = np.array([4100, 5200, 5900, 6600, 7300, 7900, 8500, 9800, 10500, 12000, 12000, 12000], float)
cens = np.array([0,0,0,0,0,0,0,0,0,1,1,1])  # 1: még működik 12000 óránál
def nll(p):
    b, e = np.exp(p)
    z = (t/e)**b
    ll = np.where(cens==0, np.log(b/e)+(b-1)*np.log(t/e)-z, -z)
    return -ll.sum()
res = optimize.minimize(nll, np.log([2, 9000]), method='Nelder-Mead', options={'xatol':1e-9,'fatol':1e-9,'maxiter':5000})
b, e = np.exp(res.x)
print(f"Weibull MLE: beta={b:.3f}, eta={e:.0f} h, MTTF={e*special.gamma(1+1/b):.0f} h")
print("B10 élettartam:", e*(-np.log(0.9))**(1/b))
print("R(5000)=", np.exp(-(5000/e)**b))
# medián rang (Benard) a nem cenzúrázott pontokra (Johnson-féle korrekció cenzúra miatt itt nincs, mert a cenzúra a végén van)
nf = (cens==0).sum(); n=len(t)
ranks = np.arange(1, nf+1)
F = (ranks-0.3)/(n+0.4)
print("pontok (t, F):", [(int(a), round(f,4)) for a,f in zip(t[:nf],F)])
x = np.log(t[:nf]); y = np.log(-np.log(1-F))
sl, ic = np.polyfit(x, y, 1)
print(f"rangregresszió: beta={sl:.3f}, eta={np.exp(-ic/sl):.0f}")
# feltételes megbízhatóság: 6000 óra után még 2000 óra
print("R(8000|6000) =", np.exp(-(8000/e)**b)/np.exp(-(6000/e)**b))
