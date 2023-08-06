from rest_framework.permissions import BasePermissionMetaclass

from drf_share_token.user import ShareTokenUser


class HasValidShareToken(metaclass=BasePermissionMetaclass):

    def has_permission(self, request, view):
        return view.action == 'retrieve'

    def has_object_permission(self, request, view, obj):

        if not request.user or not isinstance(request.user, ShareTokenUser):
            return False

        return request.user.model_name == f"{obj._meta.app_label}:{obj._meta.model_name}" \
            and request.user.model_pk == obj.pk
