import django.template

register = django.template.Library()

@register .filter(name='remove_underscore')
def remove_underscore(value):
    return value.replace('_', ' ')