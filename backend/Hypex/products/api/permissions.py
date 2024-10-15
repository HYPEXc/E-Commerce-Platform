from rest_framework import permissions


class IsStaffEditorPermission(permissions.DjangoModelPermissions):
    """
    Custom permission to allow staff editor to modify, destroy, create and view a product.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and is a staff member
        if request.user and request.user.is_authenticated and request.user.is_staff:
            # Allow access to list and modify products
            if view.action in ['list', 'retrieve', 'create', 'update', 'partial_update', 'destroy']:
                return True

        # If not staff, deny permission
        return False


class IsProductOwnerPermission(permissions.DjangoModelPermissions):
    """
    Custom permission to only allow owners of a product to update it.
    """

    def has_permission(self, request, view):
        # Ensure the user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Check if the requesting user is the owner of the product
        return obj.owner == request.user
