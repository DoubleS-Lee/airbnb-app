from rest_framework import viewsets
from .models import Room
from .serializers import BigRoomSerializer


# viewsets을 사용하면 get, post, put, delete를 아주 간단하게 구현할 수 있다는 장점이 있음
# 유저의 종류나 상황에 맞게 get, post, put, delete를 사용해야하는데 이런 조건들을 걸어주기 어려움
class RoomViewset(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = BigRoomSerializer