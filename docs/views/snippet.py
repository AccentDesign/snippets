from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from django.views.generic.detail import DetailView

from ..forms import SnippetForm
from ..models import Snippet


class SnippetDetailView(LoginRequiredMixin, DetailView):
    model = Snippet


class SnippetCreateView(LoginRequiredMixin, CreateView):
    model = Snippet
    form_class = SnippetForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs


class SnippetUpdateView(LoginRequiredMixin, UpdateView):
    model = Snippet
    form_class = SnippetForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs
