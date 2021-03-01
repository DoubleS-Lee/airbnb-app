# serializers : 데이터가 보여야하는 방식을 설명해줘야하는 form. JSON 방식이어야만 함

from rest_framework import serializers
from .models import Room
from users.serializers import UserSerializer

# 여기서 serializers.Serializer를 쓰면 각각의 데이터에 해당하는 것을 다 일일이 지정해줘야하는데 serializers.ModelSerializer를 쓰면 이게 해결된다
# serializers.ModelSerializer를 사용한다
class ReadRoomSerializer(serializers.ModelSerializer):

    # room과 foreignkey로 연결되어 있는 user에 있는 데이터들을 불러오려면 이런식으로 users-serializers.py에서 serializer를 생성해주고 이곳으로 불러와서 사용하면 된다
    user = UserSerializer()

    class Meta:
        model = Room
        exclude = ()


class WriteRoomSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=140)
    address = serializers.CharField(max_length=140)
    price = serializers.IntegerField()
    beds = serializers.IntegerField(default=1)
    lat = serializers.DecimalField(max_digits=10, decimal_places=6)
    lng = serializers.DecimalField(max_digits=10, decimal_places=6)
    bedrooms = serializers.IntegerField(default=1)
    bathrooms = serializers.IntegerField(default=1)
    check_in = serializers.TimeField(default="00:00:00")
    check_out = serializers.TimeField(default="00:00:00")
    instant_book = serializers.BooleanField(default=False)

    # https://www.django-rest-framework.org/api-guide/serializers/#writing-create-methods-for-nested-representations
    def create(self, validated_data):
        # print(validated_data)
        # Room을 만든다(validated_data로 부터 받은 정보들을 **(=다 풀어서)Room을 만든다)
        return Room.objects.create(**validated_data)

    # https://www.django-rest-framework.org/api-guide/serializers/#validation
    # 유효성(validation) 검사를 위한 코드를 작성할 수 있다
    # 여기서 데이터가 valid되지 않게 된다면 views의 serializer.is_valid() 값이 False가 된다
    def validate(self, data):
        check_in = data.get("check_in")
        check_out = data.get("check_out")
        if check_in == check_out:
            # 에러를 띄우고 views.py의 serializer.errors에 "Not enough time between changes" 값을 전달한다
            raise serializers.ValidationError("Not enough time between changes")
        else:
            return data