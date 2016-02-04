from django.contrib import admin
from . import models
from .forms import RequiredInlineFormSet

# Register your models here.


class StudentArgumentInline (admin.TabularInline):
    model = models.Student_Argument
    formset = RequiredInlineFormSet
    extra = 3
    max_num = 3
    raw_id_fields = ('student',)


@admin.register(models.Scoring_Sheet)
class ScoringSheetAdmin (admin.ModelAdmin):
    raw_id_fields = ('judge', 'group')
    list_display = ('group', 'judge', 'total')
    inlines = [StudentArgumentInline]
    fieldsets = [
        (None, {'fields': ['group', 'judge']}),
        ('Opening Argument', {'fields': ['opening']}),
        ('Team Argument', {'fields': ['teamArg']}),
        ('Cross-Examination', {'fields': ['crossEx', 'decorum']}),
        ('Rebutal', {'fields': ['rebuttal', 'time', 'newArg']}),
        (None, {'fields': ['participation']})
    ]
