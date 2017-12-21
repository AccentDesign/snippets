from django.urls import path

from .views import *

app_name = 'docs'

urlpatterns = [
    path('search/', SearchView.as_view(), name='search'),
    path('pages/create/', PageCreateView.as_view(), name='page-create'),
    path('pages/<slug:slug>/', PageDetailView.as_view(), name='page-detail'),
    path('pages/<slug:slug>/update/', PageUpdateView.as_view(), name='page-update'),
    path('snippets/create/', SnippetCreateView.as_view(), name='snippet-create'),
    path('snippets/<slug:slug>/', SnippetDetailView.as_view(), name='snippet-detail'),
    path('snippets/<slug:slug>/update/', SnippetUpdateView.as_view(), name='snippet-update')
]
