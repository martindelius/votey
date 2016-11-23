# -*- coding: latin-1 -*-
from django.contrib import admin

from .models import Choice, Question, Token, Votes

# Register your models here.

class ChoiceInline(admin.TabularInline):
    model = Choice
    readonly_fields = ['votes']
    extra = 0

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_title']}),
	(None,               {'fields': ['question_text']}),
        ('Startdatum und Uhrzeit', {'fields': ['pub_date'], 'classes': ['collapse']}),
	('Dauer', {'fields': ['duration'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]

    list_display = ('question_title', 'pub_date', 'is_finished')
    list_filter = ['pub_date']

class TokenAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['token']}),
    ]

    list_display = ('token', 'used', 'used_by')

class VotesAdmin(admin.ModelAdmin):
    fieldsets = [
    ]

    list_display = ('token', 'question', 'voting_time')

admin.site.register(Votes, VotesAdmin)
admin.site.register(Token, TokenAdmin)
admin.site.register(Question, QuestionAdmin)
