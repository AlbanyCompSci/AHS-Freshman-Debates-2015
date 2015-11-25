from django import forms
from . import models


class StudentGroupForm(forms.ModelForm):
    class Meta:
        model = models.Student_Group
        exclude = ('teacher',)

    def get_media_js(self):
        return ','.join('"%s"' % self.media.absolute_path(path) for
                        path in self.media._js)

    def __init__(self, *args, **kwargs):
        self.teacher = kwargs.pop('teacher', None)
        self.periods = kwargs.pop('periods', None)
        super().__init__(*args, **kwargs)

        self.fields['students'] = forms.ModelMultipleChoiceField(
                                queryset=models
                                .Student.objects
                                .filter(group__isnull=True)
                                .filter(english_class__teacher=self.teacher)
                                .filter(
                                    english_class__period__in=self.periods))
        if self.instance:
            self.fields['students'].initial = self.instance.student_set.all()
            self.fields['students'].widget.attrs['size'] = '40'

    def save(self, *args, **kwargs):
        instance = super().save(commit=False)
        self.fields['students'].initial.update(group=None)
        return instance
