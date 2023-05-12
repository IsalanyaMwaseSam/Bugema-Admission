from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=33)
    email = models.EmailField(max_length=33)
    phone_number = models.CharField(max_length=13)

class Qualification(models.Model):
    name = models.CharField(max_length=255)

class School(models.Model):
    name = models.CharField(max_length=255)

class Department(models.Model):
    name = models.CharField(max_length=255)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

class Programs(models.Model):
    name = models.CharField(max_length=255)
    qualification = models.ForeignKey(Qualification, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE,  null=True, blank=True)
    
class Application(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    program = models.ForeignKey(Programs, on_delete=models.CASCADE)
    document = models.FileField(upload_to='documents/')
    name = models.CharField(max_length=255, null=True)
    email = models.EmailField(max_length=255, null=True)
    phone_number = models.CharField(max_length=20, null=True)
    status = models.CharField(max_length=50, default='pending')
