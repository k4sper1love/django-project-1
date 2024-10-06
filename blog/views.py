from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from blog.forms import PostForm, CommentForm
from blog.models import Post


def list_posts(request):
    posts = Post.objects.all()
    return render(request, 'blog/list_posts.html', {'posts': posts})

def single_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    form = CommentForm()
    return render(request, 'blog/single_post.html', {
        "post": post,
        "comments": comments,
        "form": form
    })

@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('single_post', post_id=post.id)

    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {"form": form})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author:
        return redirect('single_post', post_id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('single_post', post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', {"form": form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author:
        post.delete()
    return redirect('list_posts')

@login_required
def create_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('single_post', post_id=post_id)
    return redirect('single_post', post_id=post_id)

