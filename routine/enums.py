from enum import Enum
from django.db import models


class Days(Enum):
    MON = 0
    TUE = 1
    WED = 2
    THU = 3
    FRI = 4
    SAT = 5
    SUN = 6


class RoutineCategory(Enum):
    MIRACLE = 'M'
    HOMEWORK = 'H'


class RoutineResult(Enum):
    NOT = 'N'
    TRY = 'T'
    DONE = 'D'


class DaysChoices(models.IntegerChoices):
    MONDAY = Days.MON.value, Days.MON.name
    TUESDAY = Days.TUE.value, Days.TUE.name
    WEDNESDAY = Days.WED.value, Days.WED.name
    THURSDAY = Days.THU.value, Days.THU.name
    FRIDAY = Days.FRI.value, Days.FRI.name
    SATURDAY = Days.SAT.value, Days.SAT.name
    SUNDAY = Days.SUN.value, Days.SUN.name


class RoutineCategoryChoices(models.TextChoices):
    MIRACLE = RoutineCategory.MIRACLE.value, RoutineCategory.MIRACLE.name
    HOMEWORK = RoutineCategory.HOMEWORK.value, RoutineCategory.HOMEWORK.name


class RoutineResultChoices(models.TextChoices):
    NOT = RoutineResult.NOT.value, RoutineResult.NOT.name
    TRY = RoutineResult.TRY.value, RoutineResult.TRY.name
    DONE = RoutineResult.DONE.value, RoutineResult.DONE.name
