from django.core.mail import send_mail
from celery import task
import logging

@task()
def send_a_letter(sender, recipient, subject, body):
	send_mail(subject, body, sender, [recipient], fail_silently=False)