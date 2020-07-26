from django.db import models

class Users(models.Model):
    username = models.CharField(max_length=50,null=False,unique=True)
    password = models.CharField(max_length=50,null=False)
    email = models.EmailField(max_length=80,null=False,unique=True)
    datetime = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images',blank=True,null=False)

class Posts(models.Model):
    title = models.CharField(null=False,max_length=50)
    tags = models.CharField(null=False,max_length=50,default='No tags')
    body = models.TextField(null=False)
    author = models.ForeignKey('Users',on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(upload_to='thumbnails',blank=True,null=False)

class Comments(models.Model):
    body = models.TextField(null=False)
    author = models.ForeignKey('Users',on_delete=models.CASCADE)
    posts = models.ForeignKey('Posts',on_delete=models.CASCADE,default=None)
    timestamp = models.DateTimeField(auto_now_add=True)

class Postlike(models.Model):
    user = models.ForeignKey('Users',on_delete=models.CASCADE)
    post = models.ForeignKey('Posts',on_delete=models.CASCADE)

class Commentlike(models.Model):
    user = models.ForeignKey('Users',on_delete=models.CASCADE)
    comment = models.ForeignKey('Comments',on_delete=models.CASCADE)

class Polls(models.Model):
    question = models.TextField(null=False)
    choice1 = models.CharField(max_length=50,null=False)
    choice2 = models.CharField(max_length=50,null=False)
    choice1_total = models.IntegerField(null=False,default=0)
    choice2_total = models.IntegerField(null=False,default=0)
    owner = models.ForeignKey('Users',on_delete=models.CASCADE)

class PollVote(models.Model):
    user = models.ForeignKey('Users',on_delete=models.CASCADE)
    poll = models.ForeignKey('Polls',on_delete=models.CASCADE)
