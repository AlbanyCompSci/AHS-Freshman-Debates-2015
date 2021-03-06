from django.db import models
from group_manager import models as groupModels
from .fields import DecimalRangeField

# Create your models here.


class Scoring_Sheet(models.Model):
    group = models.ForeignKey(
        groupModels.Student_Group, on_delete=models.CASCADE)
    judge = models.CharField(max_length=140)

    opening = DecimalRangeField(
        max_digits=4,
        decimal_places=2,
        min_value=5,
        max_value=10,
        verbose_name='opening argument slide show \
                                (5-10)')
    teamArg = DecimalRangeField(
        max_digits=4,
        decimal_places=2,
        min_value=5,
        max_value=10,
        verbose_name='team argument (5-10)')
    crossEx = DecimalRangeField(
        max_digits=4,
        decimal_places=2,
        min_value=5,
        max_value=10,
        verbose_name='raw cross-examination score \
                                (5-10)')
    decorum = models.BooleanField(verbose_name='decorum penalty?')
    rebuttal = DecimalRangeField(
        max_digits=4,
        decimal_places=2,
        min_value=5,
        max_value=10,
        verbose_name='raw rebuttal score (5-10)')
    time = models.BooleanField(verbose_name='time violation?')
    newArg = models.BooleanField(verbose_name='new line of argument \
                                 or substantial new evidence?')
    participation = models.BooleanField(verbose_name='participation penalty? \
                                        (not everyone spoke)')

    def total(self):
        total = self.opening + self.teamArg + self.crossEx + self.rebuttal
        total += sum(
            [student.total() for student in self.student_argument_set.all()])
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
        return "%s's judgement of %s" % (self.judge, self.group)

    @staticmethod
    def autocomplete_search_fields():
        return ('group__teacher__initial__startswith', )


class Student_Argument(models.Model):
    student = models.CharField(max_length=140)
    scoring = models.ForeignKey(Scoring_Sheet, on_delete=models.CASCADE)

    totalTime = models.CharField(max_length=140)
    score = DecimalRangeField(
        max_digits=4,
        decimal_places=2,
        min_value=5,
        max_value=10,
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
        return "%s's individual score by %s" % (self.student,
                                                self.scoring.judge)
