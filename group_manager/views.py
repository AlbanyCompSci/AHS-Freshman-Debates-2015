from django.views import generic
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from itertools import groupby
from . import models

# Create your views here.


class StaffIndexView (generic.ListView):
    model = models.Student_Group

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(teacher=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dates'] = sorted(list(set([
                i.date for i in models.Schedule.objects.all()])))
        return context


class IndexView (generic.View):
    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return HttpResponseRedirect(reverse('groups:schedule'))
        return StaffIndexView.as_view()(request)


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
        except (models.Debate.DoesNotExist):
            context['debate'] = None
        try:
            context['opposition'] = models.Debate.filter(
                schedule=context['debate'].schedule,
                isPresenting=True).exclude(pk=self.object.pk)
        except (models.Debate.DoesNotExist, AttributeError):
            context['opposition'] = None

        return context


class ScheduleDetailView (generic.DetailView):
    # GET GROUPS WATCHING TO WORK
    model = models.Schedule

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['aff'] = self.object.debate_set.get(
                isPresenting=True, group__position=True)
        except models.Debate.DoesNotExist:
            context['aff'] = None
        try:
            context['neg'] = self.object.debate_set.get(
                isPresenting=True, group__position=False)
        except models.Debate.DoesNotExist:
            context['neg'] = None
        try:
            groupsWatching = [i.group for i in self.object.debate_set.filter(
                isPresenting=False)]
            presents = models.Debate.objects.filter(
                isPresenting=True,
                group__in=groupsWatching).order_by(
                'schedule.pk')
            presents = groupby(presents,
                               lambda x: x.schedule.pk)
        except models.Debate.DoesNotExist:
            context['debates'] = None
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
                isPresenting=True).exclude(pk=self.objects.pk)
        except (models.Debate.DoesNotExist, AttributeError):
            context['opposition'] = None
        return context


class AZList (generic.ListView):
    # OPTIMIZE QUERY
    model = models.Student

    def get_queryset(self):
        return self.model.objects.select_related('group__teacher').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dates'] = sorted(list(set([
                i.date for i in models.Schedule.objects.all()
                if str(i.date) != self.kwargs['date']])))
        context['dat'] = self.kwargs['date']
        return context
