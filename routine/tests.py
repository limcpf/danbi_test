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

    def test_enum_value(self):
        for day in ["MON", "TUE"]:
            day = Days[day].value
            RoutineDay.objects.create(day=day, routine_id=self.routine_id)

