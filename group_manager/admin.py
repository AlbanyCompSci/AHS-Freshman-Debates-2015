from django.contrib import admin
from django.db.models import Q
from . import forms
from . import models
# Register your models here.


@admin.register(models.Student_Group)
class StudentGroupAdmin (admin.ModelAdmin):
    form = forms.StudentGroupForm

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(Q(ihs_teacher=request.user) |
                         Q(english_teacher=request.user))


admin.site.register(models.Student_Class)
admin.site.register(models.Judge)
admin.site.register(models.Debate_Group)
admin.site.register(models.Location)
admin.site.register(models.Schedule)
admin.site.register(models.Debate)
admin.site.register(models.Judge_Group)
