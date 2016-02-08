# http://stackoverflow.com/a/1233644

from django.forms.models import BaseInlineFormSet


class RequiredInlineFormSet(BaseInlineFormSet):
    """
    Generates an inline formset that is required
    """

    def _construct_form(self, i, **kwargs):
        """
        Override the method to change the form attribute empty_permitted
        """
        form = super()._construct_form(i, **kwargs)
        form.empty_permitted = False
        return form
