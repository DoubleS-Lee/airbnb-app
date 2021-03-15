# serializers : 데이터가 보여야하는 방식을 설명해줘야하는 form. JSON 방식이어야만 함

from rest_framework import serializers
from .models import Room
from users.serializers import UserSerializer
from .models import Room, Photo


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        exclude = ("room",)


class RoomSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)
    # https://www.django-rest-framework.org/api-guide/fields/#serializermethodfield
    # 밑에 def get_is_fav 메소드를 생성한다
    # 메소드 앞에 get_을 붙여야한다
    is_fav = serializers.SerializerMethodField()
    photos = PhotoSerializer(read_only=True, many=True)

    # ModelSerializer 하나로 create, update 메소드를 따로 구현할 필요가 없음
    class Meta:
        model = Room
        exclude = ("modified",)
        # read_only_fields : 수정은 안되고 읽어오기만 가능한 항목을 넣어준다
        # ModelSerializer에서만 사용가능
        # https://www.django-rest-framework.org/api-guide/serializers/#specifying-read-only-fields
        read_only_fields = ("id", "user", "created", "updated")

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

    # 아주 중요한 개념!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # dynamic field : 페이지를 요청하는 유저에 따라서 바뀌는 필드 예)is_fav
    # https://www.django-rest-framework.org/api-guide/fields/#serializermethodfield
    # get_is_fav가 serializer에 있는 모든 object를 불러오는 역할을 한다
    # 그래서 obj를 print 해보면 현재 페이지의 room 정보가 뜨는 것이다
    def get_is_fav(self, obj):
        # self는 serializers.ModelSerializer를 obj는 현재 보고있는 room의 정보를 말한다
        # print(obj)
        # 우리는 이 serializer를 찾는 user가 알아낼 필요가 있다. 그래야 유저 각각에 맞게 is_fav값을 내보내 줄 수 있기 때문
        # views.py class RoomsView - serializer = RoomSerializer(results, many=True, context=["request": request]) 에서 context로 받아온
        # request를 이용해서 request.user(현재 이 정보(serializer)를 찾는 유저가 누구인지 알아내기 위함)를 가져온다
        request = self.context.get("request")
        # print(request.user)
        if request:
            user = request.user
            # 인증된 유저라면
            if user.is_authenticated:
                # 현재 user(=로그인 된, 요청하고 있는)의 models에 있는 favs 목록에 현재 rooms이 담겨있다면(=user가 fav 목록에 포함시켜놨다면) True를 반환
                return obj in user.favs.all()
        return False

    # RoomSerializer를 사용하여 create 활동을 할 떄 (in RoomViewSet)
    # room 정보 입력 말고 user 정보 입력도 하라는 문제가 발생한다 이때 해결책은
    # 1. user = UserSerializer(read_only=True)를 해주고 (<- 이것만 하면 user 정보가 없어서 room을 생성할 수 없다는 오류가 뜸(user 정보가 read_only이기 때문))
    # 2. def create에서 새로 생성하는 room 정보에 user 정보를 추가해 준 다음 생성한 room(user 정보가 담긴)을 return 한다
    def create(self, validated_data):
        # selializer가 user 정보에 관련된 context를 받는 방법 (Viewset class 안에 있는 def get_serializer_context가 이미 request를 보내고 있음 이걸 이용하면 된다)
        # http://www.cdrf.co/3.9/rest_framework.viewsets/ModelViewSet.html#get_serializer_context
        # cdrf를 잘 살펴보면 해야할 수고를 덜어내는 경우가 생긴다
        # print(self.context.get("request").user)
        request = self.context.get("request")
        room = Room.objects.create(**validated_data, user=request.user)
        return room