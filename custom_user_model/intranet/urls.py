from django.contrib import admin
from django.urls import path, re_path, reverse
from . import views

urlpatterns=[
    #path(''),
    path('borrowers/', borrowers),
    re_path(r'borrowers/(?P<pk>[a-zA-Z0-9]+)/$', views.BorrowerDetailView.as_view(), name='borrower-detail'),
    path('books/', views.BooksListView.as_view(), name = 'bookslist'),
    re_path(r'books/(?P<pk>[a-zA-Z0-9]+)/$', views.BookDetailsView.as_view(), name='biblio-detail'),


]