from django.contrib import admin
from . import forms as forms
from . import models
# Register your models here.


class GroupMixin (object):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fieldName = name

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

    def __init__(self, *args, **kwargs):
        super().__init__('students', *args, **kwargs)

    def save_form(self, request, form, change):
        """ Set teacher to current user """
        form_uncommited = super().save_form(request, form, change)
        form_uncommited.teacher = request.user
        return form_uncommited


@admin.register(models.Judge_Group)
class JudgeGroupAdmin (GroupMixin, admin.ModelAdmin):
    form = forms.JudgeGroupForm

    def __init__(self, *args, **kwargs):
        super().__init__('judges', *args, **kwargs)


@admin.register(models.Debate_Group)
class DebateGroupAdmin (admin.ModelAdmin):
    form = forms.DebateGroupForm


@admin.register(models.Debate)
class DebateAdmin(admin.ModelAdmin):
    form = forms.DebateForm

admin.site.register(models.Student_Class)
admin.site.register(models.Student)
admin.site.register(models.Judge)
admin.site.register(models.Location)
admin.site.register(models.Schedule)
