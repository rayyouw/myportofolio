from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsPortfolioOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow superusers (portfolio owner) to edit/delete.
    Read permissions are allowed for any request (SAFE_METHODS).
    """
    message = "Only the portfolio owner can change projects."

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or (request.user.is_authenticated and request.user.is_superuser)
        )

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class IsPortfolioOwnerOrEditorOrReadOnly(BasePermission):
    """
    Custom permission for assignment section:
    - SAFE_METHODS (GET, HEAD, OPTIONS): allowed for everyone.
    - Superusers: full access (GET, POST, PUT, PATCH, DELETE).
    - Editors: can only update with PUT or PATCH.
    - Regular users and unauthenticated visitors: cannot modify data.
    """
    message = "Only the portfolio owner can create or delete data; editors can only update."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        return (
            request.method in ("PUT", "PATCH")
            and request.user.groups.filter(name="Editor").exists()
        )

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
