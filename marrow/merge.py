import json, datetime as dt
S=json.load(open('hy/schedule2.json'))
MP=json.load(open('marrow/mplan.json'))
when={}
for ph,key in (('phase1','p1'),('phase2','p2')):
    for d in S[ph]:
        items=MP['plan'].get(f"{key}:{d['n']}",[])
        d['items']=d['items']+items
        lab=("Day " if key=='p1' else "Rev ")+str(d['n'])+" · "+dt.date.fromisoformat(d['date']).strftime("%a %-d %b")
        for i in items: when[i['id']]=lab
order=[]
bysubj={}
for m in MP['modules']:
    s=bysubj.setdefault(m['subj'],dict(subj=m['subj'],sys=m['sys'],items=[]))
    parts=[(pid,w) for pid,w in when.items() if pid==m['id'] or pid.startswith(m['id']+'#')]
    for ph in ('phase1','phase2'):
        for d in S[ph]:
            for i in d['items']:
                if i['k']=='mar' and (i['id']==m['id'] or i['id'].startswith(m['id']+'#')):
                    s['items'].append(dict(id=i['id'],k='mar',t=i['t'],q=i['q'],tier=i['tier'],subj=m['subj'],when=when[i['id']]))
    if m['left']:
        s['items'].append(dict(id=m['id'] if m['left']==m['q'] else m['id']+'#spare',k='mar',t=m['t'],q=m['left'],tier=m['tier'],subj=m['subj'],when='Spare time'))
S['marrow']=list(bysubj.values())
tot=sum(i['q'] for s in S['marrow'] for i in s['items']); sch=sum(i['q'] for s in S['marrow'] for i in s['items'] if i['when']!='Spare time')
ids=[i['id'] for d in S['phase1']+S['phase2'] for i in d['items']]
print('marrow total',tot,'scheduled',sch,'ids unique',len(ids)==len(set(ids)))
json.dump(S,open('marrow/schedule3.json','w'),separators=(",",":"))
