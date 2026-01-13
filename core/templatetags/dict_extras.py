from django import template

register = template.Library()

@register.filter
def dict_get(d, key):
    if d is None:
        return None
    try:
        return d.get(key)
    except Exception:
        try:
            return d.get(str(key))
        except Exception:
            return None
