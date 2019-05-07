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



def index(request):
    posts = Post.objects.all().order_by('timestamp')
    context={'posts':posts}
    return render(request, 'newspost/index.html',context)


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

    if request.user.is_authenticated:

        if request.method == 'POST':
            # create a form instance and populate it with data from the request:

            form = CommentForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                # redirect to a new URL:
                comment=Comment(text=form.cleaned_data['text'],post_id=post,user_id=request.user)
                comment.save()
                comments=Comment.objects.all().filter(post_id=post).filter(parent_comment=None)
                return render(request,'newspost/post.html',{'form': form,'post':post,'comments':comments})
        # if a GET (or any other method) we'll create a blank form
        else:
            form = CommentForm()
    else:
        form = CommentForm()
        if request.method=='POST':
            return render(request,'newspost/post.html',{'error':'please log in','form': form,'post':post,'comments':comments})
    return render(request,'newspost/post.html',{'form': form,'post':post,'comments':comments})


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

def allcomment(request ):

    comments=Comment.objects.all()
    return render(request,'newspost/allcomment.html',{'comments':comments})

def upvote_comment(request,comment_id):

    comment=Comment.objects.get(id=comment_id)
    comment.comment_upvote.add(request.user)
    post=comment.post_id
    return redirect('newspost:post',post_id=post.id)

def upvote_post(request,post_id):

    post=Post.objects.get(id=post_id)
    post.post_upvote.add(request.user)
    return redirect('newspost:post',post_id=post.id)

@login_required(login_url='newspost:login1')
def reply(request,comment_id):
    comment=Comment.objects.get(id=comment_id)
    post=comment.post_id
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CommentForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            child_comment=Comment(text=form.cleaned_data['text'],post_id=post,user_id=request.user,level_count=comment.level_count+1,parent_comment=comment)
            child_comment.save()

        return redirect('newspost:post',post_id=post.id)

    else:
        form = CommentForm()
    return render(request,'newspost/reply.html',{'form': form,'post':post,'comments':comment})

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
            post=Post(post_title=form.cleaned_data['post_title'],post_link=form.cleaned_data['post_link'],user_id=request.user)
            post.save()
            return post(request,post.id)

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

