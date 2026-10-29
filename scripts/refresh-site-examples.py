#!/usr/bin/env python3
"""Build public site previews from real application outputs. Requires NumPy."""
import argparse
import csv
import hashlib
import html
import json
import math
import shutil
import subprocess
import textwrap
import xml.etree.ElementTree as ET
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'assets/examples'
C = {k: f'var(--{k}-text)' for k in ['amber', 'cyan', 'emerald', 'violet', 'rose']}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text(x, y, value, anchor='start', size=12, color='var(--text-secondary)'):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" fill="{color}">{html.escape(str(value))}</text>'


def line(x1, y1, x2, y2, color='var(--border-subtle)', extra=''):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" {extra}/>'


def svg(name, title, desc, body, height=340):
    # Inline SVG resolves the site's semantic colors in both themes.
    source = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 {height}" role="img" aria-label="{html.escape(title, quote=True)}"><title>{html.escape(title)}</title><desc>{html.escape(desc)}</desc><g font-family="Inter, sans-serif">{body}</g></svg>'
    (OUT / (name + '.svg')).write_text(source + '\n')


def poly(rows, key, lo, hi, top=46, bottom=270, color='emerald'):
    assert min(r[key] for r in rows) >= lo and max(r[key] for r in rows) <= hi, key
    pts = ' '.join(f'{46+i*466/(len(rows)-1):.2f},{bottom-(r[key]-lo)/(hi-lo)*(bottom-top):.2f}' for i, r in enumerate(rows))
    return f'<polyline points="{pts}" fill="none" stroke="{C[color]}" stroke-width="1.7" stroke-linejoin="round"/>'


def grid(lo, hi, top=46, bottom=270, ticks=4):
    s = ''
    for i in range(ticks+1):
        y = bottom-i*(bottom-top)/ticks
        s += line(46, y, 512, y) + text(37, y+4, f'{lo+i*(hi-lo)/ticks:g}', 'end')
    return s


def months(y=295):
    # Actual positions in leap-year 2024, rather than equally spaced month labels.
    return ''.join(text(46+day*466/365, y, m, 'middle') for day, m in [(0,'Jan 1'),(91,'Apr 1'),(182,'Jul 1'),(274,'Oct 1'),(365,'Dec 31')])


def legend(items, y=324):
    s = ''
    for i, (label, color) in enumerate(items):
        x = 46+i*126
        s += line(x, y-4, x+16, y-4, C[color], 'stroke-width="3"') + text(x+21, y, label, size=11)
    return s


def weather(path):
    rows = []
    for row in csv.DictReader(path.open()):
        r = {k: float(v) if k != 'date' else v for k, v in row.items()}
        assert all(math.isfinite(v) and v != -999 for k, v in r.items() if k != 'date')
        r['VPD'] = .6108*math.exp(17.27*r['T2M']/(r['T2M']+237.3))*(1-r['RH2M']/100)
        assert r['T2M_MIN'] <= r['T2M'] <= r['T2M_MAX']
        assert all(0 <= r[k] <= 1 for k in ['GWETTOP', 'GWETROOT', 'GWETPROF'])
        rows.append(r)
    assert len(rows) == 366 and rows[0]['date'] == '2024-01-01' and rows[-1]['date'] == '2024-12-31'
    data = {'location':'Jaguariúna, Brazil', 'latitude':-22.72547, 'longitude':-47.011603,
            'units':{'T2M':'°C','T2M_MAX':'°C','T2M_MIN':'°C','PRECTOTCORR':'mm/day','RH2M':'%','PS':'kPa','VPD':'kPa','GWETTOP':'0–1','GWETROOT':'0–1','GWETPROF':'0–1'},
            'vpd_method':'Estimated from daily mean T2M and RH2M; 0.6108 exp(17.27 T/(T+237.3)) (1-RH/100). Not a daily maximum.', 'daily':rows}
    (OUT/'weather.json').write_text(json.dumps(data,separators=(',',':'))+'\n')
    shutil.copy2(path,OUT/'weather.csv')
    rain_max = math.ceil(max(r['PRECTOTCORR'] for r in rows)/20)*20
    s = grid(0,40)+text(46,20,'Temperature · °C')+text(512,20,'Rain · mm/day','end')
    for i,r in enumerate(rows):
        s += line(46+i*466/365,270,46+i*466/365,270-r['PRECTOTCORR']/rain_max*224,C['cyan'],'stroke-width="1.1" opacity=".4"')
    for i in range(5):s+=text(522,274-i*56,f'{rain_max*i/4:g}')
    for key,color in [('T2M_MAX','amber'),('T2M_MIN','violet'),('T2M','emerald')]:s+=poly(rows,key,0,40,color=color)
    svg('weather-temperature','Temperature and rainfall · 2024','All 366 daily values. Left axis: T2M, maximum and minimum in °C. Right axis: precipitation in mm/day. NASA POWER grid data near Jaguariúna, Brazil.',s+months()+legend([('T2M','emerald'),('T2M_MAX','amber'),('T2M_MIN','violet'),('Rain','cyan')]))
    s=grid(0,4,45,186)+text(46,20,'VPD · kPa')+text(512,20,'RH2M · %','end')
    for i in range(5):s+=text(522,190-i*141/4,i*25)
    s+=poly(rows,'VPD',0,4,45,186,'violet')+poly(rows,'RH2M',0,100,45,186,'cyan')
    s+=grid(91,95,235,275,2)+text(46,222,'Surface pressure · PS · kPa')+poly(rows,'PS',91,95,235,275,'amber')
    svg('weather-atmosphere','Atmospheric demand, humidity and pressure · 2024','Left VPD axis 0–4 kPa; right RH2M axis 0–100%. Surface pressure in a separate aligned strip, 91–95 kPa. VPD estimated from daily means. No smoothing.',s+months(298)+legend([('VPD','violet'),('RH2M','cyan'),('PS','amber')],327),345)
    s=grid(0,1)+text(46,20,'Soil wetness · fraction of saturation (0–1)')
    for key,color in [('GWETPROF','violet'),('GWETROOT','emerald'),('GWETTOP','amber')]:s+=poly(rows,key,0,1,color=color)
    svg('weather-soil','Soil wetness at three depths · 2024','Modeled surface, root-zone and full-profile soil wetness, fraction of saturation on a shared 0–1 axis. Not a field measurement or a crop stress diagnosis.',s+months()+legend([('GWETTOP','amber'),('GWETROOT','emerald'),('GWETPROF','violet')]))
    return {'source':'NASA POWER via AidWeather','source_sha256':sha(path),'period':'2024-01-01/2024-12-31','rows':366,'coordinate':[-22.72547,-47.011603],'limitation':'Grid data; VPD estimated from daily means. No smoothing or station observation claim.'}


def aid2go(dev):
    gallery=dev/'aid2go/reports/visualization-gallery/data.json'
    g=json.loads(gallery.read_text());terms={t['id']:t for t in g['go']}
    original=next(s for s in g['go_subgraphs'] if s['id']=='GO:0005739')
    ns={'s':'http://www.w3.org/2000/svg'};tree=ET.fromstring(original['svg'])
    positions={'GO:0043231':(395,38),'GO:0005737':(160,38),'GO:0005739':(280,156),'GO:0005759':(95,280),'GO:0005740':(280,280),'GO:0044290':(465,280)}
    edges=[];names={}
    for node in tree.findall('.//s:g',ns):
        title=node.find('s:title',ns)
        if title is None:continue
        if node.get('class')=='node':names[title.text]=' '.join(t.text for t in node.findall('.//s:text',ns) if t.text and not t.text.startswith('GO:'))
        elif node.get('class')=='edge':
            a,b=title.text.split('->')
            if a in positions and b in positions:edges.append({'source':a,'target':b,'relation':node.find('s:text',ns).text})
    s='<defs><marker id="go-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10Z" fill="var(--text-muted)"/></marker></defs>'
    for e in edges:
        a,b=positions[e['source']],positions[e['target']]
        s+=line(a[0],a[1]-25,b[0],b[1]+28,'var(--text-muted)','stroke-width="1.7" marker-end="url(#go-arrow)"'+(' stroke-dasharray="5 4"' if e['relation']=='part_of' else ''))
        s+=text((a[0]+b[0])/2+5,(a[1]+b[1])/2,e['relation'],size=10)
    for tid,(x,y) in positions.items():
        color=C['emerald' if tid=='GO:0005739' else 'violet']
        s+=f'<rect x="{x-88}" y="{y-25}" width="176" height="55" rx="9" fill="var(--surface-card)" stroke="{color}"/>'
        for j,t in enumerate(textwrap.wrap(names[tid],27)):s+=text(x,y-7+j*13,t,'middle',10,'var(--text-primary)')
        s+=text(x,y+22,tid,'middle',10,color)
    svg('aid2go-ontology','A mitochondrion GO subnetwork','Six actual terms from the saved ontology. Arrows point from child to parent: solid is_a, dashed part_of. Ontology relationships, not protein interactions.',s)
    xs=[t['tsne'][0] for t in g['go']];ys=[t['tsne'][1] for t in g['go']]
    s=text(46,20,'GO term embeddings · t-SNE')
    for t in g['go']:
        x=46+(t['tsne'][0]-min(xs))/(max(xs)-min(xs))*466;y=270-(t['tsne'][1]-min(ys))/(max(ys)-min(ys))*224
        color=C[{'BP':'emerald','MF':'violet','CC':'amber'}[t['aspect']]]
        s+=f'<circle cx="{x:.2f}" cy="{y:.2f}" r="2.2" opacity=".7" fill="{color}"><title>{html.escape(t["id"]+" · "+t["name"])}</title></circle>'
    s+=text(46,295,'1,000 terms · perplexity 30 · seed 42',size=11)
    # Short legend labels stay legible at mobile sizes; full names are in the caption.
    svg('aid2go-tsne','Saved GO term t-SNE projection','All 1,000 GO terms. BP: biological process; MF: molecular function; CC: cellular component. Axes arbitrary; exploratory embedding layout, not accuracy.',s+legend([('BP','emerald'),('MF','violet'),('CC','amber')]))
    ontology_nodes=[{'id':k,'name':names[k]} for k in positions]
    net=g['protein_network'];positions={n['id']:(280+n['x']*205,150+n['y']*125) for n in net['nodes']};s=''
    for e in net['edges']:s+=line(*positions[e['source']],*positions[e['target']],C['violet'],'opacity=".22" stroke-width="1"')
    for n in net['nodes']:
        x,y=positions[n['id']];focal=n['id']==net['focal'];radius=8 if focal else 3+math.sqrt(n['degree'])*.5
        s+=f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{radius:.2f}" fill="{C["amber" if focal else "violet"]}"><title>{n["id"]} · degree {n["degree"]}</title></circle>'
        if focal:s+=text(x+12,y-10,n['id'],color='var(--text-primary)')
    svg('aid2go-network','Protein embedding similarity network','Saved 35-protein neighborhood around Q80Y84. Edges represent embedding similarity, not experimentally measured protein interactions. Node size follows saved degree.',s+text(46,320,f'{len(net["nodes"])} proteins · {len(net["edges"])} similarity edges',size=11))
    exp=dev/'aid2go/reports/experiments/v2_unique_pairs_sample_1000x100_seed42/baseline'
    a=np.load(exp/'heldout_scores.npz',allow_pickle=False);metrics=json.loads((exp/'metrics.json').read_text());threshold=metrics['validation_selected_threshold'];pid='Q9NT62';i=list(a['protein_ids']).index(pid)
    rank=list(np.argsort(-a['scores'][i])[:4]);rank+=[j for j in np.where(a['truth'][i])[0] if j not in rank]
    predictions=[{'go_id':str(a['go_ids'][j]),'name':terms.get(str(a['go_ids'][j]),{}).get('name',str(a['go_ids'][j])),'score':float(a['scores'][i,j]),'annotated':bool(a['truth'][i,j])} for j in rank]
    s=text(12,20,f'{pid} · test scores vs. known annotations',size=13,color='var(--text-primary)')
    for j,r in enumerate(predictions):
        y=49+j*33;color=C['emerald' if r['annotated'] else 'violet']
        s+=text(12,y+10,r['go_id'],size=11)+f'<rect x="119" y="{y}" width="{r["score"]*275:.2f}" height="14" rx="3" fill="{color}"/>'
        s+=text(403,y+11,f'{r["score"]:.3f}',size=11)+text(460,y+11,'● known' if r['annotated'] else '○ unlisted',size=11)
    s+=line(119+threshold*275,40,119+threshold*275,280,'var(--text-primary)','stroke-dasharray="3 4"')
    s+=text(12,305,'Score: 0–1 · validation threshold: 0.55',size=11)+text(12,327,'Known terms below threshold are missed annotations.',size=11)
    svg('aid2go-test','Held-out test predictions and known GO annotations','Baseline model, Q9NT62. Top four scores plus all known terms. Green: held-out annotation; purple: unlisted, not confirmed negative. Scores are not calibrated probabilities. Threshold selected on validation data.',s,345)
    compact={'protocol':metrics['protocol'],'model':'baseline','model_status':'in development','selection':'Pre-existing true-positive explanation protein Q9NT62; top four scores plus all known test annotations. Illustrative, not representative. Includes unlisted and missed annotations.','threshold':threshold,'threshold_source':'validation','protein_id':pid,'predictions':predictions,'overall':metrics['overall'],'ontology':{'nodes':ontology_nodes,'edges':edges},'projection':{'metadata':g['projection'],'terms':[{'id':t['id'],'aspect':t['aspect'],'tsne':t['tsne']} for t in g['go']]},'protein_network':net}
    (OUT/'aid2go.json').write_text(json.dumps(compact,separators=(',',':'))+'\n')
    return {'gallery_sha256':sha(gallery),'test_scores_sha256':sha(exp/'heldout_scores.npz'),'metrics_sha256':sha(exp/'metrics.json'),'sample':'v2_unique_pairs_sample_1000x100_seed42','protocol':metrics['protocol'],'limitation':'Internal protein-held-out evaluation, not CAFA/external certification. Model in development. Projection/network are exploratory.'}


def arabidopsis(path):
    folder=OUT/'arabidopsis';folder.mkdir(exist_ok=True)
    for name in ['metadata.json','deseq2_4_week_vs_2_week.csv','gsea/4_week_vs_2_week/4_week_vs_2_week_prerank_all.csv']:
        shutil.copy2(path/name,folder/Path(name).name)
    wanted={'volcano_4_week_vs_2_week.png':'volcano.png','ma_4_week_vs_2_week.png':'ma.png','pca_condition_time.png':'pca.png','top_genes.png':'top-genes.png','top_variable_genes_heatmap.png':'heatmap.png'}
    for source,target in wanted.items():shutil.copy2(path/'plots/4_week_vs_2_week'/source,folder/target)
    for source,target in [('4_week_vs_2_week_prerank_dotplot.png','gsea.png'),('running_sum.png','gsea-running.png')]:shutil.copy2(path/'gsea/4_week_vs_2_week'/source,folder/target)
    de=list(csv.DictReader((path/'deseq2_4_week_vs_2_week.csv').open()));points={'emerald':[],'rose':[],'muted':[]};valid=0
    for r in de:
        try:x=float(r['log2FC_shrunk']);q=float(r['padj'])
        except ValueError:continue
        if not math.isfinite(x) or not math.isfinite(q):continue
        valid+=1;y=min(100,-math.log10(max(q,1e-100)));color='rose' if q<.05 and x>=1 else 'emerald' if q<.05 and x<=-1 else 'muted'
        points[color].append(f'M{46+(max(-20,min(20,x))+20)/40*466:.1f},{270-y/100*224:.1f}h.1')
    s=grid(0,100)+text(46,20,'−log₁₀(adjusted p) · capped at 100')
    for color,pts in points.items():s+=f'<path d="{" ".join(pts)}" fill="none" stroke="{C.get(color,"var(--text-muted)")}" opacity=".5" stroke-width="2.5" stroke-linecap="round"/>'
    s+=line(46,270-(-math.log10(.05))/100*224,512,270-(-math.log10(.05))/100*224,'var(--text-primary)','stroke-dasharray="4 4"')
    for x in [-20,-10,0,10,20]:s+=text(46+(x+20)/40*466,293,x,'middle')
    svg('arabidopsis-volcano','Arabidopsis differential expression · PRJNA968041',f'All {valid} finite genes, no sampling. Color: adjusted p <0.05 and |shrunken log2FC| ≥1. Overview caps x at ±20 and y at 100; uncapped figure and table linked. Age and tissue differ together.',s+text(280,324,'Shrunken log₂ fold change · 4-week / 2-week','middle'))
    gs=list(csv.DictReader((path/'gsea/4_week_vs_2_week/4_week_vs_2_week_prerank_all.csv').open()))
    enriched=[r for r in gs if float(r['FDR q-val'])<.05 and math.isfinite(float(r['NES']))]
    selected=sorted(enriched,key=lambda r:float(r['NES']))[:4]+sorted(enriched,key=lambda r:float(r['NES']),reverse=True)[:4]
    s=text(12,18,'GO enrichment · strongest NES in each direction',size=12)
    for i,r in enumerate(selected):
        y=48+i*31;nes=float(r['NES']);name=r['Term'].split(' ',1)[1];color=C['rose' if nes>0 else 'emerald'];x=400+nes*32
        s+=text(12,y+5,name[:43]+('…' if len(name)>43 else ''),size=10)+line(400,y,x,y,color,'stroke-width="5"')+f'<circle cx="{x}" cy="{y}" r="4" fill="{color}"/>'
    s+=line(400,31,400,285,'var(--text-muted)')+line(304,290,496,290,'var(--text-muted)')
    for tick in [-3,-1.5,0,1.5,3]:s+=text(400+tick*32,306,tick,'middle',10)
    s+=text(400,330,'← 2-week     NES     4-week →','middle',11)
    svg('arabidopsis-gsea','Preranked GO enrichment · PRJNA968041','Four most negative and four most positive normalized enrichment scores among terms with FDR <0.05. Selection by NES, not significance. Full enrichment table and original dotplot linked.',s)
    finite=[r for r in de if r['stat_wald'] not in ['NA','NaN',''] and math.isfinite(float(r['stat_wald']))]
    selected=sorted(finite,key=lambda r:float(r['stat_wald']),reverse=True)[:5]+sorted(finite,key=lambda r:float(r['stat_wald']))[:5]
    s=text(12,18,'Top five genes in each direction · Wald statistic',size=12)
    for i,r in enumerate(selected):
        y=42+i*25;w=float(r['stat_wald']);s+=text(12,y+5,r['gene_id'],size=11)+line(340,y,340+w*2,y,C['rose' if w>0 else 'emerald'],'stroke-width="9"')
    s+=line(340,29,340,285,'var(--text-muted)')
    for x in [-60,-30,0,30,60]:s+=text(340+x*2,317,x,'middle',11)
    svg('arabidopsis-top','Top genes by signed Wald statistic','Five largest and five smallest signed DESeq2 Wald statistics, not fold-change magnitude. Positive values favor four-week inflorescences. Full top-ten figure and table linked.',s)
    return {'bioproject':'PRJNA968041','study':'https://www.ncbi.nlm.nih.gov/bioproject/968041','publication':'https://doi.org/10.1073/pnas.2221181120','authors':['Tieqiang Hu','Xiaohui Li','Liren Du','Darren Manuela','Mingli Xu'],'citation':'Hu et al. (2023), PNAS 120(22): e2221181120','contrast':'4-week inflorescence / 2-week shoot apex, Col-0; three replicates per group','source_files':{p.name:sha(p) for p in [path/'metadata.json',path/'deseq2_4_week_vs_2_week.csv',path/'gsea/4_week_vs_2_week/4_week_vs_2_week_prerank_all.csv']},'rights':'Original AidCistrome/AidBio figures and site redraws from public sequencing data; no figures copied from the paper.','limitation':'Age and tissue confounded. Differential expression and enrichment do not establish causation. Overview volcano display-capped; full output supplied.'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--dev-root',type=Path,default=Path('/home/clever/aidbio/dev'))
    p.add_argument('--weather-csv',type=Path,required=True)
    p.add_argument('--arabidopsis-root',type=Path,required=True)
    p.add_argument('--aidcistrome-revision',help='Optional observed server HEAD; not a generating-revision claim')
    args=p.parse_args();OUT.mkdir(exist_ok=True)
    manifest={'policy':'Public data only. AidWeather fetch, saved Aid2GO test artifacts, completed AidCistrome analysis. No retraining or private datasets.','weather':weather(args.weather_csv),'aid2go':aid2go(args.dev_root),'aidcistrome':arabidopsis(args.arabidopsis_root)}
    for app in ['aid2go','aidweather','aidweather-report']:
        repo=args.dev_root/app
        manifest.setdefault('collection_checkouts',{})[app]={'head':subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip(),'dirty':bool(subprocess.check_output(['git','-C',str(repo),'status','--porcelain'])),'scope':'HEAD at collection, not proof of generating revision'}
    if args.aidcistrome_revision:
        manifest['collection_checkouts']['aidcistrome_server']={'head':args.aidcistrome_revision,'scope':'Observed server HEAD supplied at collection; working-tree status and generating revision are not established by this value.'}
    manifest['outputs']={str(p.relative_to(OUT)):sha(p) for p in sorted(OUT.rglob('*')) if p.is_file() and p.name!='manifest.json'}
    (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('Built 10 previews, data extracts and full-resolution study figures.')


if __name__=='__main__':main()
