from flask import Blueprint, jsonify, request, make_response
from flask_cors import cross_origin
from azure.storage.blob import BlobServiceClient
from src.dto.UserDTO import *
from src.data.UserToDatabase import *
from src.data.AdressToDatabase import fetch_user_adress
from src.routes.auth import authorize, get_role

images_bp = Blueprint("images", __name__, url_prefix="/file")

# Create a BlobServiceClient using the connection string for your storage account
blob_service_client = BlobServiceClient.from_connection_string(
    'DefaultEndpointsProtocol=https;AccountName=pfeimages;AccountKey=qJsnpFU47OAFr6voB/vLbULP/AlGmv8ITHT9gXJ9IYuTP73CiXKHviWj5Q00AW6C3F//4GcNnJSB+AStlqY5qw==;EndpointSuffix=core.windows.net'
)


@images_bp.route("/upload-image", methods=["POST"])
@cross_origin()
def upload_image():
    # Get the image from the request
    print("ici")
    image = request.files['image']
    print(image)
    container_name = 'images'
    container_client = blob_service_client.create_container(container_name)
    print(container_client)
    # Upload the image to the container
    blob_client = container_client.upload_blob(image, blob_name=image.filename)

    return 'Image uploaded successfully'
