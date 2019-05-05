from django.contrib import admin
# from django.contrib.auth import get_user_model
# from django.contrib.auth.admin import UserAdmin

# from .forms import UserCreationForm1, UserChangeForm1
from .models import Post,Comment

# class CustomUserAdmin(UserAdmin):
#     add_form = UserCreationForm1
#     model = User
#     list_display = ['email', 'username','password','created_at','updated_at']

admin.site.register(Post)
admin.site.register(Comment)



