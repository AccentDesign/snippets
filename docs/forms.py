from django import forms
from django.forms import inlineformset_factory

from .models import Page, PageContentItem, Snippet


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        exclude = ('content_type',)


class PageContentItemForm(forms.ModelForm):
    class Meta:
        model = PageContentItem
        fields = ('content', 'snippet', 'order')


PageContentItemFormset = inlineformset_factory(
    Page,
    PageContentItem,
    form=PageContentItemForm,
    extra=0,
    can_delete=True,
    can_order=False,
    widgets={}
)


class SnippetForm(forms.ModelForm):
    class Meta:
        model = Snippet
        exclude = ('content_type', )
