import json,sys,glob,html
S=sys.argv[1]
A=json.load(open(S+'/analysis.json'))
films=A['films']
rows=[]
for r in A['reviews']:
    o=r['own']
    hist=[{'f':films[h['film']]['title'],'g':films[h['film']]['group'],'s':h['score'],'m':films[h['film']]['metascore'],'by':h['by']} for h in r['history']
          if (r['baseline_level']!='critic' or h['by']=='critic')]
    rows.append({'critic':r['critic'],'outlet':r['outlet'],'score':r['score'],'exp':r.get('expected'),'res':r.get('residual'),'gen':r.get('generosity'),
      'lvl':r['baseline_level'],'quote':html.unescape(r['quote'] or ''),'url':r['url'],'date':r['date'],'hist':hist,
      'owner':o['owner'],'ult':o['ultimate'],'type':o['type'],'depth':o['depth'],'tech':bool(o['tech_links']),'techWhy':o.get('tech_reason') or '',
      'oil':bool(o['oil_links']),'oilWhy':o.get('oil_reason') or '','tie':o.get('wb_or_paramount_tie') or '','src':o.get('source') or ''})
rt=[]
for f in sorted(glob.glob(S+'/rt_in/*.json')):
    rt+=json.load(open(f))
seen=set(); rtu=[]
for x in rt:
    if x['id'] in seen: continue
    seen.add(x['id']); rtu.append({k:x[k] for k in ('critic','outlet','top','fresh','score','date')})
st=A['stats']
data={'reviews':rows,'stats':st,'rt':rtu,'rtTotal':319,'rtScore':53}
open(S+'/site/data.js','w').write('window.DIGGER='+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';')
print(len(rows),len(rtu),round(len(open(S+'/site/data.js').read())/1024),'KB')
