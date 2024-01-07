# In your app's filters.py
from django import template

register = template.Library()

@register.filter
def my_timestamp_format(value):
    month_names = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")

    # Format time without seconds using strftime
    time_str = value.strftime("%I:%M %p")  # Example format: 09:45 PM

    return f'{month_names[value.month - 1]} {value.day}, {time_str}'

