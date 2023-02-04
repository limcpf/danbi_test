from django.db import transaction
from rest_framework import serializers, exceptions, status

from routine.enums import RoutineCategoryChoices, DaysChoices, Days, RoutineResultChoices
from routine.models import Routine, RoutineResult, RoutineDay


class RoutineSerializer(serializers.Serializer):
    class Meta:
        model = Routine
        fields = ["account_id", "title", "category", "goal", "is_alarm"]

    title = serializers.CharField(max_length=255)
    category = serializers.ChoiceField(choices=RoutineCategoryChoices)
    goal = serializers.CharField()
    is_alarm = serializers.BooleanField()
    result = serializers.ChoiceField(choices=RoutineResultChoices, read_only=True)
    days = serializers.ListField(child=serializers.ChoiceField(choices=DaysChoices), read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    modified_at = serializers.DateTimeField(read_only=True)

    @transaction.atomic()
    def create(self, data):
        routine = Routine.objects.create(**data)
        self.create_result(routine.routine_id)
        try:
            days = self.context["request"].data["days"]
            self.create_day(days, routine.routine_id)
        except KeyError as e:
            raise exceptions.APIException(detail="days 값이 들어오지 않았습니다1.", code=status.HTTP_400_BAD_REQUEST)
        return routine

    def create_result(self, routine_id):
        RoutineResult.objects.create(routine_id=routine_id)

    def create_day(self, days, routine_id):
        if len(days) < 1:
            raise exceptions.APIException(detail="days 값이 들어오지 않았습니다.", code=status.HTTP_400_BAD_REQUEST)

        print(days)
        for day in days:
            day = Days[day].value
            RoutineDay.objects.create(day=day, routine_id=routine_id)
