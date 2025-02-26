from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Post
from django.core.paginator import Paginator
# Create your views here.

def home(request):
    return render(request, 'index.html')

@login_required
def posts(request):
    q = request.GET.get('q')
    print(q)
    posts = None
    if q and q != 'None':
        posts = Post.published_posts.filter(Q(title__icontains=q) | Q(body__icontains=q) | Q(slug__icontains=q))
    else:
        posts = Post.published_posts.all()

    #pagination
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    context = {
        'posts': posts,
        'q': q
    }
    return render(request, 'posts.html', context=context)

def post_details(request, pk):
    if pk:
        post = Post.published_posts.filter(pk=pk).first()

        data = {
            'post': post
        }

        return render(request, 'post_details.html', context=data)
    return redirect('home')

def post_edit(request, pk):
    if request.method == 'POST':
        if pk:
            title = request.POST.get('title')
            slug = request.POST.get('slug')
            body = request.POST.get('body')
            status = request.POST.get('status')

            Post.published_posts.filter(pk=pk).update(
                title=title,
                slug=slug,
                body=body,
                status=status
            )
            return redirect('posts')
        else:
            return redirect('posts')
    if pk:
        post = Post.published_posts.filter(pk=pk).first()
        print(pk, post)
        data = {
            'post': post
        }
        return render(request, 'post_edit.html', context=data)

def post_delete(request, pk):
    if pk:
        Post.published_posts.filter(pk=pk).update(is_deleted=True)

        return redirect('posts')
    return redirect('home')

