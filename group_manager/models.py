from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Student_Group (models.Model):
#   A single group of students.
#   Stduents use foreign keys to refer to group
    teacher = models.ForeignKey(User, limit_choices_to={
        'groups__name': 'teacher'
    })
    id = models.AutoField(primary_key=True)

    class Meta:
        verbose_name = "Student Group"
        verbose_name_plural = "Student Groups"

    def __str__(self):
        return "%s%i" % (self.teacher.last_name[0], self.id)


class Class (models.Model):
#   A single English class period
    ENGLISH_TYPE = 1
    IHS_TYPE = 2
    TYPE_CHOICES = (
        (ENGLISH_TYPE, 'English'),
        (IHS_TYPE, 'IHS'),
    )

    teacher = models.ForeignKey(User, limit_choices_to={
        'groups__name': 'teacher'
    })
    period = models.IntegerField()
    type = models.IntegerField(choices=TYPE_CHOICES)

    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classes"

    def __str__(self):
        return "%s's %d period %s class" % (
            self.teacher.last_name, self.period,
            'English' if self.type == self.ENGLISH_TYPE else 'IHS'
        )


class Student (models.Model):

    student_id = models.BigIntegerField()
    first_name = models.CharField(max_length=140)
    last_name = models.CharField(max_length=140)
    email = models.EmailField(unique=True)
    english_class = models.ForeignKey(Class, related_name="english_class",
                                      limit_choices_to={
                                        'type': Class.ENGLISH_TYPE
                                        })
    ihs_class = models.ForeignKey(Class, limit_choices_to={
        'type': Class.IHS_TYPE
    })
    group = models.ForeignKey(Student_Group)

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Judge (models.Model):
    student_id = models.BigIntegerField()
    first_name = models.CharField(max_length=140)
    last_name = models.CharField(max_length=140)
    email = models.EmailField(unique=True)


class Debate_Group (models.Model):
#    A debate. Main components are the two groups.
    affTeam = models.OneToOneField(Student_Group, related_name='affTeam')
    negTeam = models.OneToOneField(Student_Group, related_name='negTeam')
    title = models.CharField(max_length=140)
    time = models.DateTimeField()
    location = models.CharField(max_length=140)
    judge = models.ManyToManyField(Judge)

    class Meta:
        verbose_name = "Debate"
        verbose_name_plural = "Debates"

    def __str__(self):
        return "%s against %s. Topic is %s" % (
            self.negTeam, self.affTeam,
            self.title
        )
