from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from .models import Room
from .serializers import RoomSerializer, BigRoomSerializer

# ListAPIView를 이용한 Class-Based-View 생성
# rest_framework.generics을 이용하여 serializer를 생성하는 것은 커스터마이징이 필요없을때는 아주 좋은 방법이다
# 하지만 유저 인증등의 커스터마이징이 필요한 경우에는 APIView를 사용하는 것이 좋다
class ListRoomView(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


# RetrieveAPIView는 1개의 모델을 읽기 위해 사용하는 APIView이다
# ListAPIView는 여러개의 모델을 다 불러오는 반면 RetrieveAPIView는 한개의 모델만 불러온다
# http://www.cdrf.co/3.9/rest_framework.generics/RetrieveAPIView.html
class SeeRoomView(RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = BigRoomSerializer