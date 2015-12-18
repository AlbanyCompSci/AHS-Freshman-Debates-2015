from django.views import generic
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from . import models

# Create your views here.


class StaffIndexView (generic.ListView):
    model = models.Student_Group

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(teacher=self.request.user)


class IndexView (generic.View):
    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return HttpResponseRedirect(reverse('groups:schedule'))
        return StaffIndexView.as_view()(request)


class StudentGroupDetailView (generic.DetailView):
    model = models.Student_Group

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            debateG = self.object.affTeam
            context['position'] = 'Affirmative'
        except models.Debate_Group.DoesNotExist:
            try:
                debateG = self.object.negTeam
                context['position'] = 'Negative'
            except models.Debate_Group.DoesNotExist:
                debateG = None
                context['position'] = 'None'

        try:
            context['schedule'] = debateG.debate_set.get(
                    isPresenting=True).schedule
        except (models.Debate.DoesNotExist, AttributeError):
            context['schedule'] = None
        context['matchup'] = debateG

        return context


class ScheduleDetailView (generic.DetailView):
    model = models.Schedule

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['presenting'] = self.object.debate_set.get(isPresenting=True)
            context['topic'] = self.object.debate_set.get(isPresenting=True).debate_group.title
        except models.Debate.DoesNotExist:
            context['presenting'] = None
            context['topic'] = None
        try:
            context['debates'] = self.object.debate_set.filter(isPresenting=False)
        except models.Debate.DoesNotExist:
            context['debates'] = None
        return context


class StudentDetailView (generic.DetailView):
    model = models.Student

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            group = self.object.group
        except models.Student_Group.DoesNotExist:
            group = None
        if group:
            try:
                debateG = group.affTeam
                context['position'] = 'Affirmative'
            except models.Debate_Group.DoesNotExist:
                try:
                    debateG = group.negTeam
                    context['position'] = 'Negative'
                except models.Debate_Group.DoesNotExist:
                    debateG = None
                    context['position'] = 'None'
            if debateG:
                try:
                    context['schedule'] = debateG.debate_set.get(
                            isPresenting=True).schedule
                except models.Debate.DoesNotExist:
                    context['schedule'] = None
            context['matchup'] = debateG
        return context


class AZList (generic.ListView):
    model = models.Student

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['dates'] = sorted(list(set([
                i.date for i in models.Schedule.objects.all()])))
        return context
