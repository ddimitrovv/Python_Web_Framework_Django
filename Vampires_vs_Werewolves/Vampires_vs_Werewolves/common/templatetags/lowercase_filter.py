from django import template

register = template.Library()


@register.filter
def model_name_lower(model):
    return model._meta.model_name.lower()
