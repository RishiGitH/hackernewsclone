from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404,  HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate
import bcrypt
from .models import User1,Post,Comment
from django.urls import reverse
from .forms import CommentForm,PostForm,UserCreationForm1,UserChangeForm1
from django.db.models import Q



def index(request):
    posts = Post.objects.all().order_by('timestamp')
    if request.session.get('username'):
        name_user=request.session.get('username')
        context={'username':name_user,'posts':posts}
        return render(request, 'newspost/index.html',context)
    else:
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
    p=Post.objects.get(id=post_id)
    c=Comment.objects.all().filter(post_id=p).order_by('path')
    # c.filter(child_comment!=None)

    # for i in c:
        # print(i.parent_comment)
    if(request.session.get('username')):
        name_user=request.session.get('username')
        user=User1.objects.get(username=name_user)
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = CommentForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                # ...
                # redirect to a new URL:
                m=Comment(text=form.cleaned_data['text'],post_id=p,user_id=user)
                m.save()
                m.path=str(m.id)
                print(str(m.id))
                m.save()
                return render(request,'newspost/post.html',{'user':user,'form': form,'post':p,'comments':c})

        # if a GET (or any other method) we'll create a blank form
        else:
            form = CommentForm()
        return render(request,'newspost/post.html',{'user':user,'form': form,'post':p,'comments':c})
    else:
        if request.method == 'POST':
            return redirect('newspost/register.html')
        else:
            form = CommentForm()
        return render(request,'newspost/post.html',{'form': form,'post':p,'comments':c})

def reply(request,comment_id):
    c=Comment.objects.get(id=comment_id)
    p=c.post_id
    if(request.session.get('username')):
        name_user=request.session.get('username')
        user=User1.objects.get(username=name_user)
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = CommentForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                m=Comment(text=form.cleaned_data['text'],post_id=p,user_id=user,level_count=c.level_count+1,parent_comment=c)
                m.save()
                m.path=c.path+'.'+str(m.id)
                m.save()
                c.save()

                # d=Comment.objects.filter(post_id=p).order_by('path')
            return redirect('newspost:post',post_id=p.id)

        else:
            form = CommentForm()
        return render(request,'newspost/reply.html',{'user':user,'form': form,'post':p,'comments':c})
    else:
        return redirect('newspost:registrationPage')

def addPost(request):
    if(request.session.get('username')):
        name_user=request.session.get('username')
        user=User1.objects.get(username=name_user)
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = PostForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                # ...
                # redirect to a new URL:
                m=Post(post_title=form.cleaned_data['post_title'],post_link=form.cleaned_data['post_link'],user_id=user)
                m.save()
                return post(request,m.id)

        # if a GET (or any other method) we'll create a blank form
        else:
            form = PostForm()
        return render(request,'newspost/addPost.html',{'user':user,'form': form})
    else:
        return redirect('newspost:registrationPage')



def register1(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UserCreationForm1(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            user = User1.objects.create(username=form.cleaned_data['username'], password=form.cleaned_data['password1'], email=form.cleaned_data['email'])
            user.save()
            request.session['username'] = user.username
            return index(request)
    else:
        form = UserCreationForm1()
    return render(request,'newspost/register1.html',{'form':form})

def login1(request):
    if request.method == 'POST':
        form = UserChangeForm1(request.POST)
        print(form)
        if (User1.objects.filter(email=form.cleaned_data['email']).exists()):
            user=User1.objects.filter(email=form.cleaned_data['email'])[0]
            print(form.cleaned_data['email'])
            if(user.password==form.cleaned_data['password']):
                request.session['username'] = user.username
                return index(request)
    form = UserChangeForm1()
    return render(request,'newspost/login.html',{'form':form})






def logout(request):
    del request.session['username']
    return index(request)

def register(request):
    # errors = User1.objects.validator(request.POST)
    # if len(errors):
    #     for tag, error in errors.iteritems():
    #         messages.error(request, error, extra_tags=tag)
    #     return redirect('registrationPage/')
    hashed_password = request.POST['password']
    user = User1.objects.create(username=request.POST['username'], password=hashed_password, email=request.POST['email'])
    user.save()
    request.session['username'] = user.username
    # name_user=request.session.get('username')
    # context={'username':name_user}
    # return render(request, 'newspost/index.html',context)
    return index(request)

def login(request):
    # if (User1.objects.filter(email=request.POST['email']).exists()):
    #     user = User1.objects.filter(email=request.POST['email'])[0]
    #     # print(user,request.POST['pass'].encode(),user.password.encode())
    #     #dataa = bcrypt.hashpw(request.POST['pass'].encode(), bcrypt.gensalt())
    #     #print("My passsssssssssssssssssss .............",dataa,user.password.encode())
    # try:
    if (User1.objects.filter(email=request.POST['email']).exists()):
        user=User1.objects.filter(email=request.POST['email'])[0]
        if(user.password==request.POST['password']):
            request.session['username'] = user.username
            # name_user=request.session.get('username')
            # context={'username':name_user}
            # return render(request, 'newspost/index.html',context)
            return index(request)
    print(request.POST['email'],request.POST['password'],check1,user.username)
    # except:
    #     pass
    # if (bcrypt.checkpw(request.POST['pass'].encode(), user.password.encode())):
    #     request.session['id'] = user.id
    #     return redirect('newspost:index')
    return redirect('registrationPage/')
