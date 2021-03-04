from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from .models import User
from .serializers import ReadUserSerializer
from rest_framework.permissions import IsAuthenticated


# APIView에 사용하는 장고 authentication, permissions
# https://www.django-rest-framework.org/api-guide/authentication/
class MeView(APIView):

    # permission_classes를 사용하면 이 클래스 내부를 실행하기전에 유저가 접근 권한을 가졌는지 자동으로 판별해준다
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(ReadUserSerializer(request.user).data)

    def put(self, request):
        pass


@api_view(["GET"])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
        return Response(ReadUserSerializer(user).data)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)