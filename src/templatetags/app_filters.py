from django import template

register = template.Library()

@register.filter(name='removewhitespace')
def removewhitespace(value):
    """
    remove white space
    """
    return value.replace(' ', '')