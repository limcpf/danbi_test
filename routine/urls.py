from django.urls import path, include
from rest_framework import routers
from .views import RoutineViewSet

app_name = "routine"

router = routers.DefaultRouter()
router.register('', RoutineViewSet)

urlpatterns = [
    path('', include(router.urls))
]
