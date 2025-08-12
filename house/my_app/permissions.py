from rest_framework import permissions


class CheckBuyerRoleReviews(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'buyer':
            return True
        return False


class CheckSellerRoleReviews(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'seller':
            return True
        return False
