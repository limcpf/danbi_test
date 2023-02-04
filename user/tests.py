import django
import os

from django.test import TestCase
from rest_framework import status

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'routine_prj.settings')
django.setup()

path_create = "/user/"
path_login = "/user/login/"

email = "limc@test.co.kr"
fake_email = "limc1@test.co.kr"
pwd = "test1234!"

error_text_pwd = "비밀번호는 특수문자, 숫자 포함 8자리 이상이어야 합니다."
error_overlap_email = "이미 이 이메일 주소로 등록된 사용자가 있습니다."
error_blank_field = "이 필드는 blank일 수 없습니다."
error_fail_login = "주어진 자격 증명으로 로그인이 불가능합니다."


class UserTests(TestCase):
    pk = 0

    # 테스트 시작 시 create
    def setUp(self) -> None:
        result = self.client.post(
            path=path_create,
            data={
                "email": email,
                "password1": pwd,
                "password2": pwd
            }
        )

        self.pk = result.json()["user"]["pk"]

    # 중복 계정 테스트
    def test_create_user_overlap_email(self):
        result = self.client.post(
            path=path_create,
            data={
                "email": email,
                "password1": pwd,
                "password2": pwd
            }
        )

        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(result.json()["email"][0], error_overlap_email)

    # 아이디 없는 경우(특수문자 없음)
    def test_create_user_error_no_email(self):
        result = self.client.post(
            path=path_create,
            data={
                "email": "",
                "password1": "test1234!",
                "password2": "test1234!"
            }
        )

        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(result.json()["email"][0], error_blank_field)

    def test_create_user_error_no_pwd1(self):
        result = self.client.post(
            path=path_create,
            data={
                "email": fake_email,
                "password1": "",
                "password2": pwd
            }
        )

        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(result.json()["password1"][0], error_blank_field)

    def test_create_user_error_no_pwd2(self):
        result = self.client.post(
            path=path_create,
            data={
                "email": fake_email,
                "password1": pwd,
                "password2": ""
            }
        )

        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(result.json()["password2"][0], error_blank_field)

    # 비밀번호 정합성 테스트(특수문자 없음)
    def test_create_user_error_pwd_special_symbols(self):
        result = self.client.post(
            path=path_create,
            data={
                "email": fake_email,
                "password1": "test1234",
                "password2": "test1234"
            }
        )

        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(result.json()["password1"][0], error_text_pwd)

    # 비밀번호 정합성 테스트(숫자 없음)
    def test_create_user_error_pwd_number(self):
        result = self.client.post(
            path=path_create,
            data={
                "email": fake_email,
                "password1": "test!!!!",
                "password2": "test!!!!"
            }
        )

        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(result.json()["password1"][0], error_text_pwd)

    # 비밀번호 정합성 테스트(영어 없음)
    def test_create_user_error_pwd_english(self):
        result = self.client.post(
            path=path_create,
            data={
                "email": fake_email,
                "password1": "!!!!1234",
                "password2": "!!!!1234"
            }
        )

        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(result.json()["password1"][0], error_text_pwd)

    # 로그인 테스트
    def test_login(self):
        result = self.client.post(
            path=path_login,
            data={
                "email": email,
                "password": pwd
            }
        )

        res_json = result.json()

        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(res_json["access_token"])
        self.assertEqual(res_json["user"]["pk"], self.pk)

    # 로그인 테스트
    def test_login_error(self):
        result = self.client.post(
            path=path_login,
            data={
                "email": fake_email,
                "password": pwd
            }
        )
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(result.json()["non_field_errors"][0], error_fail_login)
