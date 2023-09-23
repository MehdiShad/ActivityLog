from django.contrib import admin
from .models import Topic, ActivityItem, ActivityLog


# Register your models here.

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['fa_title', 'en_title']


@admin.register(ActivityItem)
class ActivityItemAdmin(admin.ModelAdmin):
    list_display = ['fa_title', 'en_title', 'content_type']


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    # todo: how to change format of created_at in admin panel
    list_display = ['activity_item', 'activity_date', 'plan', 'is_holiday', 'amount', 'unit_of_measure', 'rate']
    list_editable = ['activity_date', 'is_holiday', 'rate']
    # list_filter = ['activity_item']
    search_fields = ['activity_date', ]