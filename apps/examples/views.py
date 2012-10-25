import os
import redis
from django.http import HttpResponse
from django.shortcuts import render
from tasks import send_a_letter
from forms import EmailForm

def email(request):
	if request.method == "POST":
		form = EmailForm(request.POST)
		if form.is_valid():
			send_a_letter.delay(form.cleaned_data["sender"],form.cleaned_data["recipient"],
				form.cleaned_data["subject"],form.cleaned_data["message"])
			return HttpResponse("all sent. thanks.")
	else:
		form = EmailForm()
	
	return render(request, 'examples/email.html', {
		'form' : form
	})