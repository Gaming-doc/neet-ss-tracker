import sys, re, json
sys.path.insert(0,'.')
from data import qrp
import plan as P
HY=json.load(open('hy/hy.json'))
S=json.load(open('schedule.json'))
RANK={'H':0,'M':1,'L':2}
def canon(n): return re.sub(r" P\d \(Q\d+-\d+\)","",n)
def sscanon(n): return re.sub(r" \(Q\d+–\d+\)","",n)
def diff(n): return P.tier.get(n,0.9 if n.startswith('IBQ') else 2)
def blk(c): return "A" if c<58 else ("B" if c<120 else "C")
for d in S['phase1']:
    main=[i for i in d['items'] if i['k']=='main']; rest=[i for i in d['items'] if i['k']!='main']
    for i in main:
        h=HY['main'][canon(i['t'])]; i.update(tier=h['t'],pyq=h['pyq'],hint=h['hint'])
    if d['n']>=3:
        main.sort(key=lambda i:(RANK[i['tier']],-diff(i['t']),-i['q']))
        cum=0
        for i in main: i['b']=blk(cum); cum+=i['q']
    for i in rest:
        if i['k']=='ss': i['tier']=HY['ss'][sscanon(i['t'])]
        if i['k']=='qrp': i['tier']=HY['qrp'][i['id'].split(':')[1]]
    ss=sorted([i for i in rest if i['k']=='ss'],key=lambda i:RANK[i['tier']])
    qq=sorted([i for i in rest if i['k']=='qrp'],key=lambda i:RANK[i['tier']])
    other=[i for i in rest if i['k'] not in('ss','qrp')]
    d['items']=main+other+ss+qq
    d['light']=all(i.get('tier')=='L' for i in main) if main else False
SWEEP={1:'Cardiology',2:'Neurology',3:'Neurology',4:'Hematology',5:'Endocrinology + Genetics',6:'Gastroenterology & Hepatology',7:'Infectious Diseases',8:'Nephrology',9:'Rheumatology & Immunology',10:'Environmental Medicine & Toxicology'}
rev = [
 (1,"2026-11-27","PYQ 2025 + Cardiology","cardio",[("pyq2:2025","NEET SS 2025 PYQ — 09:00 exam conditions + audit",150,"pyq")],"Cardiology",[28,25,23,24,26,27,29,30]),
 (2,"2026-11-28","Neurology I","neuro",[],"Neurology",[66,68,74,75,73,67,71,70,60]),
 (3,"2026-11-29","Mock 1 + Neurology II","neuro",[("mock:1","Grand Mock #1 — 09:00–11:30 + 90-min audit",150,"pyq")],"Neuromuscular",[78,72,77,76,69]),
 (4,"2026-11-30","Heme + Onco (light)","onco",[],"Haematology",[33,31,52,55,51,49,53,32,50,54,56]),
 (5,"2026-12-01","Endo, Metabolism, Genetics","endo",[],"Endo + Metabolism + Genetics",[8,10,12,9,11,48,6]),
 (6,"2026-12-02","Mock 2 + GI","gi",[("mock:2","Grand Mock #2 — 09:00–11:30 + 90-min audit",150,"pyq")],"GI + Hepatology",[5,3,4,7,2]),
 (7,"2026-12-03","ID + PUO","id",[],"Infectious Diseases",[16,14,15,13,17,57,58]),
 (8,"2026-12-04","Nephrology","nephro",[],"Nephro (acid-base first)",[20,21,18,19,22,35,39]),
 (9,"2026-12-05","Mock 3 + Rheumatology","rheum",[("mock:3","Grand Mock #3 — 09:00–11:30 + 90-min audit",150,"pyq")],"Rheum (flagged CTD/vasculitis SS)",[1,63,65,62]),
 (10,"2026-12-06","Toxicology + Pulm/CC (light)","cc",[],"Toxicology & environment",[36,64,81,79,80,82,34,38,37,40,59,61]),
 (11,"2026-12-07","Mock 4 + PYQ re-solve","misc",[("mock:4","Grand Mock #4 (last new test) + audit",150,"pyq"),("re:2022","Rapid re-solve NEET SS 2022",150,"pyq"),("re:2023","Rapid re-solve NEET SS 2023",150,"pyq"),("t:biostat","Biostat 2×2 formulas drill (1 PYQ so far — keep it short)",0,"task")],None,[]),
 (12,"2026-12-08","PYQ re-solve + Image spotters","misc",[("re:2024","Rapid re-solve NEET SS 2024",150,"pyq"),("re:2025","Rapid re-solve NEET SS 2025",150,"pyq")],None,[41,42,43,44,45,46,47]),
 (13,"2026-12-09","Final flip","misc",[("t:mockwrong","Re-solve only wrong Qs from Mocks 1–4",0,"task"),("t:hyflip","Flip every PYQ high-yield topic you ticked",0,"task"),("t:flip","Green ★ PYQ + orange cutoff flip, all subjects",0,"task"),("t:sleep13","Lights out 22:30",0,"task")],None,[]),
 (14,"2026-12-10","Rest day","misc",[("t:sheet","Write 1-page cutoff & formula sheet",0,"task"),("t:stop","Stop all study by 16:00",0,"task"),("t:admit","Check admit card, centre route, ID",0,"task"),("t:sleep14","Lights out 22:00",0,"task")],None,[]),
]
rdays=[]
for n,date,title,sys_,tasks,eb,qs in rev:
    items=[dict(id=i,k=k,t=t,q=q,b="A") for i,t,q,k in tasks]
    if eb: items.insert(0 if not tasks else 1, dict(id=f"eb:{n}",k="task",t=f"Error bank: re-solve your wrong/bookmarked {eb} Qs",q=0,b="A"))
    ql=sorted(qs,key=lambda k:RANK[HY['qrp'][str(k)]])
    for k in ql: items.append(dict(id=f"q2:{k}",k="qrp",t=f"QRP #{k} {qrp[k][0]}",q=qrp[k][1],b="B",tier=HY['qrp'][str(k)]))
    if n in SWEEP: items.append(dict(id=f"hyt:{n}",k="task",t=f"PYQ topic sweep: {SWEEP[n]} (PYQ tab)",q=0,b="C"))
    if n<=10: items.append(dict(id=f"flip:{n}",k="task",t="iPad Harrison flip + red ★ SS notes for this system",q=0,b="C"))
    rdays.append(dict(n=n,date=date,title=title,sys=sys_,items=items))
S['phase2']=rdays
S['hy']=HY['checklist']
m=sum(i["q"] for d in S['phase1'] for i in d["items"] if i["k"]=="main")
s=sum(i["q"] for d in S['phase1'] for i in d["items"] if i["k"]=="ss")
q1=sum(i["q"] for d in S['phase1'] for i in d["items"] if i["k"]=="qrp")
q2=sum(i["q"] for d in rdays for i in d["items"] if i["id"].startswith("q2:"))
ids=[i["id"] for d in S['phase1']+rdays for i in d["items"]]
print(m+53,s,q1,q2,len(ids),len(set(ids)))
for d in S['phase1'][2:]:
    print(d['n'],'LIGHT' if d['light'] else '', ' > '.join(f"{i['tier']}:{i['t'][:24]}" for i in d['items'] if i['k']=='main'))
json.dump(S,open('hy/schedule2.json','w'),separators=(",",":"))
