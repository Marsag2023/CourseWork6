from django.forms import ModelForm

from blogs.models import Blog


class BlogForm(ModelForm):
    class Meta:
        model = Blog
        exclude = ("slug", "created_at", "number_of_views",)
