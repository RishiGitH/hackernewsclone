from django.shortcuts import render, HttpResponse, redirect,render
from django.http import HttpResponse, HttpResponseNotFound, Http404,  HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Post,Comment,RecursiveThing
from django.urls import reverse
from .forms import CommentForm,PostForm,UserCreationForm1,UserChangeForm1,UserForm
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User



def index(request):
    posts = Post.objects.all().order_by('timestamp')
    tt=RecursiveThing.objects.all().filter(parent=None)
    context={'posts':posts,'things':tt}
    return render(request, 'newspost/new.html',context)


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
    p=Post.objects.get(id=post_id)
    c=Comment.objects.all().filter(post_id=p).order_by('path')
    # c.filter(child_comment!=None)

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:

        form = CommentForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            m=Comment(text=form.cleaned_data['text'],post_id=p,user_id=request.user)
            m.save()
            m.path=str(m.id)
            print(str(m.id))
            m.save()
            return render(request,'newspost/post.html',{'form': form,'post':p,'comments':c})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CommentForm()
    return render(request,'newspost/post.html',{'form': form,'post':p,'comments':c})


def upvote_comment(request,comment_id):
    c=Comment.objects.get(id=comment_id)
    c.comment_upvote.add(request.user)
    p=c.post_id
    return redirect('newspost:post',post_id=p.id)

def upvote_post(request,post_id):
    p=Post.objects.get(id=post_id)
    p.post_upvote.add(request.user)
    return redirect('newspost:post',post_id=p.id)

@login_required(login_url='newspost:login1')
def reply(request,comment_id):
    c=Comment.objects.get(id=comment_id)
    p=c.post_id
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CommentForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            m=Comment(text=form.cleaned_data['text'],post_id=p,user_id=request.user,level_count=c.level_count+1,parent_comment=c)
            m.save()
            m.path=c.path+'.'+str(m.id)
            m.save()
            c.save()

            # d=Comment.objects.filter(post_id=p).order_by('path')
        return redirect('newspost:post',post_id=p.id)

    else:
        form = CommentForm()
    return render(request,'newspost/reply.html',{'form': form,'post':p,'comments':c})

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
            m=Post(post_title=form.cleaned_data['post_title'],post_link=form.cleaned_data['post_link'],user_id=request.user)
            m.save()
            return post(request,m.id)

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
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            # user = User1.objects.create(username=form.cleaned_data['username'], password=form.cleaned_data['password1'], email=form.cleaned_data['email'])
            # user.save()
            # request.session['username'] = user.username
            print(form)
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            # user.set_password(password)
            # user.save()
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

