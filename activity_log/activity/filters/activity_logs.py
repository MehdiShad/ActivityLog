from django_filters import (CharFilter, FilterSet)
from activity_log.activity.models import ActivityLog


class ActivityLogsFiter(FilterSet):
    class Meta:
        model = ActivityLog
        fields = ('activity_item', 'is_holiday')
