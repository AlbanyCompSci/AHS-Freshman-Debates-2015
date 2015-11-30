from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


# Create your models here.

class Student_Group (models.Model):
    """A single group of students.
    Stduents use foreign keys to refer to group"""
    teacher = models.ForeignKey(User, limit_choices_to={
        'groups__name': 'teacher'
    })

    def get_success_url(self):
        return reverse('GroupDetailView', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = "Student Group"
        verbose_name_plural = "Student Groups"

    def __str__(self):
        return "%s%i" % (self.teacher.last_name[0],
                         list(Student_Group.objects
                              .filter(teacher=self.teacher).order_by('pk'))
                         .index(self) + 1
                         )


class Student_Class (models.Model):
    """A single English class period"""
    ENGLISH_TYPE = 0
    IHS_TYPE = 1

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
        ordering = ['teacher', 'period']

    def __str__(self):
        return "%s's %d period %s class" % (
            self.teacher.last_name, self.period,
            'English' if self.type == self.ENGLISH_TYPE else 'IHS'
        )


class Student (models.Model):

    student_id = models.BigIntegerField(primary_key=True)
    first_name = models.CharField(max_length=140)
    last_name = models.CharField(max_length=140)
    email = models.EmailField(unique=True)
    english_class = models.ForeignKey(Student_Class,
                                      related_name="english_class",
                                      limit_choices_to={
                                        'type': Student_Class.ENGLISH_TYPE
                                        }, null=True, blank=True)
    ihs_class = models.ForeignKey(Student_Class, limit_choices_to={
        'type': Student_Class.IHS_TYPE
    }, null=True, blank=True)
    group = models.ForeignKey(Student_Group, null=True, blank=True)

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
        ordering = ['english_class', 'last_name', 'first_name']

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Judge (models.Model):
    student_id = models.BigIntegerField(primary_key=True)
    first_name = models.CharField(max_length=140)
    last_name = models.CharField(max_length=140)
    email = models.EmailField(unique=True)

    class Meta:
        verbose_name = "Judge"
        verbose_name_plural = "Judges"
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Debate_Group (models.Model):
    """A debate. Main components are the two groups."""
    affTeam = models.OneToOneField(Student_Group, related_name='affTeam',
                                   limit_choices_to={'negTeam__isnull': True,
                                   'affTeam__isnull': True})
    negTeam = models.OneToOneField(Student_Group, related_name='negTeam',
                                   limit_choices_to={'affTeam__isnull': True,
                                        'negTeam__isnull': True})
    title = models.CharField(max_length=140)
    time = models.DateTimeField()
    location = models.CharField(max_length=140)
    judge = models.ManyToManyField(Judge)

    class Meta:
        verbose_name = "Debate"
        verbose_name_plural = "Debates"

    def get_absolute_url(self):
        return reverse('groups:debate_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return "%s against %s. Topic is %s" % (
            self.negTeam, self.affTeam,
            self.title
        )
