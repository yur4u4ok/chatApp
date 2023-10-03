import os

from django.core.exceptions import ValidationError

from PIL import Image


def validate_icon_image_size(image):
    if image:
        with Image.open(image) as img:
            if img.width > 70 or img.height > 70:
                raise ValidationError(
                    f'image size must be 70x70, your image size is {img.size}'
                )


def validate_image_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    if not ext in valid_extensions:
        raise ValidationError('Unsupported file extension')
