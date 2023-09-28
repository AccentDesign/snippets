from django.urls import reverse
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

from .base import BaseDoc


class Snippet(BaseDoc):
    """Snippet model"""

    content = MarkdownxField()

    def get_absolute_url(self):
        return reverse("docs:snippet-detail", kwargs={"slug": self.slug})

    @property
    def formatted_content(self):
        return markdownify(self.content)
