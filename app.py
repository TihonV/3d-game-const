# app.py
from flask import Flask, request, jsonify, render_template, redirect, session, url_for, send_from_directory
from flask_cors import CORS  # <-- Добавляем CORS
from auth import register_user, verify_user
from storage import save_model, save_preview, save_public_project, load_public_projects, init_storage
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 't-studio-secret-2025'

# --- Включаем CORS для всех доменов ---
CORS(app, origins=["http://localhost:5500", "https://your-github-username.github.io", "http://127.0.0.1:5000"])

@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('profile'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if verify_user(username, password):
            session['user'] = username
            return redirect(url_for('profile'))
        return render_template('login.html', error="Неверный логин или пароль")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if register_user(username, password):
            session['user'] = username
            return redirect(url_for('profile'))
        return render_template('register.html', error="Пользователь уже существует")
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))
    projects = load_public_projects()
    user_projects = [p for p in projects if p.get('author') == session['user']]
    return render_template('profile.html', username=session['user'], projects=user_projects, all_projects=projects)

@app.route('/project/<int:pid>')
def project_view(pid):
    projects = load_public_projects()
    if pid < len(projects):
        proj = projects[pid]
        return render_template('project_view.html', project=proj, pid=pid)
    return "Проект не найден", 404

# --- API для конструктора ---

@app.route('/api/upload_model', methods=['POST'])
def api_upload_model():
    if 'file' not in request.files:
        return jsonify({"error": "Нет файла"}), 400
    file = request.files['file']
    url = save_model(file)
    return jsonify({"url": url})

@app.route('/api/publish', methods=['POST'])
def api_publish():
    if 'user' not in session:
        return jsonify({"error": "Не авторизован"}), 401

    title = request.form.get('title', 'Без названия')
    description = request.form.get('description', '')
    html_file = request.files.get('html_file')
    preview = request.files.get('preview')

    html_url = ''
    preview_url = '/static/default-preview.png'

    if html_file:
        html_url = f"/uploads/{session['user']}_{secure_filename(html_file.filename)}"
        os.makedirs('static/uploads', exist_ok=True)
        html_file.save(f"static/{html_url}")

    if preview:
        preview_url = save_preview(preview)

    project_data = {
        'author': session['user'],
        'title': title,
        'description': description,
        'html_url': html_url,
        'preview_url': preview_url,
        'likes': 0
    }

    save_public_project(project_data)
    return jsonify({"success": True, "message": "Проект опубликован!"})

@app.route('/uploads/<path:filename>')
def custom_uploads(filename):
    return send_from_directory('static/uploads', filename)

if __name__ == '__main__':
    init_storage()
    os.makedirs('static/uploads', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
