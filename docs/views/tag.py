from taggit.models import Tag

from app.views.mixins import AutoCompleteView


class TagsAutocomplete(AutoCompleteView):
    model = Tag
    filter_arg = 'name__istartswith'
