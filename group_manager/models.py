from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from datetime import datetime


# Create your models here.

class Student_Group (models.Model):
    """A single group of students.
    Stduents use foreign keys to refer to group"""
    CHOICES = (
        (None, "---"),
        (True, "Affirmative"),
        (False, "Negative")
    )

    teacher = models.ForeignKey(User, limit_choices_to={
                'groups__name': 'teacher'})
    number = models.IntegerField()
    position = models.NullBooleanField(choices=CHOICES)

    def get_success_url(self):
        return reverse('groups:GroupDetailView', kwargs={'pk': self.pk})

    def get_absolute_url(self):
        return reverse('groups:index')

    class Meta:
        verbose_name = "Student Group"
        verbose_name_plural = "Student Groups"
        unique_together = ('teacher', 'number')

    def __str__(self):
        return "%s%i" % (self.teacher.last_name[0], self.number)


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
    period = models.IntegerField(choices=tuple(zip(
                                 range(1, 8),
                                 (str(i) for i in range(1, 8)))))
    type = models.IntegerField(choices=TYPE_CHOICES)

    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classes"
        ordering = ['teacher', 'period']
        unique_together = ('teacher', 'period')

    def __str__(self):
        return "%s's %d period %s class" % (
            self.teacher.last_name, self.period,
            'English' if self.type == self.ENGLISH_TYPE else 'IHS'
        )


class Judge_Group (models.Model):
    class Meta:
        verbose_name = "Judge Group"
        verbose_name_plural = "Judge Groups"

    def __str__(self):
        return "%s" % ', '.join([str(i) for i in self.judge_set.all()])


class Student (models.Model):

    student_id = models.BigIntegerField(primary_key=True, unique=True)
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
    group = models.ForeignKey(Student_Group, null=True, blank=True,
                              on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return "%s, %s" % (self.last_name, self.first_name)


class Judge (models.Model):
    student_id = models.BigIntegerField(primary_key=True, unique=True)
    first_name = models.CharField(max_length=140)
    last_name = models.CharField(max_length=140)
    email = models.EmailField(unique=True)
    group = models.ForeignKey(Judge_Group, null=True, blank=True,
                              on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Judge"
        verbose_name_plural = "Judges"
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return "%s, %s" % (self.last_name, self.first_name)


class Location (models.Model):
    location = models.CharField(max_length=140, unique=True)

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"

    def __str__(self):
        return self.location


class Debate_Group (models.Model):
    # A debate. Main components are the two groups.
    affTeam = models.OneToOneField(Student_Group, related_name='affTeam',
                                   verbose_name="Affirmative Team")
    negTeam = models.OneToOneField(Student_Group, related_name='negTeam',
                                   verbose_name="Negative Team")
    title = models.CharField(max_length=140, verbose_name="topic")

    class Meta:
        verbose_name = "Debate Group"
        verbose_name_plural = "Debate Groups"

    def get_absolute_url(self):
        return reverse('groups:debate_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return "%s against %s. Topic is %s" % (
            self.negTeam, self.affTeam,
            self.title
        )


class Topic (models.Model):
    topic = models.CharField(max_length=500, unique=True)
    detail = models.TextField()

    class Meta:
        verbose_name = "Topic"
        verbose_name_plural = "Topics"

    def __str__(self):
        return self.topic


class Schedule (models.Model):
    period = models.IntegerField(choices=tuple(zip(
                                 range(1, 8),
                                 (str(i) for i in range(1, 8)))))
    location = models.ForeignKey(Location)
    date = models.DateField()
    judge_group = models.ForeignKey(Judge_Group, null=True, blank=True)
    topic = models.ForeignKey(Topic, null=True, blank=True)

    class Meta:
        verbose_name = "Schedule"
        verbose_name_plural = "Schedules"
        unique_together = (('period', 'location', 'date'),
                           ('period', 'date', 'judge_group'))
        ordering = ['date', 'period']

    def __str__(self):
        return "%s, period %s, %s" % (
                datetime.strftime(self.date, '%A'),
                self.period,
                self.location)


class Debate (models.Model):
    schedule = models.ForeignKey(Schedule)
    group = models.ForeignKey(Student_Group)
    isPresenting = models.BooleanField(verbose_name='group presenting')

    class Meta:
        verbose_name = "Debate"
        verbose_name_plural = "Debates"

    def __str__(self):
        return "%s in %s at %s period %s and %s presenting" % (
                self.group,
                self. schedule.location,
                self.schedule.date,
                self.schedule.period,
                "are" if self.isPresenting else "are not")
