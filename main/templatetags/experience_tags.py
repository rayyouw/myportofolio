import re

from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter
def highlight_person_in_charge(value):
    escaped_value = conditional_escape(value)
    highlighted_value = re.sub(
        r"Person in Charge",
        lambda match: f"<strong>{match.group(0)}</strong>",
        escaped_value,
        flags=re.IGNORECASE,
    )
    return mark_safe(highlighted_value)