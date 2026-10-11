import json,sys,random,statistics as st
S=sys.argv[1]
A=json.load(open(S+'/analysis_base.json')); own=json.load(open(S+'/ownership.json')); base=json.load(open(S+'/mc_baseline.json'))
norm=lambda x:x.lower().split('(')[0].replace('the ','').strip()
om={norm(o['outlet']):o for o in own}
rev=A['reviews']
for r in rev:
    o=om.get(norm(r['outlet']))
    if not o: print('MISSING',r['outlet']); continue
    r['own']=o
def ranks(x):
    s=sorted(range(len(x)),key=lambda i:x[i]); rk=[0]*len(x); i=0
    while i<len(s):
        j=i
        while j+1<len(s) and x[s[j+1]]==x[s[i]]: j+=1
        for k in range(i,j+1): rk[s[k]]=(i+j)/2
        i=j+1
    return rk
def pearson(a,b):
    ma,mb=st.mean(a),st.mean(b); num=sum((x-ma)*(y-mb) for x,y in zip(a,b)); den=(sum((x-ma)**2 for x in a)*sum((y-mb)**2 for y in b))**.5; return num/den
spear=lambda a,b:pearson(ranks(a),ranks(b))
random.seed(7)
def perm_corr(a,b,n=20000):
    obs=spear(a,b); bb=list(b); c=0
    for _ in range(n):
        random.shuffle(bb)
        if abs(spear(a,bb))>=abs(obs): c+=1
    return obs,c/n
def perm_diff(vals,flags,n=20000):
    g1=[v for v,f in zip(vals,flags) if f]; g0=[v for v,f in zip(vals,flags) if not f]
    obs=st.mean(g1)-st.mean(g0); vv=list(vals); c=0
    for _ in range(n):
        random.shuffle(vv); a=[v for v,f in zip(vv,flags) if f]; b=[v for v,f in zip(vv,flags) if not f]
        if abs(st.mean(a)-st.mean(b))>=abs(obs): c+=1
    return round(obs,1),len(g1),c/n
out={}
R=[r for r in rev if 'own' in r]; Rr=[r for r in R if r.get('residual') is not None]
for label,rows,key in [('score',R,'score'),('residual',Rr,'residual')]:
    v=[r[key] for r in rows]
    d=[r['own']['depth'] for r in rows]
    out[label]={'n':len(rows),'depth_spearman':perm_corr(d,v),
      'tech':perm_diff(v,[r['own']['tech_links'] for r in rows]),
      'oil':perm_diff(v,[r['own']['oil_links'] for r in rows]),
      'tech_or_oil':perm_diff(v,[r['own']['tech_links'] or r['own']['oil_links'] for r in rows]),
      'billionaire':perm_diff(v,[r['own']['type']=='billionaire-owned' for r in rows]),
      'independent':perm_diff(v,[r['own']['type']=='independent/small' for r in rows]),
      'by_depth':{k:(round(st.mean([x for x,dd in zip(v,d) if dd==k]),1),sum(1 for dd in d if dd==k)) for k in sorted(set(d))},
      'by_type':{t:(round(st.mean([r[key] for r in rows if r['own']['type']==t]),1),sum(1 for r in rows if r['own']['type']==t)) for t in sorted({r['own']['type'] for r in rows})}}
# control: Don't Look Up — same outlets
dly={norm(i['publicationName']):i['score'] for i in base['dont-look-up']}
pairs=[(r['score'],dly[norm(r['outlet'])],r['own']['tech_links'] or r['own']['oil_links']) for r in R if norm(r['outlet']) in dly]
out['dont_look_up']={'n':len(pairs),'spearman_with_digger':perm_corr([p[0] for p in pairs],[p[1] for p in pairs]),'tech_or_oil_diff_on_DLU':perm_diff([p[1] for p in pairs],[p[2] for p in pairs])}
print(json.dumps(out,indent=1))
json.dump({'films':A['films'],'reviews':R,'stats':out},open(S+'/analysis.json','w'),indent=1)
