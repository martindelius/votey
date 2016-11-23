import datetime

from django.utils import timezone
from django.test import TestCase

from .models import Question


class QuestionMethodTests(TestCase):

	def test_is_finished_with_future_question(self):
		time = timezone.now() + datetime.timedelta(days=30)
		future_question = Question(pub_date=time)
		self.assertIs(future_question.is_finished(), False)

        def test_is_finished_with_less_than_duration_question(self):
                time = timezone.now() - datetime.timedelta(days=1) + datetime.timedelta(seconds=1)
                future_question = Question(pub_date=time, duration=1)
                self.assertIs(future_question.is_finished(), False)

# Create your tests here.
