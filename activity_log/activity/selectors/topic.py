from typing import Optional
from django.db.models import QuerySet
from activity_log.activity.models import Topic
from activity_log.activity.filters.topic import TopicsFiter


def get_topic(topic_id: int) -> Optional[Topic]:
    try:
        return Topic.objects.get(id=topic_id)
    except Topic.DoesNotExist:
        return None


def get_filtered_topics(*, filters=None) -> QuerySet[Topic]:
    filters = filters or {}
    qs = Topic.objects.filter().order_by('-id')
    return TopicsFiter(filters, qs).qs
