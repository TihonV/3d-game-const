import json
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/models'
PROJECTS_FOLDER = 'projects'

def save_project(user_id, project_data):
    filename = f"{user_id}_project.json"
    filepath = os.path.join(PROJECTS_FOLDER, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(project_data, f, ensure_ascii=False, indent=2)

def load_project(user_id):
    filename = f"{user_id}_project.json"
    filepath = os.path.join(PROJECTS_FOLDER, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def save_model(file, filename):
    filename = secure_filename(filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    return filepath
