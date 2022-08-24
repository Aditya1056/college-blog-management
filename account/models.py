from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

IMPORTANCE = (
    ('High','High'),
    ('Medium','Medium'),
    ('Low','Low'),
)

BLOGTYPE = (
    ('Question','Question'),
    ('BlogPost','BlogPost'),
)

# Create your models here.


class Student(models.Model):

    user = models.OneToOneField(User, on_delete = models.CASCADE)

    name = models.CharField(max_length=255, blank=False, null= False)
    email = models.EmailField(max_length=255, blank=False,null=False,unique=True)

    registration_number = models.CharField(max_length=255, blank=False,null=False,unique=True)

    blogpost_count = models.IntegerField(default = 0)

    def __str__(self):
        return self.name


class Coordinator(models.Model):

    user = models.OneToOneField(User, on_delete = models.CASCADE)

    name = models.CharField(max_length=255, blank = False , null= False)
    email = models.EmailField(max_length=255, blank = False , null = False, unique = True)

    coordinator_number = models.CharField(max_length=255, blank = False, null = False, unique=True)

    blogpost_count = models.IntegerField(default = 0)

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    title = models.CharField(max_length=255, blank = False, null= False)
    content = models.TextField(blank = False, null = False)

    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)

    updated_time = models.DateTimeField(auto_now_add = True)

    importance = models.CharField(max_length=255, blank = True, choices = IMPORTANCE)

    blogtype = models.CharField(max_length = 255, blank = False, null = False, choices = BLOGTYPE)

    def __str__(self):
        return f"{self.title} --> {self.user.username}"


class Comment(models.Model):

    user= models.ForeignKey(User, on_delete= models.CASCADE)

    blogpost= models.ForeignKey(BlogPost, on_delete= models.CASCADE)

    content = models.TextField(blank = False, null= False)

    date = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return f"comment to {self.blogpost.id}"



class Voting(models.Model):

    user = models.ForeignKey(User, on_delete = models.CASCADE)

    blogpost = models.ForeignKey(BlogPost, on_delete = models.CASCADE)

    upvotable = models.BooleanField(default=True)

    downvotable = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} --> {self.blogpost.title}"








    



