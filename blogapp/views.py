from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render,redirect
# View
# creating a new object > form,model,template_name createView
# fetching a specific object
# fetching all objects
# deleting an object
# Create your views here.
from django.urls import reverse_lazy
from blogapp.forms import UserRegistranForm,LoginForm,UserProfileForm,PasswordResetForm,BlogForm,ChangeProfilePicForm,CommentsForm
from blogapp.models import UserProfile,Blogs,Comments
from django.contrib.auth.models import User
from django.views.generic import View,CreateView,FormView,TemplateView,UpdateView
class SignUpView(CreateView):
    form_class= UserRegistranForm
    template_name="registration.html"
    model=User
    success_url = reverse_lazy('login')
    # def get(self,request,*args,**kwargs):
    #     form=self.form_class()
    #     return render(request, self.template_name, {"form": form})
    # def post(self,request,*args,**kwargs):
    #     form=self.form_class(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request,"your profile has bees created successfully")
    #         return redirect("signup")
    #     else:
    #         messages.error(request, "profile creation failed")
    #         return render(request,self.template_name, {"form": form})
class LoginView(FormView):
    form_class=LoginForm
    template_name="login.html"
    model=User

    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("uname")
            pwd=form.cleaned_data.get("pw")
            user=authenticate(request,username=uname,password=pwd)
            if user:
                login(request,user)
                print("success")
                return redirect("home")
            else:
                messages.error(request,"invalied credentials")
                return render(request,self.template_name,{"form":form})
        return render(request,self.template_name,{"form":form})
class IndexView(CreateView):
    template_name="home.html"
    model = Blogs
    form_class = BlogForm
    success_url = reverse_lazy("home")
    def form_valid(self, form):
        form.instance.author=self.request.user
        self.object = form.save()
        messages.success(self.request, "post has been saved")
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        blogs=Blogs.objects.all().order_by("posted_date")
        context["blogs"]=blogs
        comment_form=CommentsForm()
        context["comment_form"]=comment_form
        return context


class CreateUserProfileView(CreateView):
    template_name = "addprofile.html"
    model = UserProfile
    form_class = UserProfileForm
    success_url = reverse_lazy("home")
    def form_valid(self, form):
        form.instance.user=self.request.user
        messages.success(self.request,"profile has been created")
        self.object=form.save()
        return super().form_valid(form)
    # def post(self, request, *args, **kwargs):
    #     form=self.form_class(request.POST,files=request.FILES)
    #     if form.is_valid():
    #         form.instance.user=request.user
    #         form.save()
    #         messages.success(request,"success")
    #         return redirect("home")
    #     else:
    #         return render()
class ViewProfileView(TemplateView):
    template_name = "view-profile.html"

class PasswordResetView(FormView):
    template_name = "passwordreset.html"
    form_class = PasswordResetForm
    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            oldpassword=form.cleaned_data.get("old_password")
            password1=form.cleaned_data.get("new_password")
            password2=form.cleaned_data.get("confirm_password")
            user = authenticate(request, username=request.user.username, password=oldpassword)
            if user:
                if password1==password2:
                    user.set_password(password2)
                    user.save()
                    messages.success(request,"password changed")
                    return redirect("login")
                else:
                    messages.error(request,"password entered is not match")
                    return render(request, self.template_name, {"form": form})
            else:
                messages.error(request,"error")
                return render(request,self.template_name,{"form":form})
class ProfileUpdateView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = "profile-update.html"
    success_url = reverse_lazy("home")
    pk_url_kwarg = "user_id"
    def form_valid(self, form):
        messages.success(self.request,"your profile has been successfully updated")
        self.object=form.save()
        return super().form_valid(form)

class ChangeProfilePicView(UpdateView):
    model = UserProfile
    template_name = "change-profilepic.html"
    form_class = ChangeProfilePicForm
    success_url = reverse_lazy("home")
    pk_url_kwarg = "user_id"
    def form_valid(self, form):
        messages.success(self.request, "your profile pic has been successfully updated")
        self.object = form.save()
        return super().form_valid(form)

def add_comment(request,*args,**kwargs):
    if request.method=='POST':
        blog_id=kwargs.get('post_id')
        blog=Blogs.objects.get(id=blog_id)
        user=request.user
        comment=request.POST.get('comment')
        Comments.objects.create(blog=blog,comment=comment,user=user)
        messages.success(request,"comment has been posted")
        return redirect("home")

def add_like(request,*args,**kwargs):
    blog_id=kwargs.get("post_id")
    blog=Blogs.objects.get(id=blog_id)

    blog.liked_by.add(request.user)
    blog.save()
    return redirect("home")
