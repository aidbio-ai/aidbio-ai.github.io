#!/usr/bin/env python3
"""Check scientific example integrity, source tables, units and provenance hashes."""
import csv
from datetime import date, timedelta
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = ROOT/'assets/examples'


def check():
    manifest = json.loads((EXAMPLES/'manifest.json').read_text())
    for name, expected in manifest['outputs'].items():
        actual = hashlib.sha256((EXAMPLES/name).read_bytes()).hexdigest()
        assert actual == expected, f'Changed asset without refreshed provenance: {name}'
    weather = json.loads((EXAMPLES/'weather.json').read_text())
    rows = weather['daily']
    assert len(rows) == 366
    for i, row in enumerate(rows):
        assert row['date'] == str(date(2024,1,1)+timedelta(days=i)), 'Missing or duplicate day'
        assert all(math.isfinite(value) for key,value in row.items() if key != 'date')
        assert row['T2M_MIN'] <= row['T2M'] <= row['T2M_MAX']
        assert row['PRECTOTCORR'] >= 0 and 0 <= row['RH2M'] <= 100
        assert all(0 <= row[key] <= 1 for key in ['GWETTOP','GWETROOT','GWETPROF'])
        vpd = .6108*math.exp(17.27*row['T2M']/(row['T2M']+237.3))*(1-row['RH2M']/100)
        assert math.isclose(row['VPD'],vpd,rel_tol=1e-12)
    assert weather['units']['PS'] == 'kPa'
    model = json.loads((EXAMPLES/'aid2go.json').read_text())
    assert model['model_status'] == 'in development'
    assert model['threshold_source'] == 'validation'
    assert 'protein-held-out' in model['protocol']
    assert model['overall']['proteins'] == 100 and model['overall']['go_terms'] == 100
    known = [r for r in model['predictions'] if r['annotated']]
    assert len(known) == 5
    assert sum(r['score'] >= model['threshold'] for r in known) == 2
    assert len(model['predictions']) == 7
    assert all(0 <= r['score'] <= 1 for r in model['predictions'])
    terms = model['projection']['terms']
    assert len(terms) == len({r['id'] for r in terms}) == 1000
    assert all(all(math.isfinite(v) for v in t['tsne']) for t in terms)
    network = model['protein_network']
    nodes = {n['id'] for n in network['nodes']}
    assert len(nodes) == 35 and len(network['edges']) == 153
    assert all(e['source'] in nodes and e['target'] in nodes for e in network['edges'])
    assert {e['relation'] for e in model['ontology']['edges']} == {'is_a','part_of'}
    study = EXAMPLES/'arabidopsis'
    metadata = json.loads((study/'metadata.json').read_text())
    de = list(csv.DictReader((study/'deseq2_4_week_vs_2_week.csv').open()))
    assert len(de) == metadata['n_genes_post_filter']
    assert metadata['n_samples'] == len(metadata['samples']) == 6
    assert sorted(s['age'] for s in metadata['samples']) == ['2_week']*3+['4_week']*3
    assert metadata['contrast'] == {'factor':'age','numerator':'4_week','denominator':'2_week'}
    qvalues = [float(r['padj']) for r in de if r['padj'] not in ['NA','NaN','']]
    assert all(0 <= q <= 1 for q in qvalues)
    assert sum(q < .05 for q in qvalues) == metadata['n_significant_padj0.05']
    provenance = json.loads((ROOT/'sample-report/provenance.json').read_text())
    for name, expected in provenance['export_sha256'].items():
        assert hashlib.sha256((ROOT/'sample-report'/name).read_bytes()).hexdigest() == expected, name
    report_rows = list(csv.DictReader((ROOT/'sample-report/weather_data.csv').open()))
    first, last = [date.fromisoformat(value) for value in provenance['period'].split('/')]
    assert len(report_rows) == provenance['observations'] == (last-first).days+1
    assert [row['date'] for row in report_rows] == [str(first+timedelta(days=i)) for i in range(len(report_rows))]
    assert all(math.isfinite(float(row['T2M'])) for row in report_rows)
    assert provenance['source_sha256']['weather_data.csv'] == provenance['export_sha256']['weather_data.csv']
    print('Example checksums, 366 preview records, VPD/units, held-out predictions, graphs, study contrast and independently dated report data pass.')


if __name__ == '__main__':
    check()
