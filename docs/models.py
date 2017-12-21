from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _

from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from taggit.managers import TaggableManager


def get_default_form_content_type():
    return ContentType.objects.get_for_model(BaseDoc)


class BaseDoc(ClusterableModel):
    """ Doc base class """

    title = models.CharField(
        max_length=150
    )
    slug = models.SlugField(
        max_length=100,
        unique=True
    )
    description = models.TextField(
        blank=True
    )
    created_on = models.DateTimeField(
        auto_now_add=True
    )
    content_type = models.ForeignKey(
        'contenttypes.ContentType',
        related_name='docs',
        on_delete=models.SET(get_default_form_content_type)
    )

    tags = TaggableManager(blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.id:
            self.content_type = ContentType.objects.get_for_model(self)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title', ]
        verbose_name = _('doc')

    @cached_property
    def specific(self):
        content_type = ContentType.objects.get_for_id(self.content_type_id)
        model_class = content_type.model_class()
        if model_class is None:
            return self
        elif isinstance(self, model_class):
            return self
        else:
            return content_type.get_object_for_this_type(id=self.id)

    @cached_property
    def specific_class(self):
        content_type = ContentType.objects.get_for_id(self.content_type_id)
        return content_type.model_class()


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


class Snippet(BaseDoc):
    """ Snippet model """

    content = MarkdownxField()

    def get_absolute_url(self):
        return reverse('docs:snippet-detail', kwargs={'slug': self.slug})

    @property
    def formatted_content(self):
        return markdownify(self.content)
