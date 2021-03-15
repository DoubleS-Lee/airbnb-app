from .models import Room
from .serializers import RoomSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .permissions import IsOwner
from rest_framework.decorators import action


# https://www.django-rest-framework.org/api-guide/viewsets/#viewsets
# RoomsView(get, post)와 RoomView(get, put, delete)를 RoomViewSet으로 변경
class RoomViewSet(ModelViewSet):

    # queryset과 serializer_class 설정이 필수임
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    # https://www.django-rest-framework.org/api-guide/viewsets/#viewset-actions
    # get(list, retrieve), post(create), put(update, partial_update), delete(destroy) 항목에 대해 유저의 접근권한을 다르게 설정해주는 메소드를 수정해준다
    # 기본적으로는 모든 유저에게 get, post, put, delete 항목이 접근가능하도록 오픈되어 있다
    # https://www.django-rest-framework.org/api-guide/permissions/
    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [permissions.AllowAny]
        elif self.action == "create":
            permission_classes = [permissions.IsAuthenticated]
        else:  # update, destroy, partial_update에 적용
            # IsOwner라는 클래스를 새로 만들어준다
            permission_classes = [IsOwner]
        # permission_classes 안에 있는 모든 permission에 대해 permission()을 실행시켜서 배열에 넣으라는 뜻
        return [permission() for permission in permission_classes]
        # 밑에 세줄이 위의 1줄과 같은 역할을 함
        # called_perm = []
        # for p in permittions_classes:
        #     called_perm.append(p())

    # viewset에 추가적인 기능을 넣고 싶다면 action을 사용하면 된다
    # urls.py에서 url을 지정해주지 않아도 메소드 명(search)으로 자동적으로 url을 생성해준다
    # https://www.django-rest-framework.org/api-guide/viewsets/#marking-extra-actions-for-routing
    # detail을 결정해줘야하는데 False라고 하면 이 메소드는 /rooms/에만 적용이되고
    # True라고 하면 이 메소드는 rooms/1에 적용이 된다
    @action(detail=False)
    def search(self, request):
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
        # ViewSet은 paginator(numberPaginator)를 기본으로 내장하고 있다. 그냥 이걸 불러와준 것이다
        paginator = self.paginator
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
