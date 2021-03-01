from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from .models import Room
from .serializers import ReadRoomSerializer, WriteRoomSerializer
from rest_framework.decorators import api_view
from rest_framework import status

# GET과 POST를 decorators를 사용해서 구현한다
@api_view(["GET", "POST"])
def rooms_view(request):
    # print(request)
    if request.method == "GET":
        rooms = Room.objects.all()
        serializer = ReadRoomSerializer(rooms, many=True).data
        return Response(serializer)
    elif request.method == "POST":
        serializer = WriteRoomSerializer(data=request.data)
        # print(serializer.is_valid())
        if serializer.is_valid():
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# RetrieveAPIView는 1개의 모델을 읽기 위해 사용하는 APIView이다
# ListAPIView는 여러개의 모델을 다 불러오는 반면 RetrieveAPIView는 한개의 모델만 불러온다
# http://www.cdrf.co/3.9/rest_framework.generics/RetrieveAPIView.html
class SeeRoomView(RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = ReadRoomSerializer