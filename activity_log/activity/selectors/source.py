from typing import Optional
from django.db.models import QuerySet
from activity_log.activity.models import Source
from activity_log.activity.filters.source import SourcesFiter


def get_source(source_id: int) -> Optional[Source]:
    try:
        return Source.objects.get(id=source_id)
    except Source.DoesNotExist:
        return None


def get_filtered_sources(*, filters=None) -> QuerySet[Source]:
    filters = filters or {}
    qs = Source.objects.filter().order_by('-id')
    return SourcesFiter(filters, qs).qs
