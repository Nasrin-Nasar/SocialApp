from django.contrib.auth.models import User
from django import forms
from blogapp.models import UserProfile,Blogs,Comments
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
class UserRegistranForm(UserCreationForm):
    class Meta:
        model=User
        fields=["first_name","last_name","username","email","password1","password2"]
class LoginForm(forms.Form):
    uname=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}),label="Username")
    pw = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}),label="Password")


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ("user",)
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"class":"form-control","type":"date"})
        }
class PasswordResetForm(forms.Form):
    old_password=forms.CharField(widget=forms.PasswordInput)
    new_password=forms.CharField(widget=forms.PasswordInput)
    confirm_password=forms.CharField()
class ChangeProfilePicForm(ModelForm):
    class Meta:
        model=UserProfile
        fields=["profile_pic"]
        widgets={
            "profile_pic":forms.FileInput(attrs={"class":"form-control"})
        }

class BlogForm(ModelForm):
    class Meta:
        model=Blogs
        fields=["title","description","image"]
        widgets={
            "title":forms.TextInput(attrs={"class":"form-control"}),
            "description":forms.Textarea(attrs={"class":"form-control"}),
            "image":forms.FileInput(attrs={"class":"form-control"})
        }
class CommentsForm(ModelForm):
    class Meta:
        model=Comments
        fields=["comment"]
        widgets={
            "comment":forms.TextInput(attrs={"class":"form-control"})
        }

