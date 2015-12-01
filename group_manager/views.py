from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.shortcuts import render
from . import models
from . import forms
from django.contrib.auth.models import User
# Create your views here.


class LoginRequiredMixin (object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


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


def StudentGroupPeriodSelect(request, teacher):
    selected = request.POST.getlist('period')
    if not selected:
        return render(request,
                      'group_manager/student_group_period_select.html', {
                        'periods': models.Student_Class.objects
                        .filter(type=models.Student_Class.ENGLISH_TYPE)
                        .filter(teacher__pk=teacher),
                        'error_message': "You didn't select a choice."
                        })
    else:
        return HttpResponseRedirect(
            reverse('groups:student_group_form', kwargs={
                        'teacher': teacher,
                        'periods': ''.join(selected),
                    }))
