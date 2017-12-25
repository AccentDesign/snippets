from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from django.views.generic.detail import DetailView

from ..forms import SnippetForm
from ..models import Snippet


class SnippetDetailView(DetailView):
    model = Snippet


class SnippetCreateView(LoginRequiredMixin, CreateView):
    model = Snippet
    form_class = SnippetForm


class SnippetUpdateView(LoginRequiredMixin, UpdateView):
    model = Snippet
    form_class = SnippetForm
