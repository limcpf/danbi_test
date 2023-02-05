from datetime import date, datetime

from django.db.models import OuterRef
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.response import Response
from rest_framework import viewsets, permissions, exceptions, status

from routine.models import Routine, RoutineDay, RoutineResult
from routine.serializers import RoutineSerializer


class RoutineViewSet(viewsets.ModelViewSet):
    routine_id = None
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        day = None
        today = None

        try:
            today = datetime.strptime(self.request.query_params['today'], "%Y-%m-%d")
            day = date.weekday(today)
        except MultiValueDictKeyError:
            today = datetime.today()
            day = today.weekday()
        except ValueError:
            raise exceptions.APIException(detail="올바른 날짜 형식(yyyy-mm-dd)이 아닙니다.", code=status.HTTP_400_BAD_REQUEST)

        queryset = Routine.objects \
            .live(self.request.user.id) \
            .filter(
            routineday__day=day
        ) \
            .annotate(
            result=RoutineResult.objects.filter(
                routine_id=OuterRef("routine_id")).values("result")
        )

        serializer = RoutineSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
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
            status=201
        )

    def perform_create(self, serializer):
        routine = serializer.save(account_id=self.request.user.id)
        self.routine_id = routine.routine_id
