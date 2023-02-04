import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from user.managers import CustomUserManager


def get_hex_uuid():
    """
    uuid 생성 시 dash(-)를 제외한 문자열을 return 해주는 함수
    :return: 무작위 32자리 숫자+영어 문자열
    """
    return uuid.uuid4().hex


class User(AbstractUser):
    """
    id - UUID에서 dash(-)를 제외한 32자리 값
    username - 별도로 사용하지 않음
    email - 이메일을 아이디로 사용하는 user
    """
    id = models.CharField(
        default=get_hex_uuid(),
        primary_key=True,
        editable=False,
        max_length=32
    )

    username = None
    email = models.EmailField(
        'email',
        unique=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.id