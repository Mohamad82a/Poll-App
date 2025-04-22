from random import choices

from rest_framework import serializers
from polls.models import Poll, PollChoices, Vote

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollChoices
        fields = ['id','choice_text']
        extra_kwargs = {
            'id': {'required': False},
        }

class PollSerializers(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    # choices = serializers.StringRelatedField(many=True)
    choices = ChoiceSerializer(many=True, required=False)
    class Meta:
        model = Poll
        fields = ['id','owner', 'title','active', 'publish_date', 'updated_at', 'choices']
        read_only_fields = ('id', 'active', 'publish_date', 'updated_at')

    def create(self, validated_data):
        validated_data['owner'] = self.context['request'].user
        validated_data['active'] = True
        choices_data = validated_data.pop('choices', [])
        poll = Poll.objects.create(**validated_data)
        for choice_data in choices_data:
            PollChoices.objects.create(poll=poll, **choice_data)

        return poll

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.save()

        if 'choices' in validated_data:
            self.updatechoice(instance, validated_data['choices'])

        return instance

    def updatechoice(self, poll, choices_data):
        poll.choices.all().delete()
        for choice_data in choices_data:
            PollChoices.objects.create(poll=poll, **choice_data)



