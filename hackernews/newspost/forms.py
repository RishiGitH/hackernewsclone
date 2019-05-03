# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import User1,Comment,Post

class UserCreationForm1(UserCreationForm):

    class Meta(UserCreationForm):
        model = User1
        fields = ('username', 'email')

class UserChangeForm1(forms.ModelForm):
    class Meta:
        model = User1
        fields = ('email','password',)

class CommentForm(forms.ModelForm):

    class Meta:
        model=Comment
        fields=('text',)
class PostForm(forms.ModelForm):

    class Meta:
        model=Post
        fields=('post_title','post_link')
