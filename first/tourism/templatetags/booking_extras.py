from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    try:
        return float(value) * int(arg)
    except:
        return 0

@register.filter
def currency(value):
    try:
        return f"{int(value):,}"
    except:
        return value

@register.simple_tag
def calc_total(hotels_with_qty):
    total = 0
    for hotel, qty in hotels_with_qty:
        try:
            total += float(hotel.price) * int(qty)
        except:
            continue
    return total

@register.filter
def to_range(start, end):
    return range(start, end + 1)
