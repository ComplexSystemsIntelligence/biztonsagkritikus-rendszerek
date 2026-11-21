import numpy as np, itertools, math
q = {'BE1':1.097e-2,'BE2':1.097e-2,'BE3':1e-3,'BE4':5e-5,'BE5':1.752e-3,'BE6':1e-3,'BE7':1.752e-3}
# CCF: szelepek beta=0.10, távadók beta=0.05, energiamentesítéssel működtetett kialakítás (BE3, BE6 kiesik)
bV, bT = 0.10, 0.05
qi = {'V1':(1-bV)*q['BE1'], 'V2':(1-bV)*q['BE2'], 'VC':bV*q['BE1'], 'L':q['BE4'],
      'T1':(1-bT)*q['BE5'], 'T2':(1-bT)*q['BE7'], 'TC':bT*q['BE5']}
mcs = [{'L'},{'VC'},{'TC'},{'V1','V2'},{'T1','T2'}]
rea = sum(math.prod(qi[e] for e in c) for c in mcs)
print('CCF-es FT (de-energize):', f'{rea:.3e}')
for c in mcs: print('  ', sorted(c), f'{math.prod(qi[e] for e in c):.3e}')
# Monte Carlo bizonytalanság, energiával működtetett eredeti fa, lognormális, EF=3 (95%/50%)
rng=np.random.default_rng(7); N=200000
sig=np.log(3)/1.645
def ln(med): return med*np.exp(sig*rng.standard_normal(N))
# medián = pontérték (egyszerűsítés)
s = {k: ln(v) for k,v in q.items()}
top = s['BE3']+s['BE4']+s['BE6']+s['BE1']*s['BE2']+s['BE5']*s['BE7']
print('MC: pontérték', 2.173e-3, 'átlag', top.mean(), 'medián', np.median(top), '5%', np.quantile(top,0.05), '95%', np.quantile(top,0.95))
# log-átlag
print('log-átlag 0.01..0.1:', math.sqrt(0.01*0.1))
# érzékenység: proof teszt évente 4x -> 8x (az eredeti jegyzet példája), szelepek
for T in (8760, 4380):
    qv = 2.5e-6*T/2; qt=4e-7*T/2
    print('T1=',T,'qv',qv,'top(energize)', 1e-3+5e-5+1e-3+qv**2+qt**2)

# --- kiegészítés: hibafa-változatok összevetése (10. fejezet, hibafa-valtozatok ábra) ---
def valtozatok(T1=8760.0, MTTR=8.0):
    lv, bv = 2.5e-6, 0.10          # szelep lambda_DU, béta
    lt, bt = 4.0e-7, 0.05          # távadó lambda_DU, béta
    qv = lv*(T1/2+MTTR); qt = lt*T1/2
    qL, qE = 5e-5, 1e-3
    vc, tc = bv*qv, bt*qt
    vi, ti = ((1-bv)*qv)**2, ((1-bt)*qt)**2
    E_noccf = dict(tap=2*qE, logika=qL, szelep_fuggetlen=qv**2, szelep_ccf=0, tavado_fuggetlen=qt**2, tavado_ccf=0)
    D_noccf = dict(tap=0, logika=qL, szelep_fuggetlen=qv**2, szelep_ccf=0, tavado_fuggetlen=qt**2, tavado_ccf=0)
    D_ccf   = dict(tap=0, logika=qL, szelep_fuggetlen=vi, szelep_ccf=vc, tavado_fuggetlen=ti, tavado_ccf=tc)
    E_ccf   = dict(tap=2*qE, logika=qL, szelep_fuggetlen=vi, szelep_ccf=vc, tavado_fuggetlen=ti, tavado_ccf=tc)
    return E_noccf, D_noccf, D_ccf, E_ccf
for T in (8760.0, 4380.0):
    print('T1 =', T)
    for nev, d in zip(['energiával, CCF nélkül','energiamentes, CCF nélkül','energiamentes, CCF-fel','energiával, CCF-fel'], valtozatok(T)):
        print(f'  {nev:28s} összeg {sum(d.values()):.4e}  ', {k: f'{v:.3e}' for k, v in d.items()})
