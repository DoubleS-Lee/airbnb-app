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


class WriteRoomSerializer(serializers.ModelSerializer):

    # ModelSerializer 하나로 create, update 메소드를 따로 구현할 필요가 없음
    class Meta:
        model = Room
        exclude = ("user", "modified", "created")

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