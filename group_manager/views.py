from django.views import generic
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Prefetch
from django.shortcuts import render
from datetime import datetime
from itertools import groupby
import csv
from . import models
from . import forms

# Create your views here.


class StaffIndexView(generic.ListView):
    model = models.Student_Group

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(
            teacher=models.Teacher.objects.get(user=self.request.user))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dates'] = sorted(
            list(set([i.date for i in models.Schedule.objects.all()])))
        return context


class IndexView(generic.View):
    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return HttpResponseRedirect(reverse('groups:schedule'))
        if request.user.groups.filter(name='teacher').exists():
            return StaffIndexView.as_view()(request)
        if request.user.groups.filter(name='teacher assistant').exists():
            return HttpResponseRedirect(
                reverse('admin:grading_scoring_sheet_add'))


class ScheduleListView(generic.ListView):
    model = models.Schedule

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dates'] = sorted(
            list(set([i.date for i in models.Schedule.objects.all()])))
        return context


class StudentGroupDetailView(generic.DetailView):
    model = models.Student_Group

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            context['debate'] = self.object.debate_set.get(isPresenting=True)
        except models.Debate.DoesNotExist:
            context['debate'] = None
        try:
            context['opposition'] = models.Debate.objects.filter(
                schedule=context['debate'].schedule,
                isPresenting=True).exclude(group=self.object).first()
        except (models.Debate.DoesNotExist, AttributeError):
            context['opposition'] = None

        return context


class ScheduleDetailView(generic.DetailView):
    model = models.Schedule

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['aff'] = self.object.debate_set.get(
                isPresenting=True, group__position=True).group
        except models.Debate.DoesNotExist:
            context['aff'] = None
        try:
            context['neg'] = self.object.debate_set.get(
                isPresenting=True, group__position=False).group
        except models.Debate.DoesNotExist:
            context['neg'] = None

        groupsWatching = list()
        for debate in self.object.debate_set.filter(isPresenting=False):
            try:
                groupsWatching.append([
                    debate.group,
                    models.Debate.objects.get(group=debate.group,
                                              isPresenting=True).schedule.pk
                ])
            except models.Debate.DoesNotExist:
                groupsWatching.append([debate.group, float('nan')])

        groupsWatching.sort(key=lambda x: x[1])
        context['watching'] = list()
        for k, g in groupby(groupsWatching, lambda x: x[1]):
            context['watching'].append([i[0] for i in g])

        return context


class StudentDetailView(generic.DetailView):
    model = models.Student

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['debate'] = self.object.group.debate_set.get(
                isPresenting=True)
        except (models.Student_Group.DoesNotExist, models.Debate.DoesNotExist):
            context['debate'] = None

        try:
            context['opposition'] = models.Debate.objects.filter(
                schedule=context['debate'].schedule,
                isPresenting=True).exclude(pk=context['debate'].pk).first()
        except (models.Debate.DoesNotExist, AttributeError):
            context['opposition'] = None
        return context


class AZListDate(generic.ListView):
    model = models.Student
    template_name = 'group_manager/AZList_date.html'

    def get_queryset(self):
        qs = self.model.objects.exclude(group=None)
        qs = qs.select_related('group__teacher')

        for period in range(1, 8):
            qs = qs.prefetch_related(
                Prefetch(
                    'group__debate_set',
                    queryset=models.Debate.objects.filter(
                        schedule__period=period),
                    to_attr='p%d' % period),
                'group__p%d__schedule__location' % period)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dates'] = context['dates'] = sorted(
            list(set([i.date for i in models.Schedule.objects.all()])))

        return context


class AZListGroup(generic.ListView):
    model = models.Student
    template_name = 'group_manager/AZList_group.html'

    def get_queryset(self):
        qs = self.model.objects.select_related('group__teacher').order_by(
            'group__teacher', 'group__number')

        for period in range(1, 8):
            qs = qs.prefetch_related(
                Prefetch(
                    'group__debate_set',
                    queryset=models.Debate.objects.filter(
                        schedule__period=period,
                        schedule__date=self.kwargs['date']),
                    to_attr='p%d' % period),
                'group__p%d__schedule__location' % period)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dates'] = sorted(
            list(
                set([
                    i.date for i in models.Schedule.objects.all()
                    if str(i.date) != self.kwargs['date']
                ])))
        context['dat'] = datetime.strptime(self.kwargs['date'],
                                           "%Y-%m-%d").strftime("%A")
        context['datdate'] = self.kwargs['date']
        return context


class AzCsvDateView(generic.View):
    def get(self, request, *args, **kwargs):
        # header
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; \
        filename="AZList by group.csv"'

        # get data
        qs = models.Student.objects.exclude(group=None)
        for period in range(1, 8):
            qs = qs.prefetch_related(
                Prefetch(
                    'group__debate_set',
                    queryset=models.Debate.objects.filter(
                        schedule__period=period),
                    to_attr='p%d' % period),
                'group__p%d__schedule__location' % period)

        # write data
        writer = csv.writer(response)
        writer.writerow([
            'name', 'team', 'date', 'period 1', 'period 2', 'period 3',
            'period 4', 'period 5', 'period 6', 'period 7'
        ])

        for student in qs:
            try:
                writer.writerow([
                    student.__str__(), student.group.__str__(),
                    student.group.p1[0].schedule.date.strftime('%A'),
                    student.group.p1[0].schedule.location.__str__(),
                    student.group.p2[0].schedule.location.__str__(),
                    student.group.p3[0].schedule.location.__str__(),
                    student.group.p4[0].schedule.location.__str__(),
                    student.group.p5[0].schedule.location.__str__(),
                    student.group.p6[0].schedule.location.__str__(),
                    student.group.p7[0].schedule.location.__str__()
                ])
            except IndexError:
                pass

        return response


class AzCsvGroupView(generic.View):
    def get(self, request, *args, **kwargs):
        # header
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; \
        filename="%s.csv"' % kwargs['date']

        # get data
        qs = models.Student.objects.exclude(group=None).order_by(
            'group__teacher', 'group__number')
        for period in range(1, 8):
            qs = qs.prefetch_related(
                Prefetch(
                    'group__debate_set',
                    queryset=models.Debate.objects.filter(
                        schedule__period=period,
                        schedule__date=kwargs['date']),
                    to_attr='p%d' % period),
                'group__p%d__schedule__location' % period)

        # write data
        writer = csv.writer(response)
        writer.writerow([
            'name', 'team', 'period 1', 'period 2', 'period 3', 'period 4',
            'period 5', 'period 6', 'period 7'
        ])
        for student in qs:
            if len(student.group.p2) == 0: continue
            writer.writerow([
                student.__str__(), student.group.__str__(),
                student.group.p1[0].schedule.location.__str__()
                if len(student.group.p1) == 1 else "None",
                student.group.p2[0].schedule.location.__str__()
                if len(student.group.p2) == 1 else "None",
                student.group.p3[0].schedule.location.__str__()
                if len(student.group.p3) == 1 else "None",
                student.group.p4[0].schedule.location.__str__()
                if len(student.group.p4) == 1 else "None",
                student.group.p5[0].schedule.location.__str__()
                if len(student.group.p5) == 1 else "None",
                student.group.p6[0].schedule.location.__str__()
                if len(student.group.p6) == 1 else "None",
                student.group.p7[0].schedule.location.__str__()
                if len(student.group.p7) == 1 else "None"
            ])
        return response


class StudentDataImportView(generic.View):
    def post(self, request, *args, **kwargs):
        form = forms.StudentDataImportForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse("admin:group_manager_student_changelist"))

    def get(self, request, *args, **kwargs):
        form = forms.StudentDataImportForm()
        context = {"form": form}
        return render(request, "group_manager/student_data_import.html",
                      context)


class StudentGroupMassSetDebate(generic.View):
    def post(self, request, *args, **kwargs):
        form = forms.StudentGroupMassSetDebateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("groups:index"))

    def get(self, request, *args, **kwargs):
        form = forms.StudentGroupMassSetDebateForm()
        context = {"form": form}
        return render(request, "group_manager/debate_mass_create.html",
                      context)
