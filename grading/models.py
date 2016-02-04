from django.db import models
from group_manager import models as groupModels
from .fields import IntegerRangeField


# Create your models here.

class Scoring_Sheet(models.Model):
    group = models.ForeignKey(groupModels.Student_Group)
    judge = models.ForeignKey(groupModels.Judge)

    opening = IntegerRangeField(min_value=5, max_value=10,
                                verbose_name='opening argument slide show \
                                (5-10)')
    teamArg = IntegerRangeField(min_value=5, max_value=10,
                                verbose_name='team argument (5-10)')
    crossEx = IntegerRangeField(min_value=5, max_value=10,
                                verbose_name='raw cross-examination score \
                                (5-10)')
    decorum = models.BooleanField(verbose_name='decorum penalty?')
    rebuttal = IntegerRangeField(min_value=5, max_value=10,
                                 verbose_name='raw rebuttal score (5-10)')
    time = models.BooleanField(verbose_name='time violation?')
    newArg = models.BooleanField(verbose_name='new line of argument \
                                 or substantial new evidence?')
    participation = models.BooleanField(verbose_name='participation penalty? \
                                        (not everyone spoke)')

    def total(self):
        total = self.opening + self.teamArg + self.crossEx + self.rebuttal
        total += sum([student.total() for student in
                     self.student_argument_set.all()])
        if self.decorum:
            total -= 1
        if self.time:
            total -= 1
        if self.newArg:
            total -= 1
        if self.participation:
            total -= 1
        return total

    class Meta:
        verbose_name = "Scoring Sheet"
        verbose_name_plural = "Scoring Sheets"
        unique_together = ('group', 'judge')

    def __str__(self):
        return "%s's judgement of %s" % (self.judge.first_name, self.group)


class Student_Argument(models.Model):
    student = models.ForeignKey(groupModels.Student)
    scoring = models.ForeignKey(Scoring_Sheet)

    totalTime = models.CharField(max_length=140)
    score = IntegerRangeField(min_value=5, max_value=10,
                              verbose_name='RAW individual score (5-10)')
    time = models.BooleanField(verbose_name='time violation?')

    def total(self):
        if self.time:
            return self.score - 1
        return self.score

    class Meta:
        verbose_name = "Student Argument"
        verbose_name_plural = "Student Arguments"

    def __str__(self):
        return "%s's individual score by %s" % (self.student.first_name,
                                                self.scoring.judge.first_name)


