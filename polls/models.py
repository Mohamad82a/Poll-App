from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import secrets

from tinymce.models import HTMLField

class Poll(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = HTMLField()
    publish_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # def user_can_vote(self, user):
    #     """
    #     Returns False if the user already voted, True otherwise.
    #     """
    #

class PollChoices(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # @property
    # def vote_count(self):
    #     return self.vo



class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(PollChoices, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.user.username} - {self.poll.title[:15]} - {self.choice.choice_text[:15]}'
