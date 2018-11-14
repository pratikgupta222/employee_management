from django.contrib import admin
from employee.models import *
# Register your models here.


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'uid', 'fname', 'lname', 'phone',
                    'email', 'role')


admin.site.register(Employee, EmployeeAdmin)
