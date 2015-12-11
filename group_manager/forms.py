from django import forms
from . import models


class StudentGroupForm (forms.ModelForm):
    """ From https://stackoverflow.com/a/8818880 """
    class Meta:
        model = models.Student_Group
        fields = '__all__'

    students = forms.ModelMultipleChoiceField(
                                        queryset=models.Student.objects.all())

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
