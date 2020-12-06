from django.contrib import admin
from .models import LaundrySnapshot, LaundryHall

# Register your models here.

admin.site.register(LaundryHall)
admin.site.register(LaundrySnapshot)
