from django.contrib import admin
from django.urls import path, re_path, reverse
from . import views

urlpatterns=[
    #path(''),
    path('borrowers/', views.BorrowerListView.as_view(), name = 'borrowerlist'),
    re_path(r'borrowers/(?P<pk>[a-zA-Z0-9]+)/$', views.BorrowerDetailView.as_view(), name='borrower-detail'),
    path('books/', views.BooksListView.as_view(), name = 'bookslist'),
    re_path(r'books/(?P<pk>[a-zA-Z0-9]+)/$', views.BookDetailsView.as_view(), name='biblio-detail'),
    path('items/', views.ItemsListView.as_view(), name='itemlist'),
    re_path(r'items/(?P<pk>[a-zA-Z0-9]+)/$', views.ItemDetailsView.as_view(), name='item-detail'),
    path('genre/', views.GenreListView.as_view(), name='genrelist'),

]