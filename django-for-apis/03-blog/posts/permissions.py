from rest_framework import permissions

# we are creating our own permission here just like "isAuthenticatedOnly"
class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        
        # authenticated users only can see list view
        if request.user.is_authenticated:
            return True
        
        return False
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request so we'll always
        # GET, HEAD, or OPTIONS requests

        if request.method in permissions.SAFE_METHODS:
            return True
        
        # the object that we are pertaining here is the object/instance of the mode
        # hence if we have a class view and we have this as the value of the permission_classes
        # it will require a model
        return obj.author == request.user  # if the same this will be true
    
    