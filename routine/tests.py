from datetime import date, datetime

from django.test import TestCase

from routine.enums import Days, RoutineCategory, DaysChoices
from routine.models import RoutineDay, Routine
from user.tests import path_create, path_login


class EnumTests(TestCase):
    def setUp(self):
        account = self.client.post(
            path=path_create,
            data={
                "email": "limc@test.co.kr",
                "password1": "test1234!",
                "password2": "test1234!"
            }
        )

        self.account_id = account.json()["user"]["pk"]

        routine = Routine.objects.create(
            title="title",
            category="H",
            goal="goal",
            is_alarm=False,
            account_id=self.account_id
        )

        self.routine_id = routine.routine_id


    def test_date(self):
        today = '2023-02-04'
        day = date.weekday(datetime.strptime(today, "%Y-%m-%d"))
        self.assertEqual(day, 5)  # 토요일

        today = ''
        try:
            day = date.weekday(datetime.strptime(today, "%Y-%m-%d"))
            self.assertTrue(False, msg="빈 값인데 날짜가 생성됨")
        except ValueError as e:
            self.assertTrue(True)
        except:
            self.assertTrue(False, msg="의도치 않은 에러")


