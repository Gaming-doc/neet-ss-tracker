import json, plan as P, final as F
from data import main, ss, qrp, qrp_recall_by_day
SS = F.SS
SS[28]=[x for x in SS[28] if not x[0].startswith(("Rheum SS: Immunology","Pulm SS: COPD"))]
if not any(n.startswith("Rheum SS: Immunology") for n,_ in SS[6]): SS[6].append(("Rheum SS: Immunology",18))
SS[27]=[x if not x[0].startswith("Pulm SS: COPD") else ("Pulm SS: COPD/Pleura/Mediastinum",40) for x in SS[27]]

titles = {1:("Cardiology I","cardio"),2:("Cardiology II","cardio"),3:("Neurology I","neuro"),4:("Neurology II","neuro"),5:("Neurology III","neuro"),
6:("Neurology IV","neuro"),7:("Hematology","onco"),8:("Oncology I","onco"),9:("Oncology II","onco"),10:("Endocrine I","endo"),11:("Endocrine II","endo"),
12:("Endo III & Metabolism","endo"),13:("GI & Liver I","gi"),14:("GI II","gi"),15:("GI III & ID I","gi"),16:("Infectious II","id"),17:("ID III & Toxicology","id"),
18:("Critical Care","cc"),19:("Nephrology I","nephro"),20:("Nephrology II","nephro"),21:("Nephro III & SLE","nephro"),22:("Rheumatology II","rheum"),
23:("Rheumatology III","rheum"),24:("Pulmonology I","pulm"),25:("Pulmonology II","pulm"),26:("Biostats & Geriatrics","misc"),27:("Genetics & Pregnancy","misc"),28:("Gen Med IBQ & Symptoms","misc")}
PYQ = {9:"2022",17:"2023",24:"2024"}
def blk(cum): return "A" if cum < 58 else ("B" if cum < 120 else "C")
days=[]
for d in range(1,29):
    items=[]
    if d==1: mods=main[1]
    elif d==2: mods=[("CVS: Heart failure",58),("Cardio: Pulm HTN",47),("Cardio: Myocarditis & CMP",27),("Cardio: DVT & PE",51),("CVS: Arrhythmias",14)]
    else:
        mods=P.ordered_main(d)
        if d==3: mods=sorted(mods,key=lambda m:(m[0]!="Neuro: Basics",))
    cum=0
    for n,c in mods:
        items.append(dict(id=f"m:{n}",k="main",t=n,q=c,b=blk(cum) if d>2 else "A")); cum+=c
    if d in PYQ:
        items.append(dict(id=f"pyq1:{PYQ[d]}",k="pyq",t=f"NEET SS {PYQ[d]} PYQ paper — timed, then tag green ★",q=150,b="S"))
    for n,c in SS[d]:
        items.append(dict(id=f"s{d}:{n}",k="ss",t=n,q=c,b="S"))
    for k in qrp_recall_by_day[d]:
        items.append(dict(id=f"q1:{k}",k="qrp",t=f"QRP #{k} {qrp[k][0]}",q=qrp[k][1],b="Q"))
    t,s=titles[d]
    days.append(dict(n=d,date=str(P.date(d)),title=t,sys=s,items=items,pyq=d in PYQ,buffer=d==12))
# Phase 2
rev = [
 (1,"2026-11-27","PYQ 2025 + Cardiology","cardio",[("pyq2:2025","NEET SS 2025 PYQ — 09:00 exam conditions + audit",150,"pyq")],"Cardiology",[28,25,23,24,26,27,29,30]),
 (2,"2026-11-28","Neurology I","neuro",[],"Neurology",[66,68,74,75,73,67,71,70,60]),
 (3,"2026-11-29","Mock 1 + Neurology II","neuro",[("mock:1","Grand Mock #1 — 09:00–11:30 + 90-min audit",150,"pyq")],"Neuromuscular",[78,72,77,76,69]),
 (4,"2026-11-30","Heme + Oncology","onco",[],"Heme + Onco",[33,31,52,55,51,49,53,32,50,54,56]),
 (5,"2026-12-01","Endo, Metabolism, Genetics","endo",[],"Endo + Metabolism + Genetics",[8,10,12,9,11,48,6]),
 (6,"2026-12-02","Mock 2 + GI","gi",[("mock:2","Grand Mock #2 — 09:00–11:30 + 90-min audit",150,"pyq")],"GI + Hepatology",[5,3,4,7,2]),
 (7,"2026-12-03","ID, PUO, Toxicology","id",[],"ID + Toxicology",[16,14,15,13,17,36,57,58,64]),
 (8,"2026-12-04","Nephrology","nephro",[],"Nephro (acid-base first)",[20,21,18,19,22,35,39]),
 (9,"2026-12-05","Mock 3 + Rheumatology","rheum",[("mock:3","Grand Mock #3 — 09:00–11:30 + 90-min audit",150,"pyq")],"Rheum (flagged CTD/vasculitis SS)",[1,63,65,62]),
 (10,"2026-12-06","Pulm + Critical Care","pulm",[],"Pulm + Critical Care",[81,79,80,82,34,38,37,40,59,61]),
 (11,"2026-12-07","Mock 4 + PYQ re-solve","misc",[("mock:4","Grand Mock #4 (last new test) + audit",150,"pyq"),("re:2022","Rapid re-solve NEET SS 2022",150,"pyq"),("re:2023","Rapid re-solve NEET SS 2023",150,"pyq"),("t:biostat","Biostat 2×2 formulas drill",0,"task")],None,[]),
 (12,"2026-12-08","PYQ re-solve + Image spotters","misc",[("re:2024","Rapid re-solve NEET SS 2024",150,"pyq"),("re:2025","Rapid re-solve NEET SS 2025",150,"pyq")],None,[41,42,43,44,45,46,47]),
 (13,"2026-12-09","Final flip","misc",[("t:mockwrong","Re-solve only wrong Qs from Mocks 1–4",0,"task"),("t:flip","Green ★ PYQ + orange cutoff flip, all subjects",0,"task"),("t:sleep13","Lights out 22:30",0,"task")],None,[]),
 (14,"2026-12-10","Rest day","misc",[("t:sheet","Write 1-page cutoff & formula sheet",0,"task"),("t:stop","Stop all study by 16:00",0,"task"),("t:admit","Check admit card, centre route, ID",0,"task"),("t:sleep14","Lights out 22:00",0,"task")],None,[]),
]
rdays=[]
for n,date,title,sys,tasks,eb,qs in rev:
    items=[dict(id=i,k=k,t=t,q=q,b="A") for i,t,q,k in tasks]
    if eb: items.insert(0 if not tasks else 1, dict(id=f"eb:{n}",k="task",t=f"Error bank: re-solve your wrong/bookmarked {eb} Qs",q=0,b="A"))
    for k in qs: items.append(dict(id=f"q2:{k}",k="qrp",t=f"QRP #{k} {qrp[k][0]}",q=qrp[k][1],b="B"))
    if n<=10: items.append(dict(id=f"flip:{n}",k="task",t="iPad Harrison flip + red ★ SS notes for this system",q=0,b="C"))
    rdays.append(dict(n=n,date=date,title=title,sys=sys,items=items))
data=dict(phase1=days,phase2=rdays)
# checks
m=sum(i["q"] for d in days for i in d["items"] if i["k"]=="main")
s=sum(i["q"] for d in days for i in d["items"] if i["k"]=="ss")
q1=sum(i["q"] for d in days for i in d["items"] if i["k"]=="qrp")
q2=sum(i["q"] for d in rdays for i in d["items"] if i["id"].startswith("q2:"))
ids=[i["id"] for d in days+rdays for i in d["items"]]
print(m+53,s,q1,q2,len(ids),len(set(ids)))
json.dump(data,open("schedule.json","w"),separators=(",",":"))
