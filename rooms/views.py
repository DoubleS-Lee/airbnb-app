from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Room
from .serializers import RoomSerializer

# APIView를 이용한 Class-Based-View 생성
# APIView는 DRF에서 제공하는 Apiview중에서 가장 일반적인 형태이다
# 여기서 한걸음 더 들어가면 ListAPIView, CreateAPIView등을 가지고 있는 Generic View가 있다
class ListRoomView(APIView):
    def get(self, request):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)