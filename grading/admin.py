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
    classes = ('grp-collapse grp-open',)
    autocomplete_lookup_fields = {'fk': ['student']}


@admin.register(models.Scoring_Sheet)
class ScoringSheetAdmin (admin.ModelAdmin):
    raw_id_fields = ('judge', 'group')
    list_display = ('group', 'judge', 'total')
    list_filter = ('group', 'judge')
    inlines = [StudentArgumentInline]
    fieldsets = [
        (None, {'fields': ['group', 'judge']}),
        ('Opening Argument', {'fields': ['opening'],
         'classes': ('grp-collapse grp-open',)}),
        ('Team Argument', {'fields': ['teamArg'],
         'classes': ('grp-collapse grp-open',)}),
        ('Cross-Examination', {'fields': ['crossEx', 'decorum'],
         'classes': ('grp-collapse grp-open',)}),
        ('Rebutal', {'fields': ['rebuttal', 'time', 'newArg'],
         'classes': ('grp-collapse grp-open',)}),
        (None, {'fields': ['participation']})
    ]
    related_lookup_fields = {'fk': ['group']}
    autocomplete_lookup_fields = {'fk': ['judge']}
