import jwt

# settings는 그냥 불러오면 안되고 꼭 이 경로로 불러와야 한다
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework import status
from .models import User
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from rooms.serializers import RoomSerializer
from rooms.models import Room
from rest_framework.viewsets import ModelViewSet

# IsAdminUser는 관리자 권한을 말함
from rest_framework.permissions import IsAdminUser, AllowAny
from .permissions import IsSelf


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        # print(self.action)    # favs에 접근하는 경우 self.action의 값이 favs가 된다
        if self.action == "list":
            permission_classes = [IsAdminUser]
        elif (
            self.action == "create"
            or self.action == "retrieve"
            or self.action == "favs"  # 다른 유저가 나의 favs를 보는 것을 허락하게하고 싶을때 사용
        ):
            permission_classes = [AllowAny]
        else:  # delete, update, partial_update가 여기 해당됨
            permission_classes = [IsSelf | IsAdminUser]
        return [permission() for permission in permission_classes]

    # methods는 이 메소드(=url)에서 어떤 작업(CRUD중)을 하는지 지정해주는건데 기본으로 get이 되어 있음 근데 login에서는 get은 필요없고 post만 필요하니까 methods에 post를 넣어준다
    @action(detail=False, methods=["post"])
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        # print(request.data)
        if not username or not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # print(username, password)
        # 입력받은 username과 password에 해당하는 가입된 유저가 있는지 찾아본다
        # 있으면 user를 반환, 없으면 None을 반환한다
        # https://docs.djangoproject.com/en/3.1/topics/auth/default/#authenticating-users
        user = authenticate(username=username, password=password)
        # print(user)
        if user is not None:
            # settings.py 파일은 그냥 불러오면 안되고 from django.conf import settings 이렇게 불러와야 한다
            # SECRET_KEY는 장고 settings.py의 SECRET_KEY를 이용
            # https://pyjwt.readthedocs.io/en/stable/
            # https://jwt.io/
            # user.pk를 가지고 고유한 토큰을 생성한다
            encoded_jwt = jwt.encode(
                {"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256"
            )
            # print(encoded_jwt)
            # 그리고 생성한 토큰을 token이라는 이름으로 내보내준다
            # user.pk값을 id라는 이름으로 token과 함께 보내준다
            # 이 id와 token을 가지고 따로 me/ 페이지를 만들지 않더라도 유저가 본인의 user 정보에 접근할수있게 할 것이다
            return Response(data={"token": encoded_jwt, "id": user.pk})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    # detail=True인 경우에는 detail을 보겠다는 의미니까 detail에 해당하는 pk값을 인자로 건네줘야만 한다
    @action(detail=True)
    def favs(self, request, pk):
        # user 정보를 viewset안에 내장되어 있는 get_object 함수로 가져온다
        user = self.get_object()
        # user의 favs의 전부를 가져온다
        serializer = RoomSerializer(user.favs.all(), many=True).data
        return Response(serializer)


class FavsView(APIView):
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
