from django.db import models

class Student(models.Model):
	SID = models.CharField(max_length = 12)
	firstname = models.CharField(max_length = 30)
	lastname = models.CharField(max_length = 30)
	emailid = models.EmailField(max_length = 400)
	phnum = models.CharField(max_length = 15)
	yearofjoining = models.IntegerField(default = 0)
	yearofpassing = models.IntegerField(default = 0)
	batchNo = models.IntegerField(default = 0)
# Create your models here
class user(models.Model):
	Fname = models.CharField(max_length=20)
	Lname = models.CharField(max_length=20)
	Email = models.EmailField(max_length=50)
	password= models.CharField(max_length=30)
	userType = models.CharField(max_length=25)
