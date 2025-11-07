from django.db import models
from django.utils import timezone

class Lesson(models.Model):
    title = models.CharField(max_length=512, default='Untitled')
    filename = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField()
    summary = models.TextField(blank=True, null=True)
    simple_summary = models.TextField(blank=True, null=True)
    outline = models.JSONField(default=list) # list of bullet points
    created_at = models.DateTimeField(default=timezone.now)


class Meta:
    db_table = 'lessons'


def __str__(self):
    return f"{self.title} ({self.id})"