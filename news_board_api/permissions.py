from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS


class IsAuthenticatedOrCreate(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        return super(IsAuthenticatedOrCreate, self).has_permission(request, view)


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
