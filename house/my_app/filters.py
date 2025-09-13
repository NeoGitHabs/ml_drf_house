import django_filters
from .models import Property

class PropertyFilter(django_filters.FilterSet):
    price = django_filters.RangeFilter()
    area = django_filters.RangeFilter()
    floor = django_filters.RangeFilter()
    rooms = django_filters.RangeFilter()
    property_type = django_filters.ChoiceFilter(choices=Property.PROPERTY_TYPE)
    condition = django_filters.ChoiceFilter(choices=Property.CHOICE_CONDITION)
    has_images = django_filters.BooleanFilter(field_name='images', lookup_expr='isnull', exclude=True)
    only_sellers = django_filters.BooleanFilter(field_name='seller__role', lookup_expr='exact', method='filter_only_sellers')

    class Meta:
        model = Property
        fields = {
            'region': ['exact'],
            'city': ['exact'],
            'district': ['exact'],
            'area': ['exact', 'gt', 'lt'],
            'rooms': ['exact', 'gt', 'lt'],
            'documents': ['exact'],
            'price': ['gt', 'lt'],
            'created_at': ['lt', 'gt'],
            'property_type': ['exact'],
            'condition': ['exact'],
            'floor': ['exact', 'gt', 'lt'],
        }

    def filter_only_sellers(self, queryset, name, value):
        if value:
            return queryset.filter(seller__role='seller')
        return queryset
