from django.urls import include, path
from gsr_booking.views import GroupMembershipViewSet, GroupViewSet, UserViewSet
from rest_framework import routers


router = routers.DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'membership', GroupMembershipViewSet)
router.register(r'groups', GroupViewSet)

urlpatterns = [
    path(r'', include(router.urls))
]