from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Comment


# Create your views here.


#def hello_world(request):
#    return render(request, 'article/base.html')

class PostListView(ListView):
    queryset = Post.objects.publish()
    template_name = 'article/index.html'

    def get_context_data(self, **kwargs):
        response = super().get_context_data(**kwargs)
        response["a"] = 100
        return response


class PostDetailView(DetailView):
    model = Post
    template_name = 'article/post.html'
