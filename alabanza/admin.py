from django.contrib import admin
from .models import (
    Coordinator,
    Group,
    Server,
    Assistance,
)

# Register your models here.
admin.site.register(Coordinator)
admin.site.register(Group)
admin.site.register(Server)
admin.site.register(Assistance)