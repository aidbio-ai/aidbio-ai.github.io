#!/usr/bin/env python3
"""Stamp the homepage's scientific previews and their EN/PT captions."""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
copy_path = ROOT/'assets/i18n/home.js'
copy = json.loads(copy_path.read_text().removeprefix('window.AIDBIO_STRINGS = ').rstrip(';\n'))
for key,en,pt in [('plot.views','Plot views','Visualizações do gráfico'),('preview.label','Scientific examples','Exemplos científicos'),('plot.region','Full-size figure','Figura ampliada')]:
    copy['en'][key],copy['pt'][key] = en,pt


def translated(key, en, pt, tag='span', attrs=''):
    copy['en'][key] = en
    copy['pt'][key] = pt
    return f'<{tag} data-i18n="{key}" {attrs}>{html.escape(en)}</{tag}>'


def previews(family, views):
    tabs = '<div class="plot-tabs" role="tablist" aria-label="Plot views" data-i18n-attr="aria-label:plot.views">'
    panels = ''
    for i, (name, label, label_pt, caption, caption_pt, image) in enumerate(views):
        tid = f'{family}-{name}'
        tabs += f'<button class="tab" type="button" role="tab" id="tab-{tid}" aria-controls="panel-{tid}" aria-selected="{str(i==0).lower()}" tabindex="{0 if i==0 else -1}">'+translated('plot.'+tid, label, label_pt)+'</button>'
        if image.endswith('.svg'):
            media = (ROOT/'assets/examples'/image).read_text()
            media = re.sub(r'<desc>.*?</desc>', lambda _: translated('caption.'+tid,caption,caption_pt,'desc'), media, flags=re.S)
        else:
            media = f'<img src="assets/examples/{image}" alt="{html.escape(label)} · PRJNA968041" loading="lazy" width="900" height="650">'
        panels += f'<div role="tabpanel" class="plot-panel" id="panel-{tid}" aria-labelledby="tab-{tid}"{ " hidden" if i else ""}><div class="preview-plot">{media}</div>'+translated('caption.'+tid,caption,caption_pt,'p','class="note plot-caption"')+'</div>'
    return tabs+'</div><div class="plot-stage">'+panels+'</div>'


weather = [('temperature',
  'Temperature + rain',
  'Temperatura + chuva',
  'Daily temperature and rainfall through a year in Jaguariúna, Brazil.',
  'Temperatura e chuva diárias ao longo de um ano em Jaguariúna, Brasil.',
  'weather-temperature.svg'),
 ('atmosphere',
  'Atmosphere',
  'Atmosfera',
  'Air humidity, pressure and vapor pressure deficit through the year.',
  'Umidade do ar, pressão e déficit de pressão de vapor ao longo do ano.',
  'weather-atmosphere.svg'),
 ('soil',
  'Soil wetness',
  'Umidade do solo',
  'Seasonal soil wetness at the surface, root zone and full soil profile.',
  'Umidade sazonal do solo na superfície, na zona radicular e no perfil completo.',
  'weather-soil.svg')]
protein = [('ontology',
  'GO subnetwork',
  'Sub-rede GO',
  'A Gene Ontology subnetwork connects a mitochondrion with related biological terms.',
  'Uma sub-rede da Gene Ontology conecta a mitocôndria a termos biológicos relacionados.',
  'aid2go-ontology.svg'),
 ('test',
  'Test predictions',
  'Predições no teste',
  'An internal test compares predicted protein functions with known annotations.',
  'Um teste interno compara funções preditas de proteínas com anotações conhecidas.',
  'aid2go-test.svg'),
 ('tsne',
  't-SNE',
  't-SNE',
  'A t-SNE view groups Gene Ontology terms by their learned representations.',
  'Uma projeção t-SNE agrupa termos da Gene Ontology por suas representações aprendidas.',
  'aid2go-tsne.svg'),
 ('network',
  'Protein network',
  'Rede de proteínas',
  'A protein network shows computational similarity between protein representations.',
  'Uma rede mostra a similaridade computacional entre representações de proteínas.',
  'aid2go-network.svg')]
study = [('volcano',
  'Volcano',
  'Vulcão',
  'A volcano plot highlights expression differences between two Arabidopsis sample groups.',
  'Um gráfico vulcão destaca diferenças de expressão entre dois grupos de amostras de Arabidopsis.',
  'arabidopsis-volcano.svg'),
 ('gsea',
  'GSEA',
  'GSEA',
  'Gene-set enrichment highlights biological processes associated with each Arabidopsis group.',
  'O enriquecimento de conjuntos gênicos destaca processos biológicos associados a cada grupo de '
  'Arabidopsis.',
  'arabidopsis-gsea.svg'),
 ('genes',
  'Top genes',
  'Genes em destaque',
  'Selected genes show contrasting expression patterns between the Arabidopsis groups.',
  'Genes selecionados mostram padrões contrastantes de expressão entre os grupos de Arabidopsis.',
  'arabidopsis-top.svg'),
 ('pca',
  'PCA',
  'PCA',
  'PCA summarizes the expression profiles of six Arabidopsis samples.',
  'A PCA resume os perfis de expressão de seis amostras de Arabidopsis.',
  'arabidopsis/pca.png'),
 ('heatmap',
  'Heatmap',
  'Mapa de calor',
  'A heatmap compares the most variable genes across six Arabidopsis samples.',
  'Um mapa de calor compara os genes mais variáveis entre seis amostras de Arabidopsis.',
  'arabidopsis/heatmap.png')]

source = '<!--examples:begin--><div class="hero-preview"><div class="window"><div class="window-bar"><span class="window-label">aidbio / field notes</span><div class="tabs" role="tablist" aria-label="Scientific examples" data-i18n-attr="aria-label:preview.label">'
for i,(family,label) in enumerate([('weather','AidWeather'),('gnn','Aid2GO'),('study','AidCistrome'),('wiki','AidWiki')]):
    source += f'<button class="tab" role="tab" id="tab-{family}" data-tab="{family}" aria-selected="{str(i==0).lower()}" tabindex="{0 if i==0 else -1}" aria-controls="panel-{family}" type="button">{label}</button>'
source += '</div></div><div class="family-stage">'
source += '<div class="panel" role="tabpanel" id="panel-weather" aria-labelledby="tab-weather"><div class="panel-head"><span>AidWeather</span><span class="tag tag-amber">NASA POWER</span></div>'+previews('weather',weather)+'<div class="preview-product">'+translated('preview.report','AidWeather-Report →','AidWeather-Report →','a','class="link-arrow" href="#app-aidweather-report"')+translated('preview.report.note','Built with open-source AidWeather.','Feito com o AidWeather de código aberto.','span')+'</div></div>'
source += '<div class="panel" role="tabpanel" id="panel-gnn" aria-labelledby="tab-gnn" hidden><div class="panel-head"><span>Aid2GO</span></div>'+previews('protein',protein)+'</div>'
source += '<div class="panel" role="tabpanel" id="panel-study" aria-labelledby="tab-study" hidden><div class="panel-head"><span>AidCistrome</span></div>'+previews('study',study)+'</div>'
source += '<div class="panel" role="tabpanel" id="panel-wiki" aria-labelledby="tab-wiki" hidden><div class="panel-head"><span>AidWiki</span></div>'+(ROOT/'assets/partials/aidwiki-preview.html').read_text().strip()+'</div></div></div></div><!--examples:end-->'
index=ROOT/'index.html';content=index.read_text()
content=re.sub(r'<!--examples:begin-->.*?<!--examples:end-->',lambda _:source,content,flags=re.S)
content=re.sub(r'<dialog class="plot-dialog".*?</dialog>', '', content, flags=re.S)
index.write_text(content)
copy_path.write_text('window.AIDBIO_STRINGS = '+json.dumps(copy,ensure_ascii=False,indent=2)+';\n')
print('Stamped 12 concise plot views and the illustrated AidWiki exchange across four tabs.')
