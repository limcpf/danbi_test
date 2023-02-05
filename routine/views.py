from datetime import date, datetime

from django.db import transaction
from django.db.models import OuterRef
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from rest_framework import viewsets, permissions, exceptions, status

from routine.enums import ResponseEnum, Days
from routine.models import Routine, RoutineDay, RoutineResult
from routine.serializers import RoutineSerializer, RoutineCreateSerializer
from routine.utils import get_response


class RoutineViewSet(viewsets.ModelViewSet):
    queryset = Routine.objects.live().select_related('account').prefetch_related('routineday_set').all()
    serializer_class = RoutineSerializer
    permission_classes = [permissions.IsAuthenticated]

    routine_id = None

    def get_object(self, request, *args, **kwargs):
        try:
            return self.get_queryset().get(routine_id=kwargs["pk"], account_id=request.user.id)
        except Routine.DoesNotExist:
            raise exceptions.APIException(detail="존재하지 않는 Routine 입니다.", code=status.HTTP_404_NOT_FOUND)

    def list(self, request, *args, **kwargs):
        try:
            today = datetime.strptime(self.request.query_params['today'], "%Y-%m-%d")
            day = date.weekday(today)
        except MultiValueDictKeyError:
            today = datetime.today()
            day = today.weekday()
        except ValueError:
            raise exceptions.APIException(detail="올바른 날짜 형식(yyyy-mm-dd)이 아닙니다.", code=status.HTTP_400_BAD_REQUEST)

        serializer = RoutineSerializer(
            self.get_queryset().filter(
                account_id=request.user.id,
                routineday__day=day
            ), many=True
        )
        return get_response(serializer.data, ResponseEnum.ROUTINE_LIST_OK)

    def create(self, request, *args, **kwargs):
        serializer = RoutineCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return get_response({"routine_id": self.routine_id}, ResponseEnum.ROUTINE_CREATE_OK)

    def perform_create(self, serializer):
        routine = serializer.save(account_id=self.request.user.id)
        self.routine_id = routine.routine_id

    def retrieve(self, request, *args, **kwargs):
        try:
            queryset = self.get_object(request, *args, **kwargs)

            days = RoutineDay.objects.filter(routine_id=kwargs["pk"])
            queryset.days = list(map(str, days))
        except Routine.DoesNotExist:
            return get_response({}, ResponseEnum.ROUTINE_NOT_FOUND)

        if queryset:
            serializer = RoutineSerializer(queryset)
            return get_response(serializer.data, ResponseEnum.ROUTINE_DETAIL_OK)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object(request, *args, **kwargs)
        instance.delete()
        return get_response({"routine_id": instance.pk}, ResponseEnum.ROUTINE_DELETE_OK)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        if request.method == "PUT":
            raise MethodNotAllowed("PUT")
        instance = self.get_object(request, *args, **kwargs)
        serializer = self.get_serializer(instance, data=request.data, partial=kwargs['partial'])
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer, *args, **kwargs)

        return get_response(serializer.data, ResponseEnum.ROUTINE_DETAIL_OK)

    def perform_update(self, serializer, *args, **kwargs):
        days = []

        try:
            days = self.request.data["days"]
        except KeyError as e:
            pass # day가 없다해도 update 진행을 위함
        pk = kwargs["pk"]

        if days:
            try:
                days = list(map(lambda d: Days[d].value, days))
            except KeyError:
                raise exceptions.APIException(detail="올바른 day 값이 아닙니다.", code=status.HTTP_400_BAD_REQUEST)

            for day in days:
                RoutineDay.objects.get_or_create(day=day, routine_id=pk)

            RoutineDay.objects.filter(
                routine_id=pk
            ).exclude(
                day__in=days
            ).delete()

        serializer.save()
