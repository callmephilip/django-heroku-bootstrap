import os
import redis
from django.http import HttpResponse
from tasks import send_a_letter

def email(request):
	send_a_letter.delay(sender, recipient, subject, body)
	return HttpResponse("Letter sent")