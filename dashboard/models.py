from django.db import models
from django.contrib.auth.models import User

class Widget(models.Model):
    name = models.CharField(max_length=255)
    widget_type = models.CharField(max_length=50)  # e.g., sales, inventory, etc.
    content = models.TextField(default='Widget Content')  # Default content for the widget

    def __str__(self):
        return self.name

class Dashboard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    layout = models.JSONField(default=dict)  # JSON to store widget positions

    def __str__(self):
        return f"{self.user.username}'s Dashboard"

class Alert(models.Model):
    type = models.CharField(max_length=255)  # e.g., Low Stock
    message = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.type}: {self.message}"
