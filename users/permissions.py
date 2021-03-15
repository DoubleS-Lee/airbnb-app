from rest_framework.permissions import BasePermission


class IsSelf(BasePermission):
    def has_object_permission(self, request, view, user):
        # 검색된 user가 현재 로그인된 user(=request.user)와 같은 경우 True를 반환
        return user == request.user