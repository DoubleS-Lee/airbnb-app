from django.http import HttpResponse
from rooms.models import Room
from django.core import serializers
import json

def list_rooms(request):
    # room 정보를 불러온다(객체형태로 불러와 짐)
    # rooms = Room.objects.all()
    # queryset을 불러온다
    # print(rooms)

    # rooms를 HttpResponse 형태로 내보낸다
    # models.py에서 def __str__(self): 로 지정해준 값이 string 형태로 내보내진다
    # response = HttpResponse(content=rooms)
    # return response

    # json.dumps()를 이용하면 queryset 형태의 데이터 파일을 json 형식으로 바꿔 줄 수 있다.
    # json_rooms = json.dumps(rooms)

    # serializers를 이용하여 queryset 형태의 데이터를 json 형태로 바꿔서 return 해준다
    # 장고 객체들은 serializers를 이용해서 json 형태로 바꿔줘야 한다
    # 장고 serializers는 단지 데이터 형태만 바꿔줄 뿐 데이터 검증이라던가 기타 부가적인 기능이 없어서 이걸 이용하기는 좀 곤란하다
    # 따라서 Django Rest Framework(DRF)를 사용해야 한다
    data = serializers.serialize('json', Room.objects.all())
    response = HttpResponse(content=data)
    return response