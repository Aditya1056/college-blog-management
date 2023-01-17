from re import S
from django.shortcuts import render,redirect

from django.contrib.auth.models import User,Group

from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.decorators import login_required

from django.template.defaulttags import register

from .models import Student,Coordinator,BlogPost,Voting,Comment

from django.contrib import messages

from django.utils import timezone

APP_NAME = 'account'

# Create your views here.

from .forms import CoordinatorRegistrationForm, StudentRegistrationForm,StudentNewBlogpostForm,CoordinatorNewBlogpostForm


@register.filter
def isStudent(user):
    if user.groups.exists():
        if user.groups.all()[0].name == 'student':
            return True

    return False

@register.filter
def isCoordinator(user):
    if user.groups.exists():
        if user.groups.all()[0].name == 'coordinator':
            return True

    return False


def renderHomeView(request):
    context ={}
    if request.user.is_authenticated:
        user_blogposts = BlogPost.objects.filter(user = request.user)
        context['user_blogposts'] = user_blogposts
        print("logged in")
    else:
        print("logged out")
    

    return render(request, APP_NAME + '/home.html',context)


def renderStudentRegisterView(request):

    if request.user.is_authenticated:
        return redirect('home')


    context={}

    if request.method == 'POST':
        studentregistrationform = StudentRegistrationForm(request.POST)

        if studentregistrationform.is_valid():

            #create a User object

            new_user = User.objects.create_user(
                username = studentregistrationform.cleaned_data['username'],
                email = studentregistrationform.cleaned_data['email'],
                password = studentregistrationform.cleaned_data['password1'],

            )
            new_user.groups.add(Group.objects.get(name = 'student'))

            # create a voting objects for existing blogpost with new user

            blogposts = BlogPost.objects.all()

            for blogpost in blogposts:
                voting  = Voting.objects.create(
                    user = new_user,
                    blogpost = blogpost,
                )


            #create a Student object

            student = Student.objects.create(
                user = new_user,
                name = studentregistrationform.cleaned_data['name'],
                email = new_user.email,
                registration_number = studentregistrationform.cleaned_data['registration_number'],
            )

            print(f"student {student} created successfully")

            return redirect('home')

        else:

            messages.error(request, "Enter The Valid Student Details!")
            return redirect('student-register')

    else:
        studentregistrationform = StudentRegistrationForm()
        context['studentregistrationform'] = studentregistrationform
        # print(studentregistrationform)
        return render(request, APP_NAME + '/student_register.html',context)



def renderCoordinatorRegisterView(request):

    if request.user.is_authenticated:
        return redirect('home')

    context={}
    if request.method == 'POST':
        coordinatorregistrationform = CoordinatorRegistrationForm(request.POST)

        if coordinatorregistrationform.is_valid():

            #create a User object

            new_user = User.objects.create_user(
                username = coordinatorregistrationform.cleaned_data['username'],
                email = coordinatorregistrationform.cleaned_data['email'],
                password = coordinatorregistrationform.cleaned_data['password1'],

            )
            new_user.groups.add(Group.objects.get(name = 'coordinator'))

            # create a voting objects for existing blogpost with new user

            blogposts = BlogPost.objects.all()

            for blogpost in blogposts:
                voting  = Voting.objects.create(
                    user = new_user,
                    blogpost = blogpost,
                )

            #create a Student object

            coordinator = Coordinator.objects.create(
                user = new_user,
                name = coordinatorregistrationform.cleaned_data['name'],
                email = new_user.email,
                coordinator_number = coordinatorregistrationform.cleaned_data['coordinator_number'],
            )

            print(f"coordinator  {coordinator} created successfully")

            return redirect('home')

        else:

            messages.error(request, "Enter The Valid Coorinator Details!")

            print(coordinatorregistrationform.errors)

            return redirect('coordinator-register')
        
    else:
        coordinatorregistrationform = CoordinatorRegistrationForm() 
        context['coordinatorregistrationform'] = coordinatorregistrationform
        # print(coordinatorregistrationform)
        return render(request, APP_NAME + '/coordinator_register.html',context)



def renderLoginView(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"{username} {password}")
        user = authenticate(request, username = username, password= password)
        if user is None:
            messages.error(request, "Invalid username/password")
            return redirect('login')
        else:
            login(request,user)

            return redirect('home')

    else:
        return render(request, APP_NAME + '/login.html')



def renderLogoutView(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect('home')


def renderErrorPageView(request):
    return render(request, APP_NAME + '/error_page.html')


def renderAllBlogPostView(request):
    context = {}

    blogposts = BlogPost.objects.filter(blogtype = 'BlogPost')

    context ['blogposts'] = blogposts
    if request.user.is_authenticated:

        user = request.user

        upvotables,downvotables = [],[]

        for blogpost in blogposts:

            try:
                voting = Voting.objects.get(user = user, blogpost = blogpost)
            except Voting.DoesNotExist:
                print('voting not found')
                return redirect('error')
            
            upvotables.append(voting.upvotable)
            downvotables.append(voting.downvotable)

        print(upvotables)
        print(downvotables)

        blogposts_votes = zip(blogposts, upvotables, downvotables)

        # zip can only be unzipped once

        context['blogposts_votes'] = blogposts_votes

        request.session['clicked_from'] = 'blogposts_page'
            

    return render(request, APP_NAME + '/all_blogposts.html',context)



def renderAllQuestionView(request):
    context={}

    questions = BlogPost.objects.filter(blogtype = 'Question')

    question_comments = {}

    for question in questions:
        comments = Comment.objects.filter(blogpost = question)
        question_comments[question] = comments
    context['question_comments'] = question_comments


    if request.user.is_authenticated:
        
        user = request.user

        upvotables,downvotables,comments_list = [],[],[]

        for question in questions:

            try:
                voting = Voting.objects.get(user = user, blogpost = question)
            except Voting.DoesNotExist:
                print('voting not found')
                return redirect('error')
            
            upvotables.append(voting.upvotable)
            downvotables.append(voting.downvotable)

            comments = Comment.objects.filter(blogpost = question)
            comments_list.append(comments)


        print(upvotables)
        print(downvotables)
        print(comments)

        questions_votes = zip(questions, upvotables, downvotables, comments_list)

        # zip can only be unzipped once

        context['questions_votes'] = questions_votes

        request.session['clicked_from'] = 'questions_page'
            

    return render(request, APP_NAME + '/all_questions.html',context)



@login_required(login_url='login')
def renderOwnProfileView(request):
    context={}

    if request.user.is_authenticated:
        user = request.user

        if isStudent(user):
            try:
                own_profile = Student.objects.get(user = user)
            except Student.DoesNotExist:
                return redirect('error')
        if isCoordinator(user):
            try:
                own_profile = Coordinator.objects.get(user = user)
            except Coordinator.DoesNotExist:
                return redirect('error')
        context['own_profile'] = own_profile
            
        return render(request, APP_NAME + '/own_profile.html', context)




@login_required(login_url= 'login')
def renderProfileView(request, blogpost_id):
    context = {}
    if request.user.is_authenticated:
        try:
            blogpost = BlogPost.objects.get(id = blogpost_id)
        except BlogPost.DoesNotExist:
            return redirect('error')

        if isStudent(blogpost.user):
            try:
                profile = Student.objects.get(user = blogpost.user)
            except Student.DoesNotExist:
                return redirect('error')

        if isCoordinator(blogpost.user):
            try:
                profile = Coordinator.objects.get(user = blogpost.user)
            except Coordinator.DoesNotExist:
                return redirect('error')      

        context['profile'] = profile

        return render(request, APP_NAME + '/profile.html', context)




@login_required(login_url='login')
def renderNewStudentBlogPostView(request):
    context = {}

    if isCoordinator(request.user):
        return redirect('error')



    if request.method == 'POST':
        studentblogpostform = StudentNewBlogpostForm(request.POST)
        if studentblogpostform.is_valid():

            #create a new student blog post

            new_blogpost = BlogPost.objects.create(
                user = request.user,
                title = studentblogpostform.cleaned_data['title'],
                content = studentblogpostform.cleaned_data['content'],
                blogtype = studentblogpostform.cleaned_data['blogtype'],
            )

            request.user.student.blogpost_count += 1

            request.user.student.save()

            # create voting objects for every existing user and new blogpost

            users = User.objects.all()

            for user in users:
                voting = Voting.objects.create(
                    user = user,
                    blogpost = new_blogpost,

                )

            return redirect('home')
    else:
        studentblogpostform = StudentNewBlogpostForm()
        print(studentblogpostform)
        context['studentblogpostform'] = studentblogpostform
        return render(request, APP_NAME + '/student_newblogpost.html',context)


@login_required(login_url='login')
def renderNewCoordinatorBlogPostView(request):
    context = {}

    if isStudent(request.user):
        return redirect('error')

    if request.method == 'POST':
        coordinatorblogpostform = CoordinatorNewBlogpostForm(request.POST)
        if coordinatorblogpostform.is_valid():

        #create a new coordinator blog post


            new_blogpost = BlogPost.objects.create(
                user = request.user,
                title = coordinatorblogpostform.cleaned_data['title'],
                content = coordinatorblogpostform.cleaned_data['content'],
                importance = coordinatorblogpostform.cleaned_data['importance'],
                blogtype = coordinatorblogpostform.cleaned_data['blogtype'],
            )

            request.user.coordinator.blogpost_count += 1

            request.user.coordinator.save()

            # create voting objects for every existing user and new blogpost

            users = User.objects.all()

            for user in users:
                voting = Voting.objects.create(
                    user = user,
                    blogpost = new_blogpost,
                    
                )

            return redirect('home')
    else:
        coordinatorblogpostform = CoordinatorNewBlogpostForm()
        print(coordinatorblogpostform)
        context['coordinatorblogpostform'] = coordinatorblogpostform
        return render(request, APP_NAME + '/coordinator_newblogpost.html',context)




@login_required(login_url='login')
def renderEditStudentBlogView(request,blogpost_id):
    context={}

    if isCoordinator(request.user):
        return redirect('error')

    try:
        blogpost = BlogPost.objects.get(id = blogpost_id)
    except:
        print("blogpost not found")
        return redirect('error')

    # allow only this blogpost user

    if blogpost.user != request.user:
        return redirect('error')

    if request.method =='POST':
        studentblogpostform = StudentNewBlogpostForm(request.POST)
        if studentblogpostform.is_valid():
            blogpost.title = studentblogpostform.cleaned_data['title']
            blogpost.content = studentblogpostform.cleaned_data['content']
            blogpost.blogtype = studentblogpostform.cleaned_data['blogtype']
            blogpost.updated_time = timezone.now()

            blogpost.save()

            return redirect('home')

    else:
        studentblogeditform = StudentNewBlogpostForm(
            initial={
                'title':blogpost.title,
                'content':blogpost.content,
                'blogtype':blogpost.blogtype,
            }
        )
        context['studentblogeditform'] = studentblogeditform
        return render(request, APP_NAME + '/edit_student_blogpost.html',context)





@login_required(login_url='login')
def renderEditCoordinatorBlogView(request,blogpost_id):
    context={}

    if isStudent(request.user):
        return redirect('error')
    
    try:
        blogpost = BlogPost.objects.get(id = blogpost_id)
    except:
        print("blogpost not found")
        return redirect('error')

    # allow only this blogpost user

    if blogpost.user != request.user:
        return redirect('error')

    if request.method =='POST':
        coordinatorblogpostform = CoordinatorNewBlogpostForm(request.POST)
        if coordinatorblogpostform.is_valid():
            blogpost.title = coordinatorblogpostform.cleaned_data['title']
            blogpost.content = coordinatorblogpostform.cleaned_data['content']
            blogpost.importance = coordinatorblogpostform.cleaned_data['importance']
            blogpost.blogtype = coordinatorblogpostform.cleaned_data['blogtype']
            blogpost.updated_time = timezone.now()

            blogpost.save()

            return redirect('home')
    else:
        coordinatorblogeditform = CoordinatorNewBlogpostForm(
            initial={
                'title':blogpost.title,
                'content':blogpost.content,
                'importance':blogpost.importance,
                'blogtype':blogpost.blogtype,
            }
        )
        context['coordinatorblogeditform'] = coordinatorblogeditform
        return render(request, APP_NAME + '/edit_coordinator_blogpost.html',context)



@login_required(login_url='login')
def renderBlogPostDeleteView(request,blogpost_id):
    context={}
    try:
        blogpost = BlogPost.objects.get(id= blogpost_id)
    except:
        print('BlogPost not found')
        return redirect('error')

    # allow only this blogpost user

    if blogpost.user != request.user:
        return redirect('error')

    blogpost.delete()

    if isStudent(request.user):
        request.user.student.blogpost_count-=1
        request.user.student.save()

    if isCoordinator(request.user):
        request.user.coordinator.blogpost_count-=1;
        request.user.coordinator.save()



    return redirect('home')


    
@login_required(login_url = 'login')
def renderUpvoteView(request, blogpost_id):

    user = request.user
    try:
        blogpost = BlogPost.objects.get(id= blogpost_id)
        voting = Voting.objects.get(user= user, blogpost = blogpost)
    except (BlogPost.DoesNotExist, Voting.DoesNotExist):
        print('BlogPost Or Voting not found')
        return redirect('error')

    voting.upvotable = False
    if not voting.downvotable:
        blogpost.downvotes -=1
    voting.downvotable = True

    voting.save()

    blogpost.upvotes +=1
    blogpost.save()

    if request.session['clicked_from'] == 'blogposts_page':
        return redirect('all_blogposts')
    else:
        return redirect('all_questions')



@login_required(login_url = 'login')
def renderDownvoteView(request, blogpost_id):

    user = request.user
    try:
        blogpost = BlogPost.objects.get(id= blogpost_id)
        voting = Voting.objects.get(user= user, blogpost = blogpost)
    except (BlogPost.DoesNotExist, Voting.DoesNotExist):
        print('BlogPost Or Voting not found')
        return redirect('error')

    voting.downvotable = False
    if not voting.upvotable:
        blogpost.upvotes -=1
    voting.upvotable = True

    voting.save()

    blogpost.downvotes +=1
    blogpost.save()

    if request.session['clicked_from'] == 'blogposts_page':
        return redirect('all_blogposts')
    else:
        return redirect('all_questions')

@login_required(login_url= 'login')
def renderPostCommentView(request, question_id):

    user = request.user
    try:
        question = BlogPost.objects.get(id = question_id)
    except BlogPost.DoesNotExist:
        print('Question Post Not Found')
        return redirect('error')
    
    if request.method == 'POST':

        content = request.POST.get('comment')

        new_comment = Comment.objects.create(
            user = user,
            blogpost = question,
            content = content,
        )

        print("Comment created")

    return redirect('all_questions')



@login_required(login_url= 'login')
def renderDeleteCommentView(request, comment_id):

    try:
        comment = Comment.objects.get(id = comment_id)
    except Comment.DoesNotExist:
        print('Comment Post Not Found')
        return redirect('error')

    # allow only this blogpost user

    if comment.user != request.user:
        return redirect('error')

    comment.delete()

    return redirect('all_questions')

        







