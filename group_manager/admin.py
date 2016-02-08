from django.contrib import admin
from . import forms as forms
from . import models
# Register your models here.


class GroupMixin (object):
    fieldName = None

    def get_form(self, request, obj=None, **kwargs):
        """ Returns form with current user passed in """
        form = super().get_form(request, obj, **kwargs)
        form.current_user = request.user
        return form

    def save_related(self, request, form, formsets, change):
        super()
        form.fields[self.fieldName].initial.update(group=None)
        form.cleaned_data[self.fieldName].update(group=form.instance)


@admin.register(models.Student_Group)
class StudentGroupAdmin (GroupMixin, admin.ModelAdmin):
    form = forms.StudentGroupForm
    fieldName = 'students'
    list_display = ('teacher', 'number', 'position')
    list_filter = ('teacher',)

    def save_form(self, request, form, change):
        """ Set teacher to current user """
        form_uncommited = super().save_form(request, form, change)
        form_uncommited.teacher = request.user
        return form_uncommited


@admin.register(models.Judge_Group)
class JudgeGroupAdmin (GroupMixin, admin.ModelAdmin):
    form = forms.JudgeGroupForm
    fieldName = 'judges'


@admin.register(models.Debate)
class DebateAdmin (admin.ModelAdmin):
    form = forms.DebateForm
    list_display = ('group', 'isPresenting', 'schedule')
    list_filter = ('isPresenting', 'group__position',
                   'schedule__topic', 'group')

    def save_related(self, request, form, formsets, change):
        form.cleaned_data['group'].position = form.cleaned_data['position']
        form.cleaned_data['group'].save()


@admin.register(models.Student)
class StudentAdmin (admin.ModelAdmin):
    search_fields = ['^first_name', '^last_name']
    list_display = ('last_name', 'first_name', 'english_class', 'group')
    list_filter = ('english_class__teacher',)


@admin.register(models.Student_Class)
class StudentClassAdmin (admin.ModelAdmin):
    list_display = ('teacher', 'period', 'type')
    list_filter = ('teacher', 'type')


@admin.register(models.Judge)
class JudgeAdmin (admin.ModelAdmin):
    search_fields = ['^first_name', '^last_name']
    list_display = ('last_name', 'first_name')


@admin.register(models.Schedule)
class ScheduleAdmin (admin.ModelAdmin):
    list_display = ('date', 'period', 'location', 'topic')
    list_filter = ('period', 'location', 'topic')


admin.site.register(models.Location)
admin.site.register(models.Topic)
