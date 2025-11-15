from flask import Flask, request, jsonify, render_template, send_from_directory, send_file
from sheets_auth import register_user, login_user
from yandex_api import yandex_geocode, yandex_tts
from storage import save_project, load_project, save_model
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/models'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    register_user(username, password)
    return jsonify({"success": True})

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if login_user(username, password):
        return jsonify({"success": True})
    return jsonify({"success": False}), 401

@app.route('/api/project', methods=['GET', 'POST'])
def api_project():
    if request.method == 'POST':
        data = request.json
        user_id = data.get('user_id')
        save_project(user_id, data.get('project'))
        return jsonify({"success": True})

    elif request.method == 'GET':
        user_id = request.args.get('user_id')
        project = load_project(user_id)
        return jsonify(project or {})

@app.route('/api/upload_model', methods=['POST'])
def api_upload_model():
    if 'file' not in request.files:
        return jsonify({"error": "No file"}), 400
    file = request.files['file']
    filename = file.filename
    save_model(file, filename)
    return jsonify({"url": f"/static/models/{filename}"})

@app.route('/api/yandex/geocode', methods=['POST'])
def api_yandex_geocode():
    data = request.json
    address = data.get('address')
    result = yandex_geocode(address)
    return jsonify(result)

@app.route('/api/yandex/tts', methods=['POST'])
def api_yandex_tts():
    data = request.json
    text = data.get('text')
    audio = yandex_tts(text)
    return send_file(audio, mimetype='audio/mpeg')

@app.route('/api/export_exe', methods=['POST'])
def api_export_exe():
    # В реальности это требует PyInstaller и сложной логики
    # Здесь просто заглушка
    return jsonify({"message": "EXE generation started. Check your email."})

@app.route('/static/models/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    os.makedirs('static/models', exist_ok=True)
    os.makedirs('projects', exist_ok=True)
    app.run(debug=True)
