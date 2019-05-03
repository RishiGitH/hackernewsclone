from django.conf.urls import url
from . import views
from django.urls import path
app_name='newspost'
urlpatterns = [
    path('',views.index,name='index'),
    # path('register',views.register),
    path('logout/',views.logout,name='logout'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('<int:post_id>/',views.post,name='post'),
    path('addPost',views.addPost,name='addPost'),
    path('reply/<int:comment_id>/',views.reply,name='reply'),
    path('search',views.search,name='search'),
    path('register1',views.register1,name='register1'),
    path('login1',views.login1,name='login1'),
]
