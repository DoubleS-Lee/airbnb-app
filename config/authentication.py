import jwt
from django.conf import settings
from rest_framework import authentication
from users.models import User

# API에게 인증(authentication)을 하기 위해 token을 어떻게 이해해야하는지 설명하는 과정
# http://127.0.0.1:8000/api/v1/users/token/  :  가입된 username과 password를 POST로 보내서 고유 token을 얻어오고(encode) header의 Authorization에 할당함(앞에 X-JWT를 붙여줌)
# http://127.0.0.1:8000/api/v1/users/me/   :  고유 token을 이용해서 decode를 하여 해당 user의 정보를 얻어오게 함
# https://www.django-rest-framework.org/api-guide/authentication/
class JWTAuthentication(authentication.BaseAuthentication):
    # custom authentication은 밑의 문서를 참고할 것
    # https://www.django-rest-framework.org/api-guide/authentication/#custom-authentication
    def authenticate(self, request):
        # print(request.META)
        # print(request.META.get.("HTTP_AUTHORIZATION"))
        try:
            # header로 보내진 토큰(users-views.py-def login)을 가져와서 token에 할당
            # HTTP_AUTHORIZATION에 저장된 token 값을 가져온다
            # header나 기타 정보를 request.META로부터 얻을 수 있다
            token = request.META.get("HTTP_AUTHORIZATION")
            # custom-authentication에서는 token이 None이면 None을 return 해야한다
            if token is None:
                return None
            # token을 받아와서 token의 구조를 분석
            # 공백(spacebar)을 기준으로 xjwt와 jwt_token으로 나뉨
            xjwt, jwt_token = token.split(" ")
            # print(xjwt, jwt_token)
            # jwt.decode : token을 해독해서 원래 값으로 돌려놓는 작업
            decoded = jwt.decode(jwt_token, settings.SECRET_KEY, algorithms=["HS256"])
            # print(decoded)
            pk = decoded.get("pk")
            # 가져온 pk 값으로 user를 찾는다
            user = User.objects.get(pk=pk)
            # user를 return 한다
            return (user, None)
        # 발생할만한 에러들을 다 집어넣음
        except (ValueError, jwt.exceptions.DecodeError, User.DoesNotExist):
            return None