import re
from rest_framework.exceptions import ValidationError


class PasswordValidator:
    def validate(self, password, user=None):
        if not re.compile("^(?=.*[a-zA-Z])(?=.*[!@#$%^*+=-])(?=.*[0-9]).{8,}$").search(password):
            raise ValidationError('비밀번호는 특수문자, 숫자 포함 8자리 이상이어야 합니다.')

