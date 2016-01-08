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
class DebateAdmin(admin.ModelAdmin):
    form = forms.DebateForm

    def save_related(self, request, form, formsets, change):
        form.cleaned_data['group'].position = form.cleaned_data['position']
        form.cleaned_data['group'].save()

admin.site.register(models.Student_Class)
admin.site.register(models.Student)
admin.site.register(models.Judge)
admin.site.register(models.Location)
admin.site.register(models.Schedule)
admin.site.register(models.Topic)
