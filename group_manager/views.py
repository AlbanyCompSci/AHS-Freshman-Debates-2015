from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views import generic
from . import models
from . import forms

# Create your views here.


class LoginRequiredMixin (object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class IndexView (LoginRequiredMixin, generic.ListView):
    template_name = 'group_manager/index.html'
    context_object_name = 'groups'

    def get_queryset(self):
        """Returns all groups belonging to user"""
        return models.Student_Group.objects.filter(teacher=self.request.user)


class GroupDetailView (generic.DetailView):
    model = models.Student_Group


class StudentDetailView (generic.DetailView):
    model = models.Student


class StudentGroupCreate (LoginRequiredMixin, generic.FormView):
    template_name = 'group_manager/student_group_form.html'
    form_class = forms.StudentGroupForm

    def get_success_url(self):
        return reverse('groups:index')

    def form_valid(self, form):
        form_uncommited = form.save(commit=False, user=self.request.user)
        form_uncommited.teacher = self.request.user
        form_uncommited.save()
        form.cleaned_data['students'].update(group=form_uncommited)
        return super().form_valid(form)



    """def form_valid(self, form):
        form_uncommited = form.save(commit=False)
        form_uncommited.teacher = self.request.user
        form.mod_students(form_uncommited)
        form_uncommited.save()
        return super().form_valid(form)"""
