from django.contrib import admin

from .models import *
# Register your models here.


class StudentInline(admin.TabularInline):
#   Stacked Inline View for Student
    model = Student
    min_num = 2
    max_num = 20
    extra = 3


class GroupAdmin (admin.ModelAdmin):
    fields = ['teacher']
    inlines = [StudentInline]

admin.site.register(Student_Group, GroupAdmin)
admin.site.register(Class)
admin.site.register(Debate_Group)
