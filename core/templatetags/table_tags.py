from django import template
from django.urls import reverse

register = template.Library()

@register.filter
def attr(obj, key):
    return getattr(obj, key, "")

@register.simple_tag
def url_with_kwargs(url_name, **kwargs):
    return reverse(url_name, kwargs=kwargs)

@register.simple_tag
def build_url(url_name, row, param):
    return reverse(url_name, args=[getattr(row, param)])