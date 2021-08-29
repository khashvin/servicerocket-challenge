import os
from werkzeug.datastructures import FileStorage

def test_base_route(client):
    response = client.get('/')
    assert response.status_code == 200

def test_upload_image_success(client):
    test_image = os.path.join("tests/files/test.png")
    image_file = FileStorage(
        stream=open(test_image, "rb"),
        filename="test.png",
        content_type="image/png"
    )

    response = client.post('/', content_type='multipart/form-data', data={
        "file": image_file
    })

    assert response.status_code == 201

def test_upload_invalid_file(client):
    test_txt = os.path.join("tests/files/test.txt")
    txt_file = FileStorage(
        stream=open(test_txt, "rb"),
        filename="test.txt",
        content_type="text/plain"
    )

    response = client.post('/', content_type='multipart/form-data', data={
        "file": txt_file
    })

    assert response.status_code == 404
