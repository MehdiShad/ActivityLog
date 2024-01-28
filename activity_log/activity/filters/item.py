from django_filters import (CharFilter, FilterSet)
from activity_log.activity.models import Item


class ItemsFiter(FilterSet):
    class Meta:
        model = Item
        fields = ('fa_title', 'en_title', 'content_type')
