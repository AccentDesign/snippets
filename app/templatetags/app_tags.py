from django.template import Library

from docs.models import Page, Snippet

register = Library()


@register.filter(name='addcss')
def addcss(value, arg):
    return value.as_widget(attrs={'class': arg})

@register.inclusion_tag(filename='tags/latest.html')
def latest_pages(count):
    return {'objects': Page.objects.all().order_by('-updated_on')[:count]}

@register.inclusion_tag(filename='tags/latest.html')
def latest_snippets(count):
    return {'objects': Snippet.objects.all().order_by('-updated_on')[:count]}
