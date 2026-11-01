import json, re
from collections import defaultdict
M=json.load(open('marrow/modules.json'))
S=json.load(open('hy/schedule2.json'))
SYS={'Cardiology':'cardio','Nephrology':'nephro','Endocrinology':'endo','Neurology':'neuro','Gastro/Hepatology':'gi','Rheumatology':'rheum',
     'Infectious Diseases':'id','Haematology':'heme','Other topics':'tox'}
SUBJ={'Other topics':'Toxicology & environment','Gastro/Hepatology':'Gastro & Hepatology','Haematology':'Haematology'}
H={ # most-asked in Medical-group PYQs (from the PYQ map); everything else in the must list = asked
 'Valvular Heart Diseases','STE-ACS','NSTE-ACS','Chronic Coronary Syndrome','Evaluation in Cardiology','Atrial Fibrillation','Ventricular Tachycardia','Bradyarrhythmia','Approach to Ventricular Arrhythmia',
 'Glomerular Diseases','Acute Kidney Injury','Tubulointerstitial Diseases','Polycystic Kidney Disease & Inherited Tubule Disorders',
 'Disorders of Adrenal Cortex','Diabetes Mellitus','Anterior Pituitary','Posterior Pituitary','Thyroid Physiology & Testing','Hypothyroidism','Hyperthyroidism','Parathyroids & Bone-Mineral Metabolism','Disorders of Sexual Development','Disorders of Testes & Male Reproductive System','Disorders of the Female Reproductive System',
 'Ischemic CVA','Delirium/Dementia/Intelligence/Memory',"Parkinson's Disease",'Demyelinating Disorders','Neurology of Nutrition and Toxicology',
 'Liver','Pancreas','Small Intestines','Nutrition and Gastroenterology',
 'Vasculitis Syndromes','SLE & APS','RA Pathogenesis & Clinical Features','RA Investigations & Treatment','Spondyloarthritides Core Concepts','SpA Individual Disorders',
 'HIV/AIDS','Tuberculosis, Leprosy & Mycobacteria','Viral Infections I','Bacterial Infections I',
 'Hypoproliferative Anemias','Megaloblastic Anemias','Disorders of Hemoglobin','Disorders of Megakaryocytes'}
must=[m for m in M if m['sec']=='must']
for m in must:
    m['sys']=SYS[m['subj']]; m['tier']='H' if (m['name'] in H or m['subj']=='Other topics') else 'M'
    m['subj']=SUBJ.get(m['subj'],m['subj'])
    m['id']='mr:'+m['name']
    m['left']=m['q']; m['done_from']=0
missing=[n for n in H if n not in {m['name'] for m in must}]
assert not missing, missing
queue=defaultdict(list)
for m in sorted(must,key=lambda m:m['tier']!='H'): queue[m['sys']].append(m)
DAYSYS={'cardio':'cardio','neuro':'neuro','onco':'heme','endo':'endo','gi':'gi','id':'id','cc':'tox','nephro':'nephro','rheum':'rheum','pulm':None,'misc':None}
RATE=30
def take(sysk,cap):
    got=[]; room=cap
    def pool():
        if sysk and any(m['left'] for m in queue[sysk]): return [m for m in queue[sysk] if m['left']]
        allm=[m for q in queue.values() for m in q if m['left']]
        return sorted(allm,key=lambda m:(m['tier']!='H', -sum(x['left'] for x in queue[m['sys']] if x['tier']=='H')))
    while room>0:
        p=pool()
        if not p: break
        m=p[0]
        if room<10 and m['left']>room+12: break
        n=m['left'] if m['left']<=room+12 else room
        if m['left']-n<8: n=m['left']
        a=m['q']-m['left']+1; b=a+n-1
        part=None if (a==1 and b==m['q']) else f"Q{a}–{b}"
        got.append(dict(id=m['id']+(f"#{a}" if part else ""),k='mar',t=m['name']+(f" ({part})" if part else ""),q=n,tier=m['tier'],subj=m['subj'],b='M'))
        m['left']-=n; room-=n
        if sysk and not any(x['left'] for x in queue[sysk]) and room<10: break
    return got
plan={}
for d in S['phase1']:
    if d['n']<3: continue
    cap=RATE*3 if d.get('light') else RATE
    sk='cardio' if d['n'] in (8,9) else DAYSYS[d['sys']]
    plan[('p1',d['n'])]=take(sk,cap)
P2CAP={1:30,2:60,3:30,4:60,5:60,6:30,7:60,8:60,9:30,10:60}
for d in S['phase2']:
    if d['n'] in P2CAP: plan[('p2',d['n'])]=take(DAYSYS[d['sys']],P2CAP[d['n']])
sched=sum(i['q'] for v in plan.values() for i in v)
left=[m for m in must if m['left']]
print('scheduled',sched,'of',sum(m['q'] for m in must),'| leftover',sum(m['left'] for m in left),[ (m['name'],m['left'],m['tier']) for m in left])
for k,v in plan.items(): print(k, sum(i['q'] for i in v), ' + '.join(f"{i['tier']}:{i['t']}({i['q']})" for i in v))
json.dump(dict(plan={f"{a}:{b}":v for (a,b),v in plan.items()},
  modules=[dict(id=m['id'],t=m['name'],q=m['q'],tier=m['tier'],subj=m['subj'],sys=m['sys'],left=m['left']) for m in must]),
  open('marrow/mplan.json','w'))
