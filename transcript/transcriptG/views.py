
from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from .models import user,Student
import cgi
import os
from io import BytesIO
import json
from datetime import datetime
from django.utils import timezone
from django.conf import settings
from django.template import RequestContext, loader
import reportlab
from reportlab.pdfbase import pdfmetrics  
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer  
from reportlab.lib.styles import getSampleStyleSheet  
from reportlab.rl_config import defaultPageSize
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

def Uploadd(request):
    return render(request,'transcriptG/upload.html')

#validating the registration Fields
def validate(request):
    # return HttpResponse("ssucess")
    First_name = request.GET.get('First_name')
    Last_name = request.GET.get('Last_name')
    EmailId = request.GET.get('EmailId')
    User_name = request.GET.get('User_name')
    password1 = request.GET.get('password1')
    userType = request.GET.get('userType')
    response = {}
    if not user.objects.filter(Email=EmailId):
        s = user(Fname=First_name,Lname = Last_name, Email = EmailId,password= password1,userType=userType)
        s.save()
        return render_to_response(
               '/admin',
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
           context_instance=RequestContext(request)
           )

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
                course.Courseyear=row[5]
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

def TranscriptGen(request):
    return render(request,'transcriptG/generateTranscript.html')

def handle_exception(e):
    print(e)
    print('But I can be safe!')

def calculateGPA(request):
    from reportlab.lib import colors  
    from reportlab.lib.units import inch
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
    buffer=BytesIO()
    # p= canvas.Canvas("filename.pdf")
    
    p = canvas.Canvas(buffer)
    # Create the PDF object, using the response object as its "file."

    stud_id = request.GET.get('stud_id')
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    students_ids=Student.objects.all()
    count = 0
    for st in students_ids:
        if stud_id in st.SID:
            count = count + 1
    if count > 0:
        stud_details = Student.objects.filter(SID = stud_id)
        p.setFont('Times-Bold',11)
        p.drawString(20,690,"MSIT")
        p.drawString(20,670, str(stud_details[0].yearofjoining)+"-"+str(stud_details[0].yearofpassing))
        p.drawString(20,650,"Date Of Issue:")
        today = datetime.now()
        p.drawString(20,635,str(today.strftime('%d-%B-%Y')))
        p.setFont('Times-Bold',8)
        p.drawString(20,620,"Consolidated Marks Sheet")
        p.setFont('Times-Bold',15)
        p.drawString(130,690,"Name:" )
        p.setFont('Times-Roman',12)
        p.drawString(175,690,stud_details[0].firstname+" "+stud_details[0].lastname)
        p.drawString(400,690,"Roll No: ")
        p.drawString(445, 690, stud_details[0].SID)
        p.setFont('Times-BoldItalic',13)
        p.drawString(130,670,"MASTER OF SCIENCE IN INFORMATION TECHNOLOGY")
        p.setFont('Times-Roman',12)
        p.drawString(130,650,"CGPA:")
        p.drawString(130,630,"Credits Obtained:")
        p.drawString(410,640,"PercentageRange:")
        p.drawString(350,630,"Required Credits for Completion:")
        p.setFont('Times-Bold',12)
        p.drawString(130, 600, "Code")
        p.drawString(250, 600, "Course Name")
        p.drawString(410, 600, "Grade")
        p.drawString(460, 600, "Credits")
        p.drawString(130, 580,"First Year")
        p.setFont('Times-Roman',12)
        gradeDictionary={'EX':10.0,'A+':9.5,'A':9.0,'B+':8.5,'B':8.0,'C':7.0}

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
            
            credits_details = Courses.objects.filter(CID=j.CID)

            credits = credits_details[0].credits
            
            sum_of_credits = sum_of_credits + credits
            GPA = GPA + (grade*credits)

            if credits_details[0].year == 1 and 'SS' not in credits_details[0].CID :
                p.drawString(420, (560-temp), j.grade)
                p.drawString(130, (560-temp), credits_details[0].CID)
                p.drawString(220, (560-temp), credits_details[0].CName)
                p.drawString(480, (560-temp), str(credits))
                # p.drawString(460, 650, str(credits))
                temp = temp + 15

        p.setFont('Times-Bold',12)
        p.drawString(130,(560-temp),"Second Year")
        p.setFont('Times-Roman',12)
        temp = temp + 15
        for j in grade_details:
            if j.grade == 'F':
                sum_of_credits = 0
                break

            grade = gradeDictionary[j.grade]
            
            credits_details = Courses.objects.filter(CID=j.CID)

            credits = credits_details[0].credits

            if credits_details[0].year == 2:
                p.drawString(420, (560-temp), j.grade)
                p.drawString(130, (560-temp), credits_details[0].CID)
                p.drawString(220, (560-temp), credits_details[0].CName)
                p.drawString(480, (560-temp), str(credits))
                # p.drawString(460, 650, str(credits))
                temp = temp + 15


        p.drawString(220, 630, str(sum_of_credits))
        p.drawString(515, 630, str(sum_of_credits))
        if not sum_of_credits == 0:
            CGPA = GPA/sum_of_credits
            p.drawString(170,650,str(round(CGPA,1)))
        
        # canvas.drawCentredString(2.75*inch, 2.5*inch, "Font size examples")
        if CGPA == 10.0 :
            p.drawString(500,640,"96-100") 
        if CGPA >= 9.0 and CGPA <10.0:
            p.drawString(500,640,"91-95")
        if CGPA >= 8.0 and CGPA < 9.0:
            p.drawString(500,640,"86-90")
        if CGPA >= 7.0 and CGPA < 8.0:
            p.drawString(500,640,"81-85")
        if CGPA >= 6.0 and CGPA < 7.0:
            p.drawString(500,640,"76-80")
        if CGPA >= 5.0 and CGPA < 6.0:
            p.drawString(500,640,"70-75")
        if CGPA < 5.0:
            p.drawString(500,640,"<70")

        temp = temp+80
        p.setFont('Times-Bold',11)
        p.drawString(350,560-temp,"Coordinator MSIT Division")

        temp = temp + 140
        p.setFont('Times-Roman',11)
        p.drawString(130,560-temp,"CGPA: Cumulative Grade Point Average")
        temp = temp + 15
        p.drawString(130,560-temp,"EX = 10.0; A+ = 9.5; A = 9.0; B+ = 8.5; B = 8.0; C = 7.0")

        p.showPage()

        stud_details = Student.objects.filter(SID = stud_id)
        p.setFont('Times-Bold',11)
        p.drawString(20,690,"MSIT")
        p.drawString(20,670, str(stud_details[0].yearofjoining)+"-"+str(stud_details[0].yearofpassing))
        p.drawString(20,650,"Date Of Issue:")
        today = datetime.now()
        p.drawString(20,635,str(today.strftime('%d-%B-%Y')))
        p.setFont('Times-Bold',8)
        p.drawString(20,620,"Consolidated Marks Sheet")
        p.setFont('Times-Bold',15)
        p.drawString(130,690,"Name:" )
        p.setFont('Times-Roman',12)
        p.drawString(175,690,stud_details[0].firstname+" "+stud_details[0].lastname)
        p.drawString(400,690,"Roll No: ")
        p.drawString(445, 690, stud_details[0].SID)
        p.setFont('Times-BoldItalic',13)
        p.drawString(130,670,"MASTER OF SCIENCE IN INFORMATION TECHNOLOGY")
        p.setFont('Times-Roman',12)
        p.drawString(130,650,"CGPA:")
        p.drawString(130,630,"Credits Obtained:")
        p.drawString(410,640,"PercentageRange:")
        p.drawString(350,630,"Required Credits for Completion:")
        p.setFont('Times-Bold',12)
        p.drawString(130, 600, "Code")
        p.drawString(250, 600, "Course Name")
        p.drawString(410, 600, "Grade")
        p.drawString(460, 600, "Credits")
        p.drawString(130, 580,"Soft Skills")
        p.setFont('Times-Roman',12)
        gradeDictionary={'EX':10.0,'A+':9.5,'A':9.0,'B+':8.5,'B':8.0,'C':7.0}

        grade_details= StudentMarks.objects.filter(SID = stud_details[0].SID)
        temp = 0
        for j in grade_details:
            if j.grade == 'F':
                sum_of_credits = 0
                break

            grade = gradeDictionary[j.grade]
            
            credits_details = Courses.objects.filter(CID=j.CID)

            credits = credits_details[0].credits

            if credits_details[0].year == 1 and 'SS' in credits_details[0].CID :
                p.drawString(420, (560-temp), j.grade)
                p.drawString(130, (560-temp), credits_details[0].CID)
                p.drawString(220, (560-temp), credits_details[0].CName)
                p.drawString(480, (560-temp), str(credits))
                # p.drawString(460, 650, str(credits))
                temp = temp + 15

        p.setFont('Times-Bold',12)
        p.drawString(220, 630, str(sum_of_credits))
        p.drawString(515, 630, str(sum_of_credits))
        if not sum_of_credits == 0:
            CGPA = GPA/sum_of_credits
            p.drawString(170,650,str(round(CGPA,1)))
        
        # canvas.drawCentredString(2.75*inch, 2.5*inch, "Font size examples")
        if CGPA == 10.0 :
            p.drawString(500,640,"96-100") 
        if CGPA >= 9.0 and CGPA <10.0:
            p.drawString(500,640,"91-95")
        if CGPA >= 8.0 and CGPA < 9.0:
            p.drawString(500,640,"86-90")
        if CGPA >= 7.0 and CGPA < 8.0:
            p.drawString(500,640,"81-85")
        if CGPA >= 6.0 and CGPA < 7.0:
            p.drawString(500,640,"76-80")
        if CGPA >= 5.0 and CGPA < 6.0:
            p.drawString(500,640,"70-75")
        if CGPA < 5.0:
            p.drawString(500,640,"<70")

        temp = temp+80
        p.setFont('Times-Bold',11)
        p.drawString(350,560-temp,"Coordinator MSIT Division")

        temp = temp + 250
        p.setFont('Times-Roman',11)
        p.drawString(130,560-temp,"CGPA: Cumulative Grade Point Average")
        temp = temp + 15
        p.drawString(130,560-temp,"EX = 10.0; A+ = 9.5; A = 9.0; B+ = 8.5; B = 8.0; C = 7.0")
        p.showPage()
        p.save()
        pdf= buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response
    else:
        return HttpResponse("Student id not found")