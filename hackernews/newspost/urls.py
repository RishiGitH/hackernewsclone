from django.conf.urls import url
from . import views
from django.urls import path
from django.views.generic import RedirectView

app_name='newspost'
urlpatterns = [
    path('',views.index,name='index'),
    # path('register',views.register),
    path('lazy_load_posts/', views.lazy_load_posts, name='lazy_load_posts'),
    path('logout1/',views.logout1,name='logout1'),
    path('<int:post_id>/',views.post,name='post'),
    path('allcomment',views.allcomment,name='allcomment'),
    path('addPost',views.addPost,name='addPost'),
    path('reply',views.reply,name='reply'),
    path('post_comment',views.post_comment,name='post_comment'),
    path('search',views.search,name='search'),
    path('register1',views.register1,name='register1'),
    path('login1',views.login1,name='login1'),
    path('upvote_p/', views.upvote_p, name='upvote_p'),
    path('upvote_c/', views.upvote_c, name='upvote_c'),
    url(r'^favicon\.ico$',RedirectView.as_view(url='/static/favicon.ico')),

]
