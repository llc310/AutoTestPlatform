from pathlib import Path

from django.contrib.auth.models import User
from django.db import models

from system.models import Role

# Create your models here.
app_path = Path(__file__).parent
app_static_path = app_path / "static"


def user_head_img_path(obj, filename):
    return f"{app_static_path}/user_{obj.user.id}/{filename}"

class HeadImg(models.Model):
    objects: models.QuerySet

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    head_img = models.FileField(verbose_name="头像", upload_to=user_head_img_path)


class Profile(models.Model):
    objects: models.QuerySet

    user = models.OneToOneField(to=User, on_delete=models.CASCADE)

    name = models.CharField(verbose_name="昵称", max_length=32)
    head_img = models.CharField(verbose_name="头像", max_length=255)

    def get_role_list(self):
        return Role.objects.filter(user=self.user)
