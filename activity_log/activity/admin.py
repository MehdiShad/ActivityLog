from django.contrib import admin
from activity_log.activity import models

# Register your models here.

@admin.register(models.Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['fa_title', 'en_title']


@admin.register(models.ActivityItem)
class ActivityItemAdmin(admin.ModelAdmin):
    list_display = ['fa_title', 'en_title', 'content_type']


@admin.register(models.ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    # todo: how to change format of created_at in admin panel
    list_display = ['activity_item', 'activity_date', 'plan', 'is_holiday', 'amount', 'unit_of_measure', 'rate']
    list_editable = ['activity_date', 'is_holiday', 'rate']
    # list_filter = ['activity_item']
    search_fields = ['activity_date', ]


@admin.register(models.ActivitySource)
class ActivitySourceAdmin(admin.ModelAdmin):
    list_display = ['id', 'fa_name', 'en_name']
    list_editable = ['fa_name', 'en_name']
    list_filter = ['fa_name', 'en_name']
    search_fields = ['fa_name', 'en_name']