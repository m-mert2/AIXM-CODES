import os
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from pda_validator import run_pda, PDA_RULES
from scenarios import SCENARIOS
from xml_parser import xml_to_pda_tokens, detect_feature, is_aixm_basic_message, split_aixm_message
from xml_generator import GENERATOR_SCENARIOS, generate as gen_xml
from map_extractor import extract_features as _extract_features

app = Flask(__name__)
CORS(app)

_MAP_CACHE = None

# ── Sayfa ─────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    themes = {}
    for s in SCENARIOS:
        t = s['tema']
        if t not in themes:
            themes[t] = []
        themes[t].append(s)
    return render_template('index.html', scenarios=SCENARIOS, themes=themes)

# ── Senaryo ───────────────────────────────────────────────────────────────────
@app.route('/api/scenario/<int:scenario_id>')
def get_scenario(scenario_id):
    scenario = next((s for s in SCENARIOS if s['id'] == scenario_id), None)
    if not scenario:
        return jsonify({'error': 'Senaryo bulunamadı'}), 404
    return jsonify(scenario)

@app.route('/api/validate', methods=['POST'])
def validate():
    data = request.json
    result = run_pda(data.get('feature'), data.get('tokens', []))
    return jsonify(result)

@app.route('/api/validate_scenario/<int:scenario_id>')
def validate_scenario(scenario_id):
    scenario = next((s for s in SCENARIOS if s['id'] == scenario_id), None)
    if not scenario:
        return jsonify({'error': 'Senaryo bulunamadı'}), 404
    results = []
    all_accepted = True
    for f in scenario['features']:
        result = run_pda(f['feature'], f['tokens'])
        results.append({'feature': f['feature'], 'aciklama': f['aciklama'], 'tokens': f['tokens'], 'result': result})
        if not result['accepted']:
            all_accepted = False
    return jsonify({'scenario': scenario, 'results': results, 'all_accepted': all_accepted})

# ── XML Doğrulama ─────────────────────────────────────────────────────────────
@app.route('/api/validate_xml', methods=['POST'])
def validate_xml():
    data = request.json
    xml_string = data.get('xml', '')

    if is_aixm_basic_message(xml_string):
        try:
            members = split_aixm_message(xml_string)
        except ValueError as e:
            return jsonify({'error': f'AIXMBasicMessage ayrıştırılamadı: {e}'}), 400
        if not members:
            return jsonify({'error': 'AIXMBasicMessage içinde hiç feature bulunamadı.'}), 400

        results = []
        stats = {'total': len(members), 'accepted': 0, 'rejected': 0, 'skipped': 0}
        for member_xml in members:
            feature = detect_feature(member_xml)
            if not feature or feature not in PDA_RULES:
                stats['skipped'] += 1
                results.append({'feature': feature or '?', 'tokens': [], 'result': {'accepted': None, 'steps': [], 'error': 'Kural yok'}, 'skipped': True})
                continue
            tokens = xml_to_pda_tokens(member_xml)
            result = run_pda(feature, tokens)
            stats['accepted' if result['accepted'] else 'rejected'] += 1
            results.append({'feature': feature, 'tokens': tokens, 'result': result, 'skipped': False})
        return jsonify({'mode': 'bulk', 'stats': stats, 'results': results})

    feature = detect_feature(xml_string)
    if not feature:
        return jsonify({'error': 'Feature tespit edilemedi.'}), 400
    if feature not in PDA_RULES:
        return jsonify({'error': f'"{feature}" için PDA kuralı tanımlanmamış.'}), 400
    tokens = xml_to_pda_tokens(xml_string)
    result = run_pda(feature, tokens)
    return jsonify({'mode': 'single', 'feature': feature, 'tokens': tokens, 'result': result})

@app.route('/api/features')
def get_features():
    return jsonify(list(PDA_RULES.keys()))

# ── Generator ─────────────────────────────────────────────────────────────────
@app.route('/api/generator/scenarios')
def generator_scenarios():
    return jsonify(GENERATOR_SCENARIOS)

@app.route('/api/generator/generate', methods=['POST'])
def generator_generate():
    data = request.json
    try:
        xml_out = gen_xml(data.get('scenario_id'), data.get('params', {}))
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    feature = detect_feature(xml_out)
    tokens  = xml_to_pda_tokens(xml_out)
    result  = run_pda(feature, tokens) if feature in PDA_RULES else {'accepted': None, 'steps': [], 'error': 'Kural yok'}
    return jsonify({'xml': xml_out, 'feature': feature, 'tokens': tokens, 'result': result})

# ── Harita ────────────────────────────────────────────────────────────────────
@app.route('/api/map/features')
def map_features():
    global _MAP_CACHE
    if _MAP_CACHE is None:
        for path in [os.path.join(os.path.dirname(__file__), 'Donlon.xml'), '/mnt/user-data/uploads/Donlon.xml']:
            if os.path.exists(path):
                _MAP_CACHE = _extract_features(path)
                break
        if _MAP_CACHE is None:
            return jsonify({'error': 'Donlon.xml bulunamadı.'}), 404
    return jsonify(_MAP_CACHE)

@app.route('/api/map/upload', methods=['POST'])
def map_upload():
    global _MAP_CACHE
    xml_string = request.json.get('xml', '')
    if not xml_string:
        return jsonify({'error': 'XML boş'}), 400
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False, encoding='utf-8') as f:
        f.write(xml_string)
        tmp = f.name
    try:
        _MAP_CACHE = _extract_features(tmp)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        os.unlink(tmp)
    return jsonify({'count': len(_MAP_CACHE)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
