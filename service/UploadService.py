import os
from zipfile import ZipFile
from flask import request, make_response
from werkzeug.utils import secure_filename
from config import config
from PIL import Image

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
            resized_image_list = resize_images_zip(image_list)
            if image_list:
                filesJson = { "files" : resized_image_list }
                return make_response(filesJson, 201)
            else:
                error = {"error" : "No images found in archive!"}
                return make_response(error, 404)
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(config.UPLOAD_FOLDER, filename))
            resize_images(filename, 32)
            resize_images(filename, 64)
            fileJson = {
                "file" : request.base_url + "view/" + filename,
                "file32": request.base_url + "view/" + "32-" + filename,
                "file64": request.base_url + "view/" + "64-" + filename
            }
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
            images.append(filename)
    return images

def resize_images(filename, size):
    im = Image.open("static/" + filename)
    width, height = im.size
    if width > 128:
        resize_ratio = width/size
        new_height = int(height/resize_ratio)
        new_size = (size, new_height)
        new_image = im.resize(new_size)
        new_image.save(os.path.join(config.UPLOAD_FOLDER + "/" + str(size) + "-" + filename))

def resize_images_zip(imagelist):
    resized_list = []
    for img in imagelist:
        resize_images(img, 32)
        resize_images(img, 64)
        fileJson = {
            "file" : request.base_url + "view/" + img,
            "file32": request.base_url + "view/" + "32-" + img,
            "file64": request.base_url + "view/" + "64-" + img
        }
        resized_list.append(fileJson)
    return resized_list
