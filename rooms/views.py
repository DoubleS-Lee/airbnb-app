from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Room
from .serializers import RoomSerializer
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view


# 앞으로 만들 paginator의 중복 코딩을 막기위해 관련 기능을 class로 만들어 놓는다
class OwnPagination(PageNumberPagination):
    page_size = 20


# function을 class로 변경
class RoomsView(APIView):
    def get(self, request):
        # 설정해놓은 pagination class를 불러와서 할당
        paginator = OwnPagination()
        rooms = Room.objects.all()
        # https://www.django-rest-framework.org/api-guide/pagination/#custom-pagination-styles
        # custom pagination 제작을 위함
        # paginator.paginate_queryset : pagination할 데이터를 정의해준다
        results = paginator.paginate_queryset(rooms, request)
        # context를 이용해서 request를 request라는 이름으로 serializers.py - class RoomSerializer에 건네준다
        serializer = RoomSerializer(results, many=True, context={"request": request})
        # paginator.get_paginated_response : page에 대한 데이터를 응답으로 반환해준다
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        # request.data를 data로 넘겨주면서 RoomSerializer를 실행하고 결과를 serializer에 담는다
        serializer = RoomSerializer(data=request.data)
        # print(dir(serializer))
        # print(serializer.is_valid())
        # serializer 내부에 있는 method를 RoomSerializer에서 정의해주고 여기 view에서 이를 불러와서 실행시켜야 함(save, create, update등)
        # 하지만 여기에 create, update 메소드를 바로 불러오면 안된다!
        # 대신 save 메소드를 불러와야 한다 save 메소드가 create를 call 할건지 update를 call 할건지 보고 판단해서 대신해준다
        if serializer.is_valid():
            # RoomSerializer의 결과를 save하는데 user는 request.user로 정해준다
            # 이게 없으면 create(post)과정에서 user가 어떤 사람인지 몰라서 에러가 발생한다
            room = serializer.save(user=request.user)
            # 방금 생성한 room 정보를 room_serializer에 담는다
            room_serializer = RoomSerializer(room).data
            # room 정보 create가 성공했으면 방금 생성한 room에 대한 정보를 보여주는 return을 실시한다
            return Response(data=room_serializer, status=status.HTTP_200_OK)
        else:
            # serializer.is_valid()가 False라면 serializers.py의 raise serializers.ValidationError("Not enough time between changes")가 serializers.errors에 값을 넘겨주게 되고 이를 data에 할당했다
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomView(APIView):
    # 중복해서 사용하는 room을 가져오는 기능을 method로 만든다
    def get_room(self, pk):
        try:
            room = Room.objects.get(pk=pk)
            return room
        except Room.DoesNotExist:
            return None

    # detail view를 구현해야하니까 각 room에 대한 pk값을 꼭 받아줘야한다
    def get(self, request, pk):
        # print(pk)
        # get_room 메소드 실행후 특정 room 받아오기
        room = self.get_room(pk)
        if room is not None:
            serializer = RoomSerializer(room).data
            return Response(data=serializer)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # room edit 기능
    def put(self, request, pk):
        room = self.get_room(pk)
        if room is not None:
            if room.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            # partial=True를 해야만 부분적으로 업데이트 했을때도 정상 작동이 가능함
            # 여기서 room을 건네줬다는것 자체가 instance가 되는 기존에 존재하는 room이 있다는 뜻을 의미한다
            # 따라서 serializer는 이것을 기준으로 create인지 update인지 구분한다
            # 여기서는 room이 있으니 update로 판단한다
            serializer = RoomSerializer(room, data=request.data, partial=True)
            # def validate(self, data):를 통과한 경우 if serializer.is_valid() 가 True가 됨
            if serializer.is_valid():
                # update한 내용을 받아서 저장하고 room에 할당한다
                room = serializer.save()
                # 업데이트하고 저장된 항목을 가지고 RoomSerializer에 집어넣어 return을 받는다
                return Response(RoomSerializer(room).data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response()
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # room delete 기능
    def delete(self, request, pk):
        # get_room 메소드 실행후 특정 room 받아오기
        room = self.get_room(pk)
        if room is not None:
            # host와 현재 유저가 같은 유저인지 확인
            if room.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            room.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def room_search(request):
    # request(url)에서 max_price를 찾아보렴~ 만약에 없으면 그건 None으로 하면 된단다 라는 뜻
    max_price = request.GET.get("max_price", None)
    min_price = request.GET.get("min_price", None)
    beds = request.GET.get("beds", None)
    bedrooms = request.GET.get("bedrooms", None)
    bathrooms = request.GET.get("bathrooms", None)
    lat = request.GET.get("lat", None)
    lng = request.GET.get("lng", None)
    # 검색 조건을 담고 있는 dictionary 생성
    filter_kwargs = {}
    if max_price is not None:
        # filter 조건을 filter_kwargs[] 내부에 넣어준다
        # https://docs.djangoproject.com/en/3.1/ref/models/querysets/#field-lookups
        # lte : ~보다 작거나 같음, gte:~보다 크거나 같음 등
        filter_kwargs["price__lte"] = max_price
    if min_price is not None:
        filter_kwargs["price__gte"] = min_price
    if beds is not None:
        filter_kwargs["beds__gte"] = beds
    if bedrooms is not None:
        filter_kwargs["bedrooms__gte"] = bedrooms
    if bathrooms is not None:
        filter_kwargs["bathrooms__gte"] = bathrooms
    # 주소창에 http://127.0.0.1:8000/api/v1/rooms/search/?max_price=30&beds=2&bathrooms=2 이렇게 넣고 검색한 뒤 그 결과인 filter_kwargs를 print하여 확인해본다
    # print(filter_kwargs)
    # *을 이용해서 filter_kwargs를 unpack하면 key값의 이름만 나오게 된다
    # print(*filter_kwargs)
    # **filter_kwargs는 price__lte='30, beds__gte='2', bathrooms__gte='2'를 뱉는다
    #  -> print는 이를 이해할 수 없다
    paginator = OwnPagination()
    if lat is not None and lng is not None:
        filter_kwargs["lat__gte"] = float(lat) - 0.005
        filter_kwargs["lat__lte"] = float(lat) + 0.005
        filter_kwargs["lng__gte"] = float(lng) - 0.005
        filter_kwargs["lng__lte"] = float(lng) + 0.005
    try:
        # filter_kwargs의 내용으로 Room에서 검색을 해준다(filter 이용)
        # 검색 내용인 **filter_kwargs를 filter object에 전달
        # 그리고 그 결과를 rooms에 담아놓는다
        rooms = Room.objects.filter(**filter_kwargs)
    except ValueError:
        rooms = Room.objects.all()
    results = paginator.paginate_queryset(rooms, request)
    serializer = RoomSerializer(results, many=True)
    return paginator.get_paginated_response(serializer.data)
