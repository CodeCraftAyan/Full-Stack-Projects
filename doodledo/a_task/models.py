from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    PRIORITY_CHOICE = [
        ('urgent-important', 'Urgent and Important'),
        ('important-not-urgent', 'Important, but Not Urgent'),
        ('urgent-not-important', 'Urgent, but Not Important'),
        ('neither', 'Neither Urgent nor Important'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    time = models.DateTimeField()
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICE, default='neither')
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.get_priority_display()})"