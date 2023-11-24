from django.urls import path
from activity_log.activity.apis.v1 import activity_logs, topic, item, source, learning_resource

urlpatterns = [
    path('activity_logs', activity_logs.ActivityLogsApi.as_view(), name="activity_logs"),
    path('topics', topic.TopicsApi.as_view(), name="topics"),
    path('items', item.ItemsApi.as_view(), name="items"),
    path('sources', source.SourcesApi.as_view(), name="sources"),
    path('learning_resources', learning_resource.LearningResourcesApi.as_view(), name="learning_resources"),
]
