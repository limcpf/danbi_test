from django.db import transaction
from rest_framework import serializers, exceptions, status
from rest_framework.serializers import ModelSerializer

from routine.enums import RoutineCategoryChoices, DaysChoices, Days, RoutineResultChoices
from routine.models import Routine, RoutineResult, RoutineDay


class RoutineDaySerializer(ModelSerializer):
    class Meta:
        model = RoutineDay
        fields = ["day"]


class RoutineResultSerializer(ModelSerializer):
    class Meta:
        model = RoutineResult
        fields = ["result"]


class RoutineSerializer(ModelSerializer):
    days = serializers.SerializerMethodField()
    result = serializers.SerializerMethodField()

    class Meta:
        model = Routine
        fields = ["routine_id", "title", "category", "goal", "days", "result"]
        read_only_fields = ["result"]
        write_only_fields = ["is_alarm"]

    def get_days(self, instance):
        return list(map(str, RoutineDay.objects.filter(routine=instance)))

    def get_result(self, instance):
        return RoutineResult.objects.get(routine=instance).result  # "H"




class RoutineCreateSerializer(ModelSerializer):
    class Meta:
        model = Routine
        fields = ["routine_id", "title", "category", "goal", "is_alarm", "days"]

    days = serializers.ListField(
        child=serializers.ChoiceField(choices=DaysChoices.names),
        required=False,
        initial=["MON"]
    )

    @transaction.atomic()
    def create(self, data):
        try:
            days = data.pop("days")  # days는 routine 을 만드는데 사용하지 않음
            routine = Routine.objects.create(**data)
            RoutineResult.objects.create(routine_id=routine.routine_id)
            self.create_day(days, routine.routine_id)
        except KeyError as e:
            raise exceptions.APIException(detail="올바른 day 값이 아닙니다.", code=status.HTTP_400_BAD_REQUEST)
        return routine

    def create_day(self, days, routine_id):
        if len(days) < 1:
            raise exceptions.APIException(detail="days 값이 들어오지 않았습니다.", code=status.HTTP_400_BAD_REQUEST)

        for day in days:
            day = Days[day].value
            RoutineDay.objects.create(day=day, routine_id=routine_id)
#
