from django.db import models
from django.contrib.auth.models import User
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

# class User1(AbstractUser):
#     # username = models.CharField(max_length=255)
#     # email = models.CharField(max_length=255,unique=True)
#     # password = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add = True)
#     updated_at = models.DateTimeField(auto_now = True)
#     # objects = UserManager1()

#     def __str__(self):
#         return self.first_name

class Post(models.Model):
    post_title=models.CharField(max_length=255)
    post_upvotes=models.IntegerField(default=0)
    post_link=models.URLField()
    post_upvote=models.ManyToManyField(User,blank=True,related_name='post_upvotes')
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    # def count1(self):
    #     c=Comment.objects.filter(id=id).count()
    #     return c


    def __str__(self):
        return self.post_title


class Comment(models.Model):
    text=models.CharField(max_length=1500)
    comment_upvotes=models.IntegerField(default=0)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    post_id=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='commented_post')
    comment_upvote=models.ManyToManyField(User,blank=True,related_name='comment_upvotes')
    timestamp = models.DateTimeField(auto_now_add=True)
    parent_comment=models.ForeignKey("self",on_delete=models.CASCADE,null=True,related_name='reply')
    level_count=models.IntegerField(default=0)
    path=models.CharField(max_length=1500)

    # def upvotes_count(self):
    #     count=Upvote.objects.filter(comment=)

    def __str__(self):
        return self.text


class RecursiveThing(models.Model):

    name = models.CharField(max_length=32)
    parent = models.ForeignKey('self', related_name='children', blank=True, null=True,on_delete=models.CASCADE)

    def as_tree(self):
        children = list(self.children.all())
        branch = bool(children)
        yield branch, self
        for child in children:
            for next in child.as_tree():
                yield next
        yield branch, None


class Upvote_Comment(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    comment_id=models.ForeignKey(Comment,on_delete=models.CASCADE)

    def __str__(self):
        return self.user_id+self.comment_id

class Upvote_Post(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    post_id=models.ForeignKey(Post,on_delete=models.CASCADE)

    def __str__(self):
        return self.user_id+self.post_id
