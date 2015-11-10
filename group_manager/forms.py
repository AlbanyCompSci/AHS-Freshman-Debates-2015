from django import forms
from . import models


class StudentGroupForm(forms.ModelForm):
    class Meta:
        model = models.Student_Group
        exclude = ('teacher',)

    students = forms.ModelMultipleChoiceField(
                                              queryset=models.Student.objects
                                              .filter(group__isnull=True))

    def __init__(self, *args, **kwargs):
        #self.user = kwargs['initial']['user']
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['students'].initial = self.instance.student_set.all()
            self.fields['students'].widget.attrs['size'] = '40'

    def save(self, *args, **kwargs):
        instance = super().save(commit=False)
        self.fields['students'].initial.update(group=None)
        return instance


    """def save(self, *args, **kwargs):
        instance = super().save(commit=False)
        instance.teacher = kwargs['user']
        self.fields['students'].initial.update(group=None)
        self.cleaned_data['students'].update(group=instance)
        return instance"""


    """def save(self, *args, **kwargs):
        instance = super().save(commit=False)
        self.fields['students'].initial.update(group=None)
        self.cleaned_data['students'].update(group=instance)
        return instance"""





    """def save(self, *args, **kwargs):
        # from: http://stackoverflow.com/a/8818880
        # 'commit' arguement not handeled
        # Previously assigned Students are silently reset
        instance = super().save(commit=False)
        #instance.teacher = kwargs['initial']['user']
        self.fields['students'].initial.update(group=None)
        self.cleaned_data['students'].update(group=instance)
        return instance"""
