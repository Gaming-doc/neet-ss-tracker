import json, re, sys
sys.path.insert(0,'hy')
S=json.load(open('marrow/schedule3.json'))
src=open('hy/hybuild.py').read()
QRP_MAP=eval(re.search(r"QRP_MAP=(\{.*?\})\n", src, re.S).group(1))
canon=lambda n: re.sub(r" P\d \(Q\d+-\d+\)","",n)
modsys={}
for d in S['phase1']:
    for i in d['items']:
        if i['k']=='main': modsys.setdefault(canon(i['t']), d['sys'])
MARSYS={'heme':'onco','tox':'cc'}
marsys={}
for s in S['marrow']:
    for i in s['items']: marsys[i['id']]=MARSYS.get(s['sys'],s['sys'])
miss=set()
for ph in ('phase1','phase2'):
    for d in S[ph]:
        for i in d['items']:
            if i['k']=='qrp':
                m=QRP_MAP[int(i['id'].split(':')[1])]; i['sys']=modsys.get(m) or (miss.add(m) or d['sys'])
            elif i['k']=='mar': i['sys']=marsys[i['id']]
            else: i['sys']=d['sys']
for s in S['marrow']:
    for i in s['items']: i['sys']=marsys[i['id']]
print('unmapped QRP modules:',miss)
json.dump(S,open('marrow/schedule4.json','w'),separators=(",",":"))
