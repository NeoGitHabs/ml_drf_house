import django_filters
from .models import Property, Review

class PropertyFilter(django_filters.FilterSet):
    price = django_filters.RangeFilter()

    class Meta:
        model = Property
        fields = {
            'region':['exact'],
            'city':['exact'],
            'district':['exact'],
            'area':['exact'],
            'rooms':['exact'],
            'documents':['exact'],
            'price':['gt', 'lt'],
            'created_at':['lt', 'gt']
        }

class ReviewFilter(django_filters.FilterSet):
    price = django_filters.RangeFilter()

    class Meta:
        model = Review
        fields = {
            'rating':['lt', 'gt'],
            'created_at':['lt', 'gt']
        }
