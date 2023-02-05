import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from user.managers import CustomUserManager


class User(AbstractUser):
    """
    id - UUID에서 dash(-)를 제외한 32자리 값
    username - 별도로 사용하지 않음
    email - 이메일을 아이디로 사용하는 user
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    username = None
    email = models.EmailField(
        'email',
        unique=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.id.__str__()
