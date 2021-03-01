from django.urls import path
from rest_framework.routers import DefaultRouter
from . import viewsets

app_name = "rooms"

# url을 설계할때 다음과 같이 설계하면 된다
router = DefaultRouter()
router.register("", viewsets.RoomViewset, basename="room")

urlpatterns = router.urls
