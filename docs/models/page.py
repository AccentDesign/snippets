from django.db import models
from django.urls import reverse

from modelcluster.fields import ParentalKey
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

from .base import BaseDoc


class PageContentItem(models.Model):
    """ Page content """

    doc = ParentalKey(
        'BaseDoc',
        on_delete=models.CASCADE,
        related_name='content_items'
    )
    content = MarkdownxField(
        blank=True
    )
    snippet = models.ForeignKey(
        'docs.Snippet',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    order = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ['order', ]

    @property
    def formatted_content(self):
        return markdownify(self.content)


class Page(BaseDoc):
    """ Page model """

    def get_absolute_url(self):
        return reverse('docs:page-detail', kwargs={'slug': self.slug})
