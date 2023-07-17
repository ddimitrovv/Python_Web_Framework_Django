from django import template

register = template.Library()


@register.filter(name='calculate_cost')
def calculate_cost(value):
    cost = int((value + 1) * 1.5)
    return cost
