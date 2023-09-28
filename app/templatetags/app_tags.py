from django.template import Library

register = Library()


@register.filter(name="addcss")
def addcss(value, arg):
    return value.as_widget(attrs={"class": arg})
