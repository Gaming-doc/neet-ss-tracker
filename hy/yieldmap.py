import re, openpyxl
XLSX='pyq/map.xlsx'
def weight(mod):
    m=mod.lower()
    if any(k in m for k in ['respiratory medicine group','medical oncology group','oncology group','critical care group','onc 38']): return 0
    return 0.5 if 'ini' in m else 1

# Topic-label rules that apply whatever subject the question was filed under.
GLOBAL = [
 (r'envenom|high-altitude|cold injury|heat illness|marine toxin|occupational toxicology|drowning', 'Environmental disorders'),
 (r'toxicolog|poisoning|toxic alcohol', 'CCM: Drugs & Poisoning'),
 (r'palliative', 'Sympt: Pain'),
 (r'biostat', 'Biostatistics'),
 (r'geriatric|delirium', 'Geriatric Medicine'),
 (r'contraception|in pregnancy|pregnancy liver|adrenal / pregnancy|haemolytic disease of newborn', 'Medical Disorders in Pregnancy'),
 (r'chromosom|inheritance|imprinting|ciliopath|premature ageing|overgrowth|dysmorpholog|genetic principles|genetic counselling|skeletal / metabolic genetics|inborn error', 'Genetics'),
 (r'primary immunodeficiency|innate immunity|autoimmune serology', 'Immunology'),
 (r'resuscitation', 'CCM: Cardiac Arrest & Shock'),
 (r'ecmo|mechanical ventilation', 'CCM: Respiratory CC'),
 (r'severity scoring|nutrition in critical|critical care neuromuscular', 'CCM: Misc'),
 (r'cardiovascular emergenc|paediatric emergenc', 'CCM: Cardiac CC'),
 (r'endocrine emergenc', 'Endo: Thyroid'),
 (r'febrile neutropenia', 'Onco: Infections in Cancer'),
]
S = {
 'Cardiology': [
  (r'valv|endocarditis|rheumatic|congenital|genetics/congenital', ['Cardio: Valvular incl RHD']),
  (r'ischemic|ischaemic|cardiac imaging|peri-operative', ['Cardio: IHD','CVS: IHD']),
  (r'ecg|arrhythm|conduction|channelopath|devices|pacing|pharmacology', ['CVS: Arrhythmias']),
  (r'cardiomyopath|cardio-oncology|myocarditis', ['Cardio: Myocarditis & CMP']),
  (r'heart failure', ['Cardio: Heart Failure','CVS: Heart failure']),
  (r'pulmonary hypertension', ['Cardio: Pulm HTN']),
  (r'pulmonary embol', ['Cardio: DVT & PE']),
  (r'.', ['Cardio: Misc'])],
 'Neurology': [
  (r'stroke|vascular malformation|hemorrhage', ['Neuro: CVA']),
  (r'demyelinat|paraneoplastic|psycho-oncology|neuro-oncology', ['Neuro: Trauma/Demyelinating/CFS/Psych']),
  (r'movement', ['Neuro: Movement Disorders']),
  (r'dementia|neurodegenerat', ['Neuro: Alzheimer & Dementia']),
  (r'neuro-infect', ['Neuro: Neuroinfections']),
  (r'motor neuron', ['Neuro: ALS & MND']),
  (r'neuromuscular|neuropathy', ['Neuro: Nerve & Muscle']),
  (r'headache|facial pain', ['Neuro: Migraine & Headache']),
  (r'epilep|neurocutaneous', ['Neuro: Seizures & Epilepsy']),
  (r'spinal|spine', ['Neuro: Spinal Cord']),
  (r'cranial nerve|brainstem|neuro-ophthal', ['Neuro: Cranial nerves']),
  (r'.', ['Neuro: Basics'])],
 'Hematology': [
  (r'thrombotic microangio|thrombocytopenia|myeloproliferative|mastocytosis', ['Heme: Platelets']),
  (r'lymphoma|plasma cell|transplant monitoring', ['Heme: WBC']),
  (r'.', ['Heme: RBC'])],
 'Oncology': [
  (r'lymphoma|leukaem|haematological malignancy|transplant oncology', ['Heme: WBC']),
  (r'cancer genetics', ['Onco: Cancer Genetics']),
  (r'oncologic emergenc', ['Onco: Emergencies']),
  (r'.', ['Onco: Misc'])],
 'Endocrinology': [
  (r'disorders of sex|male reproductive|reproductive endocrine', ['Endo: DSD & Sexual Disorders']),
  (r'adrenal', ['Endo: Adrenal']),
  (r'thyroid|men syndrome', ['Endo: Thyroid']),
  (r'diabetes|hypoglyc|insulin resist|lipodystroph|obesity|metabolic syndrome', ['Endo: Diabetes & Obesity']),
  (r'calcium|bone', ['Endo: Bone & Mineral']),
  (r'pituitary|growth|pediatric endocrine|genetic endocrine|endocrine physiology|endocrine investigation', ['Endo: Hypothalamus & Pituitary']),
  (r'.', ['Metabolism'])],
 'Gastroenterology & Hepatology': [
  (r'malabsorption|celiac|coeliac', ['GIT: Altered GI Function']),
  (r'nutrition', ['GIT: Nutrition']),
  (r'pancrea|biliary|gallbladder|ibd', ['GIT: Pancreas/GB/IBD']),
  (r'hepatocellular|gi oncology|neuroendocrine', ['GIT: GI Malignancies']),
  (r'liver|hepat|cirrho|portal|alcoh', ['GIT: Liver']),
  (r'.', ['GIT: Alimentary except IBD'])],
 'Infectious Diseases': [
  (r'viral|hiv|hepatitis|rabies|antiviral|congenital infection|pml', ['ID: Viral']),
  (r'fung', ['ID: Fungal']),
  (r'parasit|malaria|tropical', ['ID: Parasites']),
  (r'clinical signs|dermatology infection', ['Sympt: Fever/Rash/PUO']),
  (r'pneumonia|vaccin|cns infection|transplant infection|reactive arthritis|infectious gi|urinary', ['ID: Community Acquired']),
  (r'.', ['ID: Bacterial'])],
 'Nephrology': [
  (r'glomerul|diabetic nephropathy|vasculitis|complement', ['Renal: Glomerular']),
  (r'tubular|interstitial nephritis', ['Renal: Tubulointerstitial']),
  (r'fluid|acid-base', ['Renal: Fluid & Electrolytes']),
  (r'cystic|genetic', ['Renal: PCKD & Inherited']),
  (r'aki|acute kidney|contrast|hepatorenal|cardiorenal', ['Renal: AKI']),
  (r'dialysis|transplant', ['Renal: Dialysis & Transplant']),
  (r'nephrolith', ['Renal: Nephrolithiasis']),
  (r'hypertension', ['Renal: Vascular']),
  (r'ckd|mbd', ['Renal: CKD']),
  (r'.', ['Renal: Physiology'])],
 'Rheumatology & Immunology': [
  (r'vasculitis', ['Rheum: Vasculitis']),
  (r'rheumatoid', ['Rheum: RA']),
  (r'spondylo|reactive arthritis', ['Rheum: SpA']),
  (r'sle', ['Rheum: SLE']),
  (r'systemic sclerosis|antiphospholipid', ['Rheum: APLA/SS/Sjogren']),
  (r'dermatomyositis', ['Rheum: Behcet & Myopathies']),
  (r'gout', ['Rheum: Gout/Sarcoid']),
  (r'soft-tissue|fibromyalgia|joint disease|still disease|igg4', ['Rheum: Articular & MSK']),
  (r'.', ['Rheum: Misc'])],
 'Pulmonology': [
  (r'interstitial|occupational|copd', ['Pulm: COPD & ILD']),
  (r'asthma', ['Pulm: Asthma/HP/Eosinophilic']),
  (r'cf', ['Pulm: Bronchiectasis/CF/Pleura']),
  (r'pulmonary hypertension', ['Cardio: Pulm HTN']),
  (r'acid-base', ['Renal: Fluid & Electrolytes']),
  (r'.', ['Pulm: Misc (mediastinum/OSA/ventilation)'])],
 'Critical Care': [(r'.', ['CCM: Misc'])],
 'Genetics': [(r'.', ['Genetics'])],
 'Environmental Medicine & Toxicology': [(r'.', ['CCM: Drugs & Poisoning'])],
 'Statistics': [(r'.', ['Biostatistics'])],
}
# cross-subject topic labels like "Rheumatology", "Pulmonology" inside another subject
CROSS = {'rheumatology':'Rheumatology & Immunology','pulmonology':'Pulmonology','nephrology':'Nephrology','oncology':'Oncology','hepatology':'Gastroenterology & Hepatology'}

def route(subj, topic):
    t=topic.lower()
    for p,m in GLOBAL:
        if re.search(p,t): return [m]
    for k,s2 in CROSS.items():
        if t.startswith(k) and s2!=subj:
            subj=s2; t=t[len(k):]
    for p,m in S[subj]:
        if p!='.' and re.search(p,t): return m
    return S[subj][-1][1]

def load():
    wb=openpyxl.load_workbook(XLSX,data_only=True)
    out=[]
    for s,mod,y,q,t,st,qt,fl in wb['Questions'].iter_rows(min_row=2,values_only=True):
        if not s: continue
        w=weight(mod)
        if not w: continue
        out.append(dict(subj=s,topic=t,sub=st,year=y,w=w,mods=route(s,t),src=mod))
    return out
