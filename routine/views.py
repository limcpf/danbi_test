from django.db.models import OuterRef
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, permissions

from routine.models import Routine, RoutineDay, RoutineResult
from routine.serializers import RoutineSerializer


class RoutineViewSet(viewsets.ModelViewSet):
    routine_id = None
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = Routine.objects\
            .live(self.request.user.id)\
            .filter(
                routineday__day=0
            )\
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
