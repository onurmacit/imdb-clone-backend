import base64

from cloudinary.uploader import upload
from django.core.files.base import ContentFile


def decode_and_upload_to_cloudinary(base64_str, category_name):
    try:
        decoded_file = base64.b64decode(base64_str)
        file_name = f"{category_name}.jpg"
        image = ContentFile(decoded_file, name=file_name)
        upload_result = upload(
            image, folder="categories", public_id=category_name, overwrite=True
        )

        return upload_result["secure_url"]
    except Exception:
        raise ValueError("Failed to upload image to Cloudinary.")
