from django.shortcuts import render
from django.http import HttpResponse
from polls.csrfExemptSessionAuthentication import CsrfExemptSessionAuthentication
from polls.models import Poll
from polls.serializers import PollSerializer

from rest_framework import generics, viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    # permission_classes = [IsAuthenticated]
    #TODO: uncomment above line about permission classes, since not anybody should be able to create a req.
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_queryset(self):
        # if not self.request.user.is_authenticated:
        #     return Poll.objects.none()
        #TODO: UNCOMMent above line later on
        return (
            super()
            .get_queryset()
        )