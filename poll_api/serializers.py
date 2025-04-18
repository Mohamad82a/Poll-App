from rest_framework import serializers
from polls.models import Poll, PollChoices, Vote

class PollSerializers(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Poll
        fields = "__all__"
        read_only_fields = ('id','active','created_at','updated_at')
