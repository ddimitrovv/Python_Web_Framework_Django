from django import template

register = template.Library()


@register.filter
def multiply(value1, value2):
    return value1 * value2
