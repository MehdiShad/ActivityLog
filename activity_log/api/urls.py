from django.urls import path, include

urlpatterns = [
    # path('blog/', include(('activity_log.blog.urls', 'blog'))),
    path('activity/', include(('activity_log.activity.urls', 'activity'))),
]
