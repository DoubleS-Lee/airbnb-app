from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from .models import User
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from rooms.serializers import RoomSerializer
from rooms.models import Room


class UsersView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            return Response(UserSerializer(new_user).data)
        else:
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


# APIView에 사용하는 장고 authentication, permissions
# https://www.django-rest-framework.org/api-guide/authentication/
class MeView(APIView):

    # permission_classes를 사용하면 이 클래스 내부를 실행하기전에 유저가 접근 권한을 가졌는지 자동으로 판별해준다
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        # print(serializer.is_valid())
        if serializer.is_valid():
            serializer.save()
            return Response()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        # delete를 구현할때 def delete를 안쓰고 add()와 remove()로 구현할수도 있다
        # 로직 : 만약에 입력한 값이 favs에 있다면 삭제(remove)하고, 없다면 추가(add)해라
        if pk is not None:
            try:
                room = Room.objects.get(pk=pk)
                # 만약 선택한 room이 user.favs안에 담겨있다면
                if room in user.favs.all():
                    # user.favs에서 room을 제거한다
                    user.favs.remove(room)
                else:
                    # user.favs에 room을 추가한다
                    user.favs.add(room)
                return Response()
            except Room.DoesNotExist:
                pass
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
        return Response(UserSerializer(user).data)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)