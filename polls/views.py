from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from polls.csrfExemptSessionAuthentication import CsrfExemptSessionAuthentication
from polls.models import Poll
from polls.serializers import PollSerializer

from rest_framework import generics, viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        return super().get_queryset()
        
    #TODO: use a decorator to restrict update, destroy and create to superuser's
    def update(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().destroy(request, *args, **kwargs)
        return self.restricted_for_superusers_error()

    def destroy(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().destroy(request, *args, **kwargs)
        return self.restricted_for_superusers_error()

    def create(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().create(request, *args, **kwargs)
        return self.restricted_for_superusers_error()

    def restricted_for_superusers_error(self):
        """ returns an error message to indicate that only superusers can access the request method """
        forbidden_error_json = {
            'error': 'only a superuser can create/update/delete polls'
        }
        forbidden_resp = JsonResponse(forbidden_error_json)
        forbidden_resp.status_code = 403
        return forbidden_resp
        