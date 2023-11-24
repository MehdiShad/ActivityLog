from django_filters import (CharFilter, FilterSet)
from activity_log.activity.models import Topic


class TopicsFiter(FilterSet):
    class Meta:
        model = Topic
        fields = ('fa_title', 'en_title')
