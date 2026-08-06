# house/my_app/serializers.py

from rest_framework import serializers
from .models import UserProfile, Property, Review, HousePredict
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.conf import settings
import joblib
import os


# ── Загрузка ML-артефактов один раз при старте ────────────────────────────────
def _load_ml():
    model  = joblib.load(os.path.join(settings.BASE_DIR, 'lin_model_House.pkl'))
    scaler = joblib.load(os.path.join(settings.BASE_DIR, 'scaler_House.pkl'))
    return model, scaler

_house_model, _house_scaler = _load_ml()


# ── Auth ───────────────────────────────────────────────────────────────────────
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'phone_number', 'role', 'created_at')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return UserProfile.objects.create_user(**validated_data)

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {'username': instance.username, 'email': instance.email},
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    email    = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {'username': instance.username, 'email': instance.email},
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


# ── Профиль ────────────────────────────────────────────────────────────────────
class UserProfileSerializer(serializers.ModelSerializer):
    created_at = serializers.DateField(format='%d-%m-%Y')

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'avatar', 'first_name',
                  'last_name', 'phone_number', 'role', 'created_at')
        extra_kwargs = {'password': {'write_only': True}}


class UserPublicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('role', 'first_name', 'last_name', 'phone_number')


# ── Недвижимость ───────────────────────────────────────────────────────────────
class PropertySerializer(serializers.ModelSerializer):
    created_at = serializers.DateField(format='%d-%m-%Y')
    seller     = UserPublicInfoSerializer(read_only=True)

    class Meta:
        model = Property
        fields = ('title', 'description', 'property_type', 'region', 'city',
                  'district', 'address', 'area', 'price', 'rooms', 'floor',
                  'total_floors', 'condition', 'images', 'documents', 'seller', 'created_at')


class CreatePropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ('title', 'description', 'property_type', 'region', 'city',
                  'district', 'address', 'area', 'price', 'rooms', 'floor',
                  'total_floors', 'condition', 'images', 'documents', 'seller')


# ── Отзывы ─────────────────────────────────────────────────────────────────────
class ReviewSerializer(serializers.ModelSerializer):
    created_at = serializers.DateField(format='%d-%m-%Y')
    buyer      = UserPublicInfoSerializer(read_only=True)
    seller     = UserPublicInfoSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ('buyer', 'seller', 'rating', 'comment', 'created_at')


class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('seller', 'rating', 'comment', 'buyer')


# ── ML: предсказание цены ──────────────────────────────────────────────────────
class HousePredictSerializer(serializers.ModelSerializer):
    predicted_price = serializers.SerializerMethodField()

    class Meta:
        model = HousePredict
        fields = '__all__'

    def get_predicted_price(self, obj) -> float:
        features = [[
            obj.area,
            obj.rooms,
            obj.floor,
            obj.total_floors,
        ]]
        scaled = _house_scaler.transform(features)
        return round(float(_house_model.predict(scaled)[0]), 2)