from django.db import models
from django.contrib.auth.models import User

class Alert(models.Model):
    ALERT_TYPE_CHOICES = (
        ('threshold', 'Threshold'),
        ('duration', 'Duration'),
    )
    CONDITION_CHOICES = (
        ('gt', '>'),
        ('lt', '<'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alerts')
    stock_symbol = models.CharField(max_length=10)  # رمز السهم (مثل AAPL)
    alert_type = models.CharField(max_length=10, choices=ALERT_TYPE_CHOICES)
    condition = models.CharField(max_length=2, choices=CONDITION_CHOICES)
    threshold_value = models.FloatField(null=True, blank=True)
    duration_hours = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.stock_symbol} ({self.alert_type})"

class TriggeredAlert(models.Model):
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, related_name='triggered_alerts')
    triggered_at = models.DateTimeField(auto_now_add=True)
    current_price = models.FloatField()

    def __str__(self):
        return f"Triggered: {self.alert.stock_symbol} at {self.current_price}"
