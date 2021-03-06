from django import template
import re

register = template.Library()

@register.filter(name='strip_non_alphanum')
def strip_non_alphanum(value):
    """
    remove all non alpha numeric
    """
    return re.sub('[^0-9a-zA-Z]+', '', value)