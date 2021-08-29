import os
from flask import Flask, render_template, request
from config import config
from flask.helpers import send_from_directory
from service import UploadService

app = Flask(__name__)
app.config.from_object(config)

config.init_dirs()

@app.route("/", methods=['GET', 'POST'])
def index(error=''):
    if request.method == 'POST':
        return UploadService.upload_file(request)
    else:
        return render_template('index.html', error=error)

@app.route("/view")
def view_images(images):
    return render_template('view.html', images=images)

@app.route("/view/<name>")
def view(name):
    return send_from_directory(config.UPLOAD_FOLDER, name)