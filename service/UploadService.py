import os
from zipfile import ZipFile
from flask import request, make_response
from werkzeug.utils import secure_filename
from config import config

def allowed_file(mimetype):
    return mimetype in config.ALLOWED_EXTENSIONS

def get_extension(filename):
    return '.'+filename.split(".")[1]

def isZip(mimetype):
    return mimetype == 'application/zip' or mimetype == 'application/x-zip-compressed'

def upload_file(request: request):
    if 'file' not in request.files:
        error = { "error" : "No file chosen!"}
        return make_response(error, 404)

    file = request.files['file']

    if(file.filename == ''):
        error = {"error" : "No file chosen!"}
        return make_response(error, 404)

    if file and allowed_file(file.mimetype):

        if isZip(file.mimetype):
            image_list = extract_images(file)
            if image_list:
                filesJson = { "files" : image_list}
                return make_response(filesJson, 201)
            else:
                error = {"error" : "No images found in archive!"}
                return make_response(error, 404)
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(config.UPLOAD_FOLDER, filename))
            fileJson = {"file" : request.base_url + "view/" + filename}
            return make_response(fileJson, 201)
    else:
        error = {"error" : "Invalid file. File is not an image or archive!"}
        return make_response(error, 404)

def extract_images(file):
    zip = ZipFile(file)
    filelist = zip.namelist()
    images = []
    for filename in filelist:
        if get_extension(filename) == '.png' or get_extension(filename) == '.jpg' or get_extension(filename) == '.jpeg':
            zip.extract(filename, os.path.join(config.UPLOAD_FOLDER))
            images.append(request.base_url + "view/" + filename)
    return images

