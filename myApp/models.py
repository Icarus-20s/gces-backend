from django.db import models
from django.db import models
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
class Branch(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self) -> str:
        return self.name

class CustomUser(models.Model):
    ROLE_CHOICES=(
        ("teacher","teacher"),
        ("student","student"),
        ("staff","staff"),
    )
    email = models.EmailField(unique=True)
    username= models.CharField(max_length=100,unique=True)
    first_name=models.CharField(max_length=100,blank=True)
    last_name =models.CharField(max_length=100,blank=True)
    password =models.CharField(max_length=100)
    branch=models.ForeignKey(Branch ,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=100 ,choices=ROLE_CHOICES)

    def save(self,*args,**kwargs):
        if self.password:
            self.password=make_password(self.password,hasher='bcrypt')
        super().save(*args,**kwargs)

    def __str__(self):
        return self.username

class Session(models.Model):
    branch=models.ForeignKey(Branch ,on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

class Notice (models.Model):
    branch= models.ForeignKey(Branch , on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content= models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

    
class StaffSalary(models.Model):
    staff = models.ForeignKey(CustomUser , on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10 , decimal_places=2)
    month =models.DateField()
    def clean(self) -> None:
        staff = getattr(self,'staff', None)
        if not staff:
            return
        if staff.role!="staff":
            raise ValidationError("User must be staff.")
        return super().clean()

#---------------------------------------------------------------------

class Assignment(models.Model):
    teacher = models.ForeignKey(CustomUser , on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    deadline = models.DateField()


class AssignmentSubmission(models.Model):
    assignment= models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student= models.ForeignKey(CustomUser ,on_delete=models.CASCADE)
    text_submission= models.TextField(blank=True ,null=True)
    file_submission=models.FileField(upload_to='assignment_submissions',blank=True, null=True)
    submission_date = models.DateTimeField(auto_now_add=True)

class Note(models.Model):
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text_content = models.TextField(blank=True , null=True)
    file_content = models.FileField(upload_to="notes")
    date_created = models.DateTimeField(auto_now_add=True)

class TeacherAttendance(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    date = models.DateField()
    is_present = models.BooleanField()

class StudentAttendance(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    date = models.DateField()
    is_present = models.BooleanField()

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email= models.EmailField()
    message=models.TextField()

    def __str__(self):
        return self.name
