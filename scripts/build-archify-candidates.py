#!/usr/bin/env python3
"""Write source-backed EN/PT Archify candidates for the homepage applications.

Run Archify `finalize dataflow` on each candidate after generation. The source
repositories are read only; candidates pin their current committed revisions.
"""

import json
import subprocess
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs/diagrams"
PT_VIEWER = json.loads((OUT / "pt-viewer.json").read_text())


def node(ident, kind, en, pt, stage, row, start, end):
    return (ident, kind, en, pt, stage, row, start, end)


SPECS = {
    "aidweather": {
        "repo": Path("/home/clever/aidbio/dev/aidweather"),
        "title": ("AidWeather: weather data with source context", "AidWeather: dados climáticos com contexto da fonte"),
        "stages": [("Inputs", "Entradas"), ("Retrieve", "Obter"), ("Prepare", "Preparar"), ("Deliver", "Entregar")],
        "nodes": [
            node("query", "external", "Place + dates", "Local + datas", 0, 1, 227, 230),
            node("power", "external", "POWER grid", "Grade POWER", 0, 3, 11, 15),
            node("client", "backend", "AidWeather", "AidWeather", 1, 1, 11, 17),
            node("metadata", "backend", "Grid + units", "Grade + unidades", 2, 0, 37, 44),
            node("cache", "database", "SQLite cache", "Cache SQLite", 2, 3, 13, 16),
            node("series", "database", "CSV + Python", "CSV + Python", 3, 1, 227, 249),
        ],
        "flows": [
            ("query", "client", "request", "pedido"),
            ("power", "client", "grid values", "valores da grade"),
            ("client", "metadata", "source details", "dados da fonte"),
            ("client", "cache", "reusable series", "séries em cache"),
            ("metadata", "series", "units + provenance", "unidades + fonte"),
            ("cache", "series", "cached values", "valores em cache"),
        ],
    },
    "report": {
        "repo": Path("/home/clever/aidbio/dev/aidweather-report"),
        "title": ("AidBio Weather Report: a portable field-season report", "Relatório Meteorológico AidBio: uma safra documentada"),
        "stages": [("Inputs", "Entradas"), ("Weather", "Clima"), ("Interpret", "Interpretar"), ("Deliver", "Entregar")],
        "nodes": [
            node("config", "external", "Site + season", "Local + safra", 0, 1, 50, 55),
            node("power", "external", "POWER series", "Séries POWER", 0, 3, 7, 10),
            node("features", "backend", "Daily metrics", "Métricas diárias", 1, 1, 57, 65),
            node("story", "backend", "Charts + context", "Gráficos + contexto", 2, 1, 66, 77),
            node("dashboard", "frontend", "Web report", "Relatório web", 3, 0, 307, 313),
            node("methods", "database", "Methods + data", "Métodos + dados", 3, 3, 309, 317),
        ],
        "flows": [
            ("config", "features", "place + dates", "local + datas"),
            ("power", "features", "daily grid data", "dados diários"),
            ("features", "story", "derived series", "séries derivadas"),
            ("story", "dashboard", "chapters", "capítulos"),
            ("story", "methods", "methods + charts", "métodos + figuras"),
        ],
    },
    "aidcistrome": {
        "repo": Path("/home/clever/aidbio/dev/aidcistrome"),
        "title": ("AidCistrome: SRA reads to candidate TF motifs", "AidCistrome: leituras SRA a motivos candidatos de TF"),
        "stages": [("Inputs", "Entradas"), ("Prepare", "Preparar"), ("Review + DE", "Revisão + DE"), ("Interpret", "Interpretar"), ("Deliver", "Entregar")],
        "nodes": [
            node("sra", "external", "Public SRA", "SRA público", 0, 0, 3, 10),
            node("profile", "database", "Genome + GO", "Genoma + GO", 0, 3, 13, 23),
            node("quant", "backend", "QC + counts", "QC + contagens", 1, 0, 3, 10),
            node("design", "backend", "Review design", "Revisar desenho", 2, 0, 30, 36),
            node("de", "backend", "DESeq2", "DESeq2", 2, 3, 44, 49),
            node("sets", "backend", "GO gene sets", "Conjuntos GO", 3, 0, 44, 49),
            node("motifs", "backend", "TF motifs", "Motivos de TF", 3, 3, 51, 54),
            node("figures", "database", "Plots + TFs", "Gráficos + TFs", 4, 1, 44, 54),
        ],
        "flows": [
            ("sra", "quant", "reads", "leituras"),
            ("profile", "quant", "reference", "referência"),
            ("quant", "design", "sample counts", "contagens"),
            ("design", "de", "approved contrasts", "contrastes"),
            ("de", "sets", "ranked genes", "genes ordenados"),
            ("sets", "motifs", "selected sets", "conjuntos"),
            ("sets", "figures", "GO results", "resultados GO"),
            ("motifs", "figures", "motif candidates", "motivos candidatos"),
        ],
    },
    "aid2go": {
        "repo": Path("/home/clever/aidbio/dev/aid2go"),
        "title": ("Aid2GO: protein evidence to predicted GO terms", "Aid2GO: evidências de proteínas a termos GO previstos"),
        "stages": [("Inputs", "Entradas"), ("Represent", "Representar"), ("Model", "Modelar"), ("Deliver", "Entregar")],
        "nodes": [
            node("proteins", "external", "Proteins", "Proteínas", 0, 0, 5, 8),
            node("go", "external", "Known GO", "GO conhecido", 0, 3, 5, 9),
            node("embeddings", "backend", "Embeddings", "Vetores", 1, 0, 54, 56),
            node("graph", "backend", "GO graph", "Grafo GO", 1, 3, 55, 58),
            node("predict", "backend", "GNN scores", "Escores GNN", 2, 1, 36, 48),
            node("terms", "database", "Predicted GO", "GO previsto", 3, 0, 179, 184),
            node("eval", "database", "Internal test", "Teste interno", 3, 3, 171, 176),
        ],
        "flows": [
            ("proteins", "embeddings", "sequences", "sequências"),
            ("go", "graph", "GO + labels", "GO + rótulos"),
            ("embeddings", "graph", "similarity", "similaridade"),
            ("graph", "predict", "typed edges", "arestas tipadas"),
            ("predict", "terms", "scores", "escores"),
            ("predict", "eval", "held-out scores", "escores retidos"),
        ],
    },
    "aidwiki": {
        "repo": Path("/home/clever/aidbio/apps/aidwiki"),
        "title": ("AidWiki: a curated library with evidence links", "AidWiki: biblioteca curada com vínculos às evidências"),
        "stages": [("Inputs", "Entradas"), ("Register", "Registrar"), ("Verify", "Verificar"), ("Curate", "Curar"), ("Use", "Usar")],
        "nodes": [
            node("sources", "external", "Project sources", "Fontes do projeto", 0, 1, 3, 12),
            node("raw", "database", "Source copies", "Cópias das fontes", 1, 1, 7, 9),
            node("evidence", "backend", "Verify quotes", "Verificar trechos", 2, 0, 7, 10),
            node("claims", "database", "Claim ledger", "Registro de fatos", 2, 3, 9, 10),
            node("library", "database", "Curated library", "Biblioteca curada", 3, 1, 8, 12),
            node("wiki", "frontend", "AidWiki", "AidWiki", 4, 1, 45, 68),
        ],
        "flows": [
            ("sources", "raw", "registered copies", "cópias registradas"),
            ("raw", "evidence", "source text", "texto da fonte"),
            ("evidence", "claims", "verified locators", "trechos verificados"),
            ("claims", "library", "traceable claims", "afirmações rastreáveis"),
            ("library", "wiki", "pages + links", "páginas + links"),
        ],
    },
}


def command(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout.strip()


def safe_origin(raw: str) -> str:
    if raw.startswith(("http://", "https://")):
        parsed = urlsplit(raw)
        raw = urlunsplit((parsed.scheme, parsed.hostname or "", parsed.path, parsed.query, parsed.fragment))
    return raw


def write(slug: str, spec: dict, lang: str) -> None:
    i = 0 if lang == "en" else 1
    folder = OUT / f"{slug}-{lang}"
    folder.mkdir(parents=True, exist_ok=True)
    candidate = {
        "schema_version": 1,
        "diagram_type": "dataflow",
        "meta": {
            "title": spec["title"][i],
            "locale": "en" if lang == "en" else "pt-BR",
            "output": f"docs/diagrams/{slug}-{lang}/diagram.html",
            "quality_profile": "showcase",
            "repository": {
                "url": safe_origin(command(spec["repo"], "remote", "get-url", "origin")),
                "revision": command(spec["repo"], "rev-parse", "HEAD"),
                "link_mode": "local-only",
            },
        },
        "stages": [{"label": pair[i]} for pair in spec["stages"]],
        "nodes": [
            {
                "id": ident,
                "type": kind,
                "label": en if i == 0 else pt,
                "stage": stage,
                "row": row,
                "sources": [{"path": "README.md", "line": start, "end_line": end}],
            }
            for ident, kind, en, pt, stage, row, start, end in spec["nodes"]
        ],
        "flows": [
            {"from": src, "to": dst, "label": en if i == 0 else pt}
            for src, dst, en, pt in spec["flows"]
        ],
    }
    if lang == "pt":
        candidate["meta"]["translations"] = PT_VIEWER
    (folder / "candidate.json").write_text(json.dumps(candidate, ensure_ascii=False, indent=2) + "\n")
    print(folder / "candidate.json")


if __name__ == "__main__":
    for slug, spec in SPECS.items():
        for lang in ("en", "pt"):
            write(slug, spec, lang)
