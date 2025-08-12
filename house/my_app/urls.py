from django.urls import path
from .views import UserProfileAPIView, PropertyAPIView, ReviewAPIView, CreatePropertyAPIView, CreateReviewAPIView
from .views import RegisterView, CustomLoginView, LogoutView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileAPIView.as_view(), name='profiles'),
    path('property/', PropertyAPIView.as_view(), name='properties'),
    path('create_property/', CreatePropertyAPIView.as_view(), name='create_properties'),
    path('review/', ReviewAPIView.as_view(), name='review'),
    path('create_review/', CreateReviewAPIView.as_view(), name='create_review'),
]
