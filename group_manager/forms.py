from django import forms
from django.db.models import Q
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from . import models


class StudentGroupForm (forms.ModelForm):
    """
        Admin form for StudentGroup to include student selected
        From https://stackoverflow.com/a/8818880
    """
    class Meta:
        model = models.Student_Group
        exclude = ('teacher', 'position')

    students = forms.ModelMultipleChoiceField(
                                        queryset=models.Student.objects.all(),
                                        widget=FilteredSelectMultiple(
                                                verbose_name='Students',
                                                is_stacked=False))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.teacher = models.Teacher.objects.get(user=self.current_user)

        try:
            self.fields['number'].initial = (models.Student_Group
                                             .objects.filter(
                                                teacher=self.teacher)
                                             .order_by(
                                                '-number'))[0].number + 1
        except IndexError:
            self.fields['number'].initial = 1

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

    def clean(self):
        cleaned_data = super().clean()
        number = cleaned_data.get('number')

        if not number:
            return cleaned_data
        if self.instance:
            if models.Student_Group.objects.filter(
                teacher=self.teacher, number=number).exclude(
                    pk=self.instance.pk):
                    raise ValidationError(_(
                        "A group already exists with this number"),
                        code="unique_together")
        else:
            if (models.Student_Group.objects.filter(
                    teacher=self.teacher, number=number)):
                raise ValidationError(_(
                        "A group already exists with this number"),
                        code="unique_together")
        return cleaned_data


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


class DebateForm (forms.ModelForm):
    class Meta:
        model = models.Debate
        fields = '__all__'

    position = forms.NullBooleanField(
        widget=forms.RadioSelect(
            choices=models.Student_Group.CHOICES))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            self.fields['position'].initial = self.instance.group.position
        except models.Student_Group.DoesNotExist:
            pass

    def clean(self):
        cleaned_data = super().clean()
        schedule = cleaned_data.get("schedule")
        group = cleaned_data.get("group")
        presenting = cleaned_data.get("isPresenting")
        position = cleaned_data.get("position")
        error = []

        if self.instance:
            pk = self.instance.pk

            if presenting:
                if models.Debate.objects.filter(
                    schedule=schedule,
                        isPresenting=True).count() > 2:
                    error.append(ValidationError(_(
                        "Two group is already presenting for this schedule"),
                        code="schedule_presenting_not_unique"))
                if models.Debate.objects.filter(
                    group=group,
                        isPresenting=True).exclude(pk=pk).exists():
                    error.append(ValidationError(_(
                        "This group is already presenting"),
                        code="already_presenting"))
                if models.Debate.objects.filter(
                        schedule=schedule,
                        group__position=position).exclude(pk=pk).exists():
                    error.append(ValidationError(_(
                            "There is already a group with this position \
                            presenting for this time slot."),
                            code="position_used"))
            if models.Debate.objects.filter(
                    schedule__period=schedule.period,
                    schedule__date=schedule.date,
                    group=group).exclude(pk=pk).exists():
                error.append(ValidationError(_(
                        "This group is already assigned to attend a \
                        debate at this time"),
                        code="already_attending"))
        else:
            if presenting:
                if models.Debate.objects.filter(
                    schedule=schedule,
                        isPresenting=True).count() > 1:
                    error.append(ValidationError(_(
                            "Two group is already presenting for \
                            this schedule"),
                            code="schedule_presenting_not_unique"))
                if models.Debate.objects.filter(
                    group=group,
                        isPresenting=True).exists():
                    error.append(ValidationError(_(
                        "This group is already presenting"),
                        code="already_presenting"))
                if models.Debate.objects.filter(
                    schedule__period=schedule.period,
                    schedule__date=schedule.date,
                        group=group).exists():
                    error.append(ValidationError(_(
                            "This group is already assigned to attend a \
                            debate at this time"),
                            code="already_attending"))
                if models.Debate.objects.filter(
                    schedule=schedule,
                        group__position=position).exists():
                    error.append(ValidationError(_(
                        "There is already a group with this position \
                        presenting for this time slot."),
                        code="position_used"))
            if models.Debate.objects.filter(
                    schedule__period=schedule.period,
                    schedule__date=schedule.date,
                    group=group).exists():
                error.append(ValidationError(_(
                        "This group is already assigned to attend a \
                        debate at this time"),
                        code="already_attending"))
        if presenting:
            if cleaned_data['position'] is None:
                error.append(ValidationError(_(
                        "Position must be set if group is presenting"),
                        code="position_not_set"))
        else:
            if cleaned_data['position'] is not None:
                error.append(ValidationError(_(
                    "Position must not be set if group is not presenting"),
                    code="position_set"))

        if error:
            raise ValidationError(error)
        return cleaned_data
