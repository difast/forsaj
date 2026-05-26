import os
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='.')
CORS(app)

BOT_TOKEN = os.environ.get('BOT_TOKEN', '8417564515:AAEWXeF0gUeasBeuaIF8zzwBluPPDALZnbs')
CHAT_IDS  = os.environ.get('CHAT_IDS', '7738750071,568686237').split(',')


@app.route('/')
def index():
    return send_from_directory('.', 'forsazh_v3.html')


@app.route('/submit', methods=['POST'])
def submit():
    data  = request.get_json(silent=True) or {}
    name  = str(data.get('name',  '')).strip()
    phone = str(data.get('phone', '')).strip()

    service = str(data.get('service', '')).strip()
    org     = str(data.get('org',     '')).strip()

    if not name or not phone:
        return jsonify({'ok': False, 'error': 'missing_fields'}), 400

    lines = ["\U0001f514 Новая заявка с сайта АК Форсаж", ""]
    lines.append(f"\U0001f464 Имя: {name}")
    lines.append(f"\U0001f4de Телефон: {phone}")
    if service:
        lines.append(f"\U0001f4cb Услуга: {service}")
    if org:
        lines.append(f"\U0001f3e2 Организация: {org}")
    text = "\n".join(lines)

    for cid in CHAT_IDS:
        cid = cid.strip()
        if not cid:
            continue
        try:
            requests.post(
                f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',
                json={'chat_id': cid, 'text': text},
                timeout=15
            )
        except Exception:
            pass

    return jsonify({'ok': True})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
