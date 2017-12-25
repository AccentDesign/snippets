from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.views.generic import ListView

from ..models import BaseDoc


class SearchView(ListView):
    template_name = 'docs/search.html'
    model = BaseDoc

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'q': self.request.GET.get('q')
        })
        return context

    def get_queryset(self):
        q = self.request.GET.get('q')
        vector = SearchVector('title', 'description', 'tags__name')
        query = SearchQuery(q)
        return self.model.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.01).order_by('-rank')
