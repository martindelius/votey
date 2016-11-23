import string
import random
import csv

from optparse import OptionParser
from django.core.management.base import BaseCommand, CommandError
from votes.models import Token
from django.contrib.auth.models import User

class Command(BaseCommand):

	def add_arguments(self, parser):
		parser.add_argument('count', type=int)
		

		parser.add_argument(
            		'--file',
            		action='store',
            		dest='filename',
            		default="tokenlist.csv",
            		help='Save tokenlist to specified .csv file.',
        	)

	def handle(self, *args, **options):
		chars= string.ascii_letters + string.digits
		tlist=[]
		for t in range(options['count']):
			token = str()
			for _ in range(6):
				token +=random.choice(chars)
			tlist.append(token)	
			new_token = Token(token=token,used=False,used_by=User.objects.get(pk=1))
			new_token.save()

		if options['filename']:
			with open(options['filename'], 'wt') as csvfile:
				output_file = csv.writer(csvfile)
				output_file.writerow(tlist)
		
		return self.stdout.write(str(tlist))


