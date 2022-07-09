from django.urls import path
from blogapp import views
urlpatterns=[
    path("accounts/signup", views.SignUpView.as_view(), name="signup"),
    path('accounts/login', views.LoginView.as_view(), name="login"),
    path('home',views.IndexView.as_view(),name="home"),
    path("users/profile/add",views.CreateUserProfileView.as_view(),name="add-profile"),
    path("users/profile",views.ViewProfileView.as_view(),name="view-profile"),
    path("users/password/new",views.PasswordResetView.as_view(),name="reset_password"),
    path("users/profile/change/<int:user_id>",views.ProfileUpdateView.as_view(),name="profile-update"),
    path("users/profile/changepic/<int:user_id>",views.ChangeProfilePicView.as_view(),name="profile-pic"),
    path("post/comment/<int:post_id>",views.add_comment,name="add-comment"),
    path('post/like/add/<int:post_id>',views.add_like,name='add-like')
    ]