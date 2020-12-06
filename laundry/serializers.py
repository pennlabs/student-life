from laundry.models import LaundryHall, LaundrySnapshot
from rest_framework import serializers

class LaundryHallSerializer(serializers.Serialization):
    class Meta:
        model = LaundryHall
        fields = (
            'name',
            'hall',
            'total_washers'
            'total_dryers',
        )


class LaundrySnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = LaundrySnapshot
        fields = (
            'date',
            'washers_available',
            'dryers_available'
        )
    
    def save(self):
        self.validated_data['hall'] = LaundryHall.objects.get(
            pk=self.context['views'].kwargs['hall_pk']
        )
        return super.save()
