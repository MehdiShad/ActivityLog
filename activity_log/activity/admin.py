from django.contrib import admin
from activity_log.activity import models


# Register your models here.

@admin.register(models.Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['fa_title', 'en_title']


@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['fa_title', 'en_title', 'content_type']


@admin.register(models.ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    # todo: how to change format of created_at in admin panel
    list_display = ['activity_item', 'activity_source', 'creator', 'amount', 'activity_date', 'learning_resource', 'is_holiday', 'plan']
    list_editable = ['is_holiday', 'learning_resource', 'amount', 'activity_source', 'creator']
    # list_filter = ['activity_item']
    search_fields = ['activity_item']
    # list_filter = ['activity_item']


@admin.register(models.Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ['id', 'fa_name', 'en_name']
    list_editable = ['fa_name', 'en_name']
    list_filter = ['fa_name', 'en_name']
    search_fields = ['fa_name', 'en_name']


@admin.register(models.LearningResource)
class LearningResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'source', 'item']
    list_editable = ['item', 'source']


@admin.register(models.Creator)
class CreatorAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'title', 'en_name', 'github_address', 'youtube_address']
    list_editable = ['title', 'en_name', 'github_address', 'youtube_address']
    list_display_links = ['id', 'first_name', 'last_name']