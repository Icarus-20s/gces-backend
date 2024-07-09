from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Branch, Contact,Session,Notice, StaffSalary,CustomUser
from .models import Assignment, AssignmentSubmission, Note, TeacherAttendance, StudentAttendance

admin.site.register(Branch)
admin.site.register(Contact)
admin.site.register(CustomUser)
admin.site.register(Session)
admin.site.register(Notice)
admin.site.register(StaffSalary)
admin.site.register(Assignment)
admin.site.register(AssignmentSubmission)
admin.site.register(Note)
admin.site.register(TeacherAttendance)
admin.site.register(StudentAttendance)
