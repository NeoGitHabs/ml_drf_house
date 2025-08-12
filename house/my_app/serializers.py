from rest_framework import serializers
from .models import UserProfile, Property, Review
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'phone_number', 'role', 'created_at')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class UserProfileSerializer(serializers.ModelSerializer):
    created_at = serializers.DateField(format='%d-%m-%Y %H:%M')
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'avatar', 'first_name', 'last_name', 'phone_number', 'role', 'created_at')
        extra_kwargs = {'password': {'write_only': True}}

class UserPublicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('role', 'first_name', 'last_name', 'phone_number')

class PropertySerializer(serializers.ModelSerializer):
    created_at = serializers.DateField(format='%d-%m-%Y %H:%M')
    seller = UserPublicInfoSerializer(read_only=True)
    class Meta:
        model = Property
        fields = ('title', 'description', 'property_type', 'region', 'city', 'district', 'address', 'area', 'price', 'rooms', 'images', 'documents', 'seller', 'created_at')

class CreatePropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ('title', 'description', 'property_type', 'region', 'city', 'district', 'address', 'area', 'price', 'rooms', 'images', 'documents', 'seller')

class ReviewSerializer(serializers.ModelSerializer):
    created_at = serializers.DateField(format='%d-%m-%Y %H:%M')
    buyer = UserPublicInfoSerializer(read_only=True)
    seller = UserPublicInfoSerializer(read_only=True)
    class Meta:
        model = Review
        fields = ('buyer', 'seller', 'rating', 'comment', 'created_at')

class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('seller', 'rating', 'comment', 'buyer')
