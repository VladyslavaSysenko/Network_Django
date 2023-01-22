from django import template
from time import strftime, localtime

register = template.Library()

# Convert server time to local time
@register.filter(name="local_time")
def time(value):
    return strftime('%d.%m.%Y %H:%M', localtime(value.timestamp()))

# Reverse list
@register.filter(name="reverse")
def reverse(value):
    return value[::-1]

# Slice 
@register.filter(name="slices")
def reverse(value, page):
    return value[:(-len(str(page))-1)]