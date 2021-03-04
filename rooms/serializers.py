# serializers : 데이터가 보여야하는 방식을 설명해줘야하는 form. JSON 방식이어야만 함

from rest_framework import serializers
from .models import Room
from users.serializers import RelatedUserSerializer

# 여기서 serializers.Serializer를 쓰면 각각의 데이터에 해당하는 것을 다 일일이 지정해줘야하는데 serializers.ModelSerializer를 쓰면 이게 해결된다
# serializers.ModelSerializer를 사용한다
class ReadRoomSerializer(serializers.ModelSerializer):

    # room과 foreignkey로 연결되어 있는 user에 있는 데이터들을 불러오려면 이런식으로 users-serializers.py에서 serializer를 생성해주고 이곳으로 불러와서 사용하면 된다
    user = RelatedUserSerializer()

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
        # update를 하는 경우 : self.instance가 True라는건 update 상황이라는 것이다
        # update 상황이라면 check_in이나 check_out을 업데이트하는 경우 data에서 check_in,out을 가져오고
        # check_in, check_out 외 다른 것만 업데이트하는 경우 Default로 기존에 갖고 있던 값인 self.instance.check_in,out을 가져오라는 뜻
        if self.instance:
            check_in = data.get("check_in", self.instance.check_in)
            check_out = data.get("check_out", self.instance.check_out)
        # create를 하는 경우 : self.instance가 False라는건 create 상황이라는 것이다
        # create를 하는 경우이니까 새로 생성된 check_in, check_out을 가져오면 된다
        else:
            check_in = data.get("check_in")
            check_out = data.get("check_out")
        # check_in과 check_out이 같다면 error를 띄움
        if check_in == check_out:
            # 에러를 띄우고 views.py의 serializer.errors에 "Not enough time between changes" 값을 전달한다
            raise serializers.ValidationError("Not enough time between changes")
        return data

    # https://www.django-rest-framework.org/api-guide/serializers/#writing-create-methods-for-nested-representations
    # create와 다르게 instance를 가지고 있다 instance로 DRF가 유저가 create를 하는지 update를 하는지 구별한다
    # instance : 초기 객체(이미 만들어져 있는 객체), update의 경우 instance가 존재하고, create의 경우 instance가 존재하지 않는다
    # update : instance를 가지고 serializer를 initialize 한다
    # create : 오직 data만을 가지고 serializer를 initialize 한다
    def update(self, instance, validated_data):
        # print(instance, validated_data)
        # data를 update 하기전에 기존에 존재하는 객체의 값인 instance 값을 가져와서
        # 존재하는지(유저가 update했는지) 확인한 뒤 update했으면 반영하고, update 안했으면 기존 값(=instance)을 가져와서 그대로 넣어준다
        instance.name = validated_data.get("name", instance.name)
        instance.address = validated_data.get("address", instance.address)
        instance.price = validated_data.get("price", instance.price)
        instance.beds = validated_data.get("beds", instance.beds)
        instance.lat = validated_data.get("lat", instance.lat)
        instance.lng = validated_data.get("lng", instance.lng)
        instance.bedrooms = validated_data.get("bedrooms", instance.bedrooms)
        instance.bathrooms = validated_data.get("bathrooms", instance.bathrooms)
        instance.check_in = validated_data.get("check_in", instance.check_in)
        instance.check_out = validated_data.get("check_out", instance.check_out)
        instance.instant_book = validated_data.get(
            "instant_book", instance.instant_book
        )
        # 변경된 instance를 저장해준다
        instance.save()
        # 꼭 return을 해줘야 함
        return instance