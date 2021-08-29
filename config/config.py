import os

BASE_URL="http://127.0.0.1:5000/"
UPLOAD_FOLDER='static'
ALLOWED_EXTENSIONS={'image/jpeg', 'image/png', 'application/zip', 'application/x-zip-compressed'}

def init_dirs():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)