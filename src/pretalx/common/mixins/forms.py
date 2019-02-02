from django import forms
from django.utils.translation import ugettext_lazy as _

from pretalx.common.forms.utils import get_help_text


class ReadOnlyFlag:
    def __init__(self, *args, read_only=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.read_only = read_only
        if read_only:
            for field in self.fields.values():
                field.disabled = True

    def clean(self):
        if self.read_only:
            raise forms.ValidationError(_('You are trying to change read only data.'))
        return super().clean()


class RequestRequire:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.Meta.request_require:
            request = self.event.settings.get('cfp_request_{}'.format(key))
            require = self.event.settings.get('cfp_require_{}'.format(key))
            if not request:
                self.fields.pop(key)
            else:
                self.fields[key].required = require
                min_value = self.event.settings.get('cfp_{}_min_length'.format(key))
                max_value = self.event.settings.get('cfp_{}_max_length'.format(key))
                if min_value:
                    self.fields[key].widget.attrs['minlength'] = min_value
                if max_value:
                    self.fields[key].widget.attrs['maxlength'] = max_value
                self.fields[key].help_text = get_help_text(
                    self.fields[key].help_text, min_value, max_value
                )
