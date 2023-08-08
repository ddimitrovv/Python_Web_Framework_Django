from django import template

register = template.Library()


@register.filter
def percent(value1, value2):
    return (value1 / value2) * 100
