import sys, re, json
sys.path.insert(0,'.'); sys.path.insert(0,'hy')
from data import main, qrp
from yieldmap import load
from collections import defaultdict, Counter
def canon(n): return re.sub(r" P\d \(Q\d+-\d+\)","",n)
bank=defaultdict(int)
for d in main.values():
    for n,c in d: bank[canon(n)]+=c
rows=load()
score=defaultdict(float); mtop=defaultdict(lambda: defaultdict(float))
for r in rows:
    for m in r['mods']:
        score[m]+=r['w']/len(r['mods']); mtop[m][r['topic']]+=r['w']/len(r['mods'])
LOWFOCUS=re.compile(r'^(Onco:|IBQ: Onco|Pulm:|CCM: (Respiratory|Cardiac|Trauma)|Biostatistics|Geriatric|Pharmacogenomics|Sympt: (Syncope|Cardiorespiratory))')
OVERRIDE={'Heme: WBC':'M'}   # leukaemia/lymphoma lean onco group
def tier(m):
    if m in OVERRIDE: return OVERRIDE[m]
    s=score.get(m,0); b=bank.get(m,0) or 1; dens=100*s/b
    if m.startswith('IBQ'): return 'L' if LOWFOCUS.match(m) else 'M'
    if LOWFOCUS.match(m): return 'L' if s<4 else 'M'
    if s>=6 or (dens>=10 and s>=4): return 'H'
    return 'M'
def clean(t): return re.sub(r'\s*/\s*',' / ',t)
def hint(m):
    seen=[]
    for t,_ in sorted(mtop[m].items(),key=lambda kv:-kv[1]):
        for part in clean(t).split(' / '):
            if part.lower() not in [s.lower() for s in seen]: seen.append(part)
    return ", ".join(seen[:4])
MAIN={m:dict(t=tier(m),pyq=round(score.get(m,0)),hint=hint(m)) for m in bank}

SS_T={ # Super Specialty modules
 'Cardio SS: STEMI':'H','Cardio SS: Angina+NSTEMI+Misc':'H','Cardio SS: Heart Failure':'M',
 'Neuro SS: Stroke':'H','Neuro SS: Epilepsy':'H','Neuro SS: Dementia':'M','Neuro SS: Neurocutaneous':'M','Neuro SS: UMN/LMN & CN':'M',
 'Neuro SS: Headache':'H','Neuro SS: Neuroinfections':'H','Neuro SS: Inflammatory/Demyelinating/Paraneoplastic':'H',
 'Onco SS: Haemat Onco':'M','Onco SS: General Onco':'L',
 'Endo SS: Adrenal':'H','Endo SS: Thyroid':'H','Endo SS: Hypothalamus & Pituitary':'H','Endo SS: Reproductive':'H','Endo SS: Pediatric Endo':'M',
 'GI SS: Liver':'H','GI SS: Pancreas':'H','GI SS: Biliary Tract':'M','GI SS: Stomach & Duodenum':'M','GI SS: Oesophagus':'M','GI SS: Endoscopic Images':'M',
 'GI SS: Small & Large Intestine':'H','GI SS: Signs & Symptoms':'M',
 'ID SS: Clinical Syndrome P1':'H','ID SS: Clinical Syndrome P2':'H',
 'Nephro SS: Fluid/Electrolyte/Acid-Base':'H','Nephro SS: Physiology/AKI/CKD/Dialysis':'M','Nephro SS: Primary Glomerular':'H','Nephro SS: Secondary Glomerular':'H',
 'Nephro SS: AKI':'H','Nephro SS: CKD':'M','Nephro SS: Hemodialysis':'M','Nephro SS: Renal Transplant':'M','Nephro SS: Basic Sciences':'H','Nephro SS: DM & HTN':'M',
 'Rheum SS: CTD':'M','Rheum SS: Arthritis':'H','Rheum SS: Vasculitis':'M','Rheum SS: Autoinflammatory':'M','Rheum SS: IgG4/AOSD/Amyloidosis':'M','Rheum SS: Immunology':'M',
 'Pulm SS: Allergic':'L','Pulm SS: COPD/Pleura/Mediastinum':'L','Pulm SS: Bronchiectasis & ARDS':'L','Pulm SS: Misc':'L',
}
QRP_MAP={1:'Rheum: SLE',2:'GIT: Altered GI Function',3:'GIT: Pancreas/GB/IBD',4:'GIT: Alimentary except IBD',5:'GIT: Liver',6:'GIT: Nutrition',7:'GIT: GI Malignancies',
 8:'Endo: Hypothalamus & Pituitary',9:'Endo: Thyroid',10:'Endo: Adrenal',11:'Endo: Diabetes & Obesity',12:'Endo: Bone & Mineral',13:'ID: Community Acquired',14:'ID: Bacterial',
 15:'ID: Fungal',16:'ID: Viral',17:'ID: Parasites',18:'Renal: AKI',19:'Renal: CKD',20:'Renal: Fluid & Electrolytes',21:'Renal: Glomerular',22:'Renal: Tubulointerstitial',
 23:'CVS: Arrhythmias',24:'Cardio: Heart Failure',25:'Cardio: Valvular incl RHD',26:'Cardio: IHD',27:'Cardio: Misc',28:'Cardio: Pulm HTN',29:'Cardio: DVT & PE',30:'Cardio: Misc',
 31:'Heme: RBC',32:'Heme: WBC',33:'Heme: Platelets',34:'CCM: Misc',35:'CCM: Cardiac Arrest & Shock',36:'CCM: Drugs & Poisoning',37:'CCM: GI Critical Care',38:'CCM: Respiratory CC',
 39:'CCM: Cardiac CC',40:'CCM: Trauma & Obstetrics',41:'IBQ: Rheumatology',42:'IBQ: Onco',43:'IBQ: Endo',44:'IBQ: Nephrology',45:'IBQ: Neurology',46:'IBQ: Cardiology',
 47:'IBQ: General Medicine',48:'Genetics',49:'Onco: Emergencies',50:'Onco: Misc',51:'Onco: Systemic-1',52:'Onco: Pharmacotherapy',53:'Onco: Infections in Cancer',
 54:'Onco: Prevention',55:'Onco: Cancer Genetics',56:'Onco: Cancer Basics',57:'Sympt: Fever/Rash/PUO',58:'Sympt: Skin',59:'Sympt: Cardiorespiratory',60:'Sympt: Neurological',
 61:'Sympt: Syncope',62:'Sympt: Pain',63:'Geriatric Medicine',64:'Environmental disorders',65:'Medical Disorders in Pregnancy',66:'Neuro: Basics',67:'Neuro: Seizures & Epilepsy',
 68:'Neuro: CVA',69:'Neuro: Migraine & Headache',70:'Neuro: Alzheimer & Dementia',71:'Neuro: Movement Disorders',72:'Neuro: ALS & MND',73:'Neuro: ANS',74:'Neuro: Cranial nerves',
 75:'Neuro: Spinal Cord',76:'Neuro: Neuroinfections',77:'Neuro: Trauma/Demyelinating/CFS/Psych',78:'Neuro: Nerve & Muscle',79:'Pulm: Infections/Pneumonia/Abscess',
 80:'CCM: Respiratory CC',81:'Pulm: COPD & ILD',82:'Pulm: Misc (mediastinum/OSA/ventilation)'}
QRP_T={k:MAIN[v]['t'] for k,v in QRP_MAP.items()}
QRP_T[1]='H'  # QRP Rheumatology covers the whole subject
# Subject checklist for the PYQ tab
subj=defaultdict(float); sneet=Counter(); sini=Counter(); tw=defaultdict(lambda: defaultdict(float)); tn=defaultdict(Counter); ti=defaultdict(Counter); subs=defaultdict(list)
for r in rows:
    s=r['subj']; subj[s]+=r['w']; t=clean(r['topic'])
    tw[s][t]+=r['w']; (tn if r['w']==1 else ti)[s][t]+=1; (sneet if r['w']==1 else sini)[s]+=1
    if r['sub'] and len(subs[(s,t)])<3: subs[(s,t)].append(r['sub'])
SYSK={'Gastroenterology & Hepatology':'gi','Infectious Diseases':'id','Endocrinology':'endo','Neurology':'neuro','Cardiology':'cardio','Nephrology':'nephro',
 'Rheumatology & Immunology':'rheum','Environmental Medicine & Toxicology':'cc','Hematology':'onco','Oncology':'onco','Critical Care':'cc','Genetics':'misc','Pulmonology':'pulm','Statistics':'misc'}
LOWS={'Oncology','Critical Care','Pulmonology','Statistics'}
checklist=[]
for s,v in sorted(subj.items(),key=lambda kv:-kv[1]):
    tops=[t for t,w in sorted(tw[s].items(),key=lambda kv:-kv[1]) if w>=1.5][:12] or [t for t,_ in sorted(tw[s].items(),key=lambda kv:-kv[1])][:4]
    checklist.append(dict(subj=s,sys=SYSK[s],low=s in LOWS,pct=round(100*v/sum(subj.values()),1),neet=sneet[s],ini=sini[s],
      topics=[dict(id=f"hy:{s}|{t}",t=t,neet=tn[s][t],ini=ti[s][t],eg=[x[:70] for x in subs[(s,t)][:2]]) for t in tops]))
json.dump(dict(main=MAIN,ss=SS_T,qrp=QRP_T,checklist=checklist),open('hy/hy.json','w'))
if __name__=='__main__':
    c=Counter(v['t'] for v in MAIN.values()); print('main tiers',c, {t:sum(bank[m] for m in MAIN if MAIN[m]['t']==t) for t in 'HML'})
    print('qrp tiers',Counter(QRP_T.values()))
    for c in checklist: print(f"{c['subj'][:26]:26} {c['pct']:5}%  topics {len(c['topics'])}  low={c['low']}")
