from django.db import models


class IntegerRangeField(models.IntegerField):
    """ An integer field range. requires min_value and max_value """
    def __init__(self, verbose_name=None, name=None,
                 min_value=1, max_value=7, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        choice = tuple(zip(
                        range(min_value, max_value + 1),
                        (str(i) for i in range(min_value, max_value + 1))))
        kwargs['choices'] = choice
        models.IntegerField.__init__(self, verbose_name, name,
                                     **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)
