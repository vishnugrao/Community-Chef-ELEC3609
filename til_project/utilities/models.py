from django.db import models

class Report(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=256)
    description = models.TextField()