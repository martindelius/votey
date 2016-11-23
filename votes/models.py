# -*- coding: latin-1 -*-
from __future__ import unicode_literals

import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Question(models.Model):
	question_title = models.CharField(max_length=50)
	question_text = models.CharField(max_length=1000)
	pub_date = models.DateTimeField('date published')
	duration = models.IntegerField(default=1)

	def __str__(self):
		return self.question_text

	def is_finished(self):
		return self.pub_date <= timezone.now() - datetime.timedelta(days=self.duration)
	is_finished.admin_order_field = 'pub_date'
	is_finished.boolean = True
	is_finished.short_description = 'Abstimmung beendet?'

class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=50)
	votes = models.IntegerField(default=0, editable = False)

	def __str__(self):
		return self.choice_text

class Token(models.Model):
	token = models.CharField(max_length=6, editable = True)
	used = models.BooleanField(default = False, editable = False)
	used_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

	def __str__(self):
                return self.token

class Votes(models.Model):
	token = models.ForeignKey(Token, on_delete=models.CASCADE, editable = False)
	question = models.ForeignKey(Question, on_delete=models.CASCADE, editable = False)
	voting_time = models.DateTimeField(auto_now_add=True, editable = False)

	def __str__(self):
		return str(self.token)

