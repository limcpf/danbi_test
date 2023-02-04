from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, passwrod, **extra_fields):
        # 이메일이 존재 하지 않는 경우
        if not email:
            raise ValueError('이메일은 필수 값 입니다.')
        # 이메일 정규화, at(@)을 기준으로 문자열을 나눈 뒤 도메인을 소문자화함
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        # 패스워드 암호화
        user.set_password(passwrod)
        user.save()
        return user

    def create_superuser(self, email, passwrod, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('관리자 계정은 staff 여부가 True 여야 합니다.')
        elif extra_fields.get('is_superuser') is not True:
            raise ValueError('관리자 계정은 관리자 여부가 True 여야 합니다.')
        return self.create_user(email, passwrod, **extra_fields)