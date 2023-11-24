from django_filters import (CharFilter, FilterSet)
from activity_log.activity.models import LearningResource


class LearningResourcesFiter(FilterSet):
    class Meta:
        model = LearningResource
        fields = ('title',)
