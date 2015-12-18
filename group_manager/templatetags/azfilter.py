from django import template
from group_manager import models

register = template.Library()


@register.simple_tag
def azfilter(student, period, date):
    """ Gets the current location given a student """
    try:
        return student.group.affTeam.debate_set.get(
            schedule__period=period,
            schedule__date=date).schedule.location
    except (models.Debate.DoesNotExist, AttributeError):
        try:
            return student.group.negTeam.debate_set.get(
                    schedule__period=period,
                    schedule__date=date).schedule.location
        except (models.Debate.DoesNotExist, AttributeError):
            return
    return
