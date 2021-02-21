# serializers : 데이터가 보여야하는 방식을 설명해줘야하는 form. JSON 방식이어야만 함

from rest_framework import serializers
from .models import Room
from users.serializers import TinyUserSerializer

# 여기서 serializers.Serializer를 쓰면 각각의 데이터에 해당하는 것을 다 일일이 지정해줘야하는데 serializers.ModelSerializer를 쓰면 이게 해결된다
# serializers.ModelSerializer를 사용한다
class RoomSerializer(serializers.ModelSerializer):

    # room과 foreignkey로 연결되어 있는 user에 있는 데이터들을 불러오려면 이런식으로 users-serializers.py에서 serializer를 생성해주고 이곳으로 불러와서 사용하면 된다
    user = TinyUserSerializer()

    class Meta:
        model = Room
        fields = ("name", "price", "instant_book", "user")