from typing import Optional
from django.db.models import QuerySet
from activity_log.activity.models import ActivityLog
from activity_log.activity.filters.activity_logs import ActivityLogsFiter


def get_activity_log(activity_log: int) -> Optional[ActivityLog]:
    try:
        return ActivityLog.objects.get(id=activity_log)
    except ActivityLog.DoesNotExist:
        return None


def get_filtered_activity_log(*, filters=None) -> QuerySet[ActivityLog]:
    filters = filters or {}
    qs = ActivityLog.objects.filter().order_by('-id')
    return ActivityLogsFiter(filters, qs).qs
