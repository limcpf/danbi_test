from django.db import transaction
from rest_framework import serializers, exceptions, status

from routine.enums import RoutineCategoryChoices, DaysChoices, Days, RoutineResultChoices
from routine.models import Routine, RoutineResult, RoutineDay


class RoutineSerializer(serializers.Serializer):
    class Meta:
        model = Routine
        fields = ["routine_id", "title", "category", "goal", "days"]

    routine_id = serializers.CharField(label="id", max_length=32, read_only=True)
    title = serializers.CharField(max_length=255, initial="title")
    category = serializers.ChoiceField(
        choices=RoutineCategoryChoices,
        initial=RoutineCategoryChoices.HOMEWORK.value
    )
    goal = serializers.CharField(initial="goal")
    days = serializers.ListField(
        child=serializers.ChoiceField(choices=DaysChoices.names),
        required=False,
        initial=["MON"]
    )
    result = serializers.CharField(read_only=True)

    @transaction.atomic()
    def create(self, data):
        data.pop("days")  # days는 routine 을 만드는데 사용하지 않음
        routine = Routine.objects.create(**data)
        self.create_result(routine.routine_id)
        try:
            days = self.context["request"].data["days"]
            self.create_day(days, routine.routine_id)
        except KeyError as e:
            raise exceptions.APIException(detail="올바른 day 값이 아닙니다.", code=status.HTTP_400_BAD_REQUEST)
        return routine

    def create_result(self, routine_id):
        RoutineResult.objects.create(routine_id=routine_id)

    def create_day(self, days, routine_id):
        if len(days) < 1:
            raise exceptions.APIException(detail="days 값이 들어오지 않았습니다.", code=status.HTTP_400_BAD_REQUEST)

        for day in days:
            day = Days[day].value
            RoutineDay.objects.create(day=day, routine_id=routine_id)
