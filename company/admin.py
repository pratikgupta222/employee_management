from django.contrib import admin
from company.models import *
# Register your models here.


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'emp_prefix')


admin.site.register(Company, CompanyAdmin)
