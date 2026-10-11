import json,re,sys
h=open(sys.argv[1]).read()
m=re.search(r'<script[^>]*id="__NUXT_DATA__"[^>]*>(.*?)</script>',h,re.S)
d=json.loads(m.group(1))
def deref(i,depth=0):
    v=d[i]
    if depth>12: return None
    if isinstance(v,list):
        if v and isinstance(v[0],str) and v[0] in('Reactive','ShallowReactive','Ref','ShallowRef'): return deref(v[1],depth+1)
        return [deref(x,depth+1) if isinstance(x,int) else x for x in v]
    if isinstance(v,dict): return {k:(deref(x,depth+1) if isinstance(x,int) else x) for k,x in v.items()}
    return v
out=[]
for i,v in enumerate(d):
    if isinstance(v,dict) and 'publicationName' in v and 'quote' in v:
        r=deref(i); out.append({k:r.get(k) for k in ('publicationName','author','score','date','url','quote')})
print(len(out)); json.dump(out,open(sys.argv[2],'w'),indent=1)
for r in out[:5]: print(r['publicationName'],r['author'],r['score'])
