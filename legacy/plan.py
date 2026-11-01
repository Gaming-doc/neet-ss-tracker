from data import main, ss, qrp, qrp_recall_by_day
import datetime as dt

START = dt.date(2026, 10, 30)
def date(d): return START + dt.timedelta(days=d - 1)

# Difficulty tier: 3 = tough (Block A, fresh brain), 2 = medium, 1 = light/visual (IBQ, symptoms, misc)
tier = {
 "Neuro: Basics":3,"Neuro: CVA":3,"Neuro: Cranial nerves":3,"Neuro: Seizures & Epilepsy":2,"Neuro: ANS":2,"IBQ: Cardiology":1,
 "Neuro: Spinal Cord":3,"Neuro: Movement Disorders":3,"Neuro: Alzheimer & Dementia":2,
 "Neuro: Nerve & Muscle P1 (Q1-70)":3,"Neuro: ALS & MND":2,"Neuro: Migraine & Headache":1,
 "Neuro: Nerve & Muscle P2 (Q71-100)":3,"Neuro: Trauma/Demyelinating/CFS/Psych":2,"Neuro: Neuroinfections":2,"IBQ: Neurology":1,
 "Heme: Platelets":3,"Heme: RBC":3,"Heme: WBC":2,"Onco: Cancer Basics":1,"Onco: Prevention":1,
 "Onco: Pharmacotherapy":3,"Onco: Systemic-2":2,"Onco: Emergencies":2,
 "Onco: Cancer Genetics":3,"Onco: Systemic-1":2,"Onco: Infections in Cancer":2,"Onco: Misc":1,"IBQ: Onco P1 (Q1-60)":1,
 "Endo: Adrenal":3,"Endo: Bone & Mineral P1 (Q1-30)":3,"Endo: Thyroid":2,"IBQ: Onco P2 (Q61-120)":1,
 "Endo: Hypothalamus & Pituitary":3,"Endo: DSD & Sexual Disorders":3,"Endo: Bone & Mineral P2 (Q31-50)":3,"Endo: Diabetes & Obesity P1 (Q1-40)":2,
 "Metabolism":3,"Endo: Diabetes & Obesity P2 (Q41-69)":2,"IBQ: Endo P1 (Q1-60)":1,
 "GIT: Liver":3,"GIT: Pancreas/GB/IBD":2,"IBQ: Endo P2 (Q61-117)":1,
 "GIT: Alimentary except IBD":3,"GIT: GI Malignancies":2,"CCM: GI Critical Care":2,"GIT: Altered GI Function P1 (Q1-20)":2,
 "ID: Fungal":3,"ID: Community Acquired P1 (Q1-65)":2,"GIT: Altered GI Function P2 (Q21-60)":2,"GIT: Nutrition":1,
 "ID: Viral":3.5,"ID: Bacterial":3,"ID: Community Acquired P2 (Q66-80)":2,
 "CCM: Drugs & Poisoning":3,"ID: Parasites":2,"Sympt: Fever/Rash/PUO":2,"Sympt: Skin":1,
 "CCM: Cardiac Arrest & Shock":3,"CCM: Cardiac CC":2,"CCM: Misc":2,"Environmental disorders":1,
 "Renal: Fluid & Electrolytes":3.5,"Renal: Glomerular":3,"Renal: AKI":2,
 "Renal: Physiology":3.5,"Renal: Tubulointerstitial":3.4,"Renal: PCKD & Inherited":3,"Renal: CKD":2,"Renal: Vascular":2,"Renal: Dialysis & Transplant":2,
 "Rheum: SLE P1 (Q1-50)":3,"Renal: Nephrolithiasis":2,"IBQ: Nephrology":1,
 "Rheum: SLE P2 (Q51-68)":3.5,"Rheum: APLA/SS/Sjogren":3,"Rheum: Behcet & Myopathies":3,"Rheum: RA":2,"Rheum: SpA":2,
 "Rheum: Vasculitis":3,"Rheum: Gout/Sarcoid":2,"Rheum: Articular & MSK":2,"Rheum: Misc":1.5,"IBQ: Rheumatology":1,
 "Pulm: Diagnosis":3.5,"Pulm: COPD & ILD":3,"Pulm: Asthma/HP/Eosinophilic":2,"Pulm: Infections/Pneumonia/Abscess":2,
 "Pulm: Misc (mediastinum/OSA/ventilation)":3,"CCM: Respiratory CC":3,"Pulm: Bronchiectasis/CF/Pleura":2,"Sympt: Syncope":1,"Sympt: Cardiorespiratory":1,
 "Biostatistics":3,"Geriatric Medicine":1,
 "Genetics":3,"Medical Disorders in Pregnancy":2,"CCM: Trauma & Obstetrics":2,"Immunology":1,
 "Pharmacogenomics":3,"Sympt: Neurological":2,"Sympt: Pain":1,"IBQ: General Medicine":1,
}

PYQ_DAYS = {10: "NEET SS 2022", 17: "NEET SS 2023", 24: "NEET SS 2024"}

for _k in list(tier):
    if _k.startswith("IBQ"): tier[_k]=0.9

def ordered_main(d):
    mods = main[d]
    if d <= 2: return mods
    return sorted(mods, key=lambda m: (-tier[m[0]], -m[1]))

def blocks(d):
    """Split ordered modules into Block A/B/C by cumulative start position (A~58, B~62, rest C)."""
    out = {"A": [], "B": [], "C": []}
    cum = 0
    for name, n in ordered_main(d):
        b = "A" if cum < 58 else ("B" if cum < 120 else "C")
        out[b].append((name, n)); cum += n
    return out

# ---- SS queue: same module order as original, gated by organ start day, smoothed cap ----
avail = {"Cardio":1,"Neuro":3,"Onco SS: Haemat":7,"Onco SS: General":8,"Endo":10,"GI":13,"ID":15,"Nephro":19,"Rheum":21,"Pulm":24}
def avail_day(name):
    for k, v in avail.items():
        if name.startswith(k) or name.startswith(k.split(":")[0] + " SS") and k in ("Cardio","Neuro","Endo","GI","ID","Nephro","Rheum","Pulm"):
            if name.startswith(k): return v
    if name.startswith("Onco SS: Haemat"): return 7
    if name.startswith("Onco SS: General"): return 8
    raise ValueError(name)

# Build whole SS modules (merge Part splits back) in original order
import re
whole = []
for d in range(1, 29):
    for name, n in ss[d]:
        base = re.sub(r" P\d \(Q\d+-\d+\)", "", name)
        if whole and whole[-1][0] == base: whole[-1][1] += n
        else: whole.append([base, n])
# sanity: original ordering may interleave parts of same module (Vasculitis P1/P2 across days) -> merged
merged = {}
order = []
for b, n in whole:
    if b not in merged: merged[b] = 0; order.append(b)
    merged[b] += n

def ss_plan(cap, last_day=27):
    plan = {d: [] for d in range(1, 29)}
    # days 1-2 already done / in progress as original
    plan[1] = ss[1]; plan[2] = ss[2]
    queue = [[b, merged[b], 0] for b in order if not b.startswith("Cardio")]  # name, total, done
    for d in range(3, last_day + 1):
        room = 0 if d in PYQ_DAYS else cap
        for item in queue:
            if room <= 0: break
            b, tot, done = item
            if done >= tot: continue
            if avail_day(b) > d: break  # keep order strict
            take = min(tot - done, room)
            # avoid tiny leftovers (<12): take them now if within +12
            if 0 < tot - done - take < 12: take = tot - done
            if take == tot and done == 0: label = b
            else: label = f"{b} (Q{done+1}-{done+take})"
            plan[d].append((label, take)); item[2] += take; room -= take
    left = sum(t - dn for _, t, dn in queue)
    return plan, left

if __name__ == "__main__":
    for cap in (120, 125, 130, 135, 140):
        p, left = ss_plan(cap)
        print(cap, "left", left, [sum(n for _, n in p[d]) for d in range(1, 29)])

def ss_plan2(cap, pyq_days, last_day=28, avail_override=None):
    global avail
    plan = {d: [] for d in range(1, 29)}
    plan[1] = ss[1]; plan[2] = ss[2]
    queue = [[b, merged[b], 0] for b in order if not b.startswith("Cardio")]
    for d in range(3, last_day + 1):
        room = 0 if d in pyq_days else cap
        for item in queue:
            if room <= 0: break
            b, tot, done = item
            if done >= tot or avail_day(b) > d: continue
            take = min(tot - done, room)
            if 0 < tot - done - take < 12: take = tot - done
            label = b if (take == tot and done == 0) else f"{b} (Q{done+1}-{done+take})"
            plan[d].append((label, take)); item[2] += take; room -= take
    return plan, sum(t - dn for _, t, dn in queue)
