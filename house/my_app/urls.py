from django.urls import path
from .views import (RegisterView, CustomLoginView, LogoutView, UserProfileAPIView,
                    PropertyAPIView, ReviewAPIView, CreatePropertyAPIView, CreateReviewAPIView,
                    UpdateDeletePropertyAPIView, UpdateDeleteReviewAPIView)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileAPIView.as_view(), name='profiles'),
    path('property/', PropertyAPIView.as_view(), name='properties'),
    path('create_property/', CreatePropertyAPIView.as_view(), name='create_properties'),
    path('update_delete_property/', UpdateDeletePropertyAPIView.as_view(), name='update_delete_properties'),
    path('review/', ReviewAPIView.as_view(), name='review'),
    path('create_review/', CreateReviewAPIView.as_view(), name='create_review'),
    path('update_delete_review/', UpdateDeleteReviewAPIView.as_view(), name='update_delete_review'),
]
