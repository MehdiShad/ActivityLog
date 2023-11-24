from django_filters import (CharFilter, FilterSet)
from activity_log.activity.models import Source


class SourcesFiter(FilterSet):
    class Meta:
        model = Source
        fields = ('fa_name', 'en_name')
