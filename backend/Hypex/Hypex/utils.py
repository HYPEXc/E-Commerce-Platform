import os
import uuid
from django.utils import timezone


def unique_file_name(base_path, filename):
    ext = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4()}_{int(timezone.now().timestamp())}.{ext}"
    return os.path.join(base_path, new_filename)
