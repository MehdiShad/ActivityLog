from django.urls import path
from activity_log.activity.apis.v1 import activity_logs, topic

urlpatterns = [
    path('activity_logs', activity_logs.ActivityLogsApi.as_view(), name="activity_logs"),
    path('topics', topic.TopicsApi.as_view(), name="activity_logs"),
]
