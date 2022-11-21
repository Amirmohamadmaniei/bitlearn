from django import template

register = template.Library()


@register.filter(name='separator')
def separator(value):
    r = ''
    c = 0
    value = str(value)
    value = value[::-1]
    for i in value:
        r += i
        c += 1
        if c % 3 == 0 and c < len(value):
            r += ','

    return r[::-1]
