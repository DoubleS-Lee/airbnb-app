from rest_framework.decorators import api_view
from rest_framework.response import Response

# DRF를 사용하기 위해 api_view 데코레이터로 함수를 감싸준다
# GET, POST, PUT, DELETE 중에 어떤 기능을 사용할지 정해준다
@api_view(["GET"])
def list_rooms(request):
    # DRF에서 제공하는 response를 return 한다
    # 이 코드로부터 데이터들을 볼수있는 페이지를 얻게 된다
    # http://127.0.0.1:8000/api/v1/rooms/list/
    return Response()
