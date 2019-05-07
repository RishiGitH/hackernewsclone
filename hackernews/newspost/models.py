from django.db import models
from django.contrib.auth.models import User


class User1(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    updated_at=models.DateTimeField(null=True)

class Post(models.Model):
    post_title=models.CharField(max_length=255)
    post_upvotes=models.IntegerField(default=0)
    post_link=models.URLField()
    post_upvote=models.ManyToManyField(User,blank=True,related_name='post_upvotes')
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post_title


class Comment(models.Model):
    text=models.CharField(max_length=1500)
    comment_upvotes=models.IntegerField(default=0)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    post_id=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='commented_post')
    comment_upvote=models.ManyToManyField(User,blank=True,related_name='comment_upvotes')
    timestamp = models.DateTimeField(auto_now_add=True)
    parent_comment=models.ForeignKey("self",on_delete=models.CASCADE,blank=True,null=True,related_name='reply')
    level_count=models.IntegerField(default=0)


    def __str__(self):
        return self.text

    def as_tree(self):
        reply = list(self.reply.all())
        branch = bool(reply)
        yield branch, self
        for child in reply:
            for next in child.as_tree():
                yield next
        yield branch, None




