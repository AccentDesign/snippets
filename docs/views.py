from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, ListView
from django.views.generic.detail import DetailView

from .forms import PageForm, PageContentItemFormset, SnippetForm
from .models import BaseDoc, Page, Snippet


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


class PageCreateView(LoginRequiredMixin, CreateView):
    model = Page
    form_class = PageForm
    formset_class = PageContentItemFormset

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = self.formset_class()
        context = self.get_context_data(form=form, formset=formset)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = self.formset_class(self.request.POST)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        self.object = form.save()
        formset.instance = self.object
        formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, formset):
        context = self.get_context_data(form=form, formset=formset)
        return self.render_to_response(context)


class PageUpdateView(LoginRequiredMixin, UpdateView):
    model = Page
    form_class = PageForm
    formset_class = PageContentItemFormset

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = self.formset_class(instance=self.object)
        context = self.get_context_data(form=form, formset=formset)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = self.formset_class(request.POST, instance=self.object)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):
        self.object = form.save()
        formset.instance = self.object
        formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, formset):
        context = self.get_context_data(form=form, formset=formset)
        return self.render_to_response(context)


class PageDetailView(DetailView):
    model = Page


class SnippetDetailView(DetailView):
    model = Snippet


class SnippetCreateView(LoginRequiredMixin, CreateView):
    model = Snippet
    form_class = SnippetForm


class SnippetUpdateView(LoginRequiredMixin, UpdateView):
    model = Snippet
    form_class = SnippetForm
