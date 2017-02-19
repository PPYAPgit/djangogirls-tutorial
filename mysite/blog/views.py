from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm

# Create your views here.
def post_list(request):
    # publish 날짜가 된 것들만 보여준다
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    try:
        post = get_object_or_404(Post, pk=pk)

        # publish된 것들만 보여준다
        if post.published_date and post.published_date <= timezone.now():
            return render(request, 'blog/post_detail.html', {'post': post})
        else:
            raise Http404()
    except Http404:
        raise Http404()

def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.publish()
            return redirect('post_detail', pk=post.pk)
        else:
            return redirect('post_list')
    else:
        form = PostForm()
        return render(request, 'blog/post_new.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.pk = pk
            post.publish()
        return redirect('post_detail', pk=pk)
    else:
        form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})

def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')
