# storage.py
import json
import os
from werkzeug.utils import secure_filename

UPLOADS_DIR = 'static/uploads'

def init_storage():
    os.makedirs(os.path.join(UPLOADS_DIR, 'models'), exist_ok=True)
    os.makedirs(os.path.join(UPLOADS_DIR, 'previews'), exist_ok=True)

def save_model(file):
    init_storage()
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOADS_DIR, 'models', filename)
    file.save(filepath)
    return f"/static/uploads/models/{filename}"

def save_preview(image_file):
    init_storage()
    filename = secure_filename(image_file.filename)
    filepath = os.path.join(UPLOADS_DIR, 'previews', filename)
    image_file.save(filepath)
    return f"/static/uploads/previews/{filename}"

def save_public_project(data):
    PROJECTS_FILE = 'projects.json'
    projects = []
    if os.path.exists(PROJECTS_FILE):
        with open(PROJECTS_FILE, 'r', encoding='utf-8') as f:
            projects = json.load(f)
    projects.append(data)
    with open(PROJECTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(projects, f, ensure_ascii=False, indent=2)

def load_public_projects():
    PROJECTS_FILE = 'projects.json'
    if os.path.exists(PROJECTS_FILE):
        with open(PROJECTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []
