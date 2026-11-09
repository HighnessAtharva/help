import csv,sys,datetime,collections
sys.path.insert(0,'.')
from load import load
TODAY=datetime.date(2026,11,3)
fac=list(csv.DictReader(open(__import__('os').environ.get('FACTORS_CSV','../references/example-2026-12-03-ariovis/inputs/France Accuknox Accounts Full.csv'),encoding='utf-8-sig')))
D=load()
def dom(r):
    for k in ('Company Domain','Email Domain'):
        if r.get(k): return str(r[k]).lower()
    return ''
TAB={'1. Luma Registrants':'Luma','2. Meetup Registrants':'Meetup',' Webinar Regs Filtered JAHANA +':'Webinar Regs','Website Form Fills DEBJANI MAM':'Website Form Fills'}
sheet=collections.defaultdict(list)
for t,recs in D.items():
    for r in recs: sheet[dom(r)].append((TAB.get(t,t),r))

# type, fit(H/M/L), lang, note
META={
'capgemini.com':('SI',  'H','English','Global SI. Sheet leads are India-based. Factors geo is France. Also a partner angle.'),
'wwf.fr':('Nonprofit','L','French','Nonprofit. Factors tags it Management Consulting. 0 identified visitors. Check for bot or one researcher.'),
'klesia.fr':('End customer','H','French','Paritaire social protection group (retirement, health, prevoyance). Spike since 13 Oct.'),
'socomec.com':('End customer','H','French','Industrial equipment maker, HQ Benfeld, cybersecurity engineer hiring seen on France Travail.'),
'se.com':('End customer','H','English','Schneider Electric. 3 people registered, all 3 events. Location of people unknown.'),
'welyb.fr':('End customer','M','French','Company identity NOT verified. No public result found.'),
'bnpparibas.com':('End customer','H','English','CIB unit. One Paris booth scan (RSA). Low intent alone.'),
'syxperiane.com':('SI/MSP','M','French','French IT services and hosting. Partner or channel angle. Last visit May 2025.'),
'orange.com':('End customer','H','English','Telecom. 10 identified visitors. No page views logged.'),
'soprasteria.com':('SI','M','English','SI with 30 identified visitors. Partner angle.'),
'trustpair.com':('End customer','M','English','Paris B2B fintech. Possible Basware acquisition (unverified).'),
'sanofi.com':('End customer','H','English','Pharma. Regulated data.'),
'valeo.com':('End customer','H','English','Automotive supplier. 78 cumulative pages.'),
'thalesgroup.com':('End customer','H','English','Defense and security. Last visit Jan 2025.'),
'contentsquare.com':('End customer','M','English','Paris SaaS. Last visit June 2025.'),
'gemaddis.com':('End customer','L','French','Annecy manufacturer. Last visit Mar 2026.'),
'engie.com':('End customer','H','English','Energy utility. Factors active 3 Nov. 1 webinar registrant.'),
'michelin.com':('End customer','H','English','Manufacturing. Last visit July 2025.'),
'allianceproit.com':('SI/MSP','L','French','Small IT firm. Last visit Apr 2025.'),
'teads.tv':('End customer','M','English','Adtech. Recent light visit.'),
'phacetlabs.com':('SI/MSP','L','French','Small IT firm. Not verified.'),
'sodexo.com':('End customer','M','English','Services group.'),
'pernod-ricard.com':('End customer','M','English','Consumer goods.'),
'socgen.com':('End customer','H','English','Bank. Sheet lead is Bengaluru-based. Factors France visit May 2025.'),
'decathlon.com':('End customer','M','English','Retail.'),
'exclusive-networks.com':('Vendor/channel','L','verify','Cybersecurity distributor. Treat as channel, not a buyer.'),
'rothschildandco.com':('End customer','M','English','Financial services.'),
'airbus.com':('End customer','H','English','Aerospace.'),
'icover-services.com':('End customer','M','French','Insurance services. Not verified.'),
'paragon-europe.com':('End customer','L','French','Visited 29 Oct. Not verified.'),
'atr-aircraft.com':('End customer','M','English','Aerospace. Factors tags it Automotive.'),
'runmyprocess.com':('End customer','M','English','Workflow SaaS. Fujitsu-owned (not verified here).'),
'asendia.com':('End customer','M','English','Postal logistics.'),
'itsintegra.com':('SI/MSP','L','French','IT services.'),
'cns-com.com':('SI/MSP','L','French','IT services, Lyon.'),
'murena.io':('End customer','M','English','Privacy-focused phone OS company.'),
'cs-soprasteria.com':('SI','M','English','Sopra Steria subsidiary. Same account as Sopra Steria.'),
'totalenergies.com':('End customer','H','English','Energy.'),
'roquette.com':('End customer','M','English','Food ingredients.'),
'noiise.com':('End customer','L','French','Lyon software firm.'),
'maif.fr':('End customer','H','French','Insurer, Niort.'),
'tikehaucapital.com':('End customer','M','English','Asset manager.'),
'octo.com':('SI','M','English','Tech consultancy.'),
'ingroupe.com':('End customer','H','English','Secure identity. State-linked. High-value fit.'),
'mistral.ai':('End customer','H','English','AI lab. Agents API is a direct agentic-AI fit. 2 pages only.'),
'legrand.fr':('End customer','M','English','Electrical equipment.'),
'guerbet.com':('End customer','M','English','Pharma.'),
'toyota-europe.com':('End customer','M','English','Automotive.'),
'oxya.com':('SI/MSP','M','English','Managed services. Partner angle.'),
'nxo.eu':('SI/MSP','M','French','IT integrator. Partner angle.'),
'airfrance.fr':('End customer','M','English','Airline.'),
'didomi.io':('End customer','M','English','Consent SaaS.'),
'notify-group.com':('End customer','M','English','AI SaaS.'),
'nameshield.com':('Vendor/channel','L','verify','Domain-name security vendor. Possible overlap with security vendors.'),
'capgemini-engineering.com':('SI','M','English','Capgemini unit. Same account as Capgemini.'),
'europcar.com':('End customer','M','English','Mobility.'),
'laredoute.fr':('End customer','M','English','Retail.'),
'gustaveroussy.fr':('End customer','M','French','Cancer hospital. Health data.'),
'c4v.com':('Vendor/channel','L','verify','Venture firm.'),
'robeaute.com':('End customer','L','English','Medtech startup.'),
'foxstream.fr':('End customer','L','French','Video analytics.'),
'arpege.fr':('End customer','L','French','Public-sector software. Not verified.'),
'ipanovia.com':('Agency','L','verify','Consulting firm.'),
'lefebvre-dalloz.fr':('End customer','L','French','Legal publisher.'),
'groupemoniteur.fr':('Agency','L','French','Trade media.'),
'aigle.com':('End customer','L','English','Apparel.'),
'driiveme.com':('End customer','L','English','Mobility startup.'),
'novaxess.fr':('End customer','L','French','Small manufacturer.'),
'bostik.com':('End customer','L','English','Chemicals.'),
'apem.com':('End customer','L','English','Electronics.'),
'maisadour.com':('End customer','L','French','Agri cooperative.'),
'ceff-electricite.fr':('End customer','L','French','Small electrical firm.'),
'campingcarpark.com':('End customer','L','French','Leisure.'),
'lesommer.fr':('End customer','L','French','Environmental products.'),
'outhere-music.com':('Agency','L','verify','Music label.'),
'quickscrum.com':('Vendor/channel','L','verify','Agile software vendor.'),
# Sheet-only accounts
'eviden.com':('SI','H','English','Atos group unit. 2 sheet rows, 3 webinars. Partner angle.'),
'worldline.com':('End customer','H','English','Payments. 2 webinar regs. Location of people unknown.'),
'natixis.com':('End customer','H','English','Bank. 1 webinar reg.'),
'swift.com':('End customer','H','English','HQ is Belgium (La Hulpe, from public knowledge, not re-checked). 1 webinar reg.'),
'tersedia.fr':('End customer','L','French','FR location confirmed in form. Company identity NOT verified.'),
}
EXCLUDE_EDU={'kedgebs.com','em-lyon.com','sciencespo.fr','univ-brest.fr','grenoble-inp.fr','omneseducation.com','digited.net','stratx-exl.com'}
JUNK={'montpellier-tourisme.fr':'Name says road authority, domain says tourism office. Ambiguous.',
'bureauxlocaux.com':'Real estate listings site. Not a fit.',
'zonama.co':'Gift-card firm. Junk-like.',
'mazetbeaute.fr':'Name says electronics, domain says beauty. Ambiguous.',
'dnd.fr':'Digital agency.','gulfstream-communication.fr':'Communication agency.','canalchat.com':'Chat vendor.',
'makethegrade.fr':'Education services, unclear.','uptoo.fr':'Recruiting firm.','gezim.fr':'Staffing agency.'}
HI_INTENT=('Introducing AgentZ','Zero Trust for Agentic','V3.0','AISPM')
def pts(r):
    d=r['Domain'].lower()
    s30=int(r['Sessions (30d)'] or 0); pv=int(r['Page Views (global)'] or 0); pc=int(r['Page Count (cumulative)'] or 0); iv=int(r['Identified Visitors'] or 0)
    la=datetime.date.fromisoformat(r['Latest Activity']); age=(TODAY-la).days
    rec=20 if s30>0 else 12 if age<=30 else 6 if age<=90 else 1
    dep=15 if pv>=200 else 11 if pv>=50 else 6 if pv>=10 else 3 if pv>=1 else 0
    rep=12 if pc>=100 else 8 if pc>=40 else 4 if pc>=10 else 1
    mp=8 if iv>=25 else 5 if iv>=10 else 0
    return rec,dep,rep,mp,s30,pv,pc,iv,age
def sheetpts(d):
    rows=sheet.get(d,[]); 
    if not rows: return 0,'',0
    refs=[f"{t} r{r['_row']}" for t,r in rows]
    p=0; tabs=set(t for t,_ in rows)
    reg=[r for t,r in rows if t in('Luma','Webinar Regs')]
    forms=[r for t,r in rows if t=='Website Form Fills']
    if rows: p+=12
    ev=max([float(r.get('Events Registered') or 0) for t,r in rows if t=='Luma']+[0])
    if ev>=2: p+=5
    ppl=max([float(r.get('Colleagues Also Registered') or 0) for t,r in rows]+[0])
    if ppl>=3: p+=4
    txt=' '.join(str(r.get('Which Webinars') or '')+str(r.get('Form / Event') or '') for t,r in rows)
    if any(k in txt for k in HI_INTENT): p+=4
    return p,'; '.join(refs),len(rows)
rank_rows=[];review=[];seen=set()
FIT={'H':15,'M':8,'L':3}
accts={}
for r in fac:
    d=r['Domain'].lower(); accts[d]=r
for d in ('eviden.com','worldline.com','natixis.com','swift.com','tersedia.fr'):
    accts.setdefault(d,None)
for d,r in accts.items():
    if d in EXCLUDE_EDU:
        review.append((r['Company Name'],d,'Education or school','Exclude. Students and staff, not buyers.','Factors rank %s'%r['Rank'])); continue
    if d in JUNK:
        review.append((r['Company Name'],d,'Ambiguous or non-ICP',JUNK[d],'Factors rank %s'%r['Rank'])); continue
    m=META.get(d,('End customer','L','verify','No note.'))
    sp,refs,nrows=sheetpts(d)
    if r:
        rec,dep,rep,mp,s30,pv,pc,iv,age=pts(r); name=r['Company Name']; city=r['City'] or 'n/a'
        fsig=f"Factors: {s30} sessions 30d, {pv} page views, {pc} cumulative pages, {iv} identified visitors, last seen {r['Latest Activity']}, rank {r['Rank']}"
        src='Factors rank %s'%r['Rank']
    else:
        rec=dep=rep=mp=0; s30=pv=pc=iv=0; age=999; name={'eviden.com':'Eviden (Atos)','worldline.com':'Worldline','natixis.com':'Natixis','swift.com':'Swift','tersedia.fr':'Tersedia'}[d]; city='n/a'
        fsig='Not in Factors list'; src=''
    fit=FIT[m[1]]
    if m[0] in('Vendor/channel',): fit=0
    score=rec+dep+rep+mp+sp+fit
    if s30>=50 and iv==0: score-=0  # spike flag only
    ev='Confirmed (Factors HQ + visitor geo)'
    if d in('klesia.fr','socomec.com','syxperiane.com','trustpair.com','wwf.fr'): ev='Confirmed (Factors + public HQ check)'
    if not r:
        ev={'swift.com':'Inferred (Belgian HQ, public knowledge)','tersedia.fr':'Confirmed in sheet (FR form location), company unverified'}.get(d,'Inferred (French HQ, sheet person location unknown)')
    elif d in('se.com','capgemini.com','bnpparibas.com','socgen.com','engie.com'):
        ev='Confirmed in Factors. Sheet leads: '+('FR (Paris)' if d=='bnpparibas.com' else 'location unknown or India')
    conf='High' if (r and sp>0 and s30>0) else 'Medium' if ((r and (s30>0 or sp>0)) or (not r and sp>0 and m[1]=='H')) else 'Low'
    if d in('welyb.fr','tersedia.fr','wwf.fr','phacetlabs.com','paragon-europe.com'): conf='Low'
    if m[0]=='Vendor/channel': conf='Low'
    if m[0] in('SI','SI/MSP'): ang='Partner angle: invite as ecosystem, then ask about their customers.'
    else: ang=''
    nxt={'High':'Send invite now. Ariovis picks the contact.','Medium':'Find a named security or platform owner first, then invite.','Low':'Verify the company and the signal first.'}[conf]
    if m[0]=='Vendor/channel': nxt='Do not invite as a buyer. Route to partnerships if relevant.'
    if m[0]=='Nonprofit': nxt='Check Factors for bot traffic, then decide.'
    rank_rows.append(dict(score=score,Company=name,Domain=d,Type=m[0],Region=city+', France' if city!='n/a' else ('France' if d!='swift.com' else 'Belgium'),
      Source='; '.join(x for x in (src,refs) if x),Signals=fsig+('. Sheet: %d row(s)'%nrows if nrows else ''),
      Fit=m[3]+((' '+ang) if ang else ''),Evidence=ev,Confidence=conf,Language=m[2],Next=nxt))
rank_rows.sort(key=lambda x:-x['score'])
for i,x in enumerate(rank_rows,1): x['Rank']=i
cols=['Rank','score','Company','Domain','Type','Region','Source','Signals','Fit','Evidence','Confidence','Language','Next']
with open(__import__('os').environ.get('OUT_DIR','../references/example-2026-12-03-ariovis')+'/ranked_accounts.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=cols,extrasaction='ignore'); w.writeheader(); w.writerows(rank_rows)
with open(__import__('os').environ.get('OUT_DIR','../references/example-2026-12-03-ariovis')+'/needs_review.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['Company','Domain','Flag','Reason','Source']); w.writerows(review)
for x in rank_rows[:30]: print(x['Rank'],x['score'],x['Company'],x['Domain'],x['Type'],x['Confidence'],x['Language'])
print(len(rank_rows),'ranked',len(review),'review')
