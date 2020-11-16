from polls.models import Poll
from rest_framework import serializers


class PollSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Poll
        fields = ["question", "org_author"]

    def create(self, validated_data):
        request = self.context.get("request", None)
        if request is None:
            return super().create(validated_data)
        return super().create(validated_data)
