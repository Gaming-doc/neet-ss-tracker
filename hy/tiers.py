import sys, re
sys.path.insert(0,'.'); sys.path.insert(0,'hy')
from data import main
from yieldmap import load
from collections import defaultdict
def canon(n): return re.sub(r" P\d \(Q\d+-\d+\)","",n)
bank=defaultdict(int)
for d in main.values():
    for n,c in d: bank[canon(n)]+=c
bank['Cardio: Valvular incl RHD']+=0
rows=load(); score=defaultdict(float); topics=defaultdict(lambda: defaultdict(float))
for r in rows:
    for m in r['mods']:
        score[m]+=r['w']/len(r['mods']); topics[m][r['topic']]+=r['w']/len(r['mods'])
LOWFOCUS=re.compile(r'^(Onco:|IBQ: Onco|Pulm:|CCM: (Respiratory|Cardiac|Misc|Trauma)|Biostatistics|Geriatric|Pharmacogenomics|Immunology|Sympt: (Syncope|Cardiorespiratory))')
def tier(m):
    s=score.get(m,0); b=bank.get(m,0) or 1; dens=100*s/b
    if m.startswith('IBQ'):
        return 'L' if LOWFOCUS.match(m) else 'M'
    if s>=6 or (dens>=10 and s>=4): return 'H'
    if LOWFOCUS.match(m) and s<4: return 'L'
    if s<=1.5 and b>=60: return 'L'
    return 'M'
if __name__=='__main__':
    from collections import Counter
    out=[]
    for m in bank:
        out.append((tier(m),score.get(m,0),bank[m],m))
    for t in 'HML':
        sel=sorted([o for o in out if o[0]==t],key=lambda o:-o[1])
        print(f"\n== {t}: {len(sel)} modules, {sum(o[2] for o in sel)} Qs")
        for o in sel: print(f"   {o[1]:5.1f} pyq  {o[2]:4} Qs  {o[3]}")
