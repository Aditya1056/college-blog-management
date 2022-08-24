from django import forms



from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import BlogPost


class StudentRegistrationForm(UserCreationForm):

    name = forms.CharField(max_length=255, required= True)
    email = forms.EmailField(max_length=255, required= True)

    registration_number = forms.CharField(max_length=255, required= True)

    class Meta:
        model= User
        fields = ('name', 'email', 'username', 'registration_number', 'password1','password2')



class CoordinatorRegistrationForm(UserCreationForm):

    name = forms.CharField(max_length=255, required= True)
    email = forms.EmailField(max_length=255, required= True)

    coordinator_number = forms.CharField(max_length=255, required= True)

    class Meta:
        model= User
        fields = ('name', 'email', 'username', 'coordinator_number', 'password1','password2')

class StudentNewBlogpostForm(forms.ModelForm):

    class Meta:
        model = BlogPost
        fields = ('title', 'content','blogtype')

class CoordinatorNewBlogpostForm(forms.ModelForm):

    class Meta:
        model = BlogPost
        fields = ('title','content','importance','blogtype')




