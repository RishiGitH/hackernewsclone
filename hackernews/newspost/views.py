from django.shortcuts import render, HttpResponse, redirect,render
from django.http import HttpResponse, HttpResponseNotFound, Http404,  HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Post,Comment
from django.urls import reverse
from .forms import CommentForm,PostForm,UserCreationForm1
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template.loader import get_template ,render_to_string
from django.template import Context
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
import json
import math
from django.http import JsonResponse



def index(request):
    posts = Post.objects.all().order_by('timestamp')
    count=len(posts)/10
    count=math.ceil(count)
    print(count)
    posts=posts[:10]
    context={'posts':posts,'pages':range(count)}
    return render(request, 'newspost/index.html',context)


def lazy_load_posts(request):
    page = request.POST.get('page')
    posts = Post.objects.all()
    results_per_page = 10
    paginator = Paginator(posts, results_per_page)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(2)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    # build a html posts list with the paginated posts
    posts_html = loader.render_to_string(
        'newspost/posts.html',
        {'posts': posts,'user':request.user}
    )
    # package output data and return it as a JSON object
    output_data = {
        'posts_html': posts_html,
        'has_next': posts.has_next()
    }
    return JsonResponse(output_data)

def search(request):

    s=request.GET.get('q')
    print(s)
    posts = Post.objects.filter(Q(post_title__icontains=s))
    if request.session.get('username'):
        name_user=request.session.get('username')
        context={'username':name_user,'posts':posts}
        return render(request, 'newspost/index.html',context)
    else:
        context={'posts':posts}
        return render(request, 'newspost/index.html',context)



def post(request,post_id):
    post=Post.objects.get(id=post_id)
    comments=Comment.objects.all().filter(post_id=post).filter(parent_comment=None)
    # c.filter(child_comment!=None)
    form = CommentForm()
    form1=CommentForm()
    return render(request,'newspost/post.html',{'form': form,'form1':form1,'post':post,'comments':comments})


@login_required
def upvote_p(request):
    post_id = None
    if request.method == 'GET':
        post_id = request.GET['post_id']

    post=Post.objects.get(id=post_id)
    post.post_upvote.add(request.user)
    post.save()

    data=post.post_upvote.count()
    print(data)
    return HttpResponse(data)

@login_required
def upvote_c(request):
    comment_id = None
    if request.method == 'GET':
        comment_id = request.GET['comment_id']

    comment=Comment.objects.get(id=comment_id)
    comment.comment_upvote.add(request.user)

    data=comment.comment_upvote.count()
    print(data)
    return HttpResponse(data)

def allcomment(request):

    comments=Comment.objects.all().order_by('-timestamp').filter(parent_comment=None)
    return render(request,'newspost/allcomment.html',{'comments':comments})


@login_required(login_url='newspost:login1')
def reply(request):
    if request.method == 'POST' and request.is_ajax() :
        comment_text = request.POST.get('data1')
        comment_id=request.POST.get('id')
        comment=Comment.objects.get(id=comment_id)
        post=comment.post_id
        text=comment_text.split('text=')

        child_comment=Comment(text=text[1],post_id=post,user_id=request.user,level_count=comment.level_count+1,parent_comment=comment)
        child_comment.save()
        form=CommentForm()
        t = get_template('newspost/reply.html')
        c = {'form':form,'obj': child_comment,'user':request.user}
        rendered = t.render(c)
        # reply_page = render_to_string('newspost/reply.html',{'form':form,'obj': child_comment})
        # html = reply_page.render({'obj': child_comment})
        return HttpResponse(json.dumps({'html':rendered,'child_id':child_comment.id}),content_type='application/json')
    else:
        return HttpResponse('error')


@login_required(login_url='newspost:login1')
def post_comment(request):
    if request.method == 'POST' and request.is_ajax() :
        post_text = request.POST.get('data1')
        post_id=request.POST.get('id')
        post=Post.objects.get(id=post_id)
        print(post_text)
        data_text=post_text.split('text=')
        text=data_text[2].split('&')
        print(text)

        comment=Comment(text=text[0],post_id=post,user_id=request.user)
        comment.save()
        form=CommentForm()
        t = get_template('newspost/reply.html')
        c = {'form':form,'obj': comment,'user':request.user}
        rendered = t.render(c)
        return HttpResponse(json.dumps({'html':rendered,'comment_id':comment.id}),content_type='application/json')
    else:
        return HttpResponse('error')

@login_required(login_url='newspost:login1')
def addPost(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PostForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            post1=Post(post_title=form.cleaned_data['post_title'],post_link=form.cleaned_data['post_link'],user_id=request.user)
            post1.save()
            return post(request,post1.id)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PostForm()
    return render(request,'newspost/addPost.html',{'form': form})



def register1(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UserCreationForm1(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            user=authenticate(username=username,password=password)

            if user is not None:
                if user.is_active:
                    login(request,user)

            return index(request)
    else:
        form = UserCreationForm1()
    return render(request,'newspost/register1.html',{'form':form})

def login1(request):
    if request.method == 'POST':
        form=AuthenticationForm()
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return index(request)
            else:
                return render(request,'newspost/login.html',{'error':'User is inactive','form':form})
        else:
            return render(request,'newspost/login.html',{'error':'wrong username or password','form':form})
    form = AuthenticationForm()
    return render(request,'newspost/login.html',{'error':None,'form':form})



def logout1(request):
    logout(request)
    return index(request)

