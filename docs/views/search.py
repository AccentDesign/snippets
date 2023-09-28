import operator
from functools import partial, reduce

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.aggregates import StringAgg
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.views.generic import ListView

from ..models import BaseDoc

AND = partial(reduce, operator.and_)


class SearchView(LoginRequiredMixin, ListView):
    template_name = "docs/search.html"
    model = BaseDoc

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({"q": self.request.GET.get("q", "")})
        return context

    def get_search_kwargs(self):
        return self.request.GET.get("q", "").split()

    def get_search_vector(self):
        return (
            SearchVector("title", weight="A")
            + SearchVector("description", weight="C")
            + SearchVector(StringAgg("tags__name", delimiter=" "), weight="B")
        )

    def get_search_query(self):
        search_terms = self.get_search_kwargs()
        if not search_terms:
            return SearchQuery("")
        return AND(SearchQuery(q) for q in search_terms)

    def get_queryset(self):
        queryset = super().get_queryset()
        vector = self.get_search_vector()
        query = self.get_search_query()
        return (
            queryset.annotate(search=vector, rank=SearchRank(vector, query))
            .filter(search=query)
            .order_by("-rank", "-pk")
        )
        return queryset
