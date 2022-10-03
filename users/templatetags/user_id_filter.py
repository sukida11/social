from django import template

register = template.Library()

@register.filter(name='id_filter')
def id_filter(value, id):

	return value.filter(user_id=id).all()