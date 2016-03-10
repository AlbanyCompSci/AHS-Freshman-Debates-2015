from django import template

register = template.Library()

@register.filter
def resolve(list, index):
    try:
        return list[index]
    except:
        return None
