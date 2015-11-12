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
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['students'].initial = self.instance.student_set.all()
            self.fields['students'].widget.attrs['size'] = '40'

    def save(self, *args, **kwargs):
        instance = super().save(commit=False)
        self.fields['students'].initial.update(group=None)
        return instance
