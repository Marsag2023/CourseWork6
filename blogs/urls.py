from django.urls import path
from django.views.decorators.cache import never_cache
from blogs.apps import BlogsConfig
from blogs.views import (BlogCreateView, BlogDetailView, BlogListView,
                         BlogUpdateView, BlogDeleteView, toggle_activity)

app_name = BlogsConfig.name

urlpatterns = [
    path('blogs/create/', BlogCreateView.as_view(), name='create'),
    path('blogs/', never_cache(BlogListView.as_view()), name='blogs'),
    path('blogs/view/<int:pk>/', BlogDetailView.as_view(), name='view'),
    path('blogs/edit/<int:pk>/', never_cache(BlogUpdateView.as_view()), name='edit'),
    path('blogs/delete/<int:pk>/', BlogDeleteView.as_view(), name='delete'),
    path('blogs/activity/<int:pk>/', toggle_activity, name="toggle_activity"),
]
