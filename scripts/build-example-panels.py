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
            media = (ROOT/'assets/examples'/image).read_text().replace('<svg ', '<svg lang="en" ', 1)
        else:
            media = f'<img src="assets/examples/{image}" alt="{html.escape(label)} · PRJNA968041" loading="lazy" width="900" height="650">'
        panels += f'<div role="tabpanel" class="plot-panel" id="panel-{tid}" aria-labelledby="tab-{tid}"{ " hidden" if i else ""}><div class="preview-plot">{media}</div>'+translated('plot.expand','Expand plot ↗','Ampliar gráfico ↗','button',f'type="button" class="plot-expand" data-expand-plot="panel-{tid}"')+translated('caption.'+tid,caption,caption_pt,'p','class="note plot-caption"')+'</div>'
    return tabs+'</div><div class="plot-stage">'+panels+'</div>'


weather = [
 ('temperature','Temperature + rain','Temperatura + chuva','Daily T2M, maximum and minimum (°C, left); rain (mm/day, right). All 366 days, without smoothing.','T2M diária, máxima e mínima (°C, à esquerda); chuva (mm/dia, à direita). Os 366 dias, sem suavização.','weather-temperature.svg'),
 ('atmosphere','Atmosphere','Atmosfera','VPD (kPa, left) and RH2M (%, right). Pressure (PS, kPa) has its own aligned strip. VPD is estimated from daily mean temperature and humidity.','DPV (kPa, à esquerda) e RH2M (%, à direita). A pressão (PS, kPa) aparece em uma faixa alinhada. DPV estimado da temperatura e umidade médias diárias.','weather-atmosphere.svg'),
 ('soil','Soil wetness','Umidade do solo','GWETTOP, GWETROOT and GWETPROF: surface, root zone and full profile. Shared 0–1 saturation scale; modeled grid values, not field sensors.','GWETTOP, GWETROOT e GWETPROF: superfície, zona radicular e perfil completo. Mesma escala de saturação de 0 a 1; valores modelados, não sensores de campo.','weather-soil.svg')]
protein = [
 ('ontology','GO subnetwork','Sub-rede GO','A mitochondrion and its ontology context. Arrows point to parents; solid is_a, dashed part_of. These are GO relationships.','Uma mitocôndria e seu contexto na ontologia. Setas apontam aos termos pais; is_a contínuo, part_of tracejado. São relações da GO.','aid2go-ontology.svg'),
 ('test','Test predictions','Predições no teste','Q9NT62: four highest scores plus all five known test annotations. Green = known; purple = unlisted, not a confirmed negative. Includes three missed annotations. Illustrative internal test, not a general performance claim.','Q9NT62: os quatro maiores escores e as cinco anotações conhecidas no teste. Verde = conhecida; roxo = ausente, não um negativo confirmado. Inclui três anotações não recuperadas. Exemplo interno, não uma medida geral de desempenho.','aid2go-test.svg'),
 ('tsne','t-SNE','t-SNE','All 1,000 saved GO term embeddings. Colors: biological process (BP), molecular function (MF), cellular component (CC). Exploratory layout, with arbitrary axes; not model validation.','Os 1.000 embeddings salvos de termos GO. Cores: processo biológico (BP), função molecular (MF) e componente celular (CC). Projeção exploratória com eixos arbitrários; não valida o modelo.','aid2go-tsne.svg'),
 ('network','Protein network','Rede de proteínas','35 proteins and 153 embedding-similarity edges around Q80Y84. Node size follows degree. These edges are computational similarities, not experimental interactions.','35 proteínas e 153 arestas de similaridade de embeddings ao redor de Q80Y84. Tamanho por grau. As arestas são similaridades computacionais, não interações experimentais.','aid2go-network.svg')]
study = [
 ('volcano','Volcano','Vulcão','All finite gene results. Color: adjusted p < 0.05 and |log₂FC| ≥ 1. Overview capped at ±20 and −log₁₀(padj) = 100; uncapped figure and full data are linked below.','Todos os resultados gênicos finitos. Cor: p ajustado < 0,05 e |log₂FC| ≥ 1. Visão limitada a ±20 e −log₁₀(padj) = 100; figura completa e dados no link abaixo.','arabidopsis-volcano.svg'),
 ('gsea','GSEA','GSEA','Four strongest GO enrichment scores (NES) in each direction among terms with FDR < 0.05. Negative favors two-week apices; positive favors four-week inflorescences.','Os quatro maiores escores de enriquecimento GO (NES) em cada direção, entre termos com FDR < 0,05. Negativos favorecem ápices de duas semanas; positivos, inflorescências de quatro semanas.','arabidopsis-gsea.svg'),
 ('genes','Top genes','Genes em destaque','Five genes in each direction, ranked by signed DESeq2 Wald statistic. Positive values favor four-week inflorescences. Full tables accompany the figures.','Cinco genes em cada direção, ordenados pela estatística de Wald do DESeq2 com sinal. Valores positivos favorecem inflorescências de quatro semanas. Tabelas completas acompanham as figuras.','arabidopsis-top.svg'),
 ('pca','PCA','PCA','A six-sample overview from the saved AidCistrome analysis. Age and tissue differ together in this contrast; separation does not identify their independent effects.','Visão das seis amostras da análise salva do AidCistrome. Idade e tecido variam juntos neste contraste; a separação não identifica seus efeitos independentes.','arabidopsis/pca.png'),
 ('heatmap','Heatmap','Mapa de calor','Most-variable genes across the six samples. This exploratory pattern view complements the formal differential-expression analysis.','Genes mais variáveis entre as seis amostras. Esta visão exploratória complementa a análise formal de expressão diferencial.','arabidopsis/heatmap.png')]

source = '<!--examples:begin--><div class="hero-preview"><div class="window"><div class="window-bar"><span class="window-label">aidbio / field notes</span><div class="tabs" role="tablist" aria-label="Scientific examples" data-i18n-attr="aria-label:preview.label">'
for i,(family,label) in enumerate([('weather','AidWeather'),('gnn','Aid2GO'),('study','AidCistrome')]):
    source += f'<button class="tab" role="tab" id="tab-{family}" data-tab="{family}" aria-selected="{str(i==0).lower()}" tabindex="{0 if i==0 else -1}" aria-controls="panel-{family}" type="button">{label}</button>'
source += '</div></div><div class="family-stage">'
source += '<div class="panel" role="tabpanel" id="panel-weather" aria-labelledby="tab-weather"><div class="panel-head">'+translated('new.weather.head','A year in the field','Um ano no campo')+'<span class="tag tag-amber">NASA POWER</span></div>'+translated('new.weather.context','Jaguariúna, Brazil · 2024 · daily grid data','Jaguariúna, Brasil · 2024 · dados diários em grade','p','class="preview-context"')+previews('weather',weather)+'<div class="preview-links">'+translated('new.weather.report','Maize report (2022) →','Relatório do milho (2022) →','a','class="link-arrow" href="sample-report/index.html"')+translated('new.weather.data','Daily values + units','Valores diários + unidades','a','href="assets/examples/weather.json"')+'</div></div>'
source += '<div class="panel" role="tabpanel" id="panel-gnn" aria-labelledby="tab-gnn" hidden><div class="panel-head"><span>Aid2GO</span>'+translated('new.protein.status','Model in development','Modelo em desenvolvimento','span','class="tag tag-violet"')+'</div>'+translated('new.protein.context','Ontology, predictions and embedding neighborhoods','Ontologia, predições e vizinhanças de embeddings','p','class="preview-context"')+previews('protein',protein)+'<div class="preview-links">'+translated('new.protein.more','About Aid2GO →','Sobre o Aid2GO →','a','class="link-arrow" href="tools.html#aid2go"')+translated('new.protein.data','Data, protocol + test metrics','Dados, protocolo + métricas do teste','a','href="assets/examples/aid2go.json"')+'</div></div>'
source += '<div class="panel" role="tabpanel" id="panel-study" aria-labelledby="tab-study" hidden><div class="panel-head"><span>AidCistrome</span><span class="tag">PRJNA968041</span></div>'+translated('new.study.context','Arabidopsis · 4-week inflorescences / 2-week shoot apices','Arabidopsis · inflorescências de 4 semanas / ápices de 2 semanas','p','class="preview-context"')+previews('study',study)+'<div class="preview-links">'+translated('new.study.more','Full figures + study sources →','Figuras completas + fontes →','a','class="link-arrow" href="arabidopsis.html"')+'<a href="https://doi.org/10.1073/pnas.2221181120">Hu et al., PNAS (2023)</a></div></div></div>'
source += '<div class="window-foot">'+translated('new.preview.foot','Real application outputs · sources and methods included','Resultados reais das aplicações · fontes e métodos incluídos')+'</div></div></div><!--examples:end-->'
report_provenance = ROOT/'sample-report/provenance.json'
version = json.loads(report_provenance.read_text()).get('version','2024') if report_provenance.exists() else '2024'
source = source.replace('href="sample-report/index.html"', f'href="sample-report/index.html?v={version}"')
dialog = '<dialog class="plot-dialog" id="plot-dialog" aria-labelledby="plot-dialog-title"><div class="dialog-head">'+translated('plot.expanded','Figure detail','Detalhe da figura','h2','id="plot-dialog-title" class="h3"')+translated('plot.close','Close','Fechar','button','type="button" class="btn btn-secondary btn-sm" data-close-plot')+'</div>'+translated('plot.pan','On a small screen, scroll sideways to inspect the full-size figure.','Em telas pequenas, role para os lados para examinar a figura ampliada.','p','class="note"')+'<div class="plot-dialog-media" tabindex="0" role="region" aria-label="Full-size figure" data-i18n-attr="aria-label:plot.region"></div></dialog>'
index=ROOT/'index.html';content=index.read_text()
if '<!--examples:begin-->' in content:
    content=re.sub(r'<!--examples:begin-->.*?<!--examples:end-->',lambda _:source,content,flags=re.S)
else:
    start=content.index('<div class="hero-preview">');end=content.index('\n</div>\n</section>',start)
    content=content[:start]+source+content[end:]
content=re.sub(r'<dialog class="plot-dialog".*?</dialog>', '', content, flags=re.S)
content=content.replace('</main>',dialog+'</main>',1)
index.write_text(content)
copy_path.write_text('window.AIDBIO_STRINGS = '+json.dumps(copy,ensure_ascii=False,indent=2)+';\n')
print('Stamped 12 views across three application tabs, with EN/PT captions.')
