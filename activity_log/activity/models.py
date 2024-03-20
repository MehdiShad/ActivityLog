from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from activity_log.users.models import BaseUser
from django.db.models.signals import post_save
from activity_log.common.models import BaseModel
from activity_log.planing.models import Plan, PlanDetail, Purpose


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


class Item(BaseModel):
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
    manager = models.ForeignKey('Creator', on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return f"{self.fa_title}"


UnitOfMeasure_CHOICES = (
    ('page', 'صفحه'),
    ('minute', 'دقیقه'),
)


class Source(BaseModel):
    fa_name = models.CharField(max_length=255, null=True, blank=True)
    en_name = models.CharField(max_length=255)
    domain = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.en_name


class LearningResource(BaseModel):
    title = models.CharField(max_length=255)
    item = models.ForeignKey(Item, models.CASCADE, null=True, blank=True)
    source = models.ForeignKey(Source, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    enrollment_date = models.DateField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    creators = models.ManyToManyField('Creator', related_name='learning_resource', null=True, blank=True)

    def __str__(self):
        return f"{self.title} :: {self.creators.first()}"


class Creator(BaseModel):
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    en_name = models.CharField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    github_address = models.URLField(null=True, blank=True)
    youtube_address = models.URLField(null=True, blank=True)
    linkedin_address = models.URLField(null=True, blank=True)
    linkedin_address = models.URLField(null=True, blank=True)
    telegram_address = models.URLField(null=True, blank=True)
    website_address = models.URLField(null=True, blank=True)
    twitter_address = models.URLField(null=True, blank=True)
    email_address = models.URLField(null=True, blank=True)
    instagram_address = models.URLField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    created_resources_creators = models.ManyToManyField('LearningResource', related_name='creator', null=True, blank=True)

    def __str__(self):
        if self.first_name is not None or self.last_name is not None:
            return f"{self.first_name} {self.last_name}"
        elif self.title is not None:
            return str(self.title)
        else:
            return "unknown"


class ActivityLog(BaseModel):
    activity_date = models.DateField(default=timezone.now, null=True, blank=True)
    activity_item = models.ForeignKey(Item, on_delete=models.CASCADE)
    purpose = models.ForeignKey(Purpose, on_delete=models.CASCADE, null=True, blank=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True, blank=True)
    activity_source = models.ForeignKey(Source, on_delete=models.PROTECT, null=True, blank=True)
    learning_resource = models.ForeignKey(LearningResource, on_delete=models.CASCADE, null=True, blank=True)
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE, null=True, blank=True)
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
