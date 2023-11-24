from django.urls import path, include

urlpatterns = [
    # path('blog/', include(('activity_log.blog.urls', 'blog'))),
    path('auth/', include(('activity_log.authentication.urls', 'auth'))),
    path('activity/', include(('activity_log.activity.urls', 'activity'))),
]
