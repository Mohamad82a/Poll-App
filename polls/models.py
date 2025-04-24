from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import secrets

from tinymce.models import HTMLField

class Poll(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField()
    publish_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def user_can_vote(self, user):
        """
        Returns False if user already voted, True otherwise.
        """
        user_votes = user.vote_set.all()
        qs = user_votes.filter(poll=self)
        if qs.exists():
            return False
        return True

    @property
    def get_all_vote_count(self):
        return self.votes.count()

    def get_result_dict(self):
        result = []
        for choice in self.choices.all():
            dict = {}
            alert_class = ['primary', 'secondary', 'success', 'danger', 'dark', 'warning', 'info']

            dict['alert_class'] = secrets.choice(alert_class)
            dict['text'] = choice.choice_text
            dict['number_of_votes'] = choice.get_vote_count_for_a_choice
            if not self.get_all_vote_count:
                dict['percentage'] = 0
            else:
                dict['percentage'] = (choice.get_vote_count_for_a_choice / self.get_all_vote_count) * 100

            result.append(dict)
        return result


class PollChoices(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_vote_count_for_a_choice(self):
        return self.vote_set.count()
    @property
    def percentage(self):
        return  (self.get_vote_count_for_a_choice / self.poll.get_all_vote_count) * 100

    def __str__(self):
        return f'{self.poll.title} - {self.choice_text[:15]}'



class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='votes')
    choice = models.ForeignKey(PollChoices, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.user.username} - {self.poll.title[:15]} - {self.choice.choice_text[:15]}'
