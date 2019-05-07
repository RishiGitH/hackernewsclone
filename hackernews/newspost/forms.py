# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Comment,Post

from django.contrib.auth.models import User


class UserCreationForm1(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm1, self).__init__(*args, **kwargs)

        self.fields['email'].required = True

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'email',)


class CommentForm(forms.ModelForm):

    class Meta:
        model=Comment
        fields=('text',)
class PostForm(forms.ModelForm):

    class Meta:
        model=Post
        fields=('post_title','post_link')
