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


class English_Class (models.Model):
#   A single English class period
    teacher = models.ForeignKey(User, limit_choices_to={
        'groups__name': 'teacher'
    })
    period = models.IntegerField()

    class Meta:
        verbose_name = "English Class"
        verbose_name_plural = "English Classses"

    def __str__(self):
        return "%s's %d period" % (self.teacher.last_name, self.period)


class Student (models.Model):

    first_name = models.CharField(max_length=140)
    last_name = models.CharField(max_length=140)
    email = models.EmailField()
    english_period = models.IntegerField()
    course_id = models.CharField(max_length=20)
    group = models.ForeignKey(Student_Group)

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Debate_Group (models.Model):
#    A debate. Main components are the two groups.
    affTeam = models.OneToOneField(Student_Group, related_name='affTeam')
    negTeam = models.OneToOneField(Student_Group, related_name='negTeam')
    title = models.CharField(max_length=140)
    time = models.DateTimeField()
    location = models.CharField(max_length=140)
    judge = models.ManyToManyField(User, limit_choices_to={
                                   'groups__name': 'judge'
                                   })

    class Meta:
        verbose_name = "Debate"
        verbose_name_plural = "Debates"

    def __str__(self):
        return "%s against %s. Topic is %s" % (
            self.negTeam, self.affTeam,
            self.title
        )
