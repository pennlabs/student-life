from polls.models import Poll, PollOption
from rest_framework import serializers


class PollSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Poll
        fields = ["question_text", "org_author", "id", "expiration"]

    def create(self, validated_data):
        request = self.context.get("request", None)
        if request is None:
            return super().create(validated_data)
        return super().create(validated_data)

class PollOptionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PollOption
        fields = ["option_text", "id", "votes"]

    def create(self, validated_data):
        request = self.context.get("request", None)
        if request is None:
            return super().create(validated_data)
        return super().create(validated_data)
