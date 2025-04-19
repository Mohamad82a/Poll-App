from rest_framework import serializers
from polls.models import Poll, PollChoices, Vote

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollChoices
        fields = ['choice_text']

class PollSerializers(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    # choices = serializers.StringRelatedField(many=True)
    choices = ChoiceSerializer(many=True)
    class Meta:
        model = Poll
        fields = ['id','owner', 'title','active', 'publish_date', 'updated_at', 'choices']
        read_only_fields = ('id', 'owner','active', 'publish_date', 'updated_at')

    def update(self, instance, validated_data):
        choices = validated_data.pop('choices', [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        instance.choices.all().delete()
        for choice in choices:
            PollChoices.objects.create(poll=instance, **choice)

        return instance


