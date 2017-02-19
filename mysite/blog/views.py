from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.utils import timezone

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    try:
        post = get_object_or_404(Post, pk=pk)
        if post.published_date and post.published_date <= timezone.now():
            return render(request, 'blog/post_detail.html', {'post': post})
        else:
            raise Http404()
    except Http404:
        raise Http404()
