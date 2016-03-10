from django.views import generic
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from itertools import groupby
from django.db.models import Prefetch
from datetime import datetime
from . import models

# Create your views here.


class StaffIndexView (generic.ListView):
    model = models.Student_Group

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(teacher=models.Teacher.objects.get(user=self.request.user))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dates'] = sorted(list(set([
                i.date for i in models.Schedule.objects.all()])))
        return context


class IndexView (generic.View):
    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return HttpResponseRedirect(reverse('groups:schedule'))
        if request.user.groups.filter(name='teacher').exists():
            return StaffIndexView.as_view()(request)
        if request.user.groups.filter(name='teacher assistant').exists():
            return HttpResponseRedirect(
                reverse('admin:grading_scoring_sheet_add'))


class ScheduleListView (generic.ListView):
    model = models.Schedule

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dates'] = sorted(list(set([
                i.date for i in models.Schedule.objects.all()])))
        return context


class StudentGroupDetailView (generic.DetailView):
    model = models.Student_Group

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            context['debate'] = self.object.debate_set.get(
                isPresenting=True)
        except models.Debate.DoesNotExist:
            context['debate'] = None
        try:
            context['opposition'] = models.Debate.objects.filter(
                schedule=context['debate'].schedule,
                isPresenting=True).exclude(group=self.object).first()
        except (models.Debate.DoesNotExist, AttributeError):
            context['opposition'] = None

        return context


class ScheduleDetailView (generic.DetailView):
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
                groupsWatching.append([debate.group,
                                      models.Debate.objects.get(
                                        group=debate.group,
                                        isPresenting=True).schedule.pk])
            except models.Debate.DoesNotExist:
                groupsWatching.append([debate.group, float('nan')])

        groupsWatching.sort(key=lambda x: x[1])
        context['watching'] = list()
        for k, g in groupby(groupsWatching, lambda x: x[1]):
            context['watching'].append([i[0] for i in g])

        return context


class StudentDetailView (generic.DetailView):
    model = models.Student

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['debate'] = self.object.group.debate_set.get(
                isPresenting=True)
        except (models.Student_Group.DoesNotExist,
                models.Debate.DoesNotExist):
            context['debate'] = None

        try:
            context['opposition'] = models.Debate.objects.filter(
                schedule=context['debate'].schedule,
                isPresenting=True).exclude(pk=context['debate'].pk).first()
        except (models.Debate.DoesNotExist, AttributeError):
            context['opposition'] = None
        return context


class AZListDate (generic.ListView):
    model = models.Student
    template_name = 'group_manager/AZList_date.html'

    def get_queryset(self):
        qs = self.model.objects.select_related('group__teacher')

        for period in range(1, 8):
            qs = qs.prefetch_related(Prefetch(
                'group__debate_set',
                queryset=models.Debate.objects.filter(
                    schedule__period=period).order_by('schedule__date'),
                to_attr='p%d' % period),
                    'group__p%d__schedule__location' % period)




        """for numDate, date in enumerate(sorted(list(set([
            i.date for i in models.Schedule.objects.all()])))):
                qs = qs.prefetch_related(Prefetch(
                    'group__debate_set',
                    queryset=models.Debate.objects.filter(
                        schedule__date=date).order_by('schedule__period'),
                    to_attr='d%d' % numDate),
                        'group__d%d__schedule__location' % numDate)"""

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dates'] = context['dates'] = sorted(list(set([
                i.date for i in models.Schedule.objects.all()])))
        context['numdates'] = range(len((context['dates'])))

        return context









    """def get_queryset(self):
        qs = self.model.objects.select_related('group__teacher')

        for i in range(1, 8):
            qs = qs.prefetch_related(Prefetch(
                'group__debate_set',
                queryset=models.Debate.objects.filter(
                    schedule__period=i,
                    schedule__date=self.kwargs['date']),
                to_attr='p%d' % i),
                    'group__p%d__schedule__location' % i)
        return qs"""

    """def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dates'] = sorted(list(set([
                i.date for i in models.Schedule.objects.all()
                if str(i.date) != self.kwargs['date']])))
        context['dat'] = datetime.strptime(self.kwargs['date'], "%Y-%m-%d").strftime("%A")
        return context"""
