from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User

from .models import Alert, TriggeredAlert
from .serializers import AlertSerializer, TriggeredAlertSerializer, UserSerializer


class AlertViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AlertSerializer

    def get_queryset(self):
        return Alert.objects.filter(user=self.request.user, is_active=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TriggeredAlertViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TriggeredAlertSerializer

    def get_queryset(self):
        return TriggeredAlert.objects.filter(alert__user=self.request.user).order_by("-triggered_at")


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    
    username = request.data.get("username", "")
    email = request.data.get("email", "")
    password = request.data.get("password", "")

    username = username.strip()  # إزالة الفراغات من الجوانب
    email = email.strip()
    print(f"Register attempt with username: '{username}'")


    if User.objects.filter(username__iexact=username).exists():
        # __iexact لمطابقة اسم المستخدم بدون فرق حالة الأحرف (case-insensitive)
        return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password)
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
