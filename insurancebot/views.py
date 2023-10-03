from django.shortcuts import render
from twilio.rest import Client
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import os
import shutil
import requests
from static.download_file import download_file_by_name

account_sid = 'ACc847352725a3bfa3c8ba8eb31cb79059'
auth_token = '0a6543dcc7cf6538f8a7d4d0b666f721'
client = Client(account_sid, auth_token)

allowed_extensions = ['.pdf', '.jpg', '.jpeg']
destination_folder = "D:\Django\insurance\documents"


sender_name = ""

greet_responses = {"hi":f"Hi {sender_name}, I'm a Assistant from PM Investment.Please pick a service from below\n 1. Download Policy\n 2. Ask about Insurance",
                    "Hello":f"Hello {sender_name}, I'm a Assistant from PM Investment.Please pick a service from below\n 1. Download Policy\n 2. Ask about Insurance",
                    "No":"I don't understand that",
                    "exit":"Goodbye, Have a nice day!",
                    "how are you": "I'm just a computer program, but thanks for asking!",
                    "goodbye": "Goodbye! Have a great day!",
                    "thanks": "You're welcome!",
                    "help": "Sure, I'm here to help. What do you need?",
                    "1":"Which type of policy you need?",
                    "2":"A. Vehicle\n B. Health\n C. General\n",
                    "A":"Send your Driving License",
                    "B": "Type filename with extension",
                    }

@csrf_exempt
def insurancebot(request):
    message=request.POST["Body"]
    global sender_name
    sender_name=request.POST["ProfileName"]
    sender_number=request.POST["From"]
    
   

    for keyword, responses in greet_responses.items():
        if message.lower() == keyword:
            response = responses
      

    
    client.messages.create(
        from_='whatsapp:+14155238886',
        body=response,
        to=sender_number)
    
    print(message)
    return HttpResponse("Hello")