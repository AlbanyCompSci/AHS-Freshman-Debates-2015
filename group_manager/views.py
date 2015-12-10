from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic
from django.shortcuts import render
from . import models
from . import forms
from django.contrib.auth.models import User
# Create your views here.


class IsSuperuserMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class IndexView (LoginRequiredMixin, generic.ListView):
    model = models.Student_Group

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(teacher=self.request.user)


class StudentGroupCreate (LoginRequiredMixin, generic.FormView):
    template_name = 'group_manager/student_group_form.html'
    form_class = forms.StudentGroupForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
                      'teacher': self.kwargs['teacher'],
                      'periods': (int(i) for i in self.kwargs['periods'])
                      })
        return kwargs

    def get_success_url(self):
        return reverse('groups:index')

    def form_valid(self, form):
        form_uncommited = form.save(commit=False)
        form_uncommited.teacher = User.objects.get(pk=self.kwargs['teacher'])
        form_uncommited.save()
        form.cleaned_data['students'].update(group=form_uncommited)
        return super().form_valid(form_uncommited)


class StudentGroupDetailView (generic.DetailView):
    model = models.Student_Group

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['location'] = self.object.affTeam.debate_set.get(
                    isPresenting=True).schedule.location
        except models.Debate_Group.DoesNotExist:
            try:
                context['location'] = self.object.negTeam.debate_set.get(
                    isPresenting=True).schedule.location
            except models.Debate_Group.DoesNotExist:
                context['location'] = 'No location currently picked'
        return context


class StudentGroupPeriodSelect(generic.View):
    def get(self, request, teacher):
        periods = models.Student_Class.objects.filter(
                            type=models.Student_Class.ENGLISH_TYPE,
                            teacher__pk=teacher)
        return render(request,
                      'group_manager/student_group_period_select.html', {
                            'periods': periods
                      })

    def post(self, request, teacher):
        selected = request.POST.getlist('period')
        if not selected:
            periods = models.Student_Class.objects.filter(
                            type=models.Student_Class.ENGLISH_TYPE,
                            teacher__pk=teacher)
            return render(request,
                        'group_manager/student_group_period_select.html', {
                            'periods': periods,
                            'error_message': "You didn't select a choice."
                                })
        return HttpResponseRedirect(
                        reverse_lazy('groups:student_group_form', kwargs={
                                'teacher': teacher,
                                'periods': ''.join(selected),
                                }))


class StudentGroupDelete (LoginRequiredMixin, generic.DeleteView):
    model = models.Student_Group
    success_url = reverse_lazy('groups:index')


class DebateGroupDelete (IsSuperuserMixin, generic.DeleteView):
    model = models.Debate_Group
    success_url = reverse_lazy('groups:debate_index')


class DebateGroupCreate (IsSuperuserMixin, generic.CreateView):
    model = models.Debate_Group
    fields = '__all__'
