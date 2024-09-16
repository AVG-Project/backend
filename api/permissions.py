from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Только чтение если НЕ админ"""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:  # метод только для чтения
            return True

        return bool(request.user and request.user.is_staff)


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        #! Если у объекта есть поле создателя
        return obj.user == request.user

