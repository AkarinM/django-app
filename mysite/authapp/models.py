from django.contrib.auth.models import User
from django.db import models


def avatar_path(instance: 'Profile', filename: str) -> str:
    '''
    Генерирует путь до аватара в профиле
    :param instance: Объект профиля
    :param filename: название файла
    :return: Путь до аватара
    '''

    return "avatar/{}/{}".format(instance.user.pk, filename)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, null=True)
    avatar = models.ImageField(null=True, blank=True, upload_to=avatar_path)

