from django.contrib import admin
from . import forms
from . import models
# Register your models here.


@admin.register(models.Student_Group)
class StudentGroupAdmin (admin.ModelAdmin):
    form = forms.StudentGroupForm

    def get_form(self, request, obj=None, **kwargs):
        """ Returns form with current user passed """
        form = super().get_form(request, obj, **kwargs)
        form.current_user = request.user
        return form

    def save_form(self, request, form, change):
        """
            Resets all inital students (in case some were removed)
            Sets teacher to current user
        """
        form_uncommited = form.save(commit=False)
        form_uncommited.teacher = request.user
        form.fields['students'].initial.update(group=None)
        return form_uncommited

    def save_related(self, request, form, formsets, change):
        """ Sets selected students' groups to this group """
        super()
        form.cleaned_data['students'].update(group=form.instance)

admin.site.register(models.Student_Class)
admin.site.register(models.Student)
admin.site.register(models.Judge)
admin.site.register(models.Debate_Group)
admin.site.register(models.Location)
admin.site.register(models.Schedule)
admin.site.register(models.Debate)
admin.site.register(models.Judge_Group)
