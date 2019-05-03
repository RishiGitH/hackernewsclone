from django.db import models
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import AbstractUserManager

# Create your models here.


# class UserManager1(AbstractUserManager):
#     def validator(self, postData):
#         errors = {}
#         if (postData['username'].isalpha()) == False:
#             if len(postData['username']) < 2:
#                 errors['username'] = "First name can not be shorter than 2 characters"

#         if len(postData['email']) == 0:
#             errors['email'] = "You must enter an email"

#         if len(postData['password']) < 8:
#             errors['password'] = "Password is too short!"

#         return errors

class User1(AbstractUser):
    # username = models.CharField(max_length=255)
    # email = models.CharField(max_length=255,unique=True)
    # password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    # objects = UserManager1()

    def __str__(self):
        return self.first_name

class Post(models.Model):
    post_title=models.CharField(max_length=255)
    post_is_upvoted=models.BooleanField(default=False)
    post_upvotes=models.IntegerField(default=0)
    post_link=models.URLField()
    user_id=models.ForeignKey(User1,on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def count1(self):
        c=Comment.objects.filter(id=id).count()
        return c


    def __str__(self):
        return self.post_title


class Comment(models.Model):
    text=models.CharField(max_length=1500)
    comment_is_upvoted=models.BooleanField(default=False)
    comment_upvotes=models.IntegerField(default=0)
    user_id=models.ForeignKey(User1,on_delete=models.CASCADE)
    post_id=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='commented_post')
    timestamp = models.DateTimeField(auto_now_add=True)
    parent_comment=models.ForeignKey("self",on_delete=models.CASCADE,null=True,related_name='reply')
    level_count=models.IntegerField(default=0)
    path=models.CharField(max_length=1500)


    def __str__(self):
        return self.text
