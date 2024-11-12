from django import template
register = template.Library()

@register.filter
def order_by(queryset, order):
    return queryset.order_by(order)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)