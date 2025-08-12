from rest_framework import generics
from rest_framework import permissions
from .filters import PropertyFilter,ReviewFilter
from .models import UserProfile, Property, Review
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from .permissions import CheckBuyerRoleReviews, CheckSellerRoleReviews
from .serializers import UserProfileSerializer, PropertySerializer, ReviewSerializer, CreatePropertySerializer, CreateReviewSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .serializers import UserSerializer, LoginSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserProfileAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)

class PropertyAPIView(generics.ListAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = PropertyFilter, ReviewFilter
    ordering_fields = ['price', 'created_at']
    ordering = ['price']
    search_fields = ['title', 'comment']

class CreatePropertyAPIView(generics.CreateAPIView):
    serializer_class = CreatePropertySerializer

    permission_classes = [permissions.IsAuthenticated, CheckSellerRoleReviews]

class ReviewAPIView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class CreateReviewAPIView(generics.CreateAPIView):
    serializer_class = CreateReviewSerializer

    permission_classes = [permissions.IsAuthenticated, CheckBuyerRoleReviews]
