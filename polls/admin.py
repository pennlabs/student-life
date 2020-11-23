from django.contrib import admin
from polls.models import Poll, PollOption

admin.site.register(Poll)
admin.site.register(PollOption)