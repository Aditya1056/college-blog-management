from django.contrib import admin

from .models import Student,Coordinator,BlogPost, Comment, Voting

# Register your models here.

admin.site.register(Student)

admin.site.register(Coordinator)

admin.site.register(BlogPost)

admin.site.register(Comment)

admin.site.register(Voting)
