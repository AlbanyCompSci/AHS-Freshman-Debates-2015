from django.contrib import admin

from . import models
# Register your models here.


class StudentInline(admin.TabularInline):
    """Stacked Inline View for Student"""
    model = models.Student
    min_num = 2
    max_num = 20
    extra = 3


class GroupAdmin (admin.ModelAdmin):
    fields = ['teacher']
    inlines = [StudentInline]

admin.site.register(models.Student_Group, GroupAdmin)
admin.site.register(models.Student_Class)
admin.site.register(models.Debate_Group)
