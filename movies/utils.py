import base64
import imghdr
import logging

from cloudinary.uploader import upload
from django.core.files.base import ContentFile

logger = logging.getLogger(__name__)

def decode_and_upload_to_cloudinary(base64_str, folder_name, file_name):
    try:
        format_map = {
            "jpeg": "jpg",
            "png": "png",
            "gif": "gif",
            "webp": "webp"
        }
        
        decoded_file = base64.b64decode(base64_str)
        
        file_format = imghdr.what(None, decoded_file)  
        file_extension = format_map.get(file_format, "jpg")

        full_file_name = f"{file_name}.{file_extension}"
        image = ContentFile(decoded_file, name=full_file_name)

        upload_result = upload(
            image, folder=folder_name, public_id=file_name, overwrite=True
        )

        return upload_result["secure_url"]

    except Exception as e:
        logger.error(f"Cloudinary upload failed: {e}")
        raise ValueError("Failed to upload image to Cloudinary.")