from django.contrib import admin
from django.db.models import Q
from django import forms
from . import models
# Register your models here.


@admin.register(models.Student)
class StudentGroupAdmin (admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(Q(ihs_teacher=request.user) |
                         Q(english_teacher=request.user))


class StudentGroupForm (forms.ModelForm):
    """ From https://stackoverflow.com/a/8818880 """
    class Meta:
        model = models.Student_Group
        fields = '__all__'

    students = forms.ModelMultipleChoiceField(queryset=models.Student.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['students'].initial = self.instance.student_set.all()

    def save(self, *args, **kwargs):
        """ Previously assigned Students are silently reset """
        instance = super().save(commit=False)
        self.fields['students'].initial.update(group=None)
        self.cleaned_data['students'].update(group=instance)
        return instance


@admin.register(models.Student_Group)
class StudentGroupAdmin (admin.ModelAdmin):
    form = StudentGroupForm


admin.site.register(models.Student_Class)
admin.site.register(models.Judge)
admin.site.register(models.Debate_Group)
admin.site.register(models.Location)
admin.site.register(models.Schedule)
admin.site.register(models.Debate)
admin.site.register(models.Judge_Group)
