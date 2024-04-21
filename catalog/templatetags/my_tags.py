from django import template

register = template.Library()


@register.filter()
def media_image(val):
    if val:
        return f'/media/{val}'
    return '#'
