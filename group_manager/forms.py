from django import forms
from . import models
from django.db.models import Q
from django.contrib.admin.widgets import FilteredSelectMultiple


class StudentGroupForm (forms.ModelForm):
    """
        Admin form for StudentGroup to include student selected
        From https://stackoverflow.com/a/8818880
    """
    class Meta:
        model = models.Student_Group
        exclude = ('teacher',)

    students = forms.ModelMultipleChoiceField(
                                        queryset=models.Student.objects.all(),
                                        widget=FilteredSelectMultiple(
                                                verbose_name='Students',
                                                is_stacked=False))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # For change. Includes already selected students
        if self.instance:
            self.fields['students'].queryset = models.Student.objects.filter(
                            (Q(group__isnull=True) &
                                Q(english_class__teacher=self.current_user)) |
                            Q(group=self.instance))
            self.fields['students'].initial = self.instance.student_set.all()
        else:
            self.fields['students'].queryset = models.Student.objects.filter(
                        group__isnull=True,
                        english_class__teacher=self.current_user)


class JudgeGroupForm (forms.ModelForm):
    class Meta:
        model = models.Judge_Group
        fields = '__all__'

    judges = forms.ModelMultipleChoiceField(
        queryset=models.Judge.objects.all(),
        widget=FilteredSelectMultiple(
                    verbose_name='Judges',
                    is_stacked=False))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # For change, includes already selected judges
        if self.instance:
            self.fields['judges'].queryset = models.Judge.objects.filter(
                            Q(group__isnull=True) | Q(group=self.instance))
            self.fields['judges'].initial = self.instance.judge_set.all()
        else:
            # For creation
            self.fields['students'].queryset = models.Judge.objects.filter(
                    group__isnull=True)


class DebateGroupForm (forms.ModelForm):
    class Meta:
        model = models.Debate_Group
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance:
            self.fields['affTeam'].queryset = models.Student_Group.objects.filter(
                    (Q(affTeam__isnull=True) & Q(negTeam__isnull=True)) |
                    Q(affTeam=self.instance))
            self.fields['negTeam'].queryset = models.Student_Group.objects.filter(
                    (Q(affTeam__isnull=True) & Q(negTeam__isnull=True)) |
                    Q(negTeam=self.instance))
