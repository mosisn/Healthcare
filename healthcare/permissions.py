from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit an object.
    All other users can only view the object.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class IsDoctorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow doctors to edit their own records.
    All other users can only view the records.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user and request.user.role == 'doctor'

class IsPatientOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow patients to edit their own records.
    All other users can only view the records.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user and request.user.role == 'patient'
