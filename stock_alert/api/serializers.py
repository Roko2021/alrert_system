from rest_framework import serializers
from .models import Alert, TriggeredAlert
from django.contrib.auth.models import User

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = '__all__'
        read_only_fields = ['user', 'created_at']

class TriggeredAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = TriggeredAlert
        fields = '__all__'




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")

class AlertSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Alert
        fields = [
            "id",
            "user",
            "stock_symbol",
            "alert_type",
            "threshold_value",
            "condition",
            "duration_hours",
            "is_active",
        ]
