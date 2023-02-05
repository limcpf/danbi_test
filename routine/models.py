from django.db import models, transaction
from django.db.models import OuterRef

import user.models
from routine.enums import RoutineCategoryChoices, RoutineResultChoices, DaysChoices, Days


class BaseTimeModel(models.Model):
    """
    생성일시, 수정일시를 공통적으로 사용하기 위한 모델\
    """

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class RoutineManager(models.Manager):
    use_for_related_fields = True

    def live(self, **kwargs):
        return self.filter(is_deleted=False, **kwargs)


class Routine(BaseTimeModel):
    """
    루틴 모델
    """
    routine_id = models.BigAutoField(primary_key=True)
    account = models.ForeignKey(
        user.models.User,
        null=False,
        on_delete=models.PROTECT,
    )
    title = models.CharField(max_length=255, null=False)
    category = models.CharField(
        max_length=2,
        choices=RoutineCategoryChoices.choices,
        null=False
    )
    goal = models.TextField()
    is_alarm = models.BooleanField(default=False, null=False)
    is_deleted = models.BooleanField(default=False, null=False)

    def __str__(self):
        return str(self.routine_id)

    def delete(self, using=None, keep_parents=False):
        RoutineResult.objects.filter(routine_id=self.routine_id).update(is_deleted=True)
        self.is_deleted = True
        self.save()

    objects = RoutineManager()


class RoutineResult(BaseTimeModel):
    """
    루틴 결과 모델
    """
    routine_result_id = models.BigAutoField(primary_key=True)
    routine = models.ForeignKey(
        Routine,
        null=False,
        to_field='routine_id',
        on_delete=models.PROTECT,
    )
    result = models.CharField(
        max_length=2,
        choices=RoutineResultChoices.choices,
        null=False,
        default=RoutineResultChoices.NOT
    )
    is_deleted = models.BooleanField(default=False, null=False)


class RoutineDay(BaseTimeModel):
    """
    루틴 수행 요일 모델
    """

    class Meta:
        unique_together = (('day', 'routine'),)

    day = models.IntegerField(
        choices=DaysChoices.choices,
        null=False
    )
    routine = models.ForeignKey(
        Routine,
        null=False,
        to_field='routine_id',
        on_delete=models.PROTECT
    )

    def __str__(self):
        return Days(self.day).name
