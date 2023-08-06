from django.db import models
from activity_log.common.models import BaseModel


# Create your models here.

class Purpose(BaseModel):
    title = models.CharField(max_length=355)
    year = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    comment = models.CharField(max_length=1000, null=True, blank=True)
    is_completed = models.BooleanField()
    effort_amount = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.title}"


class Plan(BaseModel):
    title = models.CharField(max_length=355)
    purpose = models.ForeignKey(Purpose, on_delete=models.CASCADE, null=True, blank=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    comment = models.CharField(max_length=1000, null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title}"


class Topic(BaseModel):
    fa_title = models.CharField(max_length=255)
    en_title = models.CharField(max_length=255)
    description = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f"{self.fa_title}"


UnitOfMeasure_CHOICES = (
    ('page', 'صفحه'),
    ('minute', 'دقیقه'),
)


class PlanDetail(BaseModel):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True, blank=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True, blank=True)
    is_completed = models.BooleanField()
    effort_amount_per_day = models.IntegerField()  # for each day
    unit_of_measure = models.CharField(max_length=75, choices=UnitOfMeasure_CHOICES, default='minute')
    description = models.CharField(max_length=555, null=True, blank=True)
    total_effort_time = models.IntegerField(null=True, blank=True)
    total_time_spent = models.IntegerField(default=0, null=True, blank=True)
    progress = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=0)

    def save(self, *args, **kwargs):
        if self.effort_amount_per_day and self.plan and self.plan.due_date and self.plan.created_at:
            duration = (self.plan.due_date - self.plan.created_at).days + 1
            print("duration", duration)
            self.total_effort_time = self.effort_amount_per_day * duration
        super(PlanDetail, self).save(*args, **kwargs)

    def calculate_progress(self):
        if self.total_effort_time > 0:
            total_spend_time = self.activitylog_set.aggregate(models.Sum('amount'))['amount__sum']
            if total_spend_time is not None:
                return (total_spend_time / self.total_effort_time) * 100
        return 0

    def calculate_total_time_spent(self):
        total_time_spent = self.activitylog_set.aggregate(models.Sum('amount'))['amount__sum']
        if total_time_spent is not None:
            return total_time_spent
        return 0

    def __str__(self):
        return f"{self.topic}"
