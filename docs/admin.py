from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin

from .models import *


class DocModelAdmin(MarkdownxModelAdmin):
    list_display = ["title", "slug", "created_on"]


class PageContentItemModelAdmin(MarkdownxModelAdmin):
    list_display = ["__str__", "doc"]


admin.site.register(Page, DocModelAdmin)
admin.site.register(PageContentItem, PageContentItemModelAdmin)
admin.site.register(Snippet, DocModelAdmin)
