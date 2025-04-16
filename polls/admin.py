from django.contrib import admin

from .models import *

# Register your models here.

class PollChoicesInline(admin.TabularInline):
    model = PollChoices
    extra = 1
    # classes = ['collapse']

class VoteInline(admin.TabularInline):
    model = Vote
    extra = 0
    # classes = ['collapse']

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title', 'owner',)
    inlines = [PollChoicesInline, VoteInline]


admin.site.register(PollChoices)
admin.site.register(Vote)