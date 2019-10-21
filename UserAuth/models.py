from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


def upload_profile_pic_path(instance, filename):
    return f'Profile/{filename}'

class CustomUser(AbstractUser):
    """
    One model for both User/Patient and Doctor. The model is extended using the Abstract User. A boolean field 'is_doctor' separates them.
    """
    is_doctor = models.BooleanField(default=False)
    pic = models.ImageField(upload_to = upload_profile_pic_path, default = 'Profile/index.png')

    def __str__(self):
        return str(self.username+" -> "+self.email + " -> " + str(self.is_doctor))