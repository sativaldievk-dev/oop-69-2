from django.urls import path
from . import views

urlpatterns = [
    path("books/", views.book_catalog, name="book_catalog"),
    path("books/<slug:slug>/", views.book_detail, name="book_detail"),
    path("library/", views.library, name="library"),
    path("book/", views.book_reader, name="book_reader"),
    path("", views.post_list, name="post_list"),
    path("profile/", views.profile, name="profile"),
    path("add/", views.add_publication, name="add_publication"),
    path("categories/add/", views.add_category, name="add_category"),
    path("quotes/", views.quote_list, name="quote_list"),
    path("quotes/add/", views.add_quote, name="add_quote"),
]
