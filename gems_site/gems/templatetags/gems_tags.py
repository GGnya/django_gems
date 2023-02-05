from django import template

register = template.Library()

menu = [
    # {'title': 'Register', 'url_name': 'register'},
    # {'title': 'Login', 'url_name': 'login'},
    {'title': 'Main page', 'url_name': 'home'},
    {'title': 'Create gem', 'url_name': 'create_gem'},
    {'title': 'Profile', 'url_name': 'profile'}
]

@register.inclusion_tag('gems/list_main_menu.html')
def show_main_menu():
    return {'menu': menu, }
