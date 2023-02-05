from datetime import date, datetime

from django.db.models import OuterRef
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.response import Response
from rest_framework import viewsets, permissions, exceptions, status

from routine.enums import ResponseEnum
from routine.models import Routine, RoutineDay, RoutineResult
from routine.serializers import RoutineSerializer, RoutineCreateSerializer
from routine.utils import get_response


# TODO: Response return 해주는 util 필요할듯...


class RoutineViewSet(viewsets.ModelViewSet):
    queryset = Routine.objects.select_related('account').prefetch_related('routineday_set').all()
    serializer_class = RoutineSerializer
    permission_classes = [permissions.IsAuthenticated]
    routine_id = None

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

    def retrieve(self, request, pk):
        try:
            queryset = self.get_queryset().get(routine_id=pk)
            queryset.days = self.get_days(RoutineDay.objects.filter(routine_id=pk))
        except Routine.DoesNotExist:
            return get_response({}, ResponseEnum.ROUTINE_NOT_FOUND)

        if queryset:
            serializer = RoutineSerializer(queryset)
            return get_response(serializer.data, ResponseEnum.ROUTINE_DETAIL_OK)


    def destroy(self, request, *args, **kwargs):
        try:
            queryset = Routine.objects.live_one(self.request.user.id, kwargs["pk"])
            queryset.days = self.get_days(RoutineDay.objects.filter(routine_id=kwargs["pk"]))
        except Routine.DoesNotExist:
            return Response(
                {
                    "data": {},
                    "message": {
                        "msg": "Routine lookup was failed",
                        "status": "ROUTINE_NOT_FOUND"
                    }
                },
                status=404
            )

    def get_days(self, days):
        return list(map(str, days))
