from django_filters import rest_framework as filters
from events.models import Appointement
from django_filters import DateFromToRangeFilter


class AppointementFilter(filters.FilterSet):
    start = DateFromToRangeFilter()
    end = DateFromToRangeFilter()

    class Meta:
        model = Appointement
        fields = ("start", "end", "title")
