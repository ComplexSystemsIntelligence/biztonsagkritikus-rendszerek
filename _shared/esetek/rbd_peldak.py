import itertools, numpy as np
from math import comb
p=0.9
# híd: 1-2 felső ág (A,B), alsó (C,D), középső E; utak: AB, CD, AED, CEB
paths=[{'A','B'},{'C','D'},{'A','E','D'},{'C','E','B'}]
comp=['A','B','C','D','E']
def works(state): return any(all(state[c] for c in P) for P in paths)
R=0
for bits in itertools.product([0,1],repeat=5):
    st=dict(zip(comp,bits)); pr=np.prod([p if b else 1-p for b in bits])
    if works(st): R+=pr
print('híd p=0.9:', R, ' képlet:', 2*p**2+2*p**3-5*p**4+2*p**5)
# dekompozíció E szerint
R_Ework = (1-(1-p)**2)**2      # E működik: (A||C) sorosan (B||D)
R_Efail = 1-(1-p*p)**2         # E hibás: AB || CD
print('dekompozíció:', p*R_Ework+(1-p)*R_Efail, R_Ework, R_Efail)
# koon
def koon(k,n,p): return sum(comb(n,j)*p**j*(1-p)**(n-j) for j in range(k,n+1))
for q in (0.9,0.99,0.5,0.3): print(q, 'R 1oo1',q,'1oo2',koon(1,2,q),'2oo2',koon(2,2,q),'2oo3',koon(2,3,q))
# MTTF 2oo3 exp
print('MTTF 2oo3 = 5/(6 lam)')
# eredeti intervallumos példa
A=(0.70,0.72); B=(0.80,0.84); C=(0.60,0.62); D=(0.98,0.99); E=(0.96,0.97); F=(0.98,0.99)
for i,lab in ((0,'alsó'),(1,'felső')):
    s1=1-(1-A[i])*(1-B[i])*(1-C[i]); s2=D[i]*E[i]*F[i]; sy=1-(1-s1)*(1-s2)
    print(lab, round(s1,6), round(s2,6), round(sy,6))
# Monte Carlo
rng=np.random.default_rng(1)
N=200000
def u(a): return rng.uniform(a[0],a[1],N)
a,b,c,d,e,f=map(u,(A,B,C,D,E,F))
s1=1-(1-a)*(1-b)*(1-c); s2=d*e*f; sy=1-(1-s1)*(1-s2)
print('MC: átlag', sy.mean(), '5%', np.quantile(sy,0.05), '95%', np.quantile(sy,0.95))
# hideg tartalék vs meleg párhuzamos
lam=1e-4
for t in (5000,10000,20000):
    print(t, 'meleg', 1-(1-np.exp(-lam*t))**2, 'hideg', np.exp(-lam*t)*(1+lam*t), 'egy', np.exp(-lam*t))
# eredeti 4.13: R3 soros (R1||R2)
print('4.13:', 0.95*(1-0.2*0.1))
