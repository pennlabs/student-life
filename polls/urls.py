from django.urls import include, path
from polls.views import (
    PollViewSet
)
from . import views #comment later
from rest_framework import routers


router = routers.DefaultRouter()

router.register(r"", PollViewSet)

urlpatterns = [
    path(r"", include(router.urls))
]
