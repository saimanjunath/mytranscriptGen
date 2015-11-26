
from django.shortcuts import render
from django.http import HttpResponse
from .models import user
import cgi
import os
import json
from django.conf import settings
from django.template import RequestContext, loader


def index(request):
    return render(request, 'transcriptG/index1.html')

def register(request):
	return render(request,'transcriptG/register.html')
def validate(request):
    print 'im in validate method'
    """return HttpResponse("Hello, world. You're at the polls index.")"""
    First_name = request.GET.get('First_name')
    Last_name = request.GET.get('Last_name')
    EmailId = request.GET.get('EmailId')
    password = request.GET.get('password')
    userType = request.GET.get('userType')
    response = {}
    
    if not user.objects.filter(Fname=First_name):
        
        s = user(Fname=First_name,Lname = Last_name, Email = EmailId,password= password,userType=userType)
        s.save()
        
        response['status'] = 'sucess'
    else:
        
        response['status'] = 'failure'
    json_data = json.dumps(response)
    
    return HttpResponse(json_data, content_type = "application/json")
    return HttpResponse(s)