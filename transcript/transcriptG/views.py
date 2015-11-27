
from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from .models import user,Student
import cgi
import os
import json
from django.conf import settings
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse

from .models import Document,Courses,StudentMarks
from .forms import DocumentForm,CourseForm,StudentForm

# render to Login page
def index(request):
    return render(request, 'transcriptG/index1.html')

# render to registration page
def register(request):
	return render(request,'transcriptG/register.html')

#validating the registration Fields
def validate(request):
    First_name = request.POST.get('First_name')
    Last_name = request.POST.get('Last_name')
    EmailId = request.POST.get('EmailId')
    password = request.POST.get('password')
    userType = request.POST.get('userType')
    response = {}
    if not user.objects.filter(Email=EmailId):
        s = user(Fname=First_name,Lname = Last_name, Email = EmailId,password= password,userType=userType)
        s.save()
        # alert ("registration successfull")
        return render_to_response(
               'transcriptG/index1.html',
               # {'form': form},
               context_instance=RequestContext(request)
           )
    else:        
        response['status'] = 'failure'
    json_data = json.dumps(response)
    return HttpResponse(json_data, content_type = "application/json")
    
def homevalidate(request):
    userid = request.POST.get('id')
    paswd = request.POST.get('pswd')
    response = {}
    if user.objects.filter(Email = userid,password=paswd):
        # response
        return render_to_response(
           'transcriptG/list.html',
           # {'form': form},
           context_instance=RequestContext(request)
           )
    else:
        return render_to_response(
           'transcriptG/index1.html',
            # {'form': form},
           context_instance=RequestContext(request)
           )
    # return HttpResponse(json_data, content_type = "application/json")

# validating and storing the data of uploaded student details csv file
def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            docfile = request.FILES['docfile']
            for row in docfile:
                student = Student()
                row = row.split(",")
                student.SID = row[0]
                student.firstname = row[1]
                student.lastname = row[2]
                student.emailid = row[3]
                student.phnum = row[4]
                student.yearofjoining = row[5]
                student.yearofpassing = row[6]
                student.batchNo = row[7]
                student.save()

            # Redirect to the document list after POST
            return render_to_response(
                'transcriptG/uploadsuccess.html',
                {'form': form},
                context_instance=RequestContext(request)
            )
            # return HttpResponseRedirect(reverse('myproject.myapp.views.list'))
    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    students = Student.objects.all()

    # # Render list page with the documents and the form
    # return HttpResponse('Fialure in uploading the student details')
    return render_to_response(
        'transcriptG/list.html',
        {'documents': students, 'form': form},
        context_instance=RequestContext(request)
    )

# validating and storing the data of uploaded couerses list csv file
def courseList(request):
    # Handle file upload
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            coursefile = request.FILES['coursefile']
            for row in coursefile:
                course = Courses()
                row = row.split(",")
                course.CID = row[0]
                course.CName = row[1]
                course.year = row[2]
                course.term = row[3]
                course.credits = row[4]
                course.save()

            # Redirect to the document list after POST
            return render_to_response(
                'transcriptG/uploadsuccess.html',
                {'form': form},
                context_instance=RequestContext(request)
            )
            # return HttpResponseRedirect(reverse('myproject.myapp.views.list'))
    else:
        form = CourseForm()  # A empty, unbound form

    # Load documents for the list page
    courses = Courses.objects.all()

    # # Render list page with the documents and the form
    # return HttpResponse('Fialure in uploading the student details')
    return render_to_response(
        'transcriptG/list.html',
        {'documents': courses, 'form': form},
        context_instance=RequestContext(request)
    )

# validating and storing the data of uploaded student marks list csv file
def studentMarkslist(request):
    # Handle file upload
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            studmarksfile = request.FILES['studmarksfile']
            for row in studmarksfile:
                studmarks = StudentMarks()
                row = row.split(",")
                studmarks.SID = row[0]
                studmarks.CID = row[1]
                studmarks.grade = row[2]
                studmarks.description = row[3]
                studmarks.save()

            # Redirect to the document list after POST
            return render_to_response(
                'transcriptG/uploadsuccess.html',
                {'form': form},
                context_instance=RequestContext(request)
            )
            # return HttpResponseRedirect(reverse('myproject.myapp.views.list'))
    else:
        form = StudentForm()  # A empty, unbound form

    # Load documents for the list page
    studmarkslist = StudentMarks.objects.all()

    # # Render list page with the documents and the form
    # return HttpResponse('Fialure in uploading the student details')
    return render_to_response(
        'transcriptG/list.html',
        {'documents': studmarkslist, 'form': form},
        context_instance=RequestContext(request)
    )
