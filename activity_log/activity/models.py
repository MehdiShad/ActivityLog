from django.db import models
from activity_log.common.models import BaseModel
from activity_log.planing.models import Plan, PlanDetail, Purpose
from activity_log.users.models import BaseUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# Create your models here.

class Topic(BaseModel):
    fa_title = models.CharField(max_length=255)
    en_title = models.CharField(max_length=255)
    description = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f"{self.fa_title}"


CONTENT_TYPE_CHOICES = (
    ('learning', 'Learning'),  # Learning
    ('working', 'Working'),  # Outsource working
    ("developing", "Developing"),  # Developing for my self
    ('reading', 'Reading'),
    ('watching', 'Watching'),
    ('writing', 'Writing'),
    ('listening', 'Listening'),
)


class ActivityItem(BaseModel):
    class ContentTypeChoices(models.TextChoices):
        learning = 'learning', 'Learning',
        working = 'working', 'Working',
        developing = "developing", "Developing",
        reading = 'reading', 'Reading',
        watching = 'watching', 'Watching',
        writing = 'writing', 'Writing',
        listening = 'listening', 'Listening',

    fa_title = models.CharField(max_length=255)
    en_title = models.CharField(max_length=255)
    purpose = models.ForeignKey(Purpose, on_delete=models.CASCADE, null=True, blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True)
    content_type = models.CharField(max_length=110, choices=ContentTypeChoices.choices, default='learning')
    description = models.CharField(max_length=1000, null=True, blank=True)
    source_path = models.CharField(max_length=1000, null=True, blank=True)
    git_source = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f"{self.fa_title}"

UnitOfMeasure_CHOICES = (
    ('page', 'صفحه'),
    ('minute', 'دقیقه'),
)


class ActivitySource(BaseModel):
    fa_name = models.CharField(max_length=255, null=True, blank=True)
    en_name = models.CharField(max_length=255)
    domain = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.en_name


class ActivityLog(BaseModel):
    activity_date = models.DateField(default=timezone.now, null=True, blank=True)
    activity_item = models.ForeignKey(ActivityItem, on_delete=models.CASCADE)
    purpose = models.ForeignKey(Purpose, on_delete=models.CASCADE, null=True, blank=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True, blank=True)
    activity_source = models.ForeignKey(ActivitySource, on_delete=models.PROTECT, null=True, blank=True)
    plan_detail = models.ForeignKey(PlanDetail, on_delete=models.CASCADE, null=True, blank=True)
    base_user = models.ForeignKey(BaseUser, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField(max_length=555, null=True, blank=True)
    detail = models.TextField(null=True, blank=True)
    is_holiday = models.BooleanField(default=False)
    amount = models.IntegerField(verbose_name='amount', default=0)
    unit_of_measure = models.CharField(max_length=75, choices=UnitOfMeasure_CHOICES, default='minute')
    rate = models.DecimalField(decimal_places=2, max_digits=3, null=True, blank=True)
    links = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.activity_item}"


@receiver(post_save, sender=ActivityLog)
def update_plan_progress(sender, instance, **kwargs):
    plan_detail = instance.plan_detail
    if plan_detail:
        plan_detail.progress = plan_detail.calculate_progress()
        plan_detail.total_time_spent = plan_detail.calculate_total_time_spent()
        plan_detail.save()

