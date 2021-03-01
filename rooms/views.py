from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Room
from .serializers import ReadRoomSerializer, WriteRoomSerializer
from rest_framework.decorators import api_view
from rest_framework import status

# function을 class로 변경
class RoomsView(APIView):
    def get(self, request):
        rooms = Room.objects.all()
        serializer = ReadRoomSerializer(rooms, many=True).data
        return Response(serializer)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        # request.data를 data로 넘겨주면서 WriteRoomSerializer를 실행하고 결과를 serializer에 담는다
        serializer = WriteRoomSerializer(data=request.data)
        # print(dir(serializer))
        # print(serializer.is_valid())
        # serializer 내부에 있는 method를 WriteRoomSerializer에서 정의해주고 여기 view에서 이를 불러와서 실행시켜야 함(save, create, update등)
        # 하지만 여기에 create, update 메소드를 바로 불러오면 안된다!
        # 대신 save 메소드를 불러와야 한다 save 메소드가 create를 call 할건지 update를 call 할건지 보고 판단해서 대신해준다
        if serializer.is_valid():
            # WriteRoomSerializer의 결과를 save하는데 user는 request.user로 정해준다
            # 이게 없으면 create(post)과정에서 user가 어떤 사람인지 몰라서 에러가 발생한다
            room = serializer.save(user=request.user)
            # 방금 생성한 room 정보를 room_serializer에 담는다
            room_serializer = ReadRoomSerializer(room).data
            # room 정보 create가 성공했으면 방금 생성한 room에 대한 정보를 보여주는 return을 실시한다
            return Response(data=room_serializer, status=status.HTTP_200_OK)
        else:
            # serializer.is_valid()가 False라면 serializers.py의 raise serializers.ValidationError("Not enough time between changes")가 serializers.errors에 값을 넘겨주게 되고 이를 data에 할당했다
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# RetrieveAPIView는 1개의 모델을 읽기 위해 사용하는 APIView이다
# ListAPIView는 여러개의 모델을 다 불러오는 반면 RetrieveAPIView는 한개의 모델만 불러온다
# http://www.cdrf.co/3.9/rest_framework.generics/RetrieveAPIView.html
class SeeRoomView(RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = ReadRoomSerializer