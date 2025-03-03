import base64
import uuid
from cloudinary.uploader import upload
from django.core.files.base import ContentFile

def decode_and_upload_to_cloudinary(base64_str):
    try:
        decoded_file = base64.b64decode(base64_str)
        file_name = f"{uuid.uuid4()}.jpg"  
        image = ContentFile(decoded_file, name=file_name)

        upload_result = upload(image)
        return upload_result['secure_url']
    except Exception as e:
        raise ValueError("Failed to upload image to Cloudinary.")