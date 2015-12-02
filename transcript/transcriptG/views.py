
from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from .models import user,Student
import cgi
import os
import json
from django.utils import timezone
from django.conf import settings
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from reportlab.pdfgen import canvas

from .models import Document,Courses,StudentMarks
from .forms import DocumentForm,CourseForm,StudentForm

# render to Login page
def index(request):
    return render(request, 'transcriptG/index.html')

# render to registration page
def register(request):
	return render(request,'transcriptG/register.html')

def Doc(request):
    return render(request,'transcriptG/DocUpload.html')

def Marks(request):
    return render(request,'transcriptG/StudentMarksUpload.html')

def Course(request):
    return render(request,'transcriptG/CoursesUpload.html')

def Uploadd(request):
    return render(request,'transcriptG/upload.html')


#validating the registration Fields
def validate(request):
    First_name = request.GET.get('First_name')
    Last_name = request.GET.get('Last_name')
    EmailId = request.GET.get('EmailId')
    password1 = request.GET.get('password1')
    userType = request.GET.get('userType')
    response = {}
    if not user.objects.filter(Email=EmailId):
        s = user(Fname=First_name,Lname = Last_name, Email = EmailId,password= password1,userType=userType)
        s.save()
        # alert ("registration successfull")
        return render_to_response(
               'transcriptG/index.html',
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
    if not user.objects.filter(Email = userid,password=paswd,user='admin'):
        # response
        return render_to_response(
           '/admin',
           # {'form': form},
           context_instance=RequestContext(request)
           )
    else:
        return render_to_response(
           'transcriptG/index.html',
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
        'transcriptG/DocUpload.html',
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
        'transcriptG/CoursesUpload.html',
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
        'transcriptG/StudentMarksUpload.html',
        {'documents': studmarkslist, 'form': form},
        context_instance=RequestContext(request)
    )

def BulkTG(request):

    return render(request,'transcriptG/selectYear.html')

# def admin2(request):
#     return render_to_response('.\transcript\templates\admin\index.html',)

def calculateGPA(request):

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
    p = canvas.Canvas(response)

    # Create the PDF object, using the response object as its "file."

    stud_id = request.GET.get('stud_id')
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    
    stud_details = Student.objects.filter(SID = stud_id)
    p.drawString(20,700,"MSIT")
    p.drawString(20,680, str(stud_details[0].yearofjoining)+"-"+str(stud_details[0].yearofpassing))
    p.drawString(20,660,"Date Of Issue:")
    p.drawString(20,640,str(timezone.datetime.now().date()))
    p.drawString(20,610,"Consolidated Marks Sheet")
    p.drawString(130,700,"Name:")
    p.drawString(170,700,stud_details[0].firstname+" "+stud_details[0].lastname)
    p.drawString(400,700,"Roll No:")
    p.drawString(440, 700, stud_details[0].SID)
    p.drawString(130,670,"MASTER OF SCIENCE IN INFORMATION TECHNOLOGY")
    p.drawString(130,650,"CGPA:")

    p.drawString(130,630,"Credits Obtained:")
    p.drawString(410,650,"PercentageRange:")
    p.drawString(350,630,"Required Credits for Completion:")
    p.drawString(130, 580, "Code")
    p.drawString(250, 580, "Course Name")
    p.drawString(410, 580, "Grade")
    p.drawString(460, 580, "Credits")
        
    array = []
    gradeDictionary={'EX':10.0,'A+':9.5,'A':9.0,'B+':8.5,'B':8.0,'C':7.0}

    # for i in stud_details:
    grade_details= StudentMarks.objects.filter(SID = stud_details[0].SID)
    GPA = 0
    CGPA = 0
    sum_of_credits = 0
    temp = 0
    for j in grade_details:
        if j.grade == 'F':
            sum_of_credits = 0
            break

        grade = gradeDictionary[j.grade]

        p.drawString(420, (560-temp), j.grade)
        credits_details = Courses.objects.filter(CID=j.CID)

        p.drawString(130, (560-temp), credits_details[0].CID)
        p.drawString(220, (560-temp), credits_details[0].CName)
        # p.drawString(460, 650, str(credits))
        credits = credits_details[0].credits
        p.drawString(480, (560-temp), str(credits))
        sum_of_credits = sum_of_credits + credits
        GPA = GPA + (grade*credits)
        temp = temp + 20

    p.drawString(225, 630, str(sum_of_credits))
    p.drawString(535, 630, str(sum_of_credits))
    if not sum_of_credits == 0:
        CGPA = GPA/sum_of_credits
        array.append(CGPA)
        p.drawString(170,650,str(CGPA))
    
    if CGPA == 10.0 :
        p.drawString(515,650,"96-100") 
    if CGPA >= 9.0 and CGPA <10.0:
        p.drawString(515,650,"91-95")
    if CGPA >= 8.0 and CGPA < 9.0:
        p.drawString(515,650,"86-90")
    if CGPA >= 7.0 and CGPA < 8.0:
        p.drawString(515,650,"81-85")
    if CGPA >= 6.0 and CGPA < 7.0:
        p.drawString(515,650,"76-80")
    if CGPA >= 5.0 and CGPA < 6.0:
        p.drawString(515,650,"70-75")
    if CGPA < 5.0:
        p.drawString(515,650,"<70")
    # p.drawString(460, 670, "Credits")    
    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response
    # template = loader.get_template('transcriptG/retrieval.html')
    # context = RequestContext(request, {
    # 'details': array
    # })
    # return HttpResponse(template.render(context))
def pdf_gen(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
    p = canvas.Canvas(response)
    p.drawString(20,700,"MSIT")
    # p.drawString(20,680, str(stud_details[0].yearofjoining)+"-"+str(stud_details[0].yearofpassing))
    p.drawString(20,660,"Date Of Issue:")
    p.drawString(20,620,"CMS")
    p.drawString(130,700,"Name:")
    p.drawString(400,700,"Roll No:")
    p.drawString(130,670,"MASTER OF SCIENCE IN INFORMATION TECHNOLOGY")
    p.drawString(130,650,"CGPA:")
    p.drawString(130,630,"Credits Obtained:")
    p.drawString(410,650,"PercentageRange:")
    p.drawString(350,630,"Required Credits for Completion:")
    p.drawString(130, 590, "Code")
    p.drawString(250, 590, "Course Name")
    p.drawString(410, 590, "Grade")
    p.drawString(460, 590, "Credits")



    p.showPage()
    p.save()
    return response