from django import template
from datetime import date, timedelta

register = template.Library()


@register.filter    
def to_int(value):
    return int(value)+1

@register.filter
def lookup(d, key):
    return d[key]

@register.filter
def lookup_food_des(d, key):
    return d[key].description

@register.filter
def lookup_food_price(d, key):
    return d[key].price

@register.filter
def lookup_food_picture(d, key):
    return d[key].picture

@register.filter
def mod(d, key):
    return d%key

@register.filter
def lookup_ingredient_name(d, key):
    return d[key].name

@register.filter
def lookup_ingredient_amount(d, key):
    return d[key].amount

@register.filter
def is_true(arg): 
    return arg is True

@register.filter
def to_string(value):
	return str(value)

@register.filter
def get_range( value ):
    return range( value )

@register.filter
def get_food_name(d, key):
    return d[key].food.name

@register.filter
def get_amount(d, key):
    return d[key].amount

@register.filter
def get_food_picture(d, key):
    return d[key].food.picture

@register.filter
def get_order_food_id(d, key):
    return d[key].id

@register.filter
def get_restaurant_name(d, key):
    return d[key].name

@register.filter
def get_restaurant_picture(d, key):
    return d[key].picture