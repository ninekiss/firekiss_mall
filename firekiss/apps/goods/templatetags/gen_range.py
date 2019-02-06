from django import template


def new_range(value, arg):
    """Removes all values of arg from the given string"""

    if arg == 'nlet6':
        arg = value + 1
        value = 1
    elif arg == 'let8':
        value = value - 4
        arg = value + 1
    elif arg == 'gt8':
        value = value - 2
        arg = value + 3
    return range(value, arg)


register = template.Library()
register.filter('range', new_range)