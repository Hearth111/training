import json
import os
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

DATA_FILE = 'data.json'
TECH_FILE = 'tech.json'


def load_data(path):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_data(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/menu.html')
def menu():
    return send_from_directory('.', 'menu.html')


@app.route('/api/records', methods=['GET'])
def get_records():
    return jsonify(load_data(DATA_FILE))


@app.route('/api/records/<date>', methods=['GET', 'POST'])
def record(date):
    data = load_data(DATA_FILE)
    if request.method == 'GET':
        return jsonify(data.get(date))
    else:
        data[date] = request.get_json(silent=True)
        save_data(DATA_FILE, data)
        return jsonify({'success': True})


@app.route('/api/tech/<week>', methods=['GET', 'POST'])
def tech(week):
    data = load_data(TECH_FILE)
    if request.method == 'GET':
        return jsonify(data.get(week))
    else:
        data[week] = request.get_json(silent=True)
        save_data(TECH_FILE, data)
        return jsonify({'success': True})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
