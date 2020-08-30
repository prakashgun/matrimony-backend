import datetime

from django_filters import rest_framework as filters

from . import models


class ProfileFilter(filters.FilterSet):
    min_weight = filters.NumberFilter(field_name='weight', lookup_expr='gte')
    max_weight = filters.NumberFilter(field_name='weight', lookup_expr='lte')
    min_age = filters.NumberFilter(method='filter_min_age')
    max_age = filters.NumberFilter(method='filter_max_age')

    class Meta:
        model = models.Profile
        fields = ('gender', 'min_weight', 'max_weight', 'min_age', 'max_age',
                  'marital_status')

    def filter_min_age(self, queryset, name, value):
        return queryset.filter(
            dob__lte=datetime.date.today() - datetime.timedelta(
                days=int(value) * 360))

    def filter_max_age(self, queryset, name, value):
        return queryset.filter(
            dob__gte=datetime.date.today() - datetime.timedelta(
                days=int(value) * 360))
