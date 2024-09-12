from django.core.mail import EmailMessage, BadHeaderError
from django.shortcuts import render
from templated_mail.mail import BaseEmailMessage
from django.http import HttpResponse



# Create your views here.
def hello(request):
    
    try:
       message = BaseEmailMessage(
           template_name= 'email/hello.html',
           context= {'name': 'Ajith'}
           
       )
       message.send(["XGqB0@example.com"])
    except BadHeaderError:
        return HttpResponse("Invalid header found.")
    
    # send_mail("hello", "hello", "XGqB0@example.com", ["XGqB0@example.com"], fail_silently=False)
    return render(request, "hello.html")
