import re

from django.core import validators
from django.utils.translation import gettext_lazy as _

class CustomASCIIUsernameValidator(validators.RegexValidator):
    regex = r'^[\w.]+$'
    message = _(
        'Enter a valid username. This value may contain only English letters, '
        'numbers, and ./_ characters.'
    )
    flags = re.ASCII
