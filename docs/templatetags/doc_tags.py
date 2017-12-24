from django.template import Library

from ..models import Page, Snippet


register = Library()


@register.inclusion_tag(filename='docs/tags/latest.html')
def latest_pages(count):
    return {'objects': Page.objects.all().order_by('-updated_on')[:count]}

@register.inclusion_tag(filename='docs/tags/latest.html')
def latest_snippets(count):
    return {'objects': Snippet.objects.all().order_by('-updated_on')[:count]}
