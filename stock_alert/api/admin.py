from django.contrib import admin
from .models import (Alert,TriggeredAlert)

# Register your models here.

admin.site.register(Alert)
admin.site.register(TriggeredAlert)