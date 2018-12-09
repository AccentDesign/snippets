from django import forms
from django.forms import inlineformset_factory

from dal import autocomplete

from app.forms.widets import MarkdownxWidget
from .models import Page, PageContentItem, Snippet


class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        exclude = ('content_type', )
        widgets = {
            'description': forms.widgets.Textarea(attrs={'rows': 5}),
            'content': MarkdownxWidget,
            'linked_pages': autocomplete.ModelSelect2Multiple(url='docs:page-autocomplete'),
            'tags': autocomplete.TaggitSelect2('docs:tag-autocomplete')
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        """ overwrite the form save to update the created_by and updated_by """

        instance = super().save(commit=False)

        if not self.instance.created_by:
            instance.created_by = self.user
        instance.updated_by = self.user

        instance.save()
        self.save_m2m()

        return instance


class PageContentItemForm(forms.ModelForm):
    class Meta:
        model = PageContentItem
        fields = ('content', 'snippet', 'order')
        widgets = {
            'content': MarkdownxWidget
        }


PageContentItemFormset = inlineformset_factory(
    Page,
    PageContentItem,
    form=PageContentItemForm,
    extra=0,
    can_delete=True,
    can_order=False
)


class SnippetForm(forms.ModelForm):
    class Meta:
        model = Snippet
        exclude = ('content_type', )
        widgets = {
            'description': forms.widgets.Textarea(attrs={'rows': 5}),
            'content': MarkdownxWidget,
            'tags': autocomplete.TaggitSelect2('docs:tag-autocomplete')
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        """ overwrite the form save to update the created_by and updated_by """

        instance = super().save(commit=False)

        if not self.instance.created_by:
            instance.created_by = self.user
        instance.updated_by = self.user

        instance.save()
        self.save_m2m()

        return instance
