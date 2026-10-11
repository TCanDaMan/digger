import json,sys,statistics as st
S=sys.argv[1]
dig=json.load(open(S+'/mc_all.json')); base=json.load(open(S+'/mc_baseline.json'))
GROUPS={'inarritu':['amores-perros','21-grams','babel','biutiful','birdman-or-the-unexpected-virtue-of-ignorance','the-revenant-2015','bardo-false-chronicle-of-a-handful-of-truths'],
 'power_critique':['dont-look-up','there-will-be-blood','killers-of-the-flower-moon','eddington','mickey-17','the-social-network','glass-onion-a-knives-out-mystery','triangle-of-sadness','one-battle-after-another'],
 'cruise':['top-gun-maverick','mission-impossible-the-final-reckoning']}
grp={s:g for g,ss in GROUPS.items() for s in ss}
films={}
for s,items in base.items():
    p=items[0]['reviewedProduct']; films[s]={'slug':s,'title':p['title'],'metascore':p['criticScoreSummary']['score'],'group':grp[s]}
norm=lambda x:(x or '').lower().replace('the ','').strip()
rows=[]
for r in dig:
    rec={'outlet':r['publicationName'],'critic':r['author'],'score':r['score'],'quote':r['quote'],'url':r['url'],'date':r['date'],'history':[]}
    for s,items in base.items():
        for it in items:
            same_critic = norm(it.get('author'))==norm(r['author']) and r['author']
            same_outlet = norm(it['publicationName'])==norm(r['publicationName'])
            if same_critic or same_outlet:
                rec['history'].append({'film':s,'score':it['score'],'by':'critic' if same_critic else 'outlet','author':it.get('author'),'outlet':it['publicationName'],'delta':it['score']-films[s]['metascore']})
    # critic-level preferred
    ch=[h for h in rec['history'] if h['by']=='critic']
    use=ch if len(ch)>=3 else rec['history']
    rec['baseline_level']='critic' if len(ch)>=3 else ('outlet' if use else 'none')
    if use:
        rec['generosity']=round(st.mean(h['delta'] for h in use),1)
        rec['expected']=round(45+rec['generosity'],1)
        rec['residual']=round(r['score']-rec['expected'],1)
        for g in GROUPS:
            gs=[h['score'] for h in use if films[h['film']]['group']==g]
            rec[g+'_avg']=round(st.mean(gs),1) if gs else None
            rec[g+'_n']=len(gs)
    rec['n_history']=len(use)
    rows.append(rec)
json.dump({'films':films,'reviews':rows},open(S+'/analysis_base.json','w'),indent=1)
for r in sorted(rows,key=lambda r:r.get('residual',99)):
    print(f"{r['score']:>3} {r['outlet'][:28]:28} {r['critic'][:20]:20} lvl={r['baseline_level']:6} n={r['n_history']:2} gen={r.get('generosity')} exp={r.get('expected')} res={r.get('residual')} inar={r.get('inarritu_avg')}({r.get('inarritu_n')}) pow={r.get('power_critique_avg')}")
