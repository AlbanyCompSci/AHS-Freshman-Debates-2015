from django.db import models

# http://stackoverflow.com/a/849426


class IntegerRangeField(models.IntegerField):
    def __init__(self,
                 verbose_name=None,
                 name=None,
                 min_value=None,
                 max_value=None,
                 **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)


class DecimalRangeField(models.DecimalField):
    def __init__(self,
                 verbose_name=None,
                 name=None,
                 max_digits=None,
                 decimal_places=None,
                 min_value=None,
                 max_value=None,
                 **kwargs):
        self.min_value, self.max_value = min_value, max_value
        super().__init__(
            verbose_name=verbose_name,
            name=name,
            max_digits=max_digits,
            decimal_places=decimal_places,
            **kwargs)

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(kwargs)
        return super().formfield(**defaults)
