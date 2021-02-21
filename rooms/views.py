from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .models import Room
from .serializers import RoomSerializer

# ListAPIView를 이용한 Class-Based-View 생성
# rest_framework.generics을 이용하여 serializer를 생성하는 것은 커스터마이징이 필요없을때는 아주 좋은 방법이다
# 하지만 유저 인증등의 커스터마이징이 필요한 경우에는 APIView를 사용하는 것이 좋다
class ListRoomView(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer