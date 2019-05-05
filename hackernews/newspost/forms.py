# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import Comment,Post

from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=['username','email','password']

class UserCreationForm1(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm1, self).__init__(*args, **kwargs)

        self.fields['email'].required = True

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'email',)

class UserChangeForm1(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username','password')

class CommentForm(forms.ModelForm):

    class Meta:
        model=Comment
        fields=('text',)
class PostForm(forms.ModelForm):

    class Meta:
        model=Post
        fields=('post_title','post_link')
