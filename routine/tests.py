import json
from datetime import date, datetime, timedelta

from django.test import TestCase

from routine.enums import Days, RoutineCategory, DaysChoices, ResponseEnum
from routine.models import RoutineDay, Routine, RoutineResult
from user.tests import path_create, path_login

_title = "title"
_category = "H"
_goal = "goal"
_is_alarm = False
_days = ["MON"]

_title2 = "title2"
_category2 = "H"
_goal2 = "goal2"
_is_alarm2 = True
_days2 = ["TUE"]

routine_path = "/routine/"

error_message_1 = "이 필드는 필수 항목입니다."
error_message_2 = "존재하지 않는 Routine 입니다.";

_another_email = "test@test.co.kr"
_email = "limc@test.co.kr"
_password = "test1234!"


def get_account_id_from_create_user(self, email=_email, password=_password):
    account = self.client.post(
        path=path_create,
        data={
            "email": email,
            "password1": password,
            "password2": password
        }
    )

    return account.json()["user"]["pk"]


def get_routine_for_create(title=_title, category=_category, goal=_goal, is_alarm=_is_alarm, days=_days):
    return {
        "title": title,
        "category": category,
        "goal": goal,
        "is_alarm": is_alarm,
        "days": days
    }


class RoutineCreateTest(TestCase):
    def setUp(self):
        self.account_id = get_account_id_from_create_user(self)
        self.client.login(email="limc@test.co.kr", password="test1234!")

    def test_create_routine_1(self):
        """
        정상 케이스(Category H)
        """
        result = self.client.post(
            routine_path,
            data=get_routine_for_create()
        )

        routine_id = result.data['data']['routine_id']
        routine = Routine.objects.get(routine_id=routine_id)
        routine_result = RoutineResult.objects.get(routine_id=routine_id)
        routine_day = RoutineDay.objects.filter(routine_id=routine_id).all()

        self.assertEqual(routine.title, _title)
        self.assertEqual(routine.category, _category)
        self.assertEqual(routine.goal, _goal)
        self.assertEqual(routine.is_alarm, _is_alarm)
        self.assertEqual(routine.is_deleted, False)
        self.assertEqual(routine_result.result, "N")
        self.assertEqual(len(routine_day), 1)

    def test_create_routine_2(self):
        """
        정상 케이스(Category M)
        """
        result = self.client.post(
            routine_path,
            data=get_routine_for_create(is_alarm=True, category=RoutineCategory.MIRACLE.value)
        )

        routine_id = result.data['data']['routine_id']
        routine = Routine.objects.get(routine_id=routine_id)
        routine_result = RoutineResult.objects.get(routine_id=routine_id)
        routine_day = RoutineDay.objects.filter(routine_id=routine_id).all()

        self.assertEqual(routine.title, _title)
        self.assertEqual(routine.category, RoutineCategory.MIRACLE.value)
        self.assertEqual(routine.goal, _goal)
        self.assertEqual(routine.is_alarm, True)
        self.assertEqual(routine.is_deleted, False)
        self.assertEqual(routine_result.result, "N")
        self.assertEqual(len(routine_day), 1)

    def test_create_routine_day_7(self):
        """
        정상 케이스(day 7일)
        """
        result = self.client.post(
            routine_path,
            data=get_routine_for_create(days=["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"])
        )

        routine_id = result.data['data']['routine_id']
        routine_day = RoutineDay.objects.filter(routine_id=routine_id).all()

        self.assertEqual(len(routine_day), 7)

    def test_create_routine_is_alarm_none(self):
        """
        정상 케이스(알람여부 없는 경우)
        """
        data = get_routine_for_create()
        data.pop("is_alarm")

        result = self.client.post(
            routine_path,
            data=data
        )

        routine_id = result.data['data']['routine_id']
        routine = Routine.objects.get(routine_id=routine_id)

        self.assertEqual(routine.is_alarm, False)

    def test_create_routine_error_empty_params(self):
        """
        에러 케이스(제목, 목표, 카테고리 없는 경우)
        """
        data = get_routine_for_create()
        data.pop("title")
        data.pop("goal")
        data.pop("category")

        result = self.client.post(
            routine_path,
            data=data
        )

        error_data = result.json()

        self.assertEqual(result.status_code, 400)
        self.assertEqual(error_data["title"][0], error_message_1)
        self.assertEqual(error_data["category"][0], error_message_1)
        self.assertEqual(error_data["goal"][0], error_message_1)

    def test_create_routine_error_empty_days(self):
        """
        에러 케이스(날짜 없는 경우)
        """
        result = self.client.post(
            routine_path,
            data=get_routine_for_create(days=[])
        )

        error_data = result.json()

        self.assertEqual(result.status_code, 500)
        self.assertEqual(error_data["detail"], "올바른 day 값이 아닙니다.")

    def test_create_routine_error_incorrect_category(self):
        """
        에러 케이스(category에 올바른 값이 들어가지 않은 경우)
        """
        result = self.client.post(
            routine_path,
            data=get_routine_for_create(category=["HOMEWORK"])
        )

        error_data = result.json()

        self.assertEqual(result.status_code, 400)

    def test_create_routine_error_incorrect_days(self):
        """
        에러 케이스(day에 올바른 값이 들어가지 않은 경우)
        """
        result = self.client.post(
            routine_path,
            data=get_routine_for_create(days=["MONDAY"])
        )

        error_data = result.json()

        self.assertEqual(result.status_code, 400)

    def test_create_routine_error_logout(self):
        """
        에러 케이스(권한이 없는 경우)
        """
        self.client.logout()

        result = self.client.post(
            routine_path,
            data=get_routine_for_create()
        )

        self.assertEqual(result.status_code, 403)


class RoutineListTest(TestCase):
    def setUp(self):
        self.today_name = Days(datetime.today().weekday()).name
        self.today_value = Days(datetime.today().weekday()).value

        # 다른 계정 테스트용 start
        self.another_account_id = get_account_id_from_create_user(self, email=_another_email)
        self.client.login(email=_another_email, password=_password)
        self.client.post(
            routine_path,
            data=get_routine_for_create(days=[self.today_name])
        )
        self.client.logout()
        # 다른 계정 테스트용 end

        self.account_id = get_account_id_from_create_user(self, email=_email)
        self.client.login(email=_email, password=_password)

        self.client.post(
            routine_path,
            data=get_routine_for_create(days=[self.today_name])
        )

    def test_get_routine_list_1(self):
        """
        정상 케이스(투데이 없는 상태로 조회 시 오늘자로 조회됨)
        오늘자로 조회할 시에 1건이 있어야함(setUp 에서 오늘자로 1건 생성)
        2건 발생 시 에러(다른 계정으로 생성된 루틴도 보이게 됨)
        """
        result = self.client.get(
            routine_path
        )

        data = result.json()

        self.assertEqual(len(data['data']), 1)
        self.assertEqual(result.status_code, ResponseEnum.ROUTINE_LIST_OK.value[1])
        self.assertEqual(data['message']['msg'], ResponseEnum.ROUTINE_LIST_OK.value[0])
        self.assertEqual(data['message']['status'], ResponseEnum.ROUTINE_LIST_OK.name)

    def test_get_routine_list_2(self):
        """
        정상 케이스(투데이 없는 상태로 조회 시 오늘자로 조회됨)
        오늘자로 조회할 시에 1건이 있어야함(setUp 에서 오늘자로 1건 생성)
        2건 발생 시 에러(다른 계정으로 생성된 루틴도 보이게 됨)
        """
        date_str = str(date.today() + timedelta(days=1))

        result = self.client.get(
            routine_path + '?today=' + date_str
        )

        data = result.json()

        self.assertEqual(len(data['data']), 0)
        self.assertEqual(result.status_code, ResponseEnum.ROUTINE_LIST_OK.value[1])
        self.assertEqual(data['message']['msg'], ResponseEnum.ROUTINE_LIST_OK.value[0])
        self.assertEqual(data['message']['status'], ResponseEnum.ROUTINE_LIST_OK.name)

    def test_get_routine_list_error_logout(self):
        """
        에러 케이스(권한이 없는 경우)
        """
        self.client.logout()

        result = self.client.get(
            routine_path
        )

        self.assertEqual(result.status_code, 403)


class RoutineDetailTest(TestCase):
    def setUp(self):
        self.today_name = Days(datetime.today().weekday()).name
        self.today_value = Days(datetime.today().weekday()).value

        # 다른 계정 테스트용 start
        self.another_account_id = get_account_id_from_create_user(self, email=_another_email)
        self.client.login(email=_another_email, password=_password)
        another_routine = self.client.post(
            routine_path,
            data=get_routine_for_create(days=[self.today_name])
        )
        self.another_routine_id = another_routine.json()['data']['routine_id']
        self.client.logout()
        # 다른 계정 테스트용 end

        self.account_id = get_account_id_from_create_user(self, email=_email)
        self.client.login(email=_email, password=_password)

        routine = self.client.post(
            routine_path,
            data=get_routine_for_create(days=[self.today_name])
        )
        self.routine_id = routine.json()['data']['routine_id']

    def test_get_routine_1(self):
        """
        자신 건 조회
        """
        result = self.client.get(
            f"{routine_path}{self.routine_id}/"
        )

        result_json = result.json()
        data = result_json['data']

        self.assertEqual(data['routine_id'], self.routine_id)
        self.assertEqual(data['category'], _category)
        self.assertEqual(data['goal'], _goal)
        self.assertEqual(data['result'], "N")
        self.assertEqual(len(data['days']), 1)

    def test_get_routine_error_another_user(self):
        """
        타인 건 조회
        """
        result = self.client.get(
            f"{routine_path}{self.another_routine_id}/"
        )

        self.assertEqual(result.status_code, 500)
        self.assertEqual(result.json()['detail'], error_message_2)

    def test_get_routine_list_2(self):
        """
        아예 존재하지 않는 케이스 조회
        """
        result = self.client.get(
            f"{routine_path}0/"
        )

        self.assertEqual(result.status_code, 500)
        self.assertEqual(result.json()['detail'], error_message_2)

    def test_get_routine_list_error_logout(self):
        """
        에러 케이스(권한이 없는 경우)
        """
        self.client.logout()

        result = self.client.get(
            f"{routine_path}{self.routine_id}/"
        )

        self.assertEqual(result.status_code, 403)


class RoutineDeleteTest(TestCase):
    def setUp(self):
        self.today_name = Days(datetime.today().weekday()).name
        self.today_value = Days(datetime.today().weekday()).value

        # 다른 계정 테스트용 start
        self.another_account_id = get_account_id_from_create_user(self, email=_another_email)
        self.client.login(email=_another_email, password=_password)
        another_routine = self.client.post(
            routine_path,
            data=get_routine_for_create(days=[self.today_name])
        )
        self.another_routine_id = another_routine.json()['data']['routine_id']
        self.client.logout()
        # 다른 계정 테스트용 end

        self.account_id = get_account_id_from_create_user(self, email=_email)
        self.client.login(email=_email, password=_password)

        routine = self.client.post(
            routine_path,
            data=get_routine_for_create(days=[self.today_name])
        )
        self.routine_id = routine.json()['data']['routine_id']

    def test_delete_routine_1(self):
        """
        자신건 정상 삭제
        """
        result = self.client.delete(
            f"{routine_path}{self.routine_id}/"
        )

        self.assertEqual(result.status_code, 204)

    def test_delete_routine_error_1(self):
        """
        이미 삭제된 건 삭제
        """
        self.client.delete(
            f"{routine_path}{self.routine_id}/"
        )

        result = self.client.delete(
            f"{routine_path}{self.routine_id}/"
        )

        self.assertEqual(result.status_code, 500)
        self.assertEqual(result.json()['detail'], error_message_2)

    def test_delete_routine_error_2(self):
        """
        아예 존재하지 않는 케이스 조회
        """
        result = self.client.delete(
            f"{routine_path}{self.another_routine_id}/"
        )

        self.assertEqual(result.status_code, 500)
        self.assertEqual(result.json()['detail'], error_message_2)

    def test_delete_routine_error_3(self):
        """
        로그아웃된 상태로 삭제
        """
        self.client.logout()

        result = self.client.delete(
            f"{routine_path}{self.routine_id}/"
        )

        self.assertEqual(result.status_code, 403)


class RoutineUpdateTest(TestCase):
    def setUp(self):
        self.today_name = Days(datetime.today().weekday()).name
        self.today_value = Days(datetime.today().weekday()).value

        # 다른 계정 테스트용 start
        self.another_account_id = get_account_id_from_create_user(self, email=_another_email)
        self.client.login(email=_another_email, password=_password)
        another_routine = self.client.post(
            routine_path,
            data=get_routine_for_create(days=[self.today_name])
        )
        self.another_routine_id = another_routine.json()['data']['routine_id']
        self.client.logout()
        # 다른 계정 테스트용 end

        self.account_id = get_account_id_from_create_user(self, email=_email)
        self.client.login(email=_email, password=_password)

        routine = self.client.post(
            routine_path,
            data=get_routine_for_create(days=[self.today_name])
        )
        self.routine_id = routine.json()['data']['routine_id']

    def test_update_routine_1(self):
        """
        자신건 정상 수정
        """
        data = get_routine_for_create(
            title=_title2,
            category=_category2,
            goal=_goal2,
            is_alarm=_is_alarm2,
            days=_days2
        )

        result = self.client.patch(
            f"{routine_path}{self.routine_id}/",
            data=json.dumps(data),
            content_type='application/json'
        )

        routine_id = result.data['data']['routine_id']
        routine = Routine.objects.get(routine_id=routine_id)
        routine_result = RoutineResult.objects.get(routine_id=routine_id)
        routine_day = RoutineDay.objects.filter(routine_id=routine_id).all()

        self.assertEqual(routine.title, _title2)
        self.assertEqual(routine.category, _category2)
        self.assertEqual(routine.goal, _goal2)
        self.assertEqual(routine.is_deleted, False)
        self.assertEqual(routine_result.result, "N")
        self.assertEqual(len(routine_day), 1)

    def test_update_routine_error_1(self):
        """
        카테고리에 올바르지 않은 값이 들어간 경우
        """
        result = self.client.patch(
            f"{routine_path}{self.routine_id}/",
            data=json.dumps({"category": "HOMEWORK"}),
            content_type='application/json'
        )

        print(result.json())

        self.assertEqual(result.status_code, 400)

    def test_update_routine_error_2(self):
        """
        days에 올바르지 않은 값이 들어간 경우
        """
        result = self.client.patch(
            f"{routine_path}{self.routine_id}/",
            data=json.dumps({"days": ["SUNDAY"]}),
            content_type='application/json'
        )

        self.assertEqual(result.status_code, 500)
        self.assertEqual(result.json()["detail"], "올바른 day 값이 아닙니다.")

    def test_update_routine_error_3(self):
        """
        타인 건 수정하는 경우
        """
        result = self.client.patch(
            f"{routine_path}{self.another_routine_id}/",
            data=json.dumps({"days": ["SUN"]}),
            content_type='application/json'
        )

        self.assertEqual(result.status_code, 500)
        self.assertEqual(result.json()['detail'], error_message_2)

    def test_delete_routine_error_3(self):
        """
        로그아웃된 상태로 수정
        """
        self.client.logout()

        result = self.client.patch(
            f"{routine_path}{self.another_routine_id}/",
            data=json.dumps({"days": ["SUN"]}),
            content_type='application/json'
        )

        self.assertEqual(result.status_code, 403)


class EnumTests(TestCase):

    def test_date_convert(self):
        today = '2023-02-04'
        day = date.weekday(datetime.strptime(today, "%Y-%m-%d"))
        self.assertEqual(day, 5)  # 토요일

    def test_date_convert_error_case(self):
        today = ''

        try:
            day = date.weekday(datetime.strptime(today, "%Y-%m-%d"))
            self.assertTrue(False, msg="빈 값인데 날짜가 생성됨")
        except ValueError as e:
            self.assertTrue(True)
        except:
            self.assertTrue(False, msg="의도치 않은 에러")

    def test_days_convert(self):
        days_int = [0, 1, 2, 3, 4, 5, 6]
        days_str = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
        days_int_to_str = list(map(lambda d: Days(d).name, days_int))
        days_str_to_int = list(map(lambda d: Days[d].value, days_str))

        self.assertEqual(days_str_to_int, days_int)
        self.assertEqual(days_int_to_str, days_str)
