from django.contrib import admin
from .models import Plan, Topic, PlanDetail, Purpose


# Register your models here.

@admin.register(Purpose)
class PurposeAdmin(admin.ModelAdmin):
    list_display = ['title', ]


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'due_date']


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['fa_title', 'en_title']


@admin.register(PlanDetail)
class PlanDetailAdmin(admin.ModelAdmin):
    list_display = ['topic', 'plan', 'effort_amount_per_day', 'total_effort_time', 'total_time_spent', 'unit_of_measure', 'progress']
