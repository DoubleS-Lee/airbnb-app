from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from .models import User
from .serializers import ReadUserSerializer
from rest_framework.permissions import IsAuthenticated
from .serializers import WriteUserSerializer
from rooms.serializers import RoomSerializer
from rooms.models import Room


# APIView에 사용하는 장고 authentication, permissions
# https://www.django-rest-framework.org/api-guide/authentication/
class MeView(APIView):

    # permission_classes를 사용하면 이 클래스 내부를 실행하기전에 유저가 접근 권한을 가졌는지 자동으로 판별해준다
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(ReadUserSerializer(request.user).data)

    def put(self, request):
        serializer = WriteUserSerializer(request.user, data=request.data, partial=True)
        # print(serializer.is_valid())
        if serializer.is_valid():
            serializer.save()
            return Response()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
        return Response(ReadUserSerializer(user).data)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


class FavsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        # user에 현재 로그인된(=요청을 한) 유저를 할당
        user = request.user
        # user의 favs의 전부를 가져온다
        serializer = RoomSerializer(user.favs.all(), many=True).data
        return Response(serializer)

    def put(self, request):
        # ("pk", None) 이렇게 써줬기 때문에 입력을 받을때 id로 받는게 아니라 pk로 입력을 받는다
        pk = request.data.get("pk", None)
        user = request.user
        if pk is not None:
            try:
                room = Room.objects.get(pk=pk)
                # user.favs에 room을 추가한다
                user.favs.add(room)
                return Response()
            except Room.DoesNotExist:
                pass
        return Response(status=status.HTTP_400_BAD_REQUEST)