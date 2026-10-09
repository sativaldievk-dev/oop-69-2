from django.urls import path
from .views import PostListView, PostDetailView, toggle_active

urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path("<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path(
        "<int:pk>/toggle-active/",
        toggle_active,
        name="toggle_active",
    ),
]