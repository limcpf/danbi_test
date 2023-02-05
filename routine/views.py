from datetime import date, datetime

from django.db.models import OuterRef
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.response import Response
from rest_framework import viewsets, permissions, exceptions, status

from routine.models import Routine, RoutineDay, RoutineResult
from routine.serializers import RoutineSerializer, RoutineCreateSerializer


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
        return Response({
            "data": serializer.data,
            "message": {"msg": "Routine lookup was successful.",
                        "status": "ROUTINE_LIST_OK"}
        })

    def create(self, request, *args, **kwargs):
        serializer = RoutineCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                "data": {
                    "routine_id": self.routine_id
                },
                "message": {
                    "msg": "You have successfully created the routine.",
                    "status": "ROUTINE_CREATE_OK"
                }
            },
            status=200
        )

    def perform_create(self, serializer):
        routine = serializer.save(account_id=self.request.user.id)
        self.routine_id = routine.routine_id

    def retrieve(self, request, pk):
        try:
            queryset = self.get_queryset()
            queryset.days = self.get_days(RoutineDay.objects.filter(routine_id=pk))
        except Routine.DoesNotExist:
            queryset = None

        if queryset:
            serializer = RoutineSerializer(queryset)
            return Response(
                {
                    "data": serializer.data,
                    "message": {
                        "msg": "Routine lookup was successful.",
                        "status": "ROUTINE_DETAIL_OK"
                    }
                },
                status=200
            )

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
