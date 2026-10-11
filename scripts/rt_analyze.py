import json,sys,glob,random,statistics as st
S=sys.argv[1]
rt=[];seen=set()
for f in sorted(glob.glob(S+'/rt_in/*.json')):
    for x in json.load(open(f)):
        if x['id'] not in seen: seen.add(x['id']); rt.append(x)
own={o['outlet']:o for o in json.load(open(S+'/rt_ownership.json'))}
miss=[x['outlet'] for x in rt if x['outlet'].strip() not in own]; print('missing',len(miss),miss[:5])
for x in rt:
    o=own[x['outlet'].strip()]; x['type']=o['type']; x['depth']=min(4,int(o['depth'])); x['tech']=bool(o['tech_links']); x['oil']=bool(o['oil_links']); x['ult']=o['ultimate']; x['f']=1 if x['fresh']=='POSITIVE' else 0
random.seed(11)
def pdiff(flag,n=20000):
    a=[x['f'] for x in rt if flag(x)]; b=[x['f'] for x in rt if not flag(x)]
    obs=st.mean(a)-st.mean(b); v=[x['f'] for x in rt]; fl=[flag(x) for x in rt]; c=0
    for _ in range(n):
        random.shuffle(v); aa=[q for q,f in zip(v,fl) if f]; bb=[q for q,f in zip(v,fl) if not f]
        if abs(st.mean(aa)-st.mean(bb))>=abs(obs)-1e-12: c+=1
    return {'diff':round(obs*100,1),'n':len(a),'fresh':round(st.mean(a)*100,1),'rest':round(st.mean(b)*100,1),'p':c/n}
def ranks(x):
    s=sorted(range(len(x)),key=lambda i:x[i]); rk=[0]*len(x); i=0
    while i<len(s):
        j=i
        while j+1<len(s) and x[s[j+1]]==x[s[i]]: j+=1
        for k in range(i,j+1): rk[s[k]]=(i+j)/2
        i=j+1
    return rk
def pear(a,b):
    ma,mb=st.mean(a),st.mean(b); return sum((x-ma)*(y-mb) for x,y in zip(a,b))/(sum((x-ma)**2 for x in a)*sum((y-mb)**2 for y in b))**.5
d=[x['depth'] for x in rt]; f=[x['f'] for x in rt]; obs=pear(ranks(d),ranks(f)); ff=list(f); c=0
for _ in range(20000):
    random.shuffle(ff)
    if abs(pear(ranks(d),ranks(ff)))>=abs(obs): c+=1
out={'n':len(rt),'fresh':round(st.mean(f)*100,1),'depth':{'rho':round(obs,3),'p':c/20000},
 'by_depth':{k:{'n':sum(1 for x in rt if x['depth']==k),'fresh':round(100*st.mean([x['f'] for x in rt if x['depth']==k]),1)} for k in sorted(set(d))},
 'by_type':{t:{'n':sum(1 for x in rt if x['type']==t),'fresh':round(100*st.mean([x['f'] for x in rt if x['type']==t]),1)} for t in sorted({x['type'] for x in rt})},
 'tech':pdiff(lambda x:x['tech']),'oil':pdiff(lambda x:x['oil']),'billionaire':pdiff(lambda x:x['type']=='billionaire-owned'),
 'independent':pdiff(lambda x:x['type']=='independent/small'),'top':pdiff(lambda x:x['top'])}
print(json.dumps(out,indent=1))
json.dump({'stats':out,'reviews':[{k:x[k] for k in ('critic','outlet','top','fresh','score','date','type','depth','tech','oil','ult')} for x in rt]},open(S+'/rt_analysis.json','w'))
