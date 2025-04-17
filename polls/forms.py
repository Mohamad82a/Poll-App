from django import forms
from .models import Poll, PollChoices

class PollAddForm(forms.ModelForm):
    choice1 = forms.CharField(label='Choice 1', max_length=100, min_length=1, widget=forms.TextInput(attrs={'class': 'form-control'}))
    choice2 = forms.CharField(label='Choice 2', max_length=100, min_length=1, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Poll
        fields = ('title', 'choice1', 'choice2')
        widgets = {
            'title': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols':20}),
        }


class PollEditForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['title',]
        widgets = {
            'title': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols':20}),
        }

class PollChoiceAddForm(forms.ModelForm):
    class Meta:
        model = PollChoices
        fields = ['choice_text']
        widgets = {
            'choice_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 20}),
        }