"""cobola URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from account.views import (renderCoordinatorRegisterView, renderHomeView,renderStudentRegisterView,renderLoginView,renderLogoutView,
renderCoordinatorRegisterView,renderAllBlogPostView,renderAllQuestionView,renderNewStudentBlogPostView,renderNewCoordinatorBlogPostView,
renderEditStudentBlogView,renderEditCoordinatorBlogView,renderBlogPostDeleteView,renderUpvoteView,renderDownvoteView,renderErrorPageView,
renderPostCommentView,renderDeleteCommentView,renderOwnProfileView,renderProfileView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',renderHomeView,name = 'home'),
    path('student_register/',renderStudentRegisterView, name= 'student-register'),
    path('login/',renderLoginView , name='login'),
    path('logout/',renderLogoutView, name='logout'),
    path('coordinator_register/',renderCoordinatorRegisterView, name='coordinator-register'),
    path('all_blogposts/',renderAllBlogPostView, name='all_blogposts'),
    path('all_questions/',renderAllQuestionView, name='all_questions'),
    path('createblogpoststudent/',renderNewStudentBlogPostView,name='student-new-blogpost'),
    path('createblogpostcoordinator/',renderNewCoordinatorBlogPostView,name='coordinator-new-blogpost'),
    path('editblogpoststudent/<str:blogpost_id>',renderEditStudentBlogView, name='blogpost-edit-student'),
    path('editblogpostcoordinator/<str:blogpost_id>',renderEditCoordinatorBlogView, name='blogpost-edit-coordinator'),
    path('deleteblogpost/<str:blogpost_id>',renderBlogPostDeleteView, name='delete-blogpost'),
    path('your_profile/', renderOwnProfileView, name='own-profile'),
    path('user_profile/<str:blogpost_id>',renderProfileView, name='profile'),
    path('upvoteblogpost/<str:blogpost_id>',renderUpvoteView, name='upvote'),
    path('downvoteblogpost/<str:blogpost_id>',renderDownvoteView, name='downvote'),
    path('question_comments/<str:question_id>',renderPostCommentView, name='post-comment'),
    path('delete_comment/<str:comment_id>',renderDeleteCommentView, name='delete-comment'),
    path('error/',renderErrorPageView,name='error'),

]
