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


class ResponseEnum(Enum):
    ROUTINE_LIST_OK = ("Routine lookup was successful.", 200)
    ROUTINE_CREATE_OK = ("Routine lookup was successful.", 201)
    ROUTINE_DETAIL_OK = ("Routine lookup was successful.", 200)
    ROUTINE_NOT_FOUND = ("Routine lookup was failed", 404)
    ROUTINE_DELETE_OK = ("The routine has been deleted.", 204)


class DaysChoices(models.IntegerChoices):
    MON = (Days.MON.value, Days.MON.name)
    TUE = (Days.TUE.value, Days.TUE.name)
    WED = (Days.WED.value, Days.WED.name)
    THU = (Days.THU.value, Days.THU.name)
    FRI = (Days.FRI.value, Days.FRI.name)
    SAT = (Days.SAT.value, Days.SAT.name)
    SUN = (Days.SUN.value, Days.SUN.name)


class RoutineCategoryChoices(models.TextChoices):
    MIRACLE = RoutineCategory.MIRACLE.value, RoutineCategory.MIRACLE.name
    HOMEWORK = RoutineCategory.HOMEWORK.value, RoutineCategory.HOMEWORK.name


class RoutineResultChoices(models.TextChoices):
    NOT = RoutineResult.NOT.value, RoutineResult.NOT.name
    TRY = RoutineResult.TRY.value, RoutineResult.TRY.name
    DONE = RoutineResult.DONE.value, RoutineResult.DONE.name
