from django import template

register = template.Library()

menu = [
    {'title': 'Main page', 'url_name': 'home'},
    {'title': 'Create gem', 'url_name': 'create_gem'},
    {'title': 'Profile', 'url_name': 'profile'}
]


@register.inclusion_tag('gems/list_main_menu.html')
def show_main_menu():
    return {'menu': menu, }



@register.filter
# Gets the name of the passed in field on the passed in object
def verbose_name(the_object, the_field):
    return the_object._meta.get_field(the_field).verbose_name
