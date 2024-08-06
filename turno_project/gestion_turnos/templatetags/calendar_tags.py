from django import template
from datetime import timedelta

register = template.Library()

@register.filter
def add_days(date, days):
    """Suma días a una fecha."""
    return date + timedelta(days=days)

@register.simple_tag
def range(start, end):
    """Genera un rango de números."""
    return range(start, end)

@register.simple_tag
def range_tag(start, end):
    """Genera un rango de números."""
    return range(start, end)