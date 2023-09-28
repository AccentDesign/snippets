from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from taggit.models import Tag

from app.views.mixins import AutoCompleteView


class TagsAutocomplete(AutoCompleteView):
    model = Tag
    filter_arg = "name__istartswith"


class TagsView(LoginRequiredMixin, ListView):
    model = Tag
    template_name = "docs/tag_list.html"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related("taggit_taggeditem_items")
            .order_by("name")
        )
