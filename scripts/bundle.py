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
RA=json.load(open(S+'/rt_analysis.json')); rtu=RA['reviews']
st=A['stats']
data={'reviews':rows,'stats':st,'rt':rtu,'rtStats':RA['stats'],'rtTotal':319,'rtScore':53}
open(S+'/site/data.js','w').write('window.DIGGER='+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';')
print(len(rows),len(rtu),round(len(open(S+'/site/data.js').read())/1024),'KB')
