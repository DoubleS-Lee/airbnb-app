from rest_framework.permissions import BasePermission


# https://www.django-rest-framework.org/api-guide/permissions/#custom-permissions
# def has_permission은 일반적인 list에 대한 permission을 수정하는 메소드이고
# def has_object_permission은 특정 object(여기서는 room)에 대한 permission을 수정하는 메소드임
# 여기서는 rooms/<int:pk>에 해당하는 특정 object(=room)에 대한 권한을 수정해야하기 때문에 def has_object_permission을 수정해 줌
class IsOwner(BasePermission):
    def has_object_permission(self, request, view, room):
        # room.user == request.user 이면 True를 return 함
        return room.user == request.user