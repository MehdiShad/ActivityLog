from typing import Optional
from django.db.models import QuerySet
from activity_log.activity.models import LearningResource
from activity_log.activity.filters.learning_resource import LearningResourcesFiter


def get_learning_resource(learning_resource_id: int) -> Optional[LearningResource]:
    try:
        return LearningResource.objects.get(id=learning_resource_id)
    except LearningResource.DoesNotExist:
        return None


def get_filtered_learning_resources(*, filters=None) -> QuerySet[LearningResource]:
    filters = filters or {}
    qs = LearningResource.objects.filter().order_by('-id')
    return LearningResourcesFiter(filters, qs).qs
